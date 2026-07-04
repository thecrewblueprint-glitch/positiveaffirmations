"""JWT session token creation and verification."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app.core.config import settings

ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 30


def create_access_token(user_id: int) -> str:
    """Issue a signed JWT for a user session."""
    expire = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[int]:
    """Return the user_id from a valid token, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except Exception:
        return None
