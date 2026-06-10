#!/usr/bin/env python3
"""Capture the V45 PowerShell-first operator surface truth and app/CLI split."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

from trinity_v45_common import (
    ARTIFACT_ARCHIVE_ROOT,
    AUTHORITATIVE_REPO,
    AUTOMATIONS_DIR,
    DEFAULT_DOWNLOAD_SOURCE_DIR,
    DOWNLOAD_ARCHIVE_ROOT,
    EXECUTION_BRANCH,
    GLOBAL_CODEX_CONFIG,
    NON_AUTHORITATIVE_WORKBENCH,
    ROOT,
    SOURCE_BRANCH,
    STALE_LOCAL_MAIN_WORKTREE,
    UBUNTU_EXE_PATH,
    V45_ARTIFACT_ROOT,
    V45_DOWNLOAD_ROOT,
    WORKTREE_ARCHIVE_ROOT,
    WORKTREE_BASELINE_SHA,
    WORKTREE_BASELINE_STATE,
    WSL_EXE_PATH,
    git_branch,
    git_head,
    now_iso,
    safe_run,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-operator-surface-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v45-operator-surface-probe-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "v45-powershell-operator-note-v1.md"
DEFAULT_APP_SURFACES = [
    "web",
    "github_plugin",
    "google_drive_plugin",
    "notion_plugin",
    "gmail_plugin",
    "figma_plugin",
    "render_plugin",
    "expo_plugin",
    "vercel_plugin",
    "circleci_plugin",
    "neon_postgres_plugin",
    "superpowers_plugin",
    "skills",
    "built_in_git",
]


def _stdout_json(command: list[str]) -> tuple[dict[str, Any], Any]:
    proc = safe_run(command, timeout=180)
    text = str(proc.stdout or "").strip()
    parsed: Any = {}
    if text:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {}
    return (
        {
            "returncode": proc.returncode,
            "stdout_excerpt": proc.stdout[-4000:],
            "stderr_excerpt": proc.stderr[-2000:],
        },
        parsed,
    )


def _codex_mcp_summary(raw_output: str) -> dict[str, list[str]]:
    local_stdio: list[str] = []
    remote_url: list[str] = []
    mode = "local"
    for raw_line in str(raw_output or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Name") and "Url" in line:
            mode = "remote"
            continue
        if line.startswith("Name") or line.startswith("-"):
            continue
        parts = line.split()
        if not parts:
            continue
        name = parts[0]
        if name in {"MCP_DOCKER", "github", "google_drive", "playwright", "composio", "figma", "linear", "notion"}:
            if mode == "remote":
                remote_url.append(name)
            else:
                local_stdio.append(name)
    return {
        "cli_mcp_local_stdio": sorted(set(local_stdio)),
        "cli_mcp_remote_url": sorted(set(remote_url)),
    }


def _config_registry() -> dict[str, Any]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return {"config_exists": False, "mcp_servers": []}
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive
        return {"config_exists": True, "config_parse_error": str(exc), "mcp_servers": []}
    mcp_servers = sorted((data.get("mcp_servers") or {}).keys()) if isinstance(data.get("mcp_servers"), dict) else []
    return {
        "config_exists": True,
        "mcp_servers": mcp_servers,
    }


def _task_inventory() -> dict[str, list[dict[str, str]]]:
    query = (
        "Get-ScheduledTask | "
        "Where-Object { $_.TaskName -like 'Codex V42*' -or $_.TaskName -like 'Codex V43*' -or $_.TaskName -like 'Codex V44*' } | "
        "Select-Object TaskName,State | ConvertTo-Json -Depth 3"
    )
    probe, parsed = _stdout_json(["powershell.exe", "-NoProfile", "-Command", query])
    rows = parsed if isinstance(parsed, list) else ([parsed] if isinstance(parsed, dict) and parsed else [])
    inventory = {"v42": [], "v43": [], "v44": []}
    for row in rows:
        task_name = str(row.get("TaskName") or "")
        state = str(row.get("State") or "")
        entry = {"task_name": task_name, "state": state}
        if "V42" in task_name:
            inventory["v42"].append(entry)
        elif "V43" in task_name:
            inventory["v43"].append(entry)
        elif "V44" in task_name:
            inventory["v44"].append(entry)
    inventory["probe"] = probe  # type: ignore[assignment]
    return inventory


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Operator Surface Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Operator shell preference: `{payload['operator_shell_preference']}`",
        f"- WSL execution mode: `{payload['wsl_execution_mode']}`",
        f"- Worktree baseline state: `{payload['worktree_baseline_state']}`",
        f"- Drive download policy state: `{payload['drive_download_policy_state']}`",
        f"- Plugin surface split state: `{payload['plugin_surface_split_state']}`",
        "",
        "## Paths",
        "",
        f"- authoritative_repo: `{payload['authoritative_repo']}`",
        f"- execution_worktree: `{payload['execution_worktree']}`",
        f"- stale_local_main_worktree: `{payload['stale_local_main_worktree']}`",
        f"- v45_download_root: `{payload['v45_download_root']}`",
        f"- v45_artifact_root: `{payload['v45_artifact_root']}`",
        "",
        "## CLI MCP vs App Session",
        "",
        f"- app_session_surfaces: `{', '.join(payload['app_session_surfaces'])}`",
        f"- config_enabled_mcp_servers: `{', '.join(payload['config_enabled_mcp_servers'])}`",
        f"- cli_mcp_local_stdio: `{', '.join(payload['cli_mcp_local_stdio'])}`",
        f"- cli_mcp_remote_url: `{', '.join(payload['cli_mcp_remote_url'])}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def operator_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V45 PowerShell Operator Note",
            "",
            "- Stay in PowerShell for the active Codex app lane. Keep WSL installed and callable, but do not switch the app execution lane there while the selector issue remains on hold.",
            f"- Use `{payload['v45_download_root']}` for bulky manual downloads tied to v45 and `{payload['v45_artifact_root']}` for bulky generated artifacts.",
            "- Use the clean D: worktree for execution and publication. Treat the dirty C: checkout as authoritative history, not as the active mutation lane.",
            "- Treat `codex mcp list` as the CLI truth and the current app plugin set as the app truth. Do not assume the CLI inherits every app plugin.",
            "- Proven command anchors:",
            "  - `codex --version`",
            "  - `codex login status`",
            "  - `codex mcp list`",
            "  - `codex features list`",
            "  - `wsl.exe --status`",
            "  - `gcloud auth list`",
            "  - `gcloud config list`",
        ]
    ).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture the V45 PowerShell-first operator surface truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--operator-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()

    ps_probe, ps_parsed = _stdout_json(["powershell.exe", "-NoProfile", "-Command", "$PSVersionTable | ConvertTo-Json -Depth 4"])
    wsl_status = safe_run(["wsl.exe", "--status"], timeout=120)
    wsl_list = safe_run(["wsl.exe", "-l", "-v"], timeout=120)
    codex_features = safe_run(["codex", "features", "list"], timeout=120)
    codex_mcp = safe_run(["codex", "mcp", "list"], timeout=120)
    config_registry = _config_registry()
    task_inventory = _task_inventory()
    cli_split = _codex_mcp_summary(codex_mcp.stdout)

    archive_roots = {
        "downloads": DOWNLOAD_ARCHIVE_ROOT.exists(),
        "artifacts": ARTIFACT_ARCHIVE_ROOT.exists(),
        "worktrees": WORKTREE_ARCHIVE_ROOT.exists(),
        "v45_download_root": V45_DOWNLOAD_ROOT.exists(),
        "v45_artifact_root": V45_ARTIFACT_ROOT.exists(),
    }

    blockers: list[str] = []
    if ps_probe["returncode"] != 0:
        blockers.append("PowerShell version probe failed.")
    if not WSL_EXE_PATH.exists():
        blockers.append("wsl.exe is missing from the expected system path.")
    if wsl_status.returncode != 0 or wsl_list.returncode != 0:
        blockers.append("WSL launch probes did not complete cleanly.")
    if not archive_roots["downloads"] or not archive_roots["artifacts"] or not archive_roots["worktrees"]:
        blockers.append("One or more D-drive archive roots are missing.")
    if not archive_roots["v45_download_root"] or not archive_roots["v45_artifact_root"]:
        blockers.append("The explicit V45 D-drive archive targets are missing.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v45_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "v45_execution_lead": "Aletheon",
        "operator_shell_preference": "windows_powershell_primary",
        "powershell_hygiene_state": "powershell_ready" if ps_probe["returncode"] == 0 else "powershell_probe_failed",
        "powershell_edition": str(ps_parsed.get("PSEdition") or ""),
        "powershell_version": str((ps_parsed.get("PSVersion") or {}).get("Major") or "") + "." + str((ps_parsed.get("PSVersion") or {}).get("Minor") or ""),
        "wsl_execution_mode": "installed_on_hold_for_agent_switching",
        "wsl_launcher_state": "launchable" if wsl_status.returncode == 0 else "probe_failed",
        "ubuntu_distribution_state": "installed_registered" if "Ubuntu" in wsl_list.stdout else "not_observed",
        "worktree_baseline_state": WORKTREE_BASELINE_STATE,
        "worktree_baseline_sha": WORKTREE_BASELINE_SHA,
        "source_branch": SOURCE_BRANCH,
        "execution_branch": git_branch() or EXECUTION_BRANCH,
        "current_head_sha": git_head(),
        "authoritative_repo": str(AUTHORITATIVE_REPO),
        "execution_worktree": str(ROOT),
        "stale_local_main_worktree": str(STALE_LOCAL_MAIN_WORKTREE),
        "stale_local_main_worktree_state": "non_execution_history_until_manual_reconciliation",
        "non_authoritative_workbench": str(NON_AUTHORITATIVE_WORKBENCH),
        "default_download_source_dir": str(DEFAULT_DOWNLOAD_SOURCE_DIR),
        "download_archive_root": str(DOWNLOAD_ARCHIVE_ROOT),
        "artifact_archive_root": str(ARTIFACT_ARCHIVE_ROOT),
        "v45_download_root": str(V45_DOWNLOAD_ROOT),
        "v45_artifact_root": str(V45_ARTIFACT_ROOT),
        "drive_download_policy_state": "explicit_v45_d_targets_ready" if archive_roots["v45_download_root"] and archive_roots["v45_artifact_root"] else "v45_d_targets_missing",
        "archive_root_presence": archive_roots,
        "wsl_paths": {
            "wsl_exe": str(WSL_EXE_PATH),
            "ubuntu_exe": str(UBUNTU_EXE_PATH),
            "wsl_exe_present": WSL_EXE_PATH.exists(),
            "ubuntu_exe_present": UBUNTU_EXE_PATH.exists(),
        },
        "global_codex_config_present": GLOBAL_CODEX_CONFIG.exists(),
        "automations_dir_present": AUTOMATIONS_DIR.exists(),
        "config_enabled_mcp_servers": config_registry.get("mcp_servers", []),
        "app_session_surfaces": list(DEFAULT_APP_SURFACES),
        "cli_mcp_local_stdio": cli_split["cli_mcp_local_stdio"],
        "cli_mcp_remote_url": cli_split["cli_mcp_remote_url"],
        "plugin_surface_split_state": "explicit_app_cli_split_recorded",
        "scheduled_task_inventory": {
            "v42": task_inventory["v42"],
            "v43": task_inventory["v43"],
            "v44": task_inventory["v44"],
        },
        "powershell_probe": ps_probe,
        "wsl_status_probe": {
            "returncode": wsl_status.returncode,
            "stdout_excerpt": wsl_status.stdout[-2400:],
            "stderr_excerpt": wsl_status.stderr[-1200:],
        },
        "wsl_list_probe": {
            "returncode": wsl_list.returncode,
            "stdout_excerpt": wsl_list.stdout[-2400:],
            "stderr_excerpt": wsl_list.stderr[-1200:],
        },
        "task_inventory_probe": task_inventory.get("probe", {}),
        "codex_features_probe": {
            "returncode": codex_features.returncode,
            "stdout_excerpt": codex_features.stdout[-4000:],
            "stderr_excerpt": codex_features.stderr[-1600:],
        },
        "codex_mcp_probe": {
            "returncode": codex_mcp.returncode,
            "stdout_excerpt": codex_mcp.stdout[-4000:],
            "stderr_excerpt": codex_mcp.stderr[-1600:],
        },
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.operator_note), operator_note(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
