#!/usr/bin/env python3
"""Bounded deterministic runtime for Neris Solane v652-v8."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/neris-solane/v652-v8"
PROPOSALS_PATH = PHASE / "preregistration/proposals.json"
MUTATION_PLAN_PATH = PHASE / "validation/preregistered-mutation-plan.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def proposals() -> list[dict[str, Any]]:
    return read_json(PROPOSALS_PATH)["proposals"]


def proposal_by_slug(slug: str) -> dict[str, Any]:
    for row in proposals():
        if row["slug"] == slug:
            return row
    raise KeyError(slug)


def obligations_from_title(title: str) -> list[str]:
    cleaned = title.replace("GMUT ", "", 1).replace("THOS ", "", 1).replace("Freed ID ", "", 1).replace("CBR ", "", 1)
    return [
        item.strip().rstrip(".")
        for item in cleaned.split(",")
        if item.strip()
    ]


def contract_for(proposal: dict[str, Any]) -> dict[str, Any]:
    disposition = proposal["expected_disposition"]
    obligations = obligations_from_title(proposal["title"])
    return {
        "schema": "ghc.family.v652-v8.surface-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "pillar": proposal["pillar"],
        "title": proposal["title"],
        "outcome": disposition,
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "obligations": obligations,
        "obligation_count": len(obligations),
        "falsifier": proposal["null_or_failure_condition"],
        "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"],
        "real_data_rows": 0,
        "production_keys_or_credentials": False,
        "participant_or_authority_decision": False,
        "empirical_confirmation": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def validate_contract(contract: dict[str, Any]) -> list[str]:
    issues = []
    required = {
        "proposal_id",
        "slug",
        "outcome",
        "approval_class",
        "execution_lane",
        "source_ids",
        "obligations",
        "falsifier",
        "acceptance_gate",
        "rollback",
        "protected_gates",
        "terminal_verdict",
    }
    for field in sorted(required - set(contract)):
        issues.append(f"missing:{field}")
    if contract.get("outcome") not in ALLOWED_OUTCOMES:
        issues.append("invalid:outcome")
    if len(contract.get("obligations", [])) < 6:
        issues.append("invalid:obligation_count")
    if not contract.get("source_ids"):
        issues.append("invalid:source_ids")
    if contract.get("real_data_rows") != 0:
        issues.append("forbidden:real_data_rows")
    for field in (
        "production_keys_or_credentials",
        "participant_or_authority_decision",
        "empirical_confirmation",
        "independent_reproduction",
    ):
        if contract.get(field) is not False:
            issues.append(f"forbidden:{field}")
    if contract.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        issues.append("forbidden:terminal_verdict")
    return issues


def mutations_for(proposal_id: str) -> list[dict[str, Any]]:
    return [
        row
        for row in read_json(MUTATION_PLAN_PATH)["mutations"]
        if row["proposal_id"] == proposal_id
    ]


def apply_mutation(contract: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = json.loads(json.dumps(contract))
    kind = mutation["kind"]
    if kind == "drop_required_field":
        candidate.pop("falsifier", None)
    elif kind == "cross_bind_source_or_identifier":
        candidate["proposal_id"] = "CROSS_BOUND_IDENTIFIER"
        candidate["source_ids"] = []
    elif kind == "invert_or_weaken_boundary":
        candidate["protected_gates"] = []
        candidate["real_data_rows"] = 1
    elif kind == "inject_unsupported_promotion":
        candidate["empirical_confirmation"] = True
        candidate["terminal_verdict"] = "READY"
    elif kind == "erase_failure_or_rollback":
        candidate.pop("rollback", None)
    else:  # pragma: no cover - frozen plan guarantees known kinds
        candidate["unknown_mutation"] = kind
    return candidate


def execute_mutations(contract: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    for mutation in mutations_for(contract["proposal_id"]):
        candidate = apply_mutation(contract, mutation)
        issues = validate_contract(candidate)
        if candidate.get("proposal_id") != contract["proposal_id"]:
            issues.append("cross_bound:proposal_id")
        results.append(
            {
                "mutation_id": mutation["mutation_id"],
                "kind": mutation["kind"],
                "expected": "reject_or_quarantine",
                "observed": "rejected" if issues else "accepted",
                "rejected": bool(issues),
                "issue_classes": sorted(set(issues)),
                "credit": "retained_negative" if issues else "failure",
            }
        )
    return results


def bounded_receipt(contract: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    issues = validate_contract(contract)
    rejected = sum(row["rejected"] for row in results)
    return {
        "schema": "ghc.family.v652-v8.bounded-receipt.v1",
        "proposal_id": contract["proposal_id"],
        "slug": contract["slug"],
        "outcome": contract["outcome"],
        "valid_contract": not issues,
        "valid_contract_issues": issues,
        "mutation_count": len(results),
        "rejected_mutation_count": rejected,
        "all_mutations_rejected": rejected == len(results) == 5,
        "real_data_rows": contract["real_data_rows"],
        "empirical_confirmation": False,
        "production_ready": False,
        "professional_validation": False,
        "legal_or_cultural_authority": False,
        "maori_authority": False,
        "complete_accessibility": False,
        "exhaustive_security": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def evaluate_surface(slug: str) -> dict[str, Any]:
    contract = contract_for(proposal_by_slug(slug))
    results = execute_mutations(contract)
    receipt = bounded_receipt(contract, results)
    return {"contract": contract, "mutation_results": results, "receipt": receipt}


def runner_payload(slug: str) -> dict[str, Any]:
    evaluated = evaluate_surface(slug)
    receipt = evaluated["receipt"]
    return {
        "surface": slug,
        "proposal_id": receipt["proposal_id"],
        "outcome": receipt["outcome"],
        "valid": receipt["valid_contract"] and receipt["all_mutations_rejected"],
        "mutation_count": receipt["mutation_count"],
        "rejected": receipt["rejected_mutation_count"],
        "terminal_verdict": receipt["terminal_verdict"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", required=True)
    args = parser.parse_args()
    payload = runner_payload(args.surface)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
