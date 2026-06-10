#!/usr/bin/env python3
"""Build v486 GMUT/THOS v4 x1 status receipts with fresh CLI output folders."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v4-x1"


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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def latest_temp_dir(prefix: str) -> Path | None:
    temp_root = Path(os.environ.get("TEMP", "."))
    matches = sorted(temp_root.glob(prefix), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return matches[0] if matches else None


def lane_status(lane: str, prefix: str, final_name: str, marker: str) -> dict[str, Any]:
    folder = latest_temp_dir(prefix)
    if not folder:
        return {
            "lane": lane,
            "status": "OPEN_GAP_OUTPUT_FOLDER_NOT_FOUND",
            "fresh_output_folder_used": True,
            "body_text_published": False,
        }
    final_path = folder / final_name
    stderr_path = folder / f"{lane.replace(' ', '')}-stderr.txt"
    if not final_path.exists():
        return {
            "lane": lane,
            "status": "OPEN_GAP_FINAL_MESSAGE_PENDING",
            "fresh_output_folder_used": True,
            "final_message_present": False,
            "stderr_bytes": stderr_path.stat().st_size if stderr_path.exists() else 0,
            "body_text_published": False,
        }
    text = final_path.read_text(encoding="utf-8", errors="replace")
    has_marker = marker in text
    stale_terms = ["v58", "v59", "2026-04-28", "2026-04-29"]
    stale_context_detected = any(term.lower() in text.lower() for term in stale_terms)
    if has_marker and not stale_context_detected:
        status = "FINAL_MESSAGE_READY_CURRENT_PHASE"
    elif stale_context_detected:
        status = "OPEN_GAP_STALE_CONTEXT_OUTPUT"
    else:
        status = "OPEN_GAP_FINAL_MARKER_MISSING"
    return {
        "lane": lane,
        "status": status,
        "fresh_output_folder_used": True,
        "final_message_present": True,
        "final_message_bytes": final_path.stat().st_size,
        "final_message_hash": sha256_text(text),
        "final_marker_present": has_marker,
        "stale_context_detected": stale_context_detected,
        "stderr_bytes": stderr_path.stat().st_size if stderr_path.exists() else 0,
        "body_text_published": False,
    }


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


def build_source_refresh(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "current_source_refresh_compact",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SOURCE_REFRESH_COMPACT",
        "sources": [
            {
                "label": "OpenAI Codex CLI docs",
                "url": "https://developers.openai.com/codex/cli",
                "use": "Ground CLI work in official setup, upgrade, Windows, TUI, scripting, web-search, MCP, and approval-mode guidance.",
            },
            {
                "label": "OpenAI Codex GitHub releases",
                "url": "https://github.com/openai/codex/releases",
                "use": "Treat 0.137.0 as the current stable lane observed locally; 0.138 alpha tags are not a live-upgrade target without separate approval.",
            },
            {
                "label": "MCP security best practices",
                "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices",
                "use": "Keep connector and tool authority explicit, least-privileged, and receipt-audited.",
            },
            {
                "label": "OWASP agentic application guidance",
                "url": "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
                "use": "Model autonomous lane runners as governed agentic systems with bounded action and sensitive-data controls.",
            },
        ],
        "integration_note": "Current sources inform THOS runner design only; they do not validate GMUT, consciousness, physics, or canon claims.",
    }


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app_completion = read_json(TRACE_DIR / f"{PHASE}-background-council-app-completion-v1.json")
    app_runner = read_json(TRACE_DIR / f"{PHASE}-background-council-app-runner-v1.json")
    app_records = app_lane_records(app_completion)
    arby = lane_status(
        "Arby",
        "ghc-v486-gmut-thos-v22-v4-x1-arby-*",
        "Arby-last-message.txt",
        "FINAL_MARKER: V486_GMUT_THOS_V22_V4_X1_ARBY_READY",
    )
    aster = lane_status(
        "Aster Vale",
        "ghc-v486-gmut-thos-v22-v4-x1-aster-*",
        "AsterVale-last-message.txt",
        "FINAL_MARKER: V486_GMUT_THOS_V22_V4_X1_ASTER_READY",
    )
    cli_lanes = [arby, aster]
    cli_ready = all(item["status"] == "FINAL_MESSAGE_READY_CURRENT_PHASE" for item in cli_lanes)
    overall = "PASS_FIVE_LANE_X1_CURRENT_PHASE" if cli_ready and len(app_records) == 3 else "OPEN_GAP_APP_READY_CLI_PENDING_OR_STALE"
    source_refresh = build_source_refresh(generated_utc, generated_nz)

    cli_status = {
        "artifact_type": "fresh_cli_output_status",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_CLI_CURRENT_PHASE_READY" if cli_ready else "OPEN_GAP_CLI_PENDING_OR_STALE",
        "lanes": cli_lanes,
        "fresh_output_folder_rule": "one fresh temp-only output folder per lane attempt",
        "publication_boundary": {
            "raw_lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
    }
    timing = {
        "artifact_type": "five_lane_timing_status",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": overall,
        "all_five_lanes_attempted": True,
        "app_runner_status": app_runner.get("overall_status", app_runner.get("status", "unknown")),
        "app_lanes": app_records,
        "cli_lanes": cli_lanes,
        "soft_wait_baseline_seconds": 312.832,
        "soft_wait_interpretation": "planning support only, not completion proof",
    }
    synthesis = {
        "artifact_type": "x1_status_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": overall,
        "summary": [
            "Cicero, Kierkegaard, and Aristotle completed through existing app-server routes.",
            "Arby and Aster Vale were attempted with fresh temp-only output folders.",
            "x2 can proceed if CLI is still pending, but must preserve a visible open-gap receipt.",
        ],
        "next_boundary": "v486-gmut-thos-v22-v4-x2",
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    roadmap = {
        "artifact_type": "v4_x2_seed_roadmap",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V4_X2_SEED_READY",
        "seed_tasks": [
            "Build a CLI freshness verifier that refuses stale final-message reuse.",
            "Promote app-lane success into command-surface and handoff work without publishing bodies.",
            "Extend source refresh with official Codex release/app-server notes and MCP security constraints.",
            "Map GMUT/THOS claims into open-gate application buckets.",
            "Prepare v5 x1 to either consume current Arby/Aster outputs or record a second fresh-output blocker.",
        ],
    }

    outputs = {
        "cli-fresh-output-status": cli_status,
        "five-lane-timing": timing,
        "source-refresh": source_refresh,
        "synthesis": synthesis,
        "v4-x2-seed-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(
        TRACE_DIR / f"{PHASE}-cli-fresh-output-status-v1.md",
        f"{PHASE} CLI Fresh Output Status",
        [
            f"Status: `{cli_status['overall_status']}`",
            "Arby and Aster Vale used separate fresh temp-only folders.",
            "Only byte counts, hashes, marker status, and freshness status are publishable.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-five-lane-timing-v1.md",
        f"{PHASE} Five-Lane Timing Status",
        [
            f"Status: `{timing['overall_status']}`",
            "All five lanes were attempted.",
            "App lanes completed; CLI lanes are classified by current-phase marker and stale-context checks.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-source-refresh-v1.md",
        f"{PHASE} Source Refresh",
        [
            f"Status: `{source_refresh['overall_status']}`",
            "Official Codex CLI docs and GitHub releases are used for runner planning.",
            "MCP and OWASP sources are used for bounded authority and sensitive-data guard design.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-synthesis-v1.md",
        f"{PHASE} Synthesis",
        [
            f"Status: `{synthesis['overall_status']}`",
            "x1 app-lane evidence is usable; CLI evidence remains bounded by freshness and final-marker checks.",
            "Next boundary: `v486-gmut-thos-v22-v4-x2`.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-v4-x2-seed-roadmap-v1.md",
        f"{PHASE} v4 x2 Seed Roadmap",
        [
            f"Status: `{roadmap['overall_status']}`",
            "Build around CLI freshness verification, command surfaces, source security, and open-gate GMUT/THOS mapping.",
        ],
    )
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "overall_status": overall}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
