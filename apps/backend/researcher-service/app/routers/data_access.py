"""
Data access router for researchers to query consent-aware patient data.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.schemas.data_access import (
    DataAccessRequestCreate,
    DataAccessRequestResponse,
    ConsentAwareDataQuery
)
from app.services.data_access_service import (
    create_access_request,
    get_researcher_access_requests,
    query_consent_aware_data
)
from app.utils.dependencies import get_current_researcher
from app.models.researcher import Researcher


router = APIRouter(prefix="/data", tags=["data-access"])


@router.post("/request-access", response_model=DataAccessRequestResponse, status_code=status.HTTP_201_CREATED)
def request_data_access(
    request_data: DataAccessRequestCreate,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Request access to consent-aware patient data.
    
    Creates a data access request with the specified purpose and requested fields.
    The system will evaluate consent policies and grant access to permitted data.
    """
    access_request = create_access_request(
        db=db,
        researcher_id=current_researcher.id,
        request_data=request_data
    )
    
    return DataAccessRequestResponse.model_validate(access_request)


@router.get("/my-requests", response_model=List[DataAccessRequestResponse])
def get_my_access_requests(
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Get all data access requests for the current researcher.
    
    Returns a list of all access requests made by the authenticated researcher,
    including their status and permitted fields.
    """
    requests = get_researcher_access_requests(db, current_researcher.id)
    return [DataAccessRequestResponse.model_validate(req) for req in requests]


@router.post("/query", response_model=Dict[str, Any])
def query_data(
    query: ConsentAwareDataQuery,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Query consent-aware patient data.
    
    Retrieves patient data filtered by consent policies based on the specified
    research purpose. Only returns data where patients have consented for the
    stated purpose.
    
    Requires an active, approved data access request for the specified purpose.
    """
    result = query_consent_aware_data(
        db=db,
        researcher_id=current_researcher.id,
        query=query
    )
    
    return result
