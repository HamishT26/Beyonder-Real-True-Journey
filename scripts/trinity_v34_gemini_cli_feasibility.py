#!/usr/bin/env python3
"""Emit a bounded feasibility note for a Gemini CLI operator path."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v34_cloud_common import PHASE, now_iso, run_cmd, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v34-gemini-cli-feasibility-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v34-gemini-cli-feasibility-v1.md"
REPO_HINT = "https://github.com/google-gemini/gemini-cli"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V34 Gemini CLI Feasibility Note",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Package hint: `{payload.get('package_hint', '') or 'unconfirmed'}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    if payload.get("notes"):
        lines.extend(["", "## Notes", ""])
        for note in payload["notes"]:
            lines.append(f"- {note}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def resolve_command(preferred: str) -> list[str]:
    candidates = []
    if not preferred.lower().endswith(".cmd"):
        candidates.append(f"{preferred}.cmd")
    candidates.append(preferred)
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    return [preferred]


def safe_run(args: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return run_cmd([*resolve_command(args[0]), *args[1:]], timeout=timeout)
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))


def main() -> int:
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "package_hint": os.getenv("GEMINI_CLI_PACKAGE", "").strip() or "@google/gemini-cli",
        "completed_steps": [],
        "blockers": [],
        "notes": [
            "This lane is intentionally a feasibility note, not a claimed runtime proof.",
            "The official repo documents `npx @google/gemini-cli` and `npm install -g @google/gemini-cli` as supported entry paths.",
        ],
    }

    node = safe_run(["node", "--version"], timeout=10)
    npm = safe_run(["npm", "--version"], timeout=10)
    npx = safe_run(["npx", "--version"], timeout=10)
    payload["toolchain_checks"] = {
        "node": {"returncode": node.returncode, "stdout": node.stdout.strip(), "stderr": node.stderr.strip()},
        "npm": {"returncode": npm.returncode, "stdout": npm.stdout.strip(), "stderr": npm.stderr.strip()},
        "npx": {"returncode": npx.returncode, "stdout": npx.stdout.strip(), "stderr": npx.stderr.strip()},
    }

    if node.returncode != 0 or npm.returncode != 0 or npx.returncode != 0:
        payload["proof_state"] = "toolchain_missing"
        payload["overall_status"] = "FAIL"
        payload["blockers"].append("Node, npm, or npx was not available in the current shell.")
        write_outputs(payload)
        return 1

    payload["completed_steps"].extend(["node_detected", "npm_detected", "npx_detected"])
    payload["repo_hint"] = REPO_HINT
    help_run = safe_run(["npx", "--yes", payload["package_hint"], "--help"], timeout=300)
    payload["help_check"] = {
        "returncode": help_run.returncode,
        "stdout": help_run.stdout.strip()[:4000],
        "stderr": help_run.stderr.strip()[:4000],
    }
    if help_run.returncode != 0:
        payload["proof_state"] = "help_invocation_blocked"
        payload["overall_status"] = "WARN"
        payload["blockers"].append("The Gemini CLI toolchain is present, but the bounded `--help` invocation did not complete cleanly.")
        write_outputs(payload)
        return 1

    payload["completed_steps"].append("help_invocation_verified")
    payload["proof_state"] = "cli_help_verified"
    payload["overall_status"] = "PASS"
    payload["notes"].append(f"The bounded invocation path is available through `{payload['package_hint']}`.")

    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
