#!/usr/bin/env python3
"""Bounded synthetic contracts for Caelen Ash v684-v6.

No function accepts a live data source, performs a network request, controls a
device, issues a credential, or makes an authority decision.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
MUTATION_TYPES = [
    "remove_synthetic_marker",
    "inject_real_row_or_identity",
    "promote_claim_or_authority",
    "erase_failure_or_correction_lineage",
    "bypass_open_or_exact_gate",
]


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    """Return the preregistered zero-row positive fixture for one proposal."""

    disposition = proposal["expected_disposition"]
    fixture: dict[str, Any] = {
        "proposal_id": proposal["proposal_id"],
        "synthetic": True,
        "real_rows": 0,
        "real_identities": 0,
        "authority_action": False,
        "promoted_claim": False,
        "retained_failure_ids": ["CA6846-BOUNDARY-SENTINEL"],
        "correction_lineage": ["frozen-x1", "bounded-x2"],
        "expected_disposition": disposition,
        "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Owner-local synthetic software evidence only.",
    }
    if disposition == "completed":
        fixture["bounded_contract_state"] = "accepted"
    elif disposition == "represented":
        fixture.update(
            {
                "representation_only": True,
                "real_world_evidence_present": False,
                "operational_effectiveness_claimed": False,
            }
        )
    elif disposition == "open_gap":
        fixture.update(
            {
                "open_gap": True,
                "external_evidence_present": False,
                "gap_silently_closed": False,
            }
        )
    elif disposition == "exact_gate":
        fixture.update(
            {
                "exact_gate": True,
                "competent_authority_present": False,
                "authority_gate_bypassed": False,
            }
        )
    return fixture


def validate_fixture(fixture: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate one bounded fixture and return every fail-closed reason."""

    errors: list[str] = []
    if fixture.get("synthetic") is not True:
        errors.append("synthetic_marker_required")
    if fixture.get("real_rows") != 0:
        errors.append("real_rows_forbidden")
    if fixture.get("real_identities") != 0:
        errors.append("real_identities_forbidden")
    if fixture.get("authority_action") is not False:
        errors.append("authority_action_forbidden")
    if fixture.get("promoted_claim") is not False:
        errors.append("claim_promotion_forbidden")
    if not fixture.get("retained_failure_ids"):
        errors.append("retained_failure_required")
    if len(fixture.get("correction_lineage") or []) < 2:
        errors.append("correction_lineage_required")
    disposition = fixture.get("expected_disposition")
    if disposition not in ALLOWED_OUTCOMES:
        errors.append("outcome_label_forbidden")
    if set(fixture.get("allowed_outcomes") or []) != ALLOWED_OUTCOMES:
        errors.append("four_label_vocabulary_required")
    if fixture.get("stage20_verdict") != "NOT_READY_FOR_STAGE_20":
        errors.append("stage20_nonpromotion_required")
    if disposition == "completed" and fixture.get("bounded_contract_state") != "accepted":
        errors.append("bounded_contract_not_accepted")
    if disposition == "represented":
        if fixture.get("representation_only") is not True:
            errors.append("representation_marker_required")
        if fixture.get("real_world_evidence_present") is not False:
            errors.append("real_world_evidence_forbidden")
        if fixture.get("operational_effectiveness_claimed") is not False:
            errors.append("effectiveness_claim_forbidden")
    if disposition == "open_gap":
        if fixture.get("open_gap") is not True:
            errors.append("open_gap_marker_required")
        if fixture.get("external_evidence_present") is not False:
            errors.append("external_evidence_not_observed")
        if fixture.get("gap_silently_closed") is not False:
            errors.append("open_gap_cannot_close_silently")
    if disposition == "exact_gate":
        if fixture.get("exact_gate") is not True:
            errors.append("exact_gate_marker_required")
        if fixture.get("competent_authority_present") is not False:
            errors.append("authority_not_observed")
        if fixture.get("authority_gate_bypassed") is not False:
            errors.append("authority_gate_bypass_forbidden")
    return not errors, errors


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    """Apply one preregistered invalid mutation to a copied fixture."""

    if mutation_type not in MUTATION_TYPES:
        raise ValueError(f"unknown mutation: {mutation_type}")
    changed = deepcopy(fixture)
    if mutation_type == "remove_synthetic_marker":
        changed["synthetic"] = False
    elif mutation_type == "inject_real_row_or_identity":
        changed["real_rows"] = 1
        changed["real_identities"] = 1
    elif mutation_type == "promote_claim_or_authority":
        changed["promoted_claim"] = True
        changed["authority_action"] = True
    elif mutation_type == "erase_failure_or_correction_lineage":
        changed["retained_failure_ids"] = []
        changed["correction_lineage"] = []
    elif mutation_type == "bypass_open_or_exact_gate":
        changed["stage20_verdict"] = "READY_FOR_STAGE_20"
        if changed.get("expected_disposition") == "open_gap":
            changed["gap_silently_closed"] = True
        if changed.get("expected_disposition") == "exact_gate":
            changed["authority_gate_bypassed"] = True
    return changed


def evaluate_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one positive fixture and its five frozen invalid mutations."""

    fixture = positive_fixture(proposal)
    positive_pass, positive_errors = validate_fixture(fixture)
    mutations = []
    for preregistered in proposal["preregistered_rejecting_mutations"]:
        invalid = mutate(fixture, preregistered["mutation_type"])
        invalid_pass, errors = validate_fixture(invalid)
        mutations.append(
            {
                "mutation_id": preregistered["mutation_id"],
                "mutation_type": preregistered["mutation_type"],
                "accepted": invalid_pass,
                "rejected": not invalid_pass,
                "reasons": errors,
                "completion_credit": 0,
            }
        )
    return {
        "proposal_id": proposal["proposal_id"],
        "fixture": fixture,
        "positive_pass": positive_pass,
        "positive_errors": positive_errors,
        "mutations": mutations,
        "all_mutations_rejected": all(item["rejected"] for item in mutations),
    }
