"""
Enterprise Data Governance Portal - Databricks Apps
FastAPI Backend + React Frontend
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routes from backend
from backend.main import health_check, get_inventory, get_lineage

app = FastAPI(title="Data Governance Portal", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.get("/api/health")(health_check)
app.get("/api/inventory")(get_inventory)
app.get("/api/lineage/{catalog}/{schema}/{table}")(get_lineage)

# Check for frontend build
build_path = "frontend/build"
build_exists = os.path.exists(build_path)
logger.info(f"Current directory: {os.getcwd()}")
logger.info(f"Build path: {os.path.abspath(build_path)}")
logger.info(f"Build exists: {build_exists}")

# Serve React build or API info
@app.get("/")
async def serve_root():
    """Serve frontend if built, otherwise show API info"""
    build_path = "frontend/build/index.html"
    if os.path.exists(build_path):
        return FileResponse(build_path)
    else:
        return {
            "message": "Data Governance Portal API",
            "version": "1.0.0",
            "status": "Backend running",
            "note": "Frontend not built. Run: cd frontend && npm run build",
            "endpoints": {
                "health": "/api/health",
                "inventory": "/api/inventory",
                "lineage": "/api/lineage/{catalog}/{schema}/{table}",
                "docs": "/docs"
            }
        }

# Serve static files if build exists
if build_exists:
    try:
        app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
        logger.info("✅ Static files mounted")
    except Exception as e:
        logger.error(f"❌ Error mounting static files: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
