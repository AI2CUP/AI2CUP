"""
========================================
AI2CUP - Marketplace Matching Service
========================================

Business logic for marketplace listing and matching.
"""

from __future__ import annotations

from app.core.exceptions import ModelNotReadyError
from app.ml.matcher import MatcherModel
from app.ml.registry import ModelRegistry
from app.schemas.match import MatchRequest, MatchResponse


class MatchService:
    """Business logic for marketplace matching."""

    def __init__(self, model_registry: ModelRegistry) -> None:
        self._registry = model_registry

    def _get_matcher(self) -> MatcherModel:
        """Get the matcher model, raising if not ready."""
        model = self._registry.get_model("matcher")
        if model is None or not model.is_ready:
            raise ModelNotReadyError("matcher")
        return model  # type: ignore[return-value]

    def get_all_listings(self) -> dict:
        """Retrieve all marketplace listings (sellers and buyers)."""
        matcher = self._get_matcher()
        return matcher.get_listings()

    def find_matches(self, request: MatchRequest) -> MatchResponse:
        """
        Find matching counterparties based on criteria.

        Results are sorted by match score (highest first).
        """
        matcher = self._get_matcher()

        matches = matcher.predict({
            "role": request.role,
            "region": request.region,
            "quality": request.quality,
            "max_price": request.max_price,
            "min_volume": request.min_volume,
        })

        return MatchResponse(
            matches=matches,
            total=len(matches),
            criteria=request.model_dump(),
        )
