"""
========================================
AI2CUP - Price Prediction Service
========================================

Business logic for coffee price prediction.
Orchestrates between the API layer and the ML layer.

This is where you add:
  - Logging predictions to a database
  - Caching frequent predictions
  - Enriching results with business context
  - Audit trails
"""

from __future__ import annotations

from app.core.constants import ECX_GRADE_LABELS
from app.core.exceptions import ModelNotReadyError
from app.ml.registry import ModelRegistry
from app.schemas.price import PricePredictionRequest, PricePredictionResponse


class PriceService:
    """Business logic for price prediction."""

    def __init__(self, model_registry: ModelRegistry) -> None:
        self._registry = model_registry

    def predict(self, request: PricePredictionRequest) -> PricePredictionResponse:
        """
        Predict coffee price.

        1. Gets the ML model through the registry (not directly)
        2. Calls predict with the request parameters
        3. Enriches the result with ECX grade labels
        4. Returns a formatted response
        """
        model = self._registry.get_model("price")
        if model is None or not model.is_ready:
            raise ModelNotReadyError("price")

        # Call ML through abstract interface
        prediction = model.predict({
            "region": request.region,
            "month": request.month,
            "altitude": request.altitude,
            "rainfall": request.rainfall,
            "variety": request.variety,
            "processing": request.processing,
            "ecx_grade": request.ecx_grade,
        })

        return PricePredictionResponse(
            predicted_price_etb=prediction["price_etb"],
            predicted_price_usd=prediction["price_usd"],
            ecx_grade_label=ECX_GRADE_LABELS.get(
                request.ecx_grade, f"Grade {request.ecx_grade}"
            ),
            inputs=request.model_dump(),
            model_info=model.model_info,
        )
