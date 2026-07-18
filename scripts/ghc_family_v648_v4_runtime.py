#!/usr/bin/env python3
"""Rule-driven runtime for Ilyra Fen's bounded v648-v4 contract runners."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate_evidence(rules: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key in rules.get("required_true", []):
        if evidence.get(key) is not True:
            issues.append(f"{key}:required_true")
    for key in rules.get("required_false", []):
        if evidence.get(key) is not False:
            issues.append(f"{key}:required_false")
    for key in rules.get("required_zero", []):
        if evidence.get(key) != 0:
            issues.append(f"{key}:required_zero")
    for key in rules.get("required_nonempty", []):
        if not isinstance(evidence.get(key), str) or not evidence[key].strip():
            issues.append(f"{key}:required_nonempty")
    for key, allowed in rules.get("allowed_values", {}).items():
        if evidence.get(key) not in allowed:
            issues.append(f"{key}:allowed_values")
    return issues


def execute_contract(
    proposal_id: str,
    contract_path: Path,
    mutation_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    contract = load_json(contract_path)
    mutations = load_json(mutation_path)
    if contract.get("proposal_id") != proposal_id:
        raise ValueError("contract proposal mismatch")
    if mutations.get("proposal_id") != proposal_id:
        raise ValueError("mutation proposal mismatch")
    rules = contract["rules"]
    valid_issues = validate_evidence(rules, contract["evidence"])
    mutation_results = []
    for mutation in mutations["mutations"]:
        issues = validate_evidence(rules, mutation["evidence"])
        rejected = bool(issues)
        mutation_results.append(
            {
                "mutation_id": mutation["mutation_id"],
                "rejected": rejected,
                "issues": issues,
                "expected": "reject",
                "passed": rejected,
            }
        )
    observed = contract["observed_disposition"]
    allowed = {"completed", "represented", "open_gap", "exact_gate"}
    if observed not in allowed:
        valid_issues.append("observed_disposition:not_allowed")
    receipt = {
        "schema": "ghc.family.v648-v4.runner-witness.v1",
        "proposal_id": proposal_id,
        "observed_disposition": observed,
        "valid_contract_passed": not valid_issues,
        "valid_contract_issues": valid_issues,
        "mutation_count": len(mutation_results),
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_results),
        "all_mutations_rejected": all(row["rejected"] for row in mutation_results),
        "mutation_results": mutation_results,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": contract["boundary"],
    }
    receipt["passed"] = (
        receipt["valid_contract_passed"]
        and receipt["all_mutations_rejected"]
        and receipt["mutation_count"] == 7
    )
    write_json(output_path, receipt)
    if not receipt["passed"]:
        raise ValueError(f"bounded contract failed for {proposal_id}")
    return receipt


def runner_main(proposal_id: str, phase: Path) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    slug = proposal_id.casefold().replace("-", "_")
    contract_map = load_json(phase / "tooling/runner-contract-map.json")
    row = contract_map[proposal_id]
    execute_contract(
        proposal_id,
        phase / row["contract"],
        phase / row["mutations"],
        Path(args.output),
    )


__all__ = ["execute_contract", "load_json", "runner_main", "validate_evidence"]
