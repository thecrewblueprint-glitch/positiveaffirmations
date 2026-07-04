"""Database initialization script. Run once at startup or manually."""

from app.db.session import engine
from app.models.base import Base

# Import all models to register them with Base.metadata
from app.models import user, google_account, affirmation, calendar_event


def init_db() -> None:
    """Create all tables from SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
