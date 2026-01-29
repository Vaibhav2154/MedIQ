from fastapi import APIRouter, HTTPException
from ..schemas.consent import InterpretationRequest, InterpretationResponse
from ..services import gemini, confidence, fhir

router = APIRouter(prefix="/consents", tags=["interpretation"])

@router.post("/interpret", response_model=InterpretationResponse)
async def interpret_consent(request: InterpretationRequest):
    # 1. LLM Extraction
    try:
        interpreted = await gemini.interpret_consent_text(request.raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {str(e)}")
    
    # 2. Confidence Scoring
    score = confidence.calculate_confidence(interpreted)
    needs_review = confidence.should_require_review(score)
    
    return InterpretationResponse(
        consent_id=request.consent_id,
        interpreted=interpreted,
        confidence_score=score,
        needs_review=needs_review
    )

@router.post("/fhir")
async def get_fhir_consent(request: InterpretationResponse):
    fhir_resource = fhir.generate_fhir_consent(request.interpreted, patient_id=None)
    return {"fhir_consent": fhir_resource}
