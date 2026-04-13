"""
========================================
AI2CUP - Domain Constants
========================================

Single source of truth for all Ethiopian coffee domain constants.
These values are used across schemas, services, and ML modules.

References:
  - Ethiopia Commodity Exchange (ECX) grading standards
  - Ethiopian coffee growing regions and their characteristics
"""

# ── ECX Grade System ──────────────────────────────────────────

ECX_GRADES: dict[int, dict] = {
    1: {
        "label": "Grade 1 - Specialty",
        "amharic": "ልዩ ደረጃ",
        "description": (
            "Premium specialty grade - suitable for direct export "
            "to specialty roasters worldwide"
        ),
        "defects": "0-3 defects per 300g",
        "scaa_range": "85+",
        "export_eligible": True,
    },
    2: {
        "label": "Grade 2 - Very Good",
        "amharic": "በጣም ጥሩ",
        "description": (
            "High quality - suitable for export and specialty domestic market"
        ),
        "defects": "4-12 defects per 300g",
        "scaa_range": "80-84",
        "export_eligible": True,
    },
    3: {
        "label": "Grade 3 - Good",
        "amharic": "ጥሩ",
        "description": (
            "Good commercial grade - suitable for export and domestic consumption"
        ),
        "defects": "13-25 defects per 300g",
        "scaa_range": "75-79",
        "export_eligible": True,
    },
    4: {
        "label": "Grade 4 - Commercial",
        "amharic": "ንግድ",
        "description": (
            "Standard commercial grade - primarily for domestic market and blending"
        ),
        "defects": "26-45 defects per 300g",
        "scaa_range": "70-74",
        "export_eligible": False,
    },
    5: {
        "label": "Grade 5 - Below Standard",
        "amharic": "ከደረጃ በታች",
        "description": (
            "Below standard - requires further sorting and processing before sale"
        ),
        "defects": "46-90 defects per 300g",
        "scaa_range": "60-69",
        "export_eligible": False,
    },
}

ECX_GRADE_LABELS: dict[int, str] = {
    1: "Grade 1 - Specialty (ልዩ ደረጃ)",
    2: "Grade 2 - Very Good (በጣም ጥሩ)",
    3: "Grade 3 - Good (ጥሩ)",
    4: "Grade 4 - Commercial (ንግድ)",
    5: "Grade 5 - Below Standard (ከደረጃ በታች)",
}

# Maps ECX grade to simple quality label (for backward compatibility)
QUALITY_MAP: dict[int, str] = {
    1: "High",
    2: "High",
    3: "Medium",
    4: "Medium",
    5: "Low",
}

# Quality hierarchy for matching comparisons
QUALITY_ORDER: dict[str, int] = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
}


# ── Ethiopian Coffee Regions ─────────────────────────────────

ETHIOPIAN_REGIONS: list[str] = [
    "Yirgacheffe",
    "Sidamo",
    "Harar",
    "Jimma",
    "Limu",
    "Guji",
    "Wellega",
    "Bench Maji",
]

# ── Coffee Varieties (all Arabica) ───────────────────────────

COFFEE_VARIETIES: list[str] = [
    "Heirloom",
    "Typica",
    "Bourbon",
    "Gesha",
    "74110",
    "74112",
]

# ── Processing Methods ───────────────────────────────────────

PROCESSING_METHODS: list[str] = [
    "Washed",
    "Natural",
    "Honey",
]

# ── Dataset Generation Constants ─────────────────────────────

REGION_PROFILES: dict[str, dict] = {
    "Yirgacheffe": {
        "zone": "Gedeo Zone, SNNPR",
        "altitude_range": (1700, 2200),
        "base_price_etb": 350,
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

VARIETY_PREMIUM: dict[str, float] = {
    "Heirloom": 1.0,
    "Typica": 0.95,
    "Bourbon": 1.05,
    "Gesha": 1.35,
    "74110": 1.0,
    "74112": 1.0,
}

ECX_GRADE_WEIGHTS: dict[int, float] = {
    1: 0.10,
    2: 0.20,
    3: 0.30,
    4: 0.25,
    5: 0.12,
}

GRADE_MULTIPLIER: dict[int, float] = {
    1: 1.6,
    2: 1.3,
    3: 1.0,
    4: 0.75,
    5: 0.5,
}
