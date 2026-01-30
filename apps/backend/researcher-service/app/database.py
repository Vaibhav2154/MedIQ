from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.zmdkpplpycidyponszkh:Vaibhav2154@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
)

# Normalize URL for synchronous SQLAlchemy engine when an async driver is present
# If the env var contains '+asyncpg' (e.g. 'postgresql+asyncpg://...'), strip
# the async driver for use with the synchronous `create_engine` below.
sync_database_url = DATABASE_URL
if DATABASE_URL and "+asyncpg" in DATABASE_URL:
    sync_database_url = DATABASE_URL.replace("+asyncpg", "")

# Create SQLAlchemy engine (synchronous, no async)
engine = create_engine(
    sync_database_url,
    echo=False,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Declarative base for ORM models
Base = declarative_base()

def get_db():
    """
    Dependency injection for database session.
    
    Usage in FastAPI endpoints:
        @router.get("/")
        def endpoint(db: Session = Depends(get_db)):
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import all models here so they are registered with Base.metadata
from app.models.researcher import Researcher  # noqa: F401
from app.models.data_access_request import DataAccessRequest  # noqa: F401
from app.models.research_session import ResearchSession  # noqa: F401
from app.models.session_audit_log import SessionAuditLog  # noqa: F401
from app.models.eda_models import Dataset, DatasetColumn  # noqa: F401


# Import models to ensure they're registered with Base
# This must be after Base is defined
from app.models import researcher, data_access_request  # noqa: E402, F401
