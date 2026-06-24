"""
AI2CUP - Coffee Price Prediction Model v2

HistGradientBoostingRegressor trained on real Ethiopian Coffee
Organization (ECO) weekly export price data.

Features: coffee_type (cat.), grade (num.), processing (cat.),
          exporter_type (cat.), month (num.)
Target:   price_usd_kg (USD per kilogram)
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

from app.config import get_settings
from app.ml.base import BaseMLModel

CATEGORICAL_FEATURES = ["coffee_type", "processing", "exporter_type"]
NUMERIC_FEATURES = ["grade", "month"]
ALL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "price_usd_kg"

INFERENCE_FIELD_MAP = {
    "coffee_type": "coffee_type",
    "month": "month",
    "processing": "processing",
    "ecx_grade": "grade",
    "exporter_type": "exporter_type",
}


class PriceModelV2(BaseMLModel):
    """Gradient-boosted tree price model trained on real ECO data."""

    def __init__(self) -> None:
        self._model: HistGradientBoostingRegressor | None = None
        self._settings = get_settings()
        self._training_metrics: dict = {}
        self._training_date: str = ""

    @property
    def model_info(self) -> str:
        if self._training_date:
            return f"HistGradientBoosting v2 (trained {self._training_date})"
        return "HistGradientBoosting v2 (scikit-learn)"

    @property
    def is_ready(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        model_path = self._settings.model_path
        if model_path.exists():
            data = joblib.load(model_path)
            if isinstance(data, dict):
                self._model = data["model"]
                self._training_metrics = data.get("metrics", {})
                self._training_date = data.get("training_date", "")
            else:
                self._model = data
        elif self._settings.auto_train_on_startup:
            self.train()

    def train(self, data_path: str | None = None) -> dict:
        training_path = (
            Path(data_path)
            if data_path
            else self._settings.training_data_path
        )

        if not training_path.exists():
            from app.data.processors.eco_data_processor import process_all_raw_files
            df = process_all_raw_files()
            training_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(training_path, index=False)
        else:
            df = pd.read_parquet(training_path)

        print(f"    Loaded {len(df)} records from {training_path}")

        df = df.sort_values(["year", "week"]).reset_index(drop=True)

        split_idx = int(len(df) * 0.85)
        df_train = df.iloc[:split_idx]
        df_test = df.iloc[split_idx:]

        X_train = df_train[ALL_FEATURES]
        y_train = df_train[TARGET]
        X_test = df_test[ALL_FEATURES]
        y_test = df_test[TARGET]

        cat_indices = [i for i, col in enumerate(ALL_FEATURES) if col in CATEGORICAL_FEATURES]

        model = HistGradientBoostingRegressor(
            categorical_features=cat_indices,
            max_iter=500,
            max_depth=12,
            learning_rate=0.08,
            min_samples_leaf=10,
            random_state=42,
        )

        print(f"    Training on {len(X_train)} samples ({len(X_test)} for test)...")
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"    MAE:  ${mae:.2f}/kg")
        print(f"    MAPE: {mape:.2%}")
        print(f"    R²:   {r2:.4f}")

        if hasattr(model, "feature_importances_"):
            print("\n    Feature importances:")
            for name, imp in sorted(
                zip(ALL_FEATURES, model.feature_importances_),
                key=lambda x: -x[1],
            ):
                print(f"      {name:25s}  {imp:.4f}")

        self._training_date = datetime.now().strftime("%Y-%m-%d")
        self._training_metrics = {
            "mae_usd": round(mae, 4),
            "mape": round(mape, 4),
            "r2": round(r2, 4),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "training_date": self._training_date,
        }

        model_path = self._settings.model_path
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "model": model,
                "metrics": self._training_metrics,
                "features": ALL_FEATURES,
                "categorical_features": CATEGORICAL_FEATURES,
                "numeric_features": NUMERIC_FEATURES,
                "training_date": self._training_date,
            },
            model_path,
        )
        print(f"\n    Model saved to {model_path}")

        self._model = model
        return self._training_metrics

    def predict(self, inputs: dict[str, Any]) -> dict[str, Any]:
        if self._model is None:
            raise RuntimeError("Price model is not loaded. Call load() first.")

        row = {INFERENCE_FIELD_MAP.get(k, k): v for k, v in inputs.items()}
        row.setdefault("exporter_type", "Commercial")

        input_df = pd.DataFrame([row])
        for col in ALL_FEATURES:
            if col not in input_df.columns:
                input_df[col] = ""

        predicted_usd = float(self._model.predict(input_df[ALL_FEATURES])[0])
        predicted_usd = max(1.0, min(25.0, predicted_usd))
        predicted_etb = predicted_usd * self._settings.usd_to_etb

        return {
            "price_usd": round(predicted_usd, 2),
            "price_etb": round(predicted_etb, 2),
        }

    @property
    def training_metrics(self) -> dict:
        return self._training_metrics
