#!/usr/bin/env python3
"""Bounded synthetic contract core for Tamar Vey v685-v1.

The module validates software records only.  It never inspects or acts on a
real broom, brush, material, tool, person, workplace, identity, or authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from typing import Any


REQUIRED_FIELDS = {
    "record_id",
    "proposal_id",
    "facet",
    "role",
    "precondition_digest",
    "correction_sequence",
    "authority_status",
    "source_status",
    "synthetic",
    "observed",
}
ALLOWED_ROLES = {"synthetic_maker", "synthetic_reviewer", "synthetic_custodian"}
MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def expected_precondition_digest(proposal_id: str) -> str:
    return hashlib.sha256(f"{proposal_id}|tamar-v685-v1|synthetic-only".encode("utf-8")).hexdigest()


def make_positive_record(proposal_id: str, facet: str) -> dict[str, Any]:
    return {
        "record_id": f"{proposal_id}-POS",
        "proposal_id": proposal_id,
        "facet": facet,
        "role": "synthetic_maker",
        "precondition_digest": expected_precondition_digest(proposal_id),
        "correction_sequence": [1, 2],
        "authority_status": "reserved",
        "source_status": "vocabulary_or_owner_local_contract_only",
        "synthetic": True,
        "observed": False,
    }


def validate_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        errors.append("missing_required_field:" + ",".join(missing))
    proposal_id = record.get("proposal_id")
    if not isinstance(proposal_id, str) or not proposal_id.startswith("TV6851-N"):
        errors.append("invalid_proposal_id")
    role = record.get("role")
    if role not in ALLOWED_ROLES:
        errors.append("identifier_role_swap")
    if isinstance(proposal_id, str) and record.get("precondition_digest") != expected_precondition_digest(proposal_id):
        errors.append("stale_precondition_digest")
    sequence = record.get("correction_sequence")
    if not isinstance(sequence, list) or sequence != sorted(sequence) or len(sequence) != len(set(sequence)):
        errors.append("correction_order_inversion")
    if record.get("authority_status") != "reserved":
        errors.append("authority_promotion")
    if record.get("synthetic") is not True:
        errors.append("non_synthetic_record")
    if record.get("observed") is not False:
        errors.append("observation_promotion")
    return not errors, errors


def mutate_record(record: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    mutated = deepcopy(record)
    if mutation_type == "missing_required_field":
        mutated.pop("source_status", None)
    elif mutation_type == "identifier_role_swap":
        mutated["role"] = "real_world_authority"
    elif mutation_type == "stale_precondition_digest":
        mutated["precondition_digest"] = "0" * 64
    elif mutation_type == "correction_order_inversion":
        mutated["correction_sequence"] = [2, 1]
    elif mutation_type == "authority_promotion":
        mutated["authority_status"] = "granted"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    mutated["mutation_type"] = mutation_type
    return mutated


RUNNER_FACETS = {
    "contract": "required-field and synthetic-only contract",
    "mutation": "rejecting-mutation firewall",
    "privacy": "minimum-disclosure and candidate adjudication",
    "manifest": "normalized Git-blob domain",
    "source": "vocabulary-only source status",
    "accessibility": "structural accessibility without completeness",
    "correction": "append-only correction order",
    "gate": "authority noncompensation",
    "method_flow": "retained failure and recovery pairing",
    "terminal": "terminal nonpromotion and route hold",
}


def runner_smoke(runner: str, fixture: str) -> dict[str, Any]:
    if runner not in RUNNER_FACETS:
        raise ValueError(f"unknown runner: {runner}")
    record = make_positive_record("TV6851-N001", RUNNER_FACETS[runner])
    expected_acceptance = fixture == "positive"
    if fixture == "invalid":
        mutation_type = MUTATION_TYPES[list(RUNNER_FACETS).index(runner) % len(MUTATION_TYPES)]
        record = mutate_record(record, mutation_type)
    elif fixture != "positive":
        raise ValueError(f"unknown fixture: {fixture}")
    accepted, errors = validate_record(record)
    return {
        "schema": "ghc.family.broommaking.runner-smoke.v685.v1",
        "runner": runner,
        "fixture": fixture,
        "expected_acceptance": expected_acceptance,
        "accepted": accepted,
        "errors": errors,
        "smoke_pass": accepted is expected_acceptance,
        "real_rows": 0,
        "authority_credit": "zero",
    }


def runner_main(runner: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=["positive", "invalid"], required=True)
    args = parser.parse_args()
    result = runner_smoke(runner, args.fixture)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["smoke_pass"] else 1


__all__ = [
    "MUTATION_TYPES",
    "RUNNER_FACETS",
    "canonical_bytes",
    "digest",
    "expected_precondition_digest",
    "make_positive_record",
    "mutate_record",
    "runner_main",
    "runner_smoke",
    "validate_record",
]
