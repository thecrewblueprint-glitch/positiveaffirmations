"""Google Calendar API service with automatic token refresh."""

import time
from datetime import datetime, timedelta, date, timezone
from typing import Optional, Dict, Any, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request as GoogleRequest
from sqlalchemy.orm import Session

from app.models.google_account import GoogleAccount
from app.core.config import settings


class GoogleCalendarService:
    """Calendar service with automatic token refresh and rate limiting."""

    def __init__(self, account: GoogleAccount, db: Session):
        self.account = account
        self.db = db
        self._credentials: Optional[Credentials] = None
        self._service: Optional[Any] = None

    def _build_credentials(self) -> Credentials:
        """Create Credentials from stored tokens."""
        return Credentials(
            token=self.account.access_token,
            refresh_token=self.account.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/calendar.events"],
        )

    def _is_token_expired(self) -> bool:
        """Check if token expires within 5 minutes (clock skew buffer)."""
        if not self.account.token_expiry:
            return True
        try:
            expiry = datetime.fromisoformat(self.account.token_expiry)
            return datetime.now(timezone.utc) >= (expiry - timedelta(minutes=5))
        except ValueError:
            return True

    def _refresh_if_needed(self) -> Credentials:
        """Return valid credentials, refreshing automatically if expired."""
        credentials = self._build_credentials()

        if self._is_token_expired() and credentials.refresh_token:
            try:
                credentials.refresh(GoogleRequest())
                self.account.access_token = credentials.token
                self.account.token_expiry = (
                    credentials.expiry.isoformat() if credentials.expiry else None
                )
                self.db.commit()
            except Exception as exc:
                raise RuntimeError(f"Failed to refresh Google token: {exc}") from exc

        self._credentials = credentials
        return credentials

    def _get_service(self):
        """Lazy-init Calendar API service with fresh credentials."""
        if self._service is None:
            credentials = self._refresh_if_needed()
            self._service = build("calendar", "v3", credentials=credentials)
        return self._service

    def list_calendars(self) -> Dict[str, Any]:
        """List calendars accessible to the user."""
        return self._get_service().calendarList().list().execute()

    def create_daily_affirmation_event(
        self,
        calendar_id: str,
        event_date: date,
        title: str,
        description: str,
        timezone: str = "UTC",
        all_day: bool = True,
    ) -> Dict[str, Any]:
        """Create a single calendar event. Auto-refreshes token if needed."""
        body = {"summary": title, "description": description}

        if all_day:
            body["start"] = {"date": event_date.isoformat()}
            body["end"] = {"date": (event_date + timedelta(days=1)).isoformat()}
        else:
            start_dt = datetime.combine(event_date, datetime.min.time())
            end_dt = start_dt + timedelta(minutes=15)
            body["start"] = {"dateTime": start_dt.isoformat(), "timeZone": timezone}
            body["end"] = {"dateTime": end_dt.isoformat(), "timeZone": timezone}

        try:
            return self._get_service().events().insert(
                calendarId=calendar_id,
                body=body,
                sendUpdates="none",
            ).execute()
        except HttpError as exc:
            raise RuntimeError(f"Google Calendar event creation failed: {exc}") from exc

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete a calendar event by Google event ID."""
        try:
            self._get_service().events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
        except HttpError as exc:
            raise RuntimeError(f"Google Calendar delete failed: {exc}") from exc

    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing calendar event."""
        try:
            service = self._get_service()
            event = service.events().get(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            if title is not None:
                event["summary"] = title
            if description is not None:
                event["description"] = description
            return service.events().update(
                calendarId=calendar_id, eventId=event_id, body=event
            ).execute()
        except HttpError as exc:
            raise RuntimeError(f"Google Calendar update failed: {exc}") from exc

    def batch_create_events(
        self,
        calendar_id: str,
        events_data: List[Dict[str, Any]],
        timezone: str = "UTC",
        all_day: bool = True,
    ) -> List[Dict[str, Any]]:
        """Create multiple events with rate limiting and progress tracking."""
        results: List[Dict] = []
        service = self._get_service()

        for idx, item in enumerate(events_data):
            if idx > 0 and idx % settings.BATCH_SIZE == 0:
                time.sleep(settings.GOOGLE_API_DELAY_MS / 1000)

            event = self.create_daily_affirmation_event(
                calendar_id=calendar_id,
                event_date=item["date"],
                title=item.get("title", "Daily Affirmation"),
                description=item["text"],
                timezone=timezone,
                all_day=all_day,
            )
            results.append({
                "date": item["date"],
                "google_event_id": event.get("id"),
                "status": "synced",
            })

        return results
