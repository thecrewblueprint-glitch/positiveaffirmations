"""Donation tracking and analytics endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
import logging

router = APIRouter(prefix="/donations", tags=["Donations"])
logger = logging.getLogger("donations")


class DonationLog(BaseModel):
    """Log a donation event."""
    amount: float = Field(..., ge=1, le=10000)
    email: Optional[str] = None
    message: Optional[str] = None
    payment_platform: str = "paypal"  # paypal, stripe, github, etc.


@router.post("/log")
def log_donation(donation: DonationLog):
    """
    Log a donation for analytics/thank-you purposes.

    Does NOT process payment — that happens on PayPal/Stripe side.
    This just tracks that a user initiated a donation.
    """
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(
            f"Donation logged: ${donation.amount} via {donation.payment_platform} at {timestamp}"
        )

        # TODO: Save to database if you want to track donations
        # db.add(Donation(...))

        return {
            "status": "logged",
            "amount": donation.amount,
            "timestamp": timestamp,
            "message": f"Thank you for your ${donation.amount} donation! 💝",
        }

    except Exception as exc:
        logger.error(f"Donation logging failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to log donation")


@router.get("/stats")
def donation_stats():
    """Get public donation statistics (optional)."""
    # TODO: Fetch from database
    return {
        "total_donations": 0,
        "donor_count": 0,
        "average_donation": 0,
        "message": "Donations help keep this project free for everyone!",
    }
