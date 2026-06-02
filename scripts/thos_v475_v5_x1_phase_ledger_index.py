#!/usr/bin/env python3
"""Build v475 THOS v5 x1 phase ledger index artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v5-x1"
SOURCE_PHASE = "v475-thos-v4-x2"
NEXT_PHASE = "v475-thos-v5-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

V4_LEDGER = ARTIFACT_ROOT / "v475-thos-v4-x1-release-readiness-ledger-v1.json"
V4_GATE = ARTIFACT_ROOT / "v475-thos-v4-x2-release-readiness-gate-v1.json"
V4_GATE_STATUS = ARTIFACT_ROOT / "v475-thos-v4-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_INDEX_COLUMNS = [
    "phase_ref",
    "artifact_ref",
    "readiness_state",
    "source_authority_state",
    "open_gap_state",
    "raw_output_state",
    "claim_ceiling",
    "next_action",
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
    if case.get("missing_required_column") or case.get("missing_claim_ceiling"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_output") or case.get("source_as_proof") or case.get("production_claim"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("open_gap"):
        observed = "OPEN_GAP"
    elif case.get("index_ready") and case.get("metadata_only"):
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
            "metadata_index_expected_pass",
            {"gmut_gate_effect": "none_open_not_tested", "index_ready": True, "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_required_column_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_required_column": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_claim_ceiling_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_claim_ceiling": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_as_proof_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "source_as_proof": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "production_claim_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "production_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_output": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "open_gap_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "open_gap": True},
            "OPEN_GAP",
        ),
        fixture(
            "gmut_effect_moved_expected_fail",
            {"gmut_gate_effect": "gate_moved", "index_ready": True},
            "FAIL_BLOCKER",
        ),
    ]


def build_index_rows(ledger: dict[str, Any], gate: dict[str, Any]) -> list[dict[str, Any]]:
    external_sources = ledger.get("external_source_refs", [])
    release_gate = gate.get("release_readiness_gate", {})
    return [
        {
            "artifact_ref": "v475-thos-v4-x1-release-readiness-ledger-v1.json",
            "claim_ceiling": "THOS release/readiness metadata only",
            "next_action": "gate ledger row coverage and source ceilings",
            "open_gap_state": "explicit_open_gap_column_present",
            "phase_ref": "v475-thos-v4-x1",
            "raw_output_state": "blocked_unpublished",
            "readiness_state": ledger.get("aggregate_status"),
            "source_authority_state": f"{len(external_sources)} official context refs recorded",
        },
        {
            "artifact_ref": "v475-thos-v4-x2-release-readiness-gate-v1.json",
            "claim_ceiling": "THOS release/readiness metadata only",
            "next_action": "build operator-facing phase ledger index gate",
            "open_gap_state": "explicit_open_gap_column_present",
            "phase_ref": "v475-thos-v4-x2",
            "raw_output_state": "blocked_unpublished",
            "readiness_state": gate.get("aggregate_status"),
            "source_authority_state": f"{release_gate.get('official_source_count', 0)} official context refs gated",
        },
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_PHASE_LEDGER_INDEX_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    ledger = read_json(V4_LEDGER)
    gate = read_json(V4_GATE)
    gate_status = read_json(V4_GATE_STATUS)
    source_refs = [source_ref(V4_LEDGER), source_ref(V4_GATE), source_ref(V4_GATE_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    index_rows = build_index_rows(ledger, gate)
    missing_columns = [
        column
        for column in REQUIRED_INDEX_COLUMNS
        if any(column not in index_row for index_row in index_rows)
    ]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v4 release/readiness sources were checked for the phase ledger index.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "index_column_coverage",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_INDEX_COLUMN_COVERAGE",
            "Required phase ledger index columns are present.",
            {"missing_columns": missing_columns, "required_columns": REQUIRED_INDEX_COLUMNS},
        ),
        row(
            "index_row_coverage",
            "PASS_SHAPE_ONLY" if len(index_rows) == 2 else "FAIL_INDEX_ROW_COVERAGE",
            "v4 x1 and v4 x2 are represented as ledger index rows.",
            {"index_row_count": len(index_rows)},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Index fixtures checked columns, claim ceilings, source-proof overclaim, production overclaim, raw output, open gaps, and GMUT boundary.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This is a THOS phase ledger index only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "index_rows": index_rows,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "required_index_columns": REQUIRED_INDEX_COLUMNS,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_run_status": gate_status.get("run_status"),
        "v5_x2_acceptance_criteria": [
            "index rows cover v4 x1 and v4 x2",
            "required columns are present",
            "source authority remains context only",
            "open gaps remain explicit",
            "raw-output and claim-expansion blockers remain active",
        ],
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-phase-ledger-index-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-phase-ledger-index-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v5 x1 Phase Ledger Index

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v5 x1 creates an operator-facing phase ledger index over v4 x1/x2, with source authority, open-gap, raw-output, and claim-ceiling columns.

Index rows: `{len(index_rows)}`.

Required column gaps: `{len(missing_columns)}`.

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
            "index column coverage checked",
            "index row coverage checked",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v5 x1 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v5 x1 creates the phase ledger index over v4 x1/x2.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
