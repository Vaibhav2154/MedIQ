from fastapi import APIRouter
from ..schemas.request import PolicyRequest, PolicyDecision
from ..services import evaluator

router = APIRouter(prefix="/policy", tags=["evaluation"])

@router.post("/evaluate", response_model=PolicyDecision)
async def evaluate(request: PolicyRequest):
    return evaluator.evaluate_policy(request)
