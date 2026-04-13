"""
========================================
AI2CUP - Quality Analysis API Routes
========================================

Endpoint: POST /api/v1/quality/analyze

Accepts image upload, returns ECX-based quality grade.
"""

from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies import get_quality_service
from app.schemas.quality import QualityAnalysisResult
from app.services.quality_service import QualityService

router = APIRouter(prefix="/quality", tags=["Quality Analysis"])


@router.post("/analyze", response_model=QualityAnalysisResult)
async def analyze_quality(
    file: UploadFile = File(..., description="Coffee bean image"),
    service: QualityService = Depends(get_quality_service),
):
    """
    Analyze uploaded coffee bean image using Ethiopian ECX grading standards.

    Returns ECX grade (1-5), quality label, confidence, and export eligibility.
    """
    contents = await file.read()
    service.validate_image(file.content_type, len(contents))
    return service.analyze(contents)
