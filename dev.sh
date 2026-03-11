#!/bin/bash

echo "🔧 Starting Development Mode..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your Databricks credentials"
    exit 1
fi

# Install Python dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Install Node dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🚀 Starting development servers..."
echo ""
echo "Backend will run on: http://localhost:8001"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
python backend/main.py &
BACKEND_PID=$!

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
