from fastapi import FastAPI
# Load .env from project root (two levels up from this file) if present so
# environment variables persist for local development. Uses python-dotenv when available.
try:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path)
except Exception:
    pass
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.data_access import router as data_access_router
from app.routers.router import router as consent_router  # Consent-aware data router
from app.routers.sessions import router as sessions_router  # Research sessions
from app.database import Base, engine
from app.core.config import settings

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Researcher Portal Service",
    description="Self-service portal for researchers to access consent-aware patient data for research purposes",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(data_access_router, prefix=settings.api_v1_prefix)
app.include_router(consent_router, prefix=settings.api_v1_prefix)  # Advanced consent-aware router
app.include_router(sessions_router, prefix=settings.api_v1_prefix)  # Research sessions

@app.get("/")
def root():
    """Root endpoint - service status."""
    return {
        "service": "Researcher Portal Service",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "Self-service portal for researchers to access consent-aware patient data"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
