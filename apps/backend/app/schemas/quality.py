"""
========================================
AI2CUP - Quality Analysis Schemas
========================================

Request and response models for the quality analysis endpoint.
"""

from pydantic import BaseModel


class QualityAnalysisResult(BaseModel):
    """ECX-based quality analysis result."""

    quality: str
    confidence: float
    description: str
    ecx_grade: int
    ecx_label: str
    ecx_amharic: str
    defect_count: str
    scaa_score_range: str
    export_eligible: bool
    details: dict
