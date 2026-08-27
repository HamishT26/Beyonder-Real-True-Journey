"""Fail-closed synthetic dry-stone wall records for Eiren v673-v3."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

RECORD_ID = re.compile(r"^dsw-syn-[0-9]{3}$")
ALLOWED_COMPONENT_STATES = {"unobserved", "represented", "quarantined", "not_applicable"}
PROHIBITED_KEYS = {
    "person_name", "owner_name", "practitioner_name", "email", "phone", "address",
    "parcel", "coordinate", "site_location", "credential", "private_key", "secret",
    "measurement", "stability_assessment", "repair_instruction", "work_instruction",
    "legal_decision", "heritage_decision", "cultural_decision",
}


def synthetic_record(record_id: str = "dsw-syn-001") -> dict[str, Any]:
    """Return a wholly synthetic record that carries explicit zero-real-world state."""
    return {
        "schema": "ghc.family.dry-stone-wall-record.v1",
        "record_id": record_id,
        "synthetic": True,
        "real_world_rows": 0,
        "network_calls": 0,
        "site_status": "withheld_synthetic_placeholder",
        "location_status": "withheld_not_collected",
        "land_status": "synthetic_role_placeholder_only",
        "component_states": {
            "wall_face": "represented",
            "hearting": "represented",
            "coping": "unobserved",
            "foundation_contact": "unobserved",
        },
        "authority_claims": [],
        "outcome_claims": [],
        "boundary": (
            "Synthetic documentation only; not a real person, site, wall, stone, land record, "
            "observation, measurement, structural assessment, intervention, ownership, custody, "
            "heritage, archaeology, safety, cultural interpretation, or authority act."
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
    """Validate a record and return stable issues without mutating the input."""
    issues: list[str] = []
    if record.get("schema") != "ghc.family.dry-stone-wall-record.v1":
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
    return {
        "valid": not issues,
        "issues": issues,
        "issue_count": len(issues),
        "record_id": record.get("record_id"),
        "same_owner_software_evidence_only": True,
    }


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
