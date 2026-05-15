"""
========================================
AI2CUP - Model Registry
========================================

Central registry that manages the lifecycle of all ML models.
Handles loading at startup and provides access by name.

Adding a new model:
  1. Create a class implementing BaseMLModel
  2. Import and register it in initialize()
"""

from __future__ import annotations

from app.config import Settings
from app.ml.base import BaseMLModel
from app.ml.price_model import PriceModel
from app.ml.quality_model import QualityModel


class ModelRegistry:
    """
    Central registry for all ML models in AI2CUP.

    Manages model loading, access, and health reporting.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._models: dict[str, BaseMLModel] = {}

    def initialize(self) -> None:
        """Load and register all models at startup."""
        models_to_load: dict[str, BaseMLModel] = {
            "price": PriceModel(),
            "quality": QualityModel(),
        }

        for name, model in models_to_load.items():
            print(f"  Loading model: {name}...")
            try:
                model.load()
                self._models[name] = model
                print(f"  [OK] {name} ready ({model.model_info})")
            except Exception as e:
                print(f"  [FAIL] {name} failed: {e}")
                # Model not registered — get_model() will return None

    def get_model(self, name: str) -> BaseMLModel | None:
        """
        Get a loaded model by name.

        Returns None if the model is not registered or failed to load.
        """
        return self._models.get(name)

    def health(self) -> dict[str, dict]:
        """Health status of all registered models."""
        return {
            name: {
                "ready": model.is_ready,
                "info": model.model_info,
            }
            for name, model in self._models.items()
        }
