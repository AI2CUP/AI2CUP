"""
========================================
AI2CUP - Synthetic Ethiopian Coffee Dataset Generator
========================================

Generates realistic synthetic coffee price data modeled on
Ethiopia's coffee trade reality. Uses constants from the
core module instead of local definitions.

Run directly:
    python -m app.data.seed.generate_dataset
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from app.core.constants import (
    COFFEE_VARIETIES,
    ECX_GRADE_WEIGHTS,
    GRADE_MULTIPLIER,
    PROCESSING_METHODS,
    REGION_PROFILES,
    VARIETY_PREMIUM,
)

# ── Configuration ──
NUM_SAMPLES = 1200
RANDOM_SEED = 42
ETB_TO_USD = 0.0175


def generate_coffee_dataset(
    num_samples: int = NUM_SAMPLES,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate a synthetic Ethiopian coffee price dataset.

    Returns:
        pd.DataFrame with columns: region, zone, month, altitude, rainfall,
                                    variety, processing, ecx_grade,
                                    price_per_kg_etb, price_per_kg_usd
    """
    np.random.seed(seed)

    regions = list(REGION_PROFILES.keys())
    grades = list(ECX_GRADE_WEIGHTS.keys())
    grade_probs = np.array(list(ECX_GRADE_WEIGHTS.values()), dtype=float)
    grade_probs = grade_probs / grade_probs.sum()

    records = []

    for _ in range(num_samples):
        # ── Pick random region ──
        region = np.random.choice(regions)
        region_info = REGION_PROFILES[region]

        # ── Random month (1-12) ──
        month = np.random.randint(1, 13)

        # ── Altitude based on region range ──
        alt_low, alt_high = region_info["altitude_range"]
        altitude = np.random.uniform(alt_low, alt_high)

        # ── Rainfall: Ethiopian seasonal pattern ──
        if month in [6, 7, 8, 9]:
            rainfall = np.random.uniform(150, 300)   # Kiremt (main rainy)
        elif month in [2, 3, 4, 5]:
            rainfall = np.random.uniform(40, 150)    # Belg (small rains)
        else:
            rainfall = np.random.uniform(5, 60)      # Bega (dry/harvest)

        # ── Coffee variety & processing ──
        variety = np.random.choice(COFFEE_VARIETIES)
        processing = np.random.choice(PROCESSING_METHODS, p=[0.5, 0.35, 0.15])

        # ── ECX Grade ──
        ecx_grade = np.random.choice(grades, p=grade_probs)

        # ── Calculate price in ETB ──
        price_etb = region_info["base_price_etb"]

        # Altitude effect
        altitude_factor = (altitude - 1200) / 1000
        price_etb += altitude_factor * 80

        # Seasonal effect
        seasonal_effect = 30 * np.sin(2 * np.pi * (month - 11) / 12)
        price_etb += seasonal_effect

        # Rainfall effect
        if 80 <= rainfall <= 180:
            price_etb += 20
        elif rainfall > 250:
            price_etb -= 30

        # Variety premium
        price_etb *= VARIETY_PREMIUM[variety]

        # Grade multiplier
        price_etb *= GRADE_MULTIPLIER[ecx_grade]

        # Processing bonus
        if processing == "Natural":
            price_etb *= 1.05
        elif processing == "Honey":
            price_etb *= 1.08

        # Market noise
        noise = np.random.normal(0, 15)
        price_etb += noise

        # Clamp to realistic range
        price_etb = max(100, min(700, price_etb))

        # Convert to USD
        price_usd = round(price_etb * ETB_TO_USD, 2)

        records.append({
            "region": region,
            "zone": region_info["zone"],
            "month": month,
            "altitude": round(altitude, 1),
            "rainfall": round(rainfall, 1),
            "variety": variety,
            "processing": processing,
            "ecx_grade": int(ecx_grade),
            "price_per_kg_etb": round(price_etb, 2),
            "price_per_kg_usd": price_usd,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    print("AI2CUP - Generating synthetic Ethiopian coffee dataset...")

    df = generate_coffee_dataset()

    output_path = Path(__file__).parent.parent / "storage" / "coffee_prices.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} records -> {output_path}")
    print(f"\nPrice Statistics (ETB/kg):")
    print(df["price_per_kg_etb"].describe().to_string())
    print(f"\nSamples per Region:")
    print(df["region"].value_counts().to_string())
    print(f"\nECX Grade Distribution:")
    print(df["ecx_grade"].value_counts().sort_index().to_string())
