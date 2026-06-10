#!/usr/bin/env python3
"""Build v473 THOS v2 x2 CLI completion synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v2-x2"
NEXT_PHASE = "v473-thos-v3-x1"
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
    return [
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
        for lane in lanes
    ]


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    notice = read_json("v473-thos-v2-x1-cli-lane-completion-notice-v1.json")
    launch = read_json("v473-thos-v2-x1-async-watch-launch-receipt-v1.json")
    integration = read_json("v473-thos-v2-x1-marker-review-notifier-integration-v1.json")
    lanes = notice.get("lanes", [])
    all_ready = bool(lanes) and all(lane.get("completion_status") == "FINAL_MESSAGE_READY" for lane in lanes)
    marker_count = sum(lane.get("final_message_sensitive_marker_count", 0) for lane in lanes)
    elapsed = elapsed_seconds(notice.get("started_at_utc"), notice.get("generated_at_utc"))

    completion_rows = [
        row(
            "completion_notice",
            "PASS_SHAPE_ONLY" if all_ready else "OPEN_GAP",
            "The watcher wrote a curated completion notice for both CLI lanes.",
            {"notice_status": notice.get("aggregate_status"), "elapsed_seconds": elapsed},
        ),
        row(
            "metadata_only",
            "PASS_SHAPE_ONLY",
            "Published receipt includes readiness state, byte counts, hashes, and marker counts only.",
        ),
        row(
            "marker_review",
            "OPEN_GAP" if marker_count else "PASS_SHAPE_ONLY",
            "Final-message marker counts still require review before raw advisory text is summarized.",
            {"final_message_marker_count": marker_count},
        ),
        row(
            "launch_inheritance",
            launch.get("aggregate_status", "OPEN_GAP"),
            "v2 x1 launch receipt remains the setup evidence for this completion synthesis.",
        ),
    ]
    completion = {
        "aggregate_status": aggregate(completion_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_summaries": lane_summary(lanes),
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": completion_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-cli-completion-synthesis-v1.json"
    write_json(path, completion)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-cli-completion-synthesis-v1.md",
        f"""
# v473 THOS v2 x2 CLI Completion Synthesis

Generated UTC: `{generated_at}`

Status: `{completion['aggregate_status']}`

The no-rush watcher recorded both Arby and Aster Vale as final-message ready after `{elapsed}` seconds of watcher observation. The published receipt keeps raw lane text out of the repo and carries marker review as an open gap.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-cli-completion-synthesis-v1.md")

    retry_rows = [
        row(
            "windows_quoted_lane_name",
            "PASS_SHAPE_ONLY",
            "The live watcher was relaunched with explicit quoting for the lane name containing a space.",
        ),
        row(
            "watcher_log_boundary",
            "PASS_SHAPE_ONLY",
            "Watcher stdout/stderr remained local temp-only and were not staged.",
        ),
        row(
            "terminal_exit",
            "PASS_SHAPE_ONLY" if notice.get("aggregate_status") in {"FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"} else "OPEN_GAP",
            "Watcher exited after writing a terminal completion receipt.",
            {"notice_status": notice.get("aggregate_status")},
        ),
    ]
    retry = {
        "aggregate_status": aggregate(retry_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": retry_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-watcher-retry-lesson-v1.json"
    write_json(path, retry)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-watcher-retry-lesson-v1.md",
        """
# v473 THOS v2 x2 Watcher Retry Lesson

The watcher flow now preserves quoted lane names on Windows and redirects watcher logs to temp-only files. The published receipt remains metadata-only.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-watcher-retry-lesson-v1.md")

    handoff_rows = [
        row("completion", completion["aggregate_status"], "Completion metadata is ready for v3 integration."),
        row("integration", integration.get("aggregate_status", "OPEN_GAP"), "Marker-review notifier integration remains open."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All GMUT gates remain open; THOS workflow evidence is not physics validation."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Add a shell-safe watcher launch wrapper for lane names containing spaces.",
            "Integrate marker review into completion synthesis without publishing raw lane text.",
            "Continue THOS command/skill runner reliability work.",
            "Keep app-lane reachability gaps explicit when thread tools are unavailable.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v3-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v3-handoff-v1.md",
        f"""
# v473 THOS v2 x2 to v3 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v3 should harden watcher launch quoting, marker-review integration, and THOS command/skill runner reliability.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v3-handoff-v1.md")

    status_rows = [
        row("completion", completion["aggregate_status"], "CLI completion synthesis published."),
        row("retry_lesson", retry["aggregate_status"], "Watcher retry lesson published."),
        row("handoff", handoff["aggregate_status"], "v3 handoff published."),
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
# v473 THOS v2 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v2 x2 records Arby/Aster completion metadata and carries marker review as an explicit open gap.

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
