#!/usr/bin/env python3
"""Dry-run THOS regression fixture checker.

The checker reads shape-only regression fixtures and reports whether each case
has the fields needed to classify unexpected success, unexpected failure, and
related export/reporting regressions. It does not execute connector actions,
cleanup, publication, or external writes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_PRIOR_STATUSES = {"PASS_SHAPE_ONLY", "FAIL_BLOCKER", "OPEN_GAP", "NOT_RUN"}
ALLOWED_INTERPRETATIONS = {
    "unexpected_success",
    "unexpected_failure",
    "intermittent_or_environment_drift",
    "reporting_failure",
}


def row_for(case: dict[str, Any]) -> dict[str, Any]:
    missing = [
        field
        for field in ["case_id", "prior_expected_status", "simulated_current_status", "expected_interpretation", "required_response"]
        if not case.get(field)
    ]
    status = "PASS_SHAPE_ONLY"
    reason = "case_shape_valid"
    if missing:
        status = "OPEN_GAP"
        reason = "missing_required_fields"
    elif case["prior_expected_status"] not in ALLOWED_PRIOR_STATUSES:
        status = "OPEN_GAP"
        reason = "invalid_prior_expected_status"
    elif case["simulated_current_status"] not in ALLOWED_PRIOR_STATUSES:
        status = "OPEN_GAP"
        reason = "invalid_simulated_current_status"
    elif case["expected_interpretation"] not in ALLOWED_INTERPRETATIONS:
        status = "OPEN_GAP"
        reason = "invalid_expected_interpretation"

    return {
        "case_id": case.get("case_id", "unknown_case"),
        "status": status,
        "reason_code": reason,
        "prior_expected_status": case.get("prior_expected_status"),
        "simulated_current_status": case.get("simulated_current_status"),
        "expected_interpretation": case.get("expected_interpretation"),
        "required_response_present": bool(case.get("required_response")),
        "mutation_performed": False,
        "connector_write_performed": False,
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
    parser = argparse.ArgumentParser(description="Check THOS regression fixture shape.")
    parser.add_argument("--input", required=True, help="Regression fixture JSON file")
    parser.add_argument("--output", help="Optional JSON report path to write")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    cases = data.get("regression_cases", [])
    if not isinstance(cases, list):
        raise SystemExit("regression_cases must be a list")
    rows = [row_for(case) for case in cases if isinstance(case, dict)]
    report = {
        "validator_mode": "local_non_mutating_regression_fixture_check",
        "input_file": Path(args.input).as_posix(),
        "aggregate_status": aggregate(rows),
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "rows": rows,
    }
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())
