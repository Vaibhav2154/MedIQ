"""
STEP 6: Clause-Level Policy Evaluation Service

Pure functional evaluation of access decisions.
No database access, no side effects.
"""

from typing import Dict, List, Any, Set
from pydantic import BaseModel


class PolicyDecision(BaseModel):
    """
    Access decision result.
    
    decision: DENY, PARTIAL_ALLOW, or ALLOW
    permitted_fields: List of fields allowed for access
    justifications: List of reasons for decision
    """
    decision: str  # DENY, PARTIAL_ALLOW, ALLOW
    permitted_fields: List[str]
    justifications: List[str]


def evaluate_policy(
    policy: Dict[str, Any],
    requested_fields: List[str]
) -> PolicyDecision:
    """
    Evaluate consent policy against requested fields.
    
    STEP 6: Clause-Level Policy Evaluation
    
    Logic:
    1. Find intersection of requested_fields and allowed_fields
    2. Check for denied_fields conflicts
    3. Build decision with justifications
    
    Args:
        policy: Consent policy dict with allowed_fields, denied_fields
        requested_fields: List of fields being requested
    
    Returns:
        PolicyDecision: decision, permitted_fields, justifications
    """
    
    # Extract field lists from policy
    allowed_fields = set(policy.get("allowed_fields", []))
    denied_fields = set(policy.get("denied_fields", []))
    requested_set = set(requested_fields)
    
    # Step 1: Find intersection
    permitted = requested_set & allowed_fields
    rejected = requested_set - allowed_fields
    
    # Step 2: Check denied_fields conflicts
    denied_conflicts = requested_set & denied_fields
    
    justifications = []
    
    # Step 3: Build decision
    if denied_conflicts:
        justifications.append(f"Explicitly denied fields: {list(denied_conflicts)}")
        # If any requested field is denied, reject
        permitted = permitted - denied_conflicts
    
    if not permitted and requested_set:
        decision = "DENY"
        justifications.insert(0, f"No permitted fields from requested: {requested_fields}")
    elif rejected and permitted:
        decision = "PARTIAL_ALLOW"
        justifications.insert(0, f"Partial access: {len(permitted)} of {len(requested_set)} fields allowed")
    elif permitted:
        decision = "ALLOW"
        justifications.insert(0, f"Full access granted for {len(permitted)} fields")
    else:
        decision = "DENY"
        justifications.insert(0, "No fields requested or all denied")
    
    return PolicyDecision(
        decision=decision,
        permitted_fields=list(permitted),
        justifications=justifications
    )


def evaluate_conditions(
    policy: Dict[str, Any],
    request_context: Dict[str, Any]
) -> PolicyDecision:
    """
    Evaluate conditional constraints in policy.
    
    Checks:
    - anonymization_required
    - study_id_required
    - time_window
    - aggregation_level
    
    Args:
        policy: Consent policy with conditions
        request_context: Request context (study_id, user_role, etc.)
    
    Returns:
        PolicyDecision: decision based on conditions
    """
    
    conditions = policy.get("conditions", {})
    justifications = []
    
    # Check anonymization requirement
    if conditions.get("anonymization_required"):
        justifications.append("Anonymization required - PII will be masked")
    
    # Check study_id requirement
    if conditions.get("study_id_required"):
        required_id = conditions.get("study_id_required")
        provided_id = request_context.get("study_id")
        
        if provided_id != required_id:
            return PolicyDecision(
                decision="DENY",
                permitted_fields=[],
                justifications=[f"Study ID mismatch: required {required_id}, got {provided_id}"]
            )
        justifications.append(f"Study ID verified: {provided_id}")
    
    # Check time window
    if conditions.get("time_window"):
        justifications.append(f"Time window restriction: {conditions.get('time_window')}")
    
    # Check aggregation level
    if conditions.get("aggregation_level"):
        justifications.append(f"Aggregation required at level: {conditions.get('aggregation_level')}")
    
    # Check max records
    if conditions.get("max_records"):
        justifications.append(f"Limited to {conditions.get('max_records')} records")
    
    return PolicyDecision(
        decision="ALLOW",
        permitted_fields=policy.get("allowed_fields", []),
        justifications=justifications
    )


def combine_decisions(decisions: List[PolicyDecision]) -> PolicyDecision:
    """
    Combine multiple policy decisions (e.g., org-level + user-level).
    
    Takes intersection of permitted fields (most restrictive).
    
    Args:
        decisions: List of PolicyDecision objects
    
    Returns:
        PolicyDecision: Combined decision
    """
    
    if not decisions:
        return PolicyDecision(
            decision="DENY",
            permitted_fields=[],
            justifications=["No policies to evaluate"]
        )
    
    if len(decisions) == 1:
        return decisions[0]
    
    # Intersection of permitted fields (most restrictive)
    permitted_sets = [set(d.permitted_fields) for d in decisions]
    combined_permitted = permitted_sets[0]
    
    for field_set in permitted_sets[1:]:
        combined_permitted = combined_permitted & field_set
    
    # Combine justifications
    all_justifications = []
    for d in decisions:
        all_justifications.extend(d.justifications)
    
    # Determine combined decision
    if not combined_permitted:
        decision = "DENY"
    elif any(d.decision == "PARTIAL_ALLOW" for d in decisions):
        decision = "PARTIAL_ALLOW"
    else:
        decision = "ALLOW"
    
    return PolicyDecision(
        decision=decision,
        permitted_fields=list(combined_permitted),
        justifications=all_justifications
    )
