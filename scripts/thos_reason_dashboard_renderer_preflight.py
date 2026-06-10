#!/usr/bin/env python3
"""Build a renderer-binding preflight from a compact THOS reason dashboard fixture."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RENDER_FIELDS = {
    "case_id": "case identifier label",
    "row_status": "status badge",
    "guard_status": "guard status badge",
    "guard_decision": "allow or deny lane",
    "observed_dominant_reason_code": "dominant reason label",
    "primary_selection_mode": "dominant reason selection label",
    "reason_codes": "full reason-code drawer",
    "expected_reason_codes": "required-code drawer",
    "matched_reason_codes": "matched required-code drawer",
    "missing_required_reason_codes": "missing required-code alert",
    "allowed_extra_reason_codes": "allowed extra-code drawer",
    "unexpected_extra_reason_codes": "unexpected extra-code alert",
    "matches_expected": "case reconciliation indicator",
}


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def row_projection(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "allowed_extra_count": len(row.get("allowed_extra_reason_codes") or []),
        "case_id": row.get("case_id"),
        "dominant_reason": row.get("observed_dominant_reason_code"),
        "guard_decision": row.get("guard_decision"),
        "guard_status": row.get("guard_status"),
        "matched_required_count": len(row.get("matched_reason_codes") or []),
        "missing_required_count": len(row.get("missing_required_reason_codes") or []),
        "reason_code_count": len(row.get("reason_codes") or []),
        "renderer_row_class": "blocked" if row.get("row_status") == "FAIL_BLOCKER" else "clean",
        "row_status": row.get("row_status"),
        "unexpected_extra_count": len(row.get("unexpected_extra_reason_codes") or []),
    }


def build_preflight(fixture: dict[str, Any], assertion: dict[str, Any], phase_slug: str) -> dict[str, Any]:
    fixture_rows = fixture.get("rows")
    if not isinstance(fixture_rows, list):
        fixture_rows = []
    missing_fields = {
        row.get("case_id", f"row_{index}"): sorted(field for field in RENDER_FIELDS if field not in row)
        for index, row in enumerate(fixture_rows)
        if isinstance(row, dict) and any(field not in row for field in RENDER_FIELDS)
    }
    malformed_rows = [
        index
        for index, row in enumerate(fixture_rows)
        if not isinstance(row, dict)
    ]
    assertion_status = assertion.get("assertion_status") or assertion.get("aggregate_status")
    fixture_status = fixture.get("aggregate_status")
    blockers: list[str] = []
    if assertion_status != "PASS_SHAPE_ONLY":
        blockers.append("fixture_assertion_not_green")
    if fixture_status != "PASS_SHAPE_ONLY":
        blockers.append("fixture_not_green")
    if missing_fields:
        blockers.append("renderer_fields_missing")
    if malformed_rows:
        blockers.append("malformed_fixture_rows")
    return {
        "aggregate_status": "FAIL_BLOCKER" if blockers else "PASS_SHAPE_ONLY",
        "blockers": blockers,
        "case_count": len(fixture_rows),
        "connector_write_performed": False,
        "fixture_assertion_status": assertion_status,
        "fixture_status": fixture_status,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "malformed_rows": malformed_rows,
        "missing_render_fields_by_case": missing_fields,
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rendered_artifact_created": False,
        "renderer_input_map": RENDER_FIELDS,
        "renderer_migration_status": "blocked_pending_rendered_artifact",
        "renderer_rows": [row_projection(row) for row in fixture_rows if isinstance(row, dict)],
        "validator_mode": "local_non_mutating_renderer_preflight",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a THOS reason dashboard renderer preflight.")
    parser.add_argument("--fixture", required=True, help="Compact reason dashboard fixture JSON path")
    parser.add_argument("--assertion", required=True, help="Compact fixture assertion JSON path")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    preflight = build_preflight(
        read_json_object(Path(args.fixture)),
        read_json_object(Path(args.assertion)),
        args.phase_slug,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(preflight, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(preflight, indent=2, sort_keys=True))
    return 0 if preflight["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
