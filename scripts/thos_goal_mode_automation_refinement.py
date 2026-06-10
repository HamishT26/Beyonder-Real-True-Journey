#!/usr/bin/env python3
"""Create a status-only goal-mode automation refinement receipt.

This helper captures the current operating rules for the v491-v515 GMUT/THOS
phase run without reading raw sibling output or mutating app, CLI, plugin, or
skill state.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


APPROVAL_CANDIDATES = [
    {
        "id": "goal-mode-automation-01",
        "title": "Five-Minute Lane Health Cadence",
        "scope": "Keep app and CLI lane checks to bounded five-minute harvests while allowing productive x2 work between checks.",
    },
    {
        "id": "goal-mode-automation-02",
        "title": "Node Entrypoint First CLI Policy",
        "scope": "Require the node codex.js bridge for CLI launchers when available, with the Windows entrypoint kept as fallback only.",
    },
    {
        "id": "goal-mode-automation-03",
        "title": "Existing-Lane Continuity Gate",
        "scope": "Use only existing Cicero, Kierkegaard, Aristotle app routes and Arby/Aster Vale read-only CLI lanes; no replacement threads or old-style subagents.",
    },
    {
        "id": "goal-mode-automation-04",
        "title": "Watcher Trust With Scheduled Harvest",
        "scope": "Let watcher and notifier receipts supervise lanes between scheduled checks instead of manual babysitting.",
    },
    {
        "id": "goal-mode-automation-05",
        "title": "X2 Build Run Test Install Use Discipline",
        "scope": "Use x2 sessions to implement, run, validate, and apply the safest high-value tasks prepared by x1 lanes.",
    },
    {
        "id": "goal-mode-automation-06",
        "title": "Vision Card and Compact Refresh Failsafe",
        "scope": "Require a compact current-state vision receipt at every phase start and Codex compact refresh point.",
    },
    {
        "id": "goal-mode-automation-07",
        "title": "Omega-Line v2 Continuity Surface",
        "scope": "Keep omega-line and omega-line-v2 aligned while indexing only the most relevant Journey, THOS, GMUT, Freed ID/CBR, runner, and approval artifacts.",
    },
    {
        "id": "goal-mode-automation-08",
        "title": "Latest-Essential Helper Stack",
        "scope": "Prefer current runner, notifier, redactor, quality, classifier, IPC, and phase-gate helpers over older versioned helpers.",
    },
    {
        "id": "goal-mode-automation-09",
        "title": "Ten Approval Candidates Per Phase",
        "scope": "Prepare at least 10 scoped approval candidates per phase for future user authorization without blocking already-approved work.",
    },
    {
        "id": "goal-mode-automation-10",
        "title": "Open-Gate GMUT THOS Boundary",
        "scope": "Keep GMUT, canon, consciousness, final-physics, and public-claim gates open unless exact future closure artifacts prove otherwise.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve(path: str | None) -> Path | None:
    if not path:
        return None
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def read_receipt(path: str | None) -> dict[str, Any]:
    candidate = resolve(path)
    if candidate is None:
        return {"available": False, "file": None, "status": "not_provided"}
    if not candidate.exists():
        return {"available": False, "file": candidate.name, "status": "missing"}
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"available": False, "file": candidate.name, "status": "json_parse_failed"}
    if not isinstance(payload, dict):
        return {"available": False, "file": candidate.name, "status": "not_object"}
    return {
        "available": True,
        "file": candidate.name,
        "status": str(
            payload.get("overall_status")
            or payload.get("aggregate_status")
            or payload.get("status")
            or "status_missing"
        ),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    receipts = {
        "app_runner": read_receipt(args.app_runner_json),
        "app_gate": read_receipt(args.app_gate_json),
        "cli_launcher": read_receipt(args.cli_launcher_json),
        "cli_check": read_receipt(args.cli_check_json),
        "cli_quality": read_receipt(args.cli_quality_json),
        "cli_marker_review": read_receipt(args.cli_marker_review_json),
        "x2_acceptance": read_receipt(args.acceptance_json),
        "next_handoff": read_receipt(args.handoff_json),
    }
    runtime_gaps = []
    marker_review_resolved = (
        receipts["cli_check"]["status"] == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"
        and receipts["cli_quality"]["status"].startswith("PASS_")
        and receipts["cli_marker_review"]["status"] == "PASS_MARKER_REVIEW_LEDGER"
    )
    for name, row in receipts.items():
        if not row["available"] or not str(row["status"]).startswith("OPEN_GAP"):
            continue
        if name == "cli_check" and marker_review_resolved:
            continue
        runtime_gaps.append(f"{name}:{row['status']}")
    missing_required = [
        name
        for name in [
            "cli_launcher",
            "cli_check",
            "cli_quality",
            "cli_marker_review",
            "x2_acceptance",
            "next_handoff",
        ]
        if not receipts[name]["available"]
    ]
    return {
        "artifact_type": "goal_mode_automation_refinement",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_GOAL_MODE_AUTOMATION_REFINEMENT_READY"
        if not missing_required
        else "OPEN_GAP_GOAL_MODE_AUTOMATION_REFINEMENT",
        "missing_required_receipts": missing_required,
        "current_runtime_gaps": runtime_gaps,
        "receipt_statuses": receipts,
        "resolved_open_gap_notes": [
            "cli_check marker-review warning resolved by quality gate plus PASS_MARKER_REVIEW_LEDGER"
        ]
        if marker_review_resolved
        else [],
        "automation_rules": {
            "five_minute_lane_checks": True,
            "manual_babysitting_between_checks": False,
            "work_while_watchers_run": True,
            "node_entrypoint_first": True,
            "windows_entrypoint_fallback_allowed": True,
            "x1_uses_all_five_existing_lanes": True,
            "x2_build_run_test_install_use": True,
            "phase_start_vision_card_required": True,
            "compact_refresh_vision_card_required": True,
            "ten_approval_candidates_per_phase": True,
            "omega_line_v2_continuity_index_required": True,
            "duration_is_completion_proof": False,
        },
        "approval_candidates": APPROVAL_CANDIDATES,
        "next_actions": [
            "Harvest the r3 app-lane watcher after the next five-minute cadence point.",
            "Use the CLI quality and marker-review pass as safe x2 input without publishing raw lane text.",
            "Keep building v504 v5 x2 artifacts while app lanes complete through the longer watcher.",
            "Launch v504 v6 x1 only after all five lanes are complete or a curated blocker receipt is present.",
        ],
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "prompt_body_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Goal Mode Automation Refinement",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Current Runtime Gaps",
    ]
    if payload["current_runtime_gaps"]:
        lines.extend(f"- `{gap}`" for gap in payload["current_runtime_gaps"])
    else:
        lines.append("- none")
    lines.extend(["", "## Automation Rules"])
    for key, value in payload["automation_rules"].items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(["", "## Approval Candidates"])
    for candidate in payload["approval_candidates"]:
        lines.append(f"- {candidate['id']}: {candidate['title']} - {candidate['scope']}")
    lines.extend(["", "## Next Actions"])
    lines.extend(f"- {item}" for item in payload["next_actions"])
    lines.extend(
        [
            "",
            "Boundary: status-only refinement; no raw lane text, logs, prompt bodies, session streams, screenshots, credentials, or local absolute paths.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--app-runner-json")
    parser.add_argument("--app-gate-json")
    parser.add_argument("--cli-launcher-json")
    parser.add_argument("--cli-check-json")
    parser.add_argument("--cli-quality-json")
    parser.add_argument("--cli-marker-review-json")
    parser.add_argument("--acceptance-json")
    parser.add_argument("--handoff-json")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
