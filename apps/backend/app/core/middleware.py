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

    # ── CORS ──
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Future: Add logging middleware
    # Future: Add rate limiting middleware
    # Future: Add request ID middleware
