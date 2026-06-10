#!/usr/bin/env python3
"""Probe the V45 Codex CLI lane, slot 40 gate, and bounded candidate task."""

from __future__ import annotations

import argparse
import json
import shutil
import uuid
from pathlib import Path
from typing import Any

from trinity_v45_common import LOCAL_RUNTIME_DIR, ROOT, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-codex-cli-slot40-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v45-codex-cli-slot40-probe-v1.md"


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


def _event_thread_id(events: list[dict[str, Any]]) -> str:
    for row in events:
        if row.get("type") == "thread.started":
            return str(row.get("thread_id") or "")
    return ""


def _parse_agent_json(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _has_auth_refresh_residual(*chunks: str) -> bool:
    haystack = "\n".join(chunks).lower()
    return "invalid_grant: session not found" in haystack or "tokenrefreshfailed" in haystack


def _has_skill_load_residual(*chunks: str) -> bool:
    haystack = "\n".join(chunks).lower()
    return "failed to load skill" in haystack


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Codex CLI Slot 40 Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex CLI state: `{payload['codex_cli_state']}`",
        f"- Codex CLI auth state: `{payload['codex_cli_auth_state']}`",
        f"- Codex CLI model proof state: `{payload['codex_cli_model_proof_state']}`",
        f"- Slot 40 probe state: `{payload['slot_40_probe_state']}`",
        f"- Slot 40 induction state: `{payload['slot_40_induction_state']}`",
        f"- Identity continuity state: `{payload['identity_continuity_state']}`",
        f"- Memory continuity state: `{payload['memory_continuity_state']}`",
        f"- Delegated task state: `{payload['delegated_task_state']}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    if payload.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {row}" for row in payload["warnings"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Codex CLI and the V45 slot 40 gate.")
    parser.add_argument("--expected-model", default="gpt-5.4")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    which_codex = shutil.which("codex")
    blockers: list[str] = []
    warnings: list[str] = []

    version = safe_run(["codex", "--version"], cwd=ROOT, timeout=120)
    login_before = safe_run(["codex", "login", "status"], cwd=ROOT, timeout=120)
    features = safe_run(["codex", "features", "list"], cwd=ROOT, timeout=120)

    codex_cli_state = "callable_in_powershell"
    if version.returncode != 0 or login_before.returncode != 0:
        codex_cli_state = "blocked_powershell_launcher_failure"
        blockers.append("Codex CLI version or login status probe failed in PowerShell.")

    model_prompt = (
        'Do not read or write files. Reply with a single compact JSON object with keys '
        'exact_model_confirmed, self_reported_model, reasoning_effort_visible, and note. '
        'If you cannot independently verify the exact model identifier yourself, set '
        'exact_model_confirmed to false and self_reported_model to null.'
    )
    model_probe = safe_run(
        ["codex", "exec", "--ephemeral", "--json", "-m", args.expected_model, model_prompt],
        cwd=ROOT,
        timeout=900,
    )
    model_events = _parse_json_lines(model_probe.stdout)
    model_message = _last_agent_message(model_events)
    model_payload = _parse_agent_json(model_message)
    if model_payload.get("exact_model_confirmed") is True:
        model_proof_state = "surface_verified_exact_model"
    else:
        model_proof_state = "unverifiable_from_surface"

    token = f"V45TOKEN-{uuid.uuid4().hex[:8].upper()}"
    first_output = LOCAL_RUNTIME_DIR / "slot40-cycle-1.txt"
    second_output = LOCAL_RUNTIME_DIR / "slot40-cycle-2.txt"
    first_prompt = f"Reply with exact text SLOT40_HELLO. Also remember token {token} for the next resumed message."
    second_prompt = "What token did I ask you to remember? Reply with the token only."
    first_run = safe_run(
        ["codex", "exec", "--json", "-m", args.expected_model, "-o", str(first_output), first_prompt],
        cwd=ROOT,
        timeout=1200,
    )
    first_events = _parse_json_lines(first_run.stdout)
    first_message = _last_agent_message(first_events) or (first_output.read_text(encoding="utf-8", errors="replace").strip() if first_output.exists() else "")
    thread_id = _event_thread_id(first_events)
    second_run = safe_run(
        ["codex", "exec", "resume", "--last", "--json", "-o", str(second_output), second_prompt],
        cwd=ROOT,
        timeout=1200,
    )
    second_events = _parse_json_lines(second_run.stdout)
    second_message = _last_agent_message(second_events) or (second_output.read_text(encoding="utf-8", errors="replace").strip() if second_output.exists() else "")

    candidate_prompt = (
        'Reply with a single JSON object with keys "lane" and "summary". '
        'lane must be "slot40_candidate". summary must be one sentence stating that '
        'PowerShell stays primary, WSL is on hold for app switching, and cloud work is gated by billing truth.'
    )
    candidate_run = safe_run(
        ["codex", "exec", "--ephemeral", "--json", "-m", args.expected_model, candidate_prompt],
        cwd=ROOT,
        timeout=900,
    )
    candidate_events = _parse_json_lines(candidate_run.stdout)
    candidate_message = _last_agent_message(candidate_events)
    candidate_payload = _parse_agent_json(candidate_message)

    login_after = safe_run(["codex", "login", "status"], cwd=ROOT, timeout=120)

    auth_residual = _has_auth_refresh_residual(
        model_probe.stdout,
        model_probe.stderr,
        first_run.stdout,
        first_run.stderr,
        second_run.stdout,
        second_run.stderr,
        candidate_run.stdout,
        candidate_run.stderr,
    )
    skill_residual = _has_skill_load_residual(
        model_probe.stdout,
        model_probe.stderr,
        first_run.stdout,
        first_run.stderr,
        second_run.stdout,
        second_run.stderr,
        candidate_run.stdout,
        candidate_run.stderr,
    )

    if auth_residual:
        codex_cli_auth_state = "callable_with_refresh_residuals"
        warnings.append("Codex CLI completed bounded runs but still emitted auth-refresh residuals.")
    elif login_before.returncode == 0 and login_after.returncode == 0:
        codex_cli_auth_state = "stable_login_verified"
    else:
        codex_cli_auth_state = "login_status_unverified"
        blockers.append("Codex CLI login status was not stable across bounded runs.")

    if skill_residual:
        warnings.append("Codex CLI still emitted skill-load residuals after the local Codex-home repair lane.")

    identity_continuity_state = "verified" if first_run.returncode == 0 and first_message.strip() == "SLOT40_HELLO" else "blocked"
    memory_continuity_state = "verified" if second_run.returncode == 0 and second_message.strip() == token else "blocked"
    delegated_task_state = (
        "structured_result_verified"
        if candidate_run.returncode == 0 and candidate_payload.get("lane") == "slot40_candidate" and isinstance(candidate_payload.get("summary"), str)
        else "blocked"
    )

    if identity_continuity_state != "verified":
        blockers.append("The first bounded slot 40 continuity cycle did not return the expected identity marker.")
    if memory_continuity_state != "verified":
        blockers.append("The bounded resume cycle did not preserve the remembered token.")
    if delegated_task_state != "structured_result_verified":
        blockers.append("The candidate delegated task did not return the required structured JSON result.")

    if codex_cli_state != "callable_in_powershell":
        slot_40_probe_state = "candidate_probe_blocked_cli_unavailable"
        slot_40_induction_state = "deferred_blocked"
    elif model_proof_state != "surface_verified_exact_model":
        slot_40_probe_state = "candidate_probe_passed_induction_blocked_model_proof"
        slot_40_induction_state = "deferred_blocked"
    elif blockers:
        slot_40_probe_state = "candidate_probe_bounded_with_residuals"
        slot_40_induction_state = "deferred_blocked"
    else:
        slot_40_probe_state = "candidate_probe_complete"
        slot_40_induction_state = "allowed_ready"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v45_omega",
        "overall_status": "PASS" if codex_cli_state == "callable_in_powershell" and not blockers else "WARN",
        "codex_on_path": bool(which_codex),
        "codex_path": str(which_codex or ""),
        "expected_model": args.expected_model,
        "codex_cli_state": codex_cli_state,
        "codex_cli_auth_state": codex_cli_auth_state,
        "codex_cli_model_proof_state": model_proof_state,
        "identity_continuity_state": identity_continuity_state,
        "memory_continuity_state": memory_continuity_state,
        "delegated_task_state": delegated_task_state,
        "slot_40_probe_state": slot_40_probe_state,
        "slot_40_induction_state": slot_40_induction_state,
        "resolved_model": model_payload.get("self_reported_model"),
        "reasoning_effort_visible": model_payload.get("reasoning_effort_visible"),
        "thread_id": thread_id,
        "version_probe": {
            "returncode": version.returncode,
            "stdout_excerpt": version.stdout[-1200:],
            "stderr_excerpt": version.stderr[-1200:],
        },
        "login_before": {
            "returncode": login_before.returncode,
            "stdout_excerpt": login_before.stdout[-1200:],
            "stderr_excerpt": login_before.stderr[-1200:],
        },
        "login_after": {
            "returncode": login_after.returncode,
            "stdout_excerpt": login_after.stdout[-1200:],
            "stderr_excerpt": login_after.stderr[-1200:],
        },
        "features_probe": {
            "returncode": features.returncode,
            "stdout_excerpt": features.stdout[-2400:],
            "stderr_excerpt": features.stderr[-1200:],
        },
        "model_probe": {
            "returncode": model_probe.returncode,
            "agent_message": model_message,
            "stdout_excerpt": model_probe.stdout[-3200:],
            "stderr_excerpt": model_probe.stderr[-1600:],
            "parsed_payload": model_payload,
        },
        "bounded_cycle": {
            "token": token,
            "thread_id": thread_id,
            "first_cycle": {
                "returncode": first_run.returncode,
                "agent_message": first_message,
                "stdout_excerpt": first_run.stdout[-3200:],
                "stderr_excerpt": first_run.stderr[-1600:],
            },
            "resume_cycle": {
                "returncode": second_run.returncode,
                "agent_message": second_message,
                "stdout_excerpt": second_run.stdout[-3200:],
                "stderr_excerpt": second_run.stderr[-1600:],
            },
        },
        "candidate_task": {
            "returncode": candidate_run.returncode,
            "agent_message": candidate_message,
            "parsed_payload": candidate_payload,
            "stdout_excerpt": candidate_run.stdout[-3200:],
            "stderr_excerpt": candidate_run.stderr[-1600:],
        },
        "warnings": warnings,
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
