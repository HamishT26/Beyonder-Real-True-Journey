#!/usr/bin/env python3
"""Capture the V44 PowerShell-first operator surface truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v44_common import (
    ARTIFACT_ARCHIVE_ROOT,
    AUTHORITATIVE_REPO,
    DOWNLOAD_ARCHIVE_ROOT,
    EXECUTION_BRANCH,
    NON_AUTHORITATIVE_WORKBENCH,
    ROOT,
    SOURCE_BRANCH,
    STALE_LOCAL_MAIN_WORKTREE,
    UBUNTU_EXE_PATH,
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

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-operator-surface-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-operator-surface-probe-v1.md"


def _stdout_json(command: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    proc = safe_run(command, timeout=120)
    parsed: dict[str, Any] = {}
    text = str(proc.stdout or "").strip()
    if text:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {}
    return (
        {
            "returncode": proc.returncode,
            "stdout_excerpt": proc.stdout[-2400:],
            "stderr_excerpt": proc.stderr[-1200:],
        },
        parsed,
    )


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Operator Surface Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Operator shell preference: `{payload['operator_shell_preference']}`",
        f"- WSL execution mode: `{payload['wsl_execution_mode']}`",
        f"- Worktree baseline state: `{payload['worktree_baseline_state']}`",
        f"- Download archive state: `{payload['download_archive_state']}`",
        "",
        "## Paths",
        "",
        f"- authoritative_repo: `{payload['authoritative_repo']}`",
        f"- execution_worktree: `{payload['execution_worktree']}`",
        f"- stale_local_main_worktree: `{payload['stale_local_main_worktree']}`",
        f"- non_authoritative_workbench: `{payload['non_authoritative_workbench']}`",
        "",
        "## WSL",
        "",
        f"- wsl_launcher_state: `{payload['wsl_launcher_state']}`",
        f"- ubuntu_distribution_state: `{payload['ubuntu_distribution_state']}`",
        f"- app_selector_posture: `{payload['app_selector_posture']}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture the V44 PowerShell-first operator surface truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    ps_probe, ps_parsed = _stdout_json(["powershell.exe", "-NoProfile", "-Command", "$PSVersionTable | ConvertTo-Json -Depth 4"])
    wsl_status = safe_run(["wsl.exe", "--status"], timeout=120)
    wsl_list = safe_run(["wsl.exe", "-l", "-v"], timeout=120)

    archive_roots = {
        "downloads": DOWNLOAD_ARCHIVE_ROOT.exists(),
        "artifacts": ARTIFACT_ARCHIVE_ROOT.exists(),
        "worktrees": WORKTREE_ARCHIVE_ROOT.exists(),
    }
    blockers: list[str] = []
    if ps_probe["returncode"] != 0:
        blockers.append("PowerShell version probe failed.")
    if not WSL_EXE_PATH.exists():
        blockers.append("wsl.exe is missing from the expected system path.")
    if wsl_status.returncode != 0 or wsl_list.returncode != 0:
        blockers.append("WSL launch probes did not complete cleanly.")
    if not all(archive_roots.values()):
        blockers.append("One or more D-drive archive roots are missing.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "v44_execution_lead": "Aletheon",
        "operator_shell_preference": "windows_powershell_primary",
        "operator_shell_state": "powershell_ready" if ps_probe["returncode"] == 0 else "powershell_probe_failed",
        "powershell_edition": str(ps_parsed.get("PSEdition") or ""),
        "powershell_version": str((ps_parsed.get("PSVersion") or {}).get("Major") or "") + "." + str((ps_parsed.get("PSVersion") or {}).get("Minor") or ""),
        "wsl_execution_mode": "installed_on_hold_for_agent_switching",
        "wsl_launcher_state": "launchable" if wsl_status.returncode == 0 else "probe_failed",
        "ubuntu_distribution_state": "installed_registered" if "Ubuntu" in wsl_list.stdout else "not_observed",
        "app_selector_posture": "intentionally_on_hold_app_side_switching",
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
        "download_archive_state": "d_archive_targets_ready" if all(archive_roots.values()) else "archive_root_missing",
        "archive_roots": {key: str(path) for key, path in {
            "downloads": DOWNLOAD_ARCHIVE_ROOT,
            "artifacts": ARTIFACT_ARCHIVE_ROOT,
            "worktrees": WORKTREE_ARCHIVE_ROOT,
        }.items()},
        "archive_root_presence": archive_roots,
        "wsl_paths": {
            "wsl_exe": str(WSL_EXE_PATH),
            "ubuntu_exe": str(UBUNTU_EXE_PATH),
            "wsl_exe_present": WSL_EXE_PATH.exists(),
            "ubuntu_exe_present": UBUNTU_EXE_PATH.exists(),
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
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

