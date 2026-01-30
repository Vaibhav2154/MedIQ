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
from app.routers.router import router
from app.database import Base, engine

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Consent-Aware Data Router",
    description="Runtime gatekeeper for healthcare data access with consent validation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

@app.get("/")
def root():
    """Root endpoint - service status."""
    return {
        "service": "Consent-Aware Data Router",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    