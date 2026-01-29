"""
API routers for Identity Service.
"""
from app.routers import users
from app.routers import organizations
from app.routers import patients
from app.routers import patient_records

__all__ = [
    "users",
    "organizations",
    "patients",
    "patient_records",
]
