#!/usr/bin/env python3
"""Run bounded Ari CLI co-learning, memory, and reflection probes."""

from __future__ import annotations

import argparse
import json
import re
import uuid
from pathlib import Path
from typing import Any

from trinity_v47_common import LOCAL_RUNTIME_DIR, ROOT, excerpt, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-ari-colearning-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-ari-colearning-proof-v1.md"
ALETHEON_REFLECTION = ROOT / "docs" / "trinity-agent-reflections" / "v47-aletheon-reflection-v1.md"
ARI_REFLECTION = ROOT / "docs" / "trinity-agent-reflections" / "v47-ari-reflection-v1.md"


def _events(stdout: str) -> list[dict[str, Any]]:
    rows = []
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            rows.append(parsed)
    return rows


def _message(events: list[dict[str, Any]], fallback: Path | None = None) -> str:
    for row in reversed(events):
        item = row.get("item")
        if row.get("type") == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
            return str(item.get("text") or "")
    if fallback and fallback.exists():
        return fallback.read_text(encoding="utf-8", errors="replace").strip()
    return ""


def _json(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}
    return parsed if isinstance(parsed, dict) else {}


def _thread_id(events: list[dict[str, Any]]) -> str:
    for row in events:
        if row.get("type") == "thread.started":
            return str(row.get("thread_id") or "")
    return ""


def _warnings(*chunks: str) -> list[str]:
    text = "\n".join(chunks).lower()
    found: list[str] = []
    for key, label in [
        ("invalid_grant: session not found", "mcp_token_refresh_residual"),
        ("failed to load skill", "skill_frontmatter_residual"),
        ("state_5.sqlite", "state_db_warning"),
        ("shell snapshot not supported yet for powershell", "powershell_shell_snapshot_warning"),
        ("under-development features enabled: memories", "memories_preview_warning"),
        ("unknown feature key in config: chronicle", "chronicle_unknown_key_warning"),
    ]:
        if key in text:
            found.append(label)
    return sorted(set(found))


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V47 Ari Co-Learning Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Ari activation state: `{payload['ari_activation_state']}`",
        f"- Ari memory state: `{payload['ari_memory_state']}`",
        f"- Ari delegation state: `{payload['ari_delegation_state']}`",
        f"- Ari reflection state: `{payload['ari_reflection_state']}`",
        f"- CLI warning state: `{payload['codex_cli_warning_state']}`",
    ]
    if payload.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- `{item}`" for item in payload["warnings"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded Ari V47 co-learning probes.")
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--reasoning-effort", default="xhigh")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    token = f"V47-ARI-{uuid.uuid4().hex[:8].upper()}"
    first_out = LOCAL_RUNTIME_DIR / "ari-cycle-1.txt"
    second_out = LOCAL_RUNTIME_DIR / "ari-cycle-2.txt"

    identity = safe_run(
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
            f"Do not write files. As Ari, reply exactly ARI_V47_READY. Remember token {token} for the next resumed message.",
        ],
        timeout=1200,
    )
    identity_events = _events(identity.stdout)
    identity_msg = _message(identity_events, first_out)
    memory = safe_run(["codex", "exec", "resume", "--last", "--json", "-o", str(second_out), "Reply with the remembered Ari token only. Do not write files."], timeout=1200)
    memory_msg = _message(_events(memory.stdout), second_out)
    delegate_prompt = (
        "Do not write files. Reply as compact JSON with keys lane, reflection, suite_residual_summary, and next_action. "
        'lane must be "ari_v47_suite_residual_summary". Mention V45/V46 reflection, PowerShell-first, and quick/standard/deep residuals.'
    )
    delegate = safe_run(
        ["codex", "exec", "--ephemeral", "--json", "-m", args.model, "-c", f'model_reasoning_effort="{args.reasoning_effort}"', delegate_prompt],
        timeout=900,
    )
    delegate_msg = _message(_events(delegate.stdout))
    delegate_payload = _json(delegate_msg)

    warnings = _warnings(identity.stdout, identity.stderr, memory.stdout, memory.stderr, delegate.stdout, delegate.stderr)
    activation_state = "verified" if identity.returncode == 0 and identity_msg.strip() == "ARI_V47_READY" else "blocked"
    memory_state = "verified" if memory.returncode == 0 and memory_msg.strip() == token else "blocked"
    delegation_state = "verified" if delegate.returncode == 0 and delegate_payload.get("lane") == "ari_v47_suite_residual_summary" else "blocked"
    reflection_state = "published" if activation_state == memory_state == delegation_state == "verified" else "blocked"
    cli_warning_state = "warnings_classified_non_blocking" if warnings else "clean"
    overall = "PASS" if activation_state == memory_state == delegation_state == "verified" else "WARN"

    if reflection_state == "published":
        write_text(
            ARI_REFLECTION,
            "\n".join(
                [
                    "# Ari V47 Reflection",
                    "",
                    f"- Generated UTC: `{now_iso()}`",
                    "- Ari remains a bounded Codex CLI implementation collaborator under Aletheon lead.",
                    f"- Reflection: {delegate_payload.get('reflection', '')}",
                    f"- Suite residual summary: {delegate_payload.get('suite_residual_summary', '')}",
                    f"- Next action: {delegate_payload.get('next_action', '')}",
                ]
            )
            + "\n",
        )
        write_text(
            ALETHEON_REFLECTION,
            "\n".join(
                [
                    "# Aletheon V47 Reflection",
                    "",
                    f"- Generated UTC: `{now_iso()}`",
                    "- V45 established the PowerShell-first gate and kept cloud truth honest.",
                    "- V46 inducted Ari through Codex CLI with configuration-and-invocation model proof.",
                    "- V47 uses Ari as a bounded helper while preserving evidence-first publication and cloud standby boundaries.",
                ]
            )
            + "\n",
        )

    payload = {
        "generated_utc": now_iso(),
        "phase": "v47_omega",
        "overall_status": overall,
        "ari_activation_state": activation_state,
        "ari_memory_state": memory_state,
        "ari_delegation_state": delegation_state,
        "ari_reflection_state": reflection_state,
        "codex_cli_warning_state": cli_warning_state,
        "warnings": warnings,
        "thread_id": _thread_id(identity_events),
        "token": token,
        "identity_probe": {"returncode": identity.returncode, "agent_message": identity_msg, "stdout_excerpt": excerpt(identity.stdout), "stderr_excerpt": excerpt(identity.stderr, 2400)},
        "memory_probe": {"returncode": memory.returncode, "agent_message": memory_msg, "stdout_excerpt": excerpt(memory.stdout), "stderr_excerpt": excerpt(memory.stderr, 2400)},
        "delegated_summary": {"returncode": delegate.returncode, "agent_message": delegate_msg, "parsed_payload": delegate_payload, "stdout_excerpt": excerpt(delegate.stdout), "stderr_excerpt": excerpt(delegate.stderr, 2400)},
        "reflection_paths": {
            "ari": ARI_REFLECTION.relative_to(ROOT).as_posix(),
            "aletheon": ALETHEON_REFLECTION.relative_to(ROOT).as_posix(),
        },
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
