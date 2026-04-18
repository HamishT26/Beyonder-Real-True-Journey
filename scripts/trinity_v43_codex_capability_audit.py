#!/usr/bin/env python3
"""Audit the V43 Codex desktop capability claims against config and session truth."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

from trinity_v43_common import ROOT, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-codex-capability-audit-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-codex-capability-audit-v1.md"
DEFAULT_CONFIG = Path(r"C:\Users\hamis\.codex\config.toml")
DEFAULT_AUTOMATIONS_DIR = Path(r"C:\Users\hamis\.codex\automations")
TARGET_PLUGINS = [
    ("github", "GitHub"),
    ("google-drive", "Google Drive"),
    ("notion", "Notion"),
    ("gmail", "Gmail"),
    ("figma", "Figma"),
    ("render", "Render"),
    ("expo", "Expo"),
    ("vercel", "Vercel"),
    ("circleci", "CircleCI"),
    ("neon-postgres", "Neon Postgres"),
    ("superpowers", "Superpowers"),
]


def load_config_plugins(path: Path) -> set[str]:
    if not path.exists():
        return set()
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("plugins", {})
    if not isinstance(rows, dict):
        return set()
    enabled: set[str] = set()
    for key, value in rows.items():
        if isinstance(value, dict) and value.get("enabled") is True:
            plugin_key = str(key).strip().lower()
            enabled.add(plugin_key)
            enabled.add(plugin_key.split("@", 1)[0])
    return enabled


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 Codex Capability Audit",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex capability audit state: `{payload['codex_capability_audit_state']}`",
        f"- Browser iteration state: `{payload['browser_iteration_state']}`",
        f"- Computer use state: `{payload['computer_use_state']}`",
        f"- Automation backend state: `{payload['automation_backend_state']}`",
        "",
        "## Target Plugins",
        "",
    ]
    for row in payload.get("target_plugins", []):
        lines.append(
            f"- `{row['display_name']}`: config=`{row['enabled_in_config']}`, callable=`{row['callable_in_session']}`, status=`{row['status']}`"
        )
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the V43 Codex desktop capability claims.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--automations-dir", default=str(DEFAULT_AUTOMATIONS_DIR))
    parser.add_argument("--callable-plugin", action="append", default=[])
    parser.add_argument("--native-automation-tool-available", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    enabled_plugins = load_config_plugins(Path(args.config))
    callable_plugins = {item.strip().lower() for item in args.callable_plugin if item.strip()}
    target_rows: list[dict[str, Any]] = []
    blockers: list[str] = []
    for key, display in TARGET_PLUGINS:
        enabled = key in enabled_plugins
        callable_here = key in callable_plugins
        if enabled and callable_here:
            status = "callable_in_session"
        elif enabled:
            status = "blocked_missing_connector"
            blockers.append(f"{display} is enabled in config but was not promoted into the live session tool surface.")
        else:
            status = "deferred_unsupported_here"
        target_rows.append(
            {
                "plugin_key": key,
                "display_name": display,
                "enabled_in_config": enabled,
                "callable_in_session": callable_here,
                "status": status,
            }
        )

    automations_dir = Path(args.automations_dir)
    native_automation_state = "callable_in_session" if args.native_automation_tool_available else "tool_unavailable_in_session"
    automation_backend_state = "native_codex_automation_ready" if args.native_automation_tool_available else "windows_task_scheduler_authoritative"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "codex_capability_audit_state": "capabilities_verified" if not blockers else "capabilities_verified_with_residuals",
        "plugin_registry_state": "target_plugins_callable" if not blockers else "target_plugins_partial",
        "browser_iteration_state": "update_claim_present_web_tool_and_playwright_fallback_only",
        "computer_use_state": "unsupported_windows_launch_scope",
        "windows_sandbox_state": "claimed_supported_in_update_material",
        "skills_state": "supported_in_session",
        "builtin_git_state": "supported_in_session",
        "native_automation_state": native_automation_state,
        "automation_backend_state": automation_backend_state,
        "automations_dir_present": automations_dir.exists(),
        "config_path": str(Path(args.config)),
        "enabled_plugins_in_config": sorted(enabled_plugins),
        "callable_plugins_in_session": sorted(callable_plugins),
        "target_plugins": target_rows,
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
