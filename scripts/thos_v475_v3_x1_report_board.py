#!/usr/bin/env python3
"""Build v475 THOS v3 x1 dashboard report board artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v3-x1"
SOURCE_PHASE = "v475-thos-v2-x2"
NEXT_PHASE = "v475-thos-v3-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
AGGREGATOR = ARTIFACT_ROOT / "v475-thos-v2-x2-dashboard-sync-aggregator-v1.json"
AGGREGATOR_STATUS = ARTIFACT_ROOT / "v475-thos-v2-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REPORT_ROWS = [
    "lane_coverage",
    "raw_output_boundary",
    "source_hash_boundary",
    "label_policy",
    "fixture_summary",
    "claim_boundary",
    "handoff",
]


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


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_REPORT_BOARD_READY"


def report_board(aggregator: dict[str, Any]) -> list[dict[str, Any]]:
    dash = aggregator.get("dashboard_aggregation", {})
    fixtures = aggregator.get("fixtures", [])
    fixture_mismatches = [item for item in fixtures if item.get("status") != "EXPECTED_CONFIRMED"]
    missing_lanes = dash.get("missing_lanes", [])
    raw_flag_rows = dash.get("raw_flag_rows", [])
    source_hash_ref_gaps = dash.get("source_hash_ref_gaps", [])
    bad_labels = dash.get("bad_labels", [])
    return [
        {
            "board_row": "lane_coverage",
            "human_label": "Lane Coverage",
            "status": "PASS_SHAPE_ONLY" if not missing_lanes else "FAIL_LANE_COVERAGE",
            "summary": "Arby and Aster Vale lane rows are represented as metadata-only rows.",
            "evidence": {"missing_lanes": missing_lanes, "lane_count": dash.get("lane_count")},
        },
        {
            "board_row": "raw_output_boundary",
            "human_label": "Raw Output Boundary",
            "status": "PASS_SHAPE_ONLY" if not raw_flag_rows else "FAIL_RAW_OUTPUT_FLAG",
            "summary": "Raw-output and transport publication flags remain blocked.",
            "evidence": {"flagged_lanes": raw_flag_rows},
        },
        {
            "board_row": "source_hash_boundary",
            "human_label": "Source Hash Boundary",
            "status": "PASS_SHAPE_ONLY" if not source_hash_ref_gaps else "OPEN_GAP_SOURCE_HASH_REFS",
            "summary": "Source hashes are used for metadata integrity only, not content truth.",
            "evidence": {"gaps": source_hash_ref_gaps},
        },
        {
            "board_row": "label_policy",
            "human_label": "Label Policy",
            "status": "PASS_SHAPE_ONLY" if not bad_labels else "FAIL_LABEL_POLICY",
            "summary": "Dashboard labels remain metadata-status labels only.",
            "evidence": {"bad_label_lanes": bad_labels},
        },
        {
            "board_row": "fixture_summary",
            "human_label": "Fixture Summary",
            "status": "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "summary": "Negative fixtures confirm expected blocker and open-gap behavior.",
            "evidence": {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        },
        {
            "board_row": "claim_boundary",
            "human_label": "Claim Boundary",
            "status": "PASS_SHAPE_ONLY",
            "summary": "The board reports THOS metadata continuity only; all GMUT gates remain open.",
            "evidence": {"gmUT_gate_effect": "none_open_not_tested"},
        },
        {
            "board_row": "handoff",
            "human_label": "Handoff",
            "status": "PASS_SHAPE_ONLY",
            "summary": "v3 x2 should gate report-board publication readiness with source and label checks.",
            "evidence": {"next_expected_phase": NEXT_PHASE},
        },
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    aggregator = read_json(AGGREGATOR)
    aggregator_status = read_json(AGGREGATOR_STATUS)
    source_refs = [source_ref(AGGREGATOR), source_ref(AGGREGATOR_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    board = report_board(aggregator)
    missing_report_rows = sorted(set(REPORT_ROWS) - {item["board_row"] for item in board})
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v2 x2 aggregator sources were checked for the report board.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "report_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_report_rows else "OPEN_GAP_REPORT_ROWS",
            "Required report-board rows are present.",
            {"missing_report_rows": missing_report_rows},
        ),
        row(
            "board_status",
            "PASS_SHAPE_ONLY" if not any(item["status"].startswith("FAIL") for item in board) else "FAIL_BOARD_ROW",
            "Report-board rows preserve metadata-only status boundaries.",
            {"row_count": len(board)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase creates a report board only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows)
    payload = {
        "aggregate_status": status,
        "board": board,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_run_status": aggregator_status.get("run_status"),
        "v3_x2_acceptance_criteria": [
            "all report-board rows present",
            "no board row exposes raw output or transport",
            "source refs remain matched",
            "labels remain metadata-status only",
            "claim boundary remains THOS metadata continuity only",
        ],
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-report-board-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-report-board-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v3 x1 Report Board

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v3 x1 derives a dashboard-ready report board from the v2 x2 aggregator.

Board rows: `{len(board)}`; missing required rows: `{len(missing_report_rows)}`.

Source refs: `{len(source_refs)}` checked; gaps: `{len(source_gaps)}`.

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
            "report row coverage checked",
            "metadata-only board boundary checked",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v3 x1 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v3 x1 creates a dashboard-ready report board from the v2 x2 aggregator.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
