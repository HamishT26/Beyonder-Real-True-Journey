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


def digest_for(row_ids: list[str]) -> str:
    canonical = "\n".join(sorted(row_ids)) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    duplicate_ids: list[str] = []
    missing_required: list[str] = []
    unknown_statuses: list[str] = []
    family_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    row_ids: list[str] = []

    for idx, row in enumerate(rows):
        row_id = row.get("row_id")
        family = row.get("family")
        status = row.get("status")
        if not isinstance(row_id, str) or not row_id:
            missing_required.append(f"row_{idx}:row_id")
            continue
        row_ids.append(row_id)
        if row_id in seen:
            duplicate_ids.append(row_id)
        seen.add(row_id)
        if not isinstance(family, str) or not family:
            missing_required.append(f"{row_id}:family")
        else:
            family_counts[family] = family_counts.get(family, 0) + 1
        if not isinstance(status, str) or not status:
            missing_required.append(f"{row_id}:status")
        elif status not in ALLOWED_STATUSES:
            unknown_statuses.append(f"{row_id}:{status}")
        else:
            status_counts[status] = status_counts.get(status, 0) + 1

    if duplicate_ids or missing_required or unknown_statuses:
        aggregate_status = "FAIL_BLOCKER"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "row_count": len(rows),
        "unique_row_count": len(seen),
        "row_universe_digest": digest_for(row_ids),
        "family_counts": family_counts,
        "status_counts": status_counts,
        "duplicate_row_ids": sorted(set(duplicate_ids)),
        "missing_required": missing_required,
        "unknown_statuses": unknown_statuses,
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
    typed_rows = [row for row in rows if isinstance(row, dict)]
    result = check_rows(typed_rows)
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
