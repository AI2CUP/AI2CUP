"""
========================================
AI2CUP - Main FastAPI Application
========================================

Application factory pattern — creates and configures the FastAPI app.

Run with:
    cd apps/backend
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.exceptions import AI2CUPError
from app.core.middleware import setup_middleware
from app.dependencies import get_model_registry
from app.models import init_db, SessionLocal, Listing
from app.data.seed.marketplace import SELLERS


def _seed_listings():
    """Populate the listings table from seed data if empty."""
    db = SessionLocal()
    try:
        if db.query(Listing).count() == 0:
            print("  Seeding marketplace listings...")
            for seller in SELLERS:
                listing = Listing(
                    user_id=None,  # seed data has no owner
                    title=seller["name"],
                    description=f"{seller.get('name_amharic', '')} — {seller.get('zone', '')}",
                    region=seller["region"],
                    ecx_grade=seller["ecx_grade"],
                    variety=seller.get("variety"),
                    processing=seller.get("processing"),
                    price_per_kg_etb=seller["price_per_kg_etb"],
                    price_per_kg_usd=seller["price_per_kg_usd"],
                    available_kg=seller["available_kg"],
                    certification=", ".join(seller.get("certification", [])),
                    contact_name=seller["name"],
                    contact_phone="+251 911 000 000",
                    contact_email="info@ai2cup.com",
                    is_active=True,
                )
                db.add(listing)
            db.commit()
            print(f"  [OK] Seeded {len(SELLERS)} listings")
        else:
            print(f"  Listings table already has data, skipping seed.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.

    Startup:
      - Initializes the model registry (loads all ML models)
      - Seeds the listings table if empty

    Shutdown:
      - Cleanup (future: close DB connections, etc.)
    """
    settings = get_settings()
    print(f"\n{settings.app_name} v{settings.app_version} starting...")

    # Initialize ML models
    registry = get_model_registry()
    registry.initialize()

    # Initialize Database
    print("Initializing database...")
    init_db()

    # Seed marketplace listings
    _seed_listings()

    print(f"{settings.app_name} is ready!\n")

    yield

    print(f"\n{settings.app_name} shutting down...")


def create_app() -> FastAPI:
    """
    Application factory — creates and configures the FastAPI app.

    This pattern allows creating multiple app instances (useful for testing).
    """
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} API",
        description=(
            "AI-powered platform for improving Ethiopian coffee trade. "
            "Features: Price Prediction, Quality Detection, Coffee Marketplace."
        ),
        version=settings.app_version,
        lifespan=lifespan,
    )

    # ── Middleware ──
    setup_middleware(app, settings)

    # ── Global exception handler ──
    @app.exception_handler(AI2CUPError)
    async def handle_app_error(request, exc: AI2CUPError):
        """Convert application exceptions to consistent JSON responses."""
        status_map = {
            "MODEL_NOT_READY": 503,
            "INVALID_INPUT": 400,
            "DATA_NOT_FOUND": 404,
            "PREDICTION_FAILED": 500,
        }
        status_code = status_map.get(exc.code, 500)
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": exc.message,
                "code": exc.code,
            },
        )

    # ── API routes ──
    app.include_router(api_router, prefix=settings.api_prefix)

    # ── Root redirect ──
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "message": f"{settings.app_name} API is running.",
            "docs": "/docs",
            "api": f"{settings.api_prefix}/health",
        }

    return app


# ── Application instance (used by uvicorn) ──
app = create_app()
