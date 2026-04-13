"""
========================================
AI2CUP - Coffee Price Prediction Model
========================================

Scikit-learn pipeline wrapping Linear Regression with
OneHotEncoder for categorical features.

Implements BaseMLModel so the service layer interacts
through a stable interface regardless of the underlying ML framework.
"""

from __future__ import annotations

from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.config import get_settings
from app.ml.base import BaseMLModel


class PriceModel(BaseMLModel):
    """
    Scikit-learn price prediction model.

    Predicts Ethiopian coffee prices in ETB/kg based on region, month,
    altitude, rainfall, variety, processing method, and ECX grade.
    """

    def __init__(self) -> None:
        self._model: Pipeline | None = None
        self._settings = get_settings()

    @property
    def model_info(self) -> str:
        return "LinearRegression v1 (scikit-learn)"

    @property
    def is_ready(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        """
        Load the trained model from disk.
        If the model file doesn't exist and auto_train is enabled,
        trains a new model from the dataset.
        """
        model_path = self._settings.model_path
        if model_path.exists():
            self._model = joblib.load(model_path)
        elif self._settings.auto_train_on_startup:
            self.train()

    def train(self, data_path: str | None = None) -> dict:
        """
        Train a Linear Regression model on the Ethiopian coffee dataset.
        Generates the dataset first if it doesn't exist.
        """
        from app.data.seed.generate_dataset import generate_coffee_dataset

        dataset_path = (
            self._settings.dataset_path
            if data_path is None
            else type(self._settings.dataset_path)(data_path)
        )

        # Generate dataset if missing
        if not dataset_path.exists():
            print("    Generating synthetic dataset...")
            dataset_path.parent.mkdir(parents=True, exist_ok=True)
            df = generate_coffee_dataset()
            df.to_csv(dataset_path, index=False)
            print(f"    Generated {len(df)} records")
        else:
            df = pd.read_csv(dataset_path)

        print(f"    Loaded {len(df)} records from dataset")

        # ── Features & target ──
        feature_cols = [
            "region", "month", "altitude", "rainfall",
            "variety", "processing", "ecx_grade",
        ]
        target_col = "price_per_kg_etb"

        X = df[feature_cols]
        y = df[target_col]

        # ── Pipeline ──
        categorical_features = ["region", "variety", "processing"]
        numerical_features = ["month", "altitude", "rainfall", "ecx_grade"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
                ("num", "passthrough", numerical_features),
            ]
        )

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression()),
        ])

        # ── Train/test split ──
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        pipeline.fit(X_train, y_train)

        # ── Evaluate ──
        y_pred = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        etb_to_usd = self._settings.etb_to_usd
        print(f"    MAE: {mae:.2f} ETB/kg (${mae * etb_to_usd:.2f} USD)")
        print(f"    R2:  {r2:.4f}")

        # ── Save ──
        model_path = self._settings.model_path
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, model_path)
        print(f"    Model saved to {model_path}")

        self._model = pipeline

        return {
            "mae_etb": round(mae, 2),
            "mae_usd": round(mae * etb_to_usd, 2),
            "r2": round(r2, 4),
        }

    def predict(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Predict coffee price for given parameters.

        Args:
            inputs: dict with keys: region, month, altitude, rainfall,
                    variety, processing, ecx_grade

        Returns:
            dict with price_etb and price_usd
        """
        if self._model is None:
            raise RuntimeError("Price model is not loaded. Call load() first.")

        input_df = pd.DataFrame([{
            "region": inputs["region"],
            "month": inputs["month"],
            "altitude": inputs["altitude"],
            "rainfall": inputs["rainfall"],
            "variety": inputs["variety"],
            "processing": inputs["processing"],
            "ecx_grade": inputs["ecx_grade"],
        }])

        predicted_etb = self._model.predict(input_df)[0]
        predicted_etb = max(100, min(700, predicted_etb))
        predicted_usd = predicted_etb * self._settings.etb_to_usd

        return {
            "price_etb": round(float(predicted_etb), 2),
            "price_usd": round(float(predicted_usd), 2),
        }
