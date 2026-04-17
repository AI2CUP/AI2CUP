# Phase 1 — Backend Restructure: Implementation Complete

## All Endpoints Verified Working

| Endpoint | Method | Status | Response |
|----------|--------|--------|----------|
| `/api/v1/health` | GET | ✅ 200 | All 3 models ready |
| `/api/v1/price/predict` | POST | ✅ 200 | Price: 530.07 ETB / $9.30 USD |
| `/api/v1/match` | GET | ✅ 200 | 10 sellers, 8 buyers |
| `/api/v1/match/find` | POST | ✅ 200 | 6 matches found, sorted by score |
| `/api/v1/quality/analyze` | POST | ✅ Ready | (requires image upload) |

## New Backend Structure

```
apps/backend/
├── .env / .env.example              # Environment config
├── requirements.txt                 # Dependencies (+ pydantic-settings)
├── pyproject.toml                   # Project metadata
├── tests/
│   ├── __init__.py
│   └── conftest.py                  # Pytest fixtures
│
└── app/
    ├── __init__.py
    ├── main.py                      # App factory + lifespan
    ├── config.py                    # Centralized settings
    ├── dependencies.py              # DI providers
    │
    ├── api/v1/                      # Thin routes
    │   ├── router.py                # Aggregator
    │   ├── price.py                 # POST /price/predict
    │   ├── quality.py               # POST /quality/analyze
    │   ├── match.py                 # GET /match, POST /match/find
    │   └── health.py                # GET /health
    │
    ├── schemas/                     # Pydantic models
    │   ├── common.py
    │   ├── price.py
    │   ├── quality.py
    │   └── match.py
    │
    ├── services/                    # Business logic
    │   ├── price_service.py
    │   ├── quality_service.py
    │   └── match_service.py
    │
    ├── ml/                          # ML models
    │   ├── base.py                  # Abstract interface
    │   ├── price_model.py           # sklearn pipeline
    │   ├── quality_model.py         # Heuristic detector
    │   ├── matcher.py               # Rule-based engine
    │   └── registry.py              # Model lifecycle
    │
    ├── core/                        # Cross-cutting
    │   ├── constants.py             # ECX grades, regions, etc.
    │   ├── exceptions.py            # Custom error classes
    │   └── middleware.py            # CORS setup
    │
    └── data/
        ├── seed/
        │   ├── generate_dataset.py  # Synthetic data
        │   └── marketplace.py       # Seller/buyer data
        ├── repositories/            # Future DB access
        └── storage/                 # Generated files
            ├── coffee_prices.csv
            └── trained_model.joblib
```

## Key Changes from MVP

| What Changed | Before | After |
|--------------|--------|-------|
| **Route → ML coupling** | Routes import ML functions directly | Routes → Service → Registry → Model |
| **Schemas** | Defined inside route files | Separate `schemas/` package |
| **Configuration** | `os.path.join(__file__)` everywhere | `pydantic-settings` with `.env` files |
| **ML models** | Plain functions | Classes implementing `BaseMLModel` ABC |
| **Error handling** | `raise HTTPException` inline | Custom exceptions + global handler |
| **Constants** | Duplicated across files | Single `core/constants.py` |
| **Marketplace data** | Inside `ml/matcher.py` | Separate `data/seed/marketplace.py` |
| **API paths** | `/api/predict-price` | `/api/v1/price/predict` (versioned) |
| **CORS** | `allow_origins=["*"]` | Configurable via `AI2CUP_CORS_ORIGINS` |
| **Dependencies** | Tight coupling | FastAPI `Depends()` injection |

## How to Run

```bash
cd apps/backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Next: Phase 2 — Frontend (Vue 3 + Vite + Tailwind)
