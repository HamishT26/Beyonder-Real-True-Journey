#!/usr/bin/env python3
"""Build a compact THOS reason-code dashboard fixture from a regression report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def case_row(case: dict[str, Any]) -> dict[str, Any]:
    reason_codes = case.get("observed_reason_codes") or []
    dominant_reason_code = case.get("observed_dominant_reason_code")
    return {
        "allowed_extra_reason_codes": case.get("allowed_extra_reason_codes") or [],
        "case_id": case.get("case_id"),
        "expected_decision": case.get("expected_decision"),
        "expected_dominant_reason_code": case.get("expected_dominant_reason_code"),
        "expected_reason_codes": case.get("expected_reason_codes") or [],
        "expected_status": case.get("expected_status"),
        "guard_decision": case.get("guard_decision"),
        "guard_status": case.get("guard_aggregate_status"),
        "matched_reason_codes": case.get("matched_reason_codes") or [],
        "matches_expected": bool(case.get("matches_expected")),
        "missing_required_reason_codes": case.get("missing_required_reason_codes") or [],
        "primary_selection_mode": "priority_table" if dominant_reason_code else "none",
        "reason_codes": reason_codes,
        "row_status": "PASS_SHAPE_ONLY" if case.get("matches_expected") else "FAIL_BLOCKER",
        "unexpected_extra_reason_codes": case.get("unexpected_extra_reason_codes") or [],
        "observed_dominant_reason_code": dominant_reason_code,
    }


def build_fixture(report: dict[str, Any], phase_slug: str) -> dict[str, Any]:
    cases = report.get("cases")
    if not isinstance(cases, list):
        raise ValueError("regression report must contain a cases list")
    rows = [case_row(case) for case in cases if isinstance(case, dict)]
    missing_required_rows = [
        row["case_id"]
        for row in rows
        if row["missing_required_reason_codes"]
    ]
    unexpected_extra_rows = [
        row["case_id"]
        for row in rows
        if row["unexpected_extra_reason_codes"]
    ]
    dominant_mismatch_rows = [
        row["case_id"]
        for row in rows
        if row["observed_dominant_reason_code"] != row["expected_dominant_reason_code"]
    ]
    nonmatching_rows = [row["case_id"] for row in rows if not row["matches_expected"]]
    return {
        "aggregate_status": "FAIL_BLOCKER"
        if missing_required_rows or unexpected_extra_rows or dominant_mismatch_rows or nonmatching_rows
        else "PASS_SHAPE_ONLY",
        "case_count": len(rows),
        "connector_write_performed": False,
        "dashboard_fixture_id": "thos_reason_code_dashboard_fixture_v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "renderer_migration_status": "blocked_until_broader_manifest_coverage_green",
        "rows": rows,
        "summary": {
            "dominant_mismatch_case_ids": dominant_mismatch_rows,
            "missing_required_case_ids": missing_required_rows,
            "nonmatching_case_ids": nonmatching_rows,
            "unexpected_extra_case_ids": unexpected_extra_rows,
        },
        "validator_mode": "local_non_mutating_dashboard_fixture",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a compact THOS reason-code dashboard fixture.")
    parser.add_argument("--report", required=True, help="Regression report JSON path")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True, help="Output fixture JSON path")
    args = parser.parse_args()

    fixture = build_fixture(read_json_object(Path(args.report)), args.phase_slug)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(fixture, indent=2, sort_keys=True))
    return 0 if fixture["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
