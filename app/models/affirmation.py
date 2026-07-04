"""Daily affirmation content model."""

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text, Date, UniqueConstraint

from app.models.base import Base


class Affirmation(Base):
    __tablename__ = "affirmations"
    __table_args__ = (
        UniqueConstraint("user_id", "affirmation_date", name="uix_user_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    affirmation_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="affirmations")
    calendar_event: Mapped["CalendarEvent"] = relationship(
        "CalendarEvent", back_populates="affirmation", uselist=False
    )
