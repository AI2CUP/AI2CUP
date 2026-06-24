"""
========================================
AI2CUP - Middleware Configuration
========================================

Sets up CORS and any future middleware (logging, rate limiting, etc.).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings


def setup_middleware(app: FastAPI, settings: Settings) -> None:
    """Configure all application middleware."""

    allowed_origins = settings.cors_origins or []
    allow_credentials = "*" not in allowed_origins

    # ── CORS ──
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Future: Add logging middleware
    # Future: Add rate limiting middleware
    # Future: Add request ID middleware
