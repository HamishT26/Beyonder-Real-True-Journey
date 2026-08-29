#!/usr/bin/env python3
"""Add the retained evidence-manifest wrapper timeout and persisted-state recovery."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
FAILED_ID = "CA6762-X2-N001"
PASS_ID = "CA6762-X2-P001"


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    branch = subprocess.check_output(["git", "-C", str(repo), "branch", "--show-current"], text=True).strip()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if branch != BRANCH or head != X1:
        raise SystemExit("operational overlay requires the x2 precommit lifecycle")
    base = repo / "docs" / "caelen-ash" / "v676-v2"
    ledger_path = base / "x2" / "method-flow" / "ledger.json"
    truth_path = base / "x2" / "phase-truth.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if any(row["method_id"] == FAILED_ID for row in ledger["methods"]):
        raise SystemExit("operational overlay already applied")
    ledger["methods"].extend(
        [
            {
                "method_id": FAILED_ID,
                "status": "failed_zero_credit",
                "truth": False,
                "description": "The evidence-manifest wrapper crossed its initial 30-second return window without an attributable result while the bounded process continued.",
                "recovered_by": PASS_ID,
                "state_change_at_failure_observation": "unknown_pending_read_only_audit",
            },
            {
                "method_id": PASS_ID,
                "status": "bounded_pass",
                "truth": True,
                "description": "Read-only process and index audit first observed the active process, then proved quiescence and the two staged manifest outputs without replaying the mutation.",
                "failed_witness_preserved": FAILED_ID,
                "replayed": False,
            },
        ]
    )
    ledger["new_x2_effective_methods"] = 432
    ledger["new_x2_negatives"] = 171
    ledger["new_x2_failed_witnesses"] = 171
    ledger["new_x2_bounded_passing_witnesses"] = 261
    ledger["current_overlay"] = {
        "effective_negatives": 41841,
        "effective_methods": 31199,
        "retained_failed_witnesses": 13502,
        "bounded_passing_witnesses": 18386,
        "open_gaps": 351,
        "exact_gates": 343,
    }
    ledger["phase_ledger_counts"] = {"methods": 445, "failed": 179, "passing": 266}
    write(ledger_path, ledger)
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["current_overlay"] = ledger["current_overlay"]
    truth["x2_operational_failures_retained"] = 1
    truth["x2_operational_recoveries"] = 1
    write(truth_path, truth)
    write(
        base / "x2" / "operational-failures.json",
        {
            "failed_witnesses": [
                {
                    "method_id": FAILED_ID,
                    "truth": False,
                    "zero_credit": True,
                    "description": ledger["methods"][-2]["description"],
                    "state_change": "no additional mutation was issued after the unattributed wrapper return",
                }
            ],
            "bounded_recoveries": [
                {
                    "method_id": PASS_ID,
                    "truth": True,
                    "description": ledger["methods"][-1]["description"],
                    "failed_witness_preserved": FAILED_ID,
                }
            ],
            "failed_witness_converted_to_pass": False,
        },
    )
    print(json.dumps({"failed": FAILED_ID, "recovery": PASS_ID, "replayed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
