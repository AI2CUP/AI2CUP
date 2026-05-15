"""
========================================
AI2CUP - API v1 Router Aggregator
========================================

Combines all v1 route modules into a single router.
Mounted in main.py under the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.v1 import health, listing, price, quality, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(price.router, prefix="/price", tags=["price"])
api_router.include_router(quality.router, prefix="/quality", tags=["quality"])
api_router.include_router(listing.router, prefix="/listings", tags=["listings"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

