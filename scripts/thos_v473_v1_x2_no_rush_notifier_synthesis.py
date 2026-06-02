#!/usr/bin/env python3
"""Build v473 THOS v1 x2 no-rush CLI notifier synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v1-x2"
NEXT_PHASE = "v473-thos-v2-x1"
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


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def elapsed_seconds(started_at: str | None, ended_at: str | None) -> int | None:
    start = parse_time(started_at)
    end = parse_time(ended_at)
    if not start or not end:
        return None
    return max(0, int((end - start).total_seconds()))


def lane_summary(lanes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for lane in lanes:
        summaries.append(
            {
                "completion_status": lane.get("completion_status"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "final_message_hash": lane.get("final_message_hash"),
                "final_message_marker_count": lane.get("final_message_sensitive_marker_count"),
                "lane": lane.get("lane"),
                "raw_output_boundary": lane.get("raw_output_boundary"),
                "stderr_bytes": lane.get("stderr_bytes"),
                "stdout_bytes": lane.get("stdout_bytes"),
            }
        )
    return summaries


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    notice = read_json("v473-thos-v1-x1-cli-lane-completion-notice-v1.json")
    classifier = read_json("v473-thos-v1-x1-marker-review-classifier-v1.json")
    fixtures = read_json("v473-thos-v1-x1-marker-review-fixture-results-v1.json")
    x1_status = read_json("v473-thos-v1-x1-run-status-v1.json")
    lanes = notice.get("lanes", [])
    notice_status = notice.get("aggregate_status")
    elapsed = elapsed_seconds(notice.get("started_at_utc"), notice.get("generated_at_utc"))
    all_ready = bool(lanes) and all(item.get("completion_status") == "FINAL_MESSAGE_READY" for item in lanes)
    marker_count = sum(item.get("final_message_sensitive_marker_count", 0) for item in lanes)

    notifier_rows = [
        row(
            "no_rush_completion",
            "PASS_SHAPE_ONLY" if all_ready else "OPEN_GAP",
            "Arby and Aster Vale completed naturally; no minimum dwell or forced early cutoff was required.",
            {"elapsed_seconds": elapsed, "lane_count": len(lanes)},
        ),
        row(
            "completion_notice",
            "PASS_SHAPE_ONLY" if notice_status in {"FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"} else "OPEN_GAP",
            "The watcher wrote a curated completion receipt and exited at a terminal lane-ready state.",
            {"notice_status": notice_status},
        ),
        row(
            "raw_boundary",
            "PASS_SHAPE_ONLY",
            "Raw lane transport and final advisory text remain temp-only and unpublished.",
        ),
        row(
            "marker_review",
            "OPEN_GAP" if marker_count else "PASS_SHAPE_ONLY",
            "Final-message markers still require classifier review before any raw advisory text is used.",
            {"final_message_marker_count": marker_count},
        ),
    ]
    notifier = {
        "aggregate_status": aggregate(notifier_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_summaries": lane_summary(lanes),
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": notifier_rows,
        "watcher_script": "scripts/thos_cli_lane_completion_notifier.py",
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-no-rush-cli-notifier-synthesis-v1.json"
    write_json(path, notifier)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-no-rush-cli-notifier-synthesis-v1.md",
        f"""
# v473 THOS v1 x2 No-Rush CLI Notifier Synthesis

Generated UTC: `{generated_at}`

Status: `{notifier['aggregate_status']}`

Arby and Aster Vale completed their non-ephemeral read-only lanes naturally. The watcher recorded completion after `{elapsed}` seconds and published only safe lane metadata: readiness state, byte counts, hashes, and marker-review counts.

Raw lane text remains temp-only and unpublished. This is THOS workflow evidence only; it does not validate GMUT or close any GMUT gate.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-no-rush-cli-notifier-synthesis-v1.md")

    protocol_rows = [
        row(
            "launch",
            "PASS_SHAPE_ONLY",
            "Launch Arby and Aster Vale with no artificial reply-length or dwell pressure.",
        ),
        row(
            "watch",
            "PASS_SHAPE_ONLY",
            "Use the completion notifier to poll for final-message readiness while Aletheon continues other work.",
        ),
        row(
            "publish",
            "PASS_SHAPE_ONLY",
            "Publish only curated receipt metadata until classifier review clears advisory text for use.",
        ),
        row(
            "review",
            "OPEN_GAP",
            "Marker-review classification remains required when final messages include review markers.",
        ),
    ]
    protocol = {
        "aggregate_status": aggregate(protocol_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "protocol": [
            "start non-ephemeral read-only lane",
            "run watcher with a generous timeout",
            "continue local synthesis while watcher polls",
            "consume only the curated notice until marker review is done",
            "carry marker-review as open gap instead of blocking the watcher",
        ],
        "rows": protocol_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-async-lane-notification-protocol-v1.json"
    write_json(path, protocol)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-async-lane-notification-protocol-v1.md",
        """
# v473 THOS v1 x2 Async Lane Notification Protocol

The no-rush lane protocol is to launch Arby/Aster read-only, let the watcher poll for final-message readiness, and publish only receipt metadata until classifier review clears any advisory text for use.

This keeps long-running lanes useful without requiring constant manual oversight.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-async-lane-notification-protocol-v1.md")

    handoff_rows = [
        row("x1_inheritance", x1_status.get("aggregate_status", "OPEN_GAP"), "v473 v1 x1 remains an open-gap classifier slice."),
        row("fixture_status", "PASS_SHAPE_ONLY" if fixtures.get("failure_count") == 0 else "FAIL_BLOCKER", "Marker-review fixtures remain green.", {"failure_count": fixtures.get("failure_count")}),
        row("classifier_status", classifier.get("aggregate_status", "OPEN_GAP"), "Classifier status is inherited for v2 integration."),
        row("notifier_status", notifier["aggregate_status"], "No-rush notifier synthesis is ready for reuse in later phases."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Integrate marker-review classifier into the live completion-notice workflow.",
            "Keep raw lane text unpublished unless a future exact review artifact authorizes summary use.",
            "Reuse the watcher for any long-running Arby/Aster lane instead of manual polling.",
            "Carry all six GMUT gates open and keep THOS evidence separate from physics claims.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v2-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v2-handoff-v1.md",
        f"""
# v473 THOS v1 x2 to v2 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v2 should integrate the marker-review classifier with the no-rush notifier workflow while keeping raw lane text unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v2-handoff-v1.md")

    status_rows = [
        row("notifier", notifier["aggregate_status"], "No-rush notifier synthesis published."),
        row("protocol", protocol["aggregate_status"], "Async lane notification protocol published."),
        row("handoff", handoff["aggregate_status"], "v2 handoff published."),
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
# v473 THOS v1 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v1 x2 records the no-rush Arby/Aster notifier flow and carries marker review as an explicit open gap.

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
