#!/usr/bin/env python3
"""Assert THOS visualization binding report contract consistency.

This checker is local and non-mutating. It verifies that a generated
visualization binding report's summary fields reconcile with its detailed
finding lists and explicit THOS/GMUT boundary markers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"FAIL_BLOCKER", "OPEN_GAP", "PASS_SHAPE_ONLY"}
PRECEDENCE_ORDER = ["FAIL_BLOCKER", "OPEN_GAP", "PASS_SHAPE_ONLY"]
BLOCKER_CODE_PRIORITY = [
    "DUPLICATE_CANONICAL_ROW_ID",
    "MALFORMED_VISUALIZATION_ROW",
    "DUPLICATE_VISUALIZATION_BINDING",
    "ORPHAN_VISUALIZATION_ROW",
    "MISSING_CANONICAL_VISUALIZATION_ROW",
    "TUPLE_MISMATCH",
    "GMUT_GATE_EFFECT_DRIFT",
    "DIGEST_MISMATCH",
]
REQUIRED_TOP_LEVEL_FIELDS = {
    "report_mode": str,
    "aggregate_status": str,
    "structural_binding_status": str,
    "digest_evidence_status": str,
    "precedence_order": list,
    "failure_codes": list,
    "dominant_failure_code": (str, type(None)),
    "dominant_finding_code": (str, type(None)),
    "secondary_findings": list,
    "precedence_reason": str,
    "weaker_findings_suppressed": bool,
    "count_reconciliation": dict,
    "digest_ref_presence": dict,
    "orphan_row_count": int,
    "duplicate_binding_count": int,
    "tuple_mismatch_count": int,
    "gate_effect_drift_count": int,
    "gmUT_gate_effect": str,
    "mutation_performed": bool,
    "connector_write_performed": bool,
}
REQUIRED_COUNT_FIELDS = {
    "count_source_ref": str,
    "count_reconciliation_status": str,
    "canonical_row_count": int,
    "visualization_row_count": int,
    "visualization_ids_matching_canonical_ids": bool,
    "missing_visual_row_count": int,
    "orphan_visual_row_count": int,
    "duplicate_visual_row_count": int,
    "tuple_mismatch_count": int,
    "digest_mismatch_count": int,
    "missing_digest_ref_count": int,
    "gate_effect_drift_count": int,
}
REQUIRED_DIGEST_FIELDS = {
    "status": str,
    "identity_digest_ref_row_count": int,
    "content_digest_ref_row_count": int,
    "both_digest_ref_row_count": int,
    "missing_any_digest_ref_row_count": int,
}


def load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return data


def unwrap_report(payload: dict[str, Any]) -> dict[str, Any]:
    nested = payload.get("sanitized_report")
    if isinstance(nested, dict):
        return nested
    return payload


def list_len(report: dict[str, Any], key: str) -> int:
    value = report.get(key, [])
    return len(value) if isinstance(value, list) else -1


def is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0 and not isinstance(value, bool)


def expected_digest_status(report: dict[str, Any]) -> str:
    digest = report["digest_ref_presence"]
    missing = digest["missing_any_digest_ref_row_count"]
    both = digest["both_digest_ref_row_count"]
    visual_count = report["visualization_row_count"]
    if missing == 0 and both == visual_count:
        return "present"
    if missing > 0 and both == 0:
        return "missing"
    if missing > 0 and both > 0:
        return "partial"
    return "present"


def expected_report_status(report: dict[str, Any]) -> str:
    structural_blocker = any(
        [
            list_len(report, "duplicate_canonical_row_ids") > 0,
            list_len(report, "malformed_visual_rows") > 0,
            list_len(report, "duplicate_visual_row_ids") > 0,
            list_len(report, "orphan_visual_row_ids") > 0,
            list_len(report, "missing_visual_row_ids") > 0,
            list_len(report, "tuple_mismatches") > 0,
            report.get("gate_effect_drift_count", 0) > 0,
            bool(report.get("top_level_gate_effect_drift")),
        ]
    )
    digest_blocker = list_len(report, "digest_mismatch_row_ids") > 0
    open_gap = list_len(report, "missing_digest_ref_row_ids") > 0
    if structural_blocker or digest_blocker:
        return "FAIL_BLOCKER"
    if open_gap:
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def dominant_codes(report: dict[str, Any]) -> tuple[str | None, str | None]:
    failure_codes = report["failure_codes"]
    dominant_failure = next((code for code in BLOCKER_CODE_PRIORITY if code in failure_codes), None)
    if dominant_failure:
        return dominant_failure, dominant_failure
    if "MISSING_DIGEST_REF_OPEN_GAP" in failure_codes:
        return None, "MISSING_DIGEST_REF_OPEN_GAP"
    return None, None


def add_row(rows: list[dict[str, Any]], row_id: str, ok: bool, message: str, evidence: Any = None) -> None:
    rows.append(
        {
            "row_id": row_id,
            "status": "PASS_SHAPE_ONLY" if ok else "FAIL_BLOCKER",
            "message": message,
            "evidence": evidence,
        }
    )


def assert_report(report: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []

    missing_fields = sorted(field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in report)
    add_row(rows, "required_top_level_fields", not missing_fields, "required fields are present", missing_fields)
    if missing_fields:
        failures.extend(f"missing:{field}" for field in missing_fields)
        return rows, failures

    type_errors = []
    for field, expected_type in REQUIRED_TOP_LEVEL_FIELDS.items():
        if not isinstance(report[field], expected_type):
            type_errors.append(field)
    for field in ("orphan_row_count", "duplicate_binding_count", "tuple_mismatch_count", "gate_effect_drift_count"):
        if not is_non_negative_int(report[field]):
            type_errors.append(field)
    add_row(rows, "required_top_level_types", not type_errors, "required field types are constrained", type_errors)
    if type_errors:
        failures.extend(f"type:{field}" for field in type_errors)

    status_errors = []
    for field in ("aggregate_status", "structural_binding_status", "digest_evidence_status"):
        if report[field] not in ALLOWED_STATUSES:
            status_errors.append(field)
    add_row(rows, "status_enums", not status_errors, "status enum values are constrained", status_errors)
    if status_errors:
        failures.extend(f"status:{field}" for field in status_errors)

    boundary_ok = (
        report["report_mode"] == "local_non_mutating"
        and report["gmUT_gate_effect"] == "none_open_not_tested"
        and report["mutation_performed"] is False
        and report["connector_write_performed"] is False
    )
    add_row(
        rows,
        "local_non_mutating_boundary",
        boundary_ok,
        "report remains local, non-mutating, and no-GMUT-gate-effect",
        {
            "report_mode": report["report_mode"],
            "gmUT_gate_effect": report["gmUT_gate_effect"],
            "mutation_performed": report["mutation_performed"],
            "connector_write_performed": report["connector_write_performed"],
        },
    )
    if not boundary_ok:
        failures.append("boundary:local_non_mutating")

    precedence_ok = report["precedence_order"] == PRECEDENCE_ORDER
    add_row(rows, "precedence_order", precedence_ok, "status precedence order is explicit", report["precedence_order"])
    if not precedence_ok:
        failures.append("precedence:order")

    expected_status = expected_report_status(report)
    aggregate_ok = report["aggregate_status"] == expected_status
    add_row(
        rows,
        "aggregate_status_rederived",
        aggregate_ok,
        "aggregate status reconciles with detailed findings",
        {"expected": expected_status, "actual": report["aggregate_status"]},
    )
    if not aggregate_ok:
        failures.append("aggregate:status")

    expected_dominant_failure, expected_dominant_finding = dominant_codes(report)
    dominant_ok = (
        report["dominant_failure_code"] == expected_dominant_failure
        and report["dominant_finding_code"] == expected_dominant_finding
    )
    add_row(
        rows,
        "dominant_codes",
        dominant_ok,
        "dominant codes reconcile with failure code precedence",
        {
            "expected_failure": expected_dominant_failure,
            "actual_failure": report["dominant_failure_code"],
            "expected_finding": expected_dominant_finding,
            "actual_finding": report["dominant_finding_code"],
        },
    )
    if not dominant_ok:
        failures.append("dominant:codes")

    expected_secondary = [code for code in report["failure_codes"] if code != expected_dominant_finding]
    secondary_ok = report["secondary_findings"] == expected_secondary and report["weaker_findings_suppressed"] is False
    add_row(
        rows,
        "secondary_findings_retained",
        secondary_ok,
        "secondary findings are deterministic and not suppressed",
        {"expected": expected_secondary, "actual": report["secondary_findings"]},
    )
    if not secondary_ok:
        failures.append("secondary:retention")

    reason_ok = bool(report["precedence_reason"].strip())
    add_row(rows, "precedence_reason", reason_ok, "precedence reason is non-empty", report["precedence_reason"])
    if not reason_ok:
        failures.append("precedence:reason")

    count = report["count_reconciliation"]
    count_missing = sorted(field for field in REQUIRED_COUNT_FIELDS if field not in count)
    count_type_errors = []
    for field, expected_type in REQUIRED_COUNT_FIELDS.items():
        if field in count and not isinstance(count[field], expected_type):
            count_type_errors.append(field)
    for field in REQUIRED_COUNT_FIELDS:
        if field in count and expected_type_is_int(field) and not is_non_negative_int(count[field]):
            count_type_errors.append(field)
    count_shape_ok = not count_missing and not count_type_errors
    add_row(
        rows,
        "count_reconciliation_shape",
        count_shape_ok,
        "count reconciliation fields are present and typed",
        {"missing": count_missing, "type_errors": sorted(set(count_type_errors))},
    )
    if not count_shape_ok:
        failures.append("count:shape")

    if count_shape_ok:
        gate_detail_count = list_len(report, "gate_effect_drift_rows") + int(bool(report["top_level_gate_effect_drift"]))
        expected_count_status = "FAIL_BLOCKER" if expected_status == "FAIL_BLOCKER" and (
            list_len(report, "duplicate_canonical_row_ids") > 0
            or list_len(report, "malformed_visual_rows") > 0
            or list_len(report, "duplicate_visual_row_ids") > 0
            or list_len(report, "orphan_visual_row_ids") > 0
            or list_len(report, "missing_visual_row_ids") > 0
            or list_len(report, "tuple_mismatches") > 0
            or gate_detail_count > 0
            or list_len(report, "digest_mismatch_row_ids") > 0
        ) else "PASS_SHAPE_ONLY"
        count_mismatches = {
            "orphan_visual_row_count": [count["orphan_visual_row_count"], list_len(report, "orphan_visual_row_ids"), report["orphan_row_count"]],
            "duplicate_visual_row_count": [count["duplicate_visual_row_count"], list_len(report, "duplicate_visual_row_ids"), report["duplicate_binding_count"]],
            "tuple_mismatch_count": [count["tuple_mismatch_count"], list_len(report, "tuple_mismatches"), report["tuple_mismatch_count"]],
            "digest_mismatch_count": [count["digest_mismatch_count"], list_len(report, "digest_mismatch_row_ids")],
            "missing_digest_ref_count": [count["missing_digest_ref_count"], list_len(report, "missing_digest_ref_row_ids")],
            "missing_visual_row_count": [count["missing_visual_row_count"], list_len(report, "missing_visual_row_ids")],
            "gate_effect_drift_count": [count["gate_effect_drift_count"], gate_detail_count, report["gate_effect_drift_count"]],
        }
        count_values_ok = all(len(set(values)) == 1 for values in count_mismatches.values())
        count_values_ok = count_values_ok and count["count_source_ref"] == "canonical_report_and_visualization_input"
        count_values_ok = count_values_ok and count["count_reconciliation_status"] == expected_count_status
        add_row(
            rows,
            "row_to_summary_reconciliation",
            count_values_ok,
            "summary counters reconcile with detailed row finding lists",
            {
                "expected_count_reconciliation_status": expected_count_status,
                "actual_count_reconciliation_status": count["count_reconciliation_status"],
                "count_vectors": count_mismatches,
            },
        )
        if not count_values_ok:
            failures.append("count:detail_reconciliation")

    digest = report["digest_ref_presence"]
    digest_missing = sorted(field for field in REQUIRED_DIGEST_FIELDS if field not in digest)
    digest_type_errors = []
    for field, expected_type in REQUIRED_DIGEST_FIELDS.items():
        if field in digest and not isinstance(digest[field], expected_type):
            digest_type_errors.append(field)
    for field in REQUIRED_DIGEST_FIELDS:
        if field in digest and field != "status" and not is_non_negative_int(digest[field]):
            digest_type_errors.append(field)
    digest_shape_ok = not digest_missing and not digest_type_errors
    add_row(
        rows,
        "digest_ref_presence_shape",
        digest_shape_ok,
        "digest-reference presence fields are present and typed",
        {"missing": digest_missing, "type_errors": sorted(set(digest_type_errors))},
    )
    if not digest_shape_ok:
        failures.append("digest:shape")

    if digest_shape_ok:
        expected_status_name = expected_digest_status(report)
        digest_counts_ok = (
            digest["status"] == expected_status_name
            and digest["missing_any_digest_ref_row_count"] == list_len(report, "missing_digest_ref_row_ids")
            and digest["identity_digest_ref_row_count"] <= report["visualization_row_count"]
            and digest["content_digest_ref_row_count"] <= report["visualization_row_count"]
            and digest["both_digest_ref_row_count"] <= report["visualization_row_count"]
        )
        add_row(
            rows,
            "digest_ref_presence_rederived",
            digest_counts_ok,
            "digest-reference presence status and counts reconcile with row evidence",
            {"expected_status": expected_status_name, "actual_status": digest["status"]},
        )
        if not digest_counts_ok:
            failures.append("digest:presence_reconciliation")

    return rows, failures


def expected_type_is_int(field: str) -> bool:
    return REQUIRED_COUNT_FIELDS.get(field) is int


def main() -> int:
    parser = argparse.ArgumentParser(description="Assert a THOS visualization binding report contract.")
    parser.add_argument("--report", required=True, help="Visualization binding report JSON")
    parser.add_argument("--output", help="Optional assertion report path")
    args = parser.parse_args()

    raw = load_json(args.report)
    report = unwrap_report(raw)
    rows, failures = assert_report(report)
    assertion_status = "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY"
    output = {
        "validator_mode": "local_non_mutating_visualization_report_assertion",
        "report_mode": "local_non_mutating",
        "assertion_status": assertion_status,
        "aggregate_status": assertion_status,
        "report_input": Path(args.report).as_posix(),
        "observed_report_status": report.get("aggregate_status"),
        "assertion_failures": failures,
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
