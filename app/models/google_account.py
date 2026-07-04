"""Google OAuth token storage with automatic credential building."""

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime
from google.oauth2.credentials import Credentials

from app.models.base import Base
from app.db.types import EncryptedText
from app.core.config import settings


class GoogleAccount(Base):
    __tablename__ = "google_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    google_sub: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    # Tokens are encrypted at rest via EncryptedText; application code still
    # reads/writes plaintext.
    access_token: Mapped[str | None] = mapped_column(EncryptedText, nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(EncryptedText, nullable=True)
    token_expiry: Mapped[str | None] = mapped_column(String(100), nullable=True)

    calendar_id: Mapped[str] = mapped_column(String(255), default="primary")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="google_account")

    def get_credentials(self) -> Credentials:
        """Build Google Credentials from stored tokens.

        Tokens are decrypted transparently by the EncryptedText column type,
        so self.access_token / self.refresh_token are already plaintext here.
        """
        return Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/calendar.events"],
        )
