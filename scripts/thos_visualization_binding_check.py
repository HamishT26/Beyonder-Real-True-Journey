#!/usr/bin/env python3
"""Check THOS visualization rows against a canonical row-universe report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TUPLE_FIELDS = ("row_id", "family", "status", "surface", "source_row_id")


def load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return data


def normalize_rows(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise SystemExit("rows must be a list")
    return [row if isinstance(row, dict) else {"_non_object_row": row} for row in rows]


def check_binding(canonical_report: dict[str, Any], visualization: dict[str, Any]) -> dict[str, Any]:
    canonical_rows = normalize_rows(canonical_report.get("canonical_rows", []))
    visualization_rows = normalize_rows(visualization.get("rows", []))
    row_identity_digest = canonical_report.get("row_identity_digest")
    row_content_digest = canonical_report.get("row_content_digest")

    canonical_by_id: dict[str, dict[str, Any]] = {}
    duplicate_canonical_row_ids: list[str] = []
    for row in canonical_rows:
        row_id = row.get("row_id")
        if not isinstance(row_id, str) or not row_id:
            continue
        if row_id in canonical_by_id:
            duplicate_canonical_row_ids.append(row_id)
        canonical_by_id[row_id] = row

    visual_seen: set[str] = set()
    visual_ids: set[str] = set()
    malformed_visual_rows: list[int] = []
    duplicate_visual_row_ids: list[str] = []
    orphan_visual_row_ids: list[str] = []
    tuple_mismatches: list[dict[str, Any]] = []
    missing_digest_ref_row_ids: list[str] = []
    digest_mismatch_row_ids: list[dict[str, Any]] = []
    gate_effect_drift_rows: list[dict[str, Any]] = []
    identity_digest_ref_row_ids: list[str] = []
    content_digest_ref_row_ids: list[str] = []
    both_digest_ref_row_ids: list[str] = []

    def row_gate_effect(row: dict[str, Any]) -> Any:
        if "gmUT_gate_effect" in row:
            return row.get("gmUT_gate_effect")
        return row.get("gmut_gate_effect")

    for idx, row in enumerate(visualization_rows):
        row_id = row.get("row_id")
        if "_non_object_row" in row or not isinstance(row_id, str) or not row_id:
            malformed_visual_rows.append(idx)
            continue
        gate_effect = row_gate_effect(row)
        if gate_effect is not None and gate_effect != "none_open_not_tested":
            gate_effect_drift_rows.append({"row_id": row_id, "gmUT_gate_effect": gate_effect})
        if row_id in visual_seen:
            duplicate_visual_row_ids.append(row_id)
        visual_seen.add(row_id)
        visual_ids.add(row_id)

        canonical_row = canonical_by_id.get(row_id)
        if canonical_row is None:
            orphan_visual_row_ids.append(row_id)
            continue

        field_mismatches = []
        for field in TUPLE_FIELDS:
            if row.get(field) != canonical_row.get(field):
                field_mismatches.append(
                    {
                        "field": field,
                        "canonical": canonical_row.get(field),
                        "visualization": row.get(field),
                    }
                )
        if field_mismatches:
            tuple_mismatches.append({"row_id": row_id, "field_mismatches": field_mismatches})

        missing_digest_fields = []
        if "row_identity_digest" not in row:
            missing_digest_fields.append("row_identity_digest")
        elif row.get("row_identity_digest") != row_identity_digest:
            digest_mismatch_row_ids.append({"row_id": row_id, "field": "row_identity_digest"})
        else:
            identity_digest_ref_row_ids.append(row_id)
        if "row_content_digest" not in row:
            missing_digest_fields.append("row_content_digest")
        elif row.get("row_content_digest") != row_content_digest:
            digest_mismatch_row_ids.append({"row_id": row_id, "field": "row_content_digest"})
        else:
            content_digest_ref_row_ids.append(row_id)
        if not missing_digest_fields and row_id in identity_digest_ref_row_ids and row_id in content_digest_ref_row_ids:
            both_digest_ref_row_ids.append(row_id)
        if missing_digest_fields:
            missing_digest_ref_row_ids.append(row_id)

    missing_visual_row_ids = sorted(set(canonical_by_id) - visual_ids)
    top_level_gate_effect = visualization.get("gmUT_gate_effect", visualization.get("gmut_gate_effect"))
    top_level_gate_effect_drift = (
        top_level_gate_effect is not None and top_level_gate_effect != "none_open_not_tested"
    )
    structural_blocker_reasons = {
        "duplicate_canonical_row_ids": sorted(set(duplicate_canonical_row_ids)),
        "malformed_visual_rows": malformed_visual_rows,
        "duplicate_visual_row_ids": sorted(set(duplicate_visual_row_ids)),
        "orphan_visual_row_ids": sorted(set(orphan_visual_row_ids)),
        "missing_visual_row_ids": missing_visual_row_ids,
        "tuple_mismatches": tuple_mismatches,
        "gate_effect_drift_rows": gate_effect_drift_rows,
        "top_level_gate_effect_drift": top_level_gate_effect_drift,
    }
    digest_blocker_reasons = {
        "digest_mismatch_row_ids": digest_mismatch_row_ids,
    }
    has_structural_blocker = any(bool(value) for value in structural_blocker_reasons.values())
    has_digest_blocker = any(bool(value) for value in digest_blocker_reasons.values())
    has_open_gap = bool(missing_digest_ref_row_ids)
    if has_structural_blocker or has_digest_blocker:
        aggregate_status = "FAIL_BLOCKER"
    elif has_open_gap:
        aggregate_status = "OPEN_GAP"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    structural_binding_status = "FAIL_BLOCKER" if has_structural_blocker else "PASS_SHAPE_ONLY"
    if has_digest_blocker:
        digest_evidence_status = "FAIL_BLOCKER"
    elif has_open_gap:
        digest_evidence_status = "OPEN_GAP"
    else:
        digest_evidence_status = "PASS_SHAPE_ONLY"
    failure_codes = []
    if duplicate_canonical_row_ids:
        failure_codes.append("DUPLICATE_CANONICAL_ROW_ID")
    if malformed_visual_rows:
        failure_codes.append("MALFORMED_VISUALIZATION_ROW")
    if duplicate_visual_row_ids:
        failure_codes.append("DUPLICATE_VISUALIZATION_BINDING")
    if orphan_visual_row_ids:
        failure_codes.append("ORPHAN_VISUALIZATION_ROW")
    if missing_visual_row_ids:
        failure_codes.append("MISSING_CANONICAL_VISUALIZATION_ROW")
    if tuple_mismatches:
        failure_codes.append("TUPLE_MISMATCH")
    if gate_effect_drift_rows or top_level_gate_effect_drift:
        failure_codes.append("GMUT_GATE_EFFECT_DRIFT")
    if digest_mismatch_row_ids:
        failure_codes.append("DIGEST_MISMATCH")
    if missing_digest_ref_row_ids:
        failure_codes.append("MISSING_DIGEST_REF_OPEN_GAP")
    blocker_code_priority = [
        "DUPLICATE_CANONICAL_ROW_ID",
        "MALFORMED_VISUALIZATION_ROW",
        "DUPLICATE_VISUALIZATION_BINDING",
        "ORPHAN_VISUALIZATION_ROW",
        "MISSING_CANONICAL_VISUALIZATION_ROW",
        "TUPLE_MISMATCH",
        "GMUT_GATE_EFFECT_DRIFT",
        "DIGEST_MISMATCH",
    ]
    dominant_failure_code = next((code for code in blocker_code_priority if code in failure_codes), None)
    if dominant_failure_code:
        dominant_finding_code = dominant_failure_code
    elif has_open_gap:
        dominant_finding_code = "MISSING_DIGEST_REF_OPEN_GAP"
    else:
        dominant_finding_code = None
    secondary_findings = [code for code in failure_codes if code != dominant_finding_code]
    weaker_findings_suppressed = False
    if aggregate_status == "FAIL_BLOCKER" and has_open_gap:
        precedence_reason = f"{dominant_failure_code} dominates weaker digest-reference open gaps"
    elif aggregate_status == "FAIL_BLOCKER":
        precedence_reason = f"{dominant_failure_code} is a blocker-class finding"
    elif aggregate_status == "OPEN_GAP":
        precedence_reason = "structural binding passes but digest-reference evidence is incomplete"
    else:
        precedence_reason = "structural binding and digest-reference evidence pass shape"
    both_digest_ref_count = len(set(both_digest_ref_row_ids))
    missing_digest_ref_count = len(set(missing_digest_ref_row_ids))
    if both_digest_ref_count == len(visualization_rows) and missing_digest_ref_count == 0:
        digest_ref_presence_status = "present"
    elif both_digest_ref_count == 0 and missing_digest_ref_count > 0:
        digest_ref_presence_status = "missing"
    elif missing_digest_ref_count > 0:
        digest_ref_presence_status = "partial"
    else:
        digest_ref_presence_status = "present"
    count_reconciliation_status = (
        "FAIL_BLOCKER"
        if (
            duplicate_canonical_row_ids
            or malformed_visual_rows
            or duplicate_visual_row_ids
            or orphan_visual_row_ids
            or missing_visual_row_ids
            or tuple_mismatches
            or gate_effect_drift_rows
            or top_level_gate_effect_drift
            or digest_mismatch_row_ids
        )
        else "PASS_SHAPE_ONLY"
    )

    return {
        "validator_mode": "local_non_mutating_visualization_binding_check",
        "report_mode": "local_non_mutating",
        "aggregate_status": aggregate_status,
        "structural_binding_status": structural_binding_status,
        "digest_evidence_status": digest_evidence_status,
        "status_precedence": "FAIL_BLOCKER overrides OPEN_GAP; OPEN_GAP overrides PASS_SHAPE_ONLY",
        "precedence_order": [
            "FAIL_BLOCKER",
            "OPEN_GAP",
            "PASS_SHAPE_ONLY",
        ],
        "failure_codes": failure_codes,
        "dominant_failure_code": dominant_failure_code,
        "dominant_finding_code": dominant_finding_code,
        "secondary_findings": secondary_findings,
        "precedence_reason": precedence_reason,
        "weaker_findings_suppressed": weaker_findings_suppressed,
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "visualization_top_level_gate_effect": top_level_gate_effect,
        "top_level_gate_effect_drift": top_level_gate_effect_drift,
        "canonical_row_count": len(canonical_by_id),
        "visualization_row_count": len(visualization_rows),
        "row_identity_digest": row_identity_digest,
        "row_content_digest": row_content_digest,
        "tuple_fields": list(TUPLE_FIELDS),
        "count_reconciliation": {
            "count_source_ref": "canonical_report_and_visualization_input",
            "count_reconciliation_status": count_reconciliation_status,
            "canonical_row_count": len(canonical_by_id),
            "visualization_row_count": len(visualization_rows),
            "visualization_ids_matching_canonical_ids": sorted(visual_ids) == sorted(canonical_by_id),
            "missing_visual_row_count": len(missing_visual_row_ids),
            "orphan_visual_row_count": len(set(orphan_visual_row_ids)),
            "duplicate_visual_row_count": len(set(duplicate_visual_row_ids)),
            "tuple_mismatch_count": len(tuple_mismatches),
            "digest_mismatch_count": len(digest_mismatch_row_ids),
            "missing_digest_ref_count": len(set(missing_digest_ref_row_ids)),
            "gate_effect_drift_count": len(gate_effect_drift_rows) + int(top_level_gate_effect_drift),
        },
        "digest_ref_presence": {
            "status": digest_ref_presence_status,
            "identity_digest_ref_row_count": len(set(identity_digest_ref_row_ids)),
            "content_digest_ref_row_count": len(set(content_digest_ref_row_ids)),
            "both_digest_ref_row_count": both_digest_ref_count,
            "missing_any_digest_ref_row_count": missing_digest_ref_count,
        },
        "orphan_row_count": len(set(orphan_visual_row_ids)),
        "duplicate_binding_count": len(set(duplicate_visual_row_ids)),
        "tuple_mismatch_count": len(tuple_mismatches),
        "gate_effect_drift_count": len(gate_effect_drift_rows) + int(top_level_gate_effect_drift),
        **structural_blocker_reasons,
        **digest_blocker_reasons,
        "missing_digest_ref_row_ids": sorted(set(missing_digest_ref_row_ids)),
        "open_gap_reason": (
            "visualization rows match canonical tuples but do not yet carry digest refs"
            if has_open_gap and not (has_structural_blocker or has_digest_blocker)
            else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check visualization rows against canonical THOS rows.")
    parser.add_argument("--canonical-report", required=True, help="Canonical row-universe report JSON")
    parser.add_argument("--visualization-input", required=True, help="Visualization row JSON")
    parser.add_argument("--output", help="Optional report path")
    args = parser.parse_args()

    report = check_binding(
        load_json(args.canonical_report),
        load_json(args.visualization_input),
    )
    report["canonical_report"] = Path(args.canonical_report).as_posix()
    report["visualization_input"] = Path(args.visualization_input).as_posix()
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())
