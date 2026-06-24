"""
========================================
AI2CUP - Coffee Quality Detection Model
========================================

Simulates coffee bean quality analysis using the ECX grading system.
Combines basic image analysis with heuristic scoring.

Implements BaseMLModel so it can be swapped for a real CNN-based
detector (e.g., ResNet, EfficientNet) without changing any other layer.
"""

from __future__ import annotations

import io
import random
from typing import Any

import numpy as np
from PIL import Image

from app.core.constants import ECX_GRADES, QUALITY_MAP
from app.ml.base import BaseMLModel

try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False


class QualityModel(BaseMLModel):
    """
    CNN-based coffee quality detector with heuristic fallback.
    
    If quality_model.pth is found, it uses MobileNetV2 for inference.
    Otherwise, it falls back to basic PIL image analysis.
    """

    def __init__(self) -> None:
        self._loaded = False
        self.model = None
        self.device = None
        self.transform = None

    @property
    def model_info(self) -> str:
        if self.model:
            return "MobileNetV2 CNN (PyTorch)"
        return "Heuristic v1 (PIL + numpy) [Fallback]"

    @property
    def is_ready(self) -> bool:
        return self._loaded

    def load(self) -> None:
        """Attempt to load the PyTorch model."""
        import os
        from pathlib import Path
        
        self._loaded = True
        
        if not TORCH_AVAILABLE:
            return
            
        model_path = Path(__file__).resolve().parent.parent.parent / "ckpt" / "quality_model.pth"
        if not model_path.exists():
            return
            
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # Load MobileNetV2 architecture
            self.model = models.mobilenet_v2(weights=None)
            num_ftrs = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(num_ftrs, 4) # 4 classes (Grade_A to D)
            
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        except Exception as e:
            # If it fails to load, we just fallback to heuristic
            print(f"Failed to load CNN model: {e}")
            self.model = None

    def predict(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Analyze a coffee bean image and return ECX-based quality assessment.

        Args:
            inputs: dict with key "image_bytes" (raw bytes of the image)

        Returns:
            dict with ECX grade, confidence, and detailed analysis
        """
        image_bytes: bytes = inputs["image_bytes"]

        try:
            if self.model is not None and self.transform is not None:
                return self._analyze_cnn(image_bytes)
            return self._analyze_image(image_bytes)
        except Exception as e:
            return self._fallback_analysis(str(e))

    def _analyze_cnn(self, image_bytes: bytes) -> dict[str, Any]:
        """Inference using the PyTorch CNN model."""
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_class = torch.max(probabilities, 0)
            
        # Map Class (0,1,2,3) to ECX Grade (1,2,3,4)
        # Class 0: Grade_A -> ECX 1
        # Class 1: Grade_B -> ECX 2
        # Class 2: Grade_C -> ECX 3
        # Class 3: Grade_D -> ECX 4
        ecx_grade = int(predicted_class.item()) + 1
        conf_val = float(confidence.item())
        
        grade_info = ECX_GRADES[ecx_grade]
        
        return {
            "quality": QUALITY_MAP[ecx_grade],
            "confidence": round(conf_val, 2),
            "description": grade_info["description"],
            "ecx_grade": ecx_grade,
            "ecx_label": grade_info["label"],
            "ecx_amharic": grade_info["amharic"],
            "defect_count": grade_info["defects"],
            "scaa_score_range": grade_info["scaa_range"],
            "export_eligible": grade_info["export_eligible"],
            "details": {
                "inference_engine": "PyTorch CNN",
                "class_probabilities": [round(p.item(), 3) for p in probabilities]
            },
        }

    def _analyze_image(self, image_bytes: bytes) -> dict[str, Any]:
        """Core image analysis logic."""
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_resized = image.resize((224, 224))
        pixels = np.array(image_resized, dtype=np.float32)

        # ── Extract features ──
        brightness = np.mean(pixels)
        r_mean = np.mean(pixels[:, :, 0])
        b_mean = np.mean(pixels[:, :, 2])

        # Color uniformity (lower std = more uniform = fewer defects)
        uniformity = 1.0 - (np.std(pixels) / 128.0)
        uniformity = max(0.0, min(1.0, uniformity))

        # Warmth score (brown tones = properly dried beans)
        warmth_score = (r_mean - b_mean) / 255.0

        # ── Compute quality score (0-1) ──
        quality_score = (
            0.30 * uniformity
            + 0.25 * (warmth_score + 0.5)
            + 0.20 * (brightness / 255.0)
            + 0.25 * random.uniform(0.3, 0.9)
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

        return {
            "quality": QUALITY_MAP[ecx_grade],
            "confidence": float(confidence),
            "description": grade_info["description"],
            "ecx_grade": ecx_grade,
            "ecx_label": grade_info["label"],
            "ecx_amharic": grade_info["amharic"],
            "defect_count": grade_info["defects"],
            "scaa_score_range": grade_info["scaa_range"],
            "export_eligible": grade_info["export_eligible"],
            "details": {
                "image_size": f"{image.width}x{image.height}",
                "brightness": float(round(brightness, 1)),
                "color_uniformity": float(round(uniformity, 3)),
                "warmth_index": float(round(warmth_score, 3)),
                "quality_score": float(round(quality_score, 3)),
            },
        }

    def _fallback_analysis(self, error_msg: str) -> dict[str, Any]:
        """Fallback when image processing fails."""
        ecx_grade = random.choice([2, 3, 4])
        grade_info = ECX_GRADES[ecx_grade]

        return {
            "quality": QUALITY_MAP[ecx_grade],
            "confidence": float(round(random.uniform(0.60, 0.80), 2)),
            "description": grade_info["description"],
            "ecx_grade": ecx_grade,
            "ecx_label": grade_info["label"],
            "ecx_amharic": grade_info["amharic"],
            "defect_count": grade_info["defects"],
            "scaa_score_range": grade_info["scaa_range"],
            "export_eligible": grade_info["export_eligible"],
            "details": {"note": f"Fallback analysis (error: {error_msg})"},
        }
