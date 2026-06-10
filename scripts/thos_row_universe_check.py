#!/usr/bin/env python3
"""Check THOS row-universe identity and digest discipline."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"PASS_SHAPE_ONLY", "FAIL_BLOCKER", "OPEN_GAP", "NOT_RUN"}
CANONICAL_FIELDS = ("row_id", "family", "status", "surface", "source_row_id")


def digest_for(row_ids: list[str]) -> str:
    canonical = "\n".join(sorted(row_ids)) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def rich_digest_for(rows: list[dict[str, str]]) -> str:
    canonical_rows = []
    for row in sorted(rows, key=lambda item: item["row_id"]):
        canonical_rows.append({field: row[field] for field in CANONICAL_FIELDS})
    canonical = "\n".join(
        json.dumps(row, separators=(",", ":"), sort_keys=True) for row in canonical_rows
    ) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_rows(rows: list[Any]) -> dict[str, Any]:
    seen: set[str] = set()
    duplicate_ids: list[str] = []
    family_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    row_ids: list[str] = []
    canonical_rows: list[dict[str, str]] = []
    rejected_rows: list[dict[str, Any]] = []
    rejected_counts_by_reason: dict[str, int] = {}

    def reject(idx: int, row_id: str | None, reasons: list[str], row: Any) -> None:
        for reason in reasons:
            rejected_counts_by_reason[reason] = rejected_counts_by_reason.get(reason, 0) + 1
        rejected_rows.append(
            {
                "index": idx,
                "row_id": row_id,
                "reasons": reasons,
                "row_type": type(row).__name__,
            }
        )

    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            reject(idx, None, ["non_object_row"], row)
            continue
        row_id = row.get("row_id")
        family = row.get("family")
        status = row.get("status")
        surface = row.get("surface")
        source_row_id = row.get("source_row_id")
        rejection_reasons: list[str] = []
        if not isinstance(row_id, str) or not row_id:
            reject(idx, None, ["missing_required:row_id"], row)
            continue
        if row_id in seen:
            rejection_reasons.append("duplicate_row_id")
            duplicate_ids.append(row_id)
        seen.add(row_id)
        if not isinstance(family, str) or not family:
            rejection_reasons.append("missing_required:family")
        if not isinstance(status, str) or not status:
            rejection_reasons.append("missing_required:status")
        elif status not in ALLOWED_STATUSES:
            rejection_reasons.append("unknown_status")
        if not isinstance(surface, str) or not surface:
            rejection_reasons.append("missing_required:surface")
        if not isinstance(source_row_id, str) or not source_row_id:
            rejection_reasons.append("missing_required:source_row_id")
        if rejection_reasons:
            reject(idx, row_id, rejection_reasons, row)
            continue
        canonical_row = {
            "row_id": row_id,
            "family": family,
            "status": status,
            "surface": surface,
            "source_row_id": source_row_id,
        }
        canonical_rows.append(canonical_row)
        row_ids.append(row_id)
        family_counts[family] = family_counts.get(family, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    if rejected_rows:
        aggregate_status = "FAIL_BLOCKER"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    source_row_count = len(rows)
    canonical_row_count = len(canonical_rows)
    rejected_row_count = len(rejected_rows)
    return {
        "aggregate_status": aggregate_status,
        "row_count": source_row_count,
        "source_row_count": source_row_count,
        "object_row_count": sum(1 for row in rows if isinstance(row, dict)),
        "canonical_row_count": canonical_row_count,
        "rejected_row_count": rejected_row_count,
        "unique_row_count": len(set(row_ids)),
        "row_universe_digest": digest_for(row_ids),
        "row_identity_digest": digest_for(row_ids),
        "rich_row_universe_digest": rich_digest_for(canonical_rows),
        "row_content_digest": rich_digest_for(canonical_rows),
        "digest_versions": {
            "row_identity_digest": {
                "version": "row_id_membership_v1",
                "algorithm": "sha256_lf_join_sorted_row_ids",
            },
            "row_content_digest": {
                "version": "canonical_tuple_v2",
                "algorithm": "sha256_lf_join_sorted_json_canonical_tuples",
            },
        },
        "digest_fields": list(CANONICAL_FIELDS),
        "normalization_policy": {
            "field_order": list(CANONICAL_FIELDS),
            "string_case": "case_sensitive",
            "whitespace": "preserved_after_json_parse",
            "missing_or_blank": "reject_row",
            "unknown_status": "reject_row",
            "duplicate_row_id": "reject_duplicate_row",
        },
        "family_counts": family_counts,
        "status_counts": status_counts,
        "duplicate_row_ids": sorted(set(duplicate_ids)),
        "rejected_counts_by_reason": rejected_counts_by_reason,
        "rejected_rows": rejected_rows,
        "count_reconciliation": {
            "source_row_count": source_row_count,
            "canonical_row_count": canonical_row_count,
            "rejected_row_count": rejected_row_count,
            "visualization_row_count": source_row_count,
            "accepted_plus_rejected_equals_source": (
                canonical_row_count + rejected_row_count == source_row_count
            ),
        },
        "canonical_rows": canonical_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check THOS row-universe identity and digest discipline.")
    parser.add_argument("--input", required=True, help="Row-universe JSON file")
    parser.add_argument("--output", help="Optional JSON report path to write")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = data.get("rows", [])
    if not isinstance(rows, list):
        raise SystemExit("rows must be a list")
    result = check_rows(rows)
    report = {
        "validator_mode": "local_non_mutating_row_universe_check",
        "input_file": Path(args.input).as_posix(),
        "row_universe_id": data.get("row_universe_id"),
        "aggregate_status": result["aggregate_status"],
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        **result,
    }
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())
