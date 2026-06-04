#!/usr/bin/env python3
"""Render a compact local multiplex status board for app and CLI sibling lanes."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {"available": False, "file": name}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False, "file": name}


def app_rows(phase_slug: str) -> list[dict[str, Any]]:
    payload = read_json(f"{phase_slug}-council-app-lane-completion-notifier-notify-v1.json")
    if not payload.get("lanes"):
        payload = read_json(f"{phase_slug}-background-council-app-completion-v1.json")
    rows = []
    for lane in payload.get("lanes", []):
        rows.append(
            {
                "platform": "app",
                "lane": lane.get("lane"),
                "status": lane.get("overall_status"),
                "completion": lane.get("turn_completion", {}).get("status", "not_waited"),
                "duration_seconds": lane.get("duration_seconds"),
            }
        )
    return rows


def cli_rows(phase_slug: str) -> list[dict[str, Any]]:
    names = [f"{phase_slug}-cli-lane-completion-poll-v1.json"] + [
        f"{phase_slug}-cli-lane-completion-poll-retry-{idx}-v1.json" for idx in range(2, 6)
    ]
    names.append(f"{phase_slug}-cli-completion-v1.json")
    names.append(f"{phase_slug}-background-cli-completion-v1.json")
    latest = None
    for name in names:
        payload = read_json(name)
        if payload.get("aggregate_status"):
            latest = payload
    if not latest:
        return []
    rows = []
    for lane in latest.get("lanes", []):
        rows.append(
            {
                "platform": "cli",
                "lane": lane.get("lane"),
                "status": latest.get("aggregate_status"),
                "completion": lane.get("completion_status"),
                "final_message_bytes": lane.get("final_message_bytes"),
            }
        )
    return rows


def build_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    rows = app_rows(args.phase_slug) + cli_rows(args.phase_slug)
    app_ready = all(row.get("completion") == "completed" for row in rows if row.get("platform") == "app")
    cli_ready = all(row.get("completion") == "FINAL_MESSAGE_READY" for row in rows if row.get("platform") == "cli")
    cli_present = any(row.get("platform") == "cli" for row in rows)
    if app_ready and cli_ready and cli_present:
        status = "ALL_LANES_READY"
    elif app_ready:
        status = "APP_READY_CLI_OPEN"
    else:
        status = "OPEN_GAP_MULTIPLEX"
    return {
        "artifact_type": "local_multiplex_tui_app_server_runner",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": status,
        "row_count": len(rows),
        "rows": rows,
        "policy": {
            "status_only_publication": True,
            "does_not_start_new_threads": True,
            "does_not_mutate_live_skills": True,
        },
        "claim_boundary": {
            "scope": "local multiplex status board only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def render_console(payload: dict[str, Any]) -> str:
    lines = [
        f"THOS Multiplex Board :: {payload['phase_slug']}",
        f"Status: {payload['overall_status']}  Generated NZ: {payload['generated_nz']}",
        "-" * 78,
        f"{'platform':<10} {'lane':<18} {'status':<34} completion",
        "-" * 78,
    ]
    for row in payload["rows"]:
        lines.append(
            f"{str(row.get('platform')):<10} {str(row.get('lane')):<18} "
            f"{str(row.get('status')):<34} {row.get('completion')}"
        )
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Local Multiplex TUI App Server Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- row_count: `{payload['row_count']}`",
        "- policy: status-only publication; no new threads; no live skill mutation.",
        "- claim boundary: local multiplex status only; all GMUT gates remain open.",
        "",
        "## Lanes",
    ]
    for row in payload["rows"]:
        lines.append(f"- {row.get('platform')} {row.get('lane')}: `{row.get('status')}`, completion `{row.get('completion')}`.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--watch-seconds", type=float, default=0)
    parser.add_argument("--poll-seconds", type=float, default=10)
    parser.add_argument("--receipt-prefix")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.receipt_prefix = args.receipt_prefix or f"{args.phase_slug}-local-multiplex-tui-app-server-runner"
    deadline = time.monotonic() + args.watch_seconds
    payload = build_snapshot(args)
    while args.watch_seconds > 0 and time.monotonic() < deadline:
        payload = build_snapshot(args)
        print(render_console(payload), flush=True)
        if payload["overall_status"] == "ALL_LANES_READY":
            break
        time.sleep(args.poll_seconds)
    write_json(TRACE_DIR / f"{args.receipt_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.receipt_prefix}-v1.md", payload)
    print(render_console(payload))
    return 0 if payload["overall_status"] in {"ALL_LANES_READY", "APP_READY_CLI_OPEN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
