"""
========================================
AI2CUP - Price Prediction API Routes
========================================

Endpoint: POST /api/v1/price/predict

Thin route — validates HTTP, calls service, returns response.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_price_service
from app.schemas.price import PricePredictionRequest, PricePredictionResponse
from app.services.price_service import PriceService

router = APIRouter(prefix="/price", tags=["Price Prediction"])


@router.post("/predict", response_model=PricePredictionResponse)
async def predict_price(
    request: PricePredictionRequest,
    service: PriceService = Depends(get_price_service),
):
    """
    Predict Ethiopian coffee price based on region, season, altitude,
    variety, processing method, and ECX grade.

    Returns price in both ETB and USD.
    """
    return service.predict(request)
