"""
========================================
AI2CUP - Abstract ML Model Interface
========================================

Every ML model in the system implements this interface.
This ensures the service layer never knows whether it's calling
scikit-learn, PyTorch, TensorFlow, or a remote API.

To add a new model:
  1. Create a class that inherits from BaseMLModel
  2. Implement predict(), load(), model_info, is_ready
  3. Register it in the ModelRegistry (ml/registry.py)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseMLModel(ABC):
    """Abstract interface for all ML models in AI2CUP."""

    @property
    @abstractmethod
    def model_info(self) -> str:
        """Human-readable model description (e.g., 'LinearRegression v1')."""
        ...

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """Whether the model is loaded and ready for predictions."""
        ...

    @abstractmethod
    def load(self) -> None:
        """Load/initialize the model. Called once at startup."""
        ...

    @abstractmethod
    def predict(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Run a prediction.

        Args:
            inputs: Dictionary of input features (model-specific).

        Returns:
            Dictionary of prediction results.
        """
        ...

    def train(self, data_path: str | None = None) -> dict:
        """
        Optional: train or retrain the model.
        Override in subclasses that support training.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support training"
        )
