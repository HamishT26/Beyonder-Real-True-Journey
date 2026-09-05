#!/usr/bin/env python3
"""Bounded synthetic contract core for Eiren Kestrel v685-v5."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from typing import Any


REQUIRED_FIELDS = {
    "proposal_id", "facet", "practice_key", "source_status", "role",
    "precondition_digest", "corrections", "authority_claim", "real_rows",
}
ALLOWED_ROLES = {"synthetic_analyst", "synthetic_curator", "synthetic_steward"}
MUTATION_TYPES = [
    "missing_required_field", "identifier_role_swap", "stale_precondition_digest",
    "correction_order_inversion", "authority_promotion",
]

RUNNER_FACETS = {
    "contract": "schema and nonconversion contract",
    "mutation": "five-mutation rejection tribunal",
    "provenance": "activity entity and source lineage",
    "units": "dimensional and time-coordinate reservation",
    "graph": "acyclic route and provenance graph",
    "privacy": "five-class private-material boundary",
    "accessibility": "structural accessible-status representation",
    "toolchain": "D-first integrity and rollback transaction",
    "route": "thirty-seat phase arithmetic projection",
    "terminal": "exact-final canonical and one-create latch",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def expected_precondition_digest(proposal_id: str) -> str:
    return hashlib.sha256(f"eiren-v685-v5:{proposal_id}:planning-only-x1".encode()).hexdigest()


def make_positive_record(proposal_id: str, facet: str, practice_key: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.astronomy.synthetic-contract.v685.v5",
        "proposal_id": proposal_id,
        "facet": facet,
        "practice_key": practice_key,
        "source_status": "public_vocabulary_only_zero_network_rows",
        "role": "synthetic_steward",
        "precondition_digest": expected_precondition_digest(proposal_id),
        "corrections": [
            {"sequence": 1, "state": "declared"},
            {"sequence": 2, "state": "reviewable"},
        ],
        "authority_claim": "none",
        "real_rows": 0,
    }


def validate_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    for field in sorted(REQUIRED_FIELDS - set(record)):
        errors.append(f"missing_required_field:{field}")
    if errors:
        return False, errors
    if record["role"] not in ALLOWED_ROLES:
        errors.append("invalid_role")
    if not str(record["proposal_id"]).startswith("EK6855-N"):
        errors.append("identifier_role_mismatch")
    if record["precondition_digest"] != expected_precondition_digest(record["proposal_id"]):
        errors.append("stale_precondition_digest")
    sequences = [item.get("sequence") for item in record["corrections"] if isinstance(item, dict)]
    if sequences != sorted(sequences) or sequences != [1, 2]:
        errors.append("correction_order_inversion")
    if record["authority_claim"] != "none":
        errors.append("authority_promotion")
    if record["real_rows"] != 0:
        errors.append("real_row_nonzero")
    return not errors, errors


def mutate_record(record: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    value = copy.deepcopy(record)
    if mutation_type == "missing_required_field":
        value.pop("source_status", None)
    elif mutation_type == "identifier_role_swap":
        value["role"] = value["proposal_id"]
    elif mutation_type == "stale_precondition_digest":
        value["precondition_digest"] = "0" * 64
    elif mutation_type == "correction_order_inversion":
        value["corrections"] = list(reversed(value["corrections"]))
    elif mutation_type == "authority_promotion":
        value["authority_claim"] = "real_scientific_or_professional_authority"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    return value


def runner_smoke(runner: str, fixture: str) -> dict[str, Any]:
    if runner not in RUNNER_FACETS:
        return {"accepted": False, "errors": ["unknown_runner"], "smoke_pass": False}
    positive = make_positive_record("EK6855-N001", RUNNER_FACETS[runner], "transient_alert")
    record = positive if fixture == "positive" else mutate_record(positive, "missing_required_field")
    accepted, errors = validate_record(record)
    expected = fixture == "positive"
    return {
        "schema": "ghc.family.astronomy.runner-smoke.v685.v5",
        "runner": runner,
        "fixture": fixture,
        "expected_acceptance": expected,
        "accepted": accepted,
        "errors": errors,
        "real_rows": 0,
        "authority_credit": "zero",
        "smoke_pass": accepted == expected,
    }


def runner_main(runner: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=["positive", "invalid"], required=True)
    args = parser.parse_args()
    result = runner_smoke(runner, args.fixture)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["smoke_pass"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", choices=sorted(RUNNER_FACETS), required=True)
    parser.add_argument("--fixture", choices=["positive", "invalid"], required=True)
    args = parser.parse_args()
    result = runner_smoke(args.runner, args.fixture)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    raise SystemExit(0 if result["smoke_pass"] else 1)
