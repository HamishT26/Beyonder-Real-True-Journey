#!/usr/bin/env python3
"""Build v474 THOS v3 x2 publication guard artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v3-x2"
SOURCE_VERIFIER_PHASE = "v474-thos-v3-x1"
SOURCE_CLASSIFIER_PHASE = "v474-thos-v2-x1"
NEXT_PHASE = "v474-thos-v4-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

BLOCKING_STATUSES = {
    "FAIL_BLOCKER",
    "REVIEW_REQUIRED",
    "OPEN_GAP",
    "OPEN_GAP_MARKER_REVIEW_REQUIRED",
    "OPEN_GAP_FINAL_MESSAGE_PENDING",
    "OPEN_GAP_WATCH_TIMEOUT",
    "OPEN_GAP_COMPLETION_RECEIPT_MISSING",
}

APP_GUARD_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "guard_points": [
            "exact staged-path allowlist must be checked before publication",
            "marker-review status must be explicit",
            "raw output in curated artifacts forces blocker status",
            "mutation scope must remain bounded and current-phase only",
            "THOS guard result must not imply GMUT validation",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "guard_points": [
            "privacy hold dominates convenience",
            "marker review pending is not publishable",
            "no-rush permits open gaps without forced retries",
            "retry only for wrapper or transport failure",
            "stop on repeated failure, privacy risk, timeout, user pause, or diminishing returns",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "guard_points": [
            "fixed precedence should dominate guard status derivation",
            "expected-negative fixtures must fail for expected reasons",
            "duplicate receipt identifiers and lane-run mismatches force blockers",
            "summary-ready contradictions force blockers",
            "guard reads summary metadata only, not temp raw text",
        ],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def classify_publication(lane: dict[str, Any]) -> dict[str, Any]:
    lane_name = lane.get("lane", "unknown")
    classification = lane.get("classification", "UNKNOWN")
    raw_temp_only = lane.get("raw_text_retained_temp_only") is True
    if not raw_temp_only:
        status = "FAIL_BLOCKER"
        reason = "raw text retention boundary is not confirmed"
    elif classification in BLOCKING_STATUSES:
        status = classification
        reason = lane.get("reason", "classification blocks publication")
    elif classification == "PASS_SUMMARY_READY":
        status = "SUMMARY_READY_METADATA_ONLY"
        reason = "lane metadata is summary-ready and raw text remains temp-only"
    else:
        status = "OPEN_GAP_UNKNOWN_CLASSIFICATION"
        reason = "unknown classifier state requires carry-forward"
    return {
        "lane": lane_name,
        "publication_status": status,
        "reason": reason,
        "source_classification": classification,
    }


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    verifier = read_json(ARTIFACT_ROOT / f"{SOURCE_VERIFIER_PHASE}-negative-fixture-verifier-v1.json")
    classifier = read_json(ARTIFACT_ROOT / f"{SOURCE_CLASSIFIER_PHASE}-receipt-classifier-v1.json")
    verifier_ok = verifier.get("aggregate_status") == "PASS_SHAPE_ONLY" and all(
        fixture.get("status") == "EXPECTED_CONFIRMED" for fixture in verifier.get("fixtures", [])
    )
    lane_publications = [
        classify_publication(lane) for lane in classifier.get("lane_classifications", [])
    ]
    blocking_lanes = [
        lane for lane in lane_publications if lane["publication_status"] != "SUMMARY_READY_METADATA_ONLY"
    ]
    aggregate_status = "OPEN_GAP_MARKER_REVIEW_REQUIRED" if blocking_lanes else "PASS_SHAPE_ONLY"
    if not verifier_ok:
        aggregate_status = "FAIL_BLOCKER"

    guard_rules = [
        "Do not publish raw CLI lane bodies or temp transcripts.",
        "Do not treat process exit or final-message detection as publication readiness.",
        "Block combined publication while any lane remains marker-review required.",
        "Allow metadata-only partial summary planning only for lanes with SUMMARY_READY_METADATA_ONLY.",
        "Fail if a receipt contains generic PASS, GMUT gate-effect drift, raw-output publication, hard credential markers, duplicate IDs, lane/run mismatches, or summary-ready contradictions.",
        "Carry open gaps rather than retrying for tone, grandeur, or desired content.",
        "Compare staged paths to the current-phase allowlist exactly before any shared commit.",
        "Prefer privacy holds over convenience whenever marker status or provenance is unclear.",
    ]
    required_guard_fields = [
        "guard_id",
        "phase_ref",
        "source_fixture_ref",
        "receipt_id",
        "lane",
        "run_id",
        "raw_text_published",
        "marker_review_status",
        "final_message_status",
        "redaction_status",
        "exit_status",
        "expected_status",
        "actual_status",
        "dominant_reason_code",
        "secondary_reason_codes",
        "blocked_claims",
        "gmUT_gate_effect",
    ]
    rows = [
        row(
            "source_verifier",
            "PASS_SHAPE_ONLY" if verifier_ok else "FAIL_BLOCKER",
            "v3 x1 negative-fixture verifier is required before publication guard use.",
            {"verifier_status": verifier.get("aggregate_status", "MISSING")},
        ),
        row(
            "source_classifier",
            "PASS_SHAPE_ONLY" if classifier else "OPEN_GAP_CLASSIFIER_MISSING",
            "v2 x1 classifier supplies lane-level metadata states.",
            {"classifier_status": classifier.get("aggregate_status", "MISSING")},
        ),
        row(
            "lane_publication_status",
            aggregate_status,
            "Combined publication remains blocked until every lane is marker-reviewed or explicitly held out.",
            {"blocking_lane_count": len(blocking_lanes), "lane_count": len(lane_publications)},
        ),
        row(
            "app_guard_advisories",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle app advisories were folded into the guard design.",
            {"advisory_count": len(APP_GUARD_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Publication guard improves THOS workflow hygiene only; GMUT gates remain open.",
        ),
    ]
    guard = {
        "aggregate_status": aggregate_status,
        "app_guard_advisories": APP_GUARD_ADVISORIES,
        "blocking_lanes": blocking_lanes,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "guard_rules": guard_rules,
        "lane_publications": lane_publications,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "required_guard_fields": required_guard_fields,
        "rows": rows,
        "source_classifier_phase": SOURCE_CLASSIFIER_PHASE,
        "source_verifier_phase": SOURCE_VERIFIER_PHASE,
    }
    run_status = {
        "aggregate_status": "OPEN_GAP" if aggregate_status.startswith("OPEN_GAP") else aggregate_status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    guard_json = ARTIFACT_ROOT / f"{PHASE}-publication-guard-v1.json"
    write_json(guard_json, guard)
    written.append(guard_json)
    guard_md = ARTIFACT_ROOT / f"{PHASE}-publication-guard-v1.md"
    lane_lines = "\n".join(
        f"- {lane['lane']}: `{lane['publication_status']}` because {lane['reason']}"
        for lane in lane_publications
    ) or "- no lane publication metadata available"
    write_md(
        guard_md,
        f"""
# v474 THOS v3 x2 Publication Guard

Generated UTC: `{generated_at}`

Status: `{aggregate_status}`

Lane publication states:
{lane_lines}

Combined publication remains blocked while any lane is marker-review required. Metadata-only partial summary planning is allowed only for lanes with summary-ready metadata and temp-only raw-output boundaries.

All six GMUT gates remain open.
""",
    )
    written.append(guard_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v3 x2 Run Status

Status: `{run_status['aggregate_status']}`

Publication guard status: `{aggregate_status}`

Next expected phase: `{NEXT_PHASE}`

v3 x2 converts the executable negative-fixture verifier into a publication guard. Arby remains blocked for marker review; Aster Vale is metadata-summary-ready only.

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
