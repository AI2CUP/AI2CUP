"""
========================================
AI2CUP - Coffee Quality Dataset Fetcher
========================================

Downloads a coffee bean quality dataset from Hugging Face
and organizes it into the project's image storage.

Run directly:
    python -m app.data.seed.fetch_quality_data
"""

from __future__ import annotations

import logging
import os
import shutil
import sys
from pathlib import Path

# ── Force Cache Location (must be before HF imports) ──
# We try to load it from environment or a known path on data-disk
HF_CACHE_PATH = "/mnt/data-disk/ai2cup/AI2CUP/apps/backend/.hf_cache"
os.environ["HF_HOME"] = HF_CACHE_PATH
os.environ["HF_DATASETS_CACHE"] = HF_CACHE_PATH
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE_PATH
# Also set TMPDIR to avoid root partition issues
os.environ["TMPDIR"] = HF_CACHE_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    from datasets import load_dataset
    from huggingface_hub import login
except ImportError:
    logger.error("Missing dependencies. Run: pip install huggingface_hub datasets")
    exit(1)

from app.config import get_settings


def get_label_from_path(image) -> str:
    """Attempt to extract label from image filename if possible."""
    if hasattr(image, "filename") and image.filename:
        path_str = str(image.filename).upper()
        if "CGA" in path_str: return "Grade_A"
        if "CGB" in path_str: return "Grade_B"
        if "CGC" in path_str: return "Grade_C"
        if "CGD" in path_str: return "Grade_D"
    return "unlabeled"


def manual_organize_from_cache(storage_path: Path) -> int:
    """Manually organize images from the HF cache since load_dataset lacks labels."""
    snapshot_base = Path(os.environ["HF_HOME"]) / "hub/datasets--SamruddhK--coffee-bean-grading-dataset/snapshots"
    if not snapshot_base.exists():
        logger.error(f"Snapshot base {snapshot_base} not found.")
        return 0
        
    snapshots = [d for d in snapshot_base.iterdir() if d.is_dir()]
    if not snapshots:
        logger.error("No snapshots found in cache.")
        return 0
        
    src_dir = snapshots[0]
    # We'll put everything in 'train' for now
    dest_base = storage_path / "train"
    
    mapping = {
        "CGA": "Grade_A",
        "CGB": "Grade_B",
        "CGC": "Grade_C",
        "CGD": "Grade_D"
    }
    
    total_count = 0
    for src_name, label in mapping.items():
        # Path: CGA/images/*.jpg
        src_images = src_dir / src_name / "images"
        if not src_images.exists():
            logger.warning(f"Source images not found for {src_name}")
            continue
            
        target_path = dest_base / label
        target_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Copying images from {src_name} to {label}...")
        count = 0
        for img_file in src_images.glob("*.jpg"):
            # Use copy2 to follow symlinks in HF cache
            shutil.copy2(img_file, target_path / img_file.name)
            count += 1
            if count % 200 == 0:
                logger.info(f"Copied {count} images...")
        
        total_count += count
        
    return total_count


def fetch_quality_data(
    dataset_name: str = "SamruddhK/coffee-bean-grading-dataset",
) -> None:
    """
    Fetch and organize coffee grading dataset.
    """
    settings = get_settings()
    
    # ── Authentication ──
    if settings.hf_token and not settings.hf_token.startswith("hf_placeholder"):
        logger.info("Authenticating with Hugging Face...")
        try:
            login(token=settings.hf_token)
        except Exception as e:
            logger.warning(f"Login failed: {e}")

    storage_path = Path(__file__).parent.parent / "storage" / "images"
    storage_path.mkdir(parents=True, exist_ok=True)
    
    # ── Trigger Download (if not already in cache) ──
    logger.info(f"Ensuring dataset '{dataset_name}' is in cache...")
    try:
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id=dataset_name, repo_type="dataset", local_files_only=False)
    except Exception as e:
        logger.error(f"Download check failed: {e}")
        # Continue anyway, maybe it's partially there

    # ── Manual Organization ──
    logger.info("Organizing images from cache to storage...")
    try:
        # Clean up previous failed attempts if they exist
        unlabeled_dir = storage_path / "train" / "unlabeled"
        if unlabeled_dir.exists():
            shutil.rmtree(unlabeled_dir)
            
        count = manual_organize_from_cache(storage_path)
        logger.info(f"Successfully organized {count} images.")
    except Exception as e:
        logger.error(f"Organization failed: {e}")

    logger.info("Done!")
    logger.info(f"Images are ready in {storage_path}")
    logger.info("You can now use these images to train a CNN-based QualityModel.")


if __name__ == "__main__":
    print("\n☕ AI2CUP - Quality Data Seeding Tool\n")
    fetch_quality_data()
