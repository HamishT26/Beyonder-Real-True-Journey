#!/usr/bin/env python3
"""Run the ten Auren v672-v2 owner-scoped synthetic runner smokes once."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    x2 = root / "docs" / "auren-lark" / "v672-v2" / "x2"
    receipt_path = x2 / "validation" / "runner-smoke-receipt.json"
    failed_path = x2 / "validation" / "runner-smoke-failed-001.json"
    if receipt_path.exists():
        raise SystemExit("successful x2 runner-smoke receipt already exists; replay refused")
    if failed_path.exists():
        raise SystemExit("failed x2 runner-smoke receipt already exists; use an isolated recovery rather than replaying the aggregate")

    registry = json.loads(
        (x2 / "tools" / "runner-registry.json").read_text(encoding="utf-8")
    )
    fixture_ledger = json.loads(
        (x2 / "fixtures" / "fixture-ledger.json").read_text(encoding="utf-8")
    )
    runner_for = {row["surface"]: root / row["path"] for row in registry["runners"]}
    results = []
    for fixture in fixture_ledger["rows"]:
        command = [
            sys.executable,
            "-B",
            str(runner_for[fixture["surface"]]),
            "--input",
            str(root / fixture["path"]),
            "--expect",
            fixture["expected"],
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        parsed = None
        if completed.stdout.strip():
            try:
                parsed = json.loads(completed.stdout)
            except json.JSONDecodeError:
                parsed = None
        passed = (
            completed.returncode == 0
            and isinstance(parsed, dict)
            and parsed.get("passed") is True
            and parsed.get("surface") == fixture["surface"]
            and parsed.get("expect") == fixture["expected"]
        )
        results.append(
            {
                "fixture_id": fixture["fixture_id"],
                "surface": fixture["surface"],
                "expected": fixture["expected"],
                "passed": passed,
                "runner_exit": completed.returncode,
                "errors": parsed.get("errors", []) if isinstance(parsed, dict) else ["unparseable_runner_output"],
            }
        )

    accepting = [row for row in results if row["expected"] == "accept"]
    rejecting = [row for row in results if row["expected"] == "reject"]
    mismatches = [row for row in results if not row["passed"]]
    payload = {
        "schema": "ghc.family.owner-scoped-runner-smoke.v4",
        "owner": "Auren Lark",
        "phase": "v672-v2",
        "scope": "ten Auren-local runners and sixty wholly synthetic fixtures only",
        "state": "VALID_X2_OWNER_SCOPED_RUNNER_SMOKE" if not mismatches else "INVALID_X2_RUNNER_SMOKE",
        "invocations": 1,
        "successful_invocations": 1 if not mismatches else 0,
        "runner_count": len(runner_for),
        "checks": len(results),
        "accepting_passed": sum(row["passed"] for row in accepting),
        "accepting_total": len(accepting),
        "rejecting_refused": sum(row["passed"] for row in rejecting),
        "rejecting_total": len(rejecting),
        "mismatch_count": len(mismatches),
        "results": results,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output_path = receipt_path if not mismatches else failed_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "state": payload["state"],
                "checks": payload["checks"],
                "accepting": f"{payload['accepting_passed']}/{payload['accepting_total']}",
                "rejecting": f"{payload['rejecting_refused']}/{payload['rejecting_total']}",
                "mismatches": payload["mismatch_count"],
            },
            sort_keys=True,
        )
    )
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
