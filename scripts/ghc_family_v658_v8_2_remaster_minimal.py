#!/usr/bin/env python3
"""Minimal exact-truth validator for the Lyren v658-v8 (2) remaster."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "e08a7bb24c9fc9c442374d251b985437a88ade11"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_minimal() -> dict[str, Any]:
    truth = load("final/final-truth.json")
    route = load("route/prepared-route.json")
    privacy = load("validation/closeout-privacy-scan.json")
    checks = {
        "owner": truth["owner"] == "Lyren Moss",
        "phase": truth["phase"] == "v658-v8-2-remaster",
        "x1": truth["x1_freeze"] == d.X1_FREEZE,
        "evidence": truth["x2_evidence"] == EVIDENCE_COMMIT,
        "frozen": truth["effective_frozen"] == 2910,
        "outcomes": truth["observed_outcomes"] == {"completed": 33, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "negatives": truth["effective_negatives"] == 18078,
        "methods": truth["effective_methods"] == 4352,
        "gaps_and_gates": truth["effective_open_gaps"] == 121 and truth["effective_exact_gates"] == 120,
        "verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_boundary": truth["same_owner_only"] and not truth["independent_reproduction"],
        "route_prepared": route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED" and not route["message_sent"],
        "route_exact": route["next_exact_title"] == "Ilyra Fen" and route["recipient_next_exact_title"] == "Auren Lark",
        "tavian_standby": route["tavian_sol_state"] == "ON_STANDBY",
        "privacy_boundary": privacy["hit_count"] == 0 and not privacy["privacy_complete"] and not privacy["security_complete"],
    }
    failed = [name for name, value in checks.items() if not value]
    return {
        "schema": "ghc.family.v658-v8-2-remaster.minimal-validation.v1",
        "phase": d.PHASE,
        "check_count": len(checks),
        "passed_count": len(checks) - len(failed),
        "failed": failed,
        "valid": not failed,
        "boundary": "Minimal exact-truth validation only; not independent reproduction or broader assurance.",
    }


if __name__ == "__main__":
    result = validate_minimal()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)
