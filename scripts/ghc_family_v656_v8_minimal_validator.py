#!/usr/bin/env python3
"""Minimal fail-closed validator for Vesper v656-v8."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v656_v8_phase_data as d
import ghc_family_v656_v8_x2_config as c


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate() -> dict:
    checks = []

    def add(label: str, condition: bool) -> None:
        checks.append({"label": label, "passed": bool(condition)})

    truth = load("truth/phase-truth-x2.json")
    negatives = load("truth/retained-negative-register-x2.json")
    flow = load("method-flow/method-flow-state-x2.json")
    route = load("orchestration/route-state-x1.json")
    readiness = load("validation/evidence-readiness.json")
    add("thirty proposals", truth["outcome_counts"] == c.EXPECTED_DISTRIBUTION)
    add("four exact truth labels", set(truth["outcome_counts"]) == d.ALLOWED_OUTCOMES)
    add("one hundred fifty mutations", negatives["mutation_count"] == 150)
    add("all negatives retained", negatives["all_retained"] is True)
    add("method failures retained", flow["all_failed_witnesses_retained"] is True)
    expected_methods = 150 + len(c.X2_OPERATIONAL_NEGATIVES)
    add("method parity", flow["counts"]["current_witness_results"] == {"fail": expected_methods, "pass": expected_methods})
    add("ten skills used", readiness["skill_smoke_receipt_count"] == 10)
    add("ten runners used", readiness["runner_receipt_count"] == 10)
    add("x1 unchanged", readiness["x1_frozen_paths_unchanged"] is True)
    add("no real data", truth["real_data_used"] is False)
    add("same-owner only", truth["independent_reproduction"] is False)
    add("route unsent", route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False)
    add("Lyren exact title", route["next_exact_title"] == "Lyren Moss")
    add("Tavian standby", route["tavian_sol_state"] == "ON_STANDBY")
    add("terminal verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    return {
        "schema": "ghc.family.v656-v8.minimal-validation.v1",
        "valid": all(row["passed"] for row in checks),
        "check_count": len(checks),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = validate()
    if args.output:
        path = ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
