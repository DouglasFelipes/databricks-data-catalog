"""
Enterprise Data Governance Portal - Databricks Apps
FastAPI Backend + React Frontend
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Data Governance Portal")

# Serve React build
if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("frontend/build/index.html")

# Mount API routes
from backend.main import app as api_app
app.mount("/api", api_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
