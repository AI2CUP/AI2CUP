"""
========================================
AI2CUP - API v1 Router Aggregator
========================================

Combines all v1 route modules into a single router.
Mounted in main.py under the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.v1 import health, match, price, quality

api_router = APIRouter()

api_router.include_router(price.router)
api_router.include_router(quality.router)
api_router.include_router(match.router)
api_router.include_router(health.router)
