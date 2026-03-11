.PHONY: help install build validate dev start deploy-dev deploy-prod clean

help:
	@echo "Data Governance Portal - Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install all dependencies"
	@echo "  make build        Build frontend for production"
	@echo "  make validate     Validate setup and connection"
	@echo ""
	@echo "Development:"
	@echo "  make dev          Run in development mode (hot reload)"
	@echo "  make start        Run in production mode (local)"
	@echo ""
	@echo "Deploy:"
	@echo "  make deploy-dev   Deploy to Databricks (dev)"
	@echo "  make deploy-prod  Deploy to Databricks (prod)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        Clean build artifacts"

install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "📦 Installing Node dependencies..."
	cd frontend && npm install

build:
	@echo "🔨 Building frontend..."
	cd frontend && npm run build

validate:
	@echo "🔍 Validating setup..."
	python validate.py

dev:
	@echo "🔧 Starting development mode..."
	./dev.sh

start:
	@echo "🚀 Starting production mode..."
	./start.sh

deploy-dev:
	@echo "📦 Building frontend..."
	cd frontend && npm run build && cd ..
	@echo "🔍 Validating..."
	databricks bundle validate
	@echo "🚀 Deploying to dev..."
	databricks bundle deploy -t dev

deploy-prod:
	@echo "📦 Building frontend..."
	cd frontend && npm run build && cd ..
	@echo "🔍 Validating..."
	databricks bundle validate
	@echo "🚀 Deploying to prod..."
	databricks bundle deploy -t prod

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf frontend/build
	rm -rf frontend/node_modules
	rm -rf **/__pycache__
	rm -rf *.egg-info
	@echo "✅ Clean complete"
