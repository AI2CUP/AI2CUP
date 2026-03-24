"""
========================================
AI2CUP - Main FastAPI Application
========================================

Entry point for the AI2CUP backend server.

This file:
1. Creates the FastAPI application
2. Configures CORS (for frontend communication)
3. Registers all API route modules
4. Auto-trains the ML model on startup if not already trained
5. Serves static frontend files

Run with:
    cd backend
    uvicorn main:app --reload --port 8000
"""

import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ── Add backend dir to path for clean imports ──
sys.path.insert(0, os.path.dirname(__file__))


# ── Startup/Shutdown lifecycle ────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs on application startup.
    - Generates dataset if missing
    - Trains the ML model if not already trained
    """
    print("\n🌿 AI2CUP Backend Starting Up...")
    
    # ── Generate dataset if it doesn't exist ──
    data_path = os.path.join(os.path.dirname(__file__), "data", "coffee_prices.csv")
    if not os.path.exists(data_path):
        print("📊 Generating synthetic dataset...")
        from data.generate_dataset import generate_coffee_dataset
        df = generate_coffee_dataset()
        df.to_csv(data_path, index=False)
        print(f"   ✅ Generated {len(df)} records")
    else:
        print("📊 Dataset already exists")
    
    # ── Train model if not already trained ──
    model_path = os.path.join(os.path.dirname(__file__), "ml", "trained_model.joblib")
    if not os.path.exists(model_path):
        print("🤖 Training price prediction model...")
        from ml.price_model import train_and_save_model
        metrics = train_and_save_model()
        print(f"   ✅ Model trained (MAE: {metrics['mae_etb']} ETB / ${metrics['mae_usd']} USD, R²: {metrics['r2']})")
    else:
        print("🤖 Trained model already exists")
    
    print("🚀 AI2CUP Backend is ready!\n")
    
    yield  # Application runs here
    
    print("\n👋 AI2CUP Backend shutting down...")


# ── Create FastAPI app ────────────────────────────────────────
app = FastAPI(
    title="AI2CUP API",
    description=(
        "AI-powered platform for improving Ethiopian coffee trade. "
        "Features: Price Prediction, Quality Detection, Buyer/Seller Matching."
    ),
    version="1.0.0-mvp",
    lifespan=lifespan,
)


# ── CORS Configuration ──────────────────────────────────────
# Allow all origins for development/demo (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Register API Routes ─────────────────────────────────────
from routes.price import router as price_router
from routes.quality import router as quality_router
from routes.match import router as match_router

app.include_router(price_router, prefix="/api")
app.include_router(quality_router, prefix="/api")
app.include_router(match_router, prefix="/api")


# ── Health Check ─────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI2CUP API",
        "version": "1.0.0-mvp",
    }


# ── Serve Frontend Static Files ─────────────────────────────
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.isdir(frontend_dir):
    # Serve static assets (CSS, JS, images)
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html."""
        return FileResponse(os.path.join(frontend_dir, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "message": "AI2CUP API is running. Visit /docs for API documentation.",
            "docs": "/docs",
        }
