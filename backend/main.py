import os
import sys

# Ensure parent directory is in sys.path so 'backend' package imports work from any cwd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import CORS_ORIGINS
from backend.database import engine, Base
import backend.models  # Ensure all models are registered
from backend.routes import (
    auth_router,
    projects_router,
    tasks_router,
    components_router,
    portfolio_router,
    public_router,
)

# Initialize database schema on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BuildFolio API",
    description="Track your engineering projects and turn them into a portfolio with local open-source AI",
    version="1.0.0"
)

# CORS configuration supporting credentials (cookies)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(components_router)
app.include_router(portfolio_router)
app.include_router(public_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "BuildFolio", "version": "1.0.0"}
