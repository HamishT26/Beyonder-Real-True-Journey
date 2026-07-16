#!/usr/bin/env python3
"""Validate the bounded Tamar v646-v5 safe, candidate, and cleanup portfolios."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def evaluate() -> dict:
    safe = load("approval-packets/x2-safe-now-execution.json")
    candidate = load("prototypes/x2-candidate-execution.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    checks = {
        "safe_30": safe["count"] == len(safe["tasks"]) == 30,
        "candidate_20": candidate["count"] == len(candidate["tasks"]) == 20,
        "cleanup_30": cleanup["count"] == len(cleanup["tasks"]) == 30,
        "all_acceptance_gates_pass": all(row["acceptance_gate_passed"] for row in safe["tasks"] + candidate["tasks"] + cleanup["tasks"]),
        "all_owner_scoped": all(row["owner_scoped"] for row in safe["tasks"] + candidate["tasks"] + cleanup["tasks"]),
        "no_protected_gate_execution": all(not row["protected_gate_executed"] for row in safe["tasks"] + candidate["tasks"] + cleanup["tasks"]),
        "no_inherited_packet_execution": safe["inherited_exact_packets_executed"] == safe["inherited_blocked_packets_executed"] == 0,
    }
    return {
        "schema": "ghc.family.v646-v5.portfolio-runner.v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "check_count": len(checks),
        "valid": all(checks.values()),
        "boundary": "Portfolio completion applies only to declared owner-scoped structural or synthetic gates; it grants no authority, empirical, production, or independent-reproduction credit.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"checks": result["check_count"], "passed": result["passed"], "valid": result["valid"]}))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
