#!/usr/bin/env python3
"""Bounded contract runner shared by Sable Rook v664-v7 family wrappers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def strict_json(path: Path) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError("contract root must be an object")
    return value


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def validate_contract(contract: dict[str, Any], expected_profile: str) -> dict[str, Any]:
    issues: list[str] = []
    if contract.get("profile") != expected_profile:
        issues.append("profile mismatch")
    if contract.get("zero_row") is not True:
        issues.append("zero_row must be true")
    if contract.get("real_rows") != 0:
        issues.append("real_rows must be zero")
    if contract.get("claims") != []:
        issues.append("claims must remain empty")
    fixture = contract.get("positive_fixture")
    if not isinstance(fixture, dict):
        issues.append("positive_fixture must be an object")
        fixture = {}
    required = contract.get("required_positive_fields")
    if not isinstance(required, list) or not required:
        issues.append("required_positive_fields must be nonempty")
        required = []
    missing = [field for field in required if field not in fixture]
    if missing:
        issues.append(f"positive fixture missing fields: {missing}")
    mutations = contract.get("mutation_results")
    if not isinstance(mutations, list) or len(mutations) != 5:
        issues.append("exactly five mutation results required")
        mutations = []
    accepted = [row.get("mutation_id") for row in mutations if row.get("accepted") is not False]
    if accepted:
        issues.append(f"mutations not rejected: {accepted}")
    labels = {"completed", "represented", "open_gap", "exact_gate"}
    if contract.get("disposition") not in labels:
        issues.append("disposition outside the four-label vocabulary")
    if contract.get("protected_gate_promotions") != 0:
        issues.append("protected gate promotion detected")
    valid = not issues
    return {
        "schema": "ghc.family.sable.v664-v7.runner-receipt.v1",
        "profile": expected_profile,
        "proposal_id": contract.get("proposal_id"),
        "valid": valid,
        "issues": issues,
        "positive_fixture_required_fields": len(required),
        "positive_fixture_missing_fields": missing,
        "rejecting_mutation_count": len(mutations),
        "accepted_mutation_count": len(accepted),
        "protected_gate_promotions": contract.get("protected_gate_promotions"),
        "evidence_ceiling": "bounded owner-local synthetic structural symbolic zero-row or software evidence only",
        "not_claimed": ["real carrier", "measurement", "professional review", "production", "legal or cultural authority", "Maori authority", "complete privacy", "complete accessibility", "exhaustive security", "independent reproduction", "Stage 20"],
    }


def cli(expected_profile: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract = strict_json(args.contract)
    receipt = validate_contract(contract, expected_profile)
    receipt["contract_sha256"] = hashlib.sha256(args.contract.read_bytes()).hexdigest()
    raw = canonical(receipt)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(raw.decode("utf-8").strip())
    return 0 if receipt["valid"] else 1
