"""Calendar sync routes with background task processing."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.google_account import GoogleAccount
from app.models.affirmation import Affirmation
from app.models.calendar_event import CalendarEvent
from app.services.google_calendar import GoogleCalendarService
from app.services.affirmation_generator import generate_year_affirmations

router = APIRouter(prefix="/calendar", tags=["Calendar"])


class CalendarSyncRequest(BaseModel):
    user_id: int
    year: int
    calendar_id: str = "primary"
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

    CRITICAL: Creates its own database session. Never pass sessions to background tasks.
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
            raise RuntimeError("Google account not connected")

        calendar_service = GoogleCalendarService(account, db)

        try:
            calendar_service.list_calendars()
        except Exception as exc:
            raise RuntimeError(f"Cannot access Google Calendar: {exc}")

        affirmations = generate_year_affirmations(year)
        synced = 0
        failed = 0

        for item in affirmations:
            existing = (
                db.query(CalendarEvent)
                .join(CalendarEvent.affirmation)
                .filter(
                    CalendarEvent.user_id == user_id,
                    Affirmation.affirmation_date == item["date"],
                )
                .first()
            )

            if existing:
                continue

            affirmation = Affirmation(
                user_id=user_id,
                affirmation_date=item["date"],
                text=item["text"],
                theme=item["theme"],
            )
            db.add(affirmation)
            db.flush()

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
                    break

                except Exception as exc:
                    if attempt == 2:
                        failed += 1
                        print(f"[User {user_id}] Permanent failure for {item['date']}: {exc}")
                    else:
                        import time
                        time.sleep(2 ** attempt)

        print(f"[User {user_id}] Sync complete: {synced} created, {failed} failed")

    except Exception as exc:
        print(f"[User {user_id}] Unhandled sync error: {exc}")
        db.rollback()
        raise

    finally:
        db.close()


@router.post("/sync")
async def sync_calendar(
    payload: CalendarSyncRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Kick off a full-year sync. Returns immediately; work continues in background.

    Frontend should poll /calendar/status/{user_id} for progress.
    """
    account = (
        db.query(GoogleAccount)
        .filter(GoogleAccount.user_id == payload.user_id)
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="Google account not connected")

    background_tasks.add_task(
        _sync_affirmations_task,
        payload.user_id,
        payload.year,
        payload.calendar_id,
        payload.timezone,
        payload.all_day,
    )

    return {
        "message": "Calendar sync started in background",
        "user_id": payload.user_id,
        "year": payload.year,
        "calendar_id": payload.calendar_id,
        "status": "processing",
    }


@router.get("/status/{user_id}")
def sync_status(user_id: int, db: Session = Depends(get_db)):
    """Check sync progress for a user."""
    total_affirmations = (
        db.query(Affirmation)
        .filter(Affirmation.user_id == user_id)
        .count()
    )
    synced_events = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == user_id)
        .count()
    )

    return {
        "user_id": user_id,
        "affirmations_generated": total_affirmations,
        "events_synced": synced_events,
        "progress_percent": round((synced_events / 365) * 100, 1) if total_affirmations > 0 else 0,
        "complete": synced_events >= 365,
    }
