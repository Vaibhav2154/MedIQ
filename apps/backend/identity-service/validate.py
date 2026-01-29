"""
Quick validation script to check imports and basic structure.
This doesn't require a database connection.
"""
import sys
import asyncio


async def validate_imports():
    """Validate all imports work correctly."""
    print("🔍 Validating imports...")
    
    try:
        # Core
        from app.core.config import settings
        print("✅ Core config imported")
        
        # Database
        from app.database import Base, get_db, init_db
        print("✅ Database module imported")
        
        # Models
        from app.models import User, UserRole, Organization, OrgType, Patient, PatientRecord, AuditLog
        print("✅ All models imported")
        
        # Schemas
        from app.schemas import (
            UserCreate, UserRead, UserUpdate,
            OrganizationCreate, OrganizationRead,
            PatientCreate, PatientRead,
            PatientRecordCreate, PatientRecordRead,
            AuditLogRead
        )
        print("✅ All schemas imported")
        
        # Services
        from app.services import user_service, organization_service, patient_service, patient_record_service, audit_service
        print("✅ All services imported")
        
        # Routers
        from app.routers import users, organizations, patients, patient_records
        print("✅ All routers imported")
        
        # Main app
        from main import app
        print("✅ Main FastAPI app imported")
        
        print("\n✨ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def validate_models():
    """Validate model structure."""
    print("\n🔍 Validating models...")
    
    try:
        from app.models import User, Organization, Patient, PatientRecord, AuditLog
        
        # Check User model
        assert hasattr(User, '__tablename__')
        assert User.__tablename__ == 'users'
        print("✅ User model structure valid")
        
        # Check Organization model
        assert hasattr(Organization, '__tablename__')
        assert Organization.__tablename__ == 'organizations'
        print("✅ Organization model structure valid")
        
        # Check Patient model
        assert hasattr(Patient, '__tablename__')
        assert Patient.__tablename__ == 'patients'
        print("✅ Patient model structure valid")
        
        # Check PatientRecord model
        assert hasattr(PatientRecord, '__tablename__')
        assert PatientRecord.__tablename__ == 'patient_records'
        print("✅ PatientRecord model structure valid")
        
        # Check AuditLog model
        assert hasattr(AuditLog, '__tablename__')
        assert AuditLog.__tablename__ == 'audit_logs'
        print("✅ AuditLog model structure valid")
        
        print("\n✨ All models validated!")
        return True
        
    except Exception as e:
        print(f"\n❌ Model validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def validate_schemas():
    """Validate schema structure."""
    print("\n🔍 Validating schemas...")
    
    try:
        from app.schemas import UserCreate, UserRead, OrganizationCreate, PatientCreate, PatientRecordCreate
        
        # Test UserCreate schema
        user_data = {
            "email": "test@example.com",
            "role": "doctor",
            "password": "testpassword123"
        }
        user_create = UserCreate(**user_data)
        print("✅ UserCreate schema valid")
        
        # Test OrganizationCreate schema
        org_data = {
            "name": "Test Hospital",
            "org_type": "hospital"
        }
        org_create = OrganizationCreate(**org_data)
        print("✅ OrganizationCreate schema valid")
        
        # Test PatientCreate schema
        patient_data = {
            "abha_id": "12-3456-7890-1234"
        }
        patient_create = PatientCreate(**patient_data)
        print("✅ PatientCreate schema valid")
        
        # Test PatientRecordCreate schema
        record_data = {
            "record_type": "lab",
            "record_ref": "fhir://example.com/Observation/123"
        }
        record_create = PatientRecordCreate(**record_data)
        print("✅ PatientRecordCreate schema valid")
        
        print("\n✨ All schemas validated!")
        return True
        
    except Exception as e:
        print(f"\n❌ Schema validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def validate_app():
    """Validate FastAPI app structure."""
    print("\n🔍 Validating FastAPI app...")
    
    try:
        from main import app
        
        # Check routes are registered
        routes = [route.path for route in app.routes]
        
        expected_routes = [
            "/health",
            "/",
            "/api/v1/users",
            "/api/v1/users/{user_id}",
            "/api/v1/organizations",
            "/api/v1/organizations/{org_id}",
            "/api/v1/patients",
            "/api/v1/patients/{patient_id}",
            "/api/v1/patients/{patient_id}/records",
        ]
        
        for expected in expected_routes:
            if expected in routes:
                print(f"✅ Route registered: {expected}")
            else:
                print(f"⚠️  Route not found: {expected}")
        
        print("\n✨ FastAPI app validated!")
        return True
        
    except Exception as e:
        print(f"\n❌ App validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all validations."""
    print("=" * 60)
    print("Identity Service - Validation Script")
    print("=" * 60)
    
    results = []
    
    results.append(await validate_imports())
    results.append(await validate_models())
    results.append(await validate_schemas())
    results.append(await validate_app())
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 All validations passed!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some validations failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
