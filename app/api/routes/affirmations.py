"""Affirmation CRUD routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.affirmation import Affirmation
from app.schemas.affirmation import AffirmationOut, AffirmationUpdate

router = APIRouter(prefix="/affirmations", tags=["Affirmations"])


@router.get("/{user_id}", response_model=List[AffirmationOut])
def get_user_affirmations(user_id: int, db: Session = Depends(get_db)):
    """Get all affirmations for a user, ordered by date."""
    affirmations = (
        db.query(Affirmation)
        .filter(Affirmation.user_id == user_id)
        .order_by(Affirmation.affirmation_date)
        .all()
    )
    return affirmations


@router.get("/{user_id}/{date_str}")
def get_affirmation_by_date(user_id: int, date_str: str, db: Session = Depends(get_db)):
    """Get a specific day's affirmation."""
    from datetime import datetime
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    affirmation = (
        db.query(Affirmation)
        .filter(
            Affirmation.user_id == user_id,
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
    db: Session = Depends(get_db),
):
    """Edit a specific affirmation's text."""
    affirmation = db.query(Affirmation).filter(Affirmation.id == affirmation_id).first()
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


@router.delete("/{user_id}/regenerate")
def regenerate_affirmations(user_id: int, db: Session = Depends(get_db)):
    """Delete all affirmations and calendar events for a user, then regenerate."""
    # TODO: Implement full regeneration flow
    return {"message": "Regeneration not yet implemented", "user_id": user_id}
