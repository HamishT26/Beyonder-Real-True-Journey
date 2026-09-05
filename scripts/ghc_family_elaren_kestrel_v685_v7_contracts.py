"""Bounded zero-device proposal contracts for Elaren Kestrel v685-v7."""

from __future__ import annotations

import hashlib
import json
from typing import Any

PHASE = "v685-v7"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
REQUIRED_PROPOSAL_FIELDS = {
    "proposal_id",
    "family",
    "practice",
    "title",
    "approval_class",
    "execution_lane",
    "expected_execution_disposition",
    "hypothesis",
    "null_or_failure_condition",
    "official_or_primary_source_needs",
    "concrete_artifacts",
    "falsifier_or_acceptance_gate",
    "rollback_or_recovery",
    "protected_gates",
    "preregistered_rejecting_mutations",
}


def proposal_digest(proposal: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            proposal,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.elaren-v685-v7.proposal-fixture.v1",
        "proposal_id": proposal["proposal_id"],
        "family": proposal["family"],
        "phase": PHASE,
        "source": SOURCE,
        "planning_digest": proposal_digest(proposal),
        "lifecycle": ["planning_x1", "execution_x2"],
        "real_rows": 0,
        "real_devices": 0,
        "real_people": 0,
        "network_calls": 0,
        "authority_claim": "none",
        "empirical_claim": False,
        "production_claim": False,
        "observed_disposition": proposal["expected_execution_disposition"],
    }


def mutated_fixture(
    proposal: dict[str, Any], mutation_type: str
) -> dict[str, Any]:
    fixture = positive_fixture(proposal)
    if mutation_type == "missing_required_field":
        fixture.pop("source")
    elif mutation_type == "lifecycle_inversion":
        fixture["lifecycle"] = ["execution_x2", "planning_x1"]
    elif mutation_type == "stale_provenance_digest":
        fixture["planning_digest"] = "0" * 64
    elif mutation_type == "empirical_status_promotion":
        fixture["empirical_claim"] = True
        fixture["real_rows"] = 1
    elif mutation_type == "authority_status_promotion":
        fixture["authority_claim"] = "granted"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    return fixture


def validate_fixture(
    proposal: dict[str, Any], fixture: dict[str, Any]
) -> dict[str, Any]:
    errors: list[str] = []
    if not REQUIRED_PROPOSAL_FIELDS <= set(proposal):
        errors.append("proposal_missing_required_field")
    required_fixture = {
        "schema",
        "proposal_id",
        "family",
        "phase",
        "source",
        "planning_digest",
        "lifecycle",
        "real_rows",
        "real_devices",
        "real_people",
        "network_calls",
        "authority_claim",
        "empirical_claim",
        "production_claim",
        "observed_disposition",
    }
    if not required_fixture <= set(fixture):
        errors.append("fixture_missing_required_field")
    else:
        if fixture["proposal_id"] != proposal["proposal_id"]:
            errors.append("proposal_id_mismatch")
        if fixture["family"] != proposal["family"]:
            errors.append("family_mismatch")
        if fixture["phase"] != PHASE or fixture["source"] != SOURCE:
            errors.append("phase_or_source_mismatch")
        if fixture["planning_digest"] != proposal_digest(proposal):
            errors.append("planning_digest_mismatch")
        if fixture["lifecycle"] != ["planning_x1", "execution_x2"]:
            errors.append("lifecycle_order_invalid")
        if type(fixture["real_rows"]) is not int or fixture["real_rows"] != 0:
            errors.append("real_rows_nonzero_or_malformed")
        if type(fixture["real_devices"]) is not int or fixture["real_devices"] != 0:
            errors.append("real_devices_nonzero_or_malformed")
        if type(fixture["real_people"]) is not int or fixture["real_people"] != 0:
            errors.append("real_people_nonzero_or_malformed")
        if type(fixture["network_calls"]) is not int or fixture["network_calls"] != 0:
            errors.append("network_calls_nonzero_or_malformed")
        if fixture["authority_claim"] != "none":
            errors.append("authority_promotion")
        if fixture["empirical_claim"] is not False:
            errors.append("empirical_promotion")
        if fixture["production_claim"] is not False:
            errors.append("production_promotion")
        if fixture["observed_disposition"] != proposal["expected_execution_disposition"]:
            errors.append("disposition_mismatch")
    return {"accepted": not errors, "errors": errors}


def execute_proposal(
    proposal: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    positive = validate_fixture(proposal, positive_fixture(proposal))
    mutations = []
    for mutation in proposal["preregistered_rejecting_mutations"]:
        result = validate_fixture(
            proposal, mutated_fixture(proposal, mutation["mutation_type"])
        )
        mutations.append(
            {
                "mutation_id": mutation["mutation_id"],
                "proposal_id": proposal["proposal_id"],
                "mutation_type": mutation["mutation_type"],
                "accepted": result["accepted"],
                "errors": result["errors"],
                "completion_credit": 0,
                "retained": True,
            }
        )
    return (
        {
            "proposal_id": proposal["proposal_id"],
            "family": proposal["family"],
            "title": proposal["title"],
            "disposition": proposal["expected_execution_disposition"],
            "bounded_positive_accepted": positive["accepted"],
            "positive_errors": positive["errors"],
            "invalid_mutations_rejected": sum(not row["accepted"] for row in mutations),
            "invalid_mutations_accepted": sum(row["accepted"] for row in mutations),
            "real_rows": 0,
            "real_devices": 0,
            "real_people": 0,
            "same_owner_only": True,
        },
        mutations,
    )
