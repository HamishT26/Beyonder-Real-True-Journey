#!/usr/bin/env python3
"""Minimal fail-closed validator for Sable Rook v653-v5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v653_v2_minimal_validator as base
from ghc_family_v653_v5_validation_common import PHASE, read_json, write_json


base.PHASE = PHASE
base.read_json = read_json
base.write_json = write_json


def validate():
    result = base.validate()
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    truth = read_json(PHASE / "phase-truth.json")
    checklist = read_json(PHASE / "complete-incomplete-checklist.json")
    result["checks"].update(
        {
            "open_gaps": gates["effective_open_gaps"] == 74,
            "exact_gates": gates["effective_exact_gates"] == 75,
            "route_gated": truth["route_state"]
            in {
                "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
                "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL",
                "NOT_ELIGIBLE_BEFORE_FINAL_GATE",
                "PREPARED_NOT_SENT",
            },
            "lifecycle_pending": len(checklist["pending_lifecycle"]) == 3,
        }
    )
    result["schema"] = "ghc.family.v653-v5.minimal-validation.v1"
    result["passed_count"] = sum(result["checks"].values())
    result["valid"] = all(result["checks"].values())
    return result


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
