"""
========================================
AI2CUP - Price Prediction Schemas
========================================

Request and response models for the price prediction endpoint.
"""

from pydantic import BaseModel, Field


class PricePredictionRequest(BaseModel):
    """Input parameters for Ethiopian coffee price prediction."""

    region: str = Field(
        ...,
        description="Ethiopian coffee region",
        examples=["Yirgacheffe"],
    )
    month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month of year (1-12)",
    )
    altitude: float = Field(
        default=1800.0,
        ge=1000,
        le=3000,
        description="Altitude in meters",
    )
    rainfall: float = Field(
        default=120.0,
        ge=0,
        le=500,
        description="Rainfall in mm",
    )
    variety: str = Field(
        default="Heirloom",
        description="Coffee variety",
        examples=["Heirloom"],
    )
    processing: str = Field(
        default="Washed",
        description="Processing method: Washed, Natural, Honey",
    )
    ecx_grade: int = Field(
        default=3,
        ge=1,
        le=5,
        description="ECX Grade (1=Specialty, 5=Below Standard)",
    )


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
