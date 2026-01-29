"""
Enum definitions for schemas.
"""
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    PATIENT = "patient"
    DOCTOR = "doctor"
    HOSPITAL_ADMIN = "hospital_admin"
    RESEARCHER = "researcher"
    REGULATOR = "regulator"


class OrgType(str, Enum):
    """Organization type enumeration."""
    HOSPITAL = "hospital"
    RESEARCH_ORG = "research_org"
    GOVERNMENT = "government"


class RecordType(str, Enum):
    """Patient record type enumeration."""
    LAB = "lab"
    IMAGING = "imaging"
    PRESCRIPTION = "prescription"
    NOTE = "note"
    VITALS = "vitals"
    DISCHARGE_SUMMARY = "discharge_summary"
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
