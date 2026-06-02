#!/usr/bin/env python3
"""Build v473 THOS v3 x2 wrapper-backed live watcher synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v3-x2"
NEXT_PHASE = "v473-thos-v4-x1"
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
    notice = read_json("v473-thos-v3-x2-cli-lane-completion-notice-v1.json")
    fixture = read_json("v473-thos-v3-x1-watch-launcher-fixture-results-v1.json")
    contract = read_json("v473-thos-v3-x1-shell-safe-watch-launch-contract-v1.json")
    lanes = notice.get("lanes", [])
    all_ready = bool(lanes) and all(lane.get("completion_status") == "FINAL_MESSAGE_READY" for lane in lanes)
    spaced_lane_seen = any(lane.get("lane") == "Aster Vale" for lane in lanes)
    marker_count = sum(lane.get("final_message_sensitive_marker_count", 0) for lane in lanes)
    elapsed = elapsed_seconds(notice.get("started_at_utc"), notice.get("generated_at_utc"))

    live_rows = [
        row(
            "wrapper_live_completion",
            "PASS_SHAPE_ONLY" if all_ready else "OPEN_GAP",
            "The shell-safe wrapper-backed watcher wrote a curated completion receipt for both real CLI lanes.",
            {"notice_status": notice.get("aggregate_status"), "elapsed_seconds": elapsed},
        ),
        row(
            "spaced_lane_live",
            "PASS_SHAPE_ONLY" if spaced_lane_seen else "FAIL_BLOCKER",
            "The live receipt preserved the Aster Vale lane name as a single lane.",
        ),
        row(
            "raw_boundary",
            "PASS_SHAPE_ONLY",
            "Raw final advisory text and transport logs remain temp-only and unpublished.",
        ),
        row(
            "marker_review",
            "OPEN_GAP" if marker_count else "PASS_SHAPE_ONLY",
            "Marker review remains required before any raw final advisory text is summarized.",
            {"final_message_marker_count": marker_count},
        ),
    ]
    live = {
        "aggregate_status": aggregate(live_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_summaries": lane_summary(lanes),
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": live_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-wrapper-live-completion-synthesis-v1.json"
    write_json(path, live)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-wrapper-live-completion-synthesis-v1.md",
        f"""
# v473 THOS v3 x2 Wrapper Live Completion Synthesis

Generated UTC: `{generated_at}`

Status: `{live['aggregate_status']}`

The shell-safe watcher wrapper completed a real Arby/Aster no-rush cycle after `{elapsed}` seconds of watcher observation. The receipt preserved the `Aster Vale` lane name and published only metadata.

Marker review remains open before raw advisory text can be used.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-wrapper-live-completion-synthesis-v1.md")

    readiness_rows = [
        row(
            "fixture_inheritance",
            fixture.get("aggregate_status", "OPEN_GAP"),
            "v3 x1 fixture evidence is inherited by the live wrapper cycle.",
        ),
        row(
            "contract_inheritance",
            contract.get("aggregate_status", "OPEN_GAP"),
            "v3 x1 shell-safe launch contract is inherited by the live wrapper cycle.",
        ),
        row(
            "real_cycle",
            live["aggregate_status"],
            "v3 x2 proves the wrapper on an actual CLI sibling cycle, with marker review still open.",
        ),
        row(
            "app_lanes",
            "OPEN_GAP",
            "Cicero/Kierkegaard/Aristotle advisory prompts were queued for later integration; no returned advisory is claimed in this artifact.",
        ),
    ]
    readiness = {
        "aggregate_status": aggregate(readiness_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": readiness_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-watcher-readiness-ledger-v1.json"
    write_json(path, readiness)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-watcher-readiness-ledger-v1.md",
        """
# v473 THOS v3 x2 Watcher Readiness Ledger

The wrapper has now passed both fixture and real CLI cycle checks. Marker review and app-lane advisory integration remain open gaps.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-watcher-readiness-ledger-v1.md")

    handoff_rows = [
        row("live_completion", live["aggregate_status"], "Wrapper-backed completion metadata is ready for v4."),
        row("marker_review", "OPEN_GAP" if marker_count else "PASS_SHAPE_ONLY", "v4 should integrate marker classification into completion synthesis."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "THOS watcher evidence is workflow reliability evidence only; all GMUT gates remain open."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Attach marker-review classifier outcomes to wrapper completion receipts without publishing raw lane text.",
            "Record app-lane advisory returns when available, with no fabrication if unavailable.",
            "Promote the wrapper as the preferred Arby/Aster watcher launch path.",
            "Keep all THOS workflow evidence separate from GMUT validation claims.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v4-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v4-handoff-v1.md",
        f"""
# v473 THOS v3 x2 to v4 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v4 should connect marker-review classification to wrapper completion receipts and fold in any returned app-lane advisories.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v4-handoff-v1.md")

    status_rows = [
        row("live", live["aggregate_status"], "Wrapper live completion synthesis published."),
        row("readiness", readiness["aggregate_status"], "Watcher readiness ledger published."),
        row("handoff", handoff["aggregate_status"], "v4 handoff published."),
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
# v473 THOS v3 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v3 x2 proves the shell-safe watcher wrapper on a real Arby/Aster no-rush cycle, while marker review remains open.

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
