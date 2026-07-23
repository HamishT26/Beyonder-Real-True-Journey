#!/usr/bin/env python3
"""Minimal fail-closed validator for Vesper Arlen v653-v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ghc_family_v653_v1_validation_common import PHASE, read_json, write_json


def validate() -> dict[str, Any]:
    truth = read_json(PHASE / "phase-truth.json")
    proposals = read_json(PHASE / "x2-proposal-ledger.json")
    final_negative_path = PHASE / "retained-negative-register-final.json"
    negatives = read_json(final_negative_path if final_negative_path.is_file() else PHASE / "retained-negative-register-x2.json")
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    final_method_path = PHASE / "method-flow/final-method-flow-ledger.json"
    methods = read_json(final_method_path if final_method_path.is_file() else PHASE / "method-flow/evidence-method-flow-ledger.json")
    skills = read_json(PHASE / "skills/skill-build-receipt.json")
    runners = read_json(PHASE / "runners/runner-invocation-receipt.json")
    portfolio = read_json(PHASE / "portfolios/execution-receipt.json")
    checklist = read_json(PHASE / "complete-incomplete-checklist.json")
    checks = {
        "thirty_proposals": proposals["proposal_count"] == 30,
        "four_truth_labels": set(proposals["allowed_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "distribution": proposals["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "negatives_preserved": truth["effective_negatives"] == negatives["effective_total"] and negatives["none_erased"],
        "mutations_preserved": read_json(PHASE / "retained-negative-register-x2.json")["synthetic_mutation_count"] == 150,
        "open_gaps": gates["effective_open_gaps"] == 70,
        "exact_gates": gates["effective_exact_gates"] == 71,
        "gates_not_closed": gates["none_silently_closed"],
        "method_failures": methods["counts"]["witness_results"]["fail"] == methods["counts"]["methods"],
        "method_passes": methods["counts"]["witness_results"]["pass"] == methods["counts"]["methods"],
        "skills": skills["quick_validated_count"] == 10,
        "skills_local": not skills["globally_installed"],
        "runners": runners["valid_count"] == 10,
        "safe_tasks": portfolio["safe_now"]["resolved"] == portfolio["safe_now"]["planned"],
        "candidate_tasks": portfolio["candidate"]["resolved"] == portfolio["candidate"]["planned"],
        "internal_tasks_closed": portfolio["unresolved_authorized_internal_tasks"] == 0,
        "real_data_zero": truth["real_data_rows"] == 0,
        "independent_reproduction_false": not truth["independent_reproduction"],
        "route_gated": truth["route_state"] in {"NOT_ELIGIBLE_BEFORE_FINAL_GATE", "OPEN_ROUTE_GAP"},
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "external_work_incomplete": len(checklist["incomplete_external"]) >= 5,
        "lifecycle_pending": len(checklist["pending_lifecycle"]) == 4,
    }
    return {
        "schema": "ghc.family.v653-v1.minimal-validation.v1",
        "check_count": len(checks),
        "passed_count": sum(checks.values()),
        "checks": checks,
        "valid": all(checks.values()),
        "boundary": "Fail-closed phase-truth summary; no external gate is promoted.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate()
    if args.receipt:
        write_json(args.receipt, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
