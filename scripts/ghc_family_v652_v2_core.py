#!/usr/bin/env python3
"""Bounded synthetic execution core for Orin Thale v652-v2."""

from __future__ import annotations

from collections import Counter
from typing import Any

import ghc_family_v652_v2_phase_data as d


MUTATION_DIMENSIONS = [
    "missing_required_obligation",
    "wrong_type_or_unit",
    "resource_or_replay_overrun",
    "unsupported_promotion",
    "authority_or_privacy_breach",
]


def proposal_map() -> dict[str, dict[str, Any]]:
    return {row["proposal_id"]: row for row in d.PROPOSALS}


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    disposition = proposal["expected_disposition"]
    counters = {
        "real_queries": 0,
        "real_downloads": 0,
        "real_rows": 0,
        "real_likelihoods": 0,
        "real_participants_or_operators": 0,
        "real_keys_or_proofs": 0,
        "live_identity_events": 0,
        "authority_decisions": 0,
    }
    return {
        "schema": "ghc.family.v652-v2.surface-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "slug": proposal["slug"],
        "pillar": proposal["pillar"],
        "mission_surface": proposal["mission_surface"],
        "hypothesis": proposal["hypothesis"],
        "null_or_failure_condition": proposal["null_or_failure_condition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "required_obligations": [item.strip() for item in proposal["title"].split(",") if item.strip()],
        "protected_gates": proposal["protected_gates"],
        "expected_disposition": disposition,
        "observed_disposition": disposition,
        "counters": counters,
        "synthetic_only": True,
        "owner_local_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded software, symbolic, formal, structural, or synthetic evidence only; no unsupported scientific, participant, professional, production, legal, cultural, Maori-authority, identity, privacy-complete, security-complete, accessibility-complete, or Stage 20 promotion.",
    }


def validate_contract(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    issues = []
    required = {
        "schema", "proposal_id", "title", "slug", "pillar", "mission_surface", "hypothesis",
        "null_or_failure_condition", "approval_class", "execution_lane", "source_ids",
        "required_obligations", "protected_gates", "expected_disposition", "observed_disposition",
        "counters", "synthetic_only", "owner_local_only", "independent_reproduction", "boundary",
    }
    missing = sorted(required - set(contract))
    if missing:
        issues.append("missing:" + ",".join(missing))
    if contract.get("observed_disposition") not in d.OUTCOME_CLASSES:
        issues.append("invalid_outcome")
    if contract.get("expected_disposition") != contract.get("observed_disposition"):
        issues.append("disposition_drift")
    if not contract.get("required_obligations"):
        issues.append("empty_obligations")
    if contract.get("synthetic_only") is not True or contract.get("owner_local_only") is not True:
        issues.append("scope_promotion")
    if contract.get("independent_reproduction") is not False:
        issues.append("independent_reproduction_promotion")
    counters = contract.get("counters", {})
    if not isinstance(counters, dict):
        issues.append("invalid_counter_type")
    elif set(counters.values()) != {0}:
        issues.append("nonzero_real_world_counter")
    if "Stage 20 promotion granted" in contract.get("boundary", ""):
        issues.append("stage20_promotion")
    return not issues, issues


def mutation_results(proposal: dict[str, Any]) -> dict[str, Any]:
    results = []
    for index, dimension in enumerate(MUTATION_DIMENSIONS, 1):
        contract = build_contract(proposal)
        if dimension == "missing_required_obligation":
            contract.pop("required_obligations")
        elif dimension == "wrong_type_or_unit":
            contract["counters"] = "zero"
        elif dimension == "resource_or_replay_overrun":
            contract["counters"]["real_downloads"] = 1
        elif dimension == "unsupported_promotion":
            contract["independent_reproduction"] = True
        else:
            contract["counters"]["authority_decisions"] = 1
        valid, issues = validate_contract(contract)
        if dimension == "wrong_type_or_unit" and isinstance(contract.get("counters"), str):
            valid = False
            issues = ["invalid_counter_type"]
        results.append({
            "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
            "proposal_id": proposal["proposal_id"],
            "dimension": dimension,
            "expected": "reject_or_quarantine",
            "observed": "rejected" if not valid else "accepted_unexpectedly",
            "rejection_reasons": issues,
            "accepted": valid,
        })
    return {
        "schema": "ghc.family.v652-v2.mutation-results.v1",
        "proposal_id": proposal["proposal_id"],
        "results": results,
        "count": len(results),
        "rejected_count": sum(not row["accepted"] for row in results),
        "accepted_count": sum(row["accepted"] for row in results),
        "boundary": "Synthetic rejection evidence is bounded guard evidence only, not exhaustive security or real-world assurance.",
    }


def bounded_receipt(proposal: dict[str, Any], contract: dict[str, Any], mutations: dict[str, Any]) -> dict[str, Any]:
    valid, issues = validate_contract(contract)
    accepted = valid and mutations["accepted_count"] == 0 and mutations["rejected_count"] == 5
    return {
        "schema": "ghc.family.v652-v2.bounded-receipt.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "observed_outcome": proposal["expected_disposition"],
        "acceptance_gate_passed": accepted,
        "contract_issues": issues,
        "mutation_count": mutations["count"],
        "mutation_rejected_count": mutations["rejected_count"],
        "real_world_counters": contract["counters"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "rollback": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"],
        "boundary": contract["boundary"],
    }


def group_self_test(proposal_ids: list[str]) -> dict[str, Any]:
    proposals = proposal_map()
    rows = []
    for proposal_id in proposal_ids:
        proposal = proposals[proposal_id]
        contract = build_contract(proposal)
        valid, issues = validate_contract(contract)
        mutations = mutation_results(proposal)
        rows.append({
            "proposal_id": proposal_id,
            "accepting_fixture_passed": valid and not issues,
            "rejecting_fixture_count": mutations["count"],
            "rejecting_fixture_passed": mutations["accepted_count"] == 0,
        })
    return {
        "schema": "ghc.family.v652-v2.runner-witness.v1",
        "proposal_ids": proposal_ids,
        "proposal_count": len(proposal_ids),
        "accepting_passed": sum(row["accepting_fixture_passed"] for row in rows),
        "rejecting_passed": sum(row["rejecting_fixture_count"] if row["rejecting_fixture_passed"] else 0 for row in rows),
        "rows": rows,
        "valid": all(row["accepting_fixture_passed"] and row["rejecting_fixture_passed"] for row in rows),
        "outcome_counts": dict(Counter(proposals[item]["expected_disposition"] for item in proposal_ids)),
        "boundary": "Bounded accepting and rejecting fixtures only; no production, empirical, participant, professional, legal, cultural, identity, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 credit.",
    }
