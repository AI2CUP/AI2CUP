"""
========================================
AI2CUP - Common Schemas
========================================

Shared base schemas and response wrappers used across the API.
"""

from pydantic import BaseModel
from typing import Any


class ErrorResponse(BaseModel):
    """Standard error response format."""

    success: bool = False
    error: str
    code: str
