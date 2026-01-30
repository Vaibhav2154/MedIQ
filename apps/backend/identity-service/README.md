# Identity Service

A production-grade Identity Service for the MedIQ healthcare platform, built with FastAPI, PostgreSQL, and async SQLAlchemy.

## Overview

The Identity Service is the **system of record** for:

- **Users** (patients, doctors, hospital admins, researchers, regulators)
- **Organizations** (hospitals, research organizations, government entities)
- **Patients** and their ABHA IDs
- **Patient Record References** (pointers to external EHR/FHIR systems)

### What This Service Does

✅ Manages identity and metadata  
✅ Provides consent-ready data structures  
✅ Logs all create operations for audit trails  
✅ Exposes clean REST APIs for downstream services  

### What This Service Does NOT Do

❌ Interpret or enforce consent policies  
❌ Filter data based on permissions  
✅ Store medical records (encounters, observations, diagnoses, medications)  
❌ Handle authentication (trusts API Gateway)  

## Architecture

```
┌─────────────────┐
│  API Gateway    │ ← Handles JWT authentication
│  (Upstream)     │   Sets X-User-Id, X-User-Role headers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Identity Service│
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   (AsyncPG)     │
└─────────────────┘
```

### Technology Stack

- **Framework**: FastAPI 0.128+
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic 2.0
- **Password Hashing**: bcrypt via passlib
- **Python**: 3.11+

## Database Schema

### Tables

#### `users`
- `id` (UUID, PK)
- `email` (String, unique, indexed)
- `role` (Enum: patient, doctor, hospital_admin, researcher, regulator)
- `password_hash` (String)
- `created_at`, `updated_at` (Timestamps)

#### `organizations`
- `id` (UUID, PK)
- `name` (String)
- `org_type` (Enum: hospital, research_org, government)
- `created_at`, `updated_at` (Timestamps)

#### `patients`
- `id` (UUID, PK)
- `abha_id` (String, unique, nullable, indexed)
- `created_at`, `updated_at` (Timestamps)

#### `patient_records`
- `id` (UUID, PK)
- `patient_id` (UUID, FK → patients)
- `record_type` (String: lab, imaging, prescription, etc.)
- `record_ref` (String: external EHR/FHIR reference)
- `created_at`, `updated_at` (Timestamps)

#### `encounters`
- `id` (UUID, PK)
- `patient_id` (UUID, FK → patients)
- `organization_id` (UUID, FK → organizations, nullable)
- `encounter_type` (String)
- `reason` (String, nullable)
- `start_at`, `end_at` (Timestamps)
- `created_at`, `updated_at` (Timestamps)

#### `observations`
- `id` (UUID, PK)
- `patient_id` (UUID, FK → patients)
- `encounter_id` (UUID, FK → encounters, nullable)
- `category` (String)
- `code` (String)
- `value` (String)
- `unit` (String, nullable)
- `effective_at` (Timestamp)
- `created_at`, `updated_at` (Timestamps)

#### `diagnoses`
- `id` (UUID, PK)
- `patient_id` (UUID, FK → patients)
- `encounter_id` (UUID, FK → encounters, nullable)
- `code` (String)
- `description` (String, nullable)
- `clinical_status` (String)
- `recorded_at` (Timestamp)
- `created_at`, `updated_at` (Timestamps)

#### `medications`
- `id` (UUID, PK)
- `patient_id` (UUID, FK → patients)
- `encounter_id` (UUID, FK → encounters, nullable)
- `name` (String)
- `dose`, `unit`, `frequency`, `route` (Strings, nullable)
- `start_at`, `end_at` (Timestamps, nullable)
- `created_at`, `updated_at` (Timestamps)

#### `audit_logs`
- `id` (UUID, PK)
- `actor_id` (UUID, nullable)
- `action` (String)
- `resource_type` (String)
- `resource_id` (UUID, nullable)
- `timestamp` (DateTime)
- `metadata` (JSON, nullable)

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- uv (Python package manager)

### Installation

1. **Clone the repository** (if not already done)

2. **Navigate to the service directory**
   ```bash
   cd apps/backend/identity-service
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Generate with `openssl rand -hex 32`
   - Other settings as needed

5. **Create the database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE mediq_identity;
   ```

6. **Run the service**
   ```bash
   uv run uvicorn main:app --reload
   ```

The service will be available at `http://localhost:8000`

## API Documentation

Once running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Endpoints

#### Users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{id}` - Get user by ID

#### Organizations
- `POST /api/v1/organizations` - Create a new organization
- `GET /api/v1/organizations/{id}` - Get organization by ID

#### Patients
- `POST /api/v1/patients` - Register a new patient
- `GET /api/v1/patients/{id}` - Get patient by ID

#### Patient Records
- `POST /api/v1/patients/{id}/records` - Create a record reference
- `GET /api/v1/patients/{id}/records` - List patient records

#### Encounters
- `POST /api/v1/patients/{id}/encounters` - Create an encounter
- `GET /api/v1/patients/{id}/encounters` - List encounters

#### Observations
- `POST /api/v1/patients/{id}/observations` - Create an observation
- `GET /api/v1/patients/{id}/observations` - List observations

#### Diagnoses
- `POST /api/v1/patients/{id}/diagnoses` - Create a diagnosis
- `GET /api/v1/patients/{id}/diagnoses` - List diagnoses

#### Medications
- `POST /api/v1/patients/{id}/medications` - Create a medication
- `GET /api/v1/patients/{id}/medications` - List medications

#### Health
- `GET /health` - Health check endpoint

## Usage Examples

### Create a User

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "email": "doctor@example.com",
    "role": "doctor",
    "password": "securepassword123"
  }'
```

### Create a Patient

```bash
curl -X POST http://localhost:8000/api/v1/patients \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "abha_id": "12-3456-7890-1234"
  }'
```

### Create a Patient Record Reference

```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_id}/records \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "record_type": "lab",
    "record_ref": "fhir://server.example.com/Observation/12345"
  }'
```

## Development

### Project Structure

```
apps/backend/identity-service/
├── app/
│   ├── core/           # Configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── routers/        # API endpoints
│   └── database.py     # Database setup
├── main.py             # FastAPI application
├── pyproject.toml      # Dependencies
└── .env.example        # Environment template
```

### Code Quality

- **Type Hints**: All functions have type annotations
- **Docstrings**: Comprehensive documentation
- **Async/Await**: Full async support for I/O operations
- **Error Handling**: Explicit HTTP exceptions
- **Validation**: Pydantic schemas for all inputs/outputs

### Database Migrations

Currently, tables are created automatically on startup. For production:

1. **Install Alembic**
   ```bash
   uv add alembic
   ```

2. **Initialize Alembic**
   ```bash
   alembic init alembic
   ```

3. **Configure and create migrations**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## Authentication

This service **does not** handle authentication. It trusts the following headers from the upstream API Gateway:

- `X-User-Id`: UUID of the authenticated user
- `X-User-Role`: Role of the authenticated user

The API Gateway must validate JWTs and set these headers before forwarding requests.

## Audit Logging

All create operations are automatically logged to the `audit_logs` table with:

- Actor ID (from `X-User-Id` header)
- Action name
- Resource type and ID
- Timestamp
- Additional metadata

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | ✅ |
| `SECRET_KEY` | Secret key for JWT (future use) | - | ✅ |
| `APP_NAME` | Application name | Identity Service | ❌ |
| `DEBUG` | Enable debug mode | false | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins | localhost:3000,localhost:5173 | ❌ |
| `API_V1_PREFIX` | API version prefix | /api/v1 | ❌ |

## Testing

### Manual Testing

1. Start the service
2. Access Swagger UI at http://localhost:8000/docs
3. Test each endpoint with sample data

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "identity-service",
  "version": "1.0.0"
}
```

## Production Considerations

- [ ] Implement Alembic for database migrations
- [ ] Add rate limiting middleware
- [ ] Configure connection pooling for production load
- [ ] Set up monitoring and logging (e.g., Sentry, DataDog)
- [ ] Use environment-specific configuration
- [ ] Implement backup and disaster recovery
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline

## License

[Your License Here]

## Contact

[Your Contact Information]
