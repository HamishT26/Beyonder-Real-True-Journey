#!/usr/bin/env python3
"""Run the bounded Sylven v647-v4 x1-only structural review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v647-v4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    proposals = load("x1-proposals.json")
    collision = load("provenance/proposal-collision-audit.json")
    portfolio = load("approval-packets/x1-approval-portfolio.json")
    plan = load("prototypes/x1-skill-runner-plan.json")
    cleanup = load("maintenance/x1-clean-refine-plan.json")
    mutations = load("validation/x1-synthetic-mutation-plan.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    method = load("method-flow/method-flow-state.json")
    checks = {
        "ten_proposals": len(proposals["proposals"]) == 10,
        "frozen_510": proposals["frozen_chain_count_after_x1"] == 510,
        "distribution": proposals["expected_distribution"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expected_not_results": proposals["expected_counts_are_results"] is False,
        "no_x2": proposals["x2_execution_present"] is False,
        "novelty": collision["valid"] and collision["passed"] == 10,
        "safe_30": portfolio["safe_now_count"] == 30,
        "candidate_20": portfolio["candidate_count"] == 20,
        "skills_20": plan["skill_count"] == 20,
        "runners_10": plan["runner_count"] == 10,
        "cleanup_30": cleanup["count"] == 30,
        "mutations_70_unexecuted": mutations["count"] == 70 and mutations["executed"] == 0,
        "negatives_3418": negatives["effective_total"] == 3418 and negatives["no_negative_erased"],
        "gates_inherited": gates["current_effective_open_gaps"] == 20 and gates["current_effective_exact_gates"] == 21,
        "method_flow": method["counts"]["witness_results"] == {"fail": 1, "pass": 1},
    }
    payload = {
        "schema": "ghc.family.v647-v4.x1-review.v1", "checks": checks, "check_count": len(checks),
        "passed": sum(checks.values()), "valid": all(checks.values()),
        "x2_execution_present": False, "completion_credit": False,
        "boundary": "X1 review only; no x2, empirical, production, authority, independent-reproduction, or Stage 20 credit.",
    }
    if args.write:
        path = PHASE / "validation/x1-review.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": payload["passed"], "checks": payload["check_count"], "valid": payload["valid"]}, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
