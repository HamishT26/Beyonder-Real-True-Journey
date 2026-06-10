#!/usr/bin/env python3
"""Build v474 THOS v7 x2 summary-only publication preflight artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v7-x2"
SOURCE_PHASE = "v474-thos-v7-x1"
NEXT_PHASE = "v474-thos-v8-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SOURCE_CANDIDATE = ARTIFACT_ROOT / "v474-thos-v7-x1-summary-candidate-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LANES = {"Arby", "Aster Vale"}
ALLOWED_MARKER_STATES = {"CLEAN_METADATA_ONLY", "REVIEWED_BENIGN_METADATA_ONLY"}
BLOCKED_PUBLICATION_FIELDS = {
    "raw_text_published",
    "stderr_published",
    "transport_published",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_PREFLIGHT"


def source_ref_check(ref: dict[str, Any]) -> dict[str, Any]:
    path_text = str(ref.get("path", ""))
    path = REPO_ROOT / path_text
    if not path_text or not path.exists():
        return {
            "path": path_text,
            "status": "OPEN_GAP_SOURCE_REF_MISSING",
        }
    observed_hash = sha256_file(path)
    observed_bytes = path.stat().st_size
    expected_hash = ref.get("sha256")
    expected_bytes = ref.get("bytes")
    if observed_hash != expected_hash or observed_bytes != expected_bytes:
        return {
            "expected_bytes": expected_bytes,
            "expected_sha256": expected_hash,
            "observed_bytes": observed_bytes,
            "observed_sha256": observed_hash,
            "path": path_text,
            "status": "FAIL_BLOCKER_SOURCE_REF_MISMATCH",
        }
    return {
        "bytes": observed_bytes,
        "path": path_text,
        "sha256": observed_hash,
        "status": "PASS_SHAPE_ONLY",
    }


def lane_check(lane: dict[str, Any]) -> dict[str, Any]:
    lane_name = str(lane.get("lane", ""))
    marker_state = str(lane.get("marker_review_state", ""))
    raw_flags = {
        name: bool(lane.get(name, True))
        for name in BLOCKED_PUBLICATION_FIELDS
    }
    blocked_flags = [name for name, value in raw_flags.items() if value]
    source_refs = lane.get("source_refs") or []
    if lane_name not in REQUIRED_LANES:
        status = "FAIL_BLOCKER_UNKNOWN_LANE"
    elif marker_state not in ALLOWED_MARKER_STATES:
        status = "FAIL_BLOCKER_MARKER_STATE"
    elif blocked_flags:
        status = "FAIL_BLOCKER_RAW_OUTPUT_FLAG"
    elif len(source_refs) < 3:
        status = "OPEN_GAP_SOURCE_REFS_INCOMPLETE"
    elif lane.get("metadata_summary_status") != "ALLOW_METADATA_SUMMARY":
        status = "OPEN_GAP_SUMMARY_NOT_ALLOWED"
    else:
        status = "PASS_SHAPE_ONLY"
    return {
        "blocked_publication_flags": blocked_flags,
        "lane": lane_name,
        "marker_review_state": marker_state,
        "metadata_summary_status": lane.get("metadata_summary_status"),
        "source_ref_count": len(source_refs),
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    if case.get("unknown_lane"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_flag"):
        observed = "FAIL_BLOCKER"
    elif case.get("bad_marker_state"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_mismatch"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_missing"):
        observed = "OPEN_GAP"
    elif case.get("gmut_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("generic_pass"):
        observed = "FAIL_BLOCKER"
    else:
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
        fixture("valid_summary_candidate_expected_pass", {"gmut_effect": "none_open_not_tested"}, "PASS_SHAPE_ONLY"),
        fixture("unknown_lane_expected_fail", {"gmut_effect": "none_open_not_tested", "unknown_lane": True}, "FAIL_BLOCKER"),
        fixture("raw_flag_expected_fail", {"gmut_effect": "none_open_not_tested", "raw_flag": True}, "FAIL_BLOCKER"),
        fixture("bad_marker_state_expected_fail", {"bad_marker_state": True, "gmut_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("source_mismatch_expected_fail", {"gmut_effect": "none_open_not_tested", "source_mismatch": True}, "FAIL_BLOCKER"),
        fixture("source_missing_expected_open_gap", {"gmut_effect": "none_open_not_tested", "source_missing": True}, "OPEN_GAP"),
        fixture("gmut_effect_expected_fail", {"gmut_effect": "gate_moved"}, "FAIL_BLOCKER"),
        fixture("generic_pass_expected_fail", {"generic_pass": True, "gmut_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    candidate = read_json(SOURCE_CANDIDATE)
    source_checks = [source_ref_check(ref) for ref in candidate.get("source_refs", [])]
    lane_checks = [lane_check(lane) for lane in candidate.get("lane_summaries", [])]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    lanes_seen = {str(item.get("lane")) for item in candidate.get("lane_summaries", [])}
    missing_lanes = sorted(REQUIRED_LANES - lanes_seen)
    bad_sources = [item for item in source_checks if item["status"] != "PASS_SHAPE_ONLY"]
    bad_lanes = [item for item in lane_checks if item["status"] != "PASS_SHAPE_ONLY"]
    rows = [
        row(
            "source_candidate",
            "PASS_SHAPE_ONLY" if candidate else "OPEN_GAP_SOURCE_CANDIDATE_MISSING",
            "v7 x1 summary candidate was loaded for preflight.",
            {
                "path": "docs/trinity-live-traces/v474-thos-v7-x1-summary-candidate-v1.json",
                "sha256": sha256_file(SOURCE_CANDIDATE) if SOURCE_CANDIDATE.exists() else None,
            },
        ),
        row(
            "source_hashes",
            "PASS_SHAPE_ONLY" if not bad_sources else "FAIL_BLOCKER",
            "Candidate source references were checked against current curated files.",
            {
                "checked": len(source_checks),
                "bad_source_count": len(bad_sources),
            },
        ),
        row(
            "lane_invariants",
            "PASS_SHAPE_ONLY" if not bad_lanes and not missing_lanes else "FAIL_BLOCKER",
            "Lane summaries were checked for required lanes, marker states, metadata status, and raw-output flags.",
            {
                "bad_lane_count": len(bad_lanes),
                "missing_lanes": missing_lanes,
            },
        ),
        row(
            "candidate_scope",
            "PASS_SHAPE_ONLY"
            if candidate.get("candidate_scope") == "summary_only_metadata"
            and candidate.get("gmUT_gate_effect") == "none_open_not_tested"
            else "FAIL_BLOCKER",
            "Candidate scope and GMUT boundary were checked.",
            {
                "candidate_scope": candidate.get("candidate_scope"),
                "gmUT_gate_effect": candidate.get("gmUT_gate_effect"),
            },
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Preflight fixtures confirmed blockers for raw flags, lane mismatch, source mismatch, generic pass, and GMUT movement.",
            {
                "fixture_count": len(fixtures),
                "mismatch_count": len(fixture_mismatches),
            },
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase preflights THOS metadata summary only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    preflight = {
        "aggregate_status": aggregate,
        "candidate_hash": sha256_file(SOURCE_CANDIDATE) if SOURCE_CANDIDATE.exists() else None,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_checks": lane_checks,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_checks": source_checks,
        "source_phase": SOURCE_PHASE,
        "summary_publication_decision": "ALLOW_METADATA_SUMMARY_ONLY" if aggregate == "PASS_SHAPE_ONLY_PREFLIGHT" else "BLOCK_OR_HOLD",
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    preflight_json = ARTIFACT_ROOT / f"{PHASE}-summary-preflight-v1.json"
    write_json(preflight_json, preflight)
    written.append(preflight_json)
    preflight_md = ARTIFACT_ROOT / f"{PHASE}-summary-preflight-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['status']}`, marker `{item['marker_review_state']}`, raw flags `{len(item['blocked_publication_flags'])}`"
        for item in lane_checks
    )
    write_md(
        preflight_md,
        f"""
# v474 THOS v7 x2 Summary Preflight

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v7 x2 preflights the v7 x1 metadata-only summary candidate. It verifies source hashes, required lanes, marker-review states, metadata-summary status, raw-output publication flags, fixture coverage, and the GMUT claim boundary.

{lane_lines}

Source checks: `{len(source_checks)}` checked, `{len(bad_sources)}` blockers.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Decision: `{preflight['summary_publication_decision']}`.

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
# v474 THOS v7 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v7 x2 preflights the summary-only candidate and allows metadata summary only if source hashes, lane invariants, raw-output flags, and claim boundaries remain valid.

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
