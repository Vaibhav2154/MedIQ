from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Using pg8000 which is a pure-python driver (no libpq dependency)
# Perfect for environments where installing C binaries is difficult.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL:
    # Ensure we use pg8000 for pure-python support
    if "postgresql" in SQLALCHEMY_DATABASE_URL and "+pg8000" not in SQLALCHEMY_DATABASE_URL:
        if "://" in SQLALCHEMY_DATABASE_URL:
            scheme, rest = SQLALCHEMY_DATABASE_URL.split("://", 1)
            # Take the primary scheme (postgresql) and add +pg8000
            base_scheme = scheme.split("+")[0]
            SQLALCHEMY_DATABASE_URL = f"{base_scheme}+pg8000://{rest}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
