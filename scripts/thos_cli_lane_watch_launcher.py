#!/usr/bin/env python3
"""Launch the CLI lane completion notifier without shell quoting hazards."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTIFIER = REPO_ROOT / "scripts" / "thos_cli_lane_completion_notifier.py"
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(NOTIFIER),
        "--output-dir",
        str(Path(args.output_dir)),
        "--phase-slug",
        args.phase_slug,
        "--poll-seconds",
        str(args.poll_seconds),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--receipt-json",
        str(Path(args.receipt_json)),
        "--receipt-md",
        str(Path(args.receipt_md)),
    ]
    for lane in args.lane:
        command.extend(["--lane", lane])
    if args.once:
        command.append("--once")
    return command


def redacted_command(command: list[str]) -> list[str]:
    redacted: list[str] = []
    for item in command:
        if ":" in item or "\\" in item or "/" in item:
            redacted.append("<path_redacted>")
        else:
            redacted.append(item)
    return redacted


def file_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    stdout_path = Path(args.watch_stdout)
    stderr_path = Path(args.watch_stderr)
    receipt_json = Path(args.receipt_json)
    receipt_md = Path(args.receipt_md)
    command = build_command(args)
    return {
        "command_preview": redacted_command(command) if args.redact else command,
        "ephemeral_flag_used": False,
        "generated_at_utc": utc_now(),
        "launcher_status": "PASS_SHAPE_ONLY" if NOTIFIER.exists() else "FAIL_BLOCKER",
        "lanes": args.lane,
        "mutation_performed": False,
        "notifier_exists": NOTIFIER.exists(),
        "phase_slug": args.phase_slug,
        "poll_seconds": args.poll_seconds,
        "receipt_json": "<path_redacted>" if args.redact else str(receipt_json),
        "receipt_md": "<path_redacted>" if args.redact else str(receipt_md),
        "shell_invoked": False,
        "stderr_file": "<path_redacted>" if args.redact else str(stderr_path),
        "stdout_file": "<path_redacted>" if args.redact else str(stdout_path),
        "timeout_seconds": args.timeout_seconds,
    }


def execute(args: argparse.Namespace, plan: dict[str, Any]) -> dict[str, Any]:
    if plan["launcher_status"] != "PASS_SHAPE_ONLY":
        plan["execution_status"] = "FAIL_BLOCKER"
        return plan
    stdout_path = Path(args.watch_stdout)
    stderr_path = Path(args.watch_stderr)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_command(args)
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(
            command,
            cwd=REPO_ROOT,
            stdout=stdout,
            stderr=stderr,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    plan["execution_status"] = "PASS_SHAPE_ONLY"
    plan["pid"] = process.pid
    plan["started_background_watcher"] = True
    if args.wait_seconds > 0:
        deadline = time.monotonic() + args.wait_seconds
        while time.monotonic() < deadline and process.poll() is None:
            time.sleep(0.25)
        plan["completed_within_wait"] = process.poll() is not None
        plan["returncode"] = process.poll()
        plan["stdout_bytes"] = file_size(stdout_path)
        plan["stderr_bytes"] = file_size(stderr_path)
    return plan


def default_receipt_json(phase_slug: str) -> str:
    return str(ARTIFACT_ROOT / f"{phase_slug}-cli-lane-completion-notice-v1.json")


def default_receipt_md(phase_slug: str) -> str:
    return str(ARTIFACT_ROOT / f"{phase_slug}-cli-lane-completion-notice-v1.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the CLI notifier with shell-safe lane arguments.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lane", action="append", required=True)
    parser.add_argument("--poll-seconds", type=float, default=60.0)
    parser.add_argument("--timeout-seconds", type=float, default=72000.0)
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    parser.add_argument("--watch-stdout")
    parser.add_argument("--watch-stderr")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--wait-seconds", type=float, default=0.0)
    parser.add_argument("--redact", action="store_true")
    args = parser.parse_args()

    args.receipt_json = args.receipt_json or default_receipt_json(args.phase_slug)
    args.receipt_md = args.receipt_md or default_receipt_md(args.phase_slug)
    args.watch_stdout = args.watch_stdout or str(Path(args.output_dir) / "watcher-stdout.txt")
    args.watch_stderr = args.watch_stderr or str(Path(args.output_dir) / "watcher-stderr.txt")

    plan = build_plan(args)
    if args.execute:
        plan = execute(args, plan)
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0 if plan.get("launcher_status") == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
