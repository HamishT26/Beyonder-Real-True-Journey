#!/usr/bin/env python3
"""Append-only Sable v652-v1 x2 operational incident records."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import ghc_family_v652_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
LEDGER = ROOT / "method-flow/method-flow-ledger.json"
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"

INCIDENTS = [
    {
        "negative_id": "V6521-X2-N01",
        "method_id": "V6521-M03",
        "category": "powershell_foreach_pipeline_recurrence",
        "failed": "A runner-collision preflight repeated the known Windows PowerShell statement-level foreach pipeline parser fault before any probe or mutation ran.",
        "recovery": "Materialize the per-runner collision rows in an array and pipe only the completed array.",
        "passing": "The corrected bounded collision inventory returned one row per proposed family-current runner.",
        "recurrence_guard": "Apply the existing M03 array-before-pipeline rule to every statement-level foreach wrapper.",
    }
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def invoke(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run([sys.executable, str(RUNNER), *args], cwd=REPO, env=env, check=True)


def record(stage: str) -> None:
    item = INCIDENTS[0]
    suffix = "fail2" if stage == "fail" else "pass2"
    witness_id = "V6521-M03-WFAIL2" if stage == "fail" else "V6521-M03-WPASS2"
    path = ROOT / f"method-flow/records/v6521-m03-{suffix}.json"
    payload = {
        "witness_id": witness_id,
        "method_id": item["method_id"],
        "procedure": "Retain the recurrence before retry." if stage == "fail" else "Apply the existing array-before-pipeline recovery to the isolated probe.",
        "scope": "Sable v652-v1 x2 runner-collision preflight",
        "expected": "The recurrence fails before execution." if stage == "fail" else "The corrected bounded probe returns exact collision rows.",
        "observed": item["failed"] if stage == "fail" else item["passing"],
        "result": "fail" if stage == "fail" else "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [item["negative_id"]],
        "boundary": "The recovery validates only the isolated wrapper rule and never erases the recurrence.",
    }
    write_json(path, payload)
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not any(row["witness_id"] == witness_id for row in ledger["witnesses"]):
        invoke("witness", "--ledger", str(LEDGER), "--witness-file", str(path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["fail", "pass"])
    args = parser.parse_args()
    record(args.stage)


if __name__ == "__main__":
    main()
