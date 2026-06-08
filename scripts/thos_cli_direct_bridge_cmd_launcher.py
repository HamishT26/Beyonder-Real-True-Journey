#!/usr/bin/env python3
"""Launch read-only Codex CLI lanes through temp .cmd bridge runners."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


REQUIRED_HEADINGS = [
    "COMMAND PROPOSALS (10+)",
    "SYSTEM EXPANSION PROPOSALS (10+)",
    "SKILL OR MICRO-WORKFLOW PROPOSALS (10+)",
    "EUREKA TASKS (10+)",
    "RISKS AND BLOCKERS",
    "X2 BUILD PRIORITIES",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def parse_lane(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("lane must use NAME=SAFE_BRIDGE form")
    name, safe = raw.split("=", 1)
    name = name.strip()
    safe = safe.strip()
    if not name or not safe:
        raise argparse.ArgumentTypeError("lane name and safe bridge must be non-empty")
    if any(ch in safe for ch in "\\/:*?\"<>| "):
        raise argparse.ArgumentTypeError("safe bridge must be a simple filename stem without spaces")
    return name, safe


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Direct Bridge CMD Launch",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- next_manual_status_check_not_before_utc: `{payload['next_manual_status_check_not_before_utc']}`",
        "",
        "Launched lanes:",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane['launch_status']}`, safe bridge `{lane['safe_output_bridge']}`"
        )
    lines.extend(
        [
            "",
            "Prompts, stdout/stderr, local temp paths, process IDs, and raw lane text remain unpublished.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_prestart_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Launch Prestart Receipt",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- next_manual_status_check_not_before_utc: `{payload['next_manual_status_check_not_before_utc']}`",
        "",
        "Planned lanes:",
    ]
    for lane in payload["lanes"]:
        lines.append(f"- {lane['lane']}: safe bridge `{lane['safe_output_bridge']}`")
    lines.extend(
        [
            "",
            "This prestart receipt is written before child process launch. Prompts, local temp paths, process IDs, stdout/stderr, and raw lane text remain unpublished.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_heading_contract_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Heading Contract",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "- raw_prompt_published: `False`",
        "",
        "Required headings:",
    ]
    for row in payload["headings"]:
        lines.append(f"- {row['heading']}: `{row['present']}`")
    lines.extend(
        [
            "",
            "This receipt publishes heading presence only. It does not publish the prompt body or raw lane responses.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def heading_present(prompt_template: str, heading: str) -> bool:
    pattern = re.compile(rf"(?im)^\s*#*\s*{re.escape(heading)}\s*:?\s*$")
    return bool(pattern.search(prompt_template))


def runner_text(
    codex_cmd: Path,
    repo: Path,
    prompt_file: Path,
    last_file: Path,
    normalized_last_file: Path,
    events_file: Path,
    stderr_file: Path,
) -> str:
    return (
        "@echo off\n"
        f"call \"{codex_cmd}\" --search --ask-for-approval never exec --sandbox read-only "
        f"--cd \"{repo}\" --output-last-message \"{last_file}\" --json - "
        f"< \"{prompt_file}\" > \"{events_file}\" 2> \"{stderr_file}\"\n"
        f"if exist \"{last_file}\" copy /Y \"{last_file}\" \"{normalized_last_file}\" >nul\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--codex-cmd", default=r"C:\Users\hamis\AppData\Roaming\npm\codex.cmd")
    parser.add_argument("--prompt-template", required=True)
    parser.add_argument("--lane", action="append", required=True, type=parse_lane)
    parser.add_argument("--next-check-minutes", type=int, default=15)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    parser.add_argument("--prestart-receipt-json")
    parser.add_argument("--prestart-receipt-md")
    parser.add_argument("--heading-contract-json")
    parser.add_argument("--heading-contract-md")
    parser.add_argument("--require-heading-contract", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    repo = Path(args.repo).resolve()
    codex_cmd = Path(args.codex_cmd)
    prompt_template = Path(args.prompt_template).read_text(encoding="utf-8")
    generated = utc_now()
    next_check = generated + timedelta(minutes=args.next_check_minutes)

    planned_lanes = [
        {
            "lane": lane_name,
            "safe_output_bridge": safe_bridge,
            "raw_boundary": "temp_only_not_published",
        }
        for lane_name, safe_bridge in args.lane
    ]
    if args.prestart_receipt_json or args.prestart_receipt_md:
        prestart_payload: dict[str, Any] = {
            "artifact_type": "cli_launch_prestart_receipt",
            "phase_slug": args.phase_slug,
            "generated_utc": iso(generated),
            "overall_status": "PASS_CLI_LAUNCH_PRESTART_RECORDED",
            "next_manual_status_check_not_before_utc": iso(next_check),
            "lanes": planned_lanes,
            "raw_boundary": {
                "prompt_body_published": False,
                "local_temp_paths_published": False,
                "process_ids_published": False,
                "stdout_stderr_published": False,
                "raw_lane_text_published": False,
            },
            "claim_boundary": {
                "gmut_gate_state": "open",
                "canon_promotion": "not_claimed",
            },
        }
        if args.prestart_receipt_json:
            write_json(Path(args.prestart_receipt_json), prestart_payload)
        if args.prestart_receipt_md:
            write_prestart_md(Path(args.prestart_receipt_md), prestart_payload)
    if args.heading_contract_json or args.heading_contract_md or args.require_heading_contract:
        heading_rows = [
            {"heading": heading, "present": heading_present(prompt_template, heading)}
            for heading in REQUIRED_HEADINGS
        ]
        contract_ok = all(row["present"] for row in heading_rows)
        heading_payload: dict[str, Any] = {
            "artifact_type": "cli_heading_contract_preflight",
            "phase_slug": args.phase_slug,
            "generated_utc": iso(generated),
            "overall_status": "PASS_CLI_HEADING_CONTRACT" if contract_ok else "OPEN_GAP_CLI_HEADING_CONTRACT",
            "headings": heading_rows,
            "raw_boundary": {
                "prompt_body_published": False,
                "raw_lane_text_published": False,
                "local_temp_paths_published": False,
            },
            "claim_boundary": {
                "gmut_gate_state": "open",
                "canon_promotion": "not_claimed",
            },
        }
        if args.heading_contract_json:
            write_json(Path(args.heading_contract_json), heading_payload)
        if args.heading_contract_md:
            write_heading_contract_md(Path(args.heading_contract_md), heading_payload)
        if args.require_heading_contract and not contract_ok:
            print(json.dumps({"status": heading_payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
            return 2

    lane_receipts: list[dict[str, Any]] = []
    for lane_name, safe_bridge in args.lane:
        prompt_file = output_dir / f"{safe_bridge}-prompt.txt"
        last_file = output_dir / f"{safe_bridge}-last-message.txt"
        normalized_last_file = output_dir / f"{lane_name}-last-message.txt"
        events_file = output_dir / f"{safe_bridge}-events.jsonl"
        stderr_file = output_dir / f"{safe_bridge}-stderr.txt"
        runner_file = output_dir / f"{safe_bridge}-runner.cmd"
        prompt_file.write_text(f"Lane identity: {lane_name}\n\n{prompt_template}", encoding="utf-8")
        for file_path in (last_file, normalized_last_file, events_file, stderr_file):
            if file_path.exists():
                file_path.unlink()
        runner_file.write_text(
            runner_text(codex_cmd, repo, prompt_file, last_file, normalized_last_file, events_file, stderr_file),
            encoding="ascii",
        )
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(
            ["cmd.exe", "/d", "/c", str(runner_file)],
            creationflags=creationflags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        lane_receipts.append(
            {
                "lane": lane_name,
                "safe_output_bridge": safe_bridge,
                "normalized_final_message_alias": True,
                "launch_status": "PASS_CMD_BRIDGE_PROCESS_STARTED",
                "process_started": proc.poll() is None,
                "process_id_redacted": True,
                "raw_boundary": "temp_only_not_published",
            }
        )

    payload: dict[str, Any] = {
        "artifact_type": "cli_direct_bridge_cmd_launcher",
        "phase_slug": args.phase_slug,
        "generated_utc": iso(generated),
        "overall_status": "PASS_CMD_BRIDGE_CLI_LANES_LAUNCHED",
        "next_manual_status_check_not_before_utc": iso(next_check),
        "lanes": lane_receipts,
        "launch_policy": {
            "wrapper": "temp_cmd_runner_files",
            "route": "existing_read_only_cli_lanes",
            "sandbox": "read-only",
            "approval_policy": "never",
            "web_search_enabled": True,
            "manual_babysitting_required": False,
            "duration_is_completion_proof": False,
        },
        "raw_boundary": {
            "output_dir": "<local_temp_redacted>",
            "prompt_files": "<local_temp_redacted>",
            "runner_files": "<local_temp_redacted>",
            "stdout_stderr": "temp_only_not_published",
            "raw_lane_text_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
