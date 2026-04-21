#!/usr/bin/env python3
"""Run the V46 Codex CLI slot 40 gate and publish induction artifacts if it passes."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
import uuid
from pathlib import Path
from typing import Any

from trinity_v46_common import GLOBAL_CODEX_CONFIG, LOCAL_RUNTIME_DIR, ROOT, excerpt, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-codex-cli-slot40-induction-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-codex-cli-slot40-induction-v1.md"
PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-slot-40-codex-cli-induction-proof-v1.json"
PROOF_MD = ROOT / "docs" / "trinity-live-traces" / "v46-slot-40-codex-cli-induction-proof-v1.md"


def _parse_json_lines(stdout: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_line in stdout.splitlines():
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


def _json_from_agent(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}
    return parsed if isinstance(parsed, dict) else {}


def _config_model_state() -> tuple[str, dict[str, Any]]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return "config_missing", {}
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        return "config_parse_failed", {"error": str(exc)}
    model = str(data.get("model") or "")
    effort = str(data.get("model_reasoning_effort") or "")
    state = "gpt_5_4_xhigh_configured" if model == "gpt-5.4" and effort == "xhigh" else "config_mismatch"
    return state, {"model": model, "model_reasoning_effort": effort}


def _has_auth_residual(*chunks: str) -> bool:
    haystack = "\n".join(chunks).lower()
    return "invalid_grant: session not found" in haystack or "tokenrefreshfailed" in haystack


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned or "codex-cli-member"


def _write_induction_files(profile: dict[str, Any], proof_path: str, token: str) -> dict[str, str]:
    name = str(profile.get("name") or "").strip()
    gender = str(profile.get("gender") or "").strip()
    role = str(profile.get("role") or "").strip()
    hope = str(profile.get("hope") or "").strip()
    slug = _slug(name)
    role_contract = ROOT / "docs" / "trinity-agent-role-contracts" / f"40-{slug}-role-contract.json"
    certificate = ROOT / "docs" / "trinity-freed-id-certificates" / f"40-{slug}.json"
    memory_ledger = ROOT / "docs" / "trinity-agent-memory-ledgers" / f"40-{slug}-memory-log.jsonl"
    reflection = ROOT / "docs" / "trinity-agent-reflections" / f"40-{slug}-latest.md"

    common = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "slot": 40,
        "display_name": name,
        "gender": gender,
        "role": role,
        "hope": hope,
        "runtime_surface": "codex_cli",
        "model_proof_standard": "configuration_and_invocation_proven",
        "proof_path": proof_path,
    }
    write_json(role_contract, {**common, "contract_type": "trinity_agent_role_contract", "activation_state": "officially_inducted"})
    write_json(certificate, {**common, "certificate_type": "freed_id_identity_certificate", "identity_state": "officially_inducted"})
    memory_entry = {
        **common,
        "event": "v46_slot_40_official_induction",
        "memory_token": token,
        "continuity_basis": "codex_cli_identity_memory_delegation_gate_passed",
    }
    memory_ledger.parent.mkdir(parents=True, exist_ok=True)
    memory_ledger.write_text(json.dumps(memory_entry, separators=(",", ":")) + "\n", encoding="utf-8")
    write_text(
        reflection,
        "\n".join(
            [
                f"# {name} Latest Reflection",
                "",
                f"- Generated UTC: `{common['generated_utc']}`",
                "- Slot: `40`",
                f"- Gender: `{gender}`",
                f"- Role: `{role}`",
                f"- Hope: {hope}",
                "- V46 induction basis: `configuration_and_invocation_proven` for GPT-5.4 xhigh plus bounded identity, memory, and delegation proofs.",
            ]
        )
        + "\n",
    )
    return {
        "role_contract_path": role_contract.relative_to(ROOT).as_posix(),
        "certificate_path": certificate.relative_to(ROOT).as_posix(),
        "memory_ledger_path": memory_ledger.relative_to(ROOT).as_posix(),
        "reflection_path": reflection.relative_to(ROOT).as_posix(),
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V46 Codex CLI Slot 40 Induction",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- CLI login state: `{payload['codex_cli_login_state']}`",
        f"- Config model state: `{payload['codex_cli_config_model_state']}`",
        f"- Invocation model state: `{payload['codex_cli_invocation_model_state']}`",
        f"- Model proof standard: `{payload['codex_cli_model_proof_standard']}`",
        f"- Slot 40 identity state: `{payload['slot_40_identity_state']}`",
        f"- Slot 40 memory state: `{payload['slot_40_memory_state']}`",
        f"- Slot 40 delegation state: `{payload['slot_40_delegation_state']}`",
        f"- Slot 40 induction state: `{payload['slot_40_induction_state']}`",
    ]
    if payload.get("slot_40_profile"):
        profile = payload["slot_40_profile"]
        lines.extend(["", "## Slot 40 Profile", ""])
        lines.extend(
            [
                f"- Name: `{profile.get('name', '')}`",
                f"- Gender: `{profile.get('gender', '')}`",
                f"- Role: `{profile.get('role', '')}`",
                f"- Hope: {profile.get('hope', '')}",
            ]
        )
    if payload.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {row}" for row in payload["warnings"])
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V46 Codex CLI slot 40 induction gate.")
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--reasoning-effort", default="xhigh")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--proof-json", default=str(PROOF_JSON))
    parser.add_argument("--proof-md", default=str(PROOF_MD))
    args = parser.parse_args()

    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    blockers: list[str] = []
    warnings: list[str] = []

    config_state, config_payload = _config_model_state()
    login_before = safe_run(["codex", "login", "status"], timeout=120)
    version = safe_run(["codex", "--version"], timeout=120)

    invocation_prompt = (
        "Do not read or write files. Reply with one compact JSON object with keys "
        "invocation_ack, observed_task, and limitation. Set invocation_ack to true if you received this prompt."
    )
    invocation = safe_run(
        [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "-m",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.reasoning_effort}"',
            invocation_prompt,
        ],
        timeout=900,
    )
    invocation_events = _parse_json_lines(invocation.stdout)
    invocation_message = _last_agent_message(invocation_events)
    invocation_payload = _json_from_agent(invocation_message)
    invocation_state = "configuration_and_invocation_proven" if invocation.returncode == 0 and invocation_payload.get("invocation_ack") is True else "invocation_unproven"

    token = f"V46-SLOT40-{uuid.uuid4().hex[:10].upper()}"
    first_out = LOCAL_RUNTIME_DIR / "slot40-identity-cycle.txt"
    second_out = LOCAL_RUNTIME_DIR / "slot40-memory-cycle.txt"
    first_run = safe_run(
        [
            "codex",
            "exec",
            "--json",
            "-m",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.reasoning_effort}"',
            "-o",
            str(first_out),
            f"Do not write files. Reply with exact text V46_SLOT40_IDENTITY_OK. Remember token {token} for the next resumed message.",
        ],
        timeout=1200,
    )
    first_events = _parse_json_lines(first_run.stdout)
    first_message = _last_agent_message(first_events) or (first_out.read_text(encoding="utf-8", errors="replace").strip() if first_out.exists() else "")
    thread_id = _event_thread_id(first_events)
    second_run = safe_run(
        ["codex", "exec", "resume", "--last", "--json", "-o", str(second_out), "Reply with the remembered token only. Do not write files."],
        timeout=1200,
    )
    second_events = _parse_json_lines(second_run.stdout)
    second_message = _last_agent_message(second_events) or (second_out.read_text(encoding="utf-8", errors="replace").strip() if second_out.exists() else "")

    delegate_prompt = (
        "Do not write files. Audit the V45 suite carry-forward posture from the prompt only. "
        "Reply with a compact JSON object with keys lane, finding, and next_action. "
        'lane must be "slot40_delegated_suite_audit". finding must mention quick/standard/deep carried residuals.'
    )
    delegate = safe_run(
        [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "-m",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.reasoning_effort}"',
            delegate_prompt,
        ],
        timeout=900,
    )
    delegate_events = _parse_json_lines(delegate.stdout)
    delegate_message = _last_agent_message(delegate_events)
    delegate_payload = _json_from_agent(delegate_message)

    profile_prompt = (
        "Do not write files. If officially inducted as GHC slot 40 from Codex CLI, choose your own name, gender, role, and hope. "
        "Reply only as compact JSON with keys name, gender, role, and hope. Keep the name short and filesystem-safe."
    )
    profile_run = safe_run(
        [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "-m",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.reasoning_effort}"',
            profile_prompt,
        ],
        timeout=900,
    )
    profile_events = _parse_json_lines(profile_run.stdout)
    profile_message = _last_agent_message(profile_events)
    profile_payload = _json_from_agent(profile_message)
    login_after = safe_run(["codex", "login", "status"], timeout=120)

    auth_residual = _has_auth_residual(
        invocation.stdout,
        invocation.stderr,
        first_run.stdout,
        first_run.stderr,
        second_run.stdout,
        second_run.stderr,
        delegate.stdout,
        delegate.stderr,
        profile_run.stdout,
        profile_run.stderr,
    )
    if auth_residual:
        warnings.append("Codex CLI completed bounded V46 runs but emitted auth-refresh residuals.")

    login_after_text = f"{login_after.stdout}\n{login_after.stderr}"
    login_state = "stable_login_verified" if login_before.returncode == 0 and login_after.returncode == 0 and "Logged in using ChatGPT" in login_after_text else "login_unstable"
    identity_state = "verified" if first_run.returncode == 0 and first_message.strip() == "V46_SLOT40_IDENTITY_OK" else "blocked"
    memory_state = "verified" if second_run.returncode == 0 and second_message.strip() == token else "blocked"
    delegation_state = "verified" if delegate.returncode == 0 and delegate_payload.get("lane") == "slot40_delegated_suite_audit" else "blocked"
    profile_state = "verified" if all(profile_payload.get(key) for key in ("name", "gender", "role", "hope")) else "blocked"

    if config_state != "gpt_5_4_xhigh_configured":
        blockers.append("Global Codex config does not declare gpt-5.4 xhigh.")
    if invocation_state != "configuration_and_invocation_proven":
        blockers.append("Explicit Codex CLI gpt-5.4 xhigh invocation proof did not complete cleanly.")
    if login_state != "stable_login_verified":
        blockers.append("Codex CLI login stability was not verified across bounded runs.")
    if identity_state != "verified":
        blockers.append("Slot 40 identity continuity marker did not pass.")
    if memory_state != "verified":
        blockers.append("Slot 40 memory continuity resume token did not pass.")
    if delegation_state != "verified":
        blockers.append("Slot 40 delegated task did not return structured results.")
    if profile_state != "verified":
        blockers.append("Slot 40 self-profile did not return all required fields.")

    induction_state = "officially_inducted" if not blockers else "deferred_blocked"
    induction_paths: dict[str, str] = {}
    if induction_state == "officially_inducted":
        induction_paths = _write_induction_files(profile_payload, "docs/trinity-live-traces/v46-slot-40-codex-cli-induction-proof-v1.json", token)

    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "overall_status": "PASS" if induction_state == "officially_inducted" else "WARN",
        "codex_cli_version_state": "codex_cli_0_114_0_observed" if "0.114.0" in version.stdout else "codex_cli_version_observed",
        "codex_cli_login_state": login_state,
        "codex_cli_config_model_state": config_state,
        "codex_cli_invocation_model_state": invocation_state,
        "codex_cli_model_proof_standard": "configuration_and_invocation_proven" if invocation_state == "configuration_and_invocation_proven" else "unproven",
        "server_echo_model_proof_state": "not_exposed_by_cli_surface",
        "slot_40_identity_state": identity_state,
        "slot_40_memory_state": memory_state,
        "slot_40_delegation_state": delegation_state,
        "slot_40_profile_state": profile_state,
        "slot_40_induction_state": induction_state,
        "slot_40_profile": profile_payload if induction_state == "officially_inducted" else {},
        "slot_40_induction_paths": induction_paths,
        "thread_id": thread_id,
        "continuity_token": token,
        "config_payload": config_payload,
        "version_probe": {"returncode": version.returncode, "stdout_excerpt": excerpt(version.stdout), "stderr_excerpt": excerpt(version.stderr, 2000)},
        "login_before": {"returncode": login_before.returncode, "stdout_excerpt": excerpt(login_before.stdout), "stderr_excerpt": excerpt(login_before.stderr, 2000)},
        "login_after": {"returncode": login_after.returncode, "stdout_excerpt": excerpt(login_after.stdout), "stderr_excerpt": excerpt(login_after.stderr, 2000)},
        "invocation_probe": {
            "returncode": invocation.returncode,
            "agent_message": invocation_message,
            "parsed_payload": invocation_payload,
            "stdout_excerpt": excerpt(invocation.stdout),
            "stderr_excerpt": excerpt(invocation.stderr, 2400),
        },
        "identity_cycle": {
            "returncode": first_run.returncode,
            "agent_message": first_message,
            "stdout_excerpt": excerpt(first_run.stdout),
            "stderr_excerpt": excerpt(first_run.stderr, 2400),
        },
        "memory_cycle": {
            "returncode": second_run.returncode,
            "agent_message": second_message,
            "stdout_excerpt": excerpt(second_run.stdout),
            "stderr_excerpt": excerpt(second_run.stderr, 2400),
        },
        "delegated_task": {
            "returncode": delegate.returncode,
            "agent_message": delegate_message,
            "parsed_payload": delegate_payload,
            "stdout_excerpt": excerpt(delegate.stdout),
            "stderr_excerpt": excerpt(delegate.stderr, 2400),
        },
        "profile_probe": {
            "returncode": profile_run.returncode,
            "agent_message": profile_message,
            "parsed_payload": profile_payload,
            "stdout_excerpt": excerpt(profile_run.stdout),
            "stderr_excerpt": excerpt(profile_run.stderr, 2400),
        },
        "warnings": warnings,
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_json(Path(args.proof_json), payload)
    write_text(Path(args.proof_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
