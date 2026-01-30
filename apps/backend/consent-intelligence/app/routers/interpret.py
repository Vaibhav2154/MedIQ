from fastapi import APIRouter, HTTPException
from ..schemas.consent import InterpretationRequest, InterpretationResponse
from ..services import gemini, confidence, fhir

router = APIRouter(prefix="/consents", tags=["interpretation"])

@router.post("/interpret", response_model=InterpretationResponse)
async def interpret_consent(request: InterpretationRequest):
    print(f"\n{'='*60}")
    print(f"📥 INTERPRET REQUEST RECEIVED")
    print(f"{'='*60}")
    print(f"Consent ID: {request.consent_id}")
    print(f"Language: {request.language}")
    print(f"Text length: {len(request.raw_text)} chars")
    print(f"Text preview: {request.raw_text[:100]}...")
    
    # 1. LLM Extraction
    try:
        print(f"\n🤖 Calling Gemini API for interpretation...")
        interpreted = await gemini.interpret_consent_text(request.raw_text)
        print(f"✓ Gemini interpretation successful")
        print(f"  - Allowed data: {interpreted.allowed_data}")
        print(f"  - Purpose: {interpreted.purpose}")
        print(f"  - Denied data: {interpreted.denied_data}")
        print(f"  - Expiry: {interpreted.expiry}")
        print(f"  - Conditions: {interpreted.conditions}")
        print(f"  - Ambiguity flags: {interpreted.ambiguity_flags}")
    except Exception as e:
        print(f"✗ Gemini API failed!")
        print(f"  Error type: {type(e).__name__}")
        print(f"  Error message: {str(e)}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {str(e)}")
    
    # 2. Confidence Scoring
    print(f"\n📊 Calculating confidence score...")
    score = confidence.calculate_confidence(interpreted)
    needs_review = confidence.should_require_review(score)
    print(f"✓ Confidence score: {score}")
    print(f"  Needs review: {needs_review}")
    
    response = InterpretationResponse(
        consent_id=request.consent_id,
        interpreted=interpreted,
        confidence_score=score,
        needs_review=needs_review
    )
    
    print(f"\n✅ Interpretation complete")
    print(f"{'='*60}\n")
    
    return response

@router.post("/fhir")
async def get_fhir_consent(request: InterpretationResponse):
    fhir_resource = fhir.generate_fhir_consent(request.interpreted, patient_id=None)
    return {"fhir_consent": fhir_resource}
