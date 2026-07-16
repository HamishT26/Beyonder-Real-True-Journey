#!/usr/bin/env python3
"""Invoke and witness all ten frozen v646-v2 family-current runners."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v2"
RUNNERS = [
    "ghc_family_source_status_drift_guard.py",
    "ghc_family_proposal_neighbor_quarantine.py",
    "ghc_family_logical_manifest_parity.py",
    "ghc_family_method_state_preflight.py",
    "ghc_family_terminal_route_guard.py",
    "ghc_family_evidence_dag_closure.py",
    "ghc_family_v646_v2_core_runner.py",
    "ghc_family_v646_v2_portfolio_runner.py",
    "ghc_family_v646_v2_skill_runner.py",
    "ghc_family_v646_v2_validation_runner.py",
]
BOUNDARY = "Runner use establishes bounded same-owner software behavior only; not deployment, domain confirmation, complete assurance, authority, or independent reproduction."


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    receipts = []
    output_dir = PHASE / "prototypes/runner-use"
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(RUNNERS, start=1):
        script = ROOT / "scripts" / name
        output = output_dir / f"{index:02d}-{script.stem}.json"
        result = subprocess.run([sys.executable, str(script), "--output", str(output)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        parsed = None
        if output.is_file():
            try:
                parsed = json.loads(output.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                parsed = None
        passed = result.returncode == 0 and isinstance(parsed, dict) and bool(parsed.get("passed", parsed.get("valid")))
        receipts.append({
            "runner": name,
            "family_current": name.startswith("ghc_family_"),
            "output": output.relative_to(PHASE).as_posix(),
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "parsed": isinstance(parsed, dict),
            "bounded_checks": parsed.get("checks", parsed.get("check_count", 0)) if isinstance(parsed, dict) else 0,
            "passed": passed,
            "same_owner_only": True,
            "independent_reproduction": False,
        })
        if not passed:
            write_json("prototypes/runner-build-use-receipt.json", {
                "schema": "ghc.family.v646-v2.runner-build-use-receipt.v1",
                "runner_count": len(RUNNERS), "invoked_before_stop": len(receipts), "passed": sum(row["passed"] for row in receipts),
                "runners": receipts, "valid": False, "boundary": BOUNDARY,
            })
            print(json.dumps({"runner": name, "returncode": result.returncode, "passed": False}))
            return 1
    payload = {
        "schema": "ghc.family.v646-v2.runner-build-use-receipt.v1",
        "runner_count": len(RUNNERS),
        "built_count": sum((ROOT / "scripts" / name).is_file() for name in RUNNERS),
        "invoked_count": len(receipts),
        "passed_count": sum(row["passed"] for row in receipts),
        "family_current_count": sum(row["family_current"] for row in receipts),
        "runners": receipts,
        "valid": all(row["passed"] for row in receipts),
        "boundary": BOUNDARY,
    }
    write_json("prototypes/runner-build-use-receipt.json", payload)
    ledger_path = PHASE / "prototypes/skill-and-runner-ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    for row in ledger.get("runners", []):
        row["state"] = "built_invoked_and_bounded_witness_passed"
    ledger["runners_built_and_used"] = len(receipts)
    ledger["runner_receipt"] = "prototypes/runner-build-use-receipt.json"
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    truth_path = PHASE / "phase-truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    truth["runners_aggregate_use_pending"] = False
    truth["runners_built_and_used"] = len(receipts)
    truth_path.write_text(json.dumps(truth, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(receipts), "built": payload["built_count"], "invoked": payload["invoked_count"], "passed": payload["passed_count"], "valid": payload["valid"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
