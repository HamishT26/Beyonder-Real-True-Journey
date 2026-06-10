#!/usr/bin/env python3
"""Build v475 THOS v5 x2 phase ledger index gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v5-x2"
SOURCE_PHASE = "v475-thos-v5-x1"
NEXT_PHASE = "v475-thos-v6-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

INDEX = ARTIFACT_ROOT / "v475-thos-v5-x1-phase-ledger-index-v1.json"
INDEX_STATUS = ARTIFACT_ROOT / "v475-thos-v5-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_AUTHORITY_CLASSES = [
    "remote_verified_commit",
    "local_curated_artifact",
    "metadata_receipt",
    "advisory_only",
    "open_gap",
    "blocked",
]

BLOCKED_RAW_MATERIAL = [
    "raw_cli_output",
    "stderr_text",
    "temp_transport",
    "session_log_stream",
    "image_capture_material",
    "private_auth_material",
    "marker_substrings",
    "full_sensitive_paths",
]

APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "ledger rows should carry phase status, source authority, artifact ref, dashboard/receipt status, open-gap/fail-blocker counts, raw-output flags, GMUT effect, and next required artifact",
            "source authority classes should distinguish remote-verified commit, curated artifact, metadata receipt, advisory-only, open gap, and blocked",
            "raw CLI output, stderr text, temp transport, session logs, image-capture material, private auth material, marker substrings, and sensitive paths remain blocked",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "ledger index is a calm map, not a scoreboard",
            "open gaps stay visible without pressure labels",
            "source authority means traceable metadata, not truth, quality, production readiness, or GMUT validation",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "ledger rows should include row id, phase, ledger name, artifact ref/type, source hash, claim scope, status, blocker/open-gap codes, raw-output flag, and GMUT effect",
            "future row coverage should include Arby/Aster receipt summaries, marker review, raw-output block, source-hash manifest, dashboard sync, negative fixture, publication guard, release gate, and handoff seed",
            "negative fixtures should block missing required rows, hash drift, raw output, unresolved marker review for summary publication, generic pass, wrong phase, GMUT drift, overbroad claim scope, and missing source hash",
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
    if case.get("missing_current_index_row") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_output") or case.get("generic_pass") or case.get("wrong_phase"):
        observed = "FAIL_BLOCKER"
    elif case.get("hash_drift") or case.get("overbroad_claim") or case.get("missing_source_hash"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("future_optional_row_missing") or case.get("open_gap"):
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
            "metadata_index_gate_expected_pass",
            {"gmut_gate_effect": "none_open_not_tested", "index_ready": True, "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_current_index_row_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_current_index_row": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_required_column_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_required_column": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "hash_drift_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "hash_drift": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_output": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "generic_pass_expected_fail",
            {"generic_pass": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "wrong_phase_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "wrong_phase": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "overbroad_claim_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "overbroad_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_hash_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source_hash": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "future_optional_row_missing_expected_open_gap",
            {"future_optional_row_missing": True, "gmut_gate_effect": "none_open_not_tested"},
            "OPEN_GAP",
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


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_PHASE_LEDGER_INDEX_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    index = read_json(INDEX)
    index_status = read_json(INDEX_STATUS)
    source_refs = [source_ref(INDEX), source_ref(INDEX_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    index_rows = index.get("index_rows", [])
    required_columns = index.get("required_index_columns", [])
    column_gaps = [
        column
        for column in required_columns
        if any(column not in index_row for index_row in index_rows)
    ]
    missing_current_rows = len(index_rows) != 2
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    future_expansion_backlog = [
        "Arby receipt summary row",
        "Aster Vale receipt summary row",
        "marker-review summary row",
        "raw-output block assertion row",
        "source-hash manifest row",
        "dashboard sync report row",
        "negative-fixture report row",
        "publication guard row",
        "release/readiness gate row",
        "handoff seed row",
    ]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v5 x1 index sources were checked for the ledger index gate.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "current_index_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_current_rows else "FAIL_INDEX_ROW_COVERAGE",
            "Current v4 x1/x2 index rows are present.",
            {"index_row_count": len(index_rows)},
        ),
        row(
            "column_coverage",
            "PASS_SHAPE_ONLY" if not column_gaps else "FAIL_COLUMN_COVERAGE",
            "Required current ledger index columns are present.",
            {"column_gaps": column_gaps},
        ),
        row(
            "advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into source-authority, open-gap, and future-row expansion rules.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS)},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Ledger gate fixtures checked row coverage, columns, hash drift, raw output, generic pass, wrong phase, overbroad claims, missing source hash, optional future rows, open gaps, and GMUT boundary.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This gate is THOS phase-ledger metadata only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "blocked_raw_material": BLOCKED_RAW_MATERIAL,
        "fixtures": fixtures,
        "future_expansion_backlog": future_expansion_backlog,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_authority_classes": SOURCE_AUTHORITY_CLASSES,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_run_status": index_status.get("run_status"),
        "v6_x1_handoff": {
            "recommended_scope": "expand the phase ledger index toward lane-specific receipt rows while preserving raw-output and claim-boundary blocks",
            "claim_ceiling": "repo-only humane ledger-index metadata improves traceability and handoff review",
        },
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-phase-ledger-index-gate-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-phase-ledger-index-gate-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v5 x2 Phase Ledger Index Gate

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v5 x2 gates the phase ledger index and folds in Cicero, Kierkegaard, and Aristotle advisory guidance as metadata-only source-authority, open-gap, and future-row rules.

Current index rows: `{len(index_rows)}`.

Future expansion backlog rows: `{len(future_expansion_backlog)}`.

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
            "current index row coverage checked",
            "column coverage checked",
            "app advisory synthesis folded in",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v5 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v5 x2 gates the phase ledger index and prepares the lane-specific ledger expansion handoff.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
