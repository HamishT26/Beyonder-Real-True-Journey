#!/usr/bin/env python3
"""Check THOS negative fixture contract readiness.

This checker verifies that negative fixture definitions contain enough
machine-readable material to be executed by a later full verifier. It does not
perform connector writes, destructive cleanup, or GMUT validation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "fixture_id",
    "target_surface",
    "expected_status",
    "trigger",
    "required_response",
}


def row_for(fixture: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(field for field in REQUIRED_FIELDS if not fixture.get(field))
    status = "PASS_SHAPE_ONLY"
    reason = "expected_fail_contract_present"
    if missing:
        status = "OPEN_GAP"
        reason = "missing_required_fields"
    elif fixture.get("expected_status") != "FAIL_BLOCKER":
        status = "FAIL_BLOCKER"
        reason = "negative_fixture_must_expect_fail_blocker"
    return {
        "fixture_id": fixture.get("fixture_id", "unknown_fixture"),
        "status": status,
        "reason_code": reason,
        "target_surface": fixture.get("target_surface"),
        "expected_runtime_status": fixture.get("expected_status"),
        "missing_fields": missing,
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmut_gate_effect": "none_open_not_tested",
    }


def aggregate(rows: list[dict[str, Any]]) -> str:
    statuses = [row["status"] for row in rows]
    if "FAIL_BLOCKER" in statuses:
        return "FAIL_BLOCKER"
    if "OPEN_GAP" in statuses:
        return "OPEN_GAP"
    if statuses and all(status == "NOT_RUN" for status in statuses):
        return "NOT_RUN"
    return "PASS_SHAPE_ONLY"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check THOS negative fixture contract readiness.")
    parser.add_argument("--input", required=True, help="Negative fixture JSON file")
    parser.add_argument("--output", help="Optional JSON report path to write")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    fixtures = data.get("negative_fixtures", [])
    if not isinstance(fixtures, list):
        raise SystemExit("negative_fixtures must be a list")
    rows = [row_for(fixture) for fixture in fixtures if isinstance(fixture, dict)]
    report = {
        "validator_mode": "local_non_mutating_negative_fixture_contract_check",
        "input_file": Path(args.input).as_posix(),
        "aggregate_status": aggregate(rows),
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "fixture_count": len(rows),
        "rows": rows,
    }
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())
