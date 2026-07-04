"""Affirmation CRUD routes, scoped to the authenticated user."""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.affirmation import Affirmation
from app.schemas.affirmation import AffirmationOut, AffirmationUpdate

router = APIRouter(prefix="/affirmations", tags=["Affirmations"])


@router.get("/", response_model=List[AffirmationOut])
def get_user_affirmations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all affirmations for the current user, ordered by date."""
    return (
        db.query(Affirmation)
        .filter(Affirmation.user_id == current_user.id)
        .order_by(Affirmation.affirmation_date)
        .all()
    )


@router.get("/date/{date_str}", response_model=AffirmationOut)
def get_affirmation_by_date(
    date_str: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the current user's affirmation for a specific day (YYYY-MM-DD)."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")

    affirmation = (
        db.query(Affirmation)
        .filter(
            Affirmation.user_id == current_user.id,
            Affirmation.affirmation_date == target_date,
        )
        .first()
    )

    if not affirmation:
        raise HTTPException(status_code=404, detail="Affirmation not found")

    return affirmation


@router.patch("/{affirmation_id}")
def update_affirmation(
    affirmation_id: int,
    payload: AffirmationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Edit one of the current user's affirmations."""
    affirmation = (
        db.query(Affirmation)
        .filter(
            Affirmation.id == affirmation_id,
            Affirmation.user_id == current_user.id,
        )
        .first()
    )
    if not affirmation:
        raise HTTPException(status_code=404, detail="Affirmation not found")

    if payload.text is not None:
        affirmation.text = payload.text
    if payload.theme is not None:
        affirmation.theme = payload.theme

    db.commit()
    db.refresh(affirmation)

    # TODO: If already synced to Google Calendar, trigger event.update()
    return {"message": "Affirmation updated", "affirmation_id": affirmation_id}


@router.delete("/regenerate")
def regenerate_affirmations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete all affirmations and calendar events for the current user, then regenerate."""
    # TODO: Implement full regeneration flow
    return {"message": "Regeneration not yet implemented", "user_id": current_user.id}
