"""
Identity Service - Main FastAPI Application

A production-grade identity service for the MedIQ healthcare platform.
Serves as the system of record for users, organizations, patients, and patient records.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import init_db
from app.routers import users, organizations, patients, patient_records


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Initialize database tables
    await init_db()
    yield
    # Shutdown: cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title="Identity Service",
    description=(
        "Identity Service for MedIQ Healthcare Platform. "
        "System of record for users, organizations, patients, and patient record references."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(organizations.router, prefix=settings.api_v1_prefix)
app.include_router(patients.router, prefix=settings.api_v1_prefix)
app.include_router(patient_records.router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and version information.
    """
    return {
        "status": "healthy",
        "service": "identity-service",
        "version": "1.0.0"
    }


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.
    
    Provides basic service information.
    """
    return {
        "service": "Identity Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
