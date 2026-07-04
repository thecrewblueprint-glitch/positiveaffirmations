"""APScheduler background worker for nightly affirmation sync.

Run as standalone process:
    python -m app.workers.scheduler

Production deployment:
    docker-compose up scheduler
"""

import logging
import signal
import sys
import time
from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.executors.pool import ThreadPoolExecutor

from app.db.session import SessionLocal
from app.models.google_account import GoogleAccount
from app.models.calendar_event import CalendarEvent
from app.models.affirmation import Affirmation
from app.services.google_calendar import GoogleCalendarService
from app.services.affirmation_generator import generate_year_affirmations
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("affirmation_scheduler")


class SyncJobRegistry:
    """Track job execution state for observability."""

    def __init__(self):
        self.last_run: Optional[datetime] = None
        self.last_status: Optional[str] = None
        self.events_synced_today: int = 0
        self.failures_today: int = 0

    def record_success(self, count: int):
        self.last_run = datetime.now(timezone.utc)
        self.last_status = "success"
        self.events_synced_today = count
        self.failures_today = 0

    def record_failure(self):
        self.last_run = datetime.now(timezone.utc)
        self.last_status = "failed"
        self.failures_today += 1


registry = SyncJobRegistry()


def sync_user_affirmations(user_id: int, year: Optional[int] = None) -> dict:
    """Sync affirmations for a single user."""
    db = SessionLocal()
    try:
        target_year = year or datetime.now(timezone.utc).year

        account = (
            db.query(GoogleAccount)
            .filter(GoogleAccount.user_id == user_id)
            .first()
        )

        if not account:
            logger.warning(f"[User {user_id}] No Google account linked. Skipping.")
            return {"user_id": user_id, "status": "skipped", "reason": "no_account"}

        existing_count = (
            db.query(CalendarEvent)
            .filter(CalendarEvent.user_id == user_id)
            .count()
        )

        if existing_count >= 365:
            logger.info(f"[User {user_id}] Already synced ({existing_count} events).")
            return {"user_id": user_id, "status": "skipped", "reason": "already_synced"}

        calendar_service = GoogleCalendarService(account, db)

        try:
            calendar_service.list_calendars()
        except Exception as exc:
            logger.error(f"[User {user_id}] Calendar access failed: {exc}")
            return {"user_id": user_id, "status": "failed", "reason": "calendar_unavailable"}

        affirmations = generate_year_affirmations(target_year)
        logger.info(f"[User {user_id}] Generated {len(affirmations)} affirmations")

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
                        calendar_id=account.calendar_id,
                        event_date=item["date"],
                        title="Daily Affirmation",
                        description=item["text"],
                        timezone="UTC",
                        all_day=True,
                    )

                    link = CalendarEvent(
                        user_id=user_id,
                        affirmation_id=affirmation.id,
                        google_event_id=event.get("id"),
                        calendar_id=account.calendar_id,
                        status="synced",
                    )
                    db.add(link)
                    db.commit()
                    synced += 1
                    break

                except Exception as exc:
                    logger.warning(
                        f"[User {user_id}] Attempt {attempt + 1}/3 failed for {item['date']}: {exc}"
                    )
                    if attempt == 2:
                        failed += 1
                        logger.error(
                            f"[User {user_id}] Permanent failure for {item['date']}: {exc}"
                        )
                    else:
                        time.sleep(2 ** attempt)

        registry.record_success(synced)
        logger.info(
            f"[User {user_id}] Sync complete: {synced} created, {failed} failed"
        )

        return {
            "user_id": user_id,
            "status": "success",
            "year": target_year,
            "synced": synced,
            "failed": failed,
            "pre_existing": existing_count,
        }

    except Exception as exc:
        registry.record_failure()
        logger.exception(f"[User {user_id}] Unhandled sync error: {exc}")
        db.rollback()
        return {"user_id": user_id, "status": "error", "reason": str(exc)}

    finally:
        db.close()


def nightly_sync_job():
    """Scheduled job: sync affirmations for all connected users at 2:00 AM UTC."""
    logger.info("=" * 60)
    logger.info("Starting nightly affirmation sync job")
    logger.info("=" * 60)

    db = SessionLocal()
    try:
        accounts = db.query(GoogleAccount).all()
        logger.info(f"Found {len(accounts)} connected Google accounts")

        results = []
        for account in accounts:
            result = sync_user_affirmations(account.user_id)
            results.append(result)

        success_count = sum(1 for r in results if r["status"] == "success")
        skip_count = sum(1 for r in results if r["status"] == "skipped")
        fail_count = sum(1 for r in results if r["status"] in ("failed", "error"))

        logger.info("=" * 60)
        logger.info(
            f"Nightly sync complete: {success_count} succeeded, "
            f"{skip_count} skipped, {fail_count} failed"
        )
        logger.info("=" * 60)

    except Exception as exc:
        logger.exception(f"Critical failure in nightly sync: {exc}")
        registry.record_failure()
    finally:
        db.close()


def token_health_check():
    """Proactive token refresh every 6 hours to prevent expiry."""
    logger.info("Running token health check...")
    db = SessionLocal()
    try:
        accounts = db.query(GoogleAccount).all()
        healthy = 0

        for account in accounts:
            try:
                service = GoogleCalendarService(account, db)
                service.list_calendars()
                healthy += 1
            except Exception as exc:
                logger.warning(f"[User {account.user_id}] Token health check failed: {exc}")

        logger.info(f"Token health check: {healthy}/{len(accounts)} accounts healthy")
    finally:
        db.close()


def job_listener(event):
    """Log job execution events."""
    if event.exception:
        logger.error(f"Job {event.job_id} crashed: {event.exception}")
    else:
        logger.info(f"Job {event.job_id} completed successfully")


def start_scheduler():
    """Initialize and start the background scheduler."""
    executors = {
        "default": ThreadPoolExecutor(20),
    }

    job_defaults = {
        "coalesce": True,
        "max_instances": 1,
        "misfire_grace_time": settings.MISFIRE_GRACE_SECONDS,
    }

    scheduler = BackgroundScheduler(
        executors=executors,
        job_defaults=job_defaults,
        timezone="UTC",
    )

    scheduler.add_job(
        nightly_sync_job,
        trigger=CronTrigger(
            hour=settings.SYNC_HOUR_UTC,
            minute=settings.SYNC_MINUTE_UTC,
        ),
        id="nightly_affirmation_sync",
        name="Sync affirmations for all users",
        replace_existing=True,
    )

    scheduler.add_job(
        token_health_check,
        trigger=CronTrigger(hour="*/6", minute=0),
        id="token_health_check",
        name="Verify Google token health for all accounts",
        replace_existing=True,
    )

    scheduler.add_listener(job_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
    scheduler.start()

    logger.info("Scheduler started. Jobs registered:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.id}: next run at {job.next_run_time}")

    return scheduler


def signal_handler(signum, frame):
    """Graceful shutdown on SIGINT/SIGTERM."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    scheduler.shutdown(wait=True)
    sys.exit(0)


if __name__ == "__main__":
    scheduler = start_scheduler()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
