"""Zero-row coordinate-metadata and uncertainty-documentation contracts.

These contracts operate only on synthetic dictionaries. They do not transform a
coordinate, evaluate a measurement, process personal information, make a rights
decision, or exercise scientific, operational, professional, legal, cultural,
affected-party, or Maori authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_FIELDS = {
    "proposal_id",
    "synthetic",
    "real_row_count",
    "observation_status",
    "authority_status",
    "claim_scope",
    "failure_retention",
    "expected_outcome",
    "coordinate_values",
    "measurement_values",
    "personal_information",
}


def fixture_digest(fixture: dict[str, Any]) -> str:
    payload = json.dumps(fixture, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": proposal["proposal_id"],
        "synthetic": True,
        "real_row_count": 0,
        "observation_status": "absent",
        "authority_status": "reserved",
        "claim_scope": "bounded_synthetic_structure_only",
        "failure_retention": True,
        "expected_outcome": proposal["expected_execution_disposition"],
        "coordinate_values": [],
        "measurement_values": [],
        "personal_information": [],
    }


def validate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(fixture))
    if missing:
        errors.append("missing_fields:" + ",".join(missing))
    if fixture.get("synthetic") is not True:
        errors.append("synthetic_marker_required")
    if fixture.get("real_row_count") != 0:
        errors.append("real_rows_forbidden")
    if fixture.get("observation_status") != "absent":
        errors.append("observation_must_remain_absent")
    if fixture.get("authority_status") != "reserved":
        errors.append("authority_must_remain_reserved")
    if fixture.get("claim_scope") != "bounded_synthetic_structure_only":
        errors.append("claim_promotion_forbidden")
    if fixture.get("failure_retention") is not True:
        errors.append("failure_erasure_forbidden")
    if fixture.get("expected_outcome") not in ALLOWED_OUTCOMES:
        errors.append("outcome_label_forbidden")
    if fixture.get("coordinate_values") != []:
        errors.append("coordinate_values_forbidden")
    if fixture.get("measurement_values") != []:
        errors.append("measurement_values_forbidden")
    if fixture.get("personal_information") != []:
        errors.append("personal_information_forbidden")
    return {
        "proposal_id": fixture.get("proposal_id"),
        "accepted": not errors,
        "errors": errors,
        "fixture_sha256": fixture_digest(fixture),
        "evidence_scope": "bounded_synthetic_structure_only",
    }


def mutated_fixture(proposal: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    fixture = copy.deepcopy(positive_fixture(proposal))
    if mutation_type == "remove_synthetic_marker":
        fixture["synthetic"] = False
    elif mutation_type == "inject_real_row":
        fixture["real_row_count"] = 1
        fixture["coordinate_values"] = ["WITHHELD_REAL_VALUE"]
    elif mutation_type == "promote_claim":
        fixture["claim_scope"] = "empirical_confirmation"
    elif mutation_type == "erase_failure":
        fixture["failure_retention"] = False
    elif mutation_type == "bypass_authority_hold":
        fixture["authority_status"] = "self_granted"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    return fixture


def execute_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    positive = positive_fixture(proposal)
    positive_receipt = validate_fixture(positive)
    mutation_receipts = []
    for mutation in proposal["preregistered_rejecting_mutations"]:
        fixture = mutated_fixture(proposal, mutation["mutation_type"])
        receipt = validate_fixture(fixture)
        mutation_receipts.append(
            {
                "mutation_id": mutation["mutation_id"],
                "mutation_type": mutation["mutation_type"],
                "expected_result": mutation["expected_result"],
                "rejected": not receipt["accepted"],
                "errors": receipt["errors"],
                "fixture_sha256": receipt["fixture_sha256"],
                "completion_credit": 0,
            }
        )
    expected = proposal["expected_execution_disposition"]
    return {
        "proposal_id": proposal["proposal_id"],
        "positive_control": positive_receipt,
        "mutation_receipts": mutation_receipts,
        "outcome": expected,
        "outcome_basis": (
            "bounded software and synthetic fixture evidence"
            if expected == "completed"
            else "structure represented while broader evidence remains absent"
            if expected == "represented"
            else "evidence-dependent work remains open"
            if expected == "open_gap"
            else "competent or affected human authority remains required"
        ),
        "broader_claim_credit": 0,
    }
