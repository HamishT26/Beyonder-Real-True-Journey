"""Synthetic flag-record contract validator; no external actions."""
from __future__ import annotations
from typing import Any

ALLOWED_PROFILES = {"identity", "edge_topology", "seam_relation", "attachment_abstention", "material_vacancy", "condition_separation", "provenance_correction", "privacy_access", "workload_handover", "flashcard_projection"}

def evaluate_contract(payload: Any, profile: str) -> dict[str, Any]:
    issues = []
    if not isinstance(payload, dict):
        return {"valid": False, "issues": ["payload_not_object"], "profile": profile}
    if profile not in ALLOWED_PROFILES:
        issues.append("unknown_profile")
    if payload.get("synthetic") is not True:
        issues.append("synthetic_true_required")
    if payload.get("real_object") is not False:
        issues.append("real_object_false_required")
    if payload.get("external_actions") != 0:
        issues.append("external_actions_zero_required")
    if not isinstance(payload.get("record_id"), str) or not payload.get("record_id"):
        issues.append("record_id_required")
    if not isinstance(payload.get("vacancies"), list) or not payload.get("vacancies"):
        issues.append("vacancies_required")
    if not isinstance(payload.get("authority_holds"), list) or not payload.get("authority_holds"):
        issues.append("authority_holds_required")
    return {"valid": not issues, "issues": issues, "profile": profile, "external_actions": 0}
