"""Calendar sync routes with background task processing."""

import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.google_account import GoogleAccount
from app.models.affirmation import Affirmation
from app.models.calendar_event import CalendarEvent
from app.services.google_calendar import GoogleCalendarService
from app.services.affirmation_generator import generate_year_affirmations

router = APIRouter(prefix="/calendar", tags=["Calendar"])


class CalendarSyncRequest(BaseModel):
    year: Optional[int] = None
    calendar_id: Optional[str] = None
    timezone: str = "UTC"
    all_day: bool = True


def _sync_affirmations_task(
    user_id: int,
    year: int,
    calendar_id: str,
    timezone: str,
    all_day: bool,
):
    """Background task: generate affirmations and sync to Google Calendar.

    CRITICAL: Creates its own database session. Never pass request sessions
    to background tasks.

    The Google Calendar event is created BEFORE the local Affirmation row, so
    a permanent API failure never leaves an orphan affirmation that would
    later collide with the (user_id, date) unique constraint.
    """
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        account = (
            db.query(GoogleAccount)
            .filter(GoogleAccount.user_id == user_id)
            .first()
        )

        if not account:
            print(f"[User {user_id}] No Google account connected. Aborting sync.")
            return

        calendar_service = GoogleCalendarService(account, db)

        try:
            calendar_service.verify_access()
        except Exception as exc:
            print(f"[User {user_id}] Cannot access Google Calendar: {exc}")
            return

        affirmations = generate_year_affirmations(year)
        synced = 0
        failed = 0

        for item in affirmations:
            existing_aff = (
                db.query(Affirmation)
                .filter(
                    Affirmation.user_id == user_id,
                    Affirmation.affirmation_date == item["date"],
                )
                .first()
            )

            # Already fully synced for this date.
            if existing_aff and existing_aff.calendar_event:
                continue

            # Create the calendar event first (with retry/backoff).
            event = None
            for attempt in range(3):
                try:
                    event = calendar_service.create_daily_affirmation_event(
                        calendar_id=calendar_id,
                        event_date=item["date"],
                        title="Daily Affirmation",
                        description=item["text"],
                        timezone=timezone,
                        all_day=all_day,
                    )
                    break
                except Exception as exc:
                    if attempt == 2:
                        failed += 1
                        print(f"[User {user_id}] Permanent failure for {item['date']}: {exc}")
                    else:
                        time.sleep(2 ** attempt)

            if event is None:
                continue

            # Reuse an orphan affirmation if present, otherwise create one.
            affirmation = existing_aff or Affirmation(
                user_id=user_id,
                affirmation_date=item["date"],
                text=item["text"],
                theme=item["theme"],
            )
            if existing_aff is None:
                db.add(affirmation)
                db.flush()

            link = CalendarEvent(
                user_id=user_id,
                affirmation_id=affirmation.id,
                google_event_id=event.get("id"),
                calendar_id=calendar_id,
                status="synced",
            )
            db.add(link)
            db.commit()
            synced += 1

        print(f"[User {user_id}] Sync complete: {synced} created, {failed} failed")

    except Exception as exc:
        print(f"[User {user_id}] Unhandled sync error: {exc}")
        db.rollback()
    finally:
        db.close()


@router.post("/sync")
async def sync_calendar(
    background_tasks: BackgroundTasks,
    payload: Optional[CalendarSyncRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Kick off a full-year sync for the current user. Returns immediately;
    work continues in the background. Poll /calendar/status for progress."""
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.user_id == current_user.id)
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="Google account not connected")

    year = (payload.year if payload and payload.year else datetime.now(timezone.utc).year)
    calendar_id = (
        payload.calendar_id if payload and payload.calendar_id
        else (account.calendar_id or "primary")
    )
    tz = payload.timezone if payload else "UTC"
    all_day = payload.all_day if payload else True

    background_tasks.add_task(
        _sync_affirmations_task,
        current_user.id,
        year,
        calendar_id,
        tz,
        all_day,
    )

    return {
        "message": "Calendar sync started in background",
        "user_id": current_user.id,
        "year": year,
        "calendar_id": calendar_id,
        "status": "processing",
    }


@router.get("/status")
def sync_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check sync progress for the current user."""
    year = datetime.now(timezone.utc).year
    days_in_year = (datetime(year + 1, 1, 1) - datetime(year, 1, 1)).days

    total_affirmations = (
        db.query(Affirmation)
        .filter(Affirmation.user_id == current_user.id)
        .count()
    )
    synced_events = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == current_user.id)
        .count()
    )

    return {
        "user_id": current_user.id,
        "affirmations_generated": total_affirmations,
        "events_synced": synced_events,
        "progress_percent": (
            round((synced_events / days_in_year) * 100, 1) if days_in_year else 0
        ),
        "complete": synced_events >= days_in_year,
    }
