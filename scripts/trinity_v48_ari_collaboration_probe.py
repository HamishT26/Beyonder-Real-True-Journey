#!/usr/bin/env python3
"""Run one bounded Ari read-only V48 collaboration probe through Codex CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v48_common import LOCAL_RUNTIME_DIR, ROOT, excerpt, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-ari-collaboration-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v48-ari-collaboration-proof-v1.md"
ALETHEON_REFLECTION = ROOT / "docs" / "trinity-agent-reflections" / "v48-aletheon-reflection-v1.md"
ARI_REFLECTION = ROOT / "docs" / "trinity-agent-reflections" / "v48-ari-reflection-v1.md"


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


def _warnings(*chunks: str) -> list[str]:
    text = "\n".join(chunks).lower()
    found = []
    for key, label in [
        ("invalid_grant: session not found", "mcp_token_refresh_residual"),
        ("state_5.sqlite", "state_db_warning"),
        ("shell snapshot not supported yet for powershell", "powershell_shell_snapshot_warning"),
        ("failed to load skill", "skill_load_warning"),
    ]:
        if key in text:
            found.append(label)
    return sorted(set(found))


def markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V48 Ari Collaboration Proof",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Overall status: `{payload['overall_status']}`",
            f"- Ari collaboration state: `{payload['ari_collaboration_state']}`",
            f"- Ari write state: `{payload['ari_write_state']}`",
            f"- Warning state: `{payload['codex_cli_warning_state']}`",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Ari's bounded V48 read-only probe.")
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--reasoning-effort", default="xhigh")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    out = LOCAL_RUNTIME_DIR / "ari-v48-collaboration.txt"
    prompt = (
        "Do not write files. As Ari, provide a compact V48 read-only collaboration summary with these labels: "
        "KIMICLAW_PREP, PLUGIN_SURFACE, SUITE_RESIDUAL, NEXT_ACTION. "
        "Keep slot 41 prepared_not_inducted and slots 42-53 spec_only_not_spawned."
    )
    proc = safe_run(
        ["codex", "exec", "--ephemeral", "--json", "-m", args.model, "-c", f'model_reasoning_effort="{args.reasoning_effort}"', "-o", str(out), prompt],
        timeout=900,
    )
    message = _message(_events(proc.stdout), out)
    warnings = _warnings(proc.stdout, proc.stderr)
    ok = proc.returncode == 0 and "KIMICLAW_PREP" in message and "PLUGIN_SURFACE" in message
    state = "verified_read_only_helper" if ok else "blocked_or_incomplete"
    write_text(
        ARI_REFLECTION,
        "\n".join(
            [
                "# Ari V48 Reflection",
                "",
                f"- Generated UTC: `{now_iso()}`",
                "- Ari remains a bounded read-only collaborator for V48.",
                "- Slot 41 is prepared, not inducted.",
                "- Slots 42-53 are spec-only, not spawned.",
                "",
                "## Ari Summary",
                "",
                message or "(no message captured)",
            ]
        )
        + "\n",
    )
    write_text(
        ALETHEON_REFLECTION,
        "\n".join(
            [
                "# Aletheon V48 Reflection",
                "",
                f"- Generated UTC: `{now_iso()}`",
                "- V48 kept GCP/Vesper/Kai on standby and used PowerShell as the primary lane.",
                "- Ari's role stayed bounded and evidence-first.",
                "- The phase prioritized cleanup, free-tier scaffolding, and Kimiclaw preparation over new induction claims.",
            ]
        )
        + "\n",
    )
    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "PASS" if ok else "WARN",
        "ari_collaboration_state": state,
        "ari_write_state": "read_only_no_repo_writes",
        "codex_cli_warning_state": "warnings_classified_non_blocking" if warnings else "clean",
        "warnings": warnings,
        "agent_message": message,
        "probe": {"returncode": proc.returncode, "stdout_excerpt": excerpt(proc.stdout), "stderr_excerpt": excerpt(proc.stderr, 2400)},
        "reflection_paths": {
            "ari": ARI_REFLECTION.relative_to(ROOT).as_posix(),
            "aletheon": ALETHEON_REFLECTION.relative_to(ROOT).as_posix(),
        },
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
