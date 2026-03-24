"""
========================================
AI2CUP - Synthetic Ethiopian Coffee Dataset Generator
========================================

Generates realistic synthetic coffee price data specifically
modeled on Ethiopia's coffee trade reality.

Key Ethiopian coffee context:
- Ethiopia is the birthplace of Arabica coffee
- Coffee is Ethiopia's #1 export (~30% of export revenue)
- ECX (Ethiopia Commodity Exchange) standardizes grading
- Main harvest season: October–February (Meher season)
- Secondary harvest: March–June (Belg season in some areas)
- Average farm-gate price: 40-120 ETB/kg ($0.70-$2.10 USD)
- Export price: 180-600 ETB/kg ($3-$10 USD)

ECX Grading System (used in this dataset):
- Grade 1: Specialty (0-3 defects per 300g)
- Grade 2: Very Good (4-12 defects)
- Grade 3: Good (13-25 defects)
- Grade 4: Commercial (26-45 defects)
- Grade 5: Below Standard (46-90 defects)
- UG: Under Grade (90+ defects)
"""

import pandas as pd
import numpy as np
import os

# ── Configuration ──────────────────────────────────────────────
NUM_SAMPLES = 1200  # Number of data points to generate
RANDOM_SEED = 42    # For reproducibility

# Ethiopian Birr to USD conversion rate (approximate, 2024-2025)
ETB_TO_USD = 0.0175  # ~57 ETB per 1 USD
USD_TO_ETB = 57.0

# ── Ethiopian coffee-growing regions with real characteristics ──
# Each region has distinct flavor profiles and altitude ranges
REGIONS = {
    "Yirgacheffe": {
        "zone": "Gedeo Zone, SNNPR",
        "altitude_range": (1700, 2200),
        "base_price_etb": 350,   # ETB per kg (export grade)
        "premium": 1.5,
        "flavor_profile": "Floral, citrus, tea-like",
        "processing": "Washed",
    },
    "Sidamo": {
        "zone": "Sidama Region",
        "altitude_range": (1550, 2000),
        "base_price_etb": 300,
        "premium": 1.2,
        "flavor_profile": "Berry, wine, citrus",
        "processing": "Washed/Natural",
    },
    "Harar": {
        "zone": "Harari Region",
        "altitude_range": (1500, 2100),
        "base_price_etb": 320,
        "premium": 1.3,
        "flavor_profile": "Blueberry, wine, mocha",
        "processing": "Natural (sun-dried)",
    },
    "Jimma": {
        "zone": "Jimma Zone, Oromia",
        "altitude_range": (1400, 1800),
        "base_price_etb": 220,
        "premium": 0.8,
        "flavor_profile": "Earthy, full-bodied",
        "processing": "Washed",
    },
    "Limu": {
        "zone": "Jimma Zone, Oromia",
        "altitude_range": (1500, 1900),
        "base_price_etb": 260,
        "premium": 1.0,
        "flavor_profile": "Wine-like, spicy, balanced",
        "processing": "Washed",
    },
    "Guji": {
        "zone": "Guji Zone, Oromia",
        "altitude_range": (1800, 2300),
        "base_price_etb": 340,
        "premium": 1.4,
        "flavor_profile": "Complex, fruity, floral",
        "processing": "Washed/Natural",
    },
    "Wellega": {
        "zone": "Wellega Zone, Oromia",
        "altitude_range": (1500, 2000),
        "base_price_etb": 240,
        "premium": 0.9,
        "flavor_profile": "Fruity, nutty, chocolate",
        "processing": "Washed",
    },
    "Bench Maji": {
        "zone": "Bench Sheko Zone, SNNPR",
        "altitude_range": (1200, 1800),
        "base_price_etb": 200,
        "premium": 0.7,
        "flavor_profile": "Wild, earthy, herbal",
        "processing": "Natural",
    },
}

# Coffee varieties grown in Ethiopia (all Arabica)
VARIETIES = ["Heirloom", "Typica", "Bourbon", "Gesha", "74110", "74112"]

# Variety premium multipliers
VARIETY_PREMIUM = {
    "Heirloom": 1.0,     # Most common Ethiopian variety
    "Typica":   0.95,
    "Bourbon":  1.05,
    "Gesha":    1.35,    # Gesha/Geisha - world's most expensive coffee origin
    "74110":    1.0,     # Ethiopian-bred rust-resistant variety
    "74112":    1.0,     # Ethiopian-bred variety
}

# ECX Processing methods
PROCESSING_METHODS = ["Washed", "Natural", "Honey"]

# ECX Grade distribution probabilities (weighted toward middle grades)
ECX_GRADE_WEIGHTS = {
    1: 0.10,  # Grade 1 - Specialty (rare)
    2: 0.20,  # Grade 2 - Very Good
    3: 0.30,  # Grade 3 - Good (most common)
    4: 0.25,  # Grade 4 - Commercial
    5: 0.12,  # Grade 5 - Below Standard
}

# Grade price multipliers
GRADE_MULTIPLIER = {1: 1.6, 2: 1.3, 3: 1.0, 4: 0.75, 5: 0.5}


def generate_coffee_dataset(num_samples: int = NUM_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate a synthetic Ethiopian coffee price dataset.

    Returns:
        pd.DataFrame with columns: region, zone, month, altitude, rainfall,
                                    variety, processing, ecx_grade, price_per_kg_etb,
                                    price_per_kg_usd
    """
    np.random.seed(seed)

    records = []

    for _ in range(num_samples):
        # ── Pick a random region ──
        region = np.random.choice(list(REGIONS.keys()))
        region_info = REGIONS[region]

        # ── Random month (1-12) ──
        month = np.random.randint(1, 13)

        # ── Altitude based on region range ──
        alt_low, alt_high = region_info["altitude_range"]
        altitude = np.random.uniform(alt_low, alt_high)

        # ── Rainfall: Ethiopian seasonal pattern ──
        # Kiremt (Jun-Sep): Heavy rains | Belg (Feb-May): Light rains | Bega (Oct-Jan): Dry
        if month in [6, 7, 8, 9]:
            rainfall = np.random.uniform(150, 300)  # Kiremt (main rainy)
        elif month in [2, 3, 4, 5]:
            rainfall = np.random.uniform(40, 150)   # Belg (small rains)
        else:
            rainfall = np.random.uniform(5, 60)      # Bega (dry/harvest)

        # ── Coffee variety ──
        variety = np.random.choice(VARIETIES)

        # ── Processing method ──
        processing = np.random.choice(PROCESSING_METHODS, p=[0.5, 0.35, 0.15])

        # ── ECX Grade ──
        grades = list(ECX_GRADE_WEIGHTS.keys())
        grade_probs = np.array(list(ECX_GRADE_WEIGHTS.values()), dtype=float)
        grade_probs = grade_probs / grade_probs.sum()
        ecx_grade = np.random.choice(grades, p=grade_probs)

        # ── Calculate price in ETB ──
        # Base price from region
        price_etb = region_info["base_price_etb"]

        # Altitude effect: higher altitude → better quality → higher price
        altitude_factor = (altitude - 1200) / 1000  # Normalize
        price_etb += altitude_factor * 80  # Up to 80 ETB bonus

        # Seasonal effect: prices peak during/after harvest (Oct-Jan)
        # and dip when supply is low (Jul-Sep)
        seasonal_effect = 30 * np.sin(2 * np.pi * (month - 11) / 12)
        price_etb += seasonal_effect

        # Rainfall effect
        if 80 <= rainfall <= 180:
            price_etb += 20   # Ideal rainfall bonus
        elif rainfall > 250:
            price_etb -= 30   # Excessive rain reduces quality

        # Variety premium
        price_etb *= VARIETY_PREMIUM[variety]

        # Grade multiplier (biggest factor)
        price_etb *= GRADE_MULTIPLIER[ecx_grade]

        # Processing bonus
        if processing == "Natural":
            price_etb *= 1.05  # Sun-dried often fetches premium
        elif processing == "Honey":
            price_etb *= 1.08

        # Market noise (price fluctuations)
        noise = np.random.normal(0, 15)
        price_etb += noise

        # Clamp to realistic range (ETB 100-700 per kg for export grade)
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
    print("🌿 AI2CUP - Generating synthetic Ethiopian coffee dataset...")

    df = generate_coffee_dataset()

    output_path = os.path.join(os.path.dirname(__file__), "coffee_prices.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Generated {len(df)} records → {output_path}")
    print(f"\n📊 Dataset Preview:")
    print(df.head(10).to_string(index=False))
    print(f"\n💰 Price Statistics (ETB/kg):")
    print(df["price_per_kg_etb"].describe().to_string())
    print(f"\n💵 Price Statistics (USD/kg):")
    print(df["price_per_kg_usd"].describe().to_string())
    print(f"\n🗺️  Samples per Region:")
    print(df["region"].value_counts().to_string())
    print(f"\n📊 ECX Grade Distribution:")
    print(df["ecx_grade"].value_counts().sort_index().to_string())
