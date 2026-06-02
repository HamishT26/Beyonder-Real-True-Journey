#!/usr/bin/env python3
"""Launch v475 THOS no-rush CLI advisory lanes with a receipt watcher."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v6-x1"
NEXT_PHASE = "v475-thos-v6-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
LANE_LAUNCHER = REPO_ROOT / "scripts" / "thos_codex_cli_advisory_launcher.py"
WATCH_LAUNCHER = REPO_ROOT / "scripts" / "thos_cli_lane_watch_launcher.py"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

LANES = [
    {
        "lane": "Arby",
        "worktree": "D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory",
    },
    {
        "lane": "Aster Vale",
        "worktree": "D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def nz_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def run_json(command: list[str]) -> tuple[int, dict[str, Any], str]:
    process = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    try:
        payload = json.loads(process.stdout) if process.stdout.strip() else {}
    except json.JSONDecodeError:
        payload = {"parse_status": "FAIL_BLOCKER", "stdout_prefix": process.stdout[:200]}
    return process.returncode, payload, process.stderr[:400]


def lane_prompt(lane: str, runtime_minutes: int) -> str:
    return (
        f"{PHASE} no-rush THOS advisory for {lane}. "
        "Run non-ephemeral and read-only. Do not write files, commit, push, mutate caches, "
        "or publish lane transport. Take the time needed inside the configured runtime window; "
        "no rushing is required. Focus on lane completion receipts, watcher durability, "
        "metadata-only handoff rows, retry safety, and CLI/App platform reliability. "
        "Return an elaborate final advisory with: 1) runtime assumptions, 2) worktree and "
        "sandbox status, 3) notifier or watcher improvements, 4) likely failure modes, "
        "5) safe next implementation tasks, and 6) claim-boundary reminder that THOS support "
        "does not close GMUT gates. "
        f"Target runtime may be up to {runtime_minutes} minutes or longer if the CLI needs it."
    )


def launch_lane(lane: dict[str, str], output_dir: Path, runtime_minutes: int, execute: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(LANE_LAUNCHER),
        "--lane-name",
        lane["lane"],
        "--worktree",
        lane["worktree"],
        "--prompt",
        lane_prompt(lane["lane"], runtime_minutes),
        "--output-dir",
        str(output_dir),
        "--wait-seconds",
        "0",
        "--redact",
    ]
    if execute:
        command.append("--execute")
    returncode, payload, stderr = run_json(command)
    return {
        "lane": lane["lane"],
        "launcher_returncode": returncode,
        "launcher_stderr_prefix": stderr,
        "launcher_summary": payload,
        "requested_runtime_minutes": runtime_minutes,
        "worktree_label": f"{lane['lane']} configured advisory worktree",
    }


def launch_watcher(output_dir: Path, timeout_seconds: int, poll_seconds: int, execute: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(WATCH_LAUNCHER),
        "--output-dir",
        str(output_dir),
        "--phase-slug",
        PHASE,
        "--lane",
        "Arby",
        "--lane",
        "Aster Vale",
        "--poll-seconds",
        str(poll_seconds),
        "--timeout-seconds",
        str(timeout_seconds),
        "--wait-seconds",
        "2",
        "--redact",
    ]
    if execute:
        command.append("--execute")
    returncode, payload, stderr = run_json(command)
    return {
        "watcher_returncode": returncode,
        "watcher_stderr_prefix": stderr,
        "watcher_summary": payload,
    }


def aggregate_status(lanes: list[dict[str, Any]], watcher: dict[str, Any]) -> str:
    if any(item["launcher_returncode"] != 0 for item in lanes):
        return "OPEN_GAP_LANE_LAUNCH_BLOCKED"
    if watcher["watcher_returncode"] != 0:
        return "OPEN_GAP_WATCHER_LAUNCH_BLOCKED"
    return "PASS_SHAPE_ONLY_ASYNC_WATCHER_RUNNING"


def build_runtime(args: argparse.Namespace) -> list[Path]:
    generated_at_utc = utc_now()
    started_at_nz = nz_now()
    safe_stamp = generated_at_utc.replace(":", "").replace("+", "Z")
    output_dir = Path(os.environ.get("TEMP", ".")) / f"{PHASE}-{safe_stamp}"
    lane_results = [launch_lane(lane, output_dir, args.runtime_minutes, args.execute) for lane in LANES]
    watcher = launch_watcher(output_dir, args.watcher_timeout_seconds, args.poll_seconds, args.execute)
    status = aggregate_status(lane_results, watcher)
    completion_notice_json = ARTIFACT_ROOT / f"{PHASE}-cli-lane-completion-notice-v1.json"
    completion_notice_md = ARTIFACT_ROOT / f"{PHASE}-cli-lane-completion-notice-v1.md"

    runtime = {
        "aggregate_status": status,
        "completion_notice_json": "docs/trinity-live-traces/" + completion_notice_json.name,
        "completion_notice_md": "docs/trinity-live-traces/" + completion_notice_md.name,
        "execution_mode": "live_launch" if args.execute else "plan_only",
        "generated_at_utc": generated_at_utc,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "lanes": lane_results,
        "mutation_boundary": "lane_transport_temp_only_curated_receipts_repo_only",
        "next_expected_phase": NEXT_PHASE,
        "notification_model": "background_receipt_watcher_no_model_wakeup_tool_available",
        "phase_slug": PHASE,
        "raw_output_dir": "<local_temp_redacted>",
        "started_at_nz": started_at_nz,
        "watcher": watcher,
        "watcher_poll_seconds": args.poll_seconds,
        "watcher_timeout_seconds": args.watcher_timeout_seconds,
    }

    run_status = {
        "aggregate_status": status,
        "generated_at_utc": generated_at_utc,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": [
            {
                "message": "Arby and Aster Vale no-rush CLI advisory lanes were launched or planned.",
                "row_id": "cli_lanes",
                "status": "PASS_SHAPE_ONLY" if not status.endswith("BLOCKED") else "OPEN_GAP",
            },
            {
                "message": "The watcher records completion metadata only and leaves lane transport local.",
                "row_id": "completion_watcher",
                "status": "PASS_SHAPE_ONLY" if watcher["watcher_returncode"] == 0 else "OPEN_GAP",
            },
            {
                "message": "No app wakeup tool is exposed, so the durable notification is the curated completion receipt.",
                "row_id": "notification_boundary",
                "status": "OPEN_GAP_EXTERNAL_WAKEUP_NOT_EXPOSED",
            },
            {
                "message": "THOS watcher support does not test or close GMUT gates.",
                "row_id": "claim_boundary",
                "status": "PASS_SHAPE_ONLY",
            },
        ],
        "started_at_nz": started_at_nz,
    }

    written: list[Path] = []
    runtime_json = ARTIFACT_ROOT / f"{PHASE}-no-rush-cli-lane-notifier-refresh-v1.json"
    write_json(runtime_json, runtime)
    written.append(runtime_json)
    runtime_md = ARTIFACT_ROOT / f"{PHASE}-no-rush-cli-lane-notifier-refresh-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: launcher return `{item['launcher_returncode']}`, runtime target `{item['requested_runtime_minutes']}` minutes"
        for item in lane_results
    )
    write_md(
        runtime_md,
        f"""
# v475 THOS v6 x1 No-Rush CLI Lane Notifier Refresh

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at_utc}`

Status: `{status}`

Arby and Aster Vale were given no-rush, non-ephemeral, read-only advisory windows. A background watcher is responsible for writing completion receipts when final messages arrive or when the configured timeout is reached.

{lane_lines}

Watcher poll seconds: `{args.poll_seconds}`
Watcher timeout seconds: `{args.watcher_timeout_seconds}`

Completion receipts expected:

- `docs/trinity-live-traces/{completion_notice_json.name}`
- `docs/trinity-live-traces/{completion_notice_md.name}`

No app wakeup tool is exposed in this session, so the durable notification is the curated receipt pair. Lane transport remains local and unpublished.

All six GMUT gates remain open.
""",
    )
    written.append(runtime_md)

    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v6 x1 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v6 x1 refreshed the no-rush Arby/Aster notifier around the existing receipt watcher. It allows long advisory runtimes without manual pressure and keeps lane transport out of curated publication.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch v475 no-rush CLI lanes and watcher.")
    parser.add_argument("--execute", action="store_true", help="Launch lanes and watcher instead of planning only.")
    parser.add_argument("--runtime-minutes", type=int, default=1200)
    parser.add_argument("--watcher-timeout-seconds", type=int, default=72000)
    parser.add_argument("--poll-seconds", type=int, default=300)
    args = parser.parse_args()
    for path in build_runtime(args):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
