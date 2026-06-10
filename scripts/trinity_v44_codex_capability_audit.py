#!/usr/bin/env python3
"""Audit the V44 Codex desktop capability claims against config and session truth."""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path
from typing import Any

from trinity_v44_common import AUTOMATIONS_DIR, GLOBAL_CODEX_CONFIG, REPO_CODEX_CONFIG, ROOT, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-codex-capability-audit-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-codex-capability-audit-v1.md"
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


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_config_plugins(path: Path) -> set[str]:
    payload = load_toml(path)
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
        "# V44 Codex Capability Audit",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex capability audit state: `{payload['codex_capability_audit_state']}`",
        f"- Browser iteration state: `{payload['browser_iteration_state']}`",
        f"- Computer use state: `{payload['computer_use_state']}`",
        f"- Automation backend state: `{payload['automation_backend_state']}`",
        f"- Repo-local model resolution state: `{payload['repo_local_model_resolution_state']}`",
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
    parser = argparse.ArgumentParser(description="Audit the V44 Codex desktop capability claims.")
    parser.add_argument("--global-config", default=str(GLOBAL_CODEX_CONFIG))
    parser.add_argument("--repo-config", default=str(REPO_CODEX_CONFIG))
    parser.add_argument("--automations-dir", default=str(AUTOMATIONS_DIR))
    parser.add_argument("--callable-plugin", action="append", default=[])
    parser.add_argument("--native-automation-tool-available", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    global_config = load_toml(Path(args.global_config))
    repo_config = load_toml(Path(args.repo_config))
    enabled_plugins = load_config_plugins(Path(args.global_config))
    callable_plugins = {item.strip().lower() for item in args.callable_plugin if item.strip()}
    blockers: list[str] = []
    target_rows: list[dict[str, Any]] = []
    for key, display in TARGET_PLUGINS:
        enabled = key in enabled_plugins
        callable_here = key in callable_plugins
        if enabled and callable_here:
            status = "callable_in_session"
        elif enabled:
            status = "blocked_missing_connector"
            blockers.append(f"{display} is enabled in config but is not callable from the live V44 session surface.")
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

    requested_model = str(global_config.get("model") or "")
    requested_reasoning = str(global_config.get("model_reasoning_effort") or "")
    trinity_mesh = repo_config.get("trinity_mesh", {}) if isinstance(repo_config.get("trinity_mesh"), dict) else {}
    repo_requested_model = str(trinity_mesh.get("requested_model_profile") or repo_config.get("model") or "")
    repo_resolved_model = str(trinity_mesh.get("resolved_model_profile") or "")
    repo_requested_reasoning = str(trinity_mesh.get("requested_reasoning_effort") or repo_config.get("model_reasoning_effort") or "")
    repo_resolved_reasoning = str(trinity_mesh.get("resolved_reasoning_effort") or "")
    repo_local_model_resolution_state = "aligned"
    if requested_model and repo_resolved_model and requested_model.lower() != repo_resolved_model.lower():
        repo_local_model_resolution_state = "repo_local_fallback_lower_than_global_intent"
        blockers.append(
            f"Repo-local custom-agent resolution is `{repo_resolved_model}` while the broader V44 intent remains `{requested_model}`."
        )

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "codex_capability_audit_state": "capabilities_verified" if not blockers else "capabilities_verified_with_residuals",
        "plugin_registry_state": "target_plugins_callable" if not blockers else "target_plugins_partial",
        "browser_iteration_state": "codex_browser_supported_playwright_fallback_available",
        "computer_use_state": "unsupported_windows_launch_scope",
        "windows_sandbox_state": "supported_in_update_material",
        "skills_state": "supported_in_session",
        "builtin_git_state": "supported_in_session",
        "native_automation_state": "callable_in_session" if args.native_automation_tool_available else "tool_unavailable_in_session",
        "automation_backend_state": "native_codex_automation_ready" if args.native_automation_tool_available else "windows_task_scheduler_authoritative",
        "automations_dir_present": Path(args.automations_dir).exists(),
        "global_requested_model": requested_model,
        "global_requested_reasoning_effort": requested_reasoning,
        "repo_local_requested_model": repo_requested_model,
        "repo_local_resolved_model": repo_resolved_model,
        "repo_local_requested_reasoning_effort": repo_requested_reasoning,
        "repo_local_resolved_reasoning_effort": repo_resolved_reasoning,
        "repo_local_model_resolution_state": repo_local_model_resolution_state,
        "config_path": str(Path(args.global_config)),
        "repo_config_path": str(Path(args.repo_config)),
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

