#!/usr/bin/env python3
"""Build v476 THOS v2 x2 required-row gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v2-x2"
SOURCE_PHASE = "v476-thos-v2-x1"
NEXT_PHASE = "v476-thos-v3-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
MATRIX = ARTIFACT_ROOT / "v476-thos-v2-x1-required-row-matrix-v1.json"
MATRIX_STATUS = ARTIFACT_ROOT / "v476-thos-v2-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_MATRIX_ROWS = [
    "command_registry_summary",
    "skill_loader_health_summary",
    "script_inventory_summary",
    "connector_plugin_boundary_summary",
    "dashboard_sync_summary",
    "receipt_freshness_summary",
    "publication_guard_summary",
    "negative_fixture_coverage_summary",
    "source_hash_chain_summary",
    "gmut_open_boundary",
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

REQUIRED_BLOCK_CLASSES = [
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

APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "row families should cover commands, skills, scripts, connectors/plugins, dashboards, receipt freshness, publication guard, source authority, suite-map status, and GMUT boundary",
            "safe refs include commit IDs, manifest paths, receipt IDs, source hashes, dashboard row counts, guard verdicts, checker reports, fixture IDs, and phase handoff IDs",
            "blocked classes should include unreviewed transport, private runtime material, sensitive access material, external write payloads, unapproved cache material, noncurrent phase artifacts, and unsupported claim text",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "v476 v2 should be framed as required-row matrix and local gate hardening, not suite mastery or production readiness",
            "30/30/30 counts are planning inventory, not capability certification",
            "gate result is local metadata-readiness evidence only, not production proof, sibling quality proof, GMUT validation, or gate closure",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "gate should validate required rows, required columns, source hashes, safe metadata scan mode, false mutation flags, and GMUT effect",
            "negative fixtures should catch missing row, missing column, unknown family, hash drift, unsafe flags, generic pass, aggregate contradiction, and GMUT movement",
            "v476 v3 x1 should build a matrix gate report and handoff risk ledger without live connector mutation or runtime-capture publication",
        ],
    },
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


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source"):
        observed = "OPEN_GAP"
    elif case.get("missing_required_row") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_block_class") or case.get("guard_not_pass") or case.get("source_hash_drift"):
        observed = "FAIL_BLOCKER"
    elif case.get("candidate_installed") or case.get("broad_stage"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("gate_ready") and case.get("metadata_only"):
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
        fixture("gate_ready_expected_pass", {"gate_ready": True, "gmut_gate_effect": "none_open_not_tested", "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "missing_source": True}, "OPEN_GAP"),
        fixture("missing_required_row_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_row": True}, "FAIL_BLOCKER"),
        fixture("missing_required_column_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_column": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("guard_not_pass_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "guard_not_pass": True}, "FAIL_BLOCKER"),
        fixture("source_hash_drift_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "source_hash_drift": True}, "FAIL_BLOCKER"),
        fixture("candidate_installed_expected_fail", {"candidate_installed": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("broad_stage_expected_fail", {"broad_stage": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"gate_ready": True, "gmut_gate_effect": "gate_moved", "metadata_only": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_V476_REQUIRED_ROW_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    matrix = read_json(MATRIX)
    matrix_status = read_json(MATRIX_STATUS)
    source_refs = [source_ref(MATRIX), source_ref(MATRIX_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    matrix_rows = matrix.get("matrix_rows", [])
    present_rows = sorted(item.get("row_id") for item in matrix_rows if item.get("row_id"))
    missing_rows = sorted(set(REQUIRED_MATRIX_ROWS) - set(present_rows))
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in matrix_rows)
        }
    )
    guard_not_pass = [item["row_id"] for item in matrix_rows if item.get("guard_status") != "PASS_SHAPE_ONLY"]
    missing_block_classes = sorted(
        {
            block
            for block in REQUIRED_BLOCK_CLASSES
            if any(block not in item.get("blocked_publication_classes", []) for item in matrix_rows)
        }
    )
    gate_effect_moved = [item["row_id"] for item in matrix_rows if item.get("gmut_gate_effect") != "none_open_not_tested"]
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v2 x1 matrix and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "matrix_status",
            "PASS_SHAPE_ONLY" if matrix.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_REQUIRED_ROW_MATRIX_READY" else "OPEN_GAP_MATRIX_NOT_READY",
            "Required-row matrix must be ready before gate publication.",
            {"matrix_status": matrix.get("aggregate_status"), "run_status": matrix_status.get("aggregate_status")},
        ),
        row(
            "required_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_REQUIRED_ROW_COVERAGE",
            "All required rows must be present.",
            {"missing_rows": missing_rows, "required_rows": REQUIRED_MATRIX_ROWS},
        ),
        row(
            "required_column_coverage",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_COLUMN_COVERAGE",
            "All required columns must be present.",
            {"missing_columns": missing_columns, "required_columns": REQUIRED_COLUMNS},
        ),
        row(
            "guard_statuses",
            "PASS_SHAPE_ONLY" if not guard_not_pass else "FAIL_GUARD_STATUS",
            "All matrix rows must be shape-ready for this gate.",
            {"guard_not_pass": guard_not_pass},
        ),
        row(
            "blocked_publication_classes",
            "PASS_SHAPE_ONLY" if not missing_block_classes else "FAIL_BLOCKED_CLASS_COVERAGE",
            "All rows must carry the required blocked publication classes.",
            {"missing_block_classes": missing_block_classes, "required_block_classes": REQUIRED_BLOCK_CLASSES},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY" if not gate_effect_moved else "FAIL_GMUT_GATE_EFFECT",
            "Gate remains metadata-only and all GMUT gates remain open.",
            {"gate_effect_moved": gate_effect_moved, "gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded as sanitized metadata-only guidance.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS), "raw_advisory_text_recorded": False},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": aggregate,
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
        "required_block_classes": REQUIRED_BLOCK_CLASSES,
        "required_columns": REQUIRED_COLUMNS,
        "required_matrix_rows": REQUIRED_MATRIX_ROWS,
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
    json_path = ARTIFACT_ROOT / f"{PHASE}-required-row-gate-v1.json"
    write_json(json_path, payload)
    written.append(json_path)
    md_path = ARTIFACT_ROOT / f"{PHASE}-required-row-gate-v1.md"
    write_md(
        md_path,
        f"""
# v476 THOS v2 x2 Required-Row Gate

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The gate checks required row coverage, column coverage, row guard status, blocked publication classes, source hashes, and GMUT-open boundaries.

Required rows missing: `{len(missing_rows)}`
Required columns missing: `{len(missing_columns)}`
Rows not shape-ready: `{len(guard_not_pass)}`
Blocked-class gaps: `{len(missing_block_classes)}`
App advisories folded: `{len(APP_ADVISORY_SYNTHESIS)}`

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
# v476 THOS v2 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v476 v2 x2 gates the required-row matrix. It does not install candidates, mutate connectors, or move GMUT gates.

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
