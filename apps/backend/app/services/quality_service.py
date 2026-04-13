"""
========================================
AI2CUP - Quality Analysis Service
========================================

Business logic for coffee quality analysis.
Handles image validation and delegates analysis to the ML layer.
"""

from __future__ import annotations

from app.core.exceptions import InvalidInputError, ModelNotReadyError
from app.ml.registry import ModelRegistry
from app.schemas.quality import QualityAnalysisResult

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class QualityService:
    """Business logic for quality analysis."""

    def __init__(self, model_registry: ModelRegistry) -> None:
        self._registry = model_registry

    def validate_image(self, content_type: str | None, file_size: int) -> None:
        """
        Validate an uploaded image before analysis.

        Raises InvalidInputError if validation fails.
        """
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidInputError(f"Invalid file type: {content_type}")
        if file_size > MAX_FILE_SIZE:
            raise InvalidInputError("File too large. Maximum 10MB.")
        if file_size == 0:
            raise InvalidInputError("Empty file uploaded.")

    def analyze(self, image_bytes: bytes) -> QualityAnalysisResult:
        """
        Analyze coffee bean image quality.

        1. Gets the quality model from the registry
        2. Passes image bytes to the model
        3. Returns a structured result
        """
        model = self._registry.get_model("quality")
        if model is None or not model.is_ready:
            raise ModelNotReadyError("quality")

        result = model.predict({"image_bytes": image_bytes})
        return QualityAnalysisResult(**result)
