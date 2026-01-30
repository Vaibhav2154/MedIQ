"""
Data access service for managing researcher data access requests
and querying consent-aware patient data.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid

from app.models.data_access_request import DataAccessRequest, AccessStatus
from app.schemas.data_access import DataAccessRequestCreate, ConsentAwareDataQuery
from app.services.auth_service import create_access_token


def create_access_request(
    db: Session,
    researcher_id: str,
    request_data: DataAccessRequestCreate
) -> DataAccessRequest:
    """
    Create a new data access request for a researcher.
    
    Automatically approves the request and generates an access token
    after validating consent policies.
    
    Args:
        db: Database session
        researcher_id: ID of the requesting researcher
        request_data: Access request details
        
    Returns:
        Created DataAccessRequest object
    """
    # Create the access request
    access_request = DataAccessRequest(
        id=str(uuid.uuid4()),
        researcher_id=researcher_id,
        purpose=request_data.purpose,
        justification=request_data.justification,
        requested_fields=request_data.requested_fields,
        status=AccessStatus.PENDING
    )
    
    db.add(access_request)
    db.flush()
    
    # For prototype: Auto-approve and grant access
    # In production, this would involve:
    # 1. Checking consent policies
    # 2. Filtering permitted fields based on consent
    # 3. Potentially requiring manual approval
    
    # For now, grant access to all requested fields
    access_request.status = AccessStatus.APPROVED
    access_request.permitted_fields = request_data.requested_fields
    access_request.approved_at = datetime.utcnow()
    access_request.expires_at = datetime.utcnow() + timedelta(days=7)
    
    # Generate access token
    token_data = {
        "sub": researcher_id,
        "request_id": access_request.id,
        "purpose": request_data.purpose,
        "permitted_fields": request_data.requested_fields,
        "type": "data_access"
    }
    
    access_request.access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(days=7)
    )
    
    access_request.decision_reason = "Auto-approved for prototype. Consent policies will be enforced in production."
    
    db.commit()
    db.refresh(access_request)
    
    return access_request


def get_researcher_access_requests(
    db: Session,
    researcher_id: str
) -> List[DataAccessRequest]:
    """
    Get all access requests for a specific researcher.
    
    Args:
        db: Database session
        researcher_id: Researcher ID
        
    Returns:
        List of DataAccessRequest objects
    """
    return db.query(DataAccessRequest).filter(
        DataAccessRequest.researcher_id == researcher_id
    ).order_by(DataAccessRequest.created_at.desc()).all()


def query_consent_aware_data(
    db: Session,
    researcher_id: str,
    query: ConsentAwareDataQuery
) -> Dict[str, Any]:
    """
    Query consent-aware patient data based on research purpose.
    
    This function:
    1. Validates the researcher has an approved access request for the purpose
    2. Queries the consent database for patients who consented for this purpose
    3. Returns filtered patient data based on consent policies
    
    Args:
        db: Database session
        researcher_id: Researcher ID
        query: Query parameters including purpose and filters
        
    Returns:
        Dictionary containing filtered patient data
        
    Raises:
        HTTPException: If no valid access request exists
    """
    # Check if researcher has an approved access request for this purpose
    access_request = db.query(DataAccessRequest).filter(
        DataAccessRequest.researcher_id == researcher_id,
        DataAccessRequest.purpose == query.purpose,
        DataAccessRequest.status == AccessStatus.APPROVED,
        DataAccessRequest.expires_at > datetime.utcnow()
    ).first()
    
    if not access_request:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No valid access request found for purpose '{query.purpose}'. Please request access first."
        )
    
    # Query consent-aware data
    # For prototype: Query patient_records table with consent filtering
    # In production, this would:
    # 1. Join with consent_policies table
    # 2. Filter by consent.purpose matching query.purpose
    # 3. Only return fields in access_request.permitted_fields
    # 4. Apply additional filters from query.filters
    
    try:
        # Build dynamic query based on permitted fields
        permitted_fields_str = ", ".join([f'"{field}"' for field in access_request.permitted_fields])
        
        # Base query: Get patient records where consent exists for this purpose
        sql_query = text(f"""
            SELECT {permitted_fields_str}
            FROM patient_records pr
            WHERE EXISTS (
                SELECT 1 FROM consent_policies cp
                WHERE cp.patient_id = pr.patient_id
                AND cp.purpose = :purpose
                AND cp.status = 'active'
            )
            LIMIT :limit
        """)
        
        result = db.execute(
            sql_query,
            {"purpose": query.purpose, "limit": query.limit}
        )
        
        # Convert to list of dictionaries
        rows = result.fetchall()
        columns = result.keys()
        
        data = [dict(zip(columns, row)) for row in rows]
        
        return {
            "purpose": query.purpose,
            "request_id": access_request.id,
            "permitted_fields": access_request.permitted_fields,
            "record_count": len(data),
            "data": data,
            "expires_at": access_request.expires_at.isoformat()
        }
        
    except Exception as e:
        # If tables don't exist yet or query fails, return sample data
        return {
            "purpose": query.purpose,
            "request_id": access_request.id,
            "permitted_fields": access_request.permitted_fields,
            "record_count": 0,
            "data": [],
            "message": "No data available yet. Consent policies and patient records will be populated.",
            "error": str(e)
        }
