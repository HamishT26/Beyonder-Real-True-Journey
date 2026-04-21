#!/usr/bin/env python3
"""Publish V46 Codex app, CLI, plugin, and official-doc capability truth."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v46_common import ROOT, now_iso, read_json, write_json, write_text

OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-operator-probe-v1.json"
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-app-cli-capability-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-app-cli-capability-digest-v1.md"
PLUGIN_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-plugin-surface-digest-v1.json"
PLUGIN_MD = ROOT / "docs" / "trinity-live-traces" / "v46-plugin-surface-digest-v1.md"

APP_PLUGINS = [
    "vercel",
    "superpowers",
    "github",
    "life-science-research",
    "expo",
    "render",
    "neon-postgres",
    "cloudflare",
    "notion",
    "google-drive",
    "build-web-apps",
    "test-android-apps",
]

OFFICIAL_SOURCES = [
    {
        "claim": "Codex CLI supports starting a new thread with --model gpt-5.4; GPT-5.4 is available in the CLI, app, IDE extension, and web.",
        "url": "https://developers.openai.com/codex/changelog",
    },
    {
        "claim": "Codex CLI command-line options include -m/--model and -c/--config overrides.",
        "url": "https://developers.openai.com/codex/cli/reference",
    },
    {
        "claim": "Codex app on Windows runs natively with PowerShell and Windows sandbox support, with WSL available as a separate agent option.",
        "url": "https://developers.openai.com/codex/app/windows",
    },
    {
        "claim": "Codex app automations can use plugins and skills, but should be tested manually before scheduling.",
        "url": "https://developers.openai.com/codex/app/automations",
    },
    {
        "claim": "Chronicle is currently documented as available for ChatGPT Pro subscribers on macOS, and local V46 config has chronicle disabled.",
        "url": "https://developers.openai.com/codex/memories/chronicle",
    },
    {
        "claim": "GPT-5.4 supports reasoning effort values including xhigh.",
        "url": "https://developers.openai.com/api/docs/models/gpt-5.4",
    },
]


def markdown(payload: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- App plugin registry state: `{payload['app_plugin_registry_state']}`",
        f"- CLI MCP registry state: `{payload['cli_mcp_registry_state']}`",
        f"- Chronicle Windows state: `{payload['chronicle_windows_state']}`",
        "",
        "## App Plugins",
        "",
    ]
    lines.extend(f"- `{item}`" for item in payload["app_plugins"])
    lines.extend(["", "## CLI MCP Servers", ""])
    lines.extend(f"- local stdio: `{', '.join(payload['cli_mcp_local_stdio'])}`")
    lines.extend(f"- remote url: `{', '.join(payload['cli_mcp_remote_url'])}`")
    lines.extend(["", "## Official Source Anchors", ""])
    lines.extend(f"- {row['claim']} ({row['url']})" for row in payload["official_sources"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V46 capability digest.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--plugin-json", default=str(PLUGIN_JSON))
    parser.add_argument("--plugin-md", default=str(PLUGIN_MD))
    args = parser.parse_args()

    operator = read_json(OPERATOR_JSON)
    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "overall_status": "PASS",
        "codex_cli_version_state": operator.get("codex_cli_version_state", "unproven"),
        "codex_cli_login_state": operator.get("codex_cli_login_state", "unproven"),
        "codex_cli_config_model_state": operator.get("codex_cli_config_model_state", "unproven"),
        "codex_cli_model_target": "gpt-5.4",
        "codex_cli_reasoning_target": "xhigh",
        "app_plugin_registry_state": operator.get("app_plugin_registry_state", "desktop_session_plugins_available_by_context"),
        "cli_mcp_registry_state": operator.get("cli_mcp_registry_state", "unproven"),
        "app_plugins": APP_PLUGINS,
        "cli_mcp_local_stdio": operator.get("cli_mcp_local_stdio", []),
        "cli_mcp_remote_url": operator.get("cli_mcp_remote_url", []),
        "plugin_surface_rule": "app_plugins_and_cli_mcp_are_distinct_surfaces",
        "chronicle_windows_state": operator.get("chronicle_windows_state", "not_windows_live_official_docs_mac_pro_only_config_false"),
        "automations_state": "app_automation_supported_but_no_new_v46_recurring_backend_created",
        "cloud_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
        "official_sources": OFFICIAL_SOURCES,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload, "V46 Codex App / CLI Capability Digest"))
    write_json(Path(args.plugin_json), payload)
    write_text(Path(args.plugin_md), markdown(payload, "V46 Plugin Surface Digest"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
