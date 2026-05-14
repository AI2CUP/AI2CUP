.PHONY: install dev-backend dev-frontend test lint format build up down

install:
	@echo "Installing dependencies..."
	cd apps/backend && ( [ -d venv ] || python3 -m venv venv ) && ./venv/bin/pip install -r requirements.txt -r requirements-dev.txt
	cd apps/frontend && npm install

dev:
	@echo "Starting both servers..."
	make dev-backend &
	make dev-frontend &


dev-backend:
	@echo "Starting backend dev server..."
	cd apps/backend && ./venv/bin/uvicorn app.main:app --reload --port 8000


dev-frontend:
	@echo "Starting frontend dev server..."
	cd apps/frontend && npm run dev

test:
	@echo "Running backend tests..."
	cd apps/backend && ./venv/bin/pytest

lint:
	@echo "Running linter..."
	cd apps/backend && ./venv/bin/ruff check .

format:
	@echo "Formatting code..."
	cd apps/backend && ./venv/bin/ruff format .

dev-docker:
	@echo "Starting both servers with docker..."
	make build &
	make up &

build:
	@echo "Building docker images..."
	cd infrastructure && docker-compose build

up:
	@echo "Starting full stack via Docker..."
	cd infrastructure && docker-compose up -d

down:
	@echo "Tearing down Docker stack..."
	cd infrastructure && docker-compose down
