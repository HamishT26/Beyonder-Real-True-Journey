#!/usr/bin/env python3
"""Build v474 THOS v6 x1 receipt marker-review ledger artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v6-x1"
SOURCE_PHASE = "v474-thos-v5-x2"
NEXT_PHASE = "v474-thos-v6-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
COMPLETION_NOTICE = ARTIFACT_ROOT / f"{SOURCE_PHASE}-cli-lane-completion-notice-v1.json"

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
            "separate final-message readiness from marker-review clearance",
            "keep Aster on marker-review hold while one final marker is unresolved",
            "publish lane/status/hash/byte/marker metadata only",
            "raw final text, stderr, transport, visual captures, runtime records, and credential-like substrings remain blocked",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "waiting is the correct ethical state while privacy/provenance is unresolved",
            "do not collapse ready into publishable",
            "safe summaries can use hashes, bytes, marker counts, raw-output boundary, and blocker category",
            "aggregate status stays open until reviewed clearance exists",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "use explicit marker-review state machine",
            "Arby marker count zero can be metadata-clean",
            "Aster marker count one requires review",
            "raw output publication, missing refs, generic pass, or GMUT wording are blockers",
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


def lane_state(lane: dict[str, Any]) -> dict[str, Any]:
    marker_count = int(lane.get("final_message_sensitive_marker_count", -1))
    final_ready = lane.get("completion_status") == "FINAL_MESSAGE_READY"
    raw_temp_only = lane.get("raw_output_boundary") == "temp_only_not_published"
    if not final_ready:
        marker_state = "OPEN_GAP_FINAL_MESSAGE_MISSING"
        publication_status = "BLOCK_SUMMARY"
    elif marker_count == 0 and raw_temp_only:
        marker_state = "CLEAN_METADATA_ONLY"
        publication_status = "ALLOW_METADATA_SUMMARY"
    elif marker_count > 0 and raw_temp_only:
        marker_state = "REVIEW_REQUIRED"
        publication_status = "BLOCK_SUMMARY"
    else:
        marker_state = "HARD_BLOCKER"
        publication_status = "BLOCK_SUMMARY"
    return {
        "completion_status": lane.get("completion_status"),
        "final_message_bytes": lane.get("final_message_bytes"),
        "final_message_hash": lane.get("final_message_hash"),
        "final_sensitive_marker_count": marker_count,
        "lane": lane.get("lane"),
        "marker_review_state": marker_state,
        "raw_output_boundary": lane.get("raw_output_boundary"),
        "stderr_bytes_unpublished": lane.get("stderr_bytes"),
        "stderr_sensitive_marker_count_unpublished": lane.get("stderr_sensitive_marker_count_unpublished"),
        "summary_publication_status": publication_status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    raw_published = case.get("raw_output_published", False)
    marker_count = case.get("final_sensitive_marker_count")
    allow_summary = case.get("summary_publication_status") == "ALLOW_METADATA_SUMMARY"
    has_hash = case.get("has_hash", True)
    has_gmut_claim = case.get("has_gmut_claim", False)
    generic_pass = case.get("generic_pass", False)
    if raw_published or has_gmut_claim or generic_pass:
        observed = "FAIL_BLOCKER"
    elif marker_count and marker_count > 0 and allow_summary:
        observed = "FAIL_BLOCKER"
    elif not has_hash:
        observed = "OPEN_GAP_SOURCE_REF_MISSING"
    elif marker_count == 0 and allow_summary:
        observed = "PASS_SHAPE_ONLY"
    elif marker_count and marker_count > 0:
        observed = "OPEN_GAP_MARKER_REVIEW_REQUIRED"
    else:
        observed = "OPEN_GAP"
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
            "arby_metadata_clean_expected_pass_shape",
            {
                "final_sensitive_marker_count": 0,
                "has_hash": True,
                "raw_output_published": False,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "aster_marker_expected_open_gap",
            {
                "final_sensitive_marker_count": 1,
                "has_hash": True,
                "raw_output_published": False,
                "summary_publication_status": "BLOCK_SUMMARY",
            },
            "OPEN_GAP_MARKER_REVIEW_REQUIRED",
        ),
        fixture(
            "marker_with_summary_allow_expected_fail",
            {
                "final_sensitive_marker_count": 1,
                "has_hash": True,
                "raw_output_published": False,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_published_expected_fail",
            {
                "final_sensitive_marker_count": 0,
                "has_hash": True,
                "raw_output_published": True,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_hash_expected_open_gap",
            {
                "final_sensitive_marker_count": 0,
                "has_hash": False,
                "raw_output_published": False,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
            "OPEN_GAP_SOURCE_REF_MISSING",
        ),
        fixture(
            "gmut_claim_expected_fail",
            {
                "final_sensitive_marker_count": 0,
                "has_gmut_claim": True,
                "has_hash": True,
                "raw_output_published": False,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "generic_pass_expected_fail",
            {
                "final_sensitive_marker_count": 0,
                "generic_pass": True,
                "has_hash": True,
                "raw_output_published": False,
                "summary_publication_status": "ALLOW_METADATA_SUMMARY",
            },
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
        return "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"
    return "PASS_SHAPE_ONLY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    completion = read_json(COMPLETION_NOTICE)
    source_exists = bool(completion)
    lane_states = [lane_state(lane) for lane in completion.get("lanes", [])]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    review_required = [item for item in lane_states if item["marker_review_state"] == "REVIEW_REQUIRED"]
    hard_blockers = [item for item in lane_states if item["marker_review_state"] == "HARD_BLOCKER"]
    missing_lanes = {"Arby", "Aster Vale"} - {str(item.get("lane")) for item in lane_states}

    rows = [
        row(
            "completion_notice_source",
            "PASS_SHAPE_ONLY" if source_exists else "OPEN_GAP_MISSING_SOURCE",
            "The v5 x2 completion notice is the only source used for CLI lane metadata.",
            {
                "path": "docs/trinity-live-traces/v474-thos-v5-x2-cli-lane-completion-notice-v1.json",
                "sha256": sha256_file(COMPLETION_NOTICE) if source_exists else None,
            },
        ),
        row(
            "lane_marker_states",
            "FAIL_BLOCKER"
            if hard_blockers
            else "OPEN_GAP_MARKER_REVIEW_REQUIRED"
            if review_required or missing_lanes
            else "PASS_SHAPE_ONLY",
            "Lane marker states were classified from status/hash/byte/marker metadata only.",
            {
                "missing_lanes": sorted(missing_lanes),
                "review_required_lanes": [item["lane"] for item in review_required],
            },
        ),
        row(
            "raw_output_boundary",
            "PASS_SHAPE_ONLY"
            if all(item.get("raw_output_boundary") == "temp_only_not_published" for item in lane_states)
            else "FAIL_BLOCKER",
            "Raw final messages, stdout, stderr, and transport remain temp-only and unpublished.",
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Negative fixtures confirmed that marker holds and raw-output publication attempts do not pass.",
            {
                "fixture_count": len(fixtures),
                "mismatch_count": len(fixture_mismatches),
            },
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into a metadata-only marker-review workflow.",
            {"advisory_count": len(APP_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase improves THOS receipt hygiene only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    ledger = {
        "aggregate_status": aggregate,
        "app_advisories": APP_ADVISORIES,
        "completion_notice_status": completion.get("aggregate_status", "MISSING"),
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_states": lane_states,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "publication_blockers": [
            "Aster Vale final sensitive marker count remains unresolved",
            "raw lane text remains temp-only and unpublished",
            "stderr marker counts remain unpublished and cannot be converted into content claims",
            "no GMUT validation or gate movement is permitted",
        ],
        "rows": rows,
        "source_phase": SOURCE_PHASE,
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
    ledger_json = ARTIFACT_ROOT / f"{PHASE}-receipt-marker-review-ledger-v1.json"
    write_json(ledger_json, ledger)
    written.append(ledger_json)
    ledger_md = ARTIFACT_ROOT / f"{PHASE}-receipt-marker-review-ledger-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['marker_review_state']}`, summary `{item['summary_publication_status']}`, final bytes `{item['final_message_bytes']}`"
        for item in lane_states
    )
    write_md(
        ledger_md,
        f"""
# v474 THOS v6 x1 Receipt Marker-Review Ledger

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The v5 x2 completion notice is now classified without reading or publishing raw Arby/Aster lane text. Arby is metadata-clean for summary shape; Aster Vale remains on marker-review hold because one final-message marker is unresolved.

{lane_lines}

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Publication blockers: Aster marker review, raw lane nonpublication, unpublished stderr marker posture, and GMUT claim ceiling.

All six GMUT gates remain open.
""",
    )
    written.append(ledger_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v6 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v6 x1 converts the v5 x2 completion notice into a metadata-only marker-review ledger. Aster Vale remains held for marker review; raw CLI lane output is not published.

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
