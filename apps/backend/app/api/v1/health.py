"""
========================================
AI2CUP - Health Check API Routes
========================================

Endpoints:
  GET /api/v1/health  → Application and model health status
"""

from fastapi import APIRouter, Depends

from app.config import get_settings, Settings
from app.dependencies import get_model_registry
from app.ml.registry import ModelRegistry

router = APIRouter()


@router.get("")
async def health_check(
    settings: Settings = Depends(get_settings),
    registry: ModelRegistry = Depends(get_model_registry),
):
    """
    Health check endpoint with model status.

    Returns application info and readiness state of all ML models.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "models": registry.health(),
    }
