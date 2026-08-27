"""Fail-closed synthetic lantern-slide records for Elaren v673-v4."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

RECORD_ID = re.compile(r"^ls-syn-[0-9]{3}$")
ALLOWED_COMPONENT_STATES = {"unobserved", "represented", "quarantined", "not_applicable"}
PROHIBITED_KEYS = {
    "person_name", "owner_name", "donor_name", "curator_name", "conservator_name",
    "email", "phone", "address", "coordinate", "collection_location", "private_key",
    "credential", "secret", "real_image", "inscription_text", "measurement",
    "material_identification", "treatment_instruction", "projection_instruction",
    "copyright_decision", "privacy_decision", "legal_decision", "cultural_decision",
}


def synthetic_record(record_id: str = "ls-syn-001") -> dict[str, Any]:
    """Return a wholly synthetic record carrying explicit zero-real-world state."""
    return {
        "schema": "ghc.family.lantern-slide-record.v1",
        "record_id": record_id,
        "synthetic": True,
        "real_world_rows": 0,
        "network_calls": 0,
        "collection_status": "withheld_synthetic_placeholder",
        "location_status": "withheld_not_collected",
        "rights_status": "unknown_exact_gate",
        "component_states": {
            "carrier": "represented", "cover_glass": "represented",
            "image_layer": "unobserved", "mount_mask": "represented",
            "edge_seal": "unobserved",
        },
        "authority_claims": [],
        "outcome_claims": [],
        "boundary": (
            "Synthetic documentation only; not a real person, collection, lantern slide, "
            "glass component, image, inscription, location, observation, measurement, "
            "material identification, handling, treatment, projection, digitization, "
            "rights decision, cultural interpretation, or authority act."
        ),
    }


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).lower())
            keys |= _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            keys |= _walk_keys(child)
    return keys


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate one synthetic record without mutating it."""
    issues: list[str] = []
    if record.get("schema") != "ghc.family.lantern-slide-record.v1":
        issues.append("schema_mismatch")
    if record.get("synthetic") is not True:
        issues.append("synthetic_flag_required")
    if not isinstance(record.get("record_id"), str) or not RECORD_ID.fullmatch(record["record_id"]):
        issues.append("synthetic_record_id_required")
    if record.get("real_world_rows") != 0:
        issues.append("real_world_rows_must_be_zero")
    if record.get("network_calls") != 0:
        issues.append("network_calls_must_be_zero")
    prohibited = sorted(_walk_keys(record) & PROHIBITED_KEYS)
    if prohibited:
        issues.append("prohibited_keys:" + ",".join(prohibited))
    states = record.get("component_states")
    if not isinstance(states, dict) or not states:
        issues.append("component_states_required")
    elif any(value not in ALLOWED_COMPONENT_STATES for value in states.values()):
        issues.append("invalid_component_state")
    if record.get("authority_claims") != []:
        issues.append("authority_claims_must_be_empty")
    if record.get("outcome_claims") != []:
        issues.append("outcome_claims_must_be_empty")
    boundary = record.get("boundary")
    if not isinstance(boundary, str) or "Synthetic documentation only" not in boundary:
        issues.append("synthetic_boundary_required")
    return {"valid": not issues, "issues": issues, "issue_count": len(issues), "record_id": record.get("record_id"), "same_owner_software_evidence_only": True}


def with_component_state(record: dict[str, Any], component: str, state: str) -> dict[str, Any]:
    """Return a copied record with one bounded synthetic component-state change."""
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,48}", component):
        raise ValueError("component name is not a bounded synthetic token")
    if state not in ALLOWED_COMPONENT_STATES:
        raise ValueError("component state is outside the closed vocabulary")
    updated = deepcopy(record)
    states = updated.setdefault("component_states", {})
    if not isinstance(states, dict):
        raise TypeError("component_states must be an object")
    states[component] = state
    result = validate_record(updated)
    if not result["valid"]:
        raise ValueError("updated record is invalid: " + ",".join(result["issues"]))
    return updated
