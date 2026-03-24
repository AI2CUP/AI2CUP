"""
========================================
AI2CUP - Price Prediction API Route
========================================

Endpoint: POST /api/predict-price
Returns coffee price in both ETB (Ethiopian Birr) and USD.
Supports ECX grade and processing method inputs.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(tags=["Price Prediction"])


# ── Request/Response models ──────────────────────────────────
class PricePredictionRequest(BaseModel):
    """Input parameters for Ethiopian coffee price prediction."""
    region: str = Field(..., description="Ethiopian coffee region", examples=["Yirgacheffe"])
    month: int = Field(..., ge=1, le=12, description="Month of year (1-12)")
    altitude: float = Field(default=1800.0, ge=1000, le=3000, description="Altitude in meters")
    rainfall: float = Field(default=120.0, ge=0, le=500, description="Rainfall in mm")
    variety: str = Field(default="Heirloom", description="Coffee variety", examples=["Heirloom"])
    processing: str = Field(default="Washed", description="Processing method: Washed, Natural, Honey")
    ecx_grade: int = Field(default=3, ge=1, le=5, description="ECX Grade (1=Specialty, 5=Below Standard)")


class PricePredictionResponse(BaseModel):
    """Predicted price in dual currency."""
    predicted_price_etb: float
    predicted_price_usd: float
    currency_primary: str = "ETB"
    currency_secondary: str = "USD"
    unit: str = "per kg"
    inputs: dict
    ecx_grade_label: str
    model_info: str = "Linear Regression (scikit-learn)"


# ── ECX grade labels ──
ECX_LABELS = {
    1: "Grade 1 — Specialty (ልዩ ደረጃ)",
    2: "Grade 2 — Very Good (በጣም ጥሩ)",
    3: "Grade 3 — Good (ጥሩ)",
    4: "Grade 4 — Commercial (ንግድ)",
    5: "Grade 5 — Below Standard (ከደረጃ በታች)",
}


@router.post("/predict-price", response_model=PricePredictionResponse)
async def predict_price(request: PricePredictionRequest):
    """
    Predict Ethiopian coffee price based on region, season, altitude,
    variety, processing method, and ECX grade.
    Returns price in both ETB and USD.
    """
    try:
        from ml.price_model import predict_price as ml_predict

        result = ml_predict(
            region=request.region,
            month=request.month,
            altitude=request.altitude,
            rainfall=request.rainfall,
            variety=request.variety,
            processing=request.processing,
            ecx_grade=request.ecx_grade,
        )

        return PricePredictionResponse(
            predicted_price_etb=result["price_etb"],
            predicted_price_usd=result["price_usd"],
            ecx_grade_label=ECX_LABELS.get(request.ecx_grade, f"Grade {request.ecx_grade}"),
            inputs={
                "region": request.region,
                "month": request.month,
                "altitude": request.altitude,
                "rainfall": request.rainfall,
                "variety": request.variety,
                "processing": request.processing,
                "ecx_grade": request.ecx_grade,
            },
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=f"Model not ready: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
