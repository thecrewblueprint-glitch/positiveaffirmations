"""Pydantic schemas for affirmation API contracts."""

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class AffirmationOut(BaseModel):
    """Response model for affirmation data."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    affirmation_date: date
    text: str
    theme: Optional[str] = None


class AffirmationUpdate(BaseModel):
    """Request model for updating an affirmation."""
    text: Optional[str] = None
    theme: Optional[str] = None
