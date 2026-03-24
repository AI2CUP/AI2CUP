"""
========================================
AI2CUP - Coffee Price Prediction Model
========================================

ML model for Ethiopian coffee price prediction.
Uses scikit-learn pipeline with:
- OneHotEncoder for categorical features (region, variety, processing)
- Linear Regression for prediction
- Dual currency output (ETB + USD)

Ethiopian context:
- Prices are in Ethiopian Birr (ETB) — converted to USD for international buyers
- ECX grade significantly impacts price
- Region and altitude are key quality indicators
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# ── Paths ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "coffee_prices.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.joblib")

# ETB/USD conversion
USD_TO_ETB = 57.0
ETB_TO_USD = 1 / USD_TO_ETB


def train_and_save_model() -> dict:
    """
    Train a Linear Regression model on the Ethiopian coffee dataset.
    Predicts price_per_kg_etb based on region, month, altitude,
    rainfall, variety, processing, and ecx_grade.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Run `python data/generate_dataset.py` first."
        )

    df = pd.read_csv(DATA_PATH)
    print(f"📦 Loaded {len(df)} records from dataset")

    # ── Features and target ──
    feature_cols = ["region", "month", "altitude", "rainfall", "variety", "processing", "ecx_grade"]
    target_col = "price_per_kg_etb"

    X = df[feature_cols]
    y = df[target_col]

    # ── Preprocessing pipeline ──
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

    print(f"📊 Model Performance:")
    print(f"   MAE:  {mae:.2f} ETB/kg (${mae * ETB_TO_USD:.2f} USD)")
    print(f"   R²:   {r2:.4f}")

    joblib.dump(pipeline, MODEL_PATH)
    print(f"💾 Model saved → {MODEL_PATH}")

    return {"mae_etb": round(mae, 2), "mae_usd": round(mae * ETB_TO_USD, 2), "r2": round(r2, 4)}


def load_model() -> Pipeline:
    """Load the trained model pipeline from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            "Run `python ml/price_model.py` first."
        )
    return joblib.load(MODEL_PATH)


def predict_price(region: str, month: int, altitude: float,
                  rainfall: float, variety: str,
                  processing: str = "Washed", ecx_grade: int = 3) -> dict:
    """
    Predict coffee price for given parameters.
    Returns both ETB and USD prices.

    Args:
        region:     Ethiopian coffee region
        month:      Month of year (1-12)
        altitude:   Altitude in meters
        rainfall:   Rainfall in mm
        variety:    Coffee variety
        processing: Processing method (Washed/Natural/Honey)
        ecx_grade:  ECX grade (1-5, where 1=best)

    Returns:
        dict with predicted_price_etb and predicted_price_usd
    """
    model = load_model()

    input_df = pd.DataFrame([{
        "region": region,
        "month": month,
        "altitude": altitude,
        "rainfall": rainfall,
        "variety": variety,
        "processing": processing,
        "ecx_grade": ecx_grade,
    }])

    predicted_etb = model.predict(input_df)[0]

    # Clamp to realistic ETB range
    predicted_etb = max(100, min(700, predicted_etb))
    predicted_usd = predicted_etb * ETB_TO_USD

    return {
        "price_etb": round(predicted_etb, 2),
        "price_usd": round(predicted_usd, 2),
    }


if __name__ == "__main__":
    print("🌿 AI2CUP — Training Ethiopian Coffee Price Model\n")
    metrics = train_and_save_model()
    print(f"\n✅ Training complete! Metrics: {metrics}")
