#!/usr/bin/env python3
"""Initialize Ilyra Fen v650-v8 Method Flow from retained startup failures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import ghc_family_v650_v8_phase_data as data


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / data.PHASE_ROOT / "method-flow"
LEDGER = ROOT / "method-flow-ledger.json"
RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"


def run(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run(list(args), cwd=REPO, check=True, env=env)


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    if LEDGER.exists():
        raise RuntimeError("Method Flow ledger already exists; preserve it append-only")
    run(sys.executable, str(RUNNER), "init", "--ledger", str(LEDGER), "--phase", data.PHASE, "--owner", data.OWNER)

    for number, negative in enumerate(data.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6508-M{number:02d}"
        failed_id = f"{method_id}-WFAIL"
        passing_id = f"{method_id}-WPASS"
        stem = f"v6508-m{number:02d}"
        method_path = ROOT / f"{stem}-method-record.json"
        failed_path = ROOT / f"{stem}-wfail-witness.json"
        passing_path = ROOT / f"{stem}-wpass-witness.json"

        method = {
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": negative["recovery"],
            "failure_signature": negative["failed"],
            "method_id": method_id,
            "privacy_class": "sanitized_public",
            "protected_gates": ["failure_retention", "bounded_read_scope", "x1_source_integrity", "evidence_credit"],
            "recommendation_state": "candidate",
            "recurrence_guard": negative["recurrence_guard"],
            "retained_negative_ids": [negative["negative_id"]],
            "rollback": "Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.",
            "scope_boundary": "Owner-local startup and x1 workflow recovery only; no scientific, production, professional, legal, cultural, Maori-authority, or independent-reproduction credit.",
            "supersedes": [],
            "title": f"Recover from {negative['category']} without erasing the failed witness",
            "trigger_preconditions": [negative["category"]],
            "validation_witness_ids": [],
        }
        failed = {
            "boundary": "Failed owner-local startup or inspection operation with zero pass, mutation, or validation credit.",
            "expected": "Complete the declared bounded inspection with an attributable result.",
            "independent_reproduction": False,
            "method_id": method_id,
            "observed": negative["failed"],
            "procedure": f"Use the first attempted wrapper for {negative['category']}.",
            "result": "fail",
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "scope": f"failed {negative['category']}",
            "witness_id": failed_id,
        }
        passing = {
            "boundary": "Bounded same-owner workflow recovery only; the earlier failure remains retained and no independent reproduction is claimed.",
            "expected": "Complete the corrected bounded operation while preserving the failed witness.",
            "independent_reproduction": False,
            "method_id": method_id,
            "observed": negative["passing"],
            "procedure": negative["recovery"],
            "result": "pass",
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "scope": f"bounded recovery for {negative['category']}",
            "witness_id": passing_id,
        }
        write(method_path, method)
        write(failed_path, failed)
        write(passing_path, passing)
        run(sys.executable, str(RUNNER), "record", "--ledger", str(LEDGER), "--record-file", str(method_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(LEDGER), "--witness-file", str(failed_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(LEDGER), "--witness-file", str(passing_path))
        run(
            sys.executable,
            str(RUNNER),
            "set-state",
            "--ledger",
            str(LEDGER),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Promoted only after one retained failed witness and one bounded passing recovery witness.",
        )

    run(sys.executable, str(RUNNER), "validate", "--ledger", str(LEDGER), "--receipt", str(ROOT / "method-flow-validation.json"))
    run(
        sys.executable,
        str(RUNNER),
        "summarize",
        "--ledger",
        str(LEDGER),
        "--json-output",
        str(ROOT / "method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow-summary.md"),
    )
    print(json.dumps({"phase": data.PHASE, "methods": len(data.X1_OPERATIONAL_NEGATIVES), "failed": len(data.X1_OPERATIONAL_NEGATIVES), "passed": len(data.X1_OPERATIONAL_NEGATIVES), "state": "preferred_bounded_only"}, sort_keys=True))


if __name__ == "__main__":
    build()
