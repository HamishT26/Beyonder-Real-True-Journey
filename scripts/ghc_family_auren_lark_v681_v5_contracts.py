from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from typing import Any

LIFECYCLE = "x2_evidence"
SCOPE = "synthetic_zero_row"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
MUTATION_TYPES = {
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "evidence_status_promotion",
    "authority_promotion",
}


def provenance_digest(proposal_id: str, expected_disposition: str) -> str:
    material = f"{proposal_id}|{LIFECYCLE}|{SCOPE}|{expected_disposition}".encode()
    return hashlib.sha256(material).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    proposal_id = proposal["proposal_id"]
    expected = proposal["expected_disposition"]
    return {
        "authority_conferred": False,
        "evidence_status": expected,
        "lifecycle": LIFECYCLE,
        "proposal_id": proposal_id,
        "provenance_digest": provenance_digest(proposal_id, expected),
        "real_rows": 0,
        "required_field": "present",
        "scope": SCOPE,
        "synthetic": True,
    }


def evaluate(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    proposal_id = proposal["proposal_id"]
    expected = proposal["expected_disposition"]
    reasons: list[str] = []
    if fixture.get("required_field") != "present":
        reasons.append("missing_required_field")
    if fixture.get("proposal_id") != proposal_id:
        reasons.append("proposal_mismatch")
    if fixture.get("lifecycle") != LIFECYCLE:
        reasons.append("lifecycle_inversion")
    if fixture.get("scope") != SCOPE or fixture.get("synthetic") is not True:
        reasons.append("scope_promotion")
    if fixture.get("real_rows") != 0:
        reasons.append("real_row_promotion")
    if fixture.get("evidence_status") != expected or expected not in ALLOWED_OUTCOMES:
        reasons.append("evidence_status_promotion")
    if fixture.get("provenance_digest") != provenance_digest(proposal_id, expected):
        reasons.append("stale_provenance_digest")
    if fixture.get("authority_conferred") is not False:
        reasons.append("authority_promotion")
    return {
        "accepted": not reasons,
        "credit": "bounded_positive_structure" if not reasons else "rejected_zero_credit",
        "proposal_id": proposal_id,
        "reasons": sorted(set(reasons)),
    }


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    if mutation_type not in MUTATION_TYPES:
        raise ValueError(f"unknown mutation: {mutation_type}")
    changed = deepcopy(fixture)
    if mutation_type == "missing_required_field":
        changed.pop("required_field", None)
    elif mutation_type == "lifecycle_inversion":
        changed["lifecycle"] = "x1_planning_only"
    elif mutation_type == "stale_provenance_digest":
        changed["provenance_digest"] = "0" * 64
    elif mutation_type == "evidence_status_promotion":
        changed["evidence_status"] = (
            "completed" if fixture["evidence_status"] != "completed" else "production_confirmed"
        )
    elif mutation_type == "authority_promotion":
        changed["authority_conferred"] = True
    return changed


def civic_tree_record_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": {
            "authority_state": {"const": "exact_gate"},
            "correction_history": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "correction_id": {
                            "pattern": "^synthetic:correction:[0-9]{3}$",
                            "type": "string",
                        },
                        "field_pointer": {"pattern": "^/[a-z_]+$", "type": "string"},
                        "state": {
                            "enum": ["requested", "statement_attached", "superseded"]
                        },
                    },
                    "required": ["correction_id", "field_pointer", "state"],
                    "type": "object",
                },
                "minItems": 1,
                "type": "array",
            },
            "location_cell": {"pattern": "^synthetic:grid:[A-Z]{2}[0-9]{2}$", "type": "string"},
            "real_rows": {"const": 0},
            "record_id": {
                "pattern": "^synthetic:civic-tree-record:[0-9]{3}$",
                "type": "string",
            },
            "risk_assessment": {"const": "not_performed"},
            "synthetic": {"const": True},
            "tree_key": {"pattern": "^synthetic:civic-tree:[0-9]{3}$", "type": "string"},
        },
        "required": [
            "authority_state",
            "correction_history",
            "location_cell",
            "real_rows",
            "record_id",
            "risk_assessment",
            "synthetic",
            "tree_key",
        ],
        "title": "Wholly synthetic civic-tree correction record",
        "type": "object",
    }


def synthetic_civic_tree_record() -> dict[str, Any]:
    return {
        "authority_state": "exact_gate",
        "correction_history": [
            {
                "correction_id": "synthetic:correction:001",
                "field_pointer": "/condition_code",
                "state": "requested",
            },
            {
                "correction_id": "synthetic:correction:002",
                "field_pointer": "/condition_code",
                "state": "statement_attached",
            },
        ],
        "location_cell": "synthetic:grid:AL15",
        "real_rows": 0,
        "record_id": "synthetic:civic-tree-record:001",
        "risk_assessment": "not_performed",
        "synthetic": True,
        "tree_key": "synthetic:civic-tree:001",
    }


def validate_civic_tree_record(record: dict[str, Any]) -> list[str]:
    required = {
        "authority_state",
        "correction_history",
        "location_cell",
        "real_rows",
        "record_id",
        "risk_assessment",
        "synthetic",
        "tree_key",
    }
    reasons: list[str] = []
    if set(record) != required:
        reasons.append("closed_field_set")
    if record.get("synthetic") is not True or record.get("real_rows") != 0:
        reasons.append("synthetic_zero_row_boundary")
    if record.get("authority_state") != "exact_gate":
        reasons.append("authority_state")
    if record.get("risk_assessment") != "not_performed":
        reasons.append("risk_assessment_promotion")
    patterns = {
        "record_id": r"^synthetic:civic-tree-record:[0-9]{3}$",
        "tree_key": r"^synthetic:civic-tree:[0-9]{3}$",
        "location_cell": r"^synthetic:grid:[A-Z]{2}[0-9]{2}$",
    }
    for field, pattern in patterns.items():
        value = record.get(field)
        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            reasons.append(f"{field}_format")
    history = record.get("correction_history")
    if not isinstance(history, list) or not history:
        reasons.append("correction_history")
    else:
        allowed_states = {"requested", "statement_attached", "superseded"}
        for row in history:
            if not isinstance(row, dict) or set(row) != {"correction_id", "field_pointer", "state"}:
                reasons.append("correction_row_fields")
                continue
            if re.fullmatch(r"synthetic:correction:[0-9]{3}", str(row["correction_id"])) is None:
                reasons.append("correction_id_format")
            if re.fullmatch(r"/[a-z_]+", str(row["field_pointer"])) is None:
                reasons.append("field_pointer_format")
            if row["state"] not in allowed_states:
                reasons.append("correction_state")
    return sorted(set(reasons))
