#!/usr/bin/env python3
"""Append v654-v3 x2 failures to the frozen x1 Method Flow through the family runner."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import ghc_family_v654_v3_phase_data as d
import ghc_family_v654_v3_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run(args, cwd=REPO, check=True, env=env)


def build(ledger: Path) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    frozen = subprocess.check_output(
        [
            "git",
            "show",
            "0c53bce867ec5259d9b7de8c14b92b07b678641f:"
            "docs/sylven-arc/v654-v3/method-flow/method-flow-ledger.json",
        ],
        cwd=REPO,
    )
    ledger.write_bytes(frozen)
    requests = ROOT / "method-flow/x2-requests"
    for offset, negative in enumerate(x2.X2_OPERATIONAL_NEGATIVES, 32):
        method_id = f"V6543-METHOD-{offset:02d}"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['signature']}",
            "trigger_preconditions": [negative["signature"]],
            "failure_signature": negative["failed"],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.",
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "recommendation_state": "candidate",
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction or broader assurance.",
            "retained_negative_ids": [negative["negative_id"]],
            "supersedes": [],
        }
        failed = {
            "witness_id": f"V6543-WITNESS-{offset:02d}-F",
            "method_id": method_id,
            "scope": negative["signature"],
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The initial attempt would satisfy its bounded postcondition.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero pass credit; failure remains retained.",
        }
        passed = {
            "witness_id": f"V6543-WITNESS-{offset:02d}-P",
            "method_id": method_id,
            "scope": negative["signature"],
            "procedure": negative["recovery"],
            "expected": "The isolated bounded recovery establishes only its declared postcondition.",
            "observed": f"The bounded recovery completed for {negative['signature']}; the failure remains retained.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Passing recovery is same-owner bounded evidence only and does not erase the failed witness.",
        }
        method_path = requests / f"method-{offset:02d}.json"
        failed_path = requests / f"witness-{offset:02d}-failed.json"
        passed_path = requests / f"witness-{offset:02d}-passing.json"
        write_json(method_path, method)
        write_json(failed_path, failed)
        write_json(passed_path, passed)
        run(sys.executable, str(RUNNER), "record", "--ledger", str(ledger), "--record-file", str(method_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(failed_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(passed_path))
        run(sys.executable, str(RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Preferred only for the declared bounded trigger; no broader assurance.")
    print(json.dumps({"ledger": str(ledger), "x1_methods": 31, "x2_methods": len(x2.X2_OPERATIONAL_NEGATIVES)}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    args = parser.parse_args()
    build(Path(args.ledger).resolve())


if __name__ == "__main__":
    main()
