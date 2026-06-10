#!/usr/bin/env python3
"""Build v475 THOS v4 x1 release/readiness ledger artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v4-x1"
SOURCE_PHASE = "v475-thos-v3-x2"
NEXT_PHASE = "v475-thos-v4-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
GATE = ARTIFACT_ROOT / "v475-thos-v3-x2-report-board-gate-v1.json"
GATE_STATUS = ARTIFACT_ROOT / "v475-thos-v3-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

OFFICIAL_SOURCE_REFS = [
    {
        "authority": "OpenAI Help Center",
        "claim_ceiling": "Codex access, controls, usage, and feature context only",
        "retrieved_context": "2026-06-03 NZ live browse",
        "url": "https://help.openai.com/en/articles/11369540",
    },
    {
        "authority": "NVIDIA DGX Spark User Guide",
        "claim_ceiling": "AI workstation/platform documentation context only",
        "retrieved_context": "2026-06-03 NZ live browse",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/",
    },
    {
        "authority": "NVIDIA DGX Spark Porting Guide",
        "claim_ceiling": "porting/optimization source routing context only",
        "retrieved_context": "2026-06-03 NZ live browse",
        "url": "https://docs.nvidia.com/dgx/dgx-spark-porting-guide/index.html",
    },
]

READINESS_STATES = [
    "NOT_STARTED",
    "METADATA_READY",
    "OPEN_GAP_CARRIED",
    "BLOCKED_BY_GUARD",
    "RELEASE_READY_METADATA_ONLY",
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
    observed = "OPEN_GAP_CARRIED"
    if case.get("missing_source") or case.get("external_source_unverified"):
        observed = "OPEN_GAP_CARRIED"
    elif case.get("raw_output") or case.get("guard_failure") or case.get("claim_expansion"):
        observed = "BLOCKED_BY_GUARD"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "BLOCKED_BY_GUARD"
    elif case.get("metadata_ready") and case.get("guards_clean"):
        observed = "RELEASE_READY_METADATA_ONLY"
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
            "metadata_ready_expected_release_ready",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "guards_clean": True,
                "metadata_ready": True,
            },
            "RELEASE_READY_METADATA_ONLY",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP_CARRIED",
        ),
        fixture(
            "external_source_unverified_expected_open_gap",
            {"external_source_unverified": True, "gmut_gate_effect": "none_open_not_tested"},
            "OPEN_GAP_CARRIED",
        ),
        fixture(
            "raw_output_expected_blocked",
            {"gmut_gate_effect": "none_open_not_tested", "raw_output": True},
            "BLOCKED_BY_GUARD",
        ),
        fixture(
            "guard_failure_expected_blocked",
            {"gmut_gate_effect": "none_open_not_tested", "guard_failure": True},
            "BLOCKED_BY_GUARD",
        ),
        fixture(
            "claim_expansion_expected_blocked",
            {"claim_expansion": True, "gmut_gate_effect": "none_open_not_tested"},
            "BLOCKED_BY_GUARD",
        ),
        fixture(
            "gmut_effect_moved_expected_blocked",
            {"gmut_gate_effect": "gate_moved", "metadata_ready": True},
            "BLOCKED_BY_GUARD",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_RELEASE_READINESS_LEDGER_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    gate = read_json(GATE)
    gate_status = read_json(GATE_STATUS)
    source_refs = [source_ref(GATE), source_ref(GATE_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    report_gate = gate.get("report_board_gate", {})
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    readiness_ledger = [
        {
            "ledger_row": "report_board_gate",
            "readiness_state": "RELEASE_READY_METADATA_ONLY"
            if gate.get("aggregate_status") == "PASS_SHAPE_ONLY_REPORT_BOARD_GATE_READY"
            else "OPEN_GAP_CARRIED",
            "source_status": gate.get("aggregate_status"),
            "summary": "Report-board gate can be carried as metadata-only release readiness.",
        },
        {
            "ledger_row": "source_authority",
            "readiness_state": "METADATA_READY",
            "source_status": "OFFICIAL_SOURCES_RECORDED",
            "summary": "Official OpenAI/NVIDIA references are recorded as source-routing context, not implementation proof.",
        },
        {
            "ledger_row": "open_gap_policy",
            "readiness_state": "METADATA_READY",
            "source_status": "OPEN_GAPS_CARRIED_EXPLICITLY",
            "summary": "Open gaps stay visible and do not become failure or success by silence.",
        },
        {
            "ledger_row": "claim_boundary",
            "readiness_state": "METADATA_READY",
            "source_status": "GMUT_EFFECT_NONE_OPEN_NOT_TESTED",
            "summary": "The ledger is THOS metadata readiness only; all GMUT gates remain open.",
        },
    ]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v3 x2 gate sources were checked for the release/readiness ledger.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "gate_status",
            "PASS_SHAPE_ONLY" if gate.get("aggregate_status") == "PASS_SHAPE_ONLY_REPORT_BOARD_GATE_READY" else "OPEN_GAP_GATE_STATUS",
            "Report-board gate status is carried into release/readiness semantics.",
            {"gate_status": gate.get("aggregate_status"), "gate_rows": report_gate},
        ),
        row(
            "external_source_authority",
            "PASS_SHAPE_ONLY",
            "Official external sources are recorded with claim ceilings and do not validate THOS/GMUT claims.",
            {"source_count": len(OFFICIAL_SOURCE_REFS)},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Readiness fixtures checked metadata-ready, open-gap, raw-output, guard-failure, claim-expansion, and GMUT boundary behavior.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This ledger is THOS release/readiness metadata only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "external_source_refs": OFFICIAL_SOURCE_REFS,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "readiness_ledger": readiness_ledger,
        "readiness_states": READINESS_STATES,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_run_status": gate_status.get("run_status"),
        "v4_x2_acceptance_criteria": [
            "ledger rows remain metadata-only",
            "official sources remain source-routing context only",
            "open gaps are explicitly carried",
            "raw-output, guard-failure, claim-expansion, and GMUT-drift fixtures block promotion",
            "next handoff does not claim production readiness, GMUT validation, or consciousness proof",
        ],
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-release-readiness-ledger-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-release-readiness-ledger-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v4 x1 Release Readiness Ledger

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v4 x1 creates a compact release/readiness ledger from the v3 x2 report-board gate. It records official OpenAI/NVIDIA source authority as routing context only.

Ledger rows: `{len(readiness_ledger)}`.

Official external sources recorded: `{len(OFFICIAL_SOURCE_REFS)}`.

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
            "official source authority recorded",
            "readiness fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v4 x1 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v4 x1 creates the release/readiness ledger and carries official source references as context only.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
