from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class RawRow(BaseModel):
    """A single row as parsed from an ECO Excel file."""

    file_name: str
    coffee_type: str
    exporter_type: str
    grade_raw: str | int | None
    processing_raw: str
    price_usc_lb: float
    week_start: date | None
    crop: str = ""


class CleanedRow(BaseModel):
    """A single cleaned and enriched record ready for training."""

    coffee_type: str
    region: str | None = None
    zone: str = ""
    grade: int
    processing: str
    exporter_type: str
    month: int
    altitude: float
    rainfall: float
    variety: str
    price_usc_lb: float
    price_etb_kg: float
    week_start: date | None = None
    crop: str = ""
