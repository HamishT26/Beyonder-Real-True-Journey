#!/usr/bin/env python3
"""Build v475 THOS v8 closure and v476 handoff artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


X1_PHASE = "v475-thos-v8-x1"
X2_PHASE = "v475-thos-v8-x2"
NEXT_PHASE = "v476-thos-v1-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
V7_CANDIDATE = ARTIFACT_ROOT / "v475-thos-v7-x1-metadata-summary-candidate-v1.json"
V7_PREFLIGHT = ARTIFACT_ROOT / "v475-thos-v7-x2-metadata-summary-preflight-v1.json"
V7_STATUS = ARTIFACT_ROOT / "v475-thos-v7-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

V476_HANDOFF_TASKS = [
    "carry metadata-only lane summary discipline into broader THOS dashboards",
    "add receipt freshness rows for active CLI and app lanes",
    "separate completion, review, publication, and quality states",
    "preserve local transport nonpublication by default",
    "add negative fixtures for broad staging and overbroad claims",
    "keep plugin-cache and user-skill repair receipts distinct from THOS capability claims",
    "route Journey material as context only when cited by local path and line",
    "continue exact-stage publication with remote equality verification",
    "track GMUT gates as open unless exact closure artifacts exist",
    "prepare v476 THOS suite-map rows for commands, skills, scripts, connectors, and dashboards",
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
    if case.get("source_missing") or case.get("missing_handoff_task"):
        observed = "OPEN_GAP"
    elif case.get("raw_text_publication") or case.get("quality_claim") or case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("closure_ready") and case.get("handoff_ready") and case.get("metadata_only"):
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
            "closure_and_handoff_expected_pass",
            {"closure_ready": True, "gmut_gate_effect": "none_open_not_tested", "handoff_ready": True, "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "source_missing_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "source_missing": True},
            "OPEN_GAP",
        ),
        fixture(
            "missing_handoff_task_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_handoff_task": True},
            "OPEN_GAP",
        ),
        fixture(
            "raw_text_publication_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_text_publication": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "quality_claim_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "quality_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_gate_move_expected_fail",
            {"closure_ready": True, "gmut_gate_effect": "gate_moved", "handoff_ready": True, "metadata_only": True},
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]], ready_status: str) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return ready_status


def build_x1(generated_at: str, fixtures: list[dict[str, Any]]) -> list[Path]:
    candidate = read_json(V7_CANDIDATE)
    preflight = read_json(V7_PREFLIGHT)
    status = read_json(V7_STATUS)
    source_refs = [source_ref(V7_CANDIDATE), source_ref(V7_PREFLIGHT), source_ref(V7_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    lane_rows = candidate.get("lane_metadata_summary", [])
    marker_total = sum(item.get("final_message_sensitive_marker_count") or 0 for item in lane_rows)
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v7 candidate and preflight sources were checked for v475 closure.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "preflight_ready",
            "PASS_SHAPE_ONLY" if preflight.get("aggregate_status") == "PASS_SHAPE_ONLY_METADATA_SUMMARY_PREFLIGHT_READY" else "OPEN_GAP_PREFLIGHT_NOT_READY",
            "v7 x2 preflight must be ready before closure handoff.",
            {"preflight_status": preflight.get("aggregate_status"), "run_status": status.get("aggregate_status")},
        ),
        row(
            "lane_metadata_summary",
            "PASS_SHAPE_ONLY" if len(lane_rows) == 2 and marker_total == 0 else "OPEN_GAP_LANE_METADATA",
            "Arby/Aster metadata summary is shape-ready with zero final-message markers.",
            {"lane_count": len(lane_rows), "marker_total": marker_total},
        ),
        row(
            "publication_boundary",
            "PASS_SHAPE_ONLY",
            "v475 closure permits metadata summary only and leaves lane text unpublished.",
            {"raw_lane_text_published": False, "quality_claimed": False},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v475 THOS closure does not validate GMUT or close any GMUT gate.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V475_CLOSURE_HANDOFF_READY")
    payload = {
        "aggregate_status": aggregate,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": X2_PHASE,
        "phase_slug": X1_PHASE,
        "rows": rows,
        "source_refs": source_refs,
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": X2_PHASE,
        "phase_slug": X1_PHASE,
        "rows": rows,
    }
    written: list[Path] = []
    json_path = ARTIFACT_ROOT / f"{X1_PHASE}-summary-closure-handoff-v1.json"
    write_json(json_path, payload)
    written.append(json_path)
    md_path = ARTIFACT_ROOT / f"{X1_PHASE}-summary-closure-handoff-v1.md"
    write_md(
        md_path,
        f"""
# v475 THOS v8 x1 Summary Closure Handoff

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v475 closes only the Arby/Aster metadata-summary path. Raw lane text remains unpublished, and summary readiness is not quality, proof, canon, or GMUT validation.

Lane metadata rows: `{len(lane_rows)}`
Final-message marker total: `{marker_total}`

Next expected phase: `{X2_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(md_path)
    status_json = ARTIFACT_ROOT / f"{X1_PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{X1_PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v8 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{X2_PHASE}`

v475 v8 x1 prepares closure for the metadata-only Arby/Aster summary arc.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def build_x2(generated_at: str, fixtures: list[dict[str, Any]]) -> list[Path]:
    x1 = ARTIFACT_ROOT / f"{X1_PHASE}-summary-closure-handoff-v1.json"
    x1_status = ARTIFACT_ROOT / f"{X1_PHASE}-run-status-v1.json"
    x1_payload = read_json(x1)
    x1_status_payload = read_json(x1_status)
    source_refs = [source_ref(x1), source_ref(x1_status)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v8 x1 closure sources were checked for v476 handoff.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "closure_ready",
            "PASS_SHAPE_ONLY" if x1_payload.get("aggregate_status") == "PASS_SHAPE_ONLY_V475_CLOSURE_HANDOFF_READY" else "OPEN_GAP_CLOSURE_NOT_READY",
            "v475 x1 closure must be ready before v476 handoff.",
            {"closure_status": x1_payload.get("aggregate_status"), "run_status": x1_status_payload.get("aggregate_status")},
        ),
        row(
            "handoff_tasks",
            "PASS_SHAPE_ONLY" if len(V476_HANDOFF_TASKS) >= 10 else "OPEN_GAP_HANDOFF_TASKS",
            "v476 receives a concrete THOS task seed.",
            {"task_count": len(V476_HANDOFF_TASKS)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v476 starts from THOS workflow evidence only; GMUT gates remain open.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V476_HANDOFF_READY")
    payload = {
        "aggregate_status": aggregate,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": X2_PHASE,
        "rows": rows,
        "source_refs": source_refs,
        "v476_handoff_tasks": V476_HANDOFF_TASKS,
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": X2_PHASE,
        "rows": rows,
    }
    written: list[Path] = []
    json_path = ARTIFACT_ROOT / f"{X2_PHASE}-v476-handoff-ledger-v1.json"
    write_json(json_path, payload)
    written.append(json_path)
    md_path = ARTIFACT_ROOT / f"{X2_PHASE}-v476-handoff-ledger-v1.md"
    write_md(
        md_path,
        f"""
# v475 THOS v8 x2 v476 Handoff Ledger

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v475 hands off to v476 with a THOS-only task seed. The handoff carries watcher, receipt, exact-stage, and metadata-summary discipline forward.

Handoff task count: `{len(V476_HANDOFF_TASKS)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(md_path)
    status_json = ARTIFACT_ROOT / f"{X2_PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{X2_PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v8 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v475 v8 x2 creates the v476 THOS handoff seed. It does not publish raw lane text and does not move any GMUT gate.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    generated_at = utc_now()
    fixtures = build_fixtures()
    written = build_x1(generated_at, fixtures)
    written.extend(build_x2(generated_at, fixtures))
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
