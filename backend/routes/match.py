"""
========================================
AI2CUP - Marketplace Matching API Route
========================================

Endpoints:
- GET  /match         → Get all marketplace listings
- POST /match/find    → Find matching counterparties
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List

from ml.matcher import get_all_listings, find_matches

# ── Router setup ──
router = APIRouter(tags=["Marketplace"])


# ── Request/Response models ──────────────────────────────────
class MatchRequest(BaseModel):
    """Parameters for finding matches."""
    role: str = Field(
        default="seller",
        description="Looking for 'seller' or 'buyer'"
    )
    region: Optional[str] = Field(
        default=None,
        description="Preferred region filter"
    )
    quality: Optional[str] = Field(
        default=None,
        description="Minimum quality grade: High, Medium, Low"
    )
    max_price: Optional[float] = Field(
        default=None,
        description="Maximum price per kg (USD)"
    )
    min_volume: Optional[int] = Field(
        default=None,
        description="Minimum volume needed (kg)"
    )


# ── Endpoints ────────────────────────────────────────────────
@router.get("/match")
async def get_marketplace():
    """
    Get all marketplace listings (buyers and sellers).
    
    Returns the complete list of registered buyers and sellers
    for the marketplace overview page.
    """
    return get_all_listings()


@router.post("/match/find")
async def find_match(request: MatchRequest):
    """
    Find matching counterparties based on criteria.
    
    A seller can find matching buyers, and vice versa.
    Results are sorted by match score (highest first).
    """
    matches = find_matches(
        role=request.role,
        region=request.region,
        quality=request.quality,
        max_price=request.max_price,
        min_volume=request.min_volume,
    )
    
    return {
        "matches": matches,
        "total": len(matches),
        "criteria": {
            "role": request.role,
            "region": request.region,
            "quality": request.quality,
            "max_price": request.max_price,
            "min_volume": request.min_volume,
        },
    }
