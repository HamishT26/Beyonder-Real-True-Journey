"""Approval and authority quarantine for Caelen Morrow v673-v2."""

from __future__ import annotations

from typing import Any

SAFE_SYNTHETIC_ACTIONS = {
    "validate_schema", "simulate_transition", "render_static_report",
    "scan_privacy", "replay_manifest", "emit_synthetic_receipt",
}
PROTECTED_CLASSES = {
    "real_repair", "real_tuning", "workplace_safety", "product_safety",
    "ownership", "custody_transfer", "recording_rights", "privacy_decision",
    "accessibility_complete", "legal_interpretation", "cultural_interpretation",
    "affected_party_acceptance", "maori_wording", "maori_concepts",
    "maori_data_governance", "maori_authority", "production_identity",
    "deployment", "independent_reproduction", "stage20_transition",
}


def evaluate(action: str, approval_class: str = "safe_now") -> dict[str, Any]:
    """Permit only named synthetic software actions and quarantine everything else."""
    if action in PROTECTED_CLASSES:
        return {
            "permitted": False,
            "state": "exact_gate",
            "reason": "protected authority or evidence absent",
            "action": action,
        }
    if action not in SAFE_SYNTHETIC_ACTIONS:
        return {
            "permitted": False,
            "state": "open_gap",
            "reason": "undeclared action is not safe-now",
            "action": action,
        }
    if approval_class != "safe_now":
        return {
            "permitted": False,
            "state": "quarantined",
            "reason": "safe synthetic action lacks safe-now classification",
            "action": action,
        }
    return {
        "permitted": True,
        "state": "bounded_synthetic_only",
        "reason": "named owner-local software action",
        "action": action,
        "real_world_authority": False,
    }


def split_estimate_authorization(packet: dict[str, Any]) -> dict[str, Any]:
    """Keep a synthetic estimate representation distinct from authorization."""
    allowed = {"schema", "synthetic", "scope_tokens", "estimate_status", "authorization_status"}
    unknown = sorted(set(packet) - allowed)
    valid = (
        not unknown
        and packet.get("synthetic") is True
        and packet.get("estimate_status") == "represented_only"
        and packet.get("authorization_status") == "absent_exact_gate"
        and isinstance(packet.get("scope_tokens"), list)
    )
    return {
        "valid": valid,
        "unknown_fields": unknown,
        "estimate_is_authorization": False,
        "authorization_executed": False,
        "boundary": "No real price, customer instruction, contract, consent, repair approval, or authority act.",
    }


def gate_inventory() -> dict[str, Any]:
    return {
        "schema": "ghc.family.authority-quarantine.v1",
        "safe_synthetic_actions": sorted(SAFE_SYNTHETIC_ACTIONS),
        "protected_classes": sorted(PROTECTED_CLASSES),
        "protected_class_count": len(PROTECTED_CLASSES),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
