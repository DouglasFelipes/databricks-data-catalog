"""
Data Governance Portal - Databricks Apps
FastAPI Backend + React Frontend
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

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

# Serve static files
if os.path.exists("frontend/build/static"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Serve frontend
@app.get("/")
async def root():
    if os.path.exists("frontend/build/index.html"):
        return FileResponse("frontend/build/index.html")
    return {
        "message": "Data Governance Portal API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "inventory": "/api/inventory",
            "lineage": "/api/lineage/{catalog}/{schema}/{table}",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
