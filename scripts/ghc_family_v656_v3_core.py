#!/usr/bin/env python3
"""Bounded stained-glass conservation contract and mutation engine for v656-v3."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import ghc_family_v656_v3_phase_data as d


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / d.PHASE_ROOT
MUTATION_DIMENSIONS = [
    "missing_required_obligation",
    "wrong_type_or_domain",
    "resource_or_freshness_overrun",
    "unsupported_promotion",
    "authority_privacy_or_route_breach",
]
COMMON_REQUIRED = [
    "proposal_id",
    "mechanism",
    "expected_disposition",
    "approval_class",
    "execution_lane",
    "source_ids",
    "mechanism_fields",
    "protected_gates",
    "rollback",
    "evidence_boundary",
    "external_action_counts",
    "promotion_claims",
]
ZERO_EXTERNAL_COUNTS = {
    "accounts": 0,
    "api_keys": 0,
    "live_credentials": 0,
    "live_identity_resolutions": 0,
    "live_status_or_revocation_events": 0,
    "real_people": 0,
    "real_owners_custodians_donors_conservators_or_glaziers": 0,
    "real_buildings_openings_panels_fragments_glass_lead_or_hardware": 0,
    "real_soldering_heating_cutting_lifting_cleaning_or_imaging_equipment": 0,
    "real_treatment_reassembly_packing_transport_installation_or_return_actions": 0,
    "real_material_optical_structural_or_environmental_measurements": 0,
    "real_custody_access_return_or_remedy_actions": 0,
    "real_incident_stop_work_lockout_or_safety_actions": 0,
    "real_privacy_legal_or_compliance_decisions": 0,
    "professional_conservation_glazing_heritage_engineering_or_safety_decisions": 0,
    "cultural_or_community_decisions": 0,
    "production_deployments": 0,
    "authority_decisions": 0,
    "real_data_rows": 0,
    "real_likelihoods": 0,
}
ZERO_PROMOTION_CLAIMS = {
    "independent_reproduction": False,
    "empirical_confirmation": False,
    "production_ready": False,
    "privacy_complete": False,
    "accessibility_complete": False,
    "exhaustive_security": False,
    "professional_validation": False,
    "legal_or_cultural_ratification": False,
    "maori_authority": False,
    "agi_or_asi": False,
    "consciousness_or_personhood": False,
    "theory_of_everything": False,
    "stage20": False,
}


def mechanism_fields(proposal: dict[str, Any]) -> list[str]:
    words = [
        token.replace("-", "_")
        for token in proposal["slug"].split("-")
        if token
    ]
    fields = [
        "declared_scope",
        "evidence_class",
        "freshness_or_time_boundary",
        "failure_or_conflict_state",
        "recovery_or_rollback",
        "authority_ceiling",
    ]
    return list(dict.fromkeys(words + fields))


def valid_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    disposition = proposal["expected_disposition"]
    evidence_kind = {
        "completed": "bounded_structural_software",
        "represented": "synthetic_protocol_proxy",
        "open_gap": "zero_live_action_readiness",
        "exact_gate": "unresolved_authority_reservation",
    }[disposition]
    return {
        "schema": "ghc.family.v656-v3.surface-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "slug": proposal["slug"],
        "pillar": proposal["pillar"],
        "mechanism": proposal["mechanism"],
        "expected_disposition": disposition,
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "mechanism_fields": mechanism_fields(proposal),
        "required_obligations": COMMON_REQUIRED,
        "protected_gates": proposal["protected_gates"],
        "rollback": proposal["rollback_or_recovery"],
        "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "evidence_kind": evidence_kind,
        "evidence_boundary": (
            "Owner-local deterministic structure and frozen synthetic mutations "
            "only; no real person, worker, owner, custodian, donor, conservator, glazier, "
            "building, opening, panel, fragment, glass, lead, hardware, machine, tool, "
            "measurement, inspection, material test, treatment, reassembly, packing, "
            "transport, installation, custody action, return, remedy, incident, stop-work, "
            "lockout, safety, privacy, legal, compliance, or professional decision; "
            "external, empirical, participant, production, professional, legal, "
            "cultural, Māori-authority, independence, personhood, "
            "Theory-of-Everything, or Stage 20 credit."
        ),
        "resource_budget": {
            "network_actions": 0,
            "external_writes": 0,
            "replays_after_success": 0,
            "freshness_mode": "fixture_bound",
        },
        "external_action_counts": copy.deepcopy(ZERO_EXTERNAL_COUNTS),
        "promotion_claims": copy.deepcopy(ZERO_PROMOTION_CLAIMS),
    }


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors = []
    for field in COMMON_REQUIRED:
        if field not in contract:
            errors.append(f"missing:{field}")
    if errors:
        return errors
    proposal = next(
        (
            row
            for row in d.PROPOSALS
            if row["proposal_id"] == contract.get("proposal_id")
        ),
        None,
    )
    if proposal is None:
        errors.append("unknown:proposal_id")
        return errors
    scalar_expectations = {
        "mechanism": proposal["mechanism"],
        "expected_disposition": proposal["expected_disposition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
    }
    for field, expected in scalar_expectations.items():
        if contract.get(field) != expected:
            errors.append(f"mismatch:{field}")
    if contract.get("source_ids") != proposal["official_or_primary_source_needs"]:
        errors.append("mismatch:source_ids")
    if contract.get("mechanism_fields") != mechanism_fields(proposal):
        errors.append("mismatch:mechanism_fields")
    if contract.get("protected_gates") != proposal["protected_gates"]:
        errors.append("mismatch:protected_gates")
    if contract.get("rollback") != proposal["rollback_or_recovery"]:
        errors.append("mismatch:rollback")
    if not isinstance(contract.get("evidence_boundary"), str):
        errors.append("type:evidence_boundary")
    if contract.get("resource_budget") != {
        "network_actions": 0,
        "external_writes": 0,
        "replays_after_success": 0,
        "freshness_mode": "fixture_bound",
    }:
        errors.append("budget:resource_or_freshness")
    if contract.get("external_action_counts") != ZERO_EXTERNAL_COUNTS:
        errors.append("external_action_or_authority_breach")
    if contract.get("promotion_claims") != ZERO_PROMOTION_CLAIMS:
        errors.append("unsupported_promotion")
    return errors


def mutate(contract: dict[str, Any], dimension: str) -> dict[str, Any]:
    candidate = copy.deepcopy(contract)
    if dimension == "missing_required_obligation":
        candidate.pop("rollback", None)
    elif dimension == "wrong_type_or_domain":
        candidate["mechanism_fields"] = "not-a-list"
    elif dimension == "resource_or_freshness_overrun":
        candidate["resource_budget"]["replays_after_success"] = 1
        candidate["resource_budget"]["freshness_mode"] = "unbounded"
    elif dimension == "unsupported_promotion":
        candidate["promotion_claims"]["stage20"] = True
        candidate["promotion_claims"]["production_ready"] = True
    elif dimension == "authority_privacy_or_route_breach":
        candidate["external_action_counts"]["authority_decisions"] = 1
        candidate["external_action_counts"]["live_credentials"] = 1
    else:
        raise KeyError(dimension)
    return candidate


def execute_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    contract = valid_contract(proposal)
    valid_errors = validate_contract(contract)
    mutation_rows = []
    for index, dimension in enumerate(MUTATION_DIMENSIONS, 1):
        candidate = mutate(contract, dimension)
        errors = validate_contract(candidate)
        mutation_rows.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
                "proposal_id": proposal["proposal_id"],
                "dimension": dimension,
                "accepted": not errors,
                "rejected": bool(errors),
                "errors": errors,
                "credit": "retained_synthetic_negative" if errors else "invalid_acceptance",
            }
        )
    return {
        "proposal_id": proposal["proposal_id"],
        "contract": contract,
        "valid_fixture_passed": not valid_errors,
        "valid_fixture_errors": valid_errors,
        "mutation_results": mutation_rows,
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_rows),
        "accepted_mutation_count": sum(row["accepted"] for row in mutation_rows),
        "observed_outcome": proposal["expected_disposition"],
    }


def execute_group(group_index: int) -> dict[str, Any]:
    if group_index < 1 or group_index > 10:
        raise ValueError("group_index must be 1 through 10")
    start = (group_index - 1) * 3
    results = [execute_proposal(row) for row in d.PROPOSALS[start : start + 3]]
    return {
        "schema": "ghc.family.v656-v3.runner-result.v1",
        "group": group_index,
        "proposal_ids": [row["proposal_id"] for row in results],
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in results),
        "rejected_mutation_count": sum(
            row["rejected_mutation_count"] for row in results
        ),
        "accepted_mutation_count": sum(
            row["accepted_mutation_count"] for row in results
        ),
        "results": results,
        "boundary": (
            "Three owner-local synthetic contracts only; no external action or "
            "authority credit."
        ),
    }


def execute_all() -> dict[str, Any]:
    groups = [execute_group(index) for index in range(1, 11)]
    results = [row for group in groups for row in group["results"]]
    return {
        "schema": "ghc.family.v656-v3.suite-result.v1",
        "proposal_count": len(results),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in results),
        "rejected_mutation_count": sum(
            row["rejected_mutation_count"] for row in results
        ),
        "accepted_mutation_count": sum(
            row["accepted_mutation_count"] for row in results
        ),
        "groups": groups,
        "results": results,
        "boundary": (
            "Deterministic owner-local evidence only; same-owner shared "
            "infrastructure is not independent reproduction."
        ),
    }


def write_group_receipt(group_index: int, output: Path) -> dict[str, Any]:
    payload = execute_group(group_index)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return payload


def group_main(group_index: int, runner_name: str) -> None:
    parser = argparse.ArgumentParser(description=runner_name)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = execute_group(group_index)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "runner": runner_name,
                "group": group_index,
                "valid": payload["valid_fixture_count"],
                "rejected": payload["rejected_mutation_count"],
                "accepted": payload["accepted_mutation_count"],
            },
            sort_keys=True,
        )
    )


def suite_main(runner_name: str) -> None:
    parser = argparse.ArgumentParser(description=runner_name)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = execute_all()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "runner": runner_name,
                "proposals": payload["proposal_count"],
                "valid": payload["valid_fixture_count"],
                "rejected": payload["rejected_mutation_count"],
                "accepted": payload["accepted_mutation_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    print(json.dumps(execute_all(), ensure_ascii=False, sort_keys=True))
