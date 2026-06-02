#!/usr/bin/env python3
"""Build v473 THOS v4 x1 receipt-level marker-review integration artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v4-x1"
NEXT_PHASE = "v473-thos-v4-x2"
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

APP_SUBMISSIONS = [
    {"lane": "Cicero", "status": "PENDING_NO_PAYLOAD", "submission_id": "019e8920-316f-7923-8073-809d2eea4234"},
    {"lane": "Kierkegaard", "status": "PENDING_NO_PAYLOAD", "submission_id": "019e8920-663a-71b2-9098-5252ab71b9db"},
    {"lane": "Aristotle", "status": "PENDING_NO_PAYLOAD", "submission_id": "019e8920-a3e5-7f50-a61a-f61b5fcff3fc"},
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def classify_lane(lane: dict[str, Any]) -> dict[str, Any]:
    marker_count = lane.get("final_message_sensitive_marker_count", 0)
    completion = lane.get("completion_status")
    if completion != "FINAL_MESSAGE_READY":
        status = "OPEN_GAP_FINAL_MESSAGE_PENDING"
    elif marker_count:
        status = "OPEN_GAP_MARKER_REVIEW_REQUIRED"
    else:
        status = "PASS_NO_MARKER"
    return {
        "completion_status": completion,
        "final_message_bytes": lane.get("final_message_bytes"),
        "final_message_hash": lane.get("final_message_hash"),
        "lane": lane.get("lane"),
        "marker_count": marker_count,
        "raw_output_boundary": lane.get("raw_output_boundary"),
        "review_status": status,
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    notice = read_json("v473-thos-v3-x2-cli-lane-completion-notice-v1.json")
    live = read_json("v473-thos-v3-x2-wrapper-live-completion-synthesis-v1.json")
    lanes = [classify_lane(lane) for lane in notice.get("lanes", [])]
    marker_lanes = [lane["lane"] for lane in lanes if lane["review_status"] == "OPEN_GAP_MARKER_REVIEW_REQUIRED"]
    pending_lanes = [lane["lane"] for lane in lanes if lane["review_status"] == "OPEN_GAP_FINAL_MESSAGE_PENDING"]

    classifier_rows = [
        row(
            "receipt_available",
            "PASS_SHAPE_ONLY" if lanes else "OPEN_GAP",
            "A curated wrapper completion receipt is available for receipt-level marker review.",
            {"lane_count": len(lanes)},
        ),
        row(
            "metadata_only",
            "PASS_SHAPE_ONLY",
            "Classification uses published receipt metadata only; raw final advisory text remains unpublished.",
        ),
        row(
            "marker_review_required",
            "OPEN_GAP" if marker_lanes else "PASS_SHAPE_ONLY",
            "Lanes with marker counts require review before advisory text can be summarized.",
            {"lanes": marker_lanes},
        ),
        row(
            "pending_final",
            "OPEN_GAP" if pending_lanes else "PASS_SHAPE_ONLY",
            "All lanes must be final-message ready before summary use.",
            {"lanes": pending_lanes},
        ),
    ]
    classifier = {
        "aggregate_status": aggregate(classifier_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_reviews": lanes,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": classifier_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-receipt-marker-review-v1.json"
    write_json(path, classifier)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-receipt-marker-review-v1.md",
        f"""
# v473 THOS v4 x1 Receipt Marker Review

Generated UTC: `{generated_at}`

Status: `{classifier['aggregate_status']}`

Receipt-level review uses only published metadata. Lanes requiring review: `{', '.join(marker_lanes) if marker_lanes else 'none'}`.

Raw final advisory text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-receipt-marker-review-v1.md")

    integration_rows = [
        row("wrapper_live", live.get("aggregate_status", "OPEN_GAP"), "v3 x2 wrapper live synthesis is inherited."),
        row("review_gate", classifier["aggregate_status"], "Receipt-level marker review is now attached to wrapper completion metadata."),
        row("app_lanes", "OPEN_GAP", "App-lane submissions remain pending without returned payloads."),
    ]
    integration = {
        "aggregate_status": aggregate(integration_rows),
        "app_submissions": APP_SUBMISSIONS,
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": integration_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-app-cli-integration-ledger-v1.json"
    write_json(path, integration)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-app-cli-integration-ledger-v1.md",
        """
# v473 THOS v4 x1 App/CLI Integration Ledger

CLI receipt-level marker review is attached to the wrapper flow. App-lane prompts were sent, but no returned payload is claimed yet.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-app-cli-integration-ledger-v1.md")

    handoff_rows = [
        row("classifier", classifier["aggregate_status"], "Receipt-level marker review is ready for v4 x2 refinement."),
        row("integration", integration["aggregate_status"], "App/CLI integration remains open."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All GMUT gates remain open and are unaffected by THOS workflow reliability evidence."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Add a summary-use policy that allows lane summaries only when review_status is PASS_NO_MARKER or separately cleared.",
            "Wait for app-lane returns and record them as advisory-only if available.",
            "Launch the next wrapper-backed Arby/Aster lane with receipt-level marker review enabled.",
            "Keep raw transport, local temp files, and final advisory bodies unpublished.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v4-x2-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v4-x2-handoff-v1.md",
        f"""
# v473 THOS v4 x1 to v4 x2 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v4 x2 should refine summary-use policy and fold in any returned app-lane advisories.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v4-x2-handoff-v1.md")

    status_rows = [
        row("classifier", classifier["aggregate_status"], "Receipt-level marker review published."),
        row("integration", integration["aggregate_status"], "App/CLI integration ledger published."),
        row("handoff", handoff["aggregate_status"], "v4 x2 handoff published."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v473 THOS v4 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v4 x1 attaches receipt-level marker review to the wrapper-backed Arby/Aster completion flow.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
