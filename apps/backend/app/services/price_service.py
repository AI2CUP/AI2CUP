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
        model = self._registry.get_model("price")
        if model is None or not model.is_ready:
            raise ModelNotReadyError("price")

        prediction = model.predict({
            "coffee_type": request.coffee_type,
            "month": request.month,
            "ecx_grade": request.ecx_grade,
            "processing": request.processing,
            "exporter_type": request.exporter_type,
        })

        return PricePredictionResponse(
            predicted_price_usd=prediction["price_usd"],
            predicted_price_etb=prediction["price_etb"],
            ecx_grade_label=ECX_GRADE_LABELS.get(
                request.ecx_grade, f"Grade {request.ecx_grade}"
            ),
            inputs=request.model_dump(),
            model_info=model.model_info,
        )
