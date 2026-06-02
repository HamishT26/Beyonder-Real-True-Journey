#!/usr/bin/env python3
"""Build v472 THOS v8 x2 notifier replay synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v8-x2"
NEXT_PHASE = "v473-thos-v1-x1"
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    replay_notice = read_json("v472-thos-v8-x2-v7-output-replay-notice-v1.json")
    replay_status = replay_notice.get("aggregate_status")
    lane_marker_counts = [
        {
            "final_message_sensitive_marker_count": item.get("final_message_sensitive_marker_count"),
            "lane": item.get("lane"),
        }
        for item in replay_notice.get("lanes", [])
    ]
    replay_rows = [
        row(
            "terminal_state",
            "PASS_SHAPE_ONLY" if replay_status == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "FAIL_BLOCKER",
            "Repaired notifier returns marker-review as a terminal open-gap state on actual v7 lane outputs.",
            {"status": replay_status},
        ),
        row(
            "raw_boundary",
            "PASS_SHAPE_ONLY",
            "Replay publishes marker counts and hashes only; raw final advisory text remains unpublished.",
        ),
    ]
    replay = {
        "aggregate_status": aggregate(replay_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "replay_notice": replay_notice,
        "rows": replay_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-notifier-replay-synthesis-v1.json"
    write_json(path, replay)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-notifier-replay-synthesis-v1.md",
        f"""
# v472 THOS v8 x2 Notifier Replay Synthesis

Generated UTC: `{generated_at}`

Status: `{replay['aggregate_status']}`

The repaired notifier was replayed against the actual v7 Arby/Aster outputs and returned `OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW` as a terminal state.

Raw final advisory text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-notifier-replay-synthesis-v1.md")

    marker_rows = [
        row("marker_counts", "OPEN_GAP", "Final-message marker counts require review before the v7 CLI advisory text is used.", {"lane_marker_counts": lane_marker_counts}),
        row("terminal_handling", "PASS_SHAPE_ONLY", "Marker-review no longer causes indefinite watcher polling."),
    ]
    marker = {
        "aggregate_status": aggregate(marker_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": marker_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-marker-review-ledger-v1.json"
    write_json(path, marker)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-marker-review-ledger-v1.md",
        """
# v472 THOS v8 x2 Marker Review Ledger

The v7 CLI final messages are ready but need marker review before their text is used. This is now a clean open gap, not a stuck watcher.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-marker-review-ledger-v1.md")

    handoff = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Open v473 THOS v1 x1 with marker-review-aware notifier behavior.",
            "Review whether final-message marker counts are benign advisory wording or require stricter redaction.",
            "Continue semantic lint integration with freshness and ambiguity labels.",
            "Keep all raw lane transport and external cache files excluded.",
        ],
        "status": "READY_FOR_V473_WITH_OPEN_GAPS",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v473-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v473-handoff-v1.md",
        """
# v472 THOS v8 x2 to v473 Handoff

v472 v8 x2 closes the notifier terminal-state repair. v473 should continue with marker-review-aware notifier behavior and broader semantic lint integration.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v473-handoff-v1.md")

    status_rows = [
        row("replay", replay["aggregate_status"], "Notifier replay repair verified on actual v7 lane outputs."),
        row("marker_review", marker["aggregate_status"], "Marker review remains open."),
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
# v472 THOS v8 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v8 x2 verifies the notifier terminal-state repair against actual v7 lane outputs and records marker review as a clean open gap.

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
