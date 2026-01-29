from ..schemas.consent import InterpretedConsent

def calculate_confidence(interpreted: InterpretedConsent) -> float:
    score = 1.0
    
    # Penalty for missing expiry (important for research)
    if not interpreted.expiry:
        score -= 0.3
        
    # Penalty for vague language detected by LLM
    if "vague_language" in interpreted.ambiguity_flags:
        score -= 0.2
        
    # Penalty for missing purposes
    if not interpreted.purpose:
        score -= 0.3
        
    # Penalty for conflicting statements
    if "conflicting_statements" in interpreted.ambiguity_flags:
        score -= 0.3
        
    return max(0.0, min(1.0, score))

def should_require_review(score: float, threshold: float = 0.75) -> bool:
    return score < threshold
