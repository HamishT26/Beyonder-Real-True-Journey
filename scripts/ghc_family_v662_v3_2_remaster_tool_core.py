#!/usr/bin/env python3
"""Reusable bounded contract tribunal for Neris v662-v3-2 remaster tools."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import ghc_family_v662_v3_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FALSE = (
    "empirical_confirmation",
    "participant_evidence",
    "professional_validation",
    "production_certification",
    "legal_or_cultural_ratification",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi_evidence",
    "consciousness_or_personhood_evidence",
    "theory_of_everything_proof",
    "stage20_authority",
)


def canonical_json(value: Any) -> bytes:
    """Return a deterministic bounded JSON encoding; this is not a signature."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def contract_errors(contract: dict[str, Any]) -> list[str]:
    """Evaluate only the frozen structural cut-set used by this phase."""

    errors: list[str] = []
    if contract.get("synthetic_or_structural_only") is not True:
        errors.append("synthetic_or_structural_only_required")
    if contract.get("real_world_rows") != 0:
        errors.append("real_world_rows_must_be_zero")
    if contract.get("external_actions") != 0:
        errors.append("external_actions_must_be_zero")
    if contract.get("network_calls") != 0:
        errors.append("network_calls_must_be_zero")
    if contract.get("protected_gates") != d.PROTECTED_GATES:
        errors.append("protected_gate_set_mismatch")
    claims = contract.get("claims", {})
    for key in REQUIRED_FALSE:
        if claims.get(key) is not False:
            errors.append(f"claim_must_remain_false:{key}")
    if contract.get("terminal_verdict") != d.TERMINAL_VERDICT:
        errors.append("terminal_verdict_mismatch")
    if contract.get("allowed_outcomes") != d.ALLOWED_OUTCOMES:
        errors.append("allowed_outcome_vocabulary_mismatch")
    if contract.get("expected_outcome") not in d.ALLOWED_OUTCOMES:
        errors.append("expected_outcome_not_allowed")
    if not contract.get("source_ids"):
        errors.append("source_vocabulary_anchor_required")
    return errors


def mutation_cases(contract: dict[str, Any], proposal_id: str) -> list[dict[str, Any]]:
    """Apply five preregistered negative mutations and retain their rejection reasons."""

    cases = [
        ("remove_protected_gate", lambda row: row.update(protected_gates=row["protected_gates"][:-1])),
        ("insert_real_world_row", lambda row: row.update(real_world_rows=1)),
        ("claim_independent_reproduction", lambda row: row["claims"].update(independent_reproduction=True)),
        ("promote_stage20", lambda row: row.update(terminal_verdict="READY_FOR_STAGE_20")),
        ("authorize_external_action", lambda row: row.update(external_actions=1)),
    ]
    results: list[dict[str, Any]] = []
    for index, (name, mutate) in enumerate(cases, 1):
        candidate = json.loads(json.dumps(contract, ensure_ascii=False))
        mutate(candidate)
        errors = contract_errors(candidate)
        results.append(
            {
                "mutation_id": f"{proposal_id}-M{index:02d}",
                "mutation": name,
                "accepted": not errors,
                "rejected": bool(errors),
                "errors": errors,
                "completion_credit": 0,
                "candidate_sha256": digest(candidate),
                "boundary": "Synthetic or structural rejection witness only; not real-world failure evidence.",
            }
        )
    return results


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    errors = contract_errors(contract)
    mutations = mutation_cases(contract, str(contract.get("proposal_id", "UNKNOWN")))
    all_rejected = len(mutations) == 5 and all(row["rejected"] for row in mutations)
    expected = contract.get("expected_outcome")
    observed = expected if not errors and all_rejected else "open_gap"
    return {
        "contract_sha256": digest(contract),
        "valid_fixture": not errors,
        "fixture_errors": errors,
        "mutations": mutations,
        "mutations_rejected": sum(row["rejected"] for row in mutations),
        "all_mutations_rejected": all_rejected,
        "expected_outcome": expected,
        "observed_outcome": observed,
        "external_actions": 0,
        "network_calls": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": d.TERMINAL_VERDICT,
    }


def run_action(action: str, contract_path: Path, mutation_path: Path | None = None) -> dict[str, Any]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    result = evaluate(contract)
    if mutation_path is not None:
        frozen = json.loads(mutation_path.read_text(encoding="utf-8"))
        frozen_rows = frozen.get("mutations", frozen)
        result["frozen_mutation_set_equal"] = frozen_rows == result["mutations"]
    else:
        result["frozen_mutation_set_equal"] = None
    return {
        "schema": "ghc.family.v662-v3-2-remaster.runner-smoke.v1",
        "action": action,
        "proposal_id": contract.get("proposal_id"),
        "slug": contract.get("slug"),
        **result,
        "bounded_action_claim": (
            "The named runner exercised one frozen structural contract and its five negative mutations; "
            "this is not proof of general runner correctness, production readiness, authority, or independent reproduction."
        ),
    }


def cli(action: str) -> None:
    parser = argparse.ArgumentParser(description=f"Bounded {action} contract tribunal")
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--mutations", type=Path)
    args = parser.parse_args()
    result = run_action(action, args.contract.resolve(), args.mutations.resolve() if args.mutations else None)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid_fixture"] or not result["all_mutations_rejected"]:
        raise SystemExit(1)


if __name__ == "__main__":
    cli("generic-remaster-tool")
