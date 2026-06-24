from __future__ import annotations

from pydantic import BaseModel, Field


class PricePredictionRequest(BaseModel):
    """Input parameters for Ethiopian coffee price prediction."""

    coffee_type: str = Field(
        default="Yirgachefe",
        description="Ethiopian coffee type",
        examples=["Yirgachefe", "Sidamo", "Guji", "Harar"],
    )
    year: int = Field(
        default=2025,
        ge=2024,
        le=2030,
        description="Year of prediction",
    )
    month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month of year (1-12)",
    )
    week: int | None = Field(
        default=None,
        ge=1,
        le=53,
        description="Week of year (1-53, optional)",
    )
    processing: str = Field(
        default="Washed",
        description="Processing method: Washed, Natural",
    )
    ecx_grade: int = Field(
        default=3,
        ge=1,
        le=5,
        description="ECX Grade (1=Specialty, 5=Below Standard)",
    )
    exporter_type: str = Field(
        default="Commercial",
        description="Exporter type: Commercial, Grower, Union, V/Integration",
    )


class PricePredictionResponse(BaseModel):
    """Predicted price in dual currency."""

    predicted_price_usd: float
    predicted_price_etb: float
    currency_primary: str = "USD"
    currency_secondary: str = "ETB"
    unit: str = "per kg"
    inputs: dict
    ecx_grade_label: str
    model_info: str
