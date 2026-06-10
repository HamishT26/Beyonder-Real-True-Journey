#!/usr/bin/env python3
"""Build v475 THOS v7 x1 metadata-only completion summary candidate."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v7-x1"
SOURCE_PHASE = "v475-thos-v6-x2"
NEXT_PHASE = "v475-thos-v7-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
COMPLETION_NOTICE = ARTIFACT_ROOT / "v475-thos-v6-x1-cli-lane-completion-notice-v1.json"
SUPERVISOR_LEDGER = ARTIFACT_ROOT / "v475-thos-v6-x2-async-supervisor-ledger-v1.json"
SUPERVISOR_STATUS = ARTIFACT_ROOT / "v475-thos-v6-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

ALLOWED_SUMMARY_FIELDS = [
    "lane",
    "completion_status",
    "final_message_bytes",
    "final_message_hash",
    "final_message_sensitive_marker_count",
    "raw_output_boundary",
]

BLOCKED_SUMMARY_FIELDS = [
    "final_message_text",
    "stdout_text",
    "stderr_text",
    "transport_body",
    "temp_path",
    "marker_substrings",
    "private_auth_material",
    "quality_score",
    "truth_score",
    "gmut_gate_closure",
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
    if case.get("blocked_field_present") or case.get("raw_text_present"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_required_lane") or case.get("marker_count_nonzero"):
        observed = "FAIL_BLOCKER"
    elif case.get("quality_claim") or case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("source_missing") or case.get("completion_not_ready"):
        observed = "OPEN_GAP"
    elif case.get("metadata_summary") and case.get("both_lanes_ready"):
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
            "metadata_summary_both_lanes_expected_pass",
            {"both_lanes_ready": True, "gmut_gate_effect": "none_open_not_tested", "metadata_summary": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "blocked_field_present_expected_fail",
            {"blocked_field_present": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_text_present_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_text_present": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_required_lane_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_required_lane": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "marker_count_nonzero_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "marker_count_nonzero": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "quality_claim_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "quality_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "completion_not_ready_expected_open_gap",
            {"completion_not_ready": True, "gmut_gate_effect": "none_open_not_tested"},
            "OPEN_GAP",
        ),
        fixture(
            "source_missing_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "source_missing": True},
            "OPEN_GAP",
        ),
        fixture(
            "gmut_gate_move_expected_fail",
            {"both_lanes_ready": True, "gmut_gate_effect": "gate_moved", "metadata_summary": True},
            "FAIL_BLOCKER",
        ),
    ]


def build_lane_summary(completion_notice: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for lane in completion_notice.get("lanes", []):
        summaries.append({field: lane.get(field) for field in ALLOWED_SUMMARY_FIELDS})
    return summaries


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_METADATA_SUMMARY_CANDIDATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    completion_notice = read_json(COMPLETION_NOTICE)
    supervisor_ledger = read_json(SUPERVISOR_LEDGER)
    supervisor_status = read_json(SUPERVISOR_STATUS)
    source_refs = [source_ref(COMPLETION_NOTICE), source_ref(SUPERVISOR_LEDGER), source_ref(SUPERVISOR_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    lane_summary = build_lane_summary(completion_notice)
    required_lanes = {"Arby", "Aster Vale"}
    present_lanes = {item.get("lane") for item in lane_summary}
    missing_lanes = sorted(required_lanes - present_lanes)
    marker_total = sum(item.get("final_message_sensitive_marker_count") or 0 for item in lane_summary)
    completion_ready = completion_notice.get("aggregate_status") == "FINAL_MESSAGES_READY"
    blocked_field_hits = sorted(set().union(*(set(item) for item in lane_summary)) & set(BLOCKED_SUMMARY_FIELDS))
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "Completion notice and v6 x2 supervisor sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "lane_coverage",
            "PASS_SHAPE_ONLY" if not missing_lanes else "FAIL_MISSING_LANE",
            "Required Arby and Aster Vale metadata rows are present.",
            {"missing_lanes": missing_lanes, "present_lanes": sorted(present_lanes)},
        ),
        row(
            "completion_status",
            "PASS_SHAPE_ONLY" if completion_ready else "OPEN_GAP_COMPLETION_NOT_READY",
            "Completion summary waits for final-ready metadata from both lanes.",
            {"completion_notice_status": completion_notice.get("aggregate_status")},
        ),
        row(
            "marker_counts",
            "PASS_SHAPE_ONLY" if marker_total == 0 else "FAIL_MARKER_REVIEW_REQUIRED",
            "Final-message marker counts must be zero before metadata-only summary publication.",
            {"final_message_marker_total": marker_total},
        ),
        row(
            "blocked_field_scan",
            "PASS_SHAPE_ONLY" if not blocked_field_hits else "FAIL_BLOCKED_FIELD_PRESENT",
            "Summary candidate contains only allowed metadata fields.",
            {"blocked_field_hits": blocked_field_hits, "allowed_summary_fields": ALLOWED_SUMMARY_FIELDS},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Metadata summary candidate does not claim advisory quality, proof, canon, or GMUT closure.",
            {"blocked_summary_fields": BLOCKED_SUMMARY_FIELDS, "gmut_gate_effect": "none_open_not_tested"},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    candidate = {
        "aggregate_status": aggregate,
        "allowed_summary_fields": ALLOWED_SUMMARY_FIELDS,
        "blocked_summary_fields": BLOCKED_SUMMARY_FIELDS,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "lane_metadata_summary": lane_summary,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_status": {
            "completion_notice": completion_notice.get("aggregate_status"),
            "supervisor_ledger": supervisor_ledger.get("aggregate_status"),
            "supervisor_status": supervisor_status.get("aggregate_status"),
        },
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
    candidate_json = ARTIFACT_ROOT / f"{PHASE}-metadata-summary-candidate-v1.json"
    write_json(candidate_json, candidate)
    written.append(candidate_json)
    candidate_md = ARTIFACT_ROOT / f"{PHASE}-metadata-summary-candidate-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['completion_status']}`, final bytes `{item['final_message_bytes']}`, markers `{item['final_message_sensitive_marker_count']}`"
        for item in lane_summary
    )
    write_md(
        candidate_md,
        f"""
# v475 THOS v7 x1 Metadata Summary Candidate

Generated UTC: `{generated_at}`

Status: `{aggregate}`

This candidate permits metadata-only summary of Arby/Aster completion. It does not publish lane text or evaluate advisory quality.

Lane metadata:

{lane_lines}

Allowed fields: `{len(ALLOWED_SUMMARY_FIELDS)}`
Blocked fields: `{len(BLOCKED_SUMMARY_FIELDS)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(candidate_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v7 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v475 v7 x1 creates a metadata-only completion summary candidate for Arby/Aster. It does not publish raw lane text and does not move any GMUT gate.

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
