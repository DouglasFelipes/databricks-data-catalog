#!/bin/bash

echo "🚀 Starting Data Governance Portal (Local)"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Create it from template:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env with your Databricks credentials"
    exit 1
fi

# Check if frontend is built
if [ ! -d "frontend/build" ]; then
    echo "⚠️  Frontend not built. Building now..."
    cd frontend
    npm install
    npm run build
    cd ..
    echo "✅ Frontend built!"
    echo ""
fi

# Check Python dependencies
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Python dependencies not installed. Installing now..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

echo "✅ Starting server..."
echo ""
echo "📍 Application: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
