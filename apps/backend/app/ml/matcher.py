"""
========================================
AI2CUP - Marketplace Matching Engine
========================================

Rule-based matching for Ethiopian coffee trade.
Matches sellers (cooperatives) with buyers (international importers)
based on region, quality, price, and volume preferences.

Implements BaseMLModel so the matching algorithm can be replaced
with an ML-based recommender system later.

Data is loaded from app/data/seed/marketplace.py (will become
database-backed in the future).
"""

from __future__ import annotations

from typing import Any

from app.core.constants import QUALITY_ORDER
from app.data.seed.marketplace import BUYERS, SELLERS
from app.ml.base import BaseMLModel


class MatcherModel(BaseMLModel):
    """
    Rule-based marketplace matching engine.

    Scores potential counterparties based on region match,
    quality requirements, price compatibility, and volume needs.
    """

    def __init__(self) -> None:
        self._loaded = False

    @property
    def model_info(self) -> str:
        return "Rule-based Matcher v1"

    @property
    def is_ready(self) -> bool:
        return self._loaded

    def load(self) -> None:
        """Matcher uses static data — always ready once loaded."""
        self._loaded = True

    def get_listings(self) -> dict[str, Any]:
        """Return all marketplace listings."""
        return {
            "sellers": SELLERS,
            "buyers": BUYERS,
            "total_sellers": len(SELLERS),
            "total_buyers": len(BUYERS),
        }

    def predict(self, inputs: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Find matching counterparties based on filters.

        Args:
            inputs: dict with keys: role, region, quality, max_price, min_volume

        Returns:
            List of matched candidates with scores, sorted desc.
        """
        role = inputs.get("role", "seller")
        region = inputs.get("region")
        quality = inputs.get("quality")
        max_price = inputs.get("max_price")
        min_volume = inputs.get("min_volume")

        candidates = SELLERS.copy() if role == "seller" else BUYERS.copy()
        matches = []

        for candidate in candidates:
            score = 50
            reasons = []

            if role == "seller":
                score, reasons = self._score_seller(
                    candidate, region, quality, max_price, min_volume,
                    score, reasons,
                )
            else:
                score, reasons = self._score_buyer(
                    candidate, region, quality, score, reasons,
                )

            if score < 0:
                continue  # Filtered out

            # Rating bonus
            rating = candidate.get("rating", 3.0)
            score += int((rating - 3.0) * 5)
            score = max(0, min(100, score))

            matches.append({
                **candidate,
                "match_score": score,
                "match_reasons": reasons if reasons else ["General match"],
            })

        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches

    def _score_seller(
        self,
        candidate: dict,
        region: str | None,
        quality: str | None,
        max_price: float | None,
        min_volume: int | None,
        score: int,
        reasons: list[str],
    ) -> tuple[int, list[str]]:
        """Score a seller candidate."""
        if region:
            if candidate["region"].lower() == region.lower():
                score += 20
                reasons.append("Region match")
            else:
                score -= 10

        if quality:
            cq = QUALITY_ORDER.get(candidate["quality"], 0)
            rq = QUALITY_ORDER.get(quality, 0)
            if cq >= rq:
                score += 15
                reasons.append(f"Quality: {candidate['quality']}")
            else:
                return -1, reasons  # Filter out

        if max_price and candidate.get("price_per_kg_usd", 999) <= max_price:
            score += 10
            reasons.append("Within budget")

        if min_volume and candidate.get("available_kg", 0) >= min_volume:
            score += 5
            reasons.append("Sufficient volume")

        if candidate.get("certification"):
            score += 5
            certs = ", ".join(candidate["certification"][:2])
            reasons.append(f"Certified: {certs}")

        return score, reasons

    def _score_buyer(
        self,
        candidate: dict,
        region: str | None,
        quality: str | None,
        score: int,
        reasons: list[str],
    ) -> tuple[int, list[str]]:
        """Score a buyer candidate."""
        if region and candidate.get("preferred_region"):
            if candidate["preferred_region"].lower() == region.lower():
                score += 20
                reasons.append("Preferred region match")
        elif candidate.get("preferred_region") is None:
            score += 10
            reasons.append("Open to any region")

        if quality:
            mbq = QUALITY_ORDER.get(candidate.get("min_quality", "Low"), 0)
            sq = QUALITY_ORDER.get(quality, 0)
            if sq >= mbq:
                score += 15
                reasons.append("Meets quality requirement")
            else:
                return -1, reasons  # Filter out

        return score, reasons
