#!/usr/bin/env python3
"""Assert compact THOS reason dashboard fixture consistency."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"FAIL_BLOCKER", "PASS_SHAPE_ONLY"}
REQUIRED_TOP_LEVEL_FIELDS = {
    "aggregate_status": str,
    "case_count": int,
    "connector_write_performed": bool,
    "dashboard_fixture_id": str,
    "gmUT_gate_effect": str,
    "mutation_performed": bool,
    "phase_slug": str,
    "renderer_migration_status": str,
    "rows": list,
    "summary": dict,
    "validator_mode": str,
}
REQUIRED_ROW_FIELDS = {
    "allowed_extra_reason_codes": list,
    "case_id": str,
    "expected_dominant_reason_code": (str, type(None)),
    "expected_reason_codes": list,
    "guard_decision": str,
    "guard_status": str,
    "matched_reason_codes": list,
    "matches_expected": bool,
    "missing_required_reason_codes": list,
    "observed_dominant_reason_code": (str, type(None)),
    "primary_selection_mode": str,
    "reason_codes": list,
    "row_status": str,
    "unexpected_extra_reason_codes": list,
}
REQUIRED_SUMMARY_FIELDS = {
    "dominant_mismatch_case_ids": list,
    "missing_required_case_ids": list,
    "nonmatching_case_ids": list,
    "unexpected_extra_case_ids": list,
}


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def status_from_failures(failures: list[str]) -> str:
    return "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY"


def add_row(rows: list[dict[str, Any]], row_id: str, ok: bool, message: str, evidence: Any = None) -> None:
    rows.append(
        {
            "evidence": evidence,
            "message": message,
            "row_id": row_id,
            "status": "PASS_SHAPE_ONLY" if ok else "FAIL_BLOCKER",
        }
    )


def list_case_ids(rows: list[dict[str, Any]], predicate: str) -> list[str]:
    return [
        row["case_id"]
        for row in rows
        if row.get(predicate)
    ]


def assert_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []

    missing_top = sorted(field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in fixture)
    add_row(rows, "top_level_fields", not missing_top, "required fixture fields are present", missing_top)
    if missing_top:
        failures.extend(f"missing_top:{field}" for field in missing_top)
        return assertion_payload(rows, failures)

    top_type_errors = [
        field
        for field, expected_type in REQUIRED_TOP_LEVEL_FIELDS.items()
        if not isinstance(fixture[field], expected_type)
    ]
    add_row(rows, "top_level_types", not top_type_errors, "required fixture field types are constrained", top_type_errors)
    failures.extend(f"type_top:{field}" for field in top_type_errors)

    boundary_ok = (
        fixture["connector_write_performed"] is False
        and fixture["mutation_performed"] is False
        and fixture["gmUT_gate_effect"] == "none_open_not_tested"
        and fixture["validator_mode"] == "local_non_mutating_dashboard_fixture"
    )
    add_row(
        rows,
        "local_non_mutating_boundary",
        boundary_ok,
        "fixture remains local, non-mutating, and no-GMUT-gate-effect",
        {
            "connector_write_performed": fixture["connector_write_performed"],
            "gmUT_gate_effect": fixture["gmUT_gate_effect"],
            "mutation_performed": fixture["mutation_performed"],
            "validator_mode": fixture["validator_mode"],
        },
    )
    if not boundary_ok:
        failures.append("boundary:local_non_mutating")

    fixture_rows = fixture["rows"]
    count_ok = fixture["case_count"] == len(fixture_rows)
    add_row(rows, "case_count", count_ok, "case_count reconciles with row count", {"case_count": fixture["case_count"], "rows": len(fixture_rows)})
    if not count_ok:
        failures.append("count:case_count")

    row_type_errors: list[str] = []
    row_field_errors: list[str] = []
    row_logic_errors: list[str] = []
    clean_rows: list[dict[str, Any]] = []
    for index, row in enumerate(fixture_rows):
        if not isinstance(row, dict):
            row_type_errors.append(f"row[{index}]")
            continue
        clean_rows.append(row)
        missing_row = sorted(field for field in REQUIRED_ROW_FIELDS if field not in row)
        row_field_errors.extend(f"{row.get('case_id', index)}:{field}" for field in missing_row)
        if missing_row:
            continue
        for field, expected_type in REQUIRED_ROW_FIELDS.items():
            if not isinstance(row[field], expected_type):
                row_type_errors.append(f"{row['case_id']}:{field}")
        allowed_codes = set(row["expected_reason_codes"]) | set(row["allowed_extra_reason_codes"])
        missing_required = [code for code in row["expected_reason_codes"] if code not in row["reason_codes"]]
        unexpected_extra = [code for code in dict.fromkeys(row["reason_codes"]) if code not in allowed_codes]
        if missing_required != row["missing_required_reason_codes"]:
            row_logic_errors.append(f"{row['case_id']}:missing_required")
        if unexpected_extra != row["unexpected_extra_reason_codes"]:
            row_logic_errors.append(f"{row['case_id']}:unexpected_extra")
        if row["observed_dominant_reason_code"] and row["observed_dominant_reason_code"] not in row["reason_codes"]:
            row_logic_errors.append(f"{row['case_id']}:dominant_not_in_reason_codes")
        expected_selection = "priority_table" if row["observed_dominant_reason_code"] else "none"
        if row["primary_selection_mode"] != expected_selection:
            row_logic_errors.append(f"{row['case_id']}:primary_selection_mode")
        expected_row_status = (
            "FAIL_BLOCKER"
            if row["missing_required_reason_codes"]
            or row["unexpected_extra_reason_codes"]
            or row["observed_dominant_reason_code"] != row["expected_dominant_reason_code"]
            or not row["matches_expected"]
            else "PASS_SHAPE_ONLY"
        )
        if row["row_status"] != expected_row_status:
            row_logic_errors.append(f"{row['case_id']}:row_status")

    add_row(rows, "row_fields", not row_field_errors, "required row fields are present", row_field_errors)
    add_row(rows, "row_types", not row_type_errors, "required row field types are constrained", row_type_errors)
    add_row(rows, "row_logic", not row_logic_errors, "row reason-code logic reconciles", row_logic_errors)
    failures.extend(f"row_field:{item}" for item in row_field_errors)
    failures.extend(f"row_type:{item}" for item in row_type_errors)
    failures.extend(f"row_logic:{item}" for item in row_logic_errors)

    summary = fixture["summary"]
    missing_summary = sorted(field for field in REQUIRED_SUMMARY_FIELDS if field not in summary)
    add_row(rows, "summary_fields", not missing_summary, "summary fields are present", missing_summary)
    failures.extend(f"missing_summary:{field}" for field in missing_summary)
    if not missing_summary:
        expected_summary = {
            "dominant_mismatch_case_ids": [
                row["case_id"]
                for row in clean_rows
                if row.get("observed_dominant_reason_code") != row.get("expected_dominant_reason_code")
            ],
            "missing_required_case_ids": list_case_ids(clean_rows, "missing_required_reason_codes"),
            "nonmatching_case_ids": [row["case_id"] for row in clean_rows if not row.get("matches_expected")],
            "unexpected_extra_case_ids": list_case_ids(clean_rows, "unexpected_extra_reason_codes"),
        }
        summary_ok = summary == expected_summary
        add_row(rows, "summary_rederived", summary_ok, "summary reconciles with rows", {"expected": expected_summary, "actual": summary})
        if not summary_ok:
            failures.append("summary:rederived")

        expected_aggregate = (
            "FAIL_BLOCKER"
            if any(expected_summary.values())
            else "PASS_SHAPE_ONLY"
        )
        aggregate_ok = fixture["aggregate_status"] == expected_aggregate
        add_row(
            rows,
            "aggregate_status_rederived",
            aggregate_ok,
            "aggregate status reconciles with summary",
            {"expected": expected_aggregate, "actual": fixture["aggregate_status"]},
        )
        if not aggregate_ok:
            failures.append("aggregate:status")

    return assertion_payload(rows, failures)


def assertion_payload(rows: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    status = status_from_failures(failures)
    return {
        "aggregate_status": status,
        "assertion_failures": failures,
        "assertion_status": status,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "report_mode": "local_non_mutating",
        "rows": rows,
        "validator_mode": "local_non_mutating_reason_dashboard_fixture_assertion",
    }


def negative_self_test_fixture() -> dict[str, Any]:
    return {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "case_count": 2,
        "connector_write_performed": False,
        "dashboard_fixture_id": "thos_reason_code_dashboard_fixture_v1",
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": "self-test-negative",
        "renderer_migration_status": "blocked_until_broader_manifest_coverage_green",
        "rows": [
            {
                "allowed_extra_reason_codes": [],
                "case_id": "negative_missing_required_and_unexpected_extra",
                "expected_dominant_reason_code": "REQUIRED_A",
                "expected_reason_codes": ["REQUIRED_A", "REQUIRED_B"],
                "guard_decision": "deny",
                "guard_status": "FAIL_BLOCKER",
                "matched_reason_codes": ["REQUIRED_A"],
                "matches_expected": True,
                "missing_required_reason_codes": [],
                "observed_dominant_reason_code": "REQUIRED_A",
                "primary_selection_mode": "priority_table",
                "reason_codes": ["REQUIRED_A", "UNEXPECTED_C"],
                "row_status": "PASS_SHAPE_ONLY",
                "unexpected_extra_reason_codes": [],
            },
            {
                "allowed_extra_reason_codes": [],
                "case_id": "negative_nonempty_missing_not_blocked",
                "expected_dominant_reason_code": None,
                "expected_reason_codes": ["REQUIRED_Z"],
                "guard_decision": "deny",
                "guard_status": "FAIL_BLOCKER",
                "matched_reason_codes": [],
                "matches_expected": True,
                "missing_required_reason_codes": ["REQUIRED_Z"],
                "observed_dominant_reason_code": None,
                "primary_selection_mode": "none",
                "reason_codes": [],
                "row_status": "PASS_SHAPE_ONLY",
                "unexpected_extra_reason_codes": [],
            }
        ],
        "summary": {
            "dominant_mismatch_case_ids": [],
            "missing_required_case_ids": [],
            "nonmatching_case_ids": [],
            "unexpected_extra_case_ids": [],
        },
        "validator_mode": "local_non_mutating_dashboard_fixture",
    }


def write_report(report: dict[str, Any], output: str | None) -> None:
    text = json.dumps(report, indent=2, sort_keys=True)
    if output:
        Path(output).write_text(text + "\n", encoding="utf-8")
    print(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Assert compact THOS reason dashboard fixture consistency.")
    parser.add_argument("--fixture", help="Compact fixture JSON path")
    parser.add_argument("--output", help="Optional assertion JSON output path")
    parser.add_argument(
        "--self-test-negative",
        action="store_true",
        help="Pass only when a deliberately inconsistent compact fixture is rejected.",
    )
    args = parser.parse_args()

    if args.self_test_negative:
        negative_report = assert_fixture(negative_self_test_fixture())
        expected_failure = negative_report["aggregate_status"] == "FAIL_BLOCKER"
        report = {
            "aggregate_status": "PASS_SHAPE_ONLY" if expected_failure else "FAIL_BLOCKER",
            "connector_write_performed": False,
            "expected_negative_report": negative_report,
            "gmUT_gate_effect": "none_open_not_tested",
            "mutation_performed": False,
            "self_test_id": "reason_dashboard_fixture_negative_detection_v1",
            "validator_mode": "local_non_mutating_reason_dashboard_fixture_negative_self_test",
        }
        write_report(report, args.output)
        return 0 if report["aggregate_status"] == "PASS_SHAPE_ONLY" else 1

    if not args.fixture:
        raise SystemExit("--fixture is required unless --self-test-negative is used")
    report = assert_fixture(load_json_object(Path(args.fixture)))
    write_report(report, args.output)
    return 0 if report["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
