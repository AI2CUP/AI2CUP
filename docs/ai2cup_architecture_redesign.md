# AI2CUP — Architecture Redesign

> From MVP to Production-Ready, Scalable Architecture

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Full Project Structure](#2-full-project-structure)
3. [Backend Architecture](#3-backend-architecture)
4. [Frontend Architecture](#4-frontend-architecture)
5. [API Design](#5-api-design)
6. [ML Integration Strategy](#6-ml-integration-strategy)
7. [Future Extensibility](#7-future-extensibility)
8. [Development Workflow](#8-development-workflow)
9. [Coding Guidelines](#9-coding-guidelines)
10. [Migration Strategy](#10-migration-strategy)

---

## 1. Current State Analysis

### What Exists (MVP)

| Component | Current State | Issues |
|-----------|--------------|--------|
| **Backend** | FastAPI with routes/, ml/, data/ folders | ML logic imported directly inside route handlers; no service layer; schemas defined inside routes |
| **Frontend** | Single HTML + CSS + JS file served by backend | No component architecture; tightly coupled to backend static serving; not scalable |
| **ML Models** | 3 modules: price_model, quality_detector, matcher | Price model uses scikit-learn; quality uses heuristic + PIL; matcher is rule-based with hardcoded data |
| **Data** | Synthetic CSV + hardcoded seller/buyer lists | No database; no persistence layer |
| **Auth** | None | No user identity, no access control |
| **Deployment** | `uvicorn main:app --reload` | No Docker; no environment separation |

### Key Architectural Problems

1. **Routes directly import and call ML functions** — tight coupling means changing a model breaks the API
2. **Pydantic schemas live inside route files** — no reusability, hard to share between services
3. **Frontend is served by the backend** — couples deployment, prevents independent scaling
4. **Business logic is scattered** — some in routes, some in ML modules, some inline
5. **No configuration management** — paths hardcoded with `os.path.join(__file__)`
6. **No dependency injection** — makes testing and swapping implementations hard

---

## 2. Full Project Structure

```
AI2CUP/
├── apps/
│   ├── backend/                    # FastAPI application
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py             # FastAPI app factory
│   │   │   ├── config.py           # Settings via pydantic-settings
│   │   │   ├── dependencies.py     # Dependency injection providers
│   │   │   │
│   │   │   ├── api/                # API layer (thin routes)
│   │   │   │   ├── __init__.py
│   │   │   │   └── v1/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── router.py   # Aggregates all v1 routes
│   │   │   │       ├── price.py    # Price prediction endpoints
│   │   │   │       ├── quality.py  # Quality analysis endpoints
│   │   │   │       ├── match.py    # Marketplace endpoints
│   │   │   │       └── health.py   # Health/status endpoints
│   │   │   │
│   │   │   ├── schemas/            # Pydantic models (shared)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── price.py        # Price request/response schemas
│   │   │   │   ├── quality.py      # Quality schemas
│   │   │   │   ├── match.py        # Marketplace schemas
│   │   │   │   └── common.py       # Shared/base schemas
│   │   │   │
│   │   │   ├── services/           # Business logic layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── price_service.py
│   │   │   │   ├── quality_service.py
│   │   │   │   └── match_service.py
│   │   │   │
│   │   │   ├── ml/                 # ML model layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py         # Abstract ML model interface
│   │   │   │   ├── price_model.py  # Price prediction model
│   │   │   │   ├── quality_model.py # Quality detection model
│   │   │   │   ├── matcher.py      # Matching engine
│   │   │   │   └── registry.py     # Model registry & lifecycle
│   │   │   │
│   │   │   ├── data/               # Data access layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── repositories/   # Future: DB repositories
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── seed/           # Synthetic data & seeders
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── generate_dataset.py
│   │   │   │   │   └── marketplace.py  # Seller/buyer seed data
│   │   │   │   └── storage/        # File-based storage (CSV, joblib)
│   │   │   │       └── .gitkeep
│   │   │   │
│   │   │   └── core/               # Cross-cutting concerns
│   │   │       ├── __init__.py
│   │   │       ├── exceptions.py   # Custom exception classes
│   │   │       ├── constants.py    # ECX grades, regions, etc.
│   │   │       └── middleware.py   # CORS, logging, etc.
│   │   │
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_api/
│   │   │   ├── test_services/
│   │   │   └── test_ml/
│   │   │
│   │   ├── .env.example            # Environment template
│   │   ├── requirements.txt        # Python dependencies
│   │   ├── requirements-dev.txt    # Dev dependencies (pytest, etc.)
│   │   └── pyproject.toml          # Project metadata
│   │
│   └── frontend/                   # Vue 3 + Vite application
│       ├── public/
│       │   └── favicon.svg
│       ├── src/
│       │   ├── main.js             # App entry point
│       │   ├── App.vue             # Root component
│       │   │
│       │   ├── assets/             # Static assets (images, fonts)
│       │   │   └── styles/
│       │   │       ├── main.css    # Tailwind imports + custom base
│       │   │       └── variables.css
│       │   │
│       │   ├── components/         # Reusable UI components
│       │   │   ├── common/         # Buttons, inputs, badges, cards
│       │   │   │   ├── AppButton.vue
│       │   │   │   ├── AppCard.vue
│       │   │   │   ├── AppBadge.vue
│       │   │   │   ├── ConfidenceBar.vue
│       │   │   │   └── LoadingSpinner.vue
│       │   │   ├── layout/         # Layout components
│       │   │   │   ├── AppNavbar.vue
│       │   │   │   ├── AppFooter.vue
│       │   │   │   └── AppToast.vue
│       │   │   ├── price/          # Price prediction components
│       │   │   │   ├── PriceForm.vue
│       │   │   │   ├── PriceResult.vue
│       │   │   │   └── PriceChart.vue
│       │   │   ├── quality/        # Quality detection components
│       │   │   │   ├── ImageUploader.vue
│       │   │   │   └── QualityResult.vue
│       │   │   └── marketplace/    # Marketplace components
│       │   │       ├── ListingCard.vue
│       │   │       ├── MarketTabs.vue
│       │   │       └── MatchFilter.vue
│       │   │
│       │   ├── views/              # Page-level components
│       │   │   ├── HomeView.vue
│       │   │   ├── PriceView.vue
│       │   │   ├── QualityView.vue
│       │   │   └── MarketplaceView.vue
│       │   │
│       │   ├── services/           # API communication layer
│       │   │   ├── api.js          # Axios instance + interceptors
│       │   │   ├── priceService.js
│       │   │   ├── qualityService.js
│       │   │   └── matchService.js
│       │   │
│       │   ├── composables/        # Reusable logic (Vue 3 composition API)
│       │   │   ├── useToast.js
│       │   │   ├── useLoading.js
│       │   │   └── useEcxGrades.js
│       │   │
│       │   └── router/
│       │       └── index.js        # Vue Router config
│       │
│       ├── index.html
│       ├── vite.config.js
│       ├── tailwind.config.js
│       ├── postcss.config.js
│       ├── package.json
│       └── .env.example
│
├── infrastructure/                 # Deployment & orchestration
│   ├── docker/
│   │   ├── backend.Dockerfile
│   │   ├── frontend.Dockerfile
│   │   └── nginx.conf              # Production reverse proxy
│   └── docker-compose.yml          # Local dev orchestration
│
├── docs/                           # Documentation
│   ├── api.md                      # API reference
│   ├── architecture.md             # This document
│   └── deployment.md               # Deployment guide
│
├── .gitignore
├── README.md
└── Makefile                        # Common commands shortcut
```

### Why This Structure?

| Directory | Purpose | Why It Exists |
|-----------|---------|---------------|
| `apps/` | Groups deployable units | Clear boundary between backend and frontend — can deploy, version, and scale independently |
| `app/api/v1/` | Versioned API routes | Enables breaking changes in v2 without affecting v1 consumers |
| `app/schemas/` | Shared Pydantic models | Single source of truth for data shapes; reusable across services and tests |
| `app/services/` | Business logic | Decouples "what to do" from "how the API exposes it" and "how ML computes it" |
| `app/ml/` | ML model implementations | Isolates ML concerns; models can change independently of API or business logic |
| `app/data/` | Data access | Future DB repositories live here; seed data is organized separately |
| `app/core/` | Cross-cutting concerns | Constants, exceptions, middleware — shared utilities that don't belong to a specific feature |
| `infrastructure/` | Docker, nginx | Deployment config separate from application code |

---

## 3. Backend Architecture

### Layered Architecture (The Core Principle)

```mermaid
graph TD
    A["HTTP Request"] --> B["API Layer<br/>(app/api/v1/)"]
    B --> C["Service Layer<br/>(app/services/)"]
    C --> D["ML Layer<br/>(app/ml/)"]
    C --> E["Data Layer<br/>(app/data/)"]
    F["Schemas<br/>(app/schemas/)"] -.->|validates| B
    F -.->|types| C
    G["Config<br/>(app/config.py)"] -.->|settings| B
    G -.->|settings| C
    G -.->|settings| D

    style A fill:#4a5568,color:#fff
    style B fill:#3182ce,color:#fff
    style C fill:#38a169,color:#fff
    style D fill:#d69e2e,color:#fff
    style E fill:#e53e3e,color:#fff
    style F fill:#805ad5,color:#fff
    style G fill:#718096,color:#fff
```

> [!IMPORTANT]
> **The Golden Rule:** Each layer only talks to the layer directly below it.
> Routes → Services → ML/Data. Never Route → ML directly.

### 3.1 Config Layer (`app/config.py`)

Centralizes ALL configuration. No more `os.path.join(__file__)` scattered everywhere.

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # App
    app_name: str = "AI2CUP"
    app_version: str = "2.0.0"
    debug: bool = False

    # API
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173"]  # Vite dev server

    # ML
    model_dir: Path = Path("app/data/storage")
    price_model_filename: str = "trained_model.joblib"
    auto_train_on_startup: bool = True

    # Data
    dataset_path: Path = Path("app/data/storage/coffee_prices.csv")

    # Currency
    usd_to_etb: float = 57.0

    # Future: Database
    # database_url: str = "sqlite:///./ai2cup.db"

    # Future: Auth
    # jwt_secret: str = "change-me"
    # jwt_algorithm: str = "HS256"
    # jwt_expiry_minutes: int = 60

    class Config:
        env_file = ".env"
        env_prefix = "AI2CUP_"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
```

**Why?**
- Single place to change paths, secrets, feature flags
- Environment-aware: `.env` file overrides defaults
- `lru_cache` ensures one instance across the app
- Future DB/auth settings are commented out — ready to uncomment when needed

### 3.2 Core Layer (`app/core/`)

#### `exceptions.py` — Standardized Error Handling

```python
# app/core/exceptions.py

class AI2CUPError(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ModelNotReadyError(AI2CUPError):
    """Raised when ML model is not loaded/trained."""
    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' is not ready. It may need training.",
            code="MODEL_NOT_READY",
        )


class InvalidInputError(AI2CUPError):
    """Raised when input data fails business validation."""
    def __init__(self, message: str):
        super().__init__(message=message, code="INVALID_INPUT")


class DataNotFoundError(AI2CUPError):
    """Raised when required data is missing."""
    def __init__(self, resource: str):
        super().__init__(
            message=f"Required data not found: {resource}",
            code="DATA_NOT_FOUND",
        )
```

#### `constants.py` — Domain Constants (Single Source of Truth)

```python
# app/core/constants.py

ECX_GRADES = {
    1: {
        "label": "Grade 1 - Specialty",
        "amharic": "ልዩ ደረጃ",
        "description": "Premium specialty grade - suitable for direct export",
        "defects": "0-3 defects per 300g",
        "scaa_range": "85+",
        "export_eligible": True,
    },
    2: { ... },  # Grade 2 - Very Good
    3: { ... },  # Grade 3 - Good
    4: { ... },  # Grade 4 - Commercial
    5: { ... },  # Grade 5 - Below Standard
}

ECX_GRADE_LABELS = {
    1: "Grade 1 - Specialty (ልዩ ደረጃ)",
    2: "Grade 2 - Very Good (በጣም ጥሩ)",
    3: "Grade 3 - Good (ጥሩ)",
    4: "Grade 4 - Commercial (ንግድ)",
    5: "Grade 5 - Below Standard (ከደረጃ በታች)",
}

QUALITY_MAP = {1: "High", 2: "High", 3: "Medium", 4: "Medium", 5: "Low"}

ETHIOPIAN_REGIONS = [
    "Yirgacheffe", "Sidamo", "Harar", "Jimma",
    "Limu", "Guji", "Wellega", "Bench Maji",
]

COFFEE_VARIETIES = ["Heirloom", "Typica", "Bourbon", "Gesha", "74110", "74112"]

PROCESSING_METHODS = ["Washed", "Natural", "Honey"]
```

**Why?** ECX grades and Ethiopian regions appear in routes, services, schemas, and the frontend. Having a single authoritative source prevents inconsistency.

### 3.3 Schema Layer (`app/schemas/`)

```python
# app/schemas/common.py
from pydantic import BaseModel
from typing import Any


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    data: Any = None
    error: str | None = None
    code: str | None = None
```

```python
# app/schemas/price.py
from pydantic import BaseModel, Field


class PricePredictionRequest(BaseModel):
    """Input for coffee price prediction."""
    region: str = Field(..., examples=["Yirgacheffe"])
    month: int = Field(..., ge=1, le=12)
    altitude: float = Field(default=1800.0, ge=1000, le=3000)
    rainfall: float = Field(default=120.0, ge=0, le=500)
    variety: str = Field(default="Heirloom")
    processing: str = Field(default="Washed")
    ecx_grade: int = Field(default=3, ge=1, le=5)


class PricePredictionResult(BaseModel):
    """Price prediction output."""
    predicted_price_etb: float
    predicted_price_usd: float
    currency_primary: str = "ETB"
    currency_secondary: str = "USD"
    unit: str = "per kg"
    ecx_grade_label: str
    inputs: dict
    model_info: str
```

**Why separate?** Schemas need to be importable from routes, services, and tests—without pulling in ML dependencies.

### 3.4 Service Layer (`app/services/`) — THE KEY LAYER

This is the most important architectural addition. Services contain **business logic** and act as the bridge between the API and ML layers.

```python
# app/services/price_service.py
from app.schemas.price import PricePredictionRequest, PricePredictionResult
from app.ml.registry import ModelRegistry
from app.core.constants import ECX_GRADE_LABELS
from app.core.exceptions import ModelNotReadyError


class PriceService:
    """Business logic for price prediction."""

    def __init__(self, model_registry: ModelRegistry):
        self._registry = model_registry

    def predict(self, request: PricePredictionRequest) -> PricePredictionResult:
        """
        Predict coffee price.
        
        The service layer:
        1. Calls the ML model through the registry (not directly)
        2. Enriches the result with business context (ECX labels)
        3. Formats the response
        
        If we later add DB logging, caching, or audit trails, 
        they go HERE — not in routes or ML code.
        """
        model = self._registry.get_model("price")
        if model is None:
            raise ModelNotReadyError("price")

        # Call ML through abstract interface
        prediction = model.predict({
            "region": request.region,
            "month": request.month,
            "altitude": request.altitude,
            "rainfall": request.rainfall,
            "variety": request.variety,
            "processing": request.processing,
            "ecx_grade": request.ecx_grade,
        })

        return PricePredictionResult(
            predicted_price_etb=prediction["price_etb"],
            predicted_price_usd=prediction["price_usd"],
            ecx_grade_label=ECX_GRADE_LABELS.get(
                request.ecx_grade, f"Grade {request.ecx_grade}"
            ),
            inputs=request.model_dump(),
            model_info=model.model_info,
        )
```

```python
# app/services/quality_service.py
from app.schemas.quality import QualityAnalysisResult
from app.ml.registry import ModelRegistry
from app.core.exceptions import ModelNotReadyError, InvalidInputError

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class QualityService:
    """Business logic for quality analysis."""

    def __init__(self, model_registry: ModelRegistry):
        self._registry = model_registry

    def validate_image(self, content_type: str | None, file_size: int) -> None:
        """Validate image file before analysis."""
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidInputError(f"Invalid file type: {content_type}")
        if file_size > MAX_FILE_SIZE:
            raise InvalidInputError("File too large. Maximum 10MB.")
        if file_size == 0:
            raise InvalidInputError("Empty file uploaded.")

    def analyze(self, image_bytes: bytes) -> QualityAnalysisResult:
        """Analyze coffee bean image quality."""
        model = self._registry.get_model("quality")
        if model is None:
            raise ModelNotReadyError("quality")

        result = model.predict({"image_bytes": image_bytes})
        return QualityAnalysisResult(**result)
```

```python
# app/services/match_service.py
from app.schemas.match import MatchRequest, MatchResponse
from app.ml.registry import ModelRegistry


class MatchService:
    """Business logic for marketplace matching."""

    def __init__(self, model_registry: ModelRegistry):
        self._registry = model_registry

    def get_all_listings(self) -> dict:
        """Get all marketplace listings."""
        matcher = self._registry.get_model("matcher")
        return matcher.get_listings()

    def find_matches(self, request: MatchRequest) -> MatchResponse:
        """Find matching counterparties."""
        matcher = self._registry.get_model("matcher")
        matches = matcher.predict({
            "role": request.role,
            "region": request.region,
            "quality": request.quality,
            "max_price": request.max_price,
            "min_volume": request.min_volume,
        })

        return MatchResponse(
            matches=matches,
            total=len(matches),
            criteria=request.model_dump(),
        )
```

> [!TIP]
> **Why services matter:** Tomorrow you want to log every prediction to a database, add caching, or send email notifications on matches. With a service layer, you modify **one place** without touching routes or ML code.

### 3.5 API Layer (`app/api/v1/`) — Thin Routes

Routes should be *thin*. Their only job: parse HTTP → call service → return HTTP.

```python
# app/api/v1/price.py
from fastapi import APIRouter, Depends
from app.schemas.price import PricePredictionRequest, PricePredictionResult
from app.dependencies import get_price_service
from app.services.price_service import PriceService

router = APIRouter(prefix="/price", tags=["Price Prediction"])


@router.post("/predict", response_model=PricePredictionResult)
async def predict_price(
    request: PricePredictionRequest,
    service: PriceService = Depends(get_price_service),
):
    """Predict Ethiopian coffee price based on market factors."""
    return service.predict(request)
```

```python
# app/api/v1/quality.py
from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.quality import QualityAnalysisResult
from app.dependencies import get_quality_service
from app.services.quality_service import QualityService

router = APIRouter(prefix="/quality", tags=["Quality Analysis"])


@router.post("/analyze", response_model=QualityAnalysisResult)
async def analyze_quality(
    file: UploadFile = File(..., description="Coffee bean image"),
    service: QualityService = Depends(get_quality_service),
):
    """Analyze coffee bean quality using ECX grading standards."""
    contents = await file.read()
    service.validate_image(file.content_type, len(contents))
    return service.analyze(contents)
```

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import price, quality, match, health

api_router = APIRouter()
api_router.include_router(price.router)
api_router.include_router(quality.router)
api_router.include_router(match.router)
api_router.include_router(health.router)
```

### 3.6 Dependency Injection (`app/dependencies.py`)

```python
# app/dependencies.py
from functools import lru_cache
from app.config import get_settings
from app.ml.registry import ModelRegistry
from app.services.price_service import PriceService
from app.services.quality_service import QualityService
from app.services.match_service import MatchService


@lru_cache
def get_model_registry() -> ModelRegistry:
    """Singleton model registry."""
    settings = get_settings()
    registry = ModelRegistry(settings)
    return registry


def get_price_service() -> PriceService:
    return PriceService(model_registry=get_model_registry())


def get_quality_service() -> QualityService:
    return QualityService(model_registry=get_model_registry())


def get_match_service() -> MatchService:
    return MatchService(model_registry=get_model_registry())

# Future: Add database session, auth dependencies here
# def get_db() -> Generator[Session, None, None]: ...
# def get_current_user(token: str = Depends(oauth2_scheme)): ...
```

**Why dependency injection?**
- Routes don't create services — they *receive* them
- In tests, you can inject mock services without touching route code
- When you add a database, you inject the DB session into services here — one change, not fifty

### 3.7 Application Factory (`app/main.py`)

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.api.v1.router import api_router
from app.core.middleware import setup_middleware
from app.core.exceptions import AI2CUPError
from app.dependencies import get_model_registry
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    settings = get_settings()
    print(f"\n{settings.app_name} v{settings.app_version} starting...")

    # Initialize ML models
    registry = get_model_registry()
    registry.initialize()

    print(f"{settings.app_name} is ready!\n")
    yield
    print(f"\n{settings.app_name} shutting down...")


def create_app() -> FastAPI:
    """Application factory pattern."""
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} API",
        description=(
            "AI-powered platform for improving Ethiopian coffee trade. "
            "Features: Price Prediction, Quality Detection, Buyer/Seller Matching."
        ),
        version=settings.app_version,
        lifespan=lifespan,
    )

    # Middleware
    setup_middleware(app, settings)

    # Exception handlers
    @app.exception_handler(AI2CUPError)
    async def handle_app_error(request, exc: AI2CUPError):
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": exc.message, "code": exc.code},
        )

    # API routes
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
```

### Data Flow Summary

```
Client Request
    │
    ▼
┌──────────────────────────────┐
│  API Route (app/api/v1/)     │  ← Validates HTTP, extracts params
│  price.py: predict_price()   │
└──────────────┬───────────────┘
               │ calls
               ▼
┌──────────────────────────────┐
│  Service (app/services/)     │  ← Business logic, orchestration
│  PriceService.predict()      │
└──────────────┬───────────────┘
               │ calls
               ▼
┌──────────────────────────────┐
│  ML Model (app/ml/)          │  ← Pure prediction logic
│  PriceModel.predict()        │
└──────────────┬───────────────┘
               │ reads
               ▼
┌──────────────────────────────┐
│  Data (app/data/)            │  ← CSV / future DB
│  trained_model.joblib        │
└──────────────────────────────┘
```

---

## 4. Frontend Architecture

### 4.1 Technology Choices

| Tool | Version | Purpose |
|------|---------|---------|
| **Vue 3** | 3.x | Component framework with Composition API |
| **Vite** | 6.x | Build tool — instant HMR, fast builds |
| **Vue Router** | 4.x | Client-side routing |
| **Tailwind CSS** | 4.x | Utility-first CSS framework |
| **Axios** | 1.x | HTTP client with interceptors |

> [!NOTE]
> **No Pinia/Vuex initially.** The app's state is page-scoped (form data, results). Add Pinia later only when state needs to be shared across unrelated components (e.g., user auth state, cart).

### 4.2 Component Architecture

```mermaid
graph TD
    App["App.vue"] --> Navbar["AppNavbar"]
    App --> Router["RouterView"]
    App --> Footer["AppFooter"]
    App --> Toast["AppToast"]

    Router --> Home["HomeView"]
    Router --> Price["PriceView"]
    Router --> Quality["QualityView"]
    Router --> Market["MarketplaceView"]

    Price --> PF["PriceForm"]
    Price --> PR["PriceResult"]
    Price --> PC["PriceChart"]

    Quality --> IU["ImageUploader"]
    Quality --> QR["QualityResult"]

    Market --> MT["MarketTabs"]
    Market --> LC["ListingCard"]
    Market --> MF["MatchFilter"]

    style App fill:#3182ce,color:#fff
    style Router fill:#805ad5,color:#fff
    style Home fill:#38a169,color:#fff
    style Price fill:#38a169,color:#fff
    style Quality fill:#38a169,color:#fff
    style Market fill:#38a169,color:#fff
```

### 4.3 API Service Layer (Frontend)

```javascript
// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for consistent error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.error || error.message || 'Network error'
    return Promise.reject(new Error(message))
  }
)

// Future: Request interceptor for auth token
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token')
//   if (token) config.headers.Authorization = `Bearer ${token}`
//   return config
// })

export default api
```

```javascript
// src/services/priceService.js
import api from './api'

export const priceService = {
  predict(params) {
    return api.post('/price/predict', params)
  },

  // Future: price history, batch predictions, etc.
  // getHistory(region) { return api.get(`/price/history/${region}`) },
}
```

```javascript
// src/services/qualityService.js
import api from './api'

export const qualityService = {
  analyze(imageFile) {
    const formData = new FormData()
    formData.append('file', imageFile)
    return api.post('/quality/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
```

```javascript
// src/services/matchService.js
import api from './api'

export const matchService = {
  getListings() {
    return api.get('/match')
  },
  findMatches(criteria) {
    return api.post('/match/find', criteria)
  },
}
```

### 4.4 Composables (Reusable Logic)

```javascript
// src/composables/useLoading.js
import { ref } from 'vue'

export function useLoading() {
  const isLoading = ref(false)
  const error = ref(null)

  async function withLoading(fn) {
    isLoading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isLoading.value = false
    }
  }

  return { isLoading, error, withLoading }
}
```

```javascript
// src/composables/useToast.js
import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

export function useToast() {
  function show(message, type = 'info', duration = 4000) {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }

  return {
    toasts,
    success: (msg) => show(msg, 'success'),
    error: (msg) => show(msg, 'error'),
    info: (msg) => show(msg, 'info'),
  }
}
```

```javascript
// src/composables/useEcxGrades.js
export function useEcxGrades() {
  const grades = {
    1: { label: 'Grade 1 - Specialty', amharic: 'ልዩ ደረጃ', color: 'emerald' },
    2: { label: 'Grade 2 - Very Good', amharic: 'በጣም ጥሩ', color: 'green' },
    3: { label: 'Grade 3 - Good', amharic: 'ጥሩ', color: 'yellow' },
    4: { label: 'Grade 4 - Commercial', amharic: 'ንግድ', color: 'orange' },
    5: { label: 'Grade 5 - Below Standard', amharic: 'ከደረጃ በታች', color: 'red' },
  }

  function getGrade(grade) {
    return grades[grade] || { label: `Grade ${grade}`, amharic: '', color: 'gray' }
  }

  return { grades, getGrade }
}
```

### 4.5 Router Configuration

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'AI2CUP - Ethiopian Coffee Trade Platform' },
  },
  {
    path: '/price',
    name: 'price',
    component: () => import('../views/PriceView.vue'),
    meta: { title: 'Price Prediction - AI2CUP' },
  },
  {
    path: '/quality',
    name: 'quality',
    component: () => import('../views/QualityView.vue'),
    meta: { title: 'Quality Detection - AI2CUP' },
  },
  {
    path: '/marketplace',
    name: 'marketplace',
    component: () => import('../views/MarketplaceView.vue'),
    meta: { title: 'Marketplace - AI2CUP' },
  },
  // Future routes:
  // { path: '/login', name: 'login', ... },
  // { path: '/dashboard', name: 'dashboard', meta: { requiresAuth: true }, ... },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

// Update page title
router.afterEach((to) => {
  document.title = to.meta.title || 'AI2CUP'
})

// Future: Auth guard
// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth && !isAuthenticated()) next('/login')
//   else next()
// })

export default router
```

---

## 5. API Design

### 5.1 URL Structure

```
BASE: /api/v1

Price:
  POST /api/v1/price/predict          → Predict coffee price

Quality:
  POST /api/v1/quality/analyze        → Analyze bean image

Marketplace:
  GET  /api/v1/match                  → List all sellers & buyers
  POST /api/v1/match/find             → Find matching counterparties

Health:
  GET  /api/v1/health                 → Health check

Future:
  POST /api/v1/auth/login             → User login
  POST /api/v1/auth/register          → Registration
  GET  /api/v1/users/me               → Current user profile
  GET  /api/v1/price/history/:region  → Historical prices
```

### 5.2 Consistent Response Format

All responses follow the same shape:

**Success:**
```json
{
  "predicted_price_etb": 342.50,
  "predicted_price_usd": 6.01,
  "currency_primary": "ETB",
  "currency_secondary": "USD",
  "unit": "per kg",
  "ecx_grade_label": "Grade 3 - Good (ጥሩ)",
  "inputs": { ... },
  "model_info": "LinearRegression v1"
}
```

**Error:**
```json
{
  "success": false,
  "error": "Model 'price' is not ready.",
  "code": "MODEL_NOT_READY"
}
```

### 5.3 Versioning Strategy

| Version | Status | Changes |
|---------|--------|---------|
| `/api/v1/` | **Active** | Current MVP routes, refactored |
| `/api/v2/` | *Future* | Auth-aware routes, pagination, filtering |

When v2 is introduced, v1 continues to work. Both routers are registered in the same app:

```python
# Future: in main.py
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")
```

---

## 6. ML Integration Strategy

### 6.1 Abstract Base Model

This is the **key to swappable ML models**:

```python
# app/ml/base.py
from abc import ABC, abstractmethod
from typing import Any


class BaseMLModel(ABC):
    """
    Abstract interface for all ML models.

    Every ML model in the system implements this interface.
    This means the service layer NEVER knows whether it's calling
    a scikit-learn model, PyTorch, TensorFlow, or an external API.

    To add a new model:
    1. Create a class that inherits from BaseMLModel
    2. Implement predict() and load()
    3. Register it in the ModelRegistry
    """

    @property
    @abstractmethod
    def model_info(self) -> str:
        """Human-readable model description."""
        ...

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """Whether the model is loaded and ready for predictions."""
        ...

    @abstractmethod
    def load(self) -> None:
        """Load/initialize the model. Called once at startup."""
        ...

    @abstractmethod
    def predict(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Run prediction.

        Args:
            inputs: Dictionary of input features

        Returns:
            Dictionary of prediction results
        """
        ...

    def train(self, data_path: str | None = None) -> dict:
        """Optional: train/retrain the model. Override if supported."""
        raise NotImplementedError(f"{self.__class__.__name__} does not support training")
```

### 6.2 Concrete Implementations

```python
# app/ml/price_model.py
import joblib
import pandas as pd
from pathlib import Path
from app.ml.base import BaseMLModel
from app.config import get_settings


class PriceModel(BaseMLModel):
    """Scikit-learn price prediction model."""

    def __init__(self):
        self._model = None
        self._settings = get_settings()

    @property
    def model_info(self) -> str:
        return "LinearRegression v1 (scikit-learn)"

    @property
    def is_ready(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        model_path = self._settings.model_dir / self._settings.price_model_filename
        if model_path.exists():
            self._model = joblib.load(model_path)
        elif self._settings.auto_train_on_startup:
            self.train()

    def train(self, data_path: str | None = None) -> dict:
        """Train and save the price prediction model."""
        path = Path(data_path) if data_path else self._settings.dataset_path
        # ... (existing training logic from price_model.py)
        # Returns metrics dict

    def predict(self, inputs: dict) -> dict:
        input_df = pd.DataFrame([inputs])
        predicted_etb = self._model.predict(input_df)[0]
        predicted_etb = max(100, min(700, predicted_etb))
        etb_to_usd = 1 / self._settings.usd_to_etb

        return {
            "price_etb": round(predicted_etb, 2),
            "price_usd": round(predicted_etb * etb_to_usd, 2),
        }
```

### 6.3 Model Registry

```python
# app/ml/registry.py
from app.ml.base import BaseMLModel
from app.ml.price_model import PriceModel
from app.ml.quality_model import QualityModel
from app.ml.matcher import MatcherModel
from app.config import Settings


class ModelRegistry:
    """
    Central registry for all ML models.

    Manages model lifecycle (load, access, health).
    Adding a new model = register it here.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._models: dict[str, BaseMLModel] = {}

    def initialize(self) -> None:
        """Load and register all models at startup."""
        models = {
            "price": PriceModel(),
            "quality": QualityModel(),
            "matcher": MatcherModel(),
        }

        for name, model in models.items():
            print(f"  Loading model: {name}...")
            try:
                model.load()
                self._models[name] = model
                print(f"  ✓ {name} ready ({model.model_info})")
            except Exception as e:
                print(f"  ✗ {name} failed: {e}")

    def get_model(self, name: str) -> BaseMLModel | None:
        """Get a loaded model by name."""
        return self._models.get(name)

    def health(self) -> dict:
        """Health status of all models."""
        return {
            name: {
                "ready": model.is_ready,
                "info": model.model_info,
            }
            for name, model in self._models.items()
        }
```

### 6.4 Upgrade Path

This architecture makes model upgrades trivial:

```
Scenario: Replace LinearRegression with XGBoost

1. Create app/ml/price_model_v2.py
   class PriceModelV2(BaseMLModel):  # same interface
       def predict(self, inputs): ...  # XGBoost logic

2. In registry.py, change one line:
   "price": PriceModelV2(),  # was PriceModel()

3. NOTHING else changes. Routes, services, schemas — untouched.
```

```
Scenario: Move ML to a separate microservice

1. Create app/ml/price_model_remote.py
   class PriceModelRemote(BaseMLModel):
       def predict(self, inputs):
           response = httpx.post("http://ml-service:5000/predict", json=inputs)
           return response.json()

2. In registry.py:
   "price": PriceModelRemote(),

3. Deploy the ML microservice separately. Backend doesn't know or care.
```

---

## 7. Future Extensibility

### 7.1 Authentication (JWT)

```
When to add: When you need user accounts, personalized dashboards, or API keys.

Files to create/modify:
  CREATE: app/core/security.py          → JWT token creation/verification
  CREATE: app/schemas/auth.py           → Login/Register schemas
  CREATE: app/services/auth_service.py  → Auth business logic
  CREATE: app/api/v1/auth.py            → Login/register endpoints
  MODIFY: app/dependencies.py           → Add get_current_user dependency
  MODIFY: app/config.py                 → Uncomment JWT settings

Protected routes become:
  @router.get("/protected")
  async def protected(user = Depends(get_current_user)):
      ...
```

### 7.2 Database (PostgreSQL)

```
When to add: When you need persistent storage (user data, prediction history, 
  real marketplace listings).

Files to create/modify:
  CREATE: app/data/database.py          → SQLAlchemy engine/session
  CREATE: app/data/models/              → SQLAlchemy ORM models
  CREATE: app/data/repositories/        → Data access methods
  MODIFY: app/dependencies.py           → Add get_db dependency
  MODIFY: app/config.py                 → Uncomment database_url
  MODIFY: app/services/*               → Inject db session, use repositories

Services gain a db parameter:
  class PriceService:
      def __init__(self, registry, db: Session):
          self._db = db

      def predict(self, request):
          result = ...
          # Log prediction to DB
          self._db.add(PredictionLog(...))
          self._db.commit()
          return result
```

### 7.3 Real-Time Features (WebSockets)

```
When to add: Live price updates, marketplace notifications.

Files to create:
  CREATE: app/api/v1/ws.py              → WebSocket endpoints
  CREATE: app/services/notification.py  → Event broadcasting

  @router.websocket("/ws/prices")
  async def price_stream(websocket: WebSocket):
      await websocket.accept()
      while True:
          prices = get_latest_prices()
          await websocket.send_json(prices)
          await asyncio.sleep(30)
```

### 7.4 Payments

```
When to add: Marketplace transactions, premium features.

Files to create:
  CREATE: app/services/payment_service.py   → Payment orchestration
  CREATE: app/api/v1/payments.py            → Payment endpoints
  CREATE: app/schemas/payment.py            → Payment schemas

The service layer acts as the integration point:
  class PaymentService:
      def __init__(self, payment_gateway: PaymentGateway, db: Session):
          ...
      def process_payment(self, order): ...
```

### 7.5 Docker Deployment

```yaml
# infrastructure/docker-compose.yml
version: "3.9"

services:
  backend:
    build:
      context: ./apps/backend
      dockerfile: ../../infrastructure/docker/backend.Dockerfile
    ports:
      - "8000:8000"
    env_file: ./apps/backend/.env
    # Future: depends_on: [db, redis]

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: ../../infrastructure/docker/frontend.Dockerfile
    ports:
      - "3000:80"

  # Future services:
  # db:
  #   image: postgres:16
  #   volumes: [pgdata:/var/lib/postgresql/data]
  #   environment: ...
  #
  # ml-service:
  #   build: ./services/ml
  #   ports: ["5001:5000"]
  #   deploy:
  #     resources:
  #       reservations:
  #         devices:
  #           - capabilities: [gpu]
```

### Extensibility Summary

```mermaid
graph LR
    subgraph "Phase 1 (Now)"
        A["FastAPI + Vue 3"]
        B["File-based data"]
        C["Embedded ML"]
    end

    subgraph "Phase 2 (Next)"
        D["+ JWT Auth"]
        E["+ PostgreSQL"]
        F["+ Docker"]
    end

    subgraph "Phase 3 (Scale)"
        G["+ WebSockets"]
        H["+ ML Microservice"]
        I["+ Redis Cache"]
    end

    subgraph "Phase 4 (Grow)"
        J["+ Payments"]
        K["+ Worker Queues"]
        L["+ CDN / S3"]
    end

    A --> D --> G --> J
    B --> E --> I --> K
    C --> F --> H --> L

    style A fill:#3182ce,color:#fff
    style D fill:#38a169,color:#fff
    style G fill:#d69e2e,color:#fff
    style J fill:#e53e3e,color:#fff
```

---

## 8. Development Workflow

### 8.1 Running Backend

```bash
# From project root
cd apps/backend

# Create virtual environment (first time)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run dev server
uvicorn app.main:app --reload --port 8000

# API docs available at:
#   http://localhost:8000/docs       (Swagger UI)
#   http://localhost:8000/redoc      (ReDoc)
```

### 8.2 Running Frontend

```bash
# From project root
cd apps/frontend

# Install dependencies (first time)
npm install

# Copy environment file
cp .env.example .env

# Run dev server (with hot reload)
npm run dev

# Frontend available at:
#   http://localhost:5173
```

### 8.3 Environment Variables

**Backend** (`apps/backend/.env.example`):
```ini
# App
AI2CUP_DEBUG=true
AI2CUP_APP_VERSION=2.0.0-dev

# CORS (comma-separated origins)
AI2CUP_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# ML
AI2CUP_AUTO_TRAIN_ON_STARTUP=true
AI2CUP_MODEL_DIR=app/data/storage

# Currency
AI2CUP_USD_TO_ETB=57.0

# Future
# AI2CUP_DATABASE_URL=postgresql://user:pass@localhost:5432/ai2cup
# AI2CUP_JWT_SECRET=your-secret-key
```

**Frontend** (`apps/frontend/.env.example`):
```ini
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=AI2CUP
# Future:
# VITE_WS_URL=ws://localhost:8000/ws
```

### 8.4 Dev vs Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Backend | `uvicorn --reload` on port 8000 | `gunicorn` with workers, behind nginx |
| Frontend | Vite dev server on port 5173 | `npm run build` → static files served by nginx |
| CORS | Allow localhost origins | Restrict to production domain |
| Debug | `AI2CUP_DEBUG=true` | `AI2CUP_DEBUG=false` |
| ML Training | Auto-train on startup | Pre-trained models mounted via Docker volumes |
| Database | SQLite (future) | PostgreSQL (future) |

---

## 9. Coding Guidelines

### 9.1 Where Logic Lives (CRITICAL)

> [!CAUTION]
> The #1 cause of unmaintainable code is putting logic in the wrong place.

| Logic Type | WHERE IT GOES | WHERE IT DOES NOT GO |
|------------|---------------|----------------------|
| HTTP parsing, status codes, headers | `api/v1/` routes | ❌ Services, ML |
| Business rules, validation, orchestration | `services/` | ❌ Routes, ML models |
| ML prediction, training | `ml/` | ❌ Routes, services |
| Data validation, shape enforcement | `schemas/` | ❌ Routes, services |
| Domain constants (ECX grades, regions) | `core/constants.py` | ❌ Scattered across files |
| Error definitions | `core/exceptions.py` | ❌ ad-hoc `raise HTTPException` |
| Configuration values | `config.py` | ❌ Hardcoded in code |

### 9.2 Naming Conventions

**Python (Backend):**
```python
# Files: snake_case
price_service.py, quality_model.py

# Classes: PascalCase
class PriceService:
class PriceModel(BaseMLModel):

# Functions/methods: snake_case
def predict_price():
def get_all_listings():

# Constants: UPPER_SNAKE_CASE
ECX_GRADES = { ... }
MAX_FILE_SIZE = 10 * 1024 * 1024

# Private methods: _leading_underscore
def _validate_input(self):
```

**JavaScript/Vue (Frontend):**
```javascript
// Files: camelCase for .js, PascalCase for .vue
priceService.js, useLoading.js
PriceForm.vue, AppNavbar.vue

// Functions: camelCase
function predictPrice() { }

// Components: PascalCase in templates
<PriceForm />
<AppButton />

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = '...'

// Composables: use* prefix
function useLoading() { }
function useToast() { }
```

### 9.3 Folder Responsibilities

| Folder | Responsibility | Rule of Thumb |
|--------|---------------|---------------|
| `api/v1/` | Accept HTTP, return HTTP | <20 lines per route function |
| `schemas/` | Define data shapes | No logic, only validation |
| `services/` | Orchestrate business flow | Can call ML + Data layers |
| `ml/` | Pure ML operations | No HTTP awareness, no business rules |
| `data/` | Raw data access | Future: SQL queries, file I/O |
| `core/` | Shared utilities | If 2+ modules need it, it's core |
| `components/` | Render UI | No API calls (use parent or composable) |
| `views/` | Page layout + orchestration | Import components, call services |
| `services/` (FE) | API communication | No UI rendering |
| `composables/` | Reusable logic | No DOM manipulation |

### 9.4 Common Mistakes to Avoid

| ❌ Don't | ✅ Do |
|----------|-------|
| Import ML models inside route functions | Call service methods from routes |
| Hardcode file paths | Use `config.py` settings |
| Define Pydantic models in route files | Put schemas in `schemas/` |
| Mix HTTP concerns (status codes) in services | Return data/raise exceptions in services; let routes handle HTTP |
| Create huge "god" components | Break into small, focused components |
| Store API base URL in component code | Use environment variables via `import.meta.env` |
| Catch-all `except Exception` everywhere | Catch specific exceptions; let unexpected ones propagate |
| `from ml.price_model import predict_price` in a route | Use dependency injection: `service = Depends(get_price_service)` |
| Put validation logic in ML models | Validate in schemas (structure) and services (business rules) |

---

## 10. Migration Strategy

### Step-by-Step Migration from MVP

> [!IMPORTANT]
> Migrate incrementally. Each step should produce a working system.

#### Phase 1: Backend Restructure (No Breaking API Changes)

```
Step 1: Create the new folder structure under apps/backend/app/
Step 2: Move constants → app/core/constants.py
Step 3: Move schemas out of routes → app/schemas/
Step 4: Create app/ml/base.py (abstract interface)
Step 5: Wrap existing ML modules with BaseMLModel interface
Step 6: Create ModelRegistry
Step 7: Create services that call registry instead of ML directly
Step 8: Rewrite routes to be thin (call services, use Depends)
Step 9: Create app/config.py with pydantic-settings
Step 10: Wire up main.py with app factory
Step 11: Test: all /api/v1/ endpoints work identically
```

#### Phase 2: Frontend Migration

```
Step 1: Scaffold Vue 3 + Vite project in apps/frontend/
Step 2: Set up Tailwind CSS
Step 3: Create API services (axios)
Step 4: Build layout components (Navbar, Footer)
Step 5: Migrate Price section → PriceView + PriceForm + PriceResult
Step 6: Migrate Quality section → QualityView + ImageUploader + QualityResult
Step 7: Migrate Marketplace → MarketplaceView + ListingCard + MarketTabs
Step 8: Set up Vue Router with all pages
Step 9: Test: full feature parity with old frontend
Step 10: Remove old frontend/ directory
```

#### Phase 3: Polish & Infrastructure

```
Step 1: Add Docker files
Step 2: Create docker-compose.yml
Step 3: Add API tests (pytest)
Step 4: Create Makefile for common commands
Step 5: Write deployment docs
```

---

## Summary

| Aspect | Before (MVP) | After (Redesign) |
|--------|-------------|------------------|
| **Backend** | Flat routes importing ML directly | Layered: API → Service → ML with DI |
| **Frontend** | Single HTML/CSS/JS | Vue 3 + Vite with component architecture |
| **ML Models** | Hardcoded in routes | Abstract interface + registry pattern |
| **Data** | Hardcoded + CSV | Storage layer ready for DB migration |
| **Config** | Scattered `os.path.join` | Centralized pydantic-settings |
| **Error Handling** | `try/except HTTPException` | Custom exceptions + global handler |
| **API** | `/api/predict-price` | `/api/v1/price/predict` (versioned) |
| **Extensibility** | Major rewrite needed | Add features by adding files, not modifying existing ones |
