"""
========================================
AI2CUP - Quality Analysis API Route
========================================

POST /api/analyze-quality
Accepts image upload, returns ECX-based quality grade.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Quality Analysis"])


class QualityResponse(BaseModel):
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


@router.post("/analyze-quality", response_model=QualityResponse)
async def analyze_quality(file: UploadFile = File(..., description="Coffee bean image")):
    """
    Analyze uploaded coffee bean image using Ethiopian ECX grading standards.
    Returns ECX grade (1-5), quality label, confidence, and export eligibility.
    """
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        from ml.quality_detector import analyze_quality as ml_analyze
        result = ml_analyze(contents)
        return QualityResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality analysis failed: {str(e)}")
