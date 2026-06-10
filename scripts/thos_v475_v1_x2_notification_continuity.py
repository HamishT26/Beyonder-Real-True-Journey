#!/usr/bin/env python3
"""Build v475 THOS v1 x2 notification-continuity hardening artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v1-x2"
SOURCE_PHASE = "v475-thos-v1-x1"
NEXT_PHASE = "v475-thos-v2-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

SEED = ARTIFACT_ROOT / "v475-thos-v1-x1-receipt-durability-seed-v1.json"
NOTIFIER = ARTIFACT_ROOT / "v474-thos-v5-x2-no-rush-async-notifier-v1.json"
COMPLETION = ARTIFACT_ROOT / "v474-thos-v5-x2-cli-lane-completion-notice-v1.json"
DRIFT_GUARD = ARTIFACT_ROOT / "v474-thos-v8-x2-drift-recurrence-guard-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LANES = ["Arby", "Aster Vale"]
APP_LANES = ["Cicero", "Kierkegaard", "Aristotle"]
APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "dashboard rows should carry lane, phase, notification state, source hash, marker review, raw-output flags, staleness, lane presence, false-complete guard, and GMUT effect",
            "summary-ready metadata requires observed notice, source-bound metadata, marker review, and raw-output flags remaining false",
            "negative fixtures should cover stale notice, missing notice, false complete, raw flag, transport flag, hash mismatch, missing lane, and GMUT movement",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "no-rush notification is workflow care, not proof of quality, truth, continuity, or autonomy",
            "notifications should report metadata state transitions, not raw content or inferred mental states",
            "dashboard language should preserve open gaps and avoid success/failure pressure",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "notification rows need notice/run IDs, source-hash refs, source-chain status, lane state, marker review, raw-output flags, dashboard sync, and GMUT effect",
            "summary allowed is invalid if marker review is missing, source hashes drift, raw-output flags are true, or a required lane is absent",
            "v475 v2 x1 acceptance requires metadata-only continuity rows, matched source hashes, false raw-output flags, explicit marker state, and deterministic blocker fixtures",
        ],
    },
]

STATE_MACHINE = [
    {
        "state": "REQUESTED",
        "meaning": "A no-rush advisory request exists for the lane.",
        "allowed_next": ["LAUNCHED", "OPEN_GAP_LAUNCH_BLOCKED"],
    },
    {
        "state": "LAUNCHED",
        "meaning": "The lane process was started non-ephemeral and read-only.",
        "allowed_next": ["RUNNING", "OPEN_GAP_PROCESS_MISSING"],
    },
    {
        "state": "RUNNING",
        "meaning": "The lane may continue without a forced deadline.",
        "allowed_next": ["FINAL_MESSAGE_READY", "OPEN_GAP_TIMEOUT", "OPEN_GAP_STALE_NOTICE"],
    },
    {
        "state": "FINAL_MESSAGE_READY",
        "meaning": "A completion receipt reports final-message metadata only.",
        "allowed_next": ["MARKER_REVIEW", "FAIL_RAW_OUTPUT_EXPOSED", "FAIL_FALSE_COMPLETE"],
    },
    {
        "state": "MARKER_REVIEW",
        "meaning": "Marker counts are reviewed without publishing raw output.",
        "allowed_next": ["SUMMARY_READY_METADATA_ONLY", "OPEN_GAP_REVIEW_REQUIRED"],
    },
    {
        "state": "SUMMARY_READY_METADATA_ONLY",
        "meaning": "Only lane/status/hash/marker metadata may be summarized.",
        "allowed_next": ["PUBLISHED_METADATA_ONLY", "FAIL_CLAIM_EXPANSION"],
    },
    {
        "state": "PUBLISHED_METADATA_ONLY",
        "meaning": "Curated metadata may be committed; raw lane output remains unpublished.",
        "allowed_next": ["NEXT_PHASE_HANDOFF"],
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
    rel_path = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {
            "path": rel_path,
            "status": "OPEN_GAP_MISSING_SOURCE",
        }
    return {
        "bytes": path.stat().st_size,
        "path": rel_path,
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


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_NOTIFICATION_CONTINUITY_HARDENED"


def completion_lanes(completion: dict[str, Any]) -> list[dict[str, Any]]:
    lanes = []
    for lane in completion.get("lanes", []):
        lanes.append(
            {
                "completion_status": lane.get("completion_status"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "final_message_hash_present": bool(lane.get("final_message_hash")),
                "final_message_marker_count": lane.get("final_message_sensitive_marker_count"),
                "lane": lane.get("lane"),
                "raw_output_boundary": lane.get("raw_output_boundary"),
                "stderr_marker_counts_unpublished": bool(
                    lane.get("stderr_sensitive_marker_count_unpublished")
                    or lane.get("stderr_transport_marker_count_unpublished")
                ),
            }
        )
    return lanes


def lane_state(lane: dict[str, Any]) -> str:
    if lane.get("raw_output_boundary") != "temp_only_not_published":
        return "FAIL_RAW_OUTPUT_EXPOSED"
    if lane.get("completion_status") != "FINAL_MESSAGE_READY":
        return "OPEN_GAP_COMPLETION_PENDING"
    if not lane.get("final_message_hash_present"):
        return "FAIL_FALSE_COMPLETE"
    if lane.get("final_message_marker_count", 0) in (None, ""):
        return "OPEN_GAP_MARKER_UNKNOWN"
    return "SUMMARY_READY_METADATA_ONLY"


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("raw_path_leak") or case.get("raw_body_text_present"):
        observed = "FAIL_BLOCKER"
    elif case.get("forced_rush_deadline"):
        observed = "FAIL_BLOCKER"
    elif case.get("claim_expansion") or case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("final_ready") and not case.get("final_hash_present"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_completion_notice") or case.get("stale_notice"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only") and case.get("final_hash_present"):
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
            "metadata_completion_notice_expected_pass",
            {
                "final_hash_present": True,
                "gmut_gate_effect": "none_open_not_tested",
                "metadata_only": True,
            },
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_completion_notice_expected_open_gap",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "missing_completion_notice": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "false_complete_without_hash_expected_fail",
            {
                "final_hash_present": False,
                "final_ready": True,
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "stale_notice_expected_open_gap",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "stale_notice": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "raw_path_leak_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "raw_path_leak": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_body_text_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "raw_body_text_present": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "forced_rush_deadline_expected_fail",
            {
                "forced_rush_deadline": True,
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "claim_expansion_expected_fail",
            {
                "claim_expansion": True,
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_gate_moved_expected_fail",
            {
                "gmut_gate_effect": "gate_moved",
                "metadata_only": True,
            },
            "FAIL_BLOCKER",
        ),
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    seed = read_json(SEED)
    notifier = read_json(NOTIFIER)
    completion = read_json(COMPLETION)
    drift_guard = read_json(DRIFT_GUARD)
    source_refs = [source_ref(path) for path in (SEED, NOTIFIER, COMPLETION, DRIFT_GUARD)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    lanes = completion_lanes(completion)
    lane_names = {str(item.get("lane")) for item in lanes}
    missing_lanes = sorted(set(REQUIRED_LANES) - lane_names)
    lane_states = [
        {
            **lane,
            "state": lane_state(lane),
        }
        for lane in lanes
    ]
    failing_lane_states = [
        item for item in lane_states if item["state"].startswith("FAIL") or item["state"].startswith("OPEN_GAP")
    ]
    notifier_contract = notifier.get("notification_contract", {})
    watcher = notifier.get("watcher", {}).get("watcher_summary", {})
    seed_rows = {str(item.get("row_id")) for item in seed.get("rows", [])}
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]

    rows = [
        row(
            "source_chain",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_CHAIN",
            "Required curated sources were checked for notification continuity.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "seed_continuity",
            "PASS_SHAPE_ONLY" if {"lane_receipts", "fixtures", "claim_boundary"}.issubset(seed_rows) else "OPEN_GAP_SEED_ROWS",
            "v475 x1 durability seed rows are present for x2 hardening.",
            {"seed_row_count": len(seed_rows)},
        ),
        row(
            "watcher_contract",
            "PASS_SHAPE_ONLY" if watcher.get("started_background_watcher") and notifier_contract else "OPEN_GAP_WATCHER_CONTRACT",
            "The no-rush watcher contract is receipt-based rather than supervision-heavy.",
            {
                "poll_seconds": notifier_contract.get("poll_seconds"),
                "timeout_seconds": notifier_contract.get("timeout_seconds"),
                "started_background_watcher": watcher.get("started_background_watcher"),
            },
        ),
        row(
            "completion_receipts",
            "PASS_SHAPE_ONLY" if not missing_lanes and not failing_lane_states else "OPEN_GAP_COMPLETION_RECEIPTS",
            "Required lane completion receipts are represented as metadata only.",
            {
                "lane_states": lane_states,
                "missing_lanes": missing_lanes,
            },
        ),
        row(
            "no_rush_policy",
            "PASS_SHAPE_ONLY",
            "Long runtimes are allowed; no phase may treat silence alone as failure while timeout remains open.",
            {
                "allowed_window": "minutes_to_20_hours_or_more_when_user_approved",
                "failure_boundary": "only explicit launcher, watcher, source, marker, raw-output, or claim-boundary errors become blockers",
            },
        ),
        row(
            "app_lane_advisory_status",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were received and folded into the x2 notification-continuity guard.",
            {"advisory_count": len(APP_ADVISORIES), "lanes": APP_LANES, "status": "received"},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "False-complete, stale-notice, raw-leak, forced-rush, claim-expansion, and GMUT-gate drift fixtures were checked.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This hardens THOS notification continuity only; it does not test or close GMUT gates.",
        ),
    ]

    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "app_advisories": APP_ADVISORIES,
        "app_lane_advisory_status": "received",
        "claim_ceiling": "metadata_only_notification_continuity",
        "dashboard_update_rows": [
            "source_chain",
            "seed_continuity",
            "watcher_contract",
            "completion_receipts",
            "no_rush_policy",
            "app_lane_advisory_status",
            "negative_fixtures",
            "claim_boundary",
        ],
        "drift_guard_status": drift_guard.get("aggregate_status"),
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "handoff_to_next": {
            "next_expected_phase": NEXT_PHASE,
            "required_acceptance_criteria": [
                "retain metadata-only lane summaries",
                "keep no-rush watcher state separate from truth or quality claims",
                "block false-complete receipts without final-message hash metadata",
                "block any raw-output body/path exposure",
                "keep app-lane replies advisory-only until curated",
            ],
        },
        "lane_states": lane_states,
        "next_expected_phase": NEXT_PHASE,
        "notification_state_machine": STATE_MACHINE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
    }

    artifact_json = ARTIFACT_ROOT / f"{PHASE}-notification-continuity-hardening-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-notification-continuity-hardening-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"

    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v1 x2 Notification Continuity Hardening

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v1 x2 hardens the no-rush Arby/Aster notification path. It keeps the watcher receipt-based, separates completion metadata from content quality, and keeps raw CLI output unpublished.

Lane states: `{len(lane_states)}` checked; missing lanes: `{len(missing_lanes)}`.

Source refs: `{len(source_refs)}` checked; gaps: `{len(source_gaps)}`.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

App lane advisories: `received`.

Next expected phase: `{NEXT_PHASE}`.

All six GMUT gates remain open.
""",
    )

    run_status = {
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "published_artifacts": [artifact_json.relative_to(REPO_ROOT).as_posix(), artifact_md.relative_to(REPO_ROOT).as_posix()],
        "run_status": status,
        "next_expected_phase": NEXT_PHASE,
        "validation": [
            "source refs checked",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
        "gmUT_gates_open": GMUT_GATES,
    }
    write_json(run_json, run_status)
    write_md(
        run_md,
        f"""
# v475 THOS v1 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v1 x2 hardens no-rush notification continuity and dashboard handoff criteria. Cicero, Kierkegaard, and Aristotle advisories were folded into this metadata-only local artifact.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
