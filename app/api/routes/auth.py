"""Google OAuth authentication routes with JWT session issuance."""

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User
from app.models.google_account import GoogleAccount

router = APIRouter(prefix="/auth", tags=["Authentication"])

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def _get_flow(state: str | None = None) -> Flow:
    """Build Google OAuth flow from environment configuration."""
    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=SCOPES,
        state=state,
    )


@router.get("/google/start")
def google_auth_start(request: Request):
    """Initiate Google OAuth flow. Returns authorization URL."""
    flow = _get_flow()
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    return {"auth_url": auth_url, "state": state}


@router.get("/google/callback")
def google_auth_callback(
    request: Request,
    code: str,
    state: str | None = None,
    db: Session = Depends(get_db),
):
    """Handle Google's redirect: exchange code, upsert user, issue a session
    token, and redirect the browser back to the SPA with that token."""
    flow = _get_flow(state=state)
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    try:
        flow.fetch_token(code=code)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {exc}")

    credentials = flow.credentials
    service = build("oauth2", "v2", credentials=credentials)
    google_user = service.userinfo().get().execute()

    google_sub = google_user.get("id")
    email = google_user.get("email")
    name = google_user.get("name") or (email.split("@")[0] if email else "")

    if not google_sub or not email:
        raise HTTPException(status_code=400, detail="Incomplete Google profile")

    # Upsert User
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.flush()

    # Upsert Google Account
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.google_sub == google_sub)
        .first()
    )

    token_expiry = credentials.expiry.isoformat() if credentials.expiry else None

    if account:
        account.access_token = credentials.token
        account.refresh_token = credentials.refresh_token or account.refresh_token
        account.token_expiry = token_expiry
        account.email = email
    else:
        account = GoogleAccount(
            user_id=user.id,
            google_sub=google_sub,
            email=email,
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_expiry=token_expiry,
            calendar_id="primary",
        )
        db.add(account)

    db.commit()

    # Issue session token and hand the browser back to the SPA.
    session_token = create_access_token(user.id)
    redirect_url = f"{settings.FRONTEND_URL}/?token={session_token}"
    return RedirectResponse(url=redirect_url)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }


@router.post("/google/refresh")
def refresh_google_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Manually refresh the current user's Google access token."""
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.user_id == current_user.id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Google account not found")

    if not account.refresh_token:
        raise HTTPException(
            status_code=400,
            detail="No refresh token available. Re-authenticate with prompt=consent."
        )

    credentials = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES,
    )

    try:
        credentials.refresh(GoogleRequest())
        account.access_token = credentials.token
        account.token_expiry = credentials.expiry.isoformat() if credentials.expiry else None
        db.commit()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Token refresh failed: {exc}")

    return {"message": "Token refreshed", "user_id": current_user.id}


@router.delete("/google/disconnect")
def disconnect_google(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove the current user's Google linkage and revoke tokens with Google."""
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.user_id == current_user.id)
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="Google account not connected")

    # Revoke token with Google (best-effort)
    try:
        if account.access_token:
            httpx.post(
                "https://oauth2.googleapis.com/revoke",
                params={"token": account.access_token},
                headers={"content-type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
    except Exception:
        pass

    db.delete(account)
    db.commit()

    return {"message": "Google account disconnected", "user_id": current_user.id}
