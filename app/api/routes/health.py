"""Health check and monitoring endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.google_account import GoogleAccount
from app.services.google_calendar import GoogleCalendarService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    """Basic liveness probe."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/calendar")
def calendar_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify Google Calendar token health for the current user."""
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.user_id == current_user.id)
        .first()
    )

    if not account:
        return {"status": "no_account", "message": "No Google account linked"}

    service = GoogleCalendarService(account, db)
    try:
        service.verify_access()
        token_was_refreshed = (
            service._credentials is not None
            and service._credentials.token != account.access_token
        )
        return {
            "status": "healthy",
            "token_refreshed": token_was_refreshed,
            "account_email": account.email,
        }
    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
            "account_email": account.email,
        }
