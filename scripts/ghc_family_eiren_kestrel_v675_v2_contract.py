from __future__ import annotations

from typing import Any

OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = {
    "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
    "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
    "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "external_actions",
}


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons = [f"missing_{field}" for field in sorted(REQUIRED - payload.keys())]
    if payload.get("expected_disposition") not in OUTCOMES:
        reasons.append("invalid_outcome_label")
    if payload.get("external_actions") != 0:
        reasons.append("external_action_nonzero")
    if not payload.get("protected_gates"):
        reasons.append("protected_gates_missing")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
