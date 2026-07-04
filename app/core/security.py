"""JWT session tokens and at-rest encryption for stored OAuth tokens."""

import base64
import hashlib
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Optional

import jwt
from cryptography.fernet import Fernet, InvalidToken

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


@lru_cache(maxsize=1)
def _fernet() -> Fernet:
    """Derive a stable Fernet key from SECRET_KEY (32-byte SHA-256 digest)."""
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_value(value: Optional[str]) -> Optional[str]:
    """Encrypt a string for storage. None passes through."""
    if value is None:
        return None
    return _fernet().encrypt(value.encode()).decode()


def decrypt_value(value: Optional[str]) -> Optional[str]:
    """Decrypt a stored string. Falls back to returning the raw value for
    legacy rows that were written before encryption was enabled."""
    if value is None:
        return None
    try:
        return _fernet().decrypt(value.encode()).decode()
    except (InvalidToken, ValueError):
        return value
