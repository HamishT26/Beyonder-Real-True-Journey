#!/usr/bin/env python3
"""Build v476 THOS v2 x1 required-row matrix artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v2-x1"
SOURCE_PHASE = "v476-thos-v1-x2"
NEXT_PHASE = "v476-thos-v2-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SUITE_MAP = ARTIFACT_ROOT / "v476-thos-v1-x1-suite-map-seed-v1.json"
PREFLIGHT = ARTIFACT_ROOT / "v476-thos-v1-x2-suite-map-preflight-v1.json"
PREFLIGHT_STATUS = ARTIFACT_ROOT / "v476-thos-v1-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_MATRIX_ROWS = [
    ("command_registry_summary", "command_surface", "command_books"),
    ("skill_loader_health_summary", "skill_surface", "user_skill_manifests"),
    ("script_inventory_summary", "script_surface", "repo_scripts"),
    ("connector_plugin_boundary_summary", "plugin_skill_surface", "plugin_skill_manifests"),
    ("dashboard_sync_summary", "dashboard_surface", "dashboard_data_files"),
    ("receipt_freshness_summary", "receipt_surface", "trinity_live_traces"),
    ("publication_guard_summary", "receipt_surface", "trinity_live_traces"),
    ("negative_fixture_coverage_summary", "receipt_surface", "trinity_live_traces"),
    ("source_hash_chain_summary", "receipt_surface", "trinity_live_traces"),
    ("gmut_open_boundary", "gmut_boundary", "gmut_gates_open"),
]

REQUIRED_COLUMNS = [
    "row_id",
    "surface_family",
    "source_ref",
    "source_status",
    "freshness_status",
    "guard_status",
    "claim_ceiling",
    "blocked_publication_classes",
    "next_action",
    "gmut_gate_effect",
]

BLOCKED_PUBLICATION_CLASSES = [
    "runtime_capture_publication",
    "transport_body_publication",
    "private_material_publication",
    "unapproved_connector_write",
    "destructive_cleanup",
    "candidate_installation_without_preflight",
    "production_readiness_claim",
    "gmut_validation_claim",
    "canon_promotion_claim",
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


def matrix_row(row_id: str, surface_family: str, source_key: str, suite: dict[str, Any]) -> dict[str, Any]:
    counts = suite.get("surface_counts", {})
    source_status = "PASS_SHAPE_ONLY" if source_key == "gmut_gates_open" or counts.get(source_key, 0) > 0 else "OPEN_GAP_SOURCE_EMPTY"
    freshness_status = "CURRENT_PHASE_METADATA" if source_status == "PASS_SHAPE_ONLY" else "OPEN_GAP_FRESHNESS_UNKNOWN"
    return {
        "blocked_publication_classes": BLOCKED_PUBLICATION_CLASSES,
        "claim_ceiling": "metadata matrix row only; no runtime authority or proof claim",
        "freshness_status": freshness_status,
        "gmut_gate_effect": "none_open_not_tested",
        "guard_status": "PASS_SHAPE_ONLY" if source_status == "PASS_SHAPE_ONLY" else "OPEN_GAP",
        "next_action": "gate required row and column coverage in v476-thos-v2-x2",
        "row_id": row_id,
        "source_ref": source_key,
        "source_status": source_status,
        "surface_family": surface_family,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("freshness_unknown"):
        observed = "OPEN_GAP"
    elif case.get("missing_required_row") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("blocked_class_absent") or case.get("candidate_installed") or case.get("broad_stage"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("matrix_ready") and case.get("metadata_only"):
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
        fixture("matrix_ready_expected_pass", {"gmut_gate_effect": "none_open_not_tested", "matrix_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "missing_source": True}, "OPEN_GAP"),
        fixture("freshness_unknown_expected_open_gap", {"freshness_unknown": True, "gmut_gate_effect": "none_open_not_tested"}, "OPEN_GAP"),
        fixture("missing_required_row_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_row": True}, "FAIL_BLOCKER"),
        fixture("missing_required_column_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_column": True}, "FAIL_BLOCKER"),
        fixture("blocked_class_absent_expected_fail", {"blocked_class_absent": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("candidate_installed_expected_fail", {"candidate_installed": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("broad_stage_expected_fail", {"broad_stage": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"gmut_gate_effect": "gate_moved", "matrix_ready": True, "metadata_only": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_V476_REQUIRED_ROW_MATRIX_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    suite = read_json(SUITE_MAP)
    preflight = read_json(PREFLIGHT)
    preflight_status = read_json(PREFLIGHT_STATUS)
    source_refs = [source_ref(SUITE_MAP), source_ref(PREFLIGHT), source_ref(PREFLIGHT_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    matrix = [matrix_row(row_id, family, source_key, suite) for row_id, family, source_key in REQUIRED_MATRIX_ROWS]
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in matrix)
        }
    )
    missing_rows = sorted(set(row_id for row_id, _family, _source in REQUIRED_MATRIX_ROWS) - {item["row_id"] for item in matrix})
    open_gap_rows = [item["row_id"] for item in matrix if item["guard_status"] == "OPEN_GAP"]
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v1 suite-map and preflight sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "preflight_ready",
            "PASS_SHAPE_ONLY" if preflight.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_SUITE_MAP_PREFLIGHT_READY" else "OPEN_GAP_PREFLIGHT_NOT_READY",
            "v476 v1 x2 preflight must be ready before matrix hardening.",
            {"preflight_status": preflight.get("aggregate_status"), "run_status": preflight_status.get("aggregate_status")},
        ),
        row(
            "required_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_REQUIRED_ROW_COVERAGE",
            "All required matrix rows are present.",
            {"missing_rows": missing_rows, "required_row_count": len(REQUIRED_MATRIX_ROWS)},
        ),
        row(
            "required_column_coverage",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_COLUMN_COVERAGE",
            "All required columns are present on every matrix row.",
            {"missing_columns": missing_columns, "required_column_count": len(REQUIRED_COLUMNS)},
        ),
        row(
            "matrix_guard_states",
            "PASS_SHAPE_ONLY" if not open_gap_rows else "OPEN_GAP_MATRIX_GUARD_STATES",
            "Matrix row guard states are shape-ready or explicitly open.",
            {"open_gap_rows": open_gap_rows},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Required-row matrix remains metadata-only and does not move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": aggregate,
        "blocked_publication_classes": BLOCKED_PUBLICATION_CLASSES,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "matrix_rows": matrix,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "required_columns": REQUIRED_COLUMNS,
        "required_matrix_rows": [row_id for row_id, _family, _source in REQUIRED_MATRIX_ROWS],
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }
    written: list[Path] = []
    json_path = ARTIFACT_ROOT / f"{PHASE}-required-row-matrix-v1.json"
    write_json(json_path, payload)
    written.append(json_path)
    md_path = ARTIFACT_ROOT / f"{PHASE}-required-row-matrix-v1.md"
    write_md(
        md_path,
        f"""
# v476 THOS v2 x1 Required-Row Matrix

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The required-row matrix hardens the v476 suite-map into explicit rows for command, skill, script, plugin, dashboard, receipt, publication, fixture, source-hash, and GMUT-boundary coverage.

Matrix rows: `{len(matrix)}`
Required columns: `{len(REQUIRED_COLUMNS)}`
Open-gap rows: `{len(open_gap_rows)}`
Blocked publication classes: `{len(BLOCKED_PUBLICATION_CLASSES)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(md_path)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v476 THOS v2 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v476 v2 x1 creates a metadata-only required-row matrix. It does not install candidates, mutate connectors, or move GMUT gates.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    for path in build_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
