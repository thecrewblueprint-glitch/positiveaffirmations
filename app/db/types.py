"""Custom SQLAlchemy column types."""

from sqlalchemy.types import TypeDecorator, Text

from app.core.security import encrypt_value, decrypt_value


class EncryptedText(TypeDecorator):
    """Text column that is transparently encrypted at rest.

    Values are encrypted on the way into the database and decrypted on the way
    out, so application code reads/writes plain strings unchanged.
    """

    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return encrypt_value(value)

    def process_result_value(self, value, dialect):
        return decrypt_value(value)
