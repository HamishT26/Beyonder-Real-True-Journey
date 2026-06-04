#!/usr/bin/env python3
"""Build the v478 THOS v14 x4 closeout timing and handoff receipt."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
REMOTE_REF = "origin/codex/GHC-Family/beyonder-shared-omega-line"


def parse_utc(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC)


def iso(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(dt.UTC).replace(microsecond=0).isoformat()


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False, "path_redacted": path.name}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False, "path_redacted": path.name}


def file_mtime_utc(path: Path) -> dt.datetime | None:
    if not path.exists():
        return None
    return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.UTC)


def parse_start_args(values: list[str]) -> dict[str, dt.datetime]:
    starts: dict[str, dt.datetime] = {}
    for value in values:
        if "=" not in value:
            continue
        lane, stamp = value.split("=", 1)
        parsed = parse_utc(stamp.strip())
        if parsed:
            starts[lane.strip()] = parsed
    return starts


def app_lane_rows(app_payload: dict[str, Any]) -> list[dict[str, Any]]:
    start = parse_utc(app_payload.get("generated_utc"))
    cursor = start
    rows: list[dict[str, Any]] = []
    for lane in app_payload.get("lanes", []):
        if not isinstance(lane, dict):
            continue
        duration = lane.get("duration_seconds")
        duration_float = float(duration) if isinstance(duration, (int, float)) else None
        completion = cursor + dt.timedelta(seconds=duration_float) if cursor and duration_float is not None else None
        rows.append(
            {
                "lane": lane.get("lane"),
                "platform": "codex_app_local_server",
                "status": lane.get("overall_status"),
                "completion_type": "app_server_turn_completed" if lane.get("overall_status") == "completed" else "app_server_open_gap",
                "start_utc": iso(cursor),
                "first_completion_utc": iso(completion),
                "duration_seconds": round(duration_float, 3) if duration_float is not None else None,
                "timing_basis": "derived_from_app_receipt_generated_utc_and_sequential_lane_duration",
                "raw_output_published": False,
            }
        )
        cursor = completion or cursor
    return rows


def cli_lane_rows(cli_payload: dict[str, Any], output_dir: Path, starts: dict[str, dt.datetime]) -> list[dict[str, Any]]:
    watcher_start = parse_utc(cli_payload.get("started_at_utc"))
    rows: list[dict[str, Any]] = []
    for lane in cli_payload.get("lanes", []):
        if not isinstance(lane, dict):
            continue
        lane_name = str(lane.get("lane"))
        start = starts.get(lane_name) or watcher_start
        completion = file_mtime_utc(output_dir / f"{lane_name}-last-message.txt") or parse_utc(cli_payload.get("generated_at_utc"))
        duration = (completion - start).total_seconds() if start and completion else None
        rows.append(
            {
                "lane": lane_name,
                "platform": "codex_cli_read_only",
                "status": lane.get("completion_status"),
                "completion_type": "cli_final_message" if lane.get("completion_status") == "FINAL_MESSAGE_READY" else "cli_open_gap",
                "start_utc": iso(start),
                "first_completion_utc": iso(completion),
                "duration_seconds": round(duration, 3) if duration is not None else None,
                "timing_basis": "observed_process_start_arg_and_final_message_mtime" if lane_name in starts else "watcher_start_and_final_message_mtime",
                "final_message_bytes": lane.get("final_message_bytes"),
                "final_message_hash": lane.get("final_message_hash"),
                "marker_review_required": int(lane.get("final_message_sensitive_marker_count") or 0) > 0,
                "raw_output_published": False,
            }
        )
    return rows


def average_duration(rows: list[dict[str, Any]]) -> float | None:
    durations = [float(row["duration_seconds"]) for row in rows if isinstance(row.get("duration_seconds"), (int, float))]
    if not durations:
        return None
    return round(sum(durations) / len(durations), 3)


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    app_payload = read_json(TRACE_DIR / f"{args.app_prefix}-v1.json")
    cli_payload = read_json(TRACE_DIR / f"{args.cli_prefix}-v1.json")
    lane_rows = app_lane_rows(app_payload) + cli_lane_rows(cli_payload, Path(args.cli_output_dir), parse_start_args(args.cli_start))
    all_attempted = {row.get("lane") for row in lane_rows} >= {"Cicero", "Kierkegaard", "Aristotle", "Arby", "Aster Vale"}
    app_ready = all(row.get("status") == "completed" for row in lane_rows if row.get("platform") == "codex_app_local_server")
    cli_ready = all(row.get("status") == "FINAL_MESSAGE_READY" for row in lane_rows if row.get("platform") == "codex_cli_read_only")
    avg = average_duration(lane_rows)
    payload: dict[str, Any] = {
        "artifact_type": "five_lane_closeout_timing_receipt",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "observation_run_index_today": args.observation_run_index,
        "observation_window_seconds": args.observation_window_seconds,
        "overall_status": "PASS_FIVE_LANE_CLOSEOUT" if all_attempted and app_ready and cli_ready else "OPEN_GAP_FIVE_LANE_CLOSEOUT",
        "lane_count": len(lane_rows),
        "all_five_lanes_attempted": all_attempted,
        "average_response_seconds_this_run": avg,
        "soft_timeout_baseline_status": "ONE_OF_THREE_OBSERVATIONS_RECORDED" if args.observation_run_index < 3 else "READY_TO_COMPUTE_THREE_RUN_AVERAGE",
        "lanes": lane_rows,
        "evidence_sources": {
            "app_completion_receipt": f"{args.app_prefix}-v1.json",
            "cli_completion_receipt": f"{args.cli_prefix}-v1.json",
            "cli_output_boundary": "local_temp_redacted_not_published",
        },
        "next_phase_handoff": [
            "Treat this as observation run 1 of 3 for the five-sibling timing baseline.",
            "Repeat the same timing ledger for the next two five-sibling runs before deriving the soft future timeout average.",
            "Keep the every-second-session five-lane rule active at both start and closeout boundaries.",
            "Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.",
        ],
        "claim_boundary": {
            "scope": "v478 THOS v14 x4 closeout timing and handoff only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
            "raw_lane_text_published": False,
        },
    }
    write_json(TRACE_DIR / f"{args.receipt_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.receipt_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Five-Lane Closeout Timing",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- observation_run_index_today: `{payload['observation_run_index_today']}`",
        f"- observation_window_seconds: `{payload['observation_window_seconds']}`",
        f"- average_response_seconds_this_run: `{payload['average_response_seconds_this_run']}`",
        f"- soft_timeout_baseline_status: `{payload['soft_timeout_baseline_status']}`",
        "- publication boundary: raw lane text, local temp paths, transport output, sessions, screenshots, and credentials are not published.",
        "- claim boundary: closeout timing only; all GMUT gates remain open.",
        "",
        "## Lane Timing",
    ]
    for row in payload["lanes"]:
        lines.append(
            f"- {row['lane']} / {row['platform']}: `{row['status']}`, start `{row['start_utc']}`, "
            f"completion `{row['first_completion_utc']}`, duration `{row['duration_seconds']}`, basis `{row['timing_basis']}`."
        )
    lines.extend(["", "## Handoff", *[f"- {item}" for item in payload["next_phase_handoff"]]])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", default="v478-thos-v14-x4-closeout")
    parser.add_argument("--app-prefix", default="v478-thos-v14-x4-closeout-background-council-app-completion")
    parser.add_argument("--cli-prefix", default="v478-thos-v14-x4-closeout-cli-completion")
    parser.add_argument("--receipt-prefix", default="v478-thos-v14-x4-closeout-five-lane-timing")
    parser.add_argument("--cli-output-dir", required=True)
    parser.add_argument("--cli-start", action="append", default=[])
    parser.add_argument("--observation-run-index", type=int, default=1)
    parser.add_argument("--observation-window-seconds", type=int, default=1800)
    return parser.parse_args()


def main() -> int:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "average": payload["average_response_seconds_this_run"]}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
