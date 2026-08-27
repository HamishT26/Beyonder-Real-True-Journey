"""Approval and authority quarantine for Neris Solane v673-v5."""

from __future__ import annotations

from typing import Any

SAFE_SYNTHETIC_ACTIONS = {"validate_schema", "simulate_transition", "render_static_report", "scan_privacy", "replay_manifest", "emit_synthetic_receipt"}
PROTECTED_CLASSES = {
    "real_station_access", "real_observation", "real_measurement", "datum_determination",
    "benchmark_transfer", "gauge_calibration", "gauge_maintenance", "real_chart_handling",
    "real_conservation_treatment", "real_digitization", "tide_prediction", "navigation_advice",
    "field_safety", "electrical_safety", "infrastructure_disclosure", "condition_assessment", "custody_transfer", "ownership", "authorship_decision",
    "copyright_decision", "publication_decision", "image_rights", "privacy_decision",
    "accessibility_complete", "legal_interpretation", "cultural_interpretation",
    "traditional_knowledge", "affected_party_acceptance", "maori_wording",
    "maori_concepts", "maori_data_governance", "maori_authority", "production_identity",
    "deployment", "independent_reproduction", "stage20_transition",
}


def evaluate(action: str, approval_class: str = "safe_now") -> dict[str, Any]:
    if action in PROTECTED_CLASSES:
        return {"permitted": False, "state": "exact_gate", "reason": "protected authority or evidence absent", "action": action}
    if action not in SAFE_SYNTHETIC_ACTIONS:
        return {"permitted": False, "state": "open_gap", "reason": "undeclared action is not safe-now", "action": action}
    if approval_class != "safe_now":
        return {"permitted": False, "state": "quarantined", "reason": "safe synthetic action lacks safe-now classification", "action": action}
    return {"permitted": True, "state": "bounded_synthetic_only", "reason": "named owner-local software action", "action": action, "real_world_authority": False}


def split_record_authorization(packet: dict[str, Any]) -> dict[str, Any]:
    allowed = {"schema", "synthetic", "scope_tokens", "record_status", "authorization_status"}
    unknown = sorted(set(packet) - allowed)
    valid = not unknown and packet.get("synthetic") is True and packet.get("record_status") == "represented_only" and packet.get("authorization_status") == "absent_exact_gate" and isinstance(packet.get("scope_tokens"), list)
    return {"valid": valid, "unknown_fields": unknown, "record_is_authorization": False, "authorization_executed": False, "boundary": "No real station or chart decision, observation, datum determination, calibration, maintenance, handling, conservation, digitization, prediction, navigation use, reproduction, publication, consent, rights clearance, or authority act."}


def gate_inventory() -> dict[str, Any]:
    return {"schema": "ghc.family.authority-quarantine.v1", "safe_synthetic_actions": sorted(SAFE_SYNTHETIC_ACTIONS), "protected_classes": sorted(PROTECTED_CLASSES), "protected_class_count": len(PROTECTED_CLASSES), "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
