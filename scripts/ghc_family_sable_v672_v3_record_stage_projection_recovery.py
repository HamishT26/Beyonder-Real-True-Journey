#!/usr/bin/env python3
"""Retain the evidence-stage wrapper projection failure and recovery."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "docs" / "sable-rook" / "v672-v3" / "x2"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    flow_path = X2 / "method-flow" / "ledger.json"
    flow = load(flow_path)
    method_id = "SR6723-RECOVERY-METHOD-003"
    if any(row.get("method_id") == method_id for row in flow["methods"]):
        raise SystemExit("stage projection recovery already recorded")
    flow["methods"].append(
        {
            "method_id": method_id,
            "trigger": "evidence-stage wrapper crossed its projection and the outer projection omitted the live session handle",
            "preferred_method": "inspect the exact child process, index lock, receipts, staged count, and diffs before waiting on the original process",
            "state": "preferred_after_bounded_passing_witness",
            "rollback": "never replay while the original child is live; retain the wrapper fault",
            "sibling_recommendation": "always preserve yielded session metadata or use bounded scalar postflight",
        }
    )
    flow["witnesses"].extend(
        [
            {
                "witness_id": "SR6723-X2-003-FAIL",
                "method_id": method_id,
                "kind": "failed",
                "credit": 0,
                "description": "outer projection discarded the stage-review session handle after the 30-second envelope",
                "state": "retained_zero_credit",
            },
            {
                "witness_id": "SR6723-X2-003-PASS",
                "method_id": method_id,
                "kind": "passing",
                "credit": "bounded_process_recovery_only",
                "description": "the original process was waited to quiescence and exact staged receipts passed without replay",
                "state": "bounded_passing_not_original_wrapper_success",
            },
        ]
    )
    flow["current_delta"] = {
        "effective_negatives": 59,
        "failed_witnesses": 59,
        "methods": 39,
        "passing_witnesses": 39,
    }
    flow["effective_counts"].update(
        {
            "effective_negatives": 35327,
            "effective_methods": 21938,
            "effective_failed_witnesses": 7148,
            "effective_passing_witnesses": 9225,
        }
    )
    write(flow_path, flow)

    negatives_path = X2 / "retained-negative-register.json"
    negatives = load(negatives_path)
    negatives["x2_unexpected_operational_failures"] = 3
    negatives["x2_operational_failure_ids"] = ["SR6723-X2-001", "SR6723-X2-002", "SR6723-X2-003"]
    negatives["effective_total"] = 35327
    write(negatives_path, negatives)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["effective_counts"].update(
        {
            "negatives": 35327,
            "methods": 21938,
            "failed_witnesses": 7148,
            "passing_witnesses": 9225,
        }
    )
    truth["staged_review_projection"] = {
        "failure_id": "SR6723-X2-003",
        "failed_wrapper_credit": 0,
        "review_replayed": False,
        "original_process_completed": True,
        "exact_staged_review_valid": True,
    }
    write(truth_path, truth)

    recovery_path = X2 / "evidence-selection-recovery.json"
    recovery = load(recovery_path)
    recovery["failures"].append(
        {
            "failure_id": "SR6723-X2-003",
            "failure": "stage wrapper projection omitted the yielded session handle",
            "recovery": "waited original child after exact process and index inspection; no stage-review replay",
        }
    )
    recovery["stage_review_replayed"] = False
    write(recovery_path, recovery)


if __name__ == "__main__":
    main()
