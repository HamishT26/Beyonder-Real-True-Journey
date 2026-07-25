#!/usr/bin/env python3
"""Build Tavian Sol v654-v6 x1 Method Flow through the family runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import ghc_family_v654_v6_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def run(*args: str) -> None:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    subprocess.run(args, cwd=REPO, check=True, env=env)


def build(ledger: Path, inherited_ledger: Path) -> None:
    if ledger.exists():
        ledger.unlink()
    inherited_bytes = inherited_ledger.read_bytes()
    inherited = json.loads(inherited_bytes.decode("utf-8"))
    if (
        len(inherited.get("methods", [])) != d.INHERITED_METHODS
        or sum(row.get("result") == "fail" for row in inherited.get("witnesses", []))
        != d.INHERITED_FAILED_WITNESSES
        or sum(row.get("result") == "pass" for row in inherited.get("witnesses", []))
        != d.INHERITED_PASSING_WITNESSES
    ):
        raise RuntimeError("inherited Method Flow counts do not match the exact Eiren source")
    inherited["phase"] = d.PHASE
    inherited["owner"] = d.OWNER
    inherited["identity_boundary"] = (
        "Tavian Sol is relational working language only; no consciousness, personhood, "
        "identity continuity, employment, qualification, authority, or independent-agency claim."
    )
    inherited["inherited_anchor"] = {
        "phase": "v654-v5",
        "method_count": d.INHERITED_METHODS,
        "failed_witness_count": d.INHERITED_FAILED_WITNESSES,
        "passing_witness_count": d.INHERITED_PASSING_WITNESSES,
        "sha256": hashlib.sha256(inherited_bytes).hexdigest(),
        "completion_credit": False,
    }
    inherited["current_phase_method_ids"] = []
    write_json(ledger, inherited)
    requests = ROOT / "method-flow/requests"
    records = [
        {**negative, "negative_ids": [negative["negative_id"]]}
        for negative in d.X1_OPERATIONAL_NEGATIVES
    ]
    for index, negative in enumerate(records, 1):
        method_id = f"V6546-METHOD-{index:02d}"
        failure_signature = negative["signature"]
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {failure_signature}",
            "trigger_preconditions": [failure_signature],
            "failure_signature": negative["failed"],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": (
                "Stop, retain the failed witness with zero credit, and leave external, sibling, participant, "
                "production, professional, legal, cultural, and authority state unchanged."
            ),
            "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "recommendation_state": "candidate",
            "scope_boundary": (
                "Same-owner bounded workflow recovery only; not independent reproduction or scientific, "
                "production, professional, legal, cultural, accessibility-complete, or authority evidence."
            ),
            "retained_negative_ids": negative["negative_ids"],
            "supersedes": [],
        }
        failed = {
            "witness_id": f"V6546-WITNESS-{index:02d}-F",
            "method_id": method_id,
            "scope": failure_signature,
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The initial attempt would satisfy its bounded postcondition.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative["negative_ids"],
            "boundary": "Zero pass credit; failure remains retained.",
        }
        passed = {
            "witness_id": f"V6546-WITNESS-{index:02d}-P",
            "method_id": method_id,
            "scope": failure_signature,
            "procedure": negative["recovery"],
            "expected": "The isolated bounded recovery establishes only its declared postcondition.",
            "observed": (
                f"The bounded recovery completed for {failure_signature}; the original failure remains retained."
            ),
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative["negative_ids"],
            "boundary": (
                "Passing recovery is same-owner bounded evidence only and does not erase the failed witness."
            ),
        }
        method_path = requests / f"method-{index:02d}.json"
        failed_path = requests / f"witness-{index:02d}-failed.json"
        passed_path = requests / f"witness-{index:02d}-passing.json"
        write_json(method_path, method)
        write_json(failed_path, failed)
        write_json(passed_path, passed)
        run(sys.executable, str(RUNNER), "record", "--ledger", str(ledger), "--record-file", str(method_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(failed_path))
        run(sys.executable, str(RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(passed_path))
        run(
            sys.executable,
            str(RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Preferred only for the declared bounded trigger; no broader assurance.",
        )
    combined = json.loads(ledger.read_text(encoding="utf-8"))
    combined["current_phase_method_ids"] = [
        f"V6546-METHOD-{index:02d}" for index in range(1, len(records) + 1)
    ]
    write_json(ledger, combined)
    print(json.dumps({"ledger": str(ledger), "methods": len(records)}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--inherited-ledger", required=True)
    args = parser.parse_args()
    build(Path(args.ledger).resolve(), Path(args.inherited_ledger).resolve())


if __name__ == "__main__":
    main()
