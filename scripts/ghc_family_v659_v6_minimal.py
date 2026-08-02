#!/usr/bin/env python3
"""Minimal exact-truth validator for Liora Venn v659-v6."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v659_v6_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "72f9a62167d6d946e8fea5a7337fe12691cf475f"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_minimal() -> dict:
    truth = load("final/final-truth.json")
    route = load("route/prepared-route.json")
    privacy = load("validation/closeout-privacy-scan.json")
    owner = load("final/final-owner-manifest.json")
    expected_negatives = d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 100
    expected_methods = d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 100
    checks = {
        "owner": truth["owner"] == "Liora Venn",
        "phase": truth["phase"] == "v659-v6",
        "source": truth["source_final"] == d.SOURCE_FINAL,
        "x1": truth["x1_freeze"] == d.X1_FREEZE,
        "evidence": truth["x2_evidence"] == EVIDENCE_COMMIT,
        "frozen": truth["effective_frozen"] == d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
        "negatives": truth["effective_negatives"] == expected_negatives,
        "methods": truth["effective_methods"] == expected_methods,
        "gaps": truth["effective_open_gaps"] == d.SOURCE_OPEN_GAPS + d.EXPECTED_DISTRIBUTION["open_gap"],
        "gates": truth["effective_exact_gates"] == d.SOURCE_EXACT_GATES + d.EXPECTED_DISTRIBUTION["exact_gate"],
        "not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": route["next_exact_title"] == "Tamar Vey" and route["next_phase"] == "v659-v7",
        "recipient_next_reserved": route["recipient_next_exact_title"] == "Elowen Cairn" and route["recipient_next_phase"] == "v659-v8",
        "unsent": not route["message_sent"] and route["state"] == "HELD_UNTIL_LIORA_EXACT_TERMINAL_GATE",
        "privacy_and_manifest": privacy["confirmed_hit_count"] == 0 and owner["below_threshold"],
    }
    return {
        "schema": "ghc.family.v659-v6.minimal-validation.v1", "checks": checks,
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
