#!/usr/bin/env python3
"""Minimal exact-truth validator for Elowen Cairn v659-v8."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v659_v8_x2_data as d
from build_ghc_family_v659_v8_closeout import FINAL_FAILURES


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "38c529d2aaa6387830d06102ab19ed9735d5f0af"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_minimal() -> dict:
    truth = load("final/final-truth.json")
    route = load("route/prepared-route.json")
    privacy = load("validation/closeout-privacy-scan.json")
    owner = load("final/final-owner-manifest.json")
    closeout_failure_count = len(FINAL_FAILURES)
    expected_negatives = d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 200 + closeout_failure_count
    expected_methods = d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 200 + closeout_failure_count
    checks = {
        "owner": truth["owner"] == "Elowen Cairn",
        "phase": truth["phase"] == "v659-v8",
        "source": truth["source_final"] == d.SOURCE_FINAL,
        "x1": truth["x1_freeze"] == d.X1_FREEZE,
        "evidence": truth["x2_evidence"] == EVIDENCE_COMMIT,
        "frozen": truth["effective_frozen"] == d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
        "negatives": truth["effective_negatives"] == expected_negatives,
        "methods": truth["effective_methods"] == expected_methods,
        "gaps": truth["effective_open_gaps"] == d.SOURCE_OPEN_GAPS + d.EXPECTED_DISTRIBUTION["open_gap"],
        "gates": truth["effective_exact_gates"] == d.SOURCE_EXACT_GATES + d.EXPECTED_DISTRIBUTION["exact_gate"],
        "not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_unresolved": route["next_exact_title"] is None and route["next_phase"] is None and not route["later_endpoint_inferred"],
        "recipient_route_unresolved": route["recipient_next_exact_title"] is None and route["recipient_next_phase"] is None,
        "unsent": not route["message_sent"] and route["state"] == "HELD_FOR_NEWEST_LIVE_ROUTE_REREAD_AFTER_EXACT_TERMINAL_GATE",
        "privacy_and_manifest": privacy["confirmed_hit_count"] == 0 and owner["below_threshold"],
    }
    return {
        "schema": "ghc.family.v659-v8.minimal-validation.v1", "checks": checks,
        "check_count": len(checks), "passed_count": sum(checks.values()),
        "failed_count": len(checks) - sum(checks.values()), "valid": all(checks.values()),
        "boundary": "Minimal same-owner truth checks only; not independent reproduction or broader assurance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = validate_minimal()
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "checks": receipt["check_count"], "passed": receipt["passed_count"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
