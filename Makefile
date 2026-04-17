.PHONY: install dev-backend dev-frontend test lint format build up down

install:
	@echo "Installing dependencies..."
	cd apps/backend && pip install -r requirements.txt
	cd apps/frontend && npm install

dev-backend:
	@echo "Starting backend dev server..."
	cd apps/backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	@echo "Starting frontend dev server..."
	cd apps/frontend && npm run dev

test:
	@echo "Running backend tests..."
	cd apps/backend && pytest

lint:
	@echo "Running linter..."
	cd apps/backend && ruff check .

format:
	@echo "Formatting code..."
	cd apps/backend && ruff format .

build:
	@echo "Building docker images..."
	cd infrastructure && docker-compose build

up:
	@echo "Starting full stack via Docker..."
	cd infrastructure && docker-compose up -d

down:
	@echo "Tearing down Docker stack..."
	cd infrastructure && docker-compose down
