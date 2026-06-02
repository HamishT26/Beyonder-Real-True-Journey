#!/usr/bin/env python3
"""Launch v474 THOS v5 x2 no-rush CLI lanes with async completion notice."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v5-x2"
SOURCE_PHASE = "v474-thos-v5-x1"
NEXT_PHASE = "v474-thos-v6-x1"
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


def safe_stamp(value: str) -> str:
    return value.replace(":", "").replace("+", "Z")


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
        payload = {
            "parse_status": "FAIL_BLOCKER",
            "stdout_prefix": process.stdout[:200],
        }
    return process.returncode, payload, process.stderr[:400]


def advisory_prompt(lane: str, runtime_hours: float) -> str:
    return (
        f"{PHASE} no-rush THOS async notifier advisory for {lane}. "
        "Run non-ephemeral and read-only. Do not use --ephemeral. Do not write files, "
        "commit, push, mutate caches, delete files, stage raw logs, or expose sensitive material. "
        "Take the time needed; silence is acceptable and should not be treated as failure. "
        f"The watcher window is up to {runtime_hours:g} hours. "
        "Return a final advisory when ready with: 1) sandbox/worktree health, "
        "2) whether the CLI lane could complete without rushing, 3) notifier or receipt "
        "improvements, 4) loader/sandbox blockers if any, 5) marker-review or privacy "
        "risks, 6) retry recommendations, and 7) a claim boundary stating that this is "
        "THOS workflow reliability only and all six GMUT gates remain open."
    )


def launch_lane(lane: dict[str, str], output_dir: Path, runtime_hours: float, execute: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(LANE_LAUNCHER),
        "--lane-name",
        lane["lane"],
        "--worktree",
        lane["worktree"],
        "--prompt",
        advisory_prompt(lane["lane"], runtime_hours),
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
        "non_ephemeral_required": True,
        "read_only_required": True,
        "requested_runtime_hours": runtime_hours,
        "worktree_label": f"{lane['lane']} configured advisory worktree",
    }


def launch_watcher(
    output_dir: Path,
    timeout_seconds: int,
    poll_seconds: int,
    execute: bool,
) -> dict[str, Any]:
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
        "--receipt-json",
        str(ARTIFACT_ROOT / f"{PHASE}-cli-lane-completion-notice-v1.json"),
        "--receipt-md",
        str(ARTIFACT_ROOT / f"{PHASE}-cli-lane-completion-notice-v1.md"),
        "--wait-seconds",
        "1",
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
    if any(lane["launcher_returncode"] != 0 for lane in lanes):
        return "OPEN_GAP_LANE_LAUNCH_BLOCKED"
    if watcher["watcher_returncode"] != 0:
        return "OPEN_GAP_WATCHER_LAUNCH_BLOCKED"
    return "PASS_SHAPE_ONLY_ASYNC_RUNNING"


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def build_artifacts(args: argparse.Namespace) -> list[Path]:
    generated_at = utc_now()
    output_dir = Path(os.environ.get("TEMP", ".")) / f"{PHASE}-{safe_stamp(generated_at)}"
    runtime_hours = args.watcher_timeout_seconds / 3600
    lanes = [launch_lane(lane, output_dir, runtime_hours, args.execute) for lane in LANES]
    watcher = launch_watcher(output_dir, args.watcher_timeout_seconds, args.poll_seconds, args.execute)
    status = aggregate_status(lanes, watcher)

    notification_contract = {
        "completion_signal": "watcher writes curated completion notice JSON/MD when final messages arrive or timeout is reached",
        "human_visible_boundary": "receipt files are repo-curated; raw CLI output remains temp-only and unpublished",
        "llm_wakeup_boundary": "local process completion cannot wake Codex by itself unless a separate app/thread wake tool is exposed; this packet creates inspectable receipts for the next active check",
        "poll_seconds": args.poll_seconds,
        "timeout_seconds": args.watcher_timeout_seconds,
    }
    lane_rows = [
        row(
            f"{lane['lane'].lower().replace(' ', '_')}_launch",
            "PASS_SHAPE_ONLY" if lane["launcher_returncode"] == 0 else "OPEN_GAP_LAUNCH",
            f"{lane['lane']} no-rush non-ephemeral read-only advisory launch was requested.",
            {
                "launcher_returncode": lane["launcher_returncode"],
                "pid_recorded": bool(lane.get("launcher_summary", {}).get("pid")),
                "sandbox": lane.get("launcher_summary", {}).get("sandbox"),
                "ephemeral_flag_used": lane.get("launcher_summary", {}).get("ephemeral_flag_used"),
            },
        )
        for lane in lanes
    ]
    rows = [
        *lane_rows,
        row(
            "watcher_launch",
            "PASS_SHAPE_ONLY" if watcher["watcher_returncode"] == 0 else "OPEN_GAP_WATCHER",
            "A background watcher was launched or planned to write completion receipts without constant polling.",
            {
                "started_background_watcher": watcher.get("watcher_summary", {}).get("started_background_watcher"),
                "pid_recorded": bool(watcher.get("watcher_summary", {}).get("pid")),
            },
        ),
        row(
            "notification_contract",
            "PASS_SHAPE_ONLY",
            "Notification is receipt-based and does not publish raw lane text.",
            notification_contract,
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This improves THOS workflow reliability only and does not close or test GMUT gates.",
        ),
    ]

    receipt = {
        "aggregate_status": status,
        "execution_mode": "live_launch" if args.execute else "plan_only",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lanes": lanes,
        "mutation_boundary": "raw_cli_outputs_temp_only_curated_receipts_repo_only",
        "next_expected_phase": NEXT_PHASE,
        "notification_contract": notification_contract,
        "phase_slug": PHASE,
        "raw_output_dir": "<local_temp_redacted>",
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "watcher": watcher,
    }
    run_status = {
        "aggregate_status": status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    receipt_json = ARTIFACT_ROOT / f"{PHASE}-no-rush-async-notifier-v1.json"
    write_json(receipt_json, receipt)
    written.append(receipt_json)
    receipt_md = ARTIFACT_ROOT / f"{PHASE}-no-rush-async-notifier-v1.md"
    lane_lines = "\n".join(
        f"- {lane['lane']}: launcher return `{lane['launcher_returncode']}`, pid recorded `{bool(lane.get('launcher_summary', {}).get('pid'))}`"
        for lane in lanes
    )
    write_md(
        receipt_md,
        f"""
# v474 THOS v5 x2 No-Rush Async Notifier

Generated UTC: `{generated_at}`

Status: `{status}`

This phase starts or plans a no-rush Arby/Aster advisory run and a background completion watcher. The watcher writes a curated completion notice when final messages arrive or when the configured timeout is reached, so the lanes can take the time they need without manual pressure.

{lane_lines}

Watcher poll seconds: `{args.poll_seconds}`

Watcher timeout seconds: `{args.watcher_timeout_seconds}`

Raw lane output remains temp-only. Completion notice files are summary-only and must still respect marker review before any advisory content is promoted.

All six GMUT gates remain open.
""",
    )
    written.append(receipt_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v5 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v5 x2 installs a receipt-based no-rush notification workflow for Arby and Aster Vale. It records launch/watcher metadata only; raw CLI lane output stays temp-only and unpublished.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch v474 v5 x2 no-rush async notifier.")
    parser.add_argument("--execute", action="store_true", help="Launch lanes and watcher instead of planning only.")
    parser.add_argument("--watcher-timeout-seconds", type=int, default=72000)
    parser.add_argument("--poll-seconds", type=int, default=300)
    args = parser.parse_args()
    for path in build_artifacts(args):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
