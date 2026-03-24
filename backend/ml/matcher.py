"""
========================================
AI2CUP - Ethiopian Coffee Marketplace Matching Engine
========================================

Rule-based matching for Ethiopian coffee trade.
Features authentic Ethiopian cooperatives, unions, and
real international buyer profiles based on Ethiopia's
top coffee export destinations.

Ethiopia's top coffee export destinations (by volume):
1. Germany, 2. Saudi Arabia, 3. Japan, 4. USA, 5. Belgium,
6. South Korea, 7. France, 8. Italy, 9. UK, 10. Australia

Ethiopian coffee trade structure:
- Farmers → Cooperatives → Unions → ECX → Exporters → Importers
- Direct Trade: Cooperatives → International Buyers (growing trend)
"""

import random

# ── Ethiopian Coffee Sellers (Cooperatives, Unions, Estates) ──
SELLERS = [
    {
        "id": "S001",
        "name": "Yirgacheffe Coffee Farmers Cooperative Union (YCFCU)",
        "name_amharic": "የይርጋጨፌ ቡና አምራች ህብረት ስራ ማህበራት ዩኒየን",
        "region": "Yirgacheffe",
        "zone": "Gedeo Zone, SNNPR",
        "quality": "High",
        "ecx_grade": 1,
        "price_per_kg_etb": 380,
        "price_per_kg_usd": 6.67,
        "available_kg": 45000,
        "variety": "Heirloom",
        "processing": "Washed",
        "certification": ["Organic", "Fair Trade"],
        "members": 43000,
        "rating": 4.9,
    },
    {
        "id": "S002",
        "name": "Sidama Coffee Farmers Cooperative Union (SCFCU)",
        "name_amharic": "የሲዳማ ቡና አምራች ህብረት ስራ ማህበራት ዩኒየን",
        "region": "Sidamo",
        "zone": "Sidama Region",
        "quality": "High",
        "ecx_grade": 2,
        "price_per_kg_etb": 330,
        "price_per_kg_usd": 5.79,
        "available_kg": 60000,
        "variety": "Heirloom",
        "processing": "Washed",
        "certification": ["Fair Trade", "Rainforest Alliance"],
        "members": 68000,
        "rating": 4.7,
    },
    {
        "id": "S003",
        "name": "Oromia Coffee Farmers Cooperative Union (OCFCU)",
        "name_amharic": "የኦሮሚያ ቡና አምራች ህብረት ስራ ዩኒየን",
        "region": "Jimma",
        "zone": "Jimma Zone, Oromia",
        "quality": "Medium",
        "ecx_grade": 3,
        "price_per_kg_etb": 240,
        "price_per_kg_usd": 4.21,
        "available_kg": 120000,
        "variety": "Typica",
        "processing": "Washed",
        "certification": ["Fair Trade"],
        "members": 200000,
        "rating": 4.4,
    },
    {
        "id": "S004",
        "name": "Harar Coffee Cooperative",
        "name_amharic": "የሐረር ቡና ህብረት ስራ ማህበር",
        "region": "Harar",
        "zone": "Harari Region",
        "quality": "High",
        "ecx_grade": 2,
        "price_per_kg_etb": 360,
        "price_per_kg_usd": 6.32,
        "available_kg": 25000,
        "variety": "Heirloom",
        "processing": "Natural",
        "certification": ["Organic"],
        "members": 15000,
        "rating": 4.8,
    },
    {
        "id": "S005",
        "name": "Guji Highland Specialty Coffee",
        "name_amharic": "የጉጂ ከፍታ ልዩ ቡና",
        "region": "Guji",
        "zone": "Guji Zone, Oromia",
        "quality": "High",
        "ecx_grade": 1,
        "price_per_kg_etb": 400,
        "price_per_kg_usd": 7.02,
        "available_kg": 18000,
        "variety": "Gesha",
        "processing": "Natural",
        "certification": ["Organic", "Specialty Coffee Assoc."],
        "members": 8000,
        "rating": 5.0,
    },
    {
        "id": "S006",
        "name": "Limu Kossa Farmers Union",
        "name_amharic": "ሊሙ ኮሳ አርሶ አደር ዩኒየን",
        "region": "Limu",
        "zone": "Jimma Zone, Oromia",
        "quality": "Medium",
        "ecx_grade": 3,
        "price_per_kg_etb": 260,
        "price_per_kg_usd": 4.56,
        "available_kg": 55000,
        "variety": "Typica",
        "processing": "Washed",
        "certification": ["Rainforest Alliance"],
        "members": 32000,
        "rating": 4.2,
    },
    {
        "id": "S007",
        "name": "Bensa Daye Specialty Cooperative",
        "name_amharic": "ቤንሳ ዳዬ ልዩ ህብረት ስራ",
        "region": "Sidamo",
        "zone": "Sidama Region",
        "quality": "High",
        "ecx_grade": 1,
        "price_per_kg_etb": 450,
        "price_per_kg_usd": 7.89,
        "available_kg": 8000,
        "variety": "Gesha",
        "processing": "Honey",
        "certification": ["Organic", "Direct Trade"],
        "members": 3500,
        "rating": 5.0,
    },
    {
        "id": "S008",
        "name": "Wellega Anfilo Coffee Producers",
        "name_amharic": "ወለጋ አንፊሎ ቡና አምራቾች",
        "region": "Wellega",
        "zone": "Wellega Zone, Oromia",
        "quality": "Medium",
        "ecx_grade": 3,
        "price_per_kg_etb": 230,
        "price_per_kg_usd": 4.04,
        "available_kg": 35000,
        "variety": "74110",
        "processing": "Washed",
        "certification": [],
        "members": 18000,
        "rating": 3.8,
    },
    {
        "id": "S009",
        "name": "Bench Maji Forest Coffee",
        "name_amharic": "ቤንች ማጂ የደን ቡና",
        "region": "Bench Maji",
        "zone": "Bench Sheko Zone, SNNPR",
        "quality": "Medium",
        "ecx_grade": 4,
        "price_per_kg_etb": 190,
        "price_per_kg_usd": 3.33,
        "available_kg": 40000,
        "variety": "Heirloom",
        "processing": "Natural",
        "certification": ["Wild Forest Coffee"],
        "members": 12000,
        "rating": 4.0,
    },
    {
        "id": "S010",
        "name": "Addis Exporter PLC",
        "name_amharic": "አዲስ ኤክስፖርተር ሃ.የተ.የግ.ማ",
        "region": "Yirgacheffe",
        "zone": "Multiple regions",
        "quality": "High",
        "ecx_grade": 2,
        "price_per_kg_etb": 340,
        "price_per_kg_usd": 5.96,
        "available_kg": 200000,
        "variety": "Heirloom",
        "processing": "Washed",
        "certification": ["ECX Certified"],
        "members": 0,
        "rating": 4.5,
    },
]

# ── International Buyers (based on real export destinations) ──
BUYERS = [
    {
        "id": "B001",
        "name": "Deutsche Kaffee Rösterei GmbH",
        "country": "Germany 🇩🇪",
        "preferred_region": "Yirgacheffe",
        "min_quality": "High",
        "max_ecx_grade": 2,
        "max_price_per_kg_usd": 8.00,
        "max_price_per_kg_etb": 456,
        "volume_needed_kg": 30000,
        "certification_required": ["Organic"],
        "rating": 4.6,
    },
    {
        "id": "B002",
        "name": "Al-Qahwa Trading Co.",
        "country": "Saudi Arabia 🇸🇦",
        "preferred_region": "Harar",
        "min_quality": "High",
        "max_ecx_grade": 2,
        "max_price_per_kg_usd": 7.50,
        "max_price_per_kg_etb": 428,
        "volume_needed_kg": 50000,
        "certification_required": [],
        "rating": 4.3,
    },
    {
        "id": "B003",
        "name": "Tokyo Specialty Coffee Inc.",
        "country": "Japan 🇯🇵",
        "preferred_region": "Guji",
        "min_quality": "High",
        "max_ecx_grade": 1,
        "max_price_per_kg_usd": 12.00,
        "max_price_per_kg_etb": 684,
        "volume_needed_kg": 10000,
        "certification_required": ["Organic", "Direct Trade"],
        "rating": 4.9,
    },
    {
        "id": "B004",
        "name": "American Coffee Imports LLC",
        "country": "USA 🇺🇸",
        "preferred_region": None,
        "min_quality": "Medium",
        "max_ecx_grade": 3,
        "max_price_per_kg_usd": 6.00,
        "max_price_per_kg_etb": 342,
        "volume_needed_kg": 80000,
        "certification_required": ["Fair Trade"],
        "rating": 4.4,
    },
    {
        "id": "B005",
        "name": "Brussels Bean Brokers NV",
        "country": "Belgium 🇧🇪",
        "preferred_region": "Sidamo",
        "min_quality": "High",
        "max_ecx_grade": 2,
        "max_price_per_kg_usd": 7.00,
        "max_price_per_kg_etb": 399,
        "volume_needed_kg": 25000,
        "certification_required": [],
        "rating": 4.5,
    },
    {
        "id": "B006",
        "name": "Seoul Roasters Co., Ltd.",
        "country": "South Korea 🇰🇷",
        "preferred_region": "Yirgacheffe",
        "min_quality": "High",
        "max_ecx_grade": 2,
        "max_price_per_kg_usd": 9.00,
        "max_price_per_kg_etb": 513,
        "volume_needed_kg": 15000,
        "certification_required": ["Specialty Coffee Assoc."],
        "rating": 4.7,
    },
    {
        "id": "B007",
        "name": "Café de France SARL",
        "country": "France 🇫🇷",
        "preferred_region": "Limu",
        "min_quality": "Medium",
        "max_ecx_grade": 3,
        "max_price_per_kg_usd": 5.50,
        "max_price_per_kg_etb": 314,
        "volume_needed_kg": 40000,
        "certification_required": ["Rainforest Alliance"],
        "rating": 4.2,
    },
    {
        "id": "B008",
        "name": "Tomoca Coffee (Domestic)",
        "country": "Ethiopia 🇪🇹",
        "preferred_region": None,
        "min_quality": "Medium",
        "max_ecx_grade": 4,
        "max_price_per_kg_usd": 4.50,
        "max_price_per_kg_etb": 257,
        "volume_needed_kg": 100000,
        "certification_required": [],
        "rating": 4.6,
    },
]

# ── Quality hierarchy ──
QUALITY_ORDER = {"Low": 1, "Medium": 2, "High": 3}


def get_all_listings() -> dict:
    """Return all marketplace listings."""
    return {
        "sellers": SELLERS,
        "buyers": BUYERS,
        "total_sellers": len(SELLERS),
        "total_buyers": len(BUYERS),
    }


def find_matches(role="seller", region=None, quality=None,
                 max_price=None, min_volume=None) -> list:
    """Find matching counterparties based on filters."""
    candidates = SELLERS.copy() if role == "seller" else BUYERS.copy()
    matches = []

    for candidate in candidates:
        score = 50
        reasons = []

        if role == "seller":
            if region:
                if candidate["region"].lower() == region.lower():
                    score += 20
                    reasons.append("Region match")
                else:
                    score -= 10
            if quality:
                cq = QUALITY_ORDER.get(candidate["quality"], 0)
                rq = QUALITY_ORDER.get(quality, 0)
                if cq >= rq:
                    score += 15
                    reasons.append(f"Quality: {candidate['quality']}")
                else:
                    continue
            if max_price and candidate.get("price_per_kg_usd", 999) <= max_price:
                score += 10
                reasons.append("Within budget")
            if min_volume and candidate.get("available_kg", 0) >= min_volume:
                score += 5
                reasons.append("Sufficient volume")
            if candidate.get("certification"):
                score += 5
                reasons.append(f"Certified: {', '.join(candidate['certification'][:2])}")
        else:
            if region and candidate.get("preferred_region"):
                if candidate["preferred_region"].lower() == region.lower():
                    score += 20
                    reasons.append("Preferred region match")
            elif candidate.get("preferred_region") is None:
                score += 10
                reasons.append("Open to any region")
            if quality:
                mbq = QUALITY_ORDER.get(candidate.get("min_quality", "Low"), 0)
                sq = QUALITY_ORDER.get(quality, 0)
                if sq >= mbq:
                    score += 15
                    reasons.append("Meets quality requirement")
                else:
                    continue

        rating = candidate.get("rating", 3.0)
        score += int((rating - 3.0) * 5)
        score = max(0, min(100, score))

        matches.append({
            **candidate,
            "match_score": score,
            "match_reasons": reasons if reasons else ["General match"],
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches
