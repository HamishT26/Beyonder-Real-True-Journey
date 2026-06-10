#!/usr/bin/env python3
"""Probe Codex CLI from the Windows PowerShell lane and hard-gate slot 40."""

from __future__ import annotations

import argparse
import json
import shutil
import uuid
from pathlib import Path
from typing import Any

from trinity_v44_common import REPO_CODEX_CONFIG, ROOT, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-codex-cli-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-codex-cli-probe-v1.md"


def _ps_probe(command: str) -> dict[str, Any]:
    proc = safe_run(["powershell.exe", "-NoProfile", "-Command", command], timeout=180)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-2400:],
        "stderr_excerpt": proc.stderr[-1600:],
    }


def _parse_json_lines(stdout: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_line in str(stdout or "").splitlines():
        line = raw_line.strip()
        if not line.startswith("{"):
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            rows.append(parsed)
    return rows


def _last_agent_message(events: list[dict[str, Any]]) -> str:
    for row in reversed(events):
        item = row.get("item")
        if row.get("type") == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
            return str(item.get("text") or "")
    return ""


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Codex CLI Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex CLI state: `{payload['codex_cli_state']}`",
        f"- Codex CLI identity state: `{payload['codex_cli_identity_state']}`",
        f"- Target model resolution state: `{payload['target_model_resolution_state']}`",
        f"- Slot 40 induction state: `{payload['slot_40_induction_state']}`",
        f"- Bounded continuity proof state: `{payload['bounded_continuity_proof_state']}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Codex CLI from the Windows PowerShell lane.")
    parser.add_argument("--expected-model", default="gpt-5.4")
    parser.add_argument("--expected-reasoning-effort", default="xhigh")
    parser.add_argument("--repo-config", default=str(REPO_CODEX_CONFIG))
    parser.add_argument("--skip-bounded-session-cycle", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    which_codex = shutil.which("codex")
    probes = {
        "version": _ps_probe("codex --version"),
        "help": _ps_probe("codex --help"),
        "login_help": _ps_probe("codex login --help"),
    }
    login_status = _ps_probe("codex login status")
    blockers: list[str] = []
    warnings: list[str] = []
    codex_cli_state = "callable_in_powershell"
    if any(row["returncode"] != 0 for row in probes.values()):
        codex_cli_state = "blocked_powershell_launcher_failure"
        blockers.append("At least one PowerShell Codex CLI probe failed.")
    launcher_failure = ""
    for row in probes.values():
        text = f"{row['stdout_excerpt']}\n{row['stderr_excerpt']}".lower()
        if "access is denied" in text:
            launcher_failure = "node_access_denied"
            break
    if launcher_failure:
        codex_cli_state = "blocked_node_access_denied"
        blockers.append("PowerShell resolves Codex CLI into a node launcher path that currently returns access denied.")

    target_model_resolution_state = "callable_but_target_model_unproven"
    codex_cli_identity_state = "login_status_unknown"
    bounded_continuity_proof_state = "not_attempted"
    slot_40_induction_state = "deferred_blocked"
    if codex_cli_state == "callable_in_powershell":
        login_text = f"{login_status['stdout_excerpt']}\n{login_status['stderr_excerpt']}".lower()
        if login_status["returncode"] == 0 and "logged in" in login_text:
            codex_cli_identity_state = "explicit_login_status_verified"
        else:
            codex_cli_identity_state = "login_status_unverified"
            warnings.append("Codex CLI is callable, but login status was not explicit.")
    else:
        blockers.append("Codex CLI is not yet a proven runtime lane from the current PowerShell operator surface.")

    bounded_cycle: dict[str, Any] = {
        "session_prompt": "",
        "resume_prompt": "",
        "thread_id": "",
        "first_cycle": {},
        "resume_cycle": {},
        "remembered_token": "",
        "resumed_token": "",
    }
    if codex_cli_state == "callable_in_powershell" and not args.skip_bounded_session_cycle:
        runtime_dir = ROOT / ".local-runtime" / "v44"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        token = f"OMEGA44TOKEN-{uuid.uuid4().hex[:8].upper()}"
        first_output = runtime_dir / "codex-cli-session-1.txt"
        second_output = runtime_dir / "codex-cli-session-2.txt"
        session_prompt = f"Reply with exact text CLI_V44_OK. Also remember token {token} for the next resumed message."
        resume_prompt = "What token did I ask you to remember? Reply with the token only."
        first_run = safe_run(
            [
                "codex",
                "exec",
                "-m",
                args.expected_model,
                "--json",
                "-o",
                str(first_output),
                session_prompt,
            ],
            timeout=900,
        )
        first_events = _parse_json_lines(first_run.stdout)
        thread_id = ""
        for row in first_events:
            if row.get("type") == "thread.started":
                thread_id = str(row.get("thread_id") or "")
                break
        first_message = _last_agent_message(first_events) or (first_output.read_text(encoding="utf-8", errors="replace").strip() if first_output.exists() else "")
        second_run = safe_run(
            [
                "codex",
                "exec",
                "resume",
                "--last",
                "--json",
                "-o",
                str(second_output),
                resume_prompt,
            ],
            timeout=900,
        )
        second_events = _parse_json_lines(second_run.stdout)
        second_message = _last_agent_message(second_events) or (second_output.read_text(encoding="utf-8", errors="replace").strip() if second_output.exists() else "")
        bounded_cycle = {
            "session_prompt": session_prompt,
            "resume_prompt": resume_prompt,
            "thread_id": thread_id,
            "first_cycle": {
                "returncode": first_run.returncode,
                "stdout_excerpt": first_run.stdout[-3200:],
                "stderr_excerpt": first_run.stderr[-2000:],
                "agent_message": first_message,
                "output_file": str(first_output),
            },
            "resume_cycle": {
                "returncode": second_run.returncode,
                "stdout_excerpt": second_run.stdout[-3200:],
                "stderr_excerpt": second_run.stderr[-2000:],
                "agent_message": second_message,
                "output_file": str(second_output),
            },
            "remembered_token": token,
            "resumed_token": second_message.strip(),
        }
        warnings.extend(
            item
            for item in (
                "Codex CLI emitted runtime warnings while still completing the bounded continuity cycle."
                if "WARN codex_state::runtime" in f"{first_run.stdout}\n{second_run.stdout}"
                else "",
                "Codex CLI emitted skill metadata errors during the bounded continuity cycle."
                if "failed to load skill" in f"{first_run.stdout}\n{second_run.stdout}"
                else "",
                "Codex CLI emitted auth transport errors during the bounded continuity cycle."
                if "invalid_grant: session not found" in f"{first_run.stdout}\n{second_run.stdout}"
                else "",
            )
            if item
        )
        if first_run.returncode == 0 and second_run.returncode == 0 and first_message.strip() == "CLI_V44_OK" and second_message.strip() == token:
            bounded_continuity_proof_state = "exec_resume_memory_verified_with_runtime_residuals" if warnings else "exec_resume_memory_verified"
            target_model_resolution_state = f"bounded_exec_verified_on_{args.expected_model}"
            slot_40_induction_state = "deferred_blocked"
            warnings.append("Slot 40 remains hard-gated because bounded continuity is only one part of the full induction rule.")
        else:
            bounded_continuity_proof_state = "exec_resume_failed"
            blockers.append("The bounded CLI exec-and-resume continuity cycle did not complete cleanly.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if codex_cli_state == "callable_in_powershell" and not blockers else "WARN",
        "codex_on_path": bool(which_codex),
        "codex_path": str(which_codex or ""),
        "expected_model": args.expected_model,
        "expected_reasoning_effort": args.expected_reasoning_effort,
        "codex_cli_state": codex_cli_state,
        "codex_cli_identity_state": codex_cli_identity_state,
        "target_model_resolution_state": target_model_resolution_state,
        "bounded_continuity_proof_state": bounded_continuity_proof_state,
        "slot_40_induction_state": slot_40_induction_state,
        "probes": probes,
        "login_status": login_status,
        "bounded_cycle": bounded_cycle,
        "warnings": warnings,
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
