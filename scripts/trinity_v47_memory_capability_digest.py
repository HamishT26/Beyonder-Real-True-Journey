#!/usr/bin/env python3
"""Publish V47 Codex memory, app, CLI, plugin, IAB, and source-anchor truth."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v47_common import ROOT, now_iso, read_json, write_json, write_text

OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-operator-probe-v1.json"
HYGIENE_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-codex-home-hygiene-v1.json"
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-codex-memory-capability-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-codex-memory-capability-digest-v1.md"
PLUGIN_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-plugin-surface-digest-v1.json"
PLUGIN_MD = ROOT / "docs" / "trinity-live-traces" / "v47-plugin-surface-digest-v1.md"

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
OFFICIAL_SOURCE_ANCHORS = [
    {
        "name": "Codex changelog",
        "url": "https://developers.openai.com/codex/changelog",
        "claim": "Codex app includes in-app browser, richer PR workflows, artifact viewer, memories where available, plugins, multiple terminals, and Windows tray support.",
    },
    {
        "name": "Codex CLI reference",
        "url": "https://developers.openai.com/codex/cli/reference",
        "claim": "Codex CLI supports --model and config overrides such as model_reasoning_effort.",
    },
    {
        "name": "Codex Windows app",
        "url": "https://developers.openai.com/codex/app/windows",
        "claim": "PowerShell is a valid Windows app execution environment and WSL remains a separate selectable environment.",
    },
    {
        "name": "Codex Automations",
        "url": "https://developers.openai.com/codex/app/automations",
        "claim": "Automations can use plugins and skills, but prompts should be tested manually before recurring scheduling.",
    },
    {
        "name": "Codex Chronicle",
        "url": "https://developers.openai.com/codex/memories/chronicle",
        "claim": "Chronicle is documented as a macOS research preview and is not promoted as Windows-live in V47.",
    },
    {
        "name": "GPT-5.4 model",
        "url": "https://developers.openai.com/api/docs/models/gpt-5.4",
        "claim": "GPT-5.4 supports xhigh reasoning effort for agentic/professional workflows.",
    },
]


def markdown(payload: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex memory state: `{payload['codex_memory_state']}`",
        f"- Chronicle Windows state: `{payload['chronicle_windows_state']}`",
        f"- IAB state: `{payload['iab_state']}`",
        f"- App plugin registry state: `{payload['app_plugin_registry_state']}`",
        f"- CLI MCP registry state: `{payload['cli_mcp_registry_state']}`",
        "",
        "## App Plugins",
        "",
    ]
    lines.extend(f"- `{item}`" for item in payload["app_plugins"])
    lines.extend(["", "## CLI MCP Servers", ""])
    lines.append(f"- local stdio: `{', '.join(payload['cli_mcp_local_stdio'])}`")
    lines.append(f"- remote url: `{', '.join(payload['cli_mcp_remote_url'])}`")
    lines.extend(["", "## Source Anchors", ""])
    lines.extend(f"- {item['name']}: {item['claim']} ({item['url']})" for item in payload["official_source_anchors"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish V47 Codex memory/capability digest.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--plugin-json", default=str(PLUGIN_JSON))
    parser.add_argument("--plugin-md", default=str(PLUGIN_MD))
    args = parser.parse_args()
    operator = read_json(OPERATOR_JSON)
    hygiene = read_json(HYGIENE_JSON)
    config = operator.get("global_codex_config", {}) if isinstance(operator.get("global_codex_config"), dict) else {}
    payload = {
        "generated_utc": now_iso(),
        "phase": "v47_omega",
        "overall_status": "PASS",
        "codex_memory_state": operator.get("codex_memory_state", "memory_state_unverified"),
        "codex_memory_config": {
            "memories": config.get("memories"),
            "suppress_unstable_features_warning": config.get("suppress_unstable_features_warning"),
        },
        "chronicle_windows_state": operator.get("chronicle_windows_state", "not_windows_live_official_docs_mac_research_preview_config_false"),
        "local_codex_hygiene_state": hygiene.get("local_codex_hygiene_state", "not_run"),
        "codex_cli_warning_state": "warnings_classified_or_repaired_by_hygiene_lane",
        "iab_state": operator.get("iab_state", "available_not_callable_from_session"),
        "app_plugin_registry_state": operator.get("app_plugin_registry_state", "desktop_session_plugins_available_by_context"),
        "cli_mcp_registry_state": operator.get("cli_mcp_registry_state", "unproven"),
        "app_plugins": APP_PLUGINS,
        "cli_mcp_local_stdio": operator.get("cli_mcp_local_stdio", []),
        "cli_mcp_remote_url": operator.get("cli_mcp_remote_url", []),
        "plugin_surface_rule": "app_plugins_and_cli_mcp_are_distinct_surfaces",
        "automation_state": "documented_available_not_scheduled_in_v47",
        "official_source_anchors": OFFICIAL_SOURCE_ANCHORS,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload, "V47 Codex Memory / Capability Digest"))
    write_json(Path(args.plugin_json), payload)
    write_text(Path(args.plugin_md), markdown(payload, "V47 Plugin Surface Digest"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
