#!/usr/bin/env python3
"""Build v476 THOS v1 x2 suite-map preflight artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v1-x2"
SOURCE_PHASE = "v476-thos-v1-x1"
NEXT_PHASE = "v476-thos-v2-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SUITE_MAP = ARTIFACT_ROOT / "v476-thos-v1-x1-suite-map-seed-v1.json"
SUITE_STATUS = ARTIFACT_ROOT / "v476-thos-v1-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_SURFACE_TYPES = [
    "api_surface",
    "command_surface",
    "dashboard_surface",
    "plugin_skill_surface",
    "receipt_surface",
    "script_surface",
    "skill_surface",
    "system_expansion_surface",
]

REQUIRED_ROWS = [
    "source_refs",
    "handoff_ready",
    "surface_counts",
    "candidate_counts",
    "materialization_boundary",
    "claim_boundary",
    "app_advisory_synthesis",
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
    if case.get("missing_source") or case.get("missing_surface") or case.get("candidate_count_low"):
        observed = "OPEN_GAP"
    elif case.get("raw_material") or case.get("installed_candidate") or case.get("broad_stage") or case.get("missing_required_row"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("preflight_ready") and case.get("candidate_only"):
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
            "preflight_ready_expected_pass",
            {"candidate_only": True, "gmut_gate_effect": "none_open_not_tested", "preflight_ready": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "missing_surface_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_surface": True},
            "OPEN_GAP",
        ),
        fixture(
            "candidate_count_low_expected_open_gap",
            {"candidate_count_low": True, "gmut_gate_effect": "none_open_not_tested"},
            "OPEN_GAP",
        ),
        fixture(
            "missing_required_row_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_required_row": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_material_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_material": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "installed_candidate_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "installed_candidate": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "broad_stage_expected_fail",
            {"broad_stage": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_gate_move_expected_fail",
            {"candidate_only": True, "gmut_gate_effect": "gate_moved", "preflight_ready": True},
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_V476_SUITE_MAP_PREFLIGHT_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    suite = read_json(SUITE_MAP)
    suite_status = read_json(SUITE_STATUS)
    source_refs = [source_ref(SUITE_MAP), source_ref(SUITE_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    surface_rows = suite.get("surface_rows", [])
    present_surface_types = sorted({item.get("surface_type") for item in surface_rows if item.get("surface_type")})
    missing_surface_types = sorted(set(REQUIRED_SURFACE_TYPES) - set(present_surface_types))
    row_ids = sorted({item.get("row_id") for item in suite.get("rows", []) if item.get("row_id")})
    missing_rows = sorted(set(REQUIRED_ROWS) - set(row_ids))
    candidate_totals = suite.get("candidate_totals", {})
    candidate_gaps = {key: value for key, value in candidate_totals.items() if value < 30}
    all_candidates = (
        suite.get("system_expansion_candidates", [])
        + suite.get("command_candidates", [])
        + suite.get("skill_candidates", [])
    )
    installed_now = [item for item in all_candidates if item.get("materialization_state") != "candidate_only_not_installed"]
    advisory_count = len(suite.get("app_advisory_synthesis", []))
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 x1 suite-map seed and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "suite_status",
            "PASS_SHAPE_ONLY" if suite.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_SUITE_MAP_SEED_READY" else "OPEN_GAP_SUITE_MAP_NOT_READY",
            "Suite-map seed must be ready before preflight.",
            {"suite_status": suite.get("aggregate_status"), "run_status": suite_status.get("aggregate_status")},
        ),
        row(
            "required_rows",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_REQUIRED_ROW_COVERAGE",
            "Required v476 x1 row IDs must be present.",
            {"missing_rows": missing_rows, "required_rows": REQUIRED_ROWS},
        ),
        row(
            "surface_family_coverage",
            "PASS_SHAPE_ONLY" if not missing_surface_types else "OPEN_GAP_SURFACE_FAMILY_COVERAGE",
            "Required THOS surface families must be represented.",
            {"missing_surface_types": missing_surface_types, "present_surface_types": present_surface_types},
        ),
        row(
            "candidate_counts",
            "PASS_SHAPE_ONLY" if not candidate_gaps else "OPEN_GAP_CANDIDATE_COUNTS",
            "Candidate counts must stay at or above 30 each.",
            {"candidate_gaps": candidate_gaps, "candidate_totals": candidate_totals},
        ),
        row(
            "candidate_materialization",
            "PASS_SHAPE_ONLY" if not installed_now else "FAIL_CANDIDATE_INSTALLED",
            "v476 x1 candidates must remain planning-only.",
            {"installed_now_count": len(installed_now), "total_candidates": len(all_candidates)},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY" if advisory_count == 3 else "OPEN_GAP_APP_ADVISORY_COUNT",
            "Cicero, Kierkegaard, and Aristotle advisory syntheses should be present.",
            {"advisory_count": advisory_count},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Preflight does not install candidates, mutate connectors, publish transport, or move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    preflight = {
        "aggregate_status": aggregate,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
        "required_rows": REQUIRED_ROWS,
        "required_surface_types": REQUIRED_SURFACE_TYPES,
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
    preflight_json = ARTIFACT_ROOT / f"{PHASE}-suite-map-preflight-v1.json"
    write_json(preflight_json, preflight)
    written.append(preflight_json)
    preflight_md = ARTIFACT_ROOT / f"{PHASE}-suite-map-preflight-v1.md"
    write_md(
        preflight_md,
        f"""
# v476 THOS v1 x2 Suite-Map Preflight

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The preflight checks the v476 x1 suite-map seed for source hashes, required rows, surface-family coverage, 30/30/30 candidate counts, candidate-only materialization, app advisory synthesis, and GMUT-open boundaries.

Required rows missing: `{len(missing_rows)}`
Surface families missing: `{len(missing_surface_types)}`
Candidate gaps: `{len(candidate_gaps)}`
Installed candidates now: `{len(installed_now)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(preflight_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v476 THOS v1 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v476 v1 x2 preflights the metadata-only suite-map seed. It keeps expansion, command, and skill candidates planning-only.

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
