#!/usr/bin/env python3
"""Capture V47 PowerShell, app, CLI, IAB, and standby truth."""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path
from typing import Any

from trinity_v47_common import (
    ARTIFACT_ARCHIVE_ROOT,
    AUTHORITATIVE_REPO,
    AUTOMATIONS_DIR,
    DOWNLOAD_ARCHIVE_ROOT,
    GLOBAL_CODEX_CONFIG,
    NON_AUTHORITATIVE_WORKBENCH,
    ROOT,
    UBUNTU_EXE_PATH,
    V47_ARTIFACT_ROOT,
    V47_DOWNLOAD_ROOT,
    WORKTREE_ARCHIVE_ROOT,
    WORKTREE_BASELINE_SHA,
    WORKTREE_BASELINE_STATE,
    WSL_EXE_PATH,
    excerpt,
    git_branch,
    git_head,
    now_iso,
    safe_run,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-operator-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-operator-probe-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "v47-powershell-operator-note-v1.md"


def _config() -> dict[str, Any]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return {"exists": False, "mcp_servers": []}
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"exists": True, "error": str(exc), "mcp_servers": []}
    mcp = data.get("mcp_servers") if isinstance(data.get("mcp_servers"), dict) else {}
    return {
        "exists": True,
        "model": str(data.get("model") or ""),
        "model_reasoning_effort": str(data.get("model_reasoning_effort") or ""),
        "approval_policy": str(data.get("approval_policy") or ""),
        "sandbox_mode": str(data.get("sandbox_mode") or ""),
        "memories": bool(data.get("memories")) if isinstance(data.get("memories"), bool) else True,
        "chronicle": bool(data.get("chronicle")) if "chronicle" in data else False,
        "suppress_unstable_features_warning": bool(data.get("suppress_unstable_features_warning")) if "suppress_unstable_features_warning" in data else False,
        "mcp_servers": sorted(mcp.keys()),
    }


def _probe(command: list[str], timeout: int = 180) -> dict[str, Any]:
    proc = safe_run(command, timeout=timeout)
    return {"returncode": proc.returncode, "stdout_excerpt": excerpt(proc.stdout), "stderr_excerpt": excerpt(proc.stderr, 2400)}


def _mcp_summary(raw: str) -> dict[str, list[str]]:
    local_stdio: list[str] = []
    remote_url: list[str] = []
    remote = False
    known = {"MCP_DOCKER", "github", "google_drive", "playwright", "composio", "figma", "linear", "notion"}
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Name") and "Url" in line:
            remote = True
            continue
        if line.startswith("Name"):
            continue
        name = line.split()[0]
        if name in known:
            (remote_url if remote else local_stdio).append(name)
    return {"cli_mcp_local_stdio": sorted(set(local_stdio)), "cli_mcp_remote_url": sorted(set(remote_url))}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V47 Operator Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Worktree baseline state: `{payload['worktree_baseline_state']}`",
        f"- PowerShell state: `{payload['powershell_hygiene_state']}`",
        f"- Admin shell state: `{payload['admin_shell_state']}`",
        f"- IAB state: `{payload['iab_state']}`",
        f"- Cloud standby state: `{payload['cloud_standby_state']}`",
        f"- Bigtable state: `{payload['bigtable_state']}`",
        f"- CLI MCP registry state: `{payload['cli_mcp_registry_state']}`",
    ]
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {item}" for item in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V47 PowerShell Operator Note",
            "",
            "- PowerShell remains the V47 operator lane. Admin mode is recorded, but destructive admin cleanup is still out of scope.",
            "- WSL remains installed/on-hold for agent switching.",
            "- GCP, Vertex AI, Bigtable, Agent Engine, Gemini CLI, Kai, and Vesper live probes stay on standby until billing/auth/project truth is restored.",
            f"- Use `{payload['v47_download_root']}` for bulky downloads and `{payload['v47_artifact_root']}` for generated artifacts.",
            "- Treat app plugins, CLI MCP servers, and in-app browser as separate surfaces. Publish actual callability, not aspiration.",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture V47 operator truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--operator-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()
    V47_DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    V47_ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

    config = _config()
    ps = _probe(["powershell.exe", "-NoProfile", "-Command", "$PSVersionTable | ConvertTo-Json -Depth 4"])
    admin = _probe(["powershell.exe", "-NoProfile", "-Command", "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)"])
    wsl_status = _probe(["wsl.exe", "--status"], timeout=120)
    wsl_list = _probe(["wsl.exe", "-l", "-v"], timeout=120)
    version = _probe(["codex", "--version"], timeout=120)
    login = _probe(["codex", "login", "status"], timeout=120)
    features_proc = safe_run(["codex", "features", "list"], timeout=120)
    mcp_proc = safe_run(["codex", "mcp", "list"], timeout=120)
    mcp = _mcp_summary(mcp_proc.stdout)
    login_text = f"{login['stdout_excerpt']}\n{login['stderr_excerpt']}"

    blockers: list[str] = []
    if git_head() != WORKTREE_BASELINE_SHA:
        blockers.append("V47 worktree baseline SHA mismatch.")
    if ps["returncode"] != 0:
        blockers.append("PowerShell probe failed.")
    if version["returncode"] != 0 or login["returncode"] != 0:
        blockers.append("Codex CLI version/login probe failed.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v47_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "v47_execution_lead": "Aletheon",
        "worktree_baseline_state": WORKTREE_BASELINE_STATE,
        "worktree_baseline_sha": WORKTREE_BASELINE_SHA,
        "current_head_sha": git_head(),
        "execution_branch": git_branch(),
        "operator_shell_preference": "windows_powershell_primary",
        "powershell_hygiene_state": "powershell_ready" if ps["returncode"] == 0 else "powershell_probe_failed",
        "admin_shell_state": "administrator_observed" if admin["stdout_excerpt"].strip().lower() == "true" else "not_administrator_or_unverified",
        "wsl_execution_mode": "installed_on_hold_for_agent_switching",
        "wsl_launcher_state": "launchable" if wsl_status["returncode"] == 0 else "probe_failed",
        "ubuntu_distribution_state": "installed_registered" if "Ubuntu" in wsl_list["stdout_excerpt"] else "not_observed",
        "cloud_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
        "bigtable_state": "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored",
        "iab_state": "available_not_callable_from_session",
        "authoritative_repo": str(AUTHORITATIVE_REPO),
        "execution_worktree": str(ROOT),
        "non_authoritative_workbench": str(NON_AUTHORITATIVE_WORKBENCH),
        "v47_download_root": str(V47_DOWNLOAD_ROOT),
        "v47_artifact_root": str(V47_ARTIFACT_ROOT),
        "archive_roots": {
            "downloads": str(DOWNLOAD_ARCHIVE_ROOT),
            "artifacts": str(ARTIFACT_ARCHIVE_ROOT),
            "worktrees": str(WORKTREE_ARCHIVE_ROOT),
        },
        "global_codex_config": config,
        "codex_cli_version_state": "codex_cli_0_114_0_observed" if "0.114.0" in version["stdout_excerpt"] else "codex_cli_version_observed",
        "codex_cli_login_state": "chatgpt_login_verified" if "Logged in using ChatGPT" in login_text else "login_status_unverified",
        "codex_memory_state": "memories_enabled_in_config_and_feature_list" if config.get("memories") and "memories" in features_proc.stdout else "memory_state_unverified",
        "chronicle_windows_state": "not_windows_live_official_docs_mac_research_preview_config_false",
        "app_plugin_registry_state": "desktop_session_plugins_available_by_context",
        "cli_mcp_registry_state": "cli_mcp_list_verified" if mcp_proc.returncode == 0 else "cli_mcp_probe_failed",
        "cli_mcp_local_stdio": mcp["cli_mcp_local_stdio"],
        "cli_mcp_remote_url": mcp["cli_mcp_remote_url"],
        "automations_dir_present": AUTOMATIONS_DIR.exists(),
        "wsl_paths": {
            "wsl_exe": str(WSL_EXE_PATH),
            "ubuntu_exe": str(UBUNTU_EXE_PATH),
            "wsl_exe_present": WSL_EXE_PATH.exists(),
            "ubuntu_exe_present": UBUNTU_EXE_PATH.exists(),
        },
        "probes": {
            "powershell": ps,
            "admin": admin,
            "wsl_status": wsl_status,
            "wsl_list": wsl_list,
            "codex_version": version,
            "codex_login": login,
            "codex_features": {"returncode": features_proc.returncode, "stdout_excerpt": excerpt(features_proc.stdout), "stderr_excerpt": excerpt(features_proc.stderr, 2000)},
            "codex_mcp": {"returncode": mcp_proc.returncode, "stdout_excerpt": excerpt(mcp_proc.stdout), "stderr_excerpt": excerpt(mcp_proc.stderr, 2000)},
        },
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.operator_note), note(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
