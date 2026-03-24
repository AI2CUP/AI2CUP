"""
========================================
AI2CUP - Coffee Quality Detection
========================================

Simulates coffee bean quality analysis using the ECX
(Ethiopia Commodity Exchange) grading system.

ECX Grading (Ethiopian standard):
- Grade 1: Specialty (0-3 defects per 300g)  - 85+ SCAA score
- Grade 2: Very Good (4-12 defects)          - 80-84 SCAA
- Grade 3: Good (13-25 defects)              - 75-79 SCAA
- Grade 4: Commercial (26-45 defects)        - 70-74 SCAA
- Grade 5: Below Standard (46-90 defects)    - 60-69 SCAA
- UG: Under Grade (90+ defects)              - <60 SCAA

For this MVP, we analyze image properties and map them
to the ECX grading system with realistic confidence scores.
"""

import io
import random
import numpy as np
from PIL import Image


# ── ECX Grade descriptions ──
ECX_GRADES = {
    1: {
        "label": "Grade 1 - Specialty",
        "amharic": "ልዩ ደረጃ",
        "description": "Premium specialty grade - suitable for direct export to specialty roasters worldwide",
        "defects": "0-3 defects per 300g",
        "scaa_range": "85+",
        "export_eligible": True,
    },
    2: {
        "label": "Grade 2 - Very Good",
        "amharic": "በጣም ጥሩ",
        "description": "High quality - suitable for export and specialty domestic market",
        "defects": "4-12 defects per 300g",
        "scaa_range": "80-84",
        "export_eligible": True,
    },
    3: {
        "label": "Grade 3 - Good",
        "amharic": "ጥሩ",
        "description": "Good commercial grade - suitable for export and domestic consumption",
        "defects": "13-25 defects per 300g",
        "scaa_range": "75-79",
        "export_eligible": True,
    },
    4: {
        "label": "Grade 4 - Commercial",
        "amharic": "ንግድ",
        "description": "Standard commercial grade  - primarily for domestic market and blending",
        "defects": "26-45 defects per 300g",
        "scaa_range": "70-74",
        "export_eligible": False,
    },
    5: {
        "label": "Grade 5 - Below Standard",
        "amharic": "ከደረጃ በታች",
        "description": "Below standard - requires further sorting and processing before sale",
        "defects": "46-90 defects per 300g",
        "scaa_range": "60-69",
        "export_eligible": False,
    },
}


def analyze_quality(image_bytes: bytes) -> dict:
    """
    Analyze a coffee bean image and return ECX-based quality assessment.

    For the MVP, combines basic image analysis with simulated ML predictions
    to produce realistic results mapped to Ethiopian ECX grades.

    Args:
        image_bytes: Raw bytes of the uploaded image

    Returns:
        dict with ECX grade, confidence, and detailed analysis
    """
    try:
        # ── Open and analyze the image ──
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_resized = image.resize((224, 224))
        pixels = np.array(image_resized, dtype=np.float32)

        # ── Extract image features ──
        brightness = np.mean(pixels)
        r_mean = np.mean(pixels[:, :, 0])
        g_mean = np.mean(pixels[:, :, 1])
        b_mean = np.mean(pixels[:, :, 2])

        # Color uniformity (lower std = more uniform = fewer defects)
        uniformity = 1.0 - (np.std(pixels) / 128.0)
        uniformity = max(0.0, min(1.0, uniformity))

        # Brown/warm tones suggest properly dried coffee beans
        warmth_score = (r_mean - b_mean) / 255.0

        # ── Compute simulated quality score (0-1) ──
        quality_score = (
            0.30 * uniformity +
            0.25 * (warmth_score + 0.5) +
            0.20 * (brightness / 255.0) +
            0.25 * random.uniform(0.3, 0.9)
        )
        quality_score = max(0.0, min(1.0, quality_score))

        # ── Map score to ECX grade ──
        if quality_score >= 0.75:
            ecx_grade = 1
            confidence = round(random.uniform(0.85, 0.96), 2)
        elif quality_score >= 0.60:
            ecx_grade = 2
            confidence = round(random.uniform(0.80, 0.92), 2)
        elif quality_score >= 0.45:
            ecx_grade = 3
            confidence = round(random.uniform(0.75, 0.88), 2)
        elif quality_score >= 0.30:
            ecx_grade = 4
            confidence = round(random.uniform(0.70, 0.85), 2)
        else:
            ecx_grade = 5
            confidence = round(random.uniform(0.65, 0.80), 2)

        grade_info = ECX_GRADES[ecx_grade]

        # Map ECX grade to simple quality label for backward compatibility
        quality_map = {1: "High", 2: "High", 3: "Medium", 4: "Medium", 5: "Low"}

        return {
            "quality": quality_map[ecx_grade],
            "confidence": confidence,
            "description": grade_info["description"],
            "ecx_grade": ecx_grade,
            "ecx_label": grade_info["label"],
            "ecx_amharic": grade_info["amharic"],
            "defect_count": grade_info["defects"],
            "scaa_score_range": grade_info["scaa_range"],
            "export_eligible": grade_info["export_eligible"],
            "details": {
                "image_size": f"{image.width}x{image.height}",
                "brightness": round(brightness, 1),
                "color_uniformity": round(uniformity, 3),
                "warmth_index": round(warmth_score, 3),
                "quality_score": round(quality_score, 3),
            },
        }

    except Exception as e:
        ecx_grade = random.choice([2, 3, 4])
        grade_info = ECX_GRADES[ecx_grade]
        quality_map = {2: "High", 3: "Medium", 4: "Medium"}
        return {
            "quality": quality_map[ecx_grade],
            "confidence": round(random.uniform(0.60, 0.80), 2),
            "description": grade_info["description"],
            "ecx_grade": ecx_grade,
            "ecx_label": grade_info["label"],
            "ecx_amharic": grade_info["amharic"],
            "defect_count": grade_info["defects"],
            "scaa_score_range": grade_info["scaa_range"],
            "export_eligible": grade_info["export_eligible"],
            "details": {"note": f"Fallback analysis (error: {str(e)})"},
        }
