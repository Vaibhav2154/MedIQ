# Researcher Portal Service - API Integration Guide

## Overview

The Researcher Portal Service now provides **three complementary ways** to access consent-aware patient data:

1. **Simple Data Access** (`/api/v1/data/*`) - Basic purpose-driven access
2. **Advanced Consent Router** (`/api/v1/router/*`) - SQL query rewriting with consent policies
3. **Authentication** (`/api/v1/auth/*`) - Researcher signup and login

---

## Authentication Endpoints

### POST /api/v1/auth/signup
Register a new researcher account.

**Request:**
```json
{
  "email": "researcher@university.edu",
  "password": "SecurePass123",
  "full_name": "Dr. Jane Smith",
  "institution": "MIT",
  "research_interests": "Diabetes research",
  "credentials": "PhD"
}
```

**Response:** `201 Created`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "researcher": { ... }
}
```

### POST /api/v1/auth/login
Authenticate and get access token.

**Request:**
```json
{
  "email": "researcher@university.edu",
  "password": "SecurePass123"
}
```

---

## Simple Data Access (Recommended for Most Use Cases)

### POST /api/v1/data/request-access
Request access to specific data fields for a research purpose.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "purpose": "diabetes_research",
  "justification": "Studying diabetes patterns in urban populations",
  "requested_fields": ["patient_id", "age", "diagnosis", "glucose_level"]
}
```

**Response:** `201 Created`
```json
{
  "id": "request-uuid",
  "researcher_id": "researcher-uuid",
  "purpose": "diabetes_research",
  "status": "approved",
  "access_token": "data-access-token...",
  "permitted_fields": ["patient_id", "age", "diagnosis", "glucose_level"],
  "expires_at": "2026-02-06T12:00:00Z"
}
```

### POST /api/v1/data/query
Query consent-aware data using your approved access request.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "purpose": "diabetes_research",
  "filters": {"age_min": 18, "age_max": 65},
  "limit": 100
}
```

---

## Advanced Consent-Aware Router (For SQL Queries)

### POST /api/v1/router/access-request
Submit a SQL query that will be automatically rewritten to enforce consent policies.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "subject_id": "patient-123",
  "purpose": "RESEARCH",
  "requested_fields": ["name", "age", "diagnosis", "aadhaar"],
  "query": "SELECT name, age, diagnosis, aadhaar FROM patients WHERE patient_id = 'patient-123'"
}
```

**Response:** `200 OK`
```json
{
  "request_id": "req-uuid",
  "status": "ALLOW",
  "access_token": "scoped-token...",
  "permitted_fields": ["age", "diagnosis"],
  "rewritten_query": "SELECT age, diagnosis FROM patients WHERE patient_id = 'patient-123'",
  "justifications": [
    "Field 'aadhaar' denied: PII not permitted for RESEARCH",
    "Field 'name' denied: Direct identifier not permitted"
  ]
}
```

**Key Features:**
- **Automatic SQL Rewriting**: Removes denied fields from SELECT queries
- **Policy Evaluation**: Checks consent policies in real-time
- **Field-Level Filtering**: Only returns permitted fields
- **Audit Logging**: All access attempts are logged
- **Token Scoping**: Access tokens are scoped to specific fields and purposes

---

## Comparison: Simple vs Advanced

| Feature | Simple Data Access | Advanced Consent Router |
|---------|-------------------|------------------------|
| **Use Case** | General research queries | Custom SQL queries |
| **Query Format** | JSON filters | Raw SQL |
| **SQL Rewriting** | ❌ Not needed | ✅ Automatic |
| **Consent Checking** | ✅ Purpose-based | ✅ Field-level |
| **Complexity** | Low | Medium |
| **Best For** | Most researchers | Advanced users with SQL needs |

---

## Example Workflow

### 1. Register and Login
```bash
# Signup
curl -X POST http://localhost:8005/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "researcher@mit.edu",
    "password": "SecurePass123",
    "full_name": "Dr. Jane Smith",
    "institution": "MIT"
  }'

# Login (if already registered)
curl -X POST http://localhost:8005/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "researcher@mit.edu",
    "password": "SecurePass123"
  }'
```

### 2. Request Data Access (Simple Method)
```bash
curl -X POST http://localhost:8005/api/v1/data/request-access \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "diabetes_research",
    "requested_fields": ["patient_id", "age", "diagnosis"]
  }'
```

### 3. Query Data
```bash
curl -X POST http://localhost:8005/api/v1/data/query \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "diabetes_research",
    "limit": 50
  }'
```

### 4. Advanced SQL Query (Advanced Method)
```bash
curl -X POST http://localhost:8005/api/v1/router/access-request \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": "patient-123",
    "purpose": "RESEARCH",
    "requested_fields": ["age", "diagnosis", "glucose_level"],
    "query": "SELECT * FROM patient_records WHERE patient_id = '\''patient-123'\''"
  }'
```

---

## Security Features

✅ **JWT Authentication**: All endpoints require valid researcher tokens  
✅ **Consent Enforcement**: Real-time consent policy checking  
✅ **Query Rewriting**: Automatic removal of denied fields  
✅ **Audit Logging**: Complete access trail  
✅ **Token Expiration**: Time-limited access tokens  
✅ **Field-Level Control**: Granular permission management  

---

## Error Handling

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied: Patient has not consented for RESEARCH purpose"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid query: Query must be a SELECT statement"
}
```

---

## Next Steps

1. **Test the APIs** using Swagger UI at `http://localhost:8005/docs`
2. **Integrate with Frontend** using the provided endpoints
3. **Set up Consent Policies** in the database
4. **Configure Policy Engine** for production use
5. **Enable Email Verification** for researcher accounts
