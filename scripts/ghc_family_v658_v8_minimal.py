#!/usr/bin/env python3
"""Minimal fail-closed verifier for Lyren Moss v658-v8 evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_minimal() -> dict[str, Any]:
    checks = {
        "thirty_proposals": load("x2/proposal-ledger.json")["proposal_count"] == 30,
        "distribution": load("x2/proposal-ledger.json")["outcome_counts"] == d.EXPECTED_DISTRIBUTION,
        "mutations": load("x2/task-execution.json")["rejected_mutation_count"] == 150,
        "skills": load("tooling/skill-creator-receipts.json")["quick_validate_passed"] == 10,
        "runners": load("tooling/runner-receipts.json")["valid_count"] == 10,
        "safe_tasks": load("x2/task-execution.json")["counts"]["safe_now"] == 30,
        "candidate_tasks": load("x2/task-execution.json")["counts"]["candidate"] == 20,
        "cleanup_tasks": load("x2/task-execution.json")["counts"]["clean"] == 30,
        "privacy": load("validation/evidence-privacy-scan.json")["hit_count"] == 0,
        "manifest": load("validation/evidence-content-manifest.json")["entry_count"] > 0,
        "route_unsent": load("orchestration/route-state-x2.json")["message_sent"] is False,
        "route_open_gap": load("orchestration/route-state-x2.json")["state"] == "OPEN_ROUTE_GAP",
        "route_no_successor": load("orchestration/route-state-x2.json")["next_exact_title"] is None,
        "tavian_standby": load("orchestration/route-state-x2.json")["tavian_sol_state"] == "ON_STANDBY",
        "no_real_data": load("truth/phase-truth-x2.json")["real_data_used"] is False,
        "no_authority": load("truth/phase-truth-x2.json")["authority_action_executed"] is False,
        "not_ready": load("truth/phase-truth-x2.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    errors = sorted(name for name, passed in checks.items() if not passed)
    return {"valid": not errors, "check_count": len(checks), "checks": checks, "error_count": len(errors), "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json")
    args = parser.parse_args()
    result = validate_minimal()
    if args.json:
        path = ROOT / args.json
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": result["valid"], "checks": result["check_count"], "errors": result["error_count"]}))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
