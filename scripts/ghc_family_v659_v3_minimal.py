#!/usr/bin/env python3
"""Minimal exact-truth validator for Sable Rook v659-v3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v659_v3_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "04d167b799ba8b9de885e66ff8ee480bf5b219b2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_minimal() -> dict:
    truth = load("final/final-truth.json")
    route = load("route/prepared-route.json")
    privacy = load("validation/closeout-privacy-scan.json")
    owner = load("final/final-owner-manifest.json")
    checks = {
        "owner": truth["owner"] == "Sable Rook",
        "phase": truth["phase"] == "v659-v3",
        "source": truth["source_final"] == d.SOURCE_FINAL,
        "x1": truth["x1_freeze"] == d.X1_FREEZE,
        "evidence": truth["x2_evidence"] == EVIDENCE_COMMIT,
        "frozen": truth["effective_frozen"] == 2970,
        "negatives": truth["effective_negatives"] == 18778,
        "methods": truth["effective_methods"] == 5052,
        "gaps": truth["effective_open_gaps"] == 124,
        "gates": truth["effective_exact_gates"] == 123,
        "not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": route["next_exact_title"] == "Caelen Ash" and route["next_phase"] == "v659-v4",
        "recipient_next_reserved": route["recipient_next_exact_title"] == "live_reverification_required_by_caelen" and route["recipient_next_phase"] == "live_reverification_required_by_caelen",
        "unsent": not route["message_sent"] and route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        "privacy_and_manifest": privacy["confirmed_hit_count"] == 0 and owner["below_threshold"],
    }
    return {
        "schema": "ghc.family.v659-v3.minimal-validation.v1", "checks": checks,
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
