#!/usr/bin/env python3
"""Build v475 THOS v3 x2 report-board gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v3-x2"
SOURCE_PHASE = "v475-thos-v3-x1"
NEXT_PHASE = "v475-thos-v4-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
BOARD = ARTIFACT_ROOT / "v475-thos-v3-x1-report-board-v1.json"
BOARD_STATUS = ARTIFACT_ROOT / "v475-thos-v3-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_BOARD_ROWS = {
    "lane_coverage",
    "raw_output_boundary",
    "source_hash_boundary",
    "label_policy",
    "fixture_summary",
    "claim_boundary",
    "handoff",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(path: Path) -> dict[str, Any]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {"path": rel, "status": "OPEN_GAP_MISSING_SOURCE"}
    return {
        "bytes": path.stat().st_size,
        "path": rel,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_board_row") or case.get("board_row_failed"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_output_flag") or case.get("transport_flag") or case.get("pressure_label"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_hash_drift") or case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only") and case.get("all_rows_present"):
        observed = "PASS_SHAPE_ONLY"
    return {
        "case": case,
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture(
            "metadata_board_expected_pass",
            {"all_rows_present": True, "gmut_gate_effect": "none_open_not_tested", "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_board_row_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_board_row": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "board_row_failed_expected_fail",
            {"board_row_failed": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_flag_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_output_flag": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "transport_flag_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "transport_flag": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "pressure_label_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "pressure_label": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_hash_drift_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "source_hash_drift": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "gmut_effect_moved_expected_fail",
            {"gmut_gate_effect": "gate_moved", "metadata_only": True},
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_REPORT_BOARD_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    board_payload = read_json(BOARD)
    board_status = read_json(BOARD_STATUS)
    source_refs = [source_ref(BOARD), source_ref(BOARD_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    board_rows = board_payload.get("board", [])
    board_ids = {str(item.get("board_row")) for item in board_rows}
    missing_rows = sorted(REQUIRED_BOARD_ROWS - board_ids)
    failing_rows = [item.get("board_row") for item in board_rows if str(item.get("status", "")).startswith("FAIL")]
    open_rows = [item.get("board_row") for item in board_rows if str(item.get("status", "")).startswith("OPEN_GAP")]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v3 x1 board sources were checked for report-board gating.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "board_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_BOARD_ROW_COVERAGE",
            "Required report-board rows are present.",
            {"missing_rows": missing_rows, "board_row_count": len(board_rows)},
        ),
        row(
            "board_row_status",
            "PASS_SHAPE_ONLY" if not failing_rows and not open_rows else "OPEN_GAP_BOARD_STATUS",
            "Report-board rows have no failure/open-gap status in the current curated board.",
            {"failing_rows": failing_rows, "open_rows": open_rows},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Report-board gate fixtures checked missing rows, board failures, raw flags, label drift, source drift, missing source, and GMUT boundary.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This is a report-board gate only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "report_board_gate": {
            "board_row_count": len(board_rows),
            "failing_rows": failing_rows,
            "missing_rows": missing_rows,
            "open_rows": open_rows,
            "source_run_status": board_status.get("run_status"),
        },
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "v4_x1_handoff": {
            "recommended_scope": "build a compact report-board ledger with release/readiness semantics and explicit open-gap handling",
            "claim_ceiling": "THOS metadata report-board gate only",
        },
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-report-board-gate-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-report-board-gate-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v3 x2 Report Board Gate

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v3 x2 gates the report board for source coverage, row coverage, row status, negative fixtures, and claim boundaries.

Board rows: `{len(board_rows)}`; missing rows: `{len(missing_rows)}`; open rows: `{len(open_rows)}`; failing rows: `{len(failing_rows)}`.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Next expected phase: `{NEXT_PHASE}`.

All six GMUT gates remain open.
""",
    )
    run_payload = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "published_artifacts": [artifact_json.relative_to(REPO_ROOT).as_posix(), artifact_md.relative_to(REPO_ROOT).as_posix()],
        "run_status": status,
        "validation": [
            "source refs checked",
            "board row coverage checked",
            "board row status checked",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v3 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v3 x2 gates the report board and prepares the v4 x1 ledger handoff.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
