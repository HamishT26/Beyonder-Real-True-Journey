#!/usr/bin/env python3
"""Launch strict read-only Codex CLI sibling lanes with safe output filenames.

This launcher exists to avoid Windows argument-splitting problems when a lane
display name contains spaces. It writes raw output only to a caller-provided temp
directory and publishes a status-only receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
DEFAULT_LANES = ["Arby", "Aster Vale"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "", text)
    return slug or "lane"


def codex_command_parts() -> list[str]:
    appdata = os.environ.get("APPDATA")
    node = shutil.which("node.exe") or shutil.which("node")
    if appdata and node:
        codex_js = Path(appdata) / "npm" / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
        if codex_js.exists():
            return [node, str(codex_js)]
    return [shutil.which("codex.cmd") or shutil.which("codex.exe") or shutil.which("codex") or "codex"]


def ps_quote(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Strict CLI Lane Launcher",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- execute: `{payload['execute']}`",
        f"- next_manual_status_check_not_before_utc: `{payload['next_manual_status_check_not_before_utc']}`",
        "- raw boundary: temp-only; local paths, prompts, stdout, and stderr are not published.",
        "",
        "## Lanes",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane['launch_status']}`, safe output bridge `{lane['safe_output_bridge']}`, "
            f"process started `{lane['process_started']}`."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_prompt(lane: str, phase_slug: str, minimum_words: int, items_per_category: int) -> str:
    effective_minimum_words = max(minimum_words, 3200)
    return f"""Lane: {lane}
Phase: {phase_slug}

You are the existing {lane} read-only CLI advisory sibling lane. Do not treat this as a new identity, new thread, or new agent. Do not use tools, shell commands, MCP, web search, file reads, file writes, or repository mutation. Produce only your final advisory composition. Do not include local absolute paths, secrets, session streams, screenshots, private dumps, or raw transport details.

Use the current operating contract: watcher-led supervision, no babysitting, timestamped five-minute productive cadence, x1 is for research/reflection/design/preparation, and x2 is for building/running/testing/installing/using the best safe tasks. Keep GMUT, physics, consciousness, and canon gates open.

Hard minimum: write at least {effective_minimum_words} words before you mark the response complete. If your draft is shorter than {effective_minimum_words} words, keep elaborating inside the six required sections before the final status phrase. Do not include credentials. End with the exact status phrase FINAL MESSAGE READY after your final advisory paragraph. Use exactly these headings, each on its own line, and include at least 12 concrete items in each of the first four sections, with at least {items_per_category} numbered items when that target is higher:

COMMAND PROPOSALS (10+)
SYSTEM EXPANSION PROPOSALS (10+)
SKILL OR MICRO-WORKFLOW PROPOSALS (10+)
EUREKA TASKS (10+)
RISKS AND BLOCKERS
X2 BUILD PRIORITIES

Make the response elaborate, concrete, status-safe, and useful for Aletheon to convert into the next x2 build/run/use packet. Prefer operational improvements for watcher/notifier repair, CLI/app multiplex resilience, command-index compatibility, source/security ledgers, skill overlays, stale-flow refresh, and Trinity Mandala continuity.
"""


def wrapper_text(
    codex_parts: list[str],
    repo: Path,
    prompt_path: Path,
    raw_output_path: Path,
    expected_output_path: Path,
    stdout_path: Path,
    stderr_path: Path,
    start_sentinel_path: Path,
    exit_sentinel_path: Path,
) -> str:
    escaped = {
        "repo": str(repo).replace("'", "''"),
        "prompt": str(prompt_path).replace("'", "''"),
        "raw": str(raw_output_path).replace("'", "''"),
        "expected": str(expected_output_path).replace("'", "''"),
        "stdout": str(stdout_path).replace("'", "''"),
        "stderr": str(stderr_path).replace("'", "''"),
        "start": str(start_sentinel_path).replace("'", "''"),
        "exit": str(exit_sentinel_path).replace("'", "''"),
    }
    command_head = " ".join(ps_quote(part) for part in codex_parts)
    return f"""$ErrorActionPreference = 'Stop'
$codexExit = $null
$wrapperErrorClass = ''
try {{
  Set-Content -Path '{escaped['start']}' -Value 'started'
  $promptText = Get-Content -Raw -Path '{escaped['prompt']}'
  $promptText | & {command_head} exec --disable plugins --sandbox read-only -C '{escaped['repo']}' -o '{escaped['raw']}' - 1> '{escaped['stdout']}' 2> '{escaped['stderr']}'
  $codexExit = $LASTEXITCODE
}} catch {{
  $wrapperErrorClass = $_.Exception.GetType().Name
  $codexExit = -999
  try {{
    Set-Content -Path '{escaped['stderr']}' -Value ('wrapper_error_class=' + $wrapperErrorClass)
  }} catch {{}}
}}
for ($i = 0; $i -lt 60; $i++) {{
  if ((Test-Path '{escaped['raw']}') -and ((Get-Item -LiteralPath '{escaped['raw']}').Length -gt 0)) {{
    break
  }}
  Start-Sleep -Seconds 1
}}
$copyStatus = 'not_attempted'
if (Test-Path '{escaped['raw']}') {{
  Copy-Item -LiteralPath '{escaped['raw']}' -Destination '{escaped['expected']}' -Force
  $copyStatus = 'copied'
}}
$rawBytes = 0
if (Test-Path '{escaped['raw']}') {{
  $rawBytes = (Get-Item -LiteralPath '{escaped['raw']}').Length
}}
$expectedBytes = 0
if (Test-Path '{escaped['expected']}') {{
  $expectedBytes = (Get-Item -LiteralPath '{escaped['expected']}').Length
}}
$status = [ordered]@{{
  codex_exit_code = $codexExit
  wrapper_error_class = $wrapperErrorClass
  copy_status = $copyStatus
  raw_exists = (Test-Path '{escaped['raw']}')
  raw_bytes = $rawBytes
  expected_exists = (Test-Path '{escaped['expected']}')
  expected_bytes = $expectedBytes
}}
$status | ConvertTo-Json -Compress | Set-Content -Path '{escaped['exit']}'
"""


def launch_lane(args: argparse.Namespace, lane: str, generated: datetime, codex_parts: list[str]) -> dict[str, Any]:
    output_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.gettempdir()) / args.phase_slug
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = safe_slug(lane)
    prompt_path = output_dir / f"{slug}-strict-prompt.txt"
    raw_output_path = output_dir / f"{slug}-strict-last-message.txt"
    expected_output_path = output_dir / f"{lane}-last-message.txt"
    stdout_path = output_dir / f"{slug}-strict-stdout.txt"
    stderr_path = output_dir / f"{slug}-strict-stderr.txt"
    wrapper_path = output_dir / f"{slug}-strict-wrapper.ps1"
    start_sentinel_path = output_dir / f"{slug}-strict-wrapper-start.txt"
    exit_sentinel_path = output_dir / f"{slug}-strict-wrapper-exit.json"
    launcher_stdout_path = output_dir / f"{slug}-strict-launcher-stdout.txt"
    launcher_stderr_path = output_dir / f"{slug}-strict-launcher-stderr.txt"
    prompt_path.write_text(
        build_prompt(lane, args.phase_slug, args.minimum_words, args.items_per_category),
        encoding="utf-8",
    )
    wrapper_path.write_text(
        wrapper_text(
            codex_parts,
            ROOT,
            prompt_path,
            raw_output_path,
            expected_output_path,
            stdout_path,
            stderr_path,
            start_sentinel_path,
            exit_sentinel_path,
        ),
        encoding="utf-8",
    )
    if not args.execute:
        return {
            "lane": lane,
            "launch_status": "PLANNED_ONLY",
            "process_started": False,
            "safe_output_bridge": True,
            "raw_boundary": "temp_only_not_published",
        }
    creationflags = 0
    for flag_name in ("CREATE_NEW_PROCESS_GROUP", "DETACHED_PROCESS", "CREATE_NO_WINDOW"):
        creationflags |= int(getattr(subprocess, flag_name, 0))
    start_sentinel_path.write_text("started\n", encoding="utf-8")
    command = [
        *codex_parts,
        "exec",
        "--disable",
        "plugins",
        "--sandbox",
        "read-only",
        "-C",
        str(ROOT),
        "-o",
        str(expected_output_path),
        "-",
    ]
    prompt_handle = prompt_path.open("rb")
    stdout_handle = stdout_path.open("wb")
    stderr_handle = stderr_path.open("wb")
    try:
        proc = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=prompt_handle,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=creationflags,
        )
    finally:
        prompt_handle.close()
        stdout_handle.close()
        stderr_handle.close()
    return {
        "lane": lane,
        "launch_status": "PASS_PROCESS_STARTED",
        "process_started": True,
        "process_id_redacted": True,
        "launch_mode": "direct_python_popen",
        "fallback_start_process_used": False,
        "start_sentinel_observed": start_sentinel_path.exists(),
        "safe_output_bridge": True,
        "wrapper_start_sentinel_expected": False,
        "wrapper_exit_sentinel_expected": False,
        "raw_boundary": "temp_only_not_published",
        "codex_command_bridge": "node_codex_js" if len(codex_parts) > 1 else "codex_executable",
        "launched_after_utc": iso(generated),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lane", action="append")
    parser.add_argument("--output-dir")
    parser.add_argument("--minimum-words", type=int, default=2500)
    parser.add_argument("--items-per-category", type=int, default=12)
    parser.add_argument("--next-check-minutes", type=int, default=15)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    generated = utc_now()
    lanes = args.lane or DEFAULT_LANES
    codex_parts = codex_command_parts()
    lane_rows = [launch_lane(args, lane, generated, codex_parts) for lane in lanes]
    all_started = all(row["process_started"] for row in lane_rows) if args.execute else True
    payload: dict[str, Any] = {
        "artifact_type": "strict_cli_lane_launcher",
        "phase_slug": args.phase_slug,
        "generated_utc": iso(generated),
        "overall_status": "PASS_STRICT_CLI_LANES_LAUNCHED" if all_started else "OPEN_GAP_STRICT_CLI_LAUNCH",
        "execute": args.execute,
        "next_manual_status_check_not_before_utc": iso(generated + timedelta(minutes=args.next_check_minutes)),
        "lanes": lane_rows,
        "raw_boundary": {
            "output_dir": "<local_temp_redacted>",
            "prompt_files": "<local_temp_redacted>",
            "stdout_stderr": "temp_only_not_published",
        },
        "launch_policy": {
            "manual_babysitting_required": False,
            "duration_is_completion_proof": False,
            "watchers_supervise_until_gate": True,
            "phase_advance_requires_all_five_responses": True,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
