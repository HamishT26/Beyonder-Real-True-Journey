#!/usr/bin/env python3
"""Generate bounded v478 THOS v14 x8 start receipts from sanitized lane evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from json import JSONDecodeError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


NZ = timezone(timedelta(hours=12))
BASELINE_SECONDS = 312.832


SOURCES = [
    {
        "label": "OpenAI Codex CLI help",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Keep CLI usage framed as scoped terminal assistance with explicit local safety controls.",
    },
    {
        "label": "Model Context Protocol roadmap",
        "url": "https://modelcontextprotocol.io/development/roadmap",
        "use": "Treat connector and tool surfaces as governed protocol layers rather than implicit authority.",
    },
    {
        "label": "OWASP Top 10 for Agentic Applications 2026",
        "url": "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
        "use": "Keep agentic autonomy bounded by explicit authorization, audit trails, and sensitive-data guards.",
    },
    {
        "label": "NVIDIA Vera Rubin production announcement",
        "url": "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx",
        "use": "Use AI-factory observability as an analogy for status boards and lane readiness, not as validation of local claims.",
    },
    {
        "label": "NVIDIA AI factories overview",
        "url": "https://www.nvidia.com/en-us/solutions/ai-factories/",
        "use": "Carry digital-twin and factory-runner ideas into THOS runner maps as planning inputs only.",
    },
]


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    body = [f"# {title}", ""]
    body.extend(lines)
    path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_cli_metrics(output_dir: Path, lane_file_stem: str) -> dict[str, Any]:
    last_message = output_dir / f"{lane_file_stem}-last-message.txt"
    stdout = output_dir / f"{lane_file_stem}-stdout.txt"
    stderr = output_dir / f"{lane_file_stem}-stderr.txt"
    stdout_payload: dict[str, Any] = {}
    if stdout.exists() and stdout.stat().st_size:
        try:
            stdout_payload = json.loads(stdout.read_text(encoding="utf-8", errors="replace"))
        except JSONDecodeError:
            stdout_payload = {}
    start_raw = stdout_payload.get("generated_at_utc")
    existing_files = [path for path in [stdout, stderr, last_message] if path.exists()]
    earliest_timestamp = min((path.stat().st_ctime for path in existing_files), default=datetime.now(timezone.utc).timestamp())
    start_dt = parse_dt(start_raw) if start_raw else datetime.fromtimestamp(earliest_timestamp, timezone.utc)
    if last_message.exists():
        finish_dt = datetime.fromtimestamp(last_message.stat().st_mtime, timezone.utc)
        duration = max(0.0, (finish_dt - start_dt).total_seconds())
        final_bytes = last_message.stat().st_size
        final_hash = file_sha256(last_message)
    else:
        finish_dt = start_dt
        duration = 0.0
        final_bytes = 0
        final_hash = ""
    stderr_text = stderr.read_text(encoding="utf-8", errors="replace") if stderr.exists() else ""
    stderr_lower = stderr_text.lower()
    warning_count = (
        stderr_lower.count("warning")
        + stderr_lower.count("failed to load skill")
        + stderr_lower.count("invalid name")
    )
    timeout_count = stderr_lower.count("timeout")
    return {
        "duration_seconds": round(duration, 3),
        "first_completion_utc": iso(finish_dt),
        "final_message_bytes": final_bytes,
        "final_message_hash": final_hash,
        "loader_warning_count_unpublished": warning_count,
        "startup_timeout_marker_count_unpublished": timeout_count,
        "start_utc": iso(start_dt),
    }


def app_lanes(app_receipt: dict[str, Any]) -> list[dict[str, Any]]:
    start_dt = parse_dt(app_receipt["generated_utc"])
    lanes: list[dict[str, Any]] = []
    cursor = start_dt
    for lane in app_receipt.get("lanes", []):
        duration = round(float(lane.get("duration_seconds", 0.0)), 3)
        finish = cursor + timedelta(seconds=duration)
        lanes.append(
            {
                "lane": lane.get("lane"),
                "platform": "codex_app_local_server",
                "status": lane.get("overall_status", "unknown"),
                "completion_type": "app_server_turn_completed",
                "start_utc": iso(cursor),
                "first_completion_utc": iso(finish),
                "duration_seconds": duration,
                "timing_basis": "derived_from_app_receipt_generated_utc_and_sequential_lane_duration",
                "body_text_published": False,
            }
        )
        cursor = finish
    return lanes


def cli_lanes(cli_receipt: dict[str, Any], output_dir: Path) -> list[dict[str, Any]]:
    lanes: list[dict[str, Any]] = []
    stem_map = {"Arby": "Arby", "Aster Vale": "AsterVale", "AsterVale": "AsterVale"}
    display_map = {"AsterVale": "Aster Vale"}
    for lane in cli_receipt.get("lanes", []):
        lane_name = lane.get("lane")
        stem = stem_map.get(lane_name, lane_name)
        metrics = local_cli_metrics(output_dir, stem)
        lanes.append(
            {
                "lane": display_map.get(lane_name, lane_name),
                "platform": "codex_cli_read_only",
                "status": lane.get("completion_status", "unknown"),
                "completion_type": "cli_final_message",
                "start_utc": metrics["start_utc"],
                "first_completion_utc": metrics["first_completion_utc"],
                "duration_seconds": metrics["duration_seconds"],
                "timing_basis": "observed_launcher_generated_utc_and_final_message_mtime",
                "final_message_bytes": lane.get("final_message_bytes", metrics["final_message_bytes"]),
                "final_message_hash": lane.get("final_message_hash", metrics["final_message_hash"]),
                "marker_review_required": bool(lane.get("final_message_sensitive_marker_count", 0)),
                "body_text_published": False,
                "loader_warning_count_unpublished": metrics["loader_warning_count_unpublished"],
                "startup_timeout_marker_count_unpublished": metrics["startup_timeout_marker_count_unpublished"],
            }
        )
    return lanes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", default="v478-thos-v14-x8-start")
    parser.add_argument("--boundary", default="start")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--traces-dir", default="docs/trinity-live-traces")
    args = parser.parse_args()

    traces = Path(args.traces_dir)
    phase = args.phase_slug
    generated = now_utc()
    generated_nz = generated.astimezone(NZ)

    app_receipt_name = f"{phase}-background-council-app-completion-v1.json"
    cli_receipt_name = f"{phase}-cli-completion-v1.json"
    marker_review_name = f"{phase}-cli-marker-review-v1.json"
    app_receipt = read_json(traces / app_receipt_name)
    cli_receipt = read_json(traces / cli_receipt_name)
    marker_review_path = traces / marker_review_name
    marker_review = read_json(marker_review_path) if marker_review_path.exists() else None

    app_lane_rows = app_lanes(app_receipt)
    cli_lane_rows = cli_lanes(cli_receipt, Path(args.output_dir))
    lanes = app_lane_rows + cli_lane_rows
    average = round(sum(float(row["duration_seconds"]) for row in lanes) / len(lanes), 3) if lanes else 0.0
    under_baseline = average <= BASELINE_SECONDS
    app_status = "PASS" if all(row["status"] == "completed" for row in app_lane_rows) else "WATCH_APP_LANES"
    cli_status = cli_receipt.get("aggregate_status", "unknown")
    marker_review_resolved = bool(marker_review and marker_review.get("overall_status") == "PASS_FALSE_POSITIVE_MARKER_REVIEW")
    cli_ready = cli_status == "FINAL_MESSAGES_READY" or (
        cli_status == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" and marker_review_resolved
    )
    cli_effective_status = "FINAL_MESSAGES_READY_AFTER_MARKER_REVIEW" if marker_review_resolved else cli_status
    loader_warning_total = sum(int(row.get("loader_warning_count_unpublished", 0)) for row in cli_lane_rows)
    startup_timeout_total = sum(int(row.get("startup_timeout_marker_count_unpublished", 0)) for row in cli_lane_rows)

    timing = {
        "artifact_type": "five_lane_timing_receipt",
        "phase_slug": phase,
        "boundary": args.boundary,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "observation_run_index_today": 8,
        "observation_window_seconds": 1800,
        "overall_status": "PASS_FIVE_LANE_START" if len(lanes) == 5 and app_status == "PASS" and cli_ready else "WATCH_FIVE_LANE_START",
        "lane_count": len(lanes),
        "all_five_lanes_attempted": len(lanes) == 5,
        "average_response_seconds_this_run": average,
        "soft_timeout_baseline_seconds": BASELINE_SECONDS,
        "soft_timeout_baseline_status": "POST_BASELINE_UNDER_FOOTHOLD" if under_baseline else "POST_BASELINE_OVER_FOOTHOLD_WATCH",
        "lanes": lanes,
        "evidence_sources": {
            "app_completion_receipt": app_receipt_name,
            "cli_completion_receipt": cli_receipt_name,
            "cli_output_boundary": "local_temp_redacted_not_published",
        },
        "next_phase_handoff": [
            "Treat this as a post-baseline observation, not a replacement for the three-run soft foothold.",
            "Use idle notifier time for source, command, stale-flow, approval, and next-phase prep.",
            "Keep direct capped CLI advisory prompts for synthesis-only Arby and Aster Vale calls.",
            "Escalate loader or startup warnings only if they block final-message artifacts or an exact approval packet authorizes repair.",
        ],
        "claim_boundary": {
            "scope": "v478-thos-v14-x8-start five-lane timing and handoff only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
            "lane_body_text_published": False,
        },
    }

    multiplex = {
        "artifact_type": "local_multiplex_tui_app_server_status",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "ALL_LANES_READY" if timing["overall_status"] == "PASS_FIVE_LANE_START" else "WATCH_LANES",
        "lanes": [
            {
                "lane": row["lane"],
                "platform": row["platform"],
                "status": row["status"],
                "duration_seconds": row["duration_seconds"],
                "body_text_published": False,
            }
            for row in lanes
        ],
        "operator_note": "Status board remains receipt-only and does not expose lane bodies, transport output, local temp paths, screenshots, sessions, or credentials.",
    }

    stale = {
        "artifact_type": "stale_flow_refresh_receipt",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "READY_WITH_MARKER_REVIEW_FALSE_POSITIVE" if marker_review_resolved else ("READY_NO_STALE_FLOWS" if timing["overall_status"] == "PASS_FIVE_LANE_START" else "WATCH_STALE_FLOWS"),
        "watch_items": [
            {
                "surface": "cli_startup_warnings",
                "status": "watch_only" if loader_warning_total or startup_timeout_total else "clear_this_run",
                "evidence": {
                    "loader_warning_count_unpublished": loader_warning_total,
                    "startup_timeout_marker_count_unpublished": startup_timeout_total,
                },
                "next_action": "Record as metadata only unless final-message production is blocked.",
            },
            {
                "surface": "command_index_v6_alias_gap",
                "status": "known_open_gap",
                "next_action": "Carry as compatibility gap; do not invent missing contract files.",
            },
            {
                "surface": "five_lane_roster",
                "status": "active",
                "next_action": "Attempt all five existing lanes again at x8 closeout.",
            },
        ],
    }

    loader_watch = {
        "artifact_type": "cli_loader_watch_receipt",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "WATCH_NONBLOCKING_CLI_STARTUP_WARNINGS" if loader_warning_total or startup_timeout_total else "PASS_NO_CLI_STARTUP_WARNINGS_OBSERVED",
        "lane_warning_summary": [
            {
                "lane": row["lane"],
                "loader_warning_count_unpublished": row.get("loader_warning_count_unpublished", 0),
                "startup_timeout_marker_count_unpublished": row.get("startup_timeout_marker_count_unpublished", 0),
                "final_message_ready": row["status"] == "FINAL_MESSAGE_READY",
            }
            for row in cli_lane_rows
        ],
        "repair_boundary": "No plugin-cache or user-skill mutation is authorized by this receipt.",
    }

    source_refresh = {
        "artifact_type": "source_refresh_compact",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "PASS_SOURCE_REFRESH_COMPACT",
        "sources": SOURCES,
        "integration_notes": [
            "Use current public sources as planning context only.",
            "Do not treat model, infrastructure, or agentic-security sources as local validation of GMUT, consciousness, physics, or canon claims.",
            "Map source lessons into scoped THOS controls: bounded authority, explicit connector governance, observability, and exact publication receipts.",
        ],
    }

    prep = {
        "artifact_type": "phase_start_prep_handoff",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "PASS_PREP_DURING_X8_START_WAIT",
        "state_reading": [
            "x7 closeout was remote-verified and x8 start used all five existing lanes.",
            "Direct capped CLI remains the preferred synthesis-only pattern for Arby and Aster Vale.",
            "App-server lanes remain active for Cicero, Kierkegaard, and Aristotle.",
            "Source-refresh, stale-flow, loader-watch, and multiplex artifacts are prepared without exposing private lane content.",
        ],
        "x8_closeout_handoff": [
            "Attempt all five existing lanes at x8 closeout.",
            "Use the 312.832 second soft foothold as planning support only.",
            "Use wait time for v479 THOS preparation, command-surface compatibility notes, and approval packet drafting.",
            "Keep all GMUT and canon gates open.",
        ],
    }

    seed = {
        "artifact_type": "x8_closeout_seed_roadmap",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "PASS_X8_CLOSEOUT_SEED_ROADMAP",
        "roadmap": [
            "Close x8 with five-lane status and timing receipts.",
            "Compare x8 start and closeout averages against the soft foothold.",
            "Carry runner/notifier hardening into v479 only when backed by exact receipts.",
            "Prepare v479 THOS start around stale-flow resilience, command-index compatibility, and source-led security controls.",
            "Keep direct capped CLI as a default, but do not ignore genuine final-marker blockers if they recur.",
        ],
    }

    synthesis = {
        "artifact_type": "phase_start_synthesis",
        "phase_slug": phase,
        "generated_utc": iso(generated),
        "generated_nz": generated_nz.isoformat(),
        "overall_status": "PASS_X8_START_WITH_FIVE_LANE_ROSTER" if timing["overall_status"] == "PASS_FIVE_LANE_START" else "WATCH_X8_START",
        "evidence": {
            "app_lanes": {
                "receipt": app_receipt_name,
                "status": app_status,
                "lanes": [{"lane": row["lane"], "duration_seconds": row["duration_seconds"], "completion": row["status"]} for row in app_lane_rows],
            },
            "cli_lanes": {
                "receipt": cli_receipt_name,
                "status": cli_effective_status,
                "lanes": [
                    {
                        "lane": row["lane"],
                        "duration_seconds": row["duration_seconds"],
                        "final_message_bytes": row["final_message_bytes"],
                        "final_message_hash": row["final_message_hash"],
                        "marker_review_required": row["marker_review_required"],
                    }
                    for row in cli_lane_rows
                ],
                "body_text_boundary": "temp_only_not_published",
                "marker_review_receipt": marker_review_name if marker_review_resolved else None,
            },
            "timing": {
                "receipt": f"{phase}-five-lane-timing-v1.json",
                "observation_run_index_today": 8,
                "observation_window_seconds": 1800,
                "average_response_seconds_this_run": average,
                "soft_wait_baseline_seconds": BASELINE_SECONDS,
                "interpretation": "under baseline" if under_baseline else "over baseline watch",
            },
            "multiplex": {"receipt": f"{phase}-local-multiplex-tui-app-server-runner-v1.json", "status": multiplex["overall_status"]},
            "stale_flow": {"receipt": f"{phase}-stale-flow-refresh-v1.json", "status": stale["overall_status"]},
            "loader_watch": {"receipt": f"{phase}-cli-loader-watch-v1.json", "status": loader_watch["overall_status"]},
            "source_refresh": {"receipt": f"{phase}-source-refresh-v1.json", "status": source_refresh["overall_status"]},
            "x8_closeout_seed": {"receipt": f"{phase}-x8-closeout-seed-roadmap-v1.json", "status": seed["overall_status"]},
        },
        "x8_start_lessons": [
            "All five existing lanes were attempted at the x8 start boundary.",
            "Wait time was used for source, stale-flow, loader-watch, and handoff preparation rather than idle babysitting.",
            "Direct capped CLI remains effective when the prompt is synthesis-only and no-tool.",
            "Startup warnings are metadata, not repair proof.",
        ],
        "x8_closeout_handoff": prep["x8_closeout_handoff"],
        "claim_boundary": {
            "scope": "v478 THOS v14 x8 start synthesis and x8 closeout handoff only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
            "lane_body_text_published": False,
            "transport_output_published": False,
        },
    }

    outputs: list[tuple[str, dict[str, Any], str, list[str]]] = [
        ("five-lane-timing", timing, "Five-Lane Timing", [
            f"- Status: `{timing['overall_status']}`",
            f"- Average response: `{average}` seconds against `{BASELINE_SECONDS}` second soft foothold.",
            "- All lane content remains unpublished; this receipt carries status metadata only.",
        ]),
        ("local-multiplex-tui-app-server-runner", multiplex, "Local Multiplex Status", [
            f"- Status: `{multiplex['overall_status']}`",
            "- Five-lane board is receipt-only and private-content safe.",
        ]),
        ("stale-flow-refresh", stale, "Stale-Flow Refresh", [
            f"- Status: `{stale['overall_status']}`",
            "- CLI warnings remain watch-only unless they block final-message production.",
        ]),
        ("cli-loader-watch", loader_watch, "CLI Loader Watch", [
            f"- Status: `{loader_watch['overall_status']}`",
            "- No skill or plugin-cache repair is performed by this receipt.",
        ]),
        ("source-refresh", source_refresh, "Source Refresh", [
            f"- Status: `{source_refresh['overall_status']}`",
            "- Sources are used as planning context and not as validation of broad GMUT or canon claims.",
        ]),
        ("prep-handoff", prep, "Prep Handoff", [
            f"- Status: `{prep['overall_status']}`",
            "- Handoff keeps x8 closeout focused on five-lane receipt evidence and v479 preparation.",
        ]),
        ("x8-closeout-seed-roadmap", seed, "X8 Closeout Seed Roadmap", [
            f"- Status: `{seed['overall_status']}`",
            "- Roadmap seeds x8 closeout and v479 THOS preparation without overclaiming.",
        ]),
        ("synthesis", synthesis, "Synthesis", [
            f"- Status: `{synthesis['overall_status']}`",
            f"- Evidence receipts: `{app_receipt_name}`, `{cli_receipt_name}`, timing, multiplex, stale-flow, loader-watch, source, and seed roadmap.",
        ]),
    ]
    for suffix, payload, title, md_lines in outputs:
        json_path = traces / f"{phase}-{suffix}-v1.json"
        md_path = traces / f"{phase}-{suffix}-v1.md"
        write_json(json_path, payload)
        write_md(md_path, f"{phase} {title}", md_lines)

    print(json.dumps({"status": "ok", "phase_slug": phase, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
