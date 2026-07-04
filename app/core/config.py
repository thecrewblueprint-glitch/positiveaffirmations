"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """All environment variables with validation and defaults."""

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./app.db",
        description="SQLAlchemy database URL. Use PostgreSQL in production."
    )

    # Google OAuth
    GOOGLE_CLIENT_ID: str = Field(
        ...,
        description="Google OAuth client ID from Google Cloud Console"
    )
    GOOGLE_CLIENT_SECRET: str = Field(
        ...,
        description="Google OAuth client secret"
    )
    GOOGLE_REDIRECT_URI: str = Field(
        default="http://localhost:8000/auth/google/callback",
        description="Must match redirect URI in Google Cloud Console"
    )

    # App Settings
    APP_NAME: str = "Daily Affirmations"
    APP_ENV: str = Field(default="development", pattern="^(development|staging|production)$")
    SECRET_KEY: str = Field(
        default="change-me-in-production",
        description="Used for session signing and token encryption"
    )

    # Scheduler
    SYNC_HOUR_UTC: int = Field(default=2, ge=0, le=23)
    SYNC_MINUTE_UTC: int = Field(default=0, ge=0, le=59)
    MISFIRE_GRACE_SECONDS: int = Field(default=3600, description="Allow 1hr late if down")

    # Rate Limiting
    GOOGLE_API_DELAY_MS: int = Field(default=100, description="Delay between API calls")
    BATCH_SIZE: int = Field(default=50, description="Events per batch before pause")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
