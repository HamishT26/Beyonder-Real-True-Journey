from __future__ import annotations

import hashlib
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
    expected_digest = provenance_digest(proposal_id, expected)
    if fixture.get("provenance_digest") != expected_digest:
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
        changed["evidence_status"] = "completed" if fixture["evidence_status"] != "completed" else "production_confirmed"
    elif mutation_type == "authority_promotion":
        changed["authority_conferred"] = True
    return changed


def photographic_plate_record_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": {
            "digitization_lineage": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "from_id": {"pattern": "^synthetic:(?:glass-plate|image-file):[0-9]{3}(?::[a-z-]+)?$", "type": "string"},
                        "relation": {"enum": ["digitized_as", "derived_as"]},
                        "to_id": {"pattern": "^synthetic:image-file:[0-9]{3}:[a-z-]+$", "type": "string"},
                    },
                    "required": ["from_id", "relation", "to_id"],
                    "type": "object",
                },
                "minItems": 2,
                "type": "array",
            },
            "plates": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "emulsion_side": {"enum": ["front", "back", "unknown"]},
                        "ordinal": {"minimum": 1, "type": "integer"},
                        "orientation": {"enum": ["landscape", "portrait", "square", "unknown"]},
                        "plate_id": {"pattern": "^synthetic:glass-plate:[0-9]{3}$", "type": "string"},
                        "synthetic": {"const": True},
                    },
                    "required": ["emulsion_side", "ordinal", "orientation", "plate_id", "synthetic"],
                    "type": "object",
                },
                "minItems": 1,
                "type": "array",
                "uniqueItems": True,
            },
            "plate_record_id": {
                "pattern": "^synthetic:glass-plate-record:[0-9]{3}$",
                "type": "string",
            },
            "process_profile": {"enum": ["declared_dry_plate", "declared_other", "unknown"]},
            "real_rows": {"const": 0},
            "rights_status": {"enum": ["unknown", "open_gap", "exact_gate"]},
            "synthetic": {"const": True},
        },
        "required": [
            "digitization_lineage",
            "plates",
            "plate_record_id",
            "process_profile",
            "real_rows",
            "rights_status",
            "synthetic",
        ],
        "title": "Synthetic historical glass-photographic-plate record",
        "type": "object",
    }
