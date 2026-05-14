# Skill: CI/CD & Automation

**Objective**: Ensure code quality is maintained through automated testing and linting.

## 🛠 CI Standards

### 1. Automated Checks
Every PR should trigger:
- **Linting**: `make lint` (using Ruff).
- **Formatting**: `make format` (checking with Ruff).
- **Testing**: `make test` (using Pytest).

### 2. GitHub Actions (Proposed)
When setting up CI, follow this structure in `.github/workflows/ci.yml`:
- **Trigger**: On push to `main` or pull requests.
- **Environment**: Use `python:3.10` and `node:20`.
- **Steps**:
  1. Checkout code.
  2. Setup Python environment.
  3. Install dependencies via `make install`.
  4. Run `make lint`.
  5. Run `make test`.

## 📦 Release Workflow
- **Versioning**: Use semantic versioning (e.g., `v1.0.0`).
- **Tags**: Create git tags for stable releases.
- **Docker**: (If applicable) Use the `dev-docker` pattern for consistent staging environments.

## 📜 Quality Gates
- **Code Coverage**: Aim for >80% coverage on core ML logic and API routes.
- **Linting**: No errors or warnings allowed in CI.
