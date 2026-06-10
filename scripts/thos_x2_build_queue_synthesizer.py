#!/usr/bin/env python3
"""Synthesize a THOS/GMUT x2 build queue from curated x1 status receipts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} is not a JSON object")
    return payload


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def has_safe_boundary(payload: dict[str, Any]) -> bool:
    boundary = payload.get("publication_boundary")
    if not isinstance(boundary, dict):
        return True
    forbidden = [
        "raw_lane_text_published",
        "raw_logs_published",
        "prompt_body_published",
        "session_streams_published",
        "screenshots_published",
        "credentials_published",
        "local_absolute_paths_published",
    ]
    return all(boundary.get(key) is False for key in forbidden if key in boundary)


def lane_summary(five_lane: dict[str, Any]) -> dict[str, Any]:
    rows = five_lane.get("lanes", [])
    app = [row for row in rows if row.get("surface") == "app"]
    cli = [row for row in rows if row.get("surface") == "cli"]
    return {
        "app_lane_count": len(app),
        "cli_lane_count": len(cli),
        "app_lanes_ready": all(str(row.get("overall_status")) == "completed" for row in app),
        "cli_lanes_ready": all(str(row.get("completion_status")) == "FINAL_MESSAGE_READY" for row in cli),
        "cli_quality_ready": all(str(row.get("quality_status")) == "PASS_ELABORATION_GATE" for row in cli),
        "raw_boundary": "status_only",
    }


def build_actions(eureka: dict[str, Any], research: dict[str, Any], prep: dict[str, Any]) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    for item in eureka.get("eureka_tasks_for_x2", [])[:8]:
        actions.append(
            {
                "source": "x1_eureka_wait_task_plan",
                "action": str(item),
                "x2_mode": "design_build_test_use",
            }
        )
    for item in research.get("x2_build_implications", [])[:4]:
        actions.append(
            {
                "source": "x1_productive_wait_research",
                "action": str(item),
                "x2_mode": "source_backed_hardening",
            }
        )
    for item in prep.get("build_queue", [])[:6]:
        actions.append(
            {
                "source": "x2_prep_start",
                "action": str(item),
                "x2_mode": "implementation_queue",
            }
        )
    return actions


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} x2 Build Queue Synthesizer",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- source_receipts_ready: `{payload['source_receipts_ready']}`",
        f"- lane_summary: app `{payload['lane_summary']['app_lane_count']}`, cli `{payload['lane_summary']['cli_lane_count']}`",
        "",
        "## Build Actions",
    ]
    for index, action in enumerate(payload["build_actions"], start=1):
        lines.append(f"- {index}. `{action['x2_mode']}`: {action['action']}")
    lines.extend(
        [
            "",
            "Boundary: status-only synthesis; raw sibling text, prompts, logs, screenshots, credentials, session streams, and local absolute paths are not published.",
            "",
            "Claim boundary: GMUT and canon gates remain open; duration is not completion proof.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--five-lane-json", required=True)
    parser.add_argument("--phase-advance-json", required=True)
    parser.add_argument("--research-json", required=True)
    parser.add_argument("--eureka-json", required=True)
    parser.add_argument("--next-prep-json", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    closeout = read_json(Path(args.closeout_json))
    five_lane = read_json(Path(args.five_lane_json))
    phase_advance = read_json(Path(args.phase_advance_json))
    research = read_json(Path(args.research_json))
    eureka = read_json(Path(args.eureka_json))
    prep = read_json(Path(args.next_prep_json))
    receipts = {
        "closeout": closeout,
        "five_lane": five_lane,
        "phase_advance": phase_advance,
        "research": research,
        "eureka": eureka,
        "next_prep": prep,
    }
    source_receipts_ready = (
        status(closeout).startswith("PASS_")
        and status(five_lane) == "PASS_FIVE_LANE_READY"
        and status(phase_advance) == "PASS_PHASE_ADVANCE_GATE"
        and status(research).startswith("PASS_")
        and status(eureka).startswith("PASS_")
        and status(prep).startswith("PASS_")
        and all(has_safe_boundary(payload) for payload in receipts.values())
    )
    actions = build_actions(eureka, research, prep)
    payload: dict[str, Any] = {
        "artifact_type": "x2_build_queue_synthesizer",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_BUILD_QUEUE_SYNTHESIZED" if source_receipts_ready and actions else "OPEN_GAP_X2_BUILD_QUEUE",
        "source_receipts_ready": source_receipts_ready,
        "source_statuses": {name: status(payload) for name, payload in receipts.items()},
        "lane_summary": lane_summary(five_lane),
        "build_actions": actions,
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
            "duration_is_completion_proof": False,
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if str(payload["overall_status"]).startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
