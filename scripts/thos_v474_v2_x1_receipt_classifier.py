#!/usr/bin/env python3
"""Classify v474 THOS CLI completion receipts without reading raw lane text."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v2-x1"
SOURCE_PHASE = "v474-thos-v1-x1"
NEXT_PHASE = "v474-thos-v2-x2"
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

STATUS_PRIORITY = [
    "FAIL_BLOCKER",
    "OPEN_GAP_MARKER_REVIEW_REQUIRED",
    "OPEN_GAP_FINAL_MESSAGE_PENDING",
    "OPEN_GAP_WATCH_TIMEOUT",
    "PASS_SUMMARY_READY",
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


def classify_lane(snapshot: dict[str, Any]) -> dict[str, Any]:
    lane = snapshot.get("lane", "unknown")
    final_status = snapshot.get("completion_status", "UNKNOWN")
    marker_count = int(snapshot.get("final_message_sensitive_marker_count") or 0)
    final_bytes = int(snapshot.get("final_message_bytes") or 0)
    if final_status != "FINAL_MESSAGE_READY":
        status = "OPEN_GAP_FINAL_MESSAGE_PENDING"
        reason = "final message is not ready"
    elif marker_count > 0:
        status = "OPEN_GAP_MARKER_REVIEW_REQUIRED"
        reason = "final message has marker count requiring human or approved marker review"
    elif final_bytes <= 0:
        status = "FAIL_BLOCKER"
        reason = "final message readiness contradicts zero final-message bytes"
    else:
        status = "PASS_SUMMARY_READY"
        reason = "final message metadata is ready and marker count is zero"
    return {
        "classification": status,
        "final_message_bytes": final_bytes,
        "final_message_status": final_status,
        "lane": lane,
        "marker_count": marker_count,
        "raw_text_retained_temp_only": snapshot.get("raw_output_boundary") == "temp_only_not_published",
        "reason": reason,
    }


def aggregate(classifications: list[dict[str, Any]]) -> str:
    statuses = {item["classification"] for item in classifications}
    for status in STATUS_PRIORITY:
        if status in statuses:
            return status
    return "OPEN_GAP_UNKNOWN"


def expected_fixtures() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "ready_clean",
            "input": {"completion_status": "FINAL_MESSAGE_READY", "final_message_sensitive_marker_count": 0, "final_message_bytes": 100},
            "expected": "PASS_SUMMARY_READY",
        },
        {
            "case_id": "marker_review",
            "input": {"completion_status": "FINAL_MESSAGE_READY", "final_message_sensitive_marker_count": 1, "final_message_bytes": 100},
            "expected": "OPEN_GAP_MARKER_REVIEW_REQUIRED",
        },
        {
            "case_id": "pending",
            "input": {"completion_status": "WAITING_FOR_FINAL_MESSAGE", "final_message_sensitive_marker_count": 0, "final_message_bytes": 0},
            "expected": "OPEN_GAP_FINAL_MESSAGE_PENDING",
        },
        {
            "case_id": "contradictory_zero_bytes",
            "input": {"completion_status": "FINAL_MESSAGE_READY", "final_message_sensitive_marker_count": 0, "final_message_bytes": 0},
            "expected": "FAIL_BLOCKER",
        },
    ]
    outputs = []
    for case in cases:
        snapshot = {"lane": case["case_id"], "raw_output_boundary": "temp_only_not_published", **case["input"]}
        observed = classify_lane(snapshot)["classification"]
        outputs.append(
            {
                "case_id": case["case_id"],
                "expected": case["expected"],
                "observed": observed,
                "status": "EXPECTED_CONFIRMED" if observed == case["expected"] else "EXPECTED_FAIL_MISMATCH",
            }
        )
    return outputs


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    completion = read_json(ARTIFACT_ROOT / f"{SOURCE_PHASE}-cli-lane-completion-notice-v1.json")
    source_status = completion.get("aggregate_status", "MISSING")
    lanes = [classify_lane(item) for item in completion.get("lanes", [])]
    fixtures = expected_fixtures()
    fixture_status = "PASS_SHAPE_ONLY" if all(item["status"] == "EXPECTED_CONFIRMED" for item in fixtures) else "FAIL_BLOCKER"
    aggregate_status = aggregate(lanes) if lanes else "OPEN_GAP_COMPLETION_RECEIPT_MISSING"

    classifier = {
        "aggregate_status": aggregate_status,
        "classifier_version": 1,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_classifications": lanes,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "raw_text_boundary": "not_read_not_published",
        "source_completion_status": source_status,
        "source_phase": SOURCE_PHASE,
        "status_order": STATUS_PRIORITY,
        "validation_fixtures": fixtures,
    }
    run_status = {
        "aggregate_status": "OPEN_GAP" if aggregate_status.startswith("OPEN_GAP") else "PASS_SHAPE_ONLY",
        "classifier_status": aggregate_status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": [
            row("classifier", aggregate_status, "Receipt classifier derived lane states without raw text reads.", {"lane_count": len(lanes)}),
            row("fixtures", fixture_status, "Expected classifier fixtures passed.", {"fixture_count": len(fixtures)}),
            row("claim_boundary", "PASS_SHAPE_ONLY", "Classifier supports THOS governance only; GMUT gates remain open."),
        ],
    }

    written: list[Path] = []
    classifier_json = ARTIFACT_ROOT / f"{PHASE}-receipt-classifier-v1.json"
    write_json(classifier_json, classifier)
    written.append(classifier_json)
    classifier_md = ARTIFACT_ROOT / f"{PHASE}-receipt-classifier-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['classification']}` because {item['reason']}"
        for item in lanes
    ) or "- no lane receipt available"
    write_md(
        classifier_md,
        f"""
# v474 THOS v2 x1 Receipt Classifier

Generated UTC: `{generated_at}`

Classifier status: `{aggregate_status}`

Lane classifications:
{lane_lines}

The classifier separates process completion evidence from marker-review clearance and never reads or publishes raw lane text.

All six GMUT gates remain open.
""",
    )
    written.append(classifier_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v2 x1 Run Status

Status: `{run_status['aggregate_status']}`

Classifier status: `{aggregate_status}`

Next expected phase: `{NEXT_PHASE}`

v2 x1 materializes a deterministic receipt classifier. Arby remains held for marker review if its marker count is nonzero; Aster Vale can be summary-ready from metadata only.

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
