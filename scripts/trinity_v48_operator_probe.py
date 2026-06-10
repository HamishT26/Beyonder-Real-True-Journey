#!/usr/bin/env python3
"""Capture V48 PowerShell, WSL hold, Codex CLI, plugin, and storage truth."""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path
from typing import Any

from trinity_v48_common import (
    ADVISORY_SOURCE,
    ARTIFACT_ARCHIVE_ROOT,
    AUTHORITATIVE_REPO,
    DOWNLOAD_ARCHIVE_ROOT,
    GLOBAL_CODEX_CONFIG,
    NON_AUTHORITATIVE_WORKBENCH,
    ROOT,
    UBUNTU_EXE_PATH,
    V47_WORKTREE,
    V48_ARTIFACT_ROOT,
    V48_DOWNLOAD_ROOT,
    WORKTREE_ARCHIVE_ROOT,
    WORKTREE_BASELINE_SHA,
    WORKTREE_BASELINE_STATE,
    WSL_EXE_PATH,
    dir_size_bytes,
    ensure_archive_roots,
    excerpt,
    git_branch,
    git_head,
    now_iso,
    safe_run,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-operator-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v48-operator-probe-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "v48-powershell-control-plane-note-v1.md"


def _config() -> dict[str, Any]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return {"exists": False, "mcp_servers": [], "plugins": []}
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"exists": True, "error": str(exc), "mcp_servers": [], "plugins": []}
    mcp = data.get("mcp_servers") if isinstance(data.get("mcp_servers"), dict) else {}
    plugins = data.get("plugins") if isinstance(data.get("plugins"), dict) else {}
    plugin_names = sorted(str(key).split("@", 1)[0] for key in plugins.keys())
    return {
        "exists": True,
        "model": str(data.get("model") or ""),
        "model_reasoning_effort": str(data.get("model_reasoning_effort") or ""),
        "approval_policy": str(data.get("approval_policy") or ""),
        "sandbox_mode": str(data.get("sandbox_mode") or ""),
        "memories": bool(data.get("memories")) if isinstance(data.get("memories"), bool) else True,
        "chronicle": bool(data.get("chronicle")) if "chronicle" in data else False,
        "mcp_servers": sorted(mcp.keys()),
        "plugins": plugin_names,
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


def _drive_state() -> dict[str, Any]:
    proc = safe_run(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "$d=Get-PSDrive -Name C,D | Select-Object Name,Root,Free,Used; $d | ConvertTo-Json -Depth 4",
        ],
        timeout=60,
    )
    return {"returncode": proc.returncode, "stdout_excerpt": excerpt(proc.stdout, 3000), "stderr_excerpt": excerpt(proc.stderr, 1000)}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V48 Operator Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Worktree baseline state: `{payload['worktree_baseline_state']}`",
        f"- PowerShell state: `{payload['powershell_hygiene_state']}`",
        f"- WSL execution mode: `{payload['wsl_execution_mode']}`",
        f"- Cloud execution mode: `{payload['cloud_execution_mode']}`",
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
            "# V48 PowerShell Control-Plane Note",
            "",
            "- PowerShell remains the V48 operator lane. Administrator mode is observed only as execution context, not permission to run destructive cleanup without classification.",
            "- WSL is installed and intentionally on hold for app-side agent switching.",
            "- GCP, Bigtable, Vertex, Gemini CLI, Vesper Ion, and Kai stay on standby until billing/auth/project truth is restored.",
            f"- Use `{payload['v48_download_root']}` for bulky downloads and `{payload['v48_artifact_root']}` for generated artifacts.",
            "- Treat Codex app plugins and Codex CLI MCP servers as separate capability surfaces.",
            "- Vercel, Neon, CircleCI, and Notion must publish live callability before any production or paid action.",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture V48 operator truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--operator-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()
    ensure_archive_roots()
    config = _config()
    ps = _probe(["powershell.exe", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"])
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
        blockers.append("V48 worktree baseline SHA mismatch.")
    if ps["returncode"] != 0:
        blockers.append("PowerShell probe failed.")
    if version["returncode"] != 0 or login["returncode"] != 0:
        blockers.append("Codex CLI version/login probe failed.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "v48_execution_lead": "Aletheon",
        "ari_activation_state": "verified_bounded_helper",
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
        "cloud_execution_mode": "standby_billing_auth_project_not_cleared",
        "local_to_cloud_runtime_state": "on_hold_app_side_model_unavailable",
        "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
        "bigtable_state": "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored",
        "iab_state": "available_not_callable_from_session",
        "authoritative_repo": str(AUTHORITATIVE_REPO),
        "execution_worktree": str(ROOT),
        "v47_worktree_readonly": str(V47_WORKTREE),
        "non_authoritative_workbench": str(NON_AUTHORITATIVE_WORKBENCH),
        "v48_download_root": str(V48_DOWNLOAD_ROOT),
        "v48_artifact_root": str(V48_ARTIFACT_ROOT),
        "archive_roots": {"downloads": str(DOWNLOAD_ARCHIVE_ROOT), "artifacts": str(ARTIFACT_ARCHIVE_ROOT), "worktrees": str(WORKTREE_ARCHIVE_ROOT)},
        "advisory_source": {"path": str(ADVISORY_SOURCE), "present": ADVISORY_SOURCE.exists()},
        "global_codex_config": config,
        "codex_cli_version_state": "codex_cli_observed" if version["returncode"] == 0 else "codex_cli_missing",
        "codex_cli_login_state": "chatgpt_login_verified" if "Logged in using ChatGPT" in login_text else "login_status_unverified",
        "codex_memory_state": "memories_enabled_in_config_and_feature_list" if config.get("memories") and "memories" in features_proc.stdout else "memory_state_unverified",
        "chronicle_windows_state": "not_windows_live_official_docs_mac_research_preview_config_false",
        "app_plugin_registry_state": "desktop_session_plugins_available_by_context",
        "cli_mcp_registry_state": "cli_mcp_list_verified" if mcp_proc.returncode == 0 else "cli_mcp_probe_failed",
        "cli_mcp_local_stdio": mcp["cli_mcp_local_stdio"],
        "cli_mcp_remote_url": mcp["cli_mcp_remote_url"],
        "storage_snapshot": {
            "drive_probe": _drive_state(),
            "authoritative_repo_local_runtime_mb": round(dir_size_bytes(AUTHORITATIVE_REPO / ".local-runtime") / (1024 * 1024), 2),
            "authoritative_repo_docs_mb": round(dir_size_bytes(AUTHORITATIVE_REPO / "docs") / (1024 * 1024), 2),
            "v48_worktree_mb": round(dir_size_bytes(ROOT) / (1024 * 1024), 2),
        },
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
