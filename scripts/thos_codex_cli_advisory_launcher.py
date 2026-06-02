#!/usr/bin/env python3
"""Plan or launch non-ephemeral read-only Codex CLI advisory lanes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def resolve_codex_executable() -> Path | None:
    local = Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin" / "codex.exe"
    if local.exists():
        return local
    for candidate in sorted((Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin").glob("*/codex.exe")):
        if candidate.exists():
            return candidate
    return None


def build_plan(worktree: Path, prompt: str, output_dir: Path, lane_name: str) -> dict[str, Any]:
    codex_exe = resolve_codex_executable()
    output_dir.mkdir(parents=True, exist_ok=True)
    last_message = output_dir / f"{lane_name}-last-message.txt"
    stdout = output_dir / f"{lane_name}-stdout.txt"
    stderr = output_dir / f"{lane_name}-stderr.txt"
    command = [
        str(codex_exe) if codex_exe else "<missing-codex-exe>",
        "exec",
        "-s",
        "read-only",
        "-C",
        str(worktree),
        "-o",
        str(last_message),
        prompt,
    ]
    return {
        "command_preview": command,
        "codex_executable_found": codex_exe is not None,
        "ephemeral_flag_used": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "lane_name": lane_name,
        "last_message_file": str(last_message),
        "launcher_status": "PASS_SHAPE_ONLY" if codex_exe and worktree.exists() else "FAIL_BLOCKER",
        "old_invalid_flags_blocked": ["-a"],
        "sandbox": "read-only",
        "stderr_file": str(stderr),
        "stdout_file": str(stdout),
        "worktree_exists": worktree.exists(),
        "worktree_path": str(worktree),
    }


def execute_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if plan["launcher_status"] != "PASS_SHAPE_ONLY":
        plan["execution_status"] = "FAIL_BLOCKER"
        plan["execution_message"] = "launcher plan was not executable"
        return plan
    stdout_path = Path(plan["stdout_file"])
    stderr_path = Path(plan["stderr_file"])
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(
            plan["command_preview"],
            stdout=stdout,
            stderr=stderr,
            cwd=plan["worktree_path"],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    plan["execution_status"] = "PASS_SHAPE_ONLY"
    plan["pid"] = process.pid
    plan["execution_message"] = "started non-ephemeral read-only advisory lane"
    return plan


def redact_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Keep local path details out of curated artifacts while preserving decisions."""
    redacted = dict(plan)
    for key in ["command_preview", "last_message_file", "stderr_file", "stdout_file", "worktree_path"]:
        if key in redacted:
            redacted[key] = "<local_path_redacted>"
    return redacted


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan or launch a Codex CLI advisory lane safely.")
    parser.add_argument("--lane-name", required=True)
    parser.add_argument("--worktree", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output-dir", default=os.path.join(os.environ.get("TEMP", "."), "ghc-v471-advisory"))
    parser.add_argument("--execute", action="store_true", help="Launch the lane; default is dry-run plan only.")
    parser.add_argument("--redact", action="store_true", help="Redact local paths in stdout JSON.")
    args = parser.parse_args()

    plan = build_plan(Path(args.worktree), args.prompt, Path(args.output_dir), args.lane_name)
    if args.execute:
        plan = execute_plan(plan)
    output = redact_plan(plan) if args.redact else plan
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if plan.get("launcher_status") == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
