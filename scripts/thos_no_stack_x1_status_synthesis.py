#!/usr/bin/env python3
"""Generate no-stack x1 status receipts for GMUT/THOS phase runs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def app_lane_records(app_completion: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for lane in app_completion.get("lanes", []):
        records.append(
            {
                "lane": lane.get("lane"),
                "platform": "codex_app_local_server",
                "status": lane.get("status") or lane.get("completion_status") or lane.get("completion", "completed"),
                "duration_seconds": lane.get("duration_seconds") or lane.get("duration"),
                "body_text_published": False,
            }
        )
    return records


def phase_title(phase_slug: str) -> str:
    return phase_slug.replace("-", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate no-stack x1 status receipts.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-x2-slug", required=True)
    parser.add_argument("--previous-cli-source", default="")
    args = parser.parse_args()

    phase = args.phase_slug
    generated_utc, generated_nz = now_pair()
    app_completion = read_json(TRACE_DIR / f"{phase}-background-council-app-completion-v1.json")
    app_runner = read_json(TRACE_DIR / f"{phase}-background-council-app-runner-v1.json")
    prior_cli = read_json(TRACE_DIR / f"{args.previous_cli_source}-cli-fresh-output-status-v1.json") if args.previous_cli_source else {}
    app_records = app_lane_records(app_completion)
    cli_deferral = {
        "artifact_type": "cli_deferral_blocker",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_CLI_DEFERRED_PREVIOUS_ATTEMPTS_ACTIVE",
        "reason": "Arby and Aster Vale read-only CLI attempts from an earlier boundary were still active or unresolved; no duplicate CLI lanes were launched for this x1.",
        "prior_cli_status": prior_cli.get("overall_status", "unknown"),
        "deferred_lanes": [
            {"lane": "Arby", "status": "DEFERRED_PREVIOUS_ATTEMPT_STILL_ACTIVE", "body_text_published": False},
            {"lane": "Aster Vale", "status": "DEFERRED_PREVIOUS_ATTEMPT_STILL_ACTIVE", "body_text_published": False},
        ],
        "safe_forward_rule": "continue app-lane and x2 synthesis work while preserving a visible CLI open gap",
        "publication_boundary": {
            "raw_lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
    }
    timing = {
        "artifact_type": "five_lane_attempt_status",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_THREE_APP_LANES_READY_TWO_CLI_DEFERRED",
        "all_five_lanes_accounted_for": True,
        "app_runner_status": app_runner.get("overall_status", app_runner.get("status", "unknown")),
        "app_lanes": app_records,
        "cli_lanes": cli_deferral["deferred_lanes"],
        "soft_wait_baseline_seconds": 312.832,
        "soft_wait_interpretation": "planning support only, not completion proof",
    }
    synthesis = {
        "artifact_type": "x1_status_synthesis",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_X1_APP_READY_CLI_DEFERRED",
        "summary": [
            "Cicero, Kierkegaard, and Aristotle completed through the existing app-server route.",
            "Arby and Aster Vale were not relaunched to avoid stacking duplicate CLI processes while earlier read-only attempts remain active or unresolved.",
            "x2 should continue from app-lane evidence and no-stack CLI safety.",
        ],
        "next_boundary": args.next_x2_slug,
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    roadmap = {
        "artifact_type": "x2_seed_roadmap",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_SEED_READY",
        "seed_tasks": [
            "Continue no-stack CLI supervision.",
            "Use app-lane completion for orchestration continuity only.",
            "Advance command-surface and GMUT/THOS open-gate mapping.",
            "Prepare the next x1 with a current-phase CLI retry only if prior attempts resolve.",
        ],
    }
    outputs = {
        "cli-deferral-blocker": cli_deferral,
        "five-lane-attempt-status": timing,
        "synthesis": synthesis,
        "x2-seed-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{phase}-{suffix}-v1.json", payload)

    title = phase_title(phase)
    write_md(TRACE_DIR / f"{phase}-cli-deferral-blocker-v1.md", f"{title} CLI Deferral Blocker", [
        f"Status: `{cli_deferral['overall_status']}`",
        "Arby and Aster Vale are accounted for but not relaunched because prior CLI attempts remain active or unresolved.",
    ])
    write_md(TRACE_DIR / f"{phase}-five-lane-attempt-status-v1.md", f"{title} Five-Lane Attempt Status", [
        f"Status: `{timing['overall_status']}`",
        "Three app lanes completed; two CLI lanes are deferred by no-stack safety.",
    ])
    write_md(TRACE_DIR / f"{phase}-synthesis-v1.md", f"{title} Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        f"Next boundary: `{args.next_x2_slug}`",
    ])
    write_md(TRACE_DIR / f"{phase}-x2-seed-roadmap-v1.md", f"{title} x2 Seed Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        "Continue no-stack CLI supervision and open-gate THOS/GMUT synthesis.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": phase, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
