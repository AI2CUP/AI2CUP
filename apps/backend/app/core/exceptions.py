"""
========================================
AI2CUP - Custom Exception Classes
========================================

Standardized exceptions for the application.
These are caught by the global exception handler in main.py
and converted to consistent error responses.
"""


class AI2CUPError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ModelNotReadyError(AI2CUPError):
    """Raised when an ML model is not loaded or trained yet."""

    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' is not ready. It may need training.",
            code="MODEL_NOT_READY",
        )


class InvalidInputError(AI2CUPError):
    """Raised when input data fails business-level validation."""

    def __init__(self, message: str):
        super().__init__(message=message, code="INVALID_INPUT")


class DataNotFoundError(AI2CUPError):
    """Raised when required data (dataset, model file) is missing."""

    def __init__(self, resource: str):
        super().__init__(
            message=f"Required data not found: {resource}",
            code="DATA_NOT_FOUND",
        )


class PredictionError(AI2CUPError):
    """Raised when an ML prediction fails unexpectedly."""

    def __init__(self, model_name: str, detail: str):
        super().__init__(
            message=f"Prediction failed in '{model_name}': {detail}",
            code="PREDICTION_FAILED",
        )
