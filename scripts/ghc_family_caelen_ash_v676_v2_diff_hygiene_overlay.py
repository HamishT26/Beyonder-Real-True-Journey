#!/usr/bin/env python3
"""Retain the precommit blank-line failure and its bounded correction witness."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
FAILED_ID = "CA6762-X2-N002"
PASS_ID = "CA6762-X2-P002"


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    branch = subprocess.check_output(["git", "-C", str(repo), "branch", "--show-current"], text=True).strip()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if branch != BRANCH or head != X1:
        raise SystemExit("diff-hygiene overlay requires the x2 precommit lifecycle")
    base = repo / "docs" / "caelen-ash" / "v676-v2"
    ledger_path = base / "x2" / "method-flow" / "ledger.json"
    truth_path = base / "x2" / "phase-truth.json"
    failures_path = base / "x2" / "operational-failures.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if any(row["method_id"] == FAILED_ID for row in ledger["methods"]):
        raise SystemExit("diff-hygiene overlay already applied")
    ledger["methods"].extend(
        [
            {
                "method_id": FAILED_ID,
                "status": "failed_zero_credit",
                "truth": False,
                "description": "Exact staged diff hygiene found one surplus blank line at the end of the new owner core module.",
                "recovered_by": PASS_ID,
                "state_change": False,
            },
            {
                "method_id": PASS_ID,
                "status": "bounded_pass",
                "truth": True,
                "description": "The isolated trailing blank line was removed and exact staged diff hygiene passed.",
                "failed_witness_preserved": FAILED_ID,
            },
        ]
    )
    ledger["new_x2_effective_methods"] = 434
    ledger["new_x2_negatives"] = 172
    ledger["new_x2_failed_witnesses"] = 172
    ledger["new_x2_bounded_passing_witnesses"] = 262
    ledger["current_overlay"] = {
        "effective_negatives": 41842,
        "effective_methods": 31201,
        "retained_failed_witnesses": 13503,
        "bounded_passing_witnesses": 18387,
        "open_gaps": 351,
        "exact_gates": 343
    }
    ledger["phase_ledger_counts"] = {"methods": 447, "failed": 180, "passing": 267}
    write(ledger_path, ledger)
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["current_overlay"] = ledger["current_overlay"]
    truth["x2_operational_failures_retained"] = 2
    truth["x2_operational_recoveries"] = 2
    write(truth_path, truth)
    failures = json.loads(failures_path.read_text(encoding="utf-8"))
    failures["failed_witnesses"].append(
        {
            "method_id": FAILED_ID,
            "truth": False,
            "zero_credit": True,
            "description": ledger["methods"][-2]["description"],
            "state_change": False
        }
    )
    failures["bounded_recoveries"].append(
        {
            "method_id": PASS_ID,
            "truth": True,
            "description": ledger["methods"][-1]["description"],
            "failed_witness_preserved": FAILED_ID
        }
    )
    write(failures_path, failures)
    print(json.dumps({"failed": FAILED_ID, "recovery": PASS_ID}, sort_keys=True))


if __name__ == "__main__":
    main()
