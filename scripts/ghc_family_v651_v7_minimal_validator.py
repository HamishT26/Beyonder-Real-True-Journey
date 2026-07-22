#!/usr/bin/env python3
"""Minimal fail-closed phase validator for Vesper v651-v7."""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate() -> dict:
    truth = load("truth/evidence-phase-truth.json")
    outcome = load("outcomes/core-outcomes.json")
    negative = load("truth/retained-negative-register-x2.json")
    gate = load("gates/exact-open-gate-register.json")
    values = [
        ("valid_truth", truth["valid"]),
        ("proposal_count", outcome["proposal_count"] == 30),
        ("four_labels", set(outcome["outcome_counts"]) == {"completed", "represented", "open_gap", "exact_gate"}),
        ("negative_total", negative["effective_total"] == 7452),
        ("no_erasure", negative["failures_erased"] == 0),
        ("open_gaps", gate["effective_open_gaps"] == 59),
        ("exact_gates", gate["effective_exact_gates"] == 60),
        ("zero_rows", truth["real_data_rows"] == 0),
        ("zero_participants", truth["participants"] == 0),
        ("zero_keys", truth["real_keys_or_tokens"] == 0),
        ("zero_authority", truth["authority_decisions"] == 0),
        ("zero_production", truth["production_actions"] == 0),
        ("no_independent_reproduction", truth["independent_reproduction"] is False),
        ("not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
    ]
    return {"schema": "ghc.family.v651-v7.minimal-validation.v1", "check_count": len(values), "passed_count": sum(passed for _, passed in values), "checks": [{"name": name, "passed": passed} for name, passed in values], "valid": all(passed for _, passed in values)}


def main() -> None:
    print(json.dumps(validate(), sort_keys=True))


if __name__ == "__main__":
    main()
