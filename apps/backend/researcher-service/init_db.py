#!/usr/bin/env python3
"""
Initialize database tables for the researcher service.
Run this script to create all tables defined in the models.
"""
from app.database import Base, engine

def init_db():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
