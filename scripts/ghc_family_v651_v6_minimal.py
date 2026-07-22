#!/usr/bin/env python3
"""Minimal fail-closed verifier for Elaren v651-v6."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/elaren-kestrel/v651-v6"


def read(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def verify() -> dict:
    proposals = read("preregistration/proposals.json")
    outcomes = read("outcomes/core-outcomes.json")
    negatives = read("truth/retained-negative-register-x2.json")
    gates = read("gates/exact-open-gate-register.json")
    portfolio = read("portfolios/x2-portfolio-outcomes.json")
    skills = read("tooling/skill-build-receipt.json")
    runners = read("tooling/runner-use-receipt.json")
    truth = read("truth/evidence-phase-truth.json")
    conditions = [
        len(proposals["proposals"]) == 30,
        outcomes["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        set(outcomes["allowed_labels"]) == {"completed", "represented", "open_gap", "exact_gate"},
        read("validation/mutation-execution-receipt.json")["rejected"] == 100,
        negatives["effective_total"] == 7325,
        negatives["failures_erased"] == 0,
        gates["effective_open_gaps"] == 57,
        gates["effective_exact_gates"] == 58,
        gates["silently_closed"] == 0,
        portfolio["all_authorized_planned_items_resolved"],
        portfolio["counts"]["safe_now_completed"] == 40,
        portfolio["counts"]["candidate_resolved"] == 30,
        portfolio["counts"]["clean_fix_refine_completed"] == 40,
        skills["quick_validated"] == skills["smoke_used"] == 20,
        runners["invoked_count"] == 10,
        truth["real_data_rows"] == truth["participants"] == truth["real_keys_or_proofs"] == 0,
        truth["authority_decisions"] == truth["production_actions"] == 0,
        truth["same_owner_only"] and not truth["independent_reproduction"],
        truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        not read("approvals/held-packets.json")["new_exact_gate"]["executed"],
    ]
    return {"schema": "ghc.family.v651-v6.minimal-validation.v1", "check_count": len(conditions), "passed": sum(conditions), "issues": [index + 1 for index, value in enumerate(conditions) if not value], "valid": all(conditions), "same_owner_only": True, "independent_reproduction": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = verify()
    if args.output:
        target = REPO / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": result["valid"], "checks": f"{result['passed']}/{result['check_count']}"}))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
