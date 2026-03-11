#!/bin/bash

echo "🚀 Starting Data Governance Portal..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your Databricks credentials"
    exit 1
fi

# Check if frontend/build exists
if [ ! -d "frontend/build" ]; then
    echo "📦 Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start application
echo "✅ Starting application on http://localhost:8000"
python app.py
