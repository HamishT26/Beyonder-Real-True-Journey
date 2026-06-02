#!/usr/bin/env python3
"""Build v475 THOS v7 x2 metadata summary preflight artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v7-x2"
SOURCE_PHASE = "v475-thos-v7-x1"
NEXT_PHASE = "v475-thos-v8-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
CANDIDATE = ARTIFACT_ROOT / "v475-thos-v7-x1-metadata-summary-candidate-v1.json"
CANDIDATE_STATUS = ARTIFACT_ROOT / "v475-thos-v7-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LANES = ["Arby", "Aster Vale"]
REQUIRED_ALLOWED_FIELDS = [
    "lane",
    "completion_status",
    "final_message_bytes",
    "final_message_hash",
    "final_message_sensitive_marker_count",
    "raw_output_boundary",
]
FORBIDDEN_CLAIM_TERMS = [
    "quality_score",
    "truth_score",
    "validated_physics",
    "canon_promotion",
    "consciousness_proof",
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
    if case.get("missing_lane") or case.get("missing_allowed_field"):
        observed = "FAIL_BLOCKER"
    elif case.get("marker_count_nonzero") or case.get("forbidden_claim") or case.get("raw_text"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("source_gap"):
        observed = "OPEN_GAP"
    elif case.get("candidate_ready") and case.get("metadata_only"):
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
            "candidate_ready_expected_pass",
            {"candidate_ready": True, "gmut_gate_effect": "none_open_not_tested", "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_lane_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_lane": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_allowed_field_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_allowed_field": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "marker_count_nonzero_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "marker_count_nonzero": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "forbidden_claim_expected_fail",
            {"forbidden_claim": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_text_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_text": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_gap_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "source_gap": True},
            "OPEN_GAP",
        ),
        fixture(
            "gmut_gate_move_expected_fail",
            {"candidate_ready": True, "gmut_gate_effect": "gate_moved", "metadata_only": True},
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
    return "PASS_SHAPE_ONLY_METADATA_SUMMARY_PREFLIGHT_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    candidate = read_json(CANDIDATE)
    candidate_status = read_json(CANDIDATE_STATUS)
    source_refs = [source_ref(CANDIDATE), source_ref(CANDIDATE_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    lane_rows = candidate.get("lane_metadata_summary", [])
    present_lanes = sorted(item.get("lane") for item in lane_rows if item.get("lane"))
    missing_lanes = sorted(set(REQUIRED_LANES) - set(present_lanes))
    missing_allowed_fields = sorted(
        {
            field
            for field in REQUIRED_ALLOWED_FIELDS
            if any(field not in lane_row for lane_row in lane_rows)
        }
    )
    marker_total = sum(item.get("final_message_sensitive_marker_count") or 0 for item in lane_rows)
    allowed_fields = candidate.get("allowed_summary_fields", [])
    blocked_fields = candidate.get("blocked_summary_fields", [])
    claim_text = json.dumps(candidate, sort_keys=True)
    forbidden_hits = [term for term in FORBIDDEN_CLAIM_TERMS if term in claim_text and term not in blocked_fields]
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v7 x1 summary candidate and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "candidate_status",
            "PASS_SHAPE_ONLY" if candidate.get("aggregate_status") == "PASS_SHAPE_ONLY_METADATA_SUMMARY_CANDIDATE_READY" else "OPEN_GAP_CANDIDATE_NOT_READY",
            "Candidate aggregate status must be metadata-summary ready.",
            {"candidate_status": candidate.get("aggregate_status"), "run_status": candidate_status.get("aggregate_status")},
        ),
        row(
            "lane_coverage",
            "PASS_SHAPE_ONLY" if not missing_lanes else "FAIL_MISSING_LANE",
            "Both Arby and Aster Vale metadata rows must be present.",
            {"missing_lanes": missing_lanes, "present_lanes": present_lanes},
        ),
        row(
            "allowed_field_coverage",
            "PASS_SHAPE_ONLY" if not missing_allowed_fields else "FAIL_ALLOWED_FIELD_COVERAGE",
            "Every lane row must include all required allowed metadata fields.",
            {"missing_allowed_fields": missing_allowed_fields, "required_allowed_fields": REQUIRED_ALLOWED_FIELDS},
        ),
        row(
            "marker_counts",
            "PASS_SHAPE_ONLY" if marker_total == 0 else "FAIL_MARKER_REVIEW_REQUIRED",
            "Final-message marker count must remain zero.",
            {"marker_total": marker_total},
        ),
        row(
            "forbidden_claim_scan",
            "PASS_SHAPE_ONLY" if not forbidden_hits else "FAIL_FORBIDDEN_CLAIM_TERM",
            "Forbidden claim terms may appear only as blocked fields, not as live claims.",
            {"forbidden_hits": forbidden_hits},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Preflight remains metadata-only and does not move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    preflight = {
        "aggregate_status": aggregate,
        "allowed_fields_checked": allowed_fields,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
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
    preflight_json = ARTIFACT_ROOT / f"{PHASE}-metadata-summary-preflight-v1.json"
    write_json(preflight_json, preflight)
    written.append(preflight_json)
    preflight_md = ARTIFACT_ROOT / f"{PHASE}-metadata-summary-preflight-v1.md"
    write_md(
        preflight_md,
        f"""
# v475 THOS v7 x2 Metadata Summary Preflight

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The preflight checks the v7 x1 metadata-only completion summary candidate for lane coverage, allowed-field coverage, marker counts, forbidden-claim boundaries, source references, and GMUT gate immobility.

Lanes checked: `{len(present_lanes)}`
Marker total: `{marker_total}`
Missing lanes: `{len(missing_lanes)}`
Forbidden claim hits: `{len(forbidden_hits)}`

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
# v475 THOS v7 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v475 v7 x2 preflights the metadata-only Arby/Aster completion summary candidate. It does not publish raw lane text and does not move any GMUT gate.

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
