"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, affirmations, calendar, health, donations
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    title=settings.APP_NAME,
    description="Generate 365 unique daily affirmations and sync to Google Calendar",
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
)


@app.on_event("startup")
def on_startup():
    """Ensure database tables exist. create_all is idempotent, so this is
    safe to run on every boot (covers fresh Postgres/SQLite on deploy)."""
    init_db()

# CORS - restrict to known origins in production. Auth uses Bearer tokens
# (Authorization header), not cookies, so credentials are not required.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        settings.FRONTEND_URL,
    ] if settings.APP_ENV == "production" else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(affirmations.router)
app.include_router(calendar.router)
app.include_router(health.router)
app.include_router(donations.router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
    }
