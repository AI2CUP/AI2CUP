"""
========================================
AI2CUP - Listing Schemas
========================================

Request and response models for the marketplace listings.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ListingCreate(BaseModel):
    """Schema for creating a new coffee listing."""

    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

    region: str
    ecx_grade: int = Field(..., ge=0, le=5)
    variety: Optional[str] = None
    processing: Optional[str] = None

    price_per_kg_etb: float = Field(..., gt=0)
    price_per_kg_usd: Optional[float] = Field(None, gt=0)
    available_kg: int = Field(..., gt=0)

    certification: Optional[str] = ""

    contact_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class ListingUpdate(BaseModel):
    """Schema for updating an existing listing (all fields optional)."""

    title: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None
    ecx_grade: Optional[int] = Field(None, ge=1, le=5)
    variety: Optional[str] = None
    processing: Optional[str] = None
    price_per_kg_etb: Optional[float] = Field(None, gt=0)
    price_per_kg_usd: Optional[float] = Field(None, gt=0)
    available_kg: Optional[int] = Field(None, gt=0)
    certification: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class ListingResponse(BaseModel):
    """Public-facing listing response."""

    id: int
    user_id: Optional[int] = None
    title: str
    description: Optional[str] = None

    region: str
    ecx_grade: int
    variety: Optional[str] = None
    processing: Optional[str] = None

    price_per_kg_etb: float
    price_per_kg_usd: float
    available_kg: int

    certification: Optional[str] = ""

    contact_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
