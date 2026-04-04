#!/usr/bin/env python3
"""Run the bounded V32 session closeout chain."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import now_iso, read_json, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-session-closeout-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-session-closeout-proof-v1.md"
PYTHON = sys.executable


def step(command: list[str], timeout: int = 1800) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Session Closeout Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Session closeout state: `{payload['session_closeout_state']}`",
        f"- Archive label: `{payload['archive_label']}`",
        "",
        "## Step Results",
        "",
    ]
    for item in payload.get("steps", []):
        lines.append(f"- `{item['name']}` -> returncode `{item['result']['returncode']}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V32 session closeout chain.")
    parser.add_argument("--archive-label", default="v32-session-closeout")
    parser.add_argument("--keep-stamps", type=int, default=2)
    parser.add_argument("--keep-archives", type=int, default=3)
    parser.add_argument("--include-workbench-pycache", action="store_true")
    args = parser.parse_args()
    workbench_flag = ["--include-workbench-pycache"] if args.include_workbench_pycache else []

    steps = [
        {
            "name": "archive",
            "command": [
                PYTHON,
                "scripts/trinity_zip_memory_converter.py",
                "archive",
                "--label",
                args.archive_label,
            ],
        },
        {
            "name": "prune_dry_run",
            "command": [
                PYTHON,
                "scripts/trinity_storage_retention.py",
                "--dry-run",
                "--clear-pycache",
                "--keep-stamps",
                str(args.keep_stamps),
                "--keep-archives",
                str(args.keep_archives),
            ]
            + workbench_flag,
        },
        {
            "name": "prune_apply",
            "command": [
                PYTHON,
                "scripts/trinity_storage_retention.py",
                "--clear-pycache",
                "--keep-stamps",
                str(args.keep_stamps),
                "--keep-archives",
                str(args.keep_archives),
            ]
            + workbench_flag,
        },
        {
            "name": "memory_bank_refresh",
            "command": [
                PYTHON,
                "scripts/trinity_memory_bank_sync.py",
                "--label",
                args.archive_label,
            ],
        },
        {
            "name": "memory_bank_validator",
            "command": [
                PYTHON,
                "scripts/trinity_memory_bank_validator.py",
            ],
        },
    ]

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "PASS",
        "session_closeout_state": "completed",
        "archive_label": args.archive_label,
        "steps": [],
        "blockers": [],
    }

    for item in steps:
        result = step(item["command"])
        payload["steps"].append({"name": item["name"], "result": result})
        if result["returncode"] != 0 and payload["overall_status"] == "PASS":
            payload["overall_status"] = "WARN"
            payload["session_closeout_state"] = "completed_with_blockers"
            payload["blockers"].append(f"{item['name']} returned {result['returncode']}")

    for path in (
        ROOT / "docs" / "trinity-storage-prune-latest.json",
        ROOT / "docs" / "trinity-memory-bank-sync-latest.json",
        ROOT / "docs" / "trinity-memory-bank-validation-latest.json",
    ):
        if path.exists():
            key = path.stem.replace("-", "_")
            try:
                payload[key] = read_json(path)
            except json.JSONDecodeError:
                payload[key] = {"error": "invalid_json"}

    write_outputs(payload)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
