"""Google Calendar event linkage for tracking and updates."""

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime

from app.models.base import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    affirmation_id: Mapped[int] = mapped_column(
        ForeignKey("affirmations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    google_event_id: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    calendar_id: Mapped[str] = mapped_column(String(255), default="primary")
    status: Mapped[str] = mapped_column(String(50), default="synced")
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="calendar_events")
    affirmation: Mapped["Affirmation"] = relationship(
        "Affirmation", back_populates="calendar_event"
    )
