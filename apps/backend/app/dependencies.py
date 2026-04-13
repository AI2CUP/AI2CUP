"""
========================================
AI2CUP - Dependency Injection Providers
========================================

FastAPI dependency providers for services and shared resources.
Routes use Depends() to receive services — they never construct them directly.

When adding new dependencies (database session, auth, etc.),
define the provider function here.
"""

from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.ml.registry import ModelRegistry
from app.services.match_service import MatchService
from app.services.price_service import PriceService
from app.services.quality_service import QualityService


@lru_cache
def get_model_registry() -> ModelRegistry:
    """Singleton model registry — created once and reused."""
    settings = get_settings()
    return ModelRegistry(settings)


def get_price_service() -> PriceService:
    """Price service with model registry injected."""
    return PriceService(model_registry=get_model_registry())


def get_quality_service() -> QualityService:
    """Quality service with model registry injected."""
    return QualityService(model_registry=get_model_registry())


def get_match_service() -> MatchService:
    """Match service with model registry injected."""
    return MatchService(model_registry=get_model_registry())


# ── Future Dependencies ──
#
# def get_db() -> Generator[Session, None, None]:
#     """Database session dependency (yields and auto-closes)."""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     """Auth dependency — extracts user from JWT token."""
#     ...
