"""
========================================
AI2CUP - Application Configuration
========================================

Centralized configuration using pydantic-settings.
All settings are loaded from environment variables with the AI2CUP_ prefix,
or from a .env file in the backend root directory.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ── App ──
    app_name: str = "AI2CUP"
    app_version: str = "2.0.0"
    debug: bool = False

    # ── API ──
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = [
        "*", 
        "http://localhost:8000", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173"]

    # ── ML ──
    model_dir: Path = Path("ckpt")
    price_model_filename: str = "trained_model_v2.joblib"
    auto_train_on_startup: bool = True

    # ── Data ──
    training_data_path: Path = Path("app/data/storage/eco_training.parquet")

    # ── Currency ──
    usd_to_etb: float = 57.0

    # ── Database ──
    database_url: str = "sqlite:///./ai2cup.db"

    # ── Auth ──
    jwt_secret: str = "8d5a0139-d6be-4d56-bee5-fd52bc0d4fb5-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    hf_token: str = ""
    hf_home: str = ""

    model_config = {
        "env_file": ".env",
        "env_prefix": "AI2CUP_",
        "extra": "ignore",
    }

    @property
    def etb_to_usd(self) -> float:
        """Derived conversion rate."""
        return 1.0 / self.usd_to_etb

    @property
    def model_path(self) -> Path:
        """Full path to the trained price model file."""
        return self.model_dir / self.price_model_filename


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — created once, reused everywhere."""
    return Settings()
