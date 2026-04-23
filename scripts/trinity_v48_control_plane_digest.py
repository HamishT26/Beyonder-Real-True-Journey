#!/usr/bin/env python3
"""Create the V48 free-tier control-plane scaffold and capability matrix."""

from __future__ import annotations

import argparse
import shutil
import tomllib
from pathlib import Path
from typing import Any

from trinity_v48_common import GLOBAL_CODEX_CONFIG, ROOT, excerpt, git_head, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-control-plane-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v48-control-plane-digest-v1.md"
CIRCLECI_CONFIG = ROOT / ".circleci" / "config.yml"
MISSION_CONTROL_MD = ROOT / "docs" / "v48-notion-mission-control-pack-v1.md"
FREE_TIER_MD = ROOT / "docs" / "v48-free-tier-control-plane-v1.md"
TEMPLATE_README = ROOT / "templates" / "v48-control-plane" / "README.md"
NEON_SCHEMA = ROOT / "templates" / "v48-control-plane" / "neon_mission_control_schema.sql"
VERCEL_ENV = ROOT / "templates" / "v48-control-plane" / "vercel_env_example.env"

REQUESTED_PLUGINS = [
    "vercel",
    "neon-postgres",
    "circleci",
    "notion",
    "github",
    "google-drive",
    "figma",
    "linear",
    "gmail",
    "superpowers",
    "life-science-research",
    "expo",
    "render",
    "cloudflare",
    "build-web-apps",
    "test-android-apps",
    "hugging-face",
    "google-calendar",
]


def _config_plugins() -> list[str]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return []
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return []
    plugins = data.get("plugins") if isinstance(data.get("plugins"), dict) else {}
    return sorted(str(key).split("@", 1)[0] for key in plugins.keys())


def _mcp_names(raw: str) -> set[str]:
    known = {"MCP_DOCKER", "github", "google_drive", "playwright", "composio", "figma", "linear", "notion"}
    names: set[str] = set()
    for line in raw.splitlines():
        bits = line.strip().split()
        if bits and bits[0] in known:
            names.add(bits[0])
    return names


def _surface(plugin: str, enabled_plugins: set[str], mcp_names: set[str]) -> str:
    cli_aliases = {
        "github": "github",
        "google-drive": "google_drive",
        "notion": "notion",
        "figma": "figma",
        "linear": "linear",
    }
    if plugin in cli_aliases and cli_aliases[plugin] in mcp_names:
        return "already_callable_in_cli"
    if plugin in {"build-web-apps", "superpowers", "life-science-research", "test-android-apps"} and plugin in enabled_plugins:
        return "callable_in_app_only"
    if plugin in {"vercel", "neon-postgres", "circleci"}:
        return "requires_manual_auth_or_install"
    if plugin in enabled_plugins:
        return "blocked_missing_connector"
    return "requires_manual_auth_or_install"


def _write_circleci() -> None:
    content = """version: 2.1

jobs:
  trinity_quick:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install Python dependencies when present
          command: |
            python -m pip install --upgrade pip
            if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
      - run:
          name: Run V48 quick suite
          command: python scripts/run_all_trinity_systems.py --profile quick
      - store_artifacts:
          path: docs/v17-system-suite-run-report-latest.md
          destination: v48-quick-report.md
      - store_artifacts:
          path: docs/v17-system-suite-status-latest.json
          destination: v48-quick-status.json

  trinity_standard:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install Python dependencies when present
          command: |
            python -m pip install --upgrade pip
            if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
      - run:
          name: Run V48 standard suite
          command: python scripts/run_all_trinity_systems.py --profile standard
      - store_artifacts:
          path: docs/system-suite-run-report.md
          destination: v48-standard-report.md
      - store_artifacts:
          path: docs/system-suite-status.json
          destination: v48-standard-status.json

workflows:
  v48_quick_standard:
    jobs:
      - trinity_quick
      - trinity_standard:
          requires:
            - trinity_quick
"""
    write_text(CIRCLECI_CONFIG, content)


def _write_templates() -> None:
    write_text(
        FREE_TIER_MD,
        """# V48 Free-Tier Control Plane

- Vercel state: scaffolded only until account/connector callability is proven.
- Neon state: scaffolded only until account/connector callability is proven.
- CircleCI state: quick and standard config scaffolded; live validation is blocked until CircleCI CLI or connector is callable.
- Notion Mission Control state: repo-side pack created; live page/database creation is not attempted in V48.

Official anchors:
- Vercel pricing: https://vercel.com/pricing
- Vercel Hobby plan: https://vercel.com/docs/accounts/plans/hobby
- Vercel Sandbox pricing and limits: https://vercel.com/docs/vercel-sandbox/pricing
- Neon pricing: https://neon.com/pricing
""",
    )
    write_text(
        MISSION_CONTROL_MD,
        """# V48 Notion Mission Control Pack

This is the repo-side Mission Control scaffold. It is not a live Notion database.

Recommended fields for a future live Notion database:
- Name
- Phase
- Lane
- Status
- Owner
- Runtime Surface
- Proof Path
- Blocker
- Next Action

Initial lanes:
- V48 cleanup
- V48 free-tier control plane
- V48 CircleCI quick-standard
- V48 Kimiclaw slot-41 prep
- V48 swarm 42-53 spec-only
- V48 suite ladder
""",
    )
    write_text(
        TEMPLATE_README,
        """# V48 Control Plane Templates

These templates are non-secret scaffolds for future Vercel and Neon free-tier proofs.
Do not add API keys, tokens, database URLs, or production secrets here.
""",
    )
    write_text(
        NEON_SCHEMA,
        """-- V48 non-production Neon mission-control scaffold.
-- Apply only after Neon account/project callability is proven.

create table if not exists mission_events (
  id bigserial primary key,
  phase text not null,
  lane text not null,
  status text not null,
  proof_path text,
  blocker text,
  created_at timestamptz not null default now()
);

create table if not exists swarm_slots (
  slot_number integer primary key,
  label text not null,
  continuity_state text not null,
  runtime_surface text,
  proof_gate text,
  created_at timestamptz not null default now()
);
""",
    )
    write_text(
        VERCEL_ENV,
        """# V48 Vercel scaffold placeholders only.
# Do not store real secrets in this file.

V48_PHASE=v48_omega
V48_CONTROL_PLANE_MODE=repo_scaffold_only
V48_NEON_DATABASE_URL=replace_after_neon_proof
""",
    )


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V48 Control Plane Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Control plane state: `{payload['control_plane_state']}`",
        f"- Vercel state: `{payload['vercel_free_tier_state']}`",
        f"- Neon state: `{payload['neon_free_tier_state']}`",
        f"- CircleCI state: `{payload['circleci_state']}`",
        f"- Notion state: `{payload['notion_mission_control_state']}`",
        "",
        "## Plugin Matrix",
        "",
    ]
    lines.extend(f"- `{row['plugin']}`: `{row['surface_state']}`" for row in payload["plugin_matrix"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create V48 control-plane scaffold.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    _write_circleci()
    _write_templates()
    mcp_proc = safe_run(["codex", "mcp", "list"], timeout=120)
    mcp_names = _mcp_names(mcp_proc.stdout)
    enabled_plugins = set(_config_plugins())
    plugin_matrix = []
    for plugin in REQUESTED_PLUGINS:
        plugin_matrix.append(
            {
                "plugin": plugin,
                "enabled_in_config": plugin in enabled_plugins,
                "surface_state": _surface(plugin, enabled_plugins, mcp_names),
            }
        )
    cli_states = {
        "vercel": shutil.which("vercel") or "",
        "neonctl": shutil.which("neonctl") or "",
        "circleci": shutil.which("circleci") or "",
    }
    vercel_state = "scaffold_created_cli_not_on_path_connector_not_callable_from_session" if not cli_states["vercel"] else "cli_present_read_only_probe_pending"
    neon_state = "scaffold_created_cli_not_on_path_connector_not_callable_from_session" if not cli_states["neonctl"] else "cli_present_read_only_probe_pending"
    circleci_state = "quick_standard_scaffold_created_cli_not_on_path" if not cli_states["circleci"] else "quick_standard_scaffold_created_cli_present_validation_pending"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "WARN",
        "current_head_sha": git_head(),
        "control_plane_state": "repo_scaffold_created_live_connectors_gated",
        "vercel_free_tier_state": vercel_state,
        "neon_free_tier_state": neon_state,
        "circleci_state": circleci_state,
        "notion_mission_control_state": "repo_scaffold_created_live_write_not_attempted",
        "plugin_surface_split_state": "app_plugins_and_cli_mcp_are_distinct_surfaces",
        "codex_cli_extension_state": "no_automatic_app_plugin_inheritance_proven",
        "cli_presence": cli_states,
        "plugin_matrix": plugin_matrix,
        "generated_files": [
            CIRCLECI_CONFIG.relative_to(ROOT).as_posix(),
            FREE_TIER_MD.relative_to(ROOT).as_posix(),
            MISSION_CONTROL_MD.relative_to(ROOT).as_posix(),
            TEMPLATE_README.relative_to(ROOT).as_posix(),
            NEON_SCHEMA.relative_to(ROOT).as_posix(),
            VERCEL_ENV.relative_to(ROOT).as_posix(),
        ],
        "official_source_anchors": [
            {"name": "Vercel pricing", "url": "https://vercel.com/pricing"},
            {"name": "Vercel Hobby plan", "url": "https://vercel.com/docs/accounts/plans/hobby"},
            {"name": "Vercel Sandbox pricing and limits", "url": "https://vercel.com/docs/vercel-sandbox/pricing"},
            {"name": "Neon pricing", "url": "https://neon.com/pricing"},
        ],
        "mcp_probe": {"returncode": mcp_proc.returncode, "stdout_excerpt": excerpt(mcp_proc.stdout), "stderr_excerpt": excerpt(mcp_proc.stderr, 1600)},
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
