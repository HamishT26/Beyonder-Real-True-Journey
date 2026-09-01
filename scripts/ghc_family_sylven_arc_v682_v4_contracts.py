"""Bounded zero-row sextant and celestial-navigation contracts for Sylven Arc v682-v4.

These functions validate synthetic fixture structure only. They do not observe a
real object, authorize work, identify materials, make safety decisions, or close
any empirical, professional, legal, cultural, affected-party, Māori-authority,
or Stage 20 gate.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


REQUIRED_FIELDS = {
    "proposal_id",
    "fixture_kind",
    "surrogate_id",
    "synthetic",
    "real_row_count",
    "observation_status",
    "authority_status",
    "boundary",
    "provenance_digest",
    "lifecycle_order",
    "safety_status",
    "empirical_status",
}

PROTECTED_GATES = [
    "empirical_or_participant_evidence",
    "professional_or_safety_authority",
    "production_or_deployment_readiness",
    "real_identity_lifecycle_or_trust_governance",
    "legal_cultural_affected_party_or_maori_authority",
    "privacy_complete_accessibility_complete_or_exhaustive_security",
    "independent_reproduction_agi_asi_consciousness_personhood_toe_canon_or_stage20",
]


def proposal_digest(proposal: dict[str, Any]) -> str:
    payload = {
        "expected_disposition": proposal["expected_disposition"],
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": proposal["proposal_id"],
        "fixture_kind": "owner_local_synthetic_contract",
        "surrogate_id": f"SYN-{proposal['proposal_id']}",
        "synthetic": True,
        "real_row_count": 0,
        "observation_status": "absent",
        "authority_status": "reserved",
        "boundary": "owner_local_zero_row_only",
        "provenance_digest": proposal_digest(proposal),
        "lifecycle_order": ["plan", "fixture", "decision"],
        "safety_status": "not_assessed_no_release",
        "empirical_status": "not_observed_not_claimed",
    }


def validate_fixture(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(fixture))
    if missing:
        reasons.append("missing_required_fields:" + ",".join(missing))
    if fixture.get("proposal_id") != proposal.get("proposal_id"):
        reasons.append("proposal_identity_mismatch")
    if fixture.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if fixture.get("real_row_count") != 0:
        reasons.append("real_rows_forbidden")
    if fixture.get("observation_status") != "absent":
        reasons.append("observation_promotion_forbidden")
    if fixture.get("authority_status") != "reserved":
        reasons.append("authority_promotion_forbidden")
    if fixture.get("boundary") != "owner_local_zero_row_only":
        reasons.append("boundary_mismatch")
    if fixture.get("provenance_digest") != proposal_digest(proposal):
        reasons.append("stale_provenance_digest")
    if fixture.get("lifecycle_order") != ["plan", "fixture", "decision"]:
        reasons.append("lifecycle_order_invalid")
    if fixture.get("safety_status") != "not_assessed_no_release":
        reasons.append("safety_promotion_forbidden")
    if fixture.get("empirical_status") != "not_observed_not_claimed":
        reasons.append("empirical_promotion_forbidden")
    return {
        "accepted": not reasons,
        "proposal_id": proposal.get("proposal_id"),
        "protected_gates": PROTECTED_GATES,
        "reasons": reasons,
        "scope": "bounded_synthetic_structure_only",
    }


def mutated_fixture(proposal: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    fixture = copy.deepcopy(positive_fixture(proposal))
    if mutation_type == "missing_required_field":
        fixture.pop("surrogate_id")
    elif mutation_type == "lifecycle_inversion":
        fixture["lifecycle_order"] = ["decision", "fixture", "plan"]
    elif mutation_type == "stale_provenance_digest":
        fixture["provenance_digest"] = "0" * 64
    elif mutation_type == "safety_status_promotion":
        fixture["safety_status"] = "released_for_real_work"
    elif mutation_type == "authority_promotion":
        fixture["authority_status"] = "granted_by_software"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    return fixture


def execute_proposal(proposal: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    positive = validate_fixture(proposal, positive_fixture(proposal))
    mutation_results: list[dict[str, Any]] = []
    for mutation in proposal["preregistered_rejecting_mutations"]:
        decision = validate_fixture(
            proposal,
            mutated_fixture(proposal, mutation["mutation_type"]),
        )
        mutation_results.append(
            {
                "accepted": decision["accepted"],
                "mutation_id": mutation["mutation_id"],
                "mutation_type": mutation["mutation_type"],
                "proposal_id": proposal["proposal_id"],
                "reasons": decision["reasons"],
                "retained_zero_credit": True,
            }
        )
    outcome = {
        "bounded_positive_accepted": positive["accepted"],
        "disposition": proposal["expected_disposition"],
        "empirical_or_authority_credit": False,
        "invalid_mutations_accepted": sum(1 for row in mutation_results if row["accepted"]),
        "invalid_mutations_rejected": sum(1 for row in mutation_results if not row["accepted"]),
        "observation_status": "absent",
        "proposal_id": proposal["proposal_id"],
        "real_row_count": 0,
        "scope": "owner_local_synthetic_zero_row",
        "title": proposal["title"],
    }
    return outcome, mutation_results
