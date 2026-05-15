"""
========================================
AI2CUP - Marketplace Listings API Routes
========================================

Endpoints:
  GET    /api/v1/listings       → Browse all active listings (public)
  POST   /api/v1/listings       → Create a new listing (auth required)
  GET    /api/v1/listings/my    → Get current user's listings (auth required)
  PUT    /api/v1/listings/{id}  → Update own listing (auth required)
  DELETE /api/v1/listings/{id}  → Delete own listing (auth required)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.auth import get_db, get_current_user
from app.models import Listing, User
from app.schemas.listing import ListingCreate, ListingUpdate, ListingResponse
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("", response_model=list[ListingResponse])
async def get_listings(
    region: Optional[str] = Query(None),
    max_grade: Optional[int] = Query(None, ge=1, le=5),
    db: Session = Depends(get_db),
):
    """
    Browse all active listings. Publicly accessible.
    Optional filters: region, max ECX grade.
    """
    query = db.query(Listing).filter(Listing.is_active == True)

    if region:
        query = query.filter(Listing.region == region)
    if max_grade:
        query = query.filter(Listing.ecx_grade <= max_grade)

    return query.order_by(Listing.created_at.desc()).all()


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_in: ListingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new coffee listing. Requires authentication."""
    # Generate title if not provided
    title = listing_in.title
    if not title:
        grade_text = f"Grade {listing_in.ecx_grade}" if listing_in.ecx_grade > 0 else "No Grade"
        parts = [listing_in.region, grade_text]
        if listing_in.processing:
            parts.append(listing_in.processing)
        if listing_in.variety:
            parts.append(listing_in.variety)
        title = " — ".join(parts)

    # Calculate USD price if not provided
    price_usd = listing_in.price_per_kg_usd
    if not price_usd:
        price_usd = listing_in.price_per_kg_etb / settings.usd_to_etb

    new_listing = Listing(
        user_id=current_user.id,
        title=title,
        description=listing_in.description,
        region=listing_in.region,
        ecx_grade=listing_in.ecx_grade,
        variety=listing_in.variety,
        processing=listing_in.processing,
        price_per_kg_etb=listing_in.price_per_kg_etb,
        price_per_kg_usd=price_usd,
        available_kg=listing_in.available_kg,
        certification=listing_in.certification or "",
        contact_name=listing_in.contact_name,
        contact_phone=listing_in.contact_phone,
        contact_email=listing_in.contact_email,
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing


@router.get("/my", response_model=list[ListingResponse])
async def get_my_listings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all listings belonging to the current user."""
    return (
        db.query(Listing)
        .filter(Listing.user_id == current_user.id)
        .order_by(Listing.created_at.desc())
        .all()
    )


@router.put("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: int,
    listing_in: ListingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing listing. Only the owner can edit."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this listing")

    update_data = listing_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an existing listing. Only the owner can delete."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this listing")

    db.delete(listing)
    db.commit()
