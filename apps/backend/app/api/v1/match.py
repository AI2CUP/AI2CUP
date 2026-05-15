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

router = APIRouter()


@router.get("")
async def get_marketplace(
    service: MatchService = Depends(get_match_service)
):
    """
    Get all marketplace listings (buyers and sellers).
    Publicly accessible.
    """
    return service.get_all_listings()


@router.post("/find", response_model=MatchResponse)
async def find_match(
    request: MatchRequest,
    service: MatchService = Depends(get_match_service)
):
    """
    Find matching counterparties based on criteria.
    Publicly accessible.
    """
    return service.find_matches(request)
