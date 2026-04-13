"""
========================================
AI2CUP - Marketplace Matching Schemas
========================================

Request and response models for the marketplace matching endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class MatchRequest(BaseModel):
    """Parameters for finding marketplace matches."""

    role: str = Field(
        default="seller",
        description="Looking for 'seller' or 'buyer'",
    )
    region: Optional[str] = Field(
        default=None,
        description="Preferred region filter",
    )
    quality: Optional[str] = Field(
        default=None,
        description="Minimum quality grade: High, Medium, Low",
    )
    max_price: Optional[float] = Field(
        default=None,
        description="Maximum price per kg (USD)",
    )
    min_volume: Optional[int] = Field(
        default=None,
        description="Minimum volume needed (kg)",
    )


class MatchResponse(BaseModel):
    """Response containing matched counterparties."""

    matches: list[dict]
    total: int
    criteria: dict
