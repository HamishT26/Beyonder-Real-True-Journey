#!/usr/bin/env python3
"""Build v473 THOS v5 x2 policy-cycle completion artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v5-x2"
NEXT_PHASE = "v473-thos-v6-x1"
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


def parse_time(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def elapsed_seconds(started_at: str | None, ended_at: str | None) -> int | None:
    start = parse_time(started_at)
    end = parse_time(ended_at)
    if not start or not end:
        return None
    return max(0, int((end - start).total_seconds()))


def decision_for_lane(lane: dict[str, Any]) -> dict[str, Any]:
    markers = lane.get("final_message_sensitive_marker_count", 0)
    if lane.get("completion_status") != "FINAL_MESSAGE_READY":
        action = "HOLD_PENDING_COMPLETION"
        status = "OPEN_GAP"
    elif markers:
        action = "HOLD_RAW_TEXT_AND_SUMMARY"
        status = "OPEN_GAP"
    else:
        action = "ALLOW_METADATA_SUMMARY"
        status = "PASS_SHAPE_ONLY"
    return {
        "action": action,
        "final_message_bytes": lane.get("final_message_bytes"),
        "final_message_hash": lane.get("final_message_hash"),
        "gate_status": status,
        "lane": lane.get("lane"),
        "marker_count": markers,
        "raw_output_boundary": lane.get("raw_output_boundary"),
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    notice = read_json("v473-thos-v5-x1-cli-lane-completion-notice-v1.json")
    launch = read_json("v473-thos-v5-x1-policy-cycle-launch-receipt-v1.json")
    policy = read_json("v473-thos-v4-x2-summary-use-policy-v1.json")
    lanes = notice.get("lanes", [])
    all_ready = bool(lanes) and all(lane.get("completion_status") == "FINAL_MESSAGE_READY" for lane in lanes)
    decisions = [decision_for_lane(lane) for lane in lanes]
    held_lanes = [item["lane"] for item in decisions if item["action"] != "ALLOW_METADATA_SUMMARY"]
    allowed_lanes = [item["lane"] for item in decisions if item["action"] == "ALLOW_METADATA_SUMMARY"]
    elapsed = elapsed_seconds(notice.get("started_at_utc"), notice.get("generated_at_utc"))

    completion_rows = [
        row("completion_notice", "PASS_SHAPE_ONLY" if all_ready else "OPEN_GAP", "Watcher wrote a final-ready receipt for the v5 policy cycle.", {"elapsed_seconds": elapsed}),
        row("policy_applied", policy.get("aggregate_status", "OPEN_GAP"), "v4 x2 summary-use policy was applied to v5 receipt metadata."),
        row("held_lanes", "OPEN_GAP" if held_lanes else "PASS_SHAPE_ONLY", "Lanes held for review remain unpublished for advisory-summary use.", {"lanes": held_lanes}),
        row("allowed_lanes", "PASS_SHAPE_ONLY", "Lanes allowed for metadata-only summary.", {"lanes": allowed_lanes}),
        row("raw_boundary", "PASS_SHAPE_ONLY", "Raw final advisory text and transport remain temp-only and unpublished."),
    ]
    completion = {
        "aggregate_status": aggregate(completion_rows),
        "decisions": decisions,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": completion_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-policy-cycle-completion-v1.json"
    write_json(path, completion)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-policy-cycle-completion-v1.md",
        f"""
# v473 THOS v5 x2 Policy-Cycle Completion

Generated UTC: `{generated_at}`

Status: `{completion['aggregate_status']}`

The watcher completed after `{elapsed}` seconds. Metadata-only allowed lanes: `{', '.join(allowed_lanes) if allowed_lanes else 'none'}`. Held lanes: `{', '.join(held_lanes) if held_lanes else 'none'}`.

Raw final advisory text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-policy-cycle-completion-v1.md")

    handoff_rows = [
        row("launch", launch.get("aggregate_status", "OPEN_GAP"), "v5 x1 launch receipt is inherited."),
        row("completion", completion["aggregate_status"], "v5 x2 completion policy application is published."),
        row("review_backlog", "OPEN_GAP" if held_lanes else "PASS_SHAPE_ONLY", "Held lanes form the review backlog for v6."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All GMUT gates remain open."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Create a review-backlog ledger for held lanes before raw advisory summaries are used.",
            "Continue wrapper-backed Arby/Aster cycles only with receipt-level policy checks.",
            "Attempt app-lane advisory collection again and record no-payload states honestly if absent.",
            "Keep THOS workflow evidence separate from GMUT validation.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.md",
        f"""
# v473 THOS v5 x2 to v6 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v6 should create a review-backlog ledger for held lanes and keep summary-use policy active.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v6-handoff-v1.md")

    status_rows = [
        row("completion", completion["aggregate_status"], "Policy-cycle completion published."),
        row("handoff", handoff["aggregate_status"], "v6 handoff published."),
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
# v473 THOS v5 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v5 x2 applies the summary-use policy to the completed policy-cycle receipt.

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
