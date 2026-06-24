"""
========================================
AI2CUP - Coffee Quality Model Training
========================================

Trains a MobileNetV2 CNN on the downloaded coffee bean dataset.
Saves the trained model weights to the storage directory.

Run directly:
    python -m app.ml.train_quality_model
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

from app.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def train_model(
    data_dir: Path,
    model_save_path: Path,
    num_epochs: int = 1,
    batch_size: int = 32,
) -> None:
    """
    Train a MobileNetV2 model for coffee bean quality classification.
    """
    logger.info(f"Starting training on data in: {data_dir}")
    
    # Check device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # ── 1. Data Preparation ──
    # Standard ImageNet transforms + some simple data augmentation
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    }

    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return

    # Load the dataset
    image_dataset = datasets.ImageFolder(data_dir, data_transforms['train'])
    
    # We map the classes (Grade_A, Grade_B, etc) to indices.
    class_names = image_dataset.classes
    logger.info(f"Found classes: {class_names}")
    num_classes = len(class_names)
    
    # We will use the entire 'train' folder for training to keep it simple for the MVP
    # In a real scenario, we'd split into train/val.
    dataloader = DataLoader(image_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    dataset_size = len(image_dataset)
    logger.info(f"Total training images: {dataset_size}")

    # ── 2. Model Setup ──
    # Load a pre-trained MobileNetV2
    logger.info("Loading pre-trained MobileNetV2...")
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    # Freeze early layers
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace the classifier head
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, num_classes)
    
    model = model.to(device)

    # ── 3. Training Loop ──
    criterion = nn.CrossEntropyLoss()
    # Optimize only the classifier parameters
    optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

    logger.info(f"Starting training for {num_epochs} epochs...")
    for epoch in range(num_epochs):
        logger.info(f"Epoch {epoch}/{num_epochs - 1}")
        logger.info("-" * 10)

        model.train()
        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

            # backward + optimize
            loss.backward()
            optimizer.step()

            # statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / dataset_size
        epoch_acc = running_corrects.double() / dataset_size

        logger.info(f"Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

    logger.info("Training complete.")

    # ── 4. Save Model ──
    logger.info(f"Saving model to {model_save_path}")
    torch.save(model.state_dict(), model_save_path)
    logger.info("Saved successfully!")


if __name__ == "__main__":
    print("\n☕ AI2CUP - Quality Model Training\n")
    
    settings = get_settings()
    data_path = Path(__file__).parent.parent / "data" / "storage" / "images" / "train"
    model_path = Path(__file__).parent.parent / "data" / "storage" / "quality_model.pth"
    
    # Train for 1 epoch by default for testing speed.
    train_model(data_path, model_path, num_epochs=1, batch_size=32)
