#!/usr/bin/env python3
"""Build v486 GMUT/THOS v5 x1 receipts with CLI deferral blocker."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v5-x1"
PREVIOUS = "v486-gmut-thos-v22-v4-x1"


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


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app_completion = read_json(TRACE_DIR / f"{PHASE}-background-council-app-completion-v1.json")
    app_runner = read_json(TRACE_DIR / f"{PHASE}-background-council-app-runner-v1.json")
    prior_cli = read_json(TRACE_DIR / f"{PREVIOUS}-cli-fresh-output-status-v1.json")
    app_records = app_lane_records(app_completion)
    cli_deferral = {
        "artifact_type": "cli_deferral_blocker",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_CLI_DEFERRED_PREVIOUS_ATTEMPTS_ACTIVE",
        "reason": "Arby and Aster Vale read-only CLI attempts from the prior x1 boundary were still active with no final messages; no duplicate CLI lanes were launched for v5 x1.",
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
        "phase_slug": PHASE,
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
    source_refresh = {
        "artifact_type": "source_refresh_carry_forward",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SOURCE_REFRESH_CARRY_FORWARD",
        "sources": [
            {
                "label": "OpenAI Codex CLI docs",
                "url": "https://developers.openai.com/codex/cli",
                "use": "Continue official CLI and Windows/PowerShell runner alignment.",
            },
            {
                "label": "OpenAI Codex GitHub releases",
                "url": "https://github.com/openai/codex/releases",
                "use": "Track stable-vs-alpha release posture before any future update proposal.",
            },
            {
                "label": "MCP security best practices",
                "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices",
                "use": "Keep connector and tool routing explicit and least-privileged.",
            },
        ],
    }
    synthesis = {
        "artifact_type": "x1_status_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_V5_X1_APP_READY_CLI_DEFERRED",
        "summary": [
            "Cicero, Kierkegaard, and Aristotle completed through the existing app-server route.",
            "Arby and Aster Vale were not relaunched to avoid stacking duplicate CLI processes while prior read-only attempts remain active.",
            "x2 should convert this into a no-stack CLI supervisor rule and continue safe THOS/GMUT preparation.",
        ],
        "next_boundary": "v486-gmut-thos-v22-v5-x2",
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    roadmap = {
        "artifact_type": "v5_x2_seed_roadmap",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V5_X2_SEED_READY",
        "seed_tasks": [
            "Build no-stack CLI lane supervisor rules.",
            "Design a stale-process watcher receipt that avoids raw process command lines.",
            "Fold app-lane completion into command-surface and GMUT/THOS open-gate work.",
            "Prepare v6 x1 to retry CLI only after prior attempts finish or are explicitly handled.",
        ],
    }
    outputs = {
        "cli-deferral-blocker": cli_deferral,
        "five-lane-attempt-status": timing,
        "source-refresh": source_refresh,
        "synthesis": synthesis,
        "v5-x2-seed-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(TRACE_DIR / f"{PHASE}-cli-deferral-blocker-v1.md", f"{PHASE} CLI Deferral Blocker", [
        f"Status: `{cli_deferral['overall_status']}`",
        "Arby and Aster Vale were accounted for but not relaunched because prior CLI attempts were still active.",
        "Raw process details and lane outputs are not published.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-five-lane-attempt-status-v1.md", f"{PHASE} Five-Lane Attempt Status", [
        f"Status: `{timing['overall_status']}`",
        "Three app lanes completed; two CLI lanes are deferred by no-stack safety.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-source-refresh-v1.md", f"{PHASE} Source Refresh", [
        f"Status: `{source_refresh['overall_status']}`",
        "Official Codex, release, and MCP security sources carry forward into x2 design.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-synthesis-v1.md", f"{PHASE} Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        "x2 should continue from app-lane evidence and no-stack CLI safety.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-v5-x2-seed-roadmap-v1.md", f"{PHASE} v5 x2 Seed Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        "Build no-stack CLI supervisor rules and continue command/GMUT open-gate work.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "overall_status": synthesis["overall_status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
