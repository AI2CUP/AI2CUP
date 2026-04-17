# AI2CUP Deployment Guide

This document covers the steps required to deploy the AI2CUP application using Docker Compose.

## Prerequisites
- Docker Engine & Docker Compose installed on the host machine.
- Git (to check out the repository).
- Target host has ports `8000` and `80` (or `3000`) available.

## Deployment Steps

1. **Clone the Source Code**
   ```bash
   git clone <repository_url>
   cd AI2CUP
   ```

2. **Configure Environment Variables**
   The backend relies on the `.env` file to function.
   ```bash
   cd apps/backend
   cp .env.example .env
   # Edit .env with your production values (e.g., set AI2CUP_DEBUG=false)
   ```

3. **Start the Infrastructure**
   We provide a Makefile for convenience. From the root directory:
   ```bash
   make up
   ```
   If you don't have `make` installed:
   ```bash
   cd infrastructure
   docker-compose up -d --build
   ```

4. **Verify Deployment**
   - Frontend is mapped to `http://localhost:3000` by default.
   - Backend API is mapped to `http://localhost:8000/api/v1/health`.
   - The Nginx reverse proxy running inside the frontend container also maps `/api` to the backend.

### Shutting Down
To gracefully stop the deployment:
```bash
make down
# or from infrastructure/ directory: docker-compose down
```

## Production Security Notes
- Re-configure `AI2CUP_CORS_ORIGINS` to accept only the production frontend domain instead of `localhost`.
- Behind a production setup, place a global reverse proxy (e.g. AWS ALB, or another Nginx layer) in front to handle HTTPS/SSL termination.
