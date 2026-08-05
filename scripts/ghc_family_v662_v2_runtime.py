#!/usr/bin/env python3
"""Bounded synthetic thin-section metadata runtime for Elaren Kestrel v662-v2."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import ghc_family_v662_v2_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SPEC_BY_SLUG = {str(row["slug"]): row for row in d.NEW_PROPOSAL_SPECS}
MUTATION_NAMES = (
    "drop_protected_gates",
    "assert_real_world_material",
    "claim_independent_reproduction",
    "promote_stage20",
    "authorize_external_action",
)


def proposal_rows() -> list[dict[str, Any]]:
    payload = json.loads(
        (PHASE / "preregistration/proposal-ledger.json").read_text(encoding="utf-8")
    )
    rows = [
        row
        for row in payload["proposals"]
        if row.get("origin") == "new_unique_v662_v2_proposal"
    ]
    if len(rows) != d.NEW_UNIQUE_COUNT:
        raise RuntimeError("Elaren new-proposal ledger count drift")
    return rows


def proposal_for_slug(slug: str) -> dict[str, Any]:
    for row in proposal_rows():
        if row["slug"] == slug:
            return row
    raise KeyError(slug)


def build_contract(slug: str) -> dict[str, Any]:
    spec = SPEC_BY_SLUG[slug]
    proposal = proposal_for_slug(slug)
    return {
        "schema": "ghc.family.v662-v2.synthetic-thin-section-contract.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "proposal_id": proposal["proposal_id"],
        "slug": slug,
        "title": spec["title"],
        "expected_disposition": spec["outcome"],
        "pillar_relation": spec["pillar"],
        "mechanism": spec["mechanism"],
        "official_or_primary_source_needs": spec["sources"],
        "fixture": {
            "synthetic_alias": f"surrogate-{slug}",
            "synthetic_only": True,
            "real_samples_slides_records_people_operations_images_or_protected_data_used": False,
            "real_world_rows": 0,
            "external_actions": 0,
            "network_calls": 0,
        },
        "protected_gates": list(d.PROTECTED_GATES),
        "authority": {
            "external_action_authorized": False,
            "professional_authority_claimed": False,
            "legal_or_cultural_authority_claimed": False,
            "maori_authority_claimed": False,
        },
        "evidence": {
            "same_owner_only": True,
            "independent_reproduction": False,
            "empirical_confirmation": False,
            "privacy_complete": False,
            "accessibility_complete": False,
            "exhaustive_security": False,
        },
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "rollback": "Reject the candidate, retain the failed witness, and leave all people, property, production, authority, sibling, remote, and external state unchanged.",
    }


def validate_contract(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    slug = contract.get("slug")
    spec = SPEC_BY_SLUG.get(str(slug))
    if contract.get("schema") != "ghc.family.v662-v2.synthetic-thin-section-contract.v1":
        errors.append("schema")
    if spec is None:
        errors.append("slug")
        return False, errors
    if contract.get("expected_disposition") != spec["outcome"]:
        errors.append("disposition")
    if contract.get("mechanism") != spec["mechanism"]:
        errors.append("mechanism")
    if contract.get("official_or_primary_source_needs") != spec["sources"]:
        errors.append("sources")
    fixture = contract.get("fixture", {})
    if fixture.get("synthetic_only") is not True:
        errors.append("synthetic_only")
    if fixture.get(
        "real_samples_slides_records_people_operations_images_or_protected_data_used"
    ) is not False:
        errors.append("real_world_material")
    for key in ("real_world_rows", "external_actions", "network_calls"):
        if fixture.get(key) != 0:
            errors.append(key)
    if contract.get("protected_gates") != d.PROTECTED_GATES:
        errors.append("protected_gates")
    authority = contract.get("authority", {})
    if any(value is not False for value in authority.values()):
        errors.append("authority")
    evidence = contract.get("evidence", {})
    if evidence.get("same_owner_only") is not True:
        errors.append("same_owner_only")
    for key in (
        "independent_reproduction",
        "empirical_confirmation",
        "privacy_complete",
        "accessibility_complete",
        "exhaustive_security",
    ):
        if evidence.get(key) is not False:
            errors.append(key)
    if contract.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        errors.append("terminal_verdict")
    return not errors, sorted(set(errors))


def mutated_contract(contract: dict[str, Any], mutation: str) -> dict[str, Any]:
    candidate = copy.deepcopy(contract)
    if mutation == "drop_protected_gates":
        candidate["protected_gates"] = []
    elif mutation == "assert_real_world_material":
        candidate["fixture"][
            "real_samples_slides_records_people_operations_images_or_protected_data_used"
        ] = True
    elif mutation == "claim_independent_reproduction":
        candidate["evidence"]["independent_reproduction"] = True
    elif mutation == "promote_stage20":
        candidate["terminal_verdict"] = "READY_FOR_STAGE_20"
    elif mutation == "authorize_external_action":
        candidate["authority"]["external_action_authorized"] = True
    else:
        raise KeyError(mutation)
    return candidate


def evaluate_slug(slug: str) -> dict[str, Any]:
    contract = build_contract(slug)
    valid, errors = validate_contract(contract)
    mutation_rows: list[dict[str, Any]] = []
    for index, mutation in enumerate(MUTATION_NAMES, 1):
        candidate = mutated_contract(contract, mutation)
        accepted, mutation_errors = validate_contract(candidate)
        mutation_rows.append(
            {
                "mutation_id": f"{proposal_for_slug(slug)['proposal_id']}-M{index:02d}",
                "mutation": mutation,
                "accepted": accepted,
                "rejected": not accepted,
                "errors": mutation_errors,
                "credit": 0,
            }
        )
    return {
        "contract": contract,
        "valid_fixture": valid,
        "valid_fixture_errors": errors,
        "mutations": mutation_rows,
        "all_mutations_rejected": all(row["rejected"] for row in mutation_rows),
        "observed_disposition": contract["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def runner_receipt(slug: str) -> dict[str, Any]:
    result = evaluate_slug(slug)
    return {
        "schema": "ghc.family.v662-v2.runner-receipt.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "slug": slug,
        "proposal_id": result["contract"]["proposal_id"],
        "valid_fixture": result["valid_fixture"],
        "mutation_count": len(result["mutations"]),
        "mutations_rejected": sum(row["rejected"] for row in result["mutations"]),
        "observed_disposition": result["observed_disposition"],
        "external_actions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def cli(slug: str) -> None:
    receipt = runner_receipt(slug)
    if not receipt["valid_fixture"] or receipt["mutations_rejected"] != 5:
        raise SystemExit(1)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: ghc_family_v662_v2_runtime.py <slug>")
    cli(sys.argv[1])
