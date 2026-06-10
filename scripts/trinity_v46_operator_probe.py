#!/usr/bin/env python3
"""Capture V46 PowerShell, Codex CLI, WSL-hold, and archive truth."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

from trinity_v46_common import (
    ARTIFACT_ARCHIVE_ROOT,
    AUTHORITATIVE_REPO,
    AUTOMATIONS_DIR,
    DOWNLOAD_ARCHIVE_ROOT,
    EXECUTION_BRANCH,
    GLOBAL_CODEX_CONFIG,
    NON_AUTHORITATIVE_WORKBENCH,
    ROOT,
    SOURCE_BRANCH,
    UBUNTU_EXE_PATH,
    V46_ARTIFACT_ROOT,
    V46_DOWNLOAD_ROOT,
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

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-operator-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-operator-probe-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "v46-powershell-operator-note-v1.md"


def _parse_config() -> dict[str, Any]:
    if not GLOBAL_CODEX_CONFIG.exists():
        return {"config_exists": False, "mcp_servers": []}
    try:
        data = tomllib.loads(GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"config_exists": True, "parse_error": str(exc), "mcp_servers": []}
    mcp = data.get("mcp_servers") if isinstance(data.get("mcp_servers"), dict) else {}
    memories = data.get("memories") if isinstance(data.get("memories"), dict) else {}
    return {
        "config_exists": True,
        "model": str(data.get("model") or ""),
        "model_reasoning_effort": str(data.get("model_reasoning_effort") or ""),
        "approval_policy": str(data.get("approval_policy") or ""),
        "sandbox_mode": str(data.get("sandbox_mode") or ""),
        "chronicle": bool(data.get("chronicle")) if "chronicle" in data else False,
        "memories": data.get("memories") if isinstance(data.get("memories"), bool) else bool(memories),
        "mcp_servers": sorted(mcp.keys()),
    }


def _mcp_summary(raw: str) -> dict[str, list[str]]:
    local_stdio: list[str] = []
    remote_url: list[str] = []
    remote_mode = False
    known = {"MCP_DOCKER", "github", "google_drive", "playwright", "composio", "figma", "linear", "notion"}
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Name") and "Url" in line:
            remote_mode = True
            continue
        if line.startswith("Name") or line.startswith("-"):
            continue
        name = line.split()[0]
        if name in known:
            (remote_url if remote_mode else local_stdio).append(name)
    return {"cli_mcp_local_stdio": sorted(set(local_stdio)), "cli_mcp_remote_url": sorted(set(remote_url))}


def _probe(command: list[str], timeout: int = 180) -> dict[str, Any]:
    proc = safe_run(command, timeout=timeout)
    return {"returncode": proc.returncode, "stdout_excerpt": excerpt(proc.stdout), "stderr_excerpt": excerpt(proc.stderr, 2000)}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V46 Operator Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Worktree baseline: `{payload['worktree_baseline_state']}`",
        f"- PowerShell state: `{payload['powershell_hygiene_state']}`",
        f"- WSL execution mode: `{payload['wsl_execution_mode']}`",
        f"- Codex CLI version state: `{payload['codex_cli_version_state']}`",
        f"- Codex CLI login state: `{payload['codex_cli_login_state']}`",
        f"- Config model state: `{payload['codex_cli_config_model_state']}`",
        "",
        "## App / CLI Split",
        "",
        f"- App plugin registry state: `{payload['app_plugin_registry_state']}`",
        f"- CLI MCP registry state: `{payload['cli_mcp_registry_state']}`",
        f"- CLI local MCPs: `{', '.join(payload['cli_mcp_local_stdio'])}`",
        f"- CLI remote MCPs: `{', '.join(payload['cli_mcp_remote_url'])}`",
    ]
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def operator_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V46 PowerShell Operator Note",
            "",
            "- PowerShell remains the active V46 lane. Keep WSL installed, callable, and on hold for app-side agent switching.",
            f"- Use `{payload['v46_download_root']}` for bulky V46 downloads and `{payload['v46_artifact_root']}` for bulky V46 artifacts.",
            "- Use `codex exec -m gpt-5.4 -c model_reasoning_effort=\"xhigh\"` for explicit CLI candidate probes.",
            "- Treat app plugins and CLI MCP servers as separate surfaces. The CLI truth is `codex mcp list`; the app truth is this desktop session's connector/plugin availability.",
            "- Keep GCP, Vesper Ion, Kai, Bigtable, Vertex AI, Agent Engine, Google Drive writes, and Gemini CLI on standby until billing/auth/project truth is restored.",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture V46 PowerShell and Codex operator truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--operator-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()

    V46_DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    V46_ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

    config = _parse_config()
    ps = _probe(["powershell.exe", "-NoProfile", "-Command", "$PSVersionTable | ConvertTo-Json -Depth 4"])
    wsl_status = _probe(["wsl.exe", "--status"], timeout=120)
    wsl_list = _probe(["wsl.exe", "-l", "-v"], timeout=120)
    codex_version = _probe(["codex", "--version"], timeout=120)
    codex_login = _probe(["codex", "login", "status"], timeout=120)
    codex_features = _probe(["codex", "features", "list"], timeout=120)
    codex_mcp_proc = safe_run(["codex", "mcp", "list"], timeout=120)
    codex_mcp = {"returncode": codex_mcp_proc.returncode, "stdout_excerpt": excerpt(codex_mcp_proc.stdout), "stderr_excerpt": excerpt(codex_mcp_proc.stderr, 2000)}
    mcp_summary = _mcp_summary(codex_mcp_proc.stdout)

    blockers: list[str] = []
    if git_head() != WORKTREE_BASELINE_SHA:
        blockers.append("V46 worktree head does not match the expected remote baseline.")
    if ps["returncode"] != 0:
        blockers.append("PowerShell probe failed.")
    if codex_version["returncode"] != 0:
        blockers.append("Codex CLI version probe failed.")
    if codex_login["returncode"] != 0:
        blockers.append("Codex login status probe failed.")
    if config.get("model") != "gpt-5.4" or config.get("model_reasoning_effort") != "xhigh":
        blockers.append("Global Codex config does not declare gpt-5.4 with xhigh reasoning.")

    codex_login_text = f"{codex_login['stdout_excerpt']}\n{codex_login['stderr_excerpt']}"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "v46_execution_lead": "Aletheon",
        "authority_model": "repo_first",
        "source_branch": SOURCE_BRANCH,
        "execution_branch": git_branch() or EXECUTION_BRANCH,
        "current_head_sha": git_head(),
        "worktree_baseline_sha": WORKTREE_BASELINE_SHA,
        "worktree_baseline_state": WORKTREE_BASELINE_STATE,
        "operator_shell_preference": "windows_powershell_primary",
        "powershell_hygiene_state": "powershell_ready" if ps["returncode"] == 0 else "powershell_probe_failed",
        "wsl_execution_mode": "installed_on_hold_for_agent_switching",
        "wsl_launcher_state": "launchable" if wsl_status["returncode"] == 0 else "probe_failed",
        "ubuntu_distribution_state": "installed_registered" if "Ubuntu" in wsl_list["stdout_excerpt"] else "not_observed",
        "cloud_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
        "authoritative_repo": str(AUTHORITATIVE_REPO),
        "execution_worktree": str(ROOT),
        "non_authoritative_workbench": str(NON_AUTHORITATIVE_WORKBENCH),
        "download_archive_root": str(DOWNLOAD_ARCHIVE_ROOT),
        "artifact_archive_root": str(ARTIFACT_ARCHIVE_ROOT),
        "worktree_archive_root": str(WORKTREE_ARCHIVE_ROOT),
        "v46_download_root": str(V46_DOWNLOAD_ROOT),
        "v46_artifact_root": str(V46_ARTIFACT_ROOT),
        "global_codex_config": str(GLOBAL_CODEX_CONFIG),
        "global_codex_config_present": GLOBAL_CODEX_CONFIG.exists(),
        "global_codex_config": config,
        "codex_cli_version_state": "codex_cli_0_114_0_observed" if "0.114.0" in codex_version["stdout_excerpt"] else "codex_cli_version_observed",
        "codex_cli_login_state": "chatgpt_login_verified" if "Logged in using ChatGPT" in codex_login_text else "login_status_unverified",
        "codex_cli_config_model_state": "gpt_5_4_xhigh_configured" if config.get("model") == "gpt-5.4" and config.get("model_reasoning_effort") == "xhigh" else "config_mismatch",
        "app_plugin_registry_state": "desktop_session_plugins_available_by_context",
        "cli_mcp_registry_state": "cli_mcp_list_verified" if codex_mcp["returncode"] == 0 else "cli_mcp_probe_failed",
        "cli_mcp_local_stdio": mcp_summary["cli_mcp_local_stdio"],
        "cli_mcp_remote_url": mcp_summary["cli_mcp_remote_url"],
        "chronicle_windows_state": "not_windows_live_official_docs_mac_pro_only_config_false",
        "automations_dir_present": AUTOMATIONS_DIR.exists(),
        "wsl_paths": {
            "wsl_exe": str(WSL_EXE_PATH),
            "ubuntu_exe": str(UBUNTU_EXE_PATH),
            "wsl_exe_present": WSL_EXE_PATH.exists(),
            "ubuntu_exe_present": UBUNTU_EXE_PATH.exists(),
        },
        "probes": {
            "powershell": ps,
            "wsl_status": wsl_status,
            "wsl_list": wsl_list,
            "codex_version": codex_version,
            "codex_login": codex_login,
            "codex_features": codex_features,
            "codex_mcp": codex_mcp,
        },
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.operator_note), operator_note(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
