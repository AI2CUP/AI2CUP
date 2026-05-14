# Skill: API & Environment Standards

**Objective**: Ensure a robust, type-safe backend and a consistent developer experience.

## 🐍 Python & FastAPI

### 1. Type Safety
Always use Type Hints and Pydantic models for request/response validation.
```python
from pydantic import BaseModel

class CoffeeResponse(BaseModel):
    id: str
    price: float
    grade: str
```

### 2. Virtual Environments
Always use the local virtual environment for running scripts and servers.
- **Path**: `apps/backend/venv/`
- **Rule**: If running a command via `make` or terminal, prefix with `./venv/bin/` if applicable.

## ✅ Quality Assurance (QA)

### 1. Linting with Ruff
- **Rule**: Run `make lint` before every commit.
- **Config**: Respect the rules defined in `pyproject.toml` or `ruff.toml` (if present).
- **Auto-Fix**: Use `make format` to resolve stylistic issues automatically.

### 2. Testing with Pytest
- **Rule**: Every new feature must have a corresponding test in `apps/backend/tests/`.
- **Naming**: Test files must start with `test_`.
- **Execution**: Run `make test` to verify the entire suite.

## 🛠 Command Patterns
Refer to the [Makefile](file:///mnt/data-disk/ai2cup/AI2CUP/Makefile) for standardized commands:
- `make install`: Sets up venv and installs dependencies.
- `make dev-backend`: Starts the server using `./venv/bin/uvicorn`.
- `make lint`: Runs ruff check.
- `make format`: Runs ruff format.
- `make test`: Runs pytest.

## 📦 Dependency Management
Add new dependencies to `requirements.txt` (prod) or `requirements-dev.txt` (tools like ruff, pytest).
