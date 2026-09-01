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


def density_record_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": {
            "certificate_record_id": {"pattern": "^synthetic:hydrometer:[0-9]{3}$", "type": "string"},
            "density_kg_m3": {"minimum": 0, "type": "number"},
            "reference_temperature_c": {"type": "number"},
            "scale_family": {
                "enum": ["density_kg_m3", "relative_density", "api_gravity", "baume", "proof"]
            },
            "synthetic": {"const": True},
            "uncertainty_kg_m3": {"exclusiveMinimum": 0, "type": "number"},
        },
        "required": [
            "certificate_record_id",
            "density_kg_m3",
            "reference_temperature_c",
            "scale_family",
            "synthetic",
            "uncertainty_kg_m3",
        ],
        "title": "Synthetic hydrometer density record",
        "type": "object",
    }
