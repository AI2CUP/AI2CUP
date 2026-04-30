"""
========================================
AI2CUP - Marketplace Matching API Routes
========================================

Endpoints:
  GET  /api/v1/match       → Get all marketplace listings
  POST /api/v1/match/find  → Find matching counterparties
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_match_service
from app.schemas.match import MatchRequest, MatchResponse
from app.services.match_service import MatchService
from app.core.auth import get_current_user
from app.models import User

router = APIRouter()


@router.get("")
async def get_marketplace(
    service: MatchService = Depends(get_match_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get all marketplace listings (buyers and sellers).
    Requires authentication.
    """
    return service.get_all_listings()


@router.post("/find", response_model=MatchResponse)
async def find_match(
    request: MatchRequest,
    service: MatchService = Depends(get_match_service),
    current_user: User = Depends(get_current_user)
):
    """
    Find matching counterparties based on criteria.
    Requires authentication.
    """
    return service.find_matches(request)
