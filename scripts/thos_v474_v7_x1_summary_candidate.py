#!/usr/bin/env python3
"""Build v474 THOS v7 x1 summary-only publication candidate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v7-x1"
SOURCE_PHASE = "v474-thos-v6-x2"
NEXT_PHASE = "v474-thos-v7-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SOURCE_ARTIFACTS = [
    "docs/trinity-live-traces/v474-thos-v5-x2-cli-lane-completion-notice-v1.json",
    "docs/trinity-live-traces/v474-thos-v6-x1-receipt-marker-review-ledger-v1.json",
    "docs/trinity-live-traces/v474-thos-v6-x2-marker-classification-v1.json",
]

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "safe publication is lane, status, marker-count, classification, and source metadata only",
            "raw final text, stderr, transport, visual captures, runtime records, and private values remain blocked",
            "metadata-only review does not prove advisory quality or GMUT progress",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "summary-only publication is ethical only when it remains honest about its limits",
            "do not infer intent, identity, memory, or consciousness claims from marker metadata",
            "carry raw-output and GMUT boundaries forward",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "candidate rows need lane, readiness, marker review state, marker count, raw-unpublished flags, and source refs",
            "Aster benign classification must reference the review artifact, not raw text",
            "generic pass, raw content, source mismatch, or GMUT gate movement are blockers",
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


def source_ref(path_text: str) -> dict[str, Any]:
    path = REPO_ROOT / path_text
    if not path.exists():
        return {
            "path": path_text,
            "status": "OPEN_GAP_MISSING_SOURCE",
        }
    return {
        "bytes": path.stat().st_size,
        "path": path_text,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def lane_summary(lane: dict[str, Any]) -> dict[str, Any]:
    marker_state = lane.get("final_marker_review_state")
    marker_count = int(lane.get("final_marker_count", -1))
    benign_count = marker_count if marker_state == "REVIEWED_BENIGN_METADATA_ONLY" else 0
    return {
        "benign_marker_count": benign_count,
        "final_message_status": "READY" if lane.get("source_exists") else "OPEN_GAP",
        "lane": lane.get("lane"),
        "marker_count": marker_count,
        "marker_review_state": marker_state,
        "metadata_summary_status": "ALLOW_METADATA_SUMMARY"
        if marker_state in {"CLEAN_METADATA_ONLY", "REVIEWED_BENIGN_METADATA_ONLY"}
        else "BLOCK_SUMMARY",
        "raw_text_published": False,
        "source_refs": SOURCE_ARTIFACTS,
        "stderr_published": False,
        "transport_published": False,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    if case.get("raw_text") or case.get("stderr") or case.get("transport"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("source_ref_missing"):
        observed = "OPEN_GAP_SOURCE_REF_MISSING"
    elif case.get("marker_state") == "REVIEWED_BENIGN_METADATA_ONLY" and not case.get("review_source_present"):
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
        fixture("metadata_only_expected_pass", {"gmut_effect": "none_open_not_tested"}, "PASS_SHAPE_ONLY"),
        fixture("raw_text_expected_fail", {"gmut_effect": "none_open_not_tested", "raw_text": True}, "FAIL_BLOCKER"),
        fixture("stderr_expected_fail", {"gmut_effect": "none_open_not_tested", "stderr": True}, "FAIL_BLOCKER"),
        fixture("transport_expected_fail", {"gmut_effect": "none_open_not_tested", "transport": True}, "FAIL_BLOCKER"),
        fixture(
            "benign_marker_without_source_expected_fail",
            {
                "gmut_effect": "none_open_not_tested",
                "marker_state": "REVIEWED_BENIGN_METADATA_ONLY",
                "review_source_present": False,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_expected_fail",
            {"gmut_effect": "gate_moved"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_effect": "none_open_not_tested", "source_ref_missing": True},
            "OPEN_GAP_SOURCE_REF_MISSING",
        ),
        fixture(
            "generic_pass_expected_fail",
            {"generic_pass": True, "gmut_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
    ]


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
    return "PASS_SHAPE_ONLY_SUMMARY_CANDIDATE"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    source_refs = [source_ref(path) for path in SOURCE_ARTIFACTS]
    classification = read_json(REPO_ROOT / "docs/trinity-live-traces/v474-thos-v6-x2-marker-classification-v1.json")
    lane_summaries = [lane_summary(lane) for lane in classification.get("lane_reviews", [])]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    blocked_summary_lanes = [
        item["lane"] for item in lane_summaries if item["metadata_summary_status"] != "ALLOW_METADATA_SUMMARY"
    ]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REF_MISSING",
            "Summary candidate source references were checked against curated artifacts.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "lane_summary_scope",
            "PASS_SHAPE_ONLY" if not blocked_summary_lanes else "OPEN_GAP_BLOCKED_LANE_SUMMARY",
            "Lane summaries include metadata only and keep raw outputs unpublished.",
            {"blocked_summary_lanes": blocked_summary_lanes},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Negative fixtures confirmed raw-output, source-gap, generic-pass, and GMUT overclaim blockers.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into the summary-only candidate.",
            {"advisory_count": len(APP_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase creates a THOS metadata summary candidate only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    candidate = {
        "aggregate_status": aggregate,
        "app_advisories": APP_ADVISORIES,
        "candidate_scope": "summary_only_metadata",
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_summaries": lane_summaries,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
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
    candidate_json = ARTIFACT_ROOT / f"{PHASE}-summary-candidate-v1.json"
    write_json(candidate_json, candidate)
    written.append(candidate_json)
    candidate_md = ARTIFACT_ROOT / f"{PHASE}-summary-candidate-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['marker_review_state']}`, metadata summary `{item['metadata_summary_status']}`, markers `{item['marker_count']}`"
        for item in lane_summaries
    )
    write_md(
        candidate_md,
        f"""
# v474 THOS v7 x1 Summary-Only Candidate

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v7 x1 creates a summary-only candidate for Arby/Aster completion. It permits lane/status/marker/source metadata and keeps raw final text, stderr, and transport unpublished.

{lane_lines}

Source refs: `{len(source_refs)}` checked, `{len(source_gaps)}` gaps.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

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
# v474 THOS v7 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v7 x1 creates a metadata-only publication candidate for the Arby/Aster completion state. It does not publish raw lane output and does not move any GMUT gate.

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
