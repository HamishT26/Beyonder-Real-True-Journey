#!/usr/bin/env python3
"""Report bounded V33 WSL health without making Ubuntu a release gate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-wsl-health-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v33-wsl-health-proof-v1.md"
REPO_MOUNT = "/mnt/c/Users/hamis/workspace/Beyonder-Real-True-Journey"
REPO_WINDOWS = r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey"


def run(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        proc.stdout = (proc.stdout or "").replace("\x00", "")
        proc.stderr = (proc.stderr or "").replace("\x00", "")
        return proc
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=(stdout or "").replace("\x00", ""),
            stderr=((stderr or "").replace("\x00", "") + f"\ncommand timed out after {timeout} seconds").strip(),
        )


def run_wsl(args: list[str], *, timeout: int = 30, linux_cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    command = ["wsl.exe", "-d", "Ubuntu"]
    if linux_cwd:
        command.extend(["--cd", linux_cwd])
    command.extend(args)
    return run(command, timeout=timeout)


def status_for(proc: subprocess.CompletedProcess[str]) -> str:
    if proc.returncode == 0:
        return "pass"
    if proc.returncode == 124:
        return "timed_out"
    return "fail"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V33 WSL Health Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- WSL health state: `{payload['wsl_health_state']}`",
        f"- Preferred operator lane: `{payload['preferred_operator_lane']}`",
        f"- Authoritative repo: `{REPO_WINDOWS}`",
        "",
        "## Probe Results",
        "",
    ]
    for key, value in payload.get("probe_results", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    status = run(["wsl.exe", "--status"], timeout=15)
    listing = run(["wsl.exe", "-l", "-v"], timeout=15)
    smoke = run_wsl(["sh", "-lc", "printf V33_WSL_READY"], timeout=20)
    mount = run_wsl(["pwd"], timeout=20, linux_cwd=REPO_MOUNT)
    path_probe = run_wsl(["sh", "-lc", "printf '%s' \"$PATH\""], timeout=20)
    python_probe = run_wsl(["python3", "--version"], timeout=20)
    git_probe = run_wsl(["git", "--version"], timeout=20)
    repo_git = run_wsl(["git", "status", "-uno", "--short"], timeout=45, linux_cwd=REPO_MOUNT)

    ubuntu_ready = all(
        proc.returncode == 0
        for proc in (smoke, mount, path_probe, python_probe, git_probe)
    ) and mount.stdout.strip() == REPO_MOUNT

    blockers: list[str] = []
    if smoke.returncode != 0:
        blockers.append("Ubuntu did not launch cleanly from PowerShell.")
    if mount.returncode != 0 or mount.stdout.strip() != REPO_MOUNT:
        blockers.append("The authoritative repo mount is not readable from Ubuntu.")
    if python_probe.returncode != 0:
        blockers.append("python3 is not available in Ubuntu PATH.")
    if git_probe.returncode != 0:
        blockers.append("git is not available in Ubuntu PATH.")
    if not path_probe.stdout.strip():
        blockers.append("Ubuntu PATH probe returned an empty result.")

    proof_state = "ubuntu_repo_ready" if ubuntu_ready else "windows_fallback_primary"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v33_omega",
        "overall_status": "PASS" if ubuntu_ready else "WARN",
        "proof_state": proof_state,
        "wsl_health_state": proof_state,
        "preferred_operator_lane": "ubuntu" if ubuntu_ready else "windows_powershell_rest_kubectl",
        "authoritative_repo_path": REPO_WINDOWS,
        "authoritative_repo_mount": REPO_MOUNT,
        "probe_results": {
            "wsl_status": status_for(status),
            "wsl_inventory": status_for(listing),
            "ubuntu_launch": status_for(smoke),
            "repo_mount_visibility": status_for(mount),
            "path_probe": status_for(path_probe),
            "python3_probe": status_for(python_probe),
            "git_probe": status_for(git_probe),
            "repo_git_status_probe": status_for(repo_git),
        },
        "probe_details": {
            "status_stdout": status.stdout.strip(),
            "status_stderr": status.stderr.strip(),
            "inventory_stdout": listing.stdout.strip(),
            "inventory_stderr": listing.stderr.strip(),
            "launch_stdout": smoke.stdout.strip(),
            "launch_stderr": smoke.stderr.strip(),
            "mount_stdout": mount.stdout.strip(),
            "mount_stderr": mount.stderr.strip(),
            "path_prefix": path_probe.stdout.strip()[:400],
            "python_stdout": python_probe.stdout.strip(),
            "python_stderr": python_probe.stderr.strip(),
            "git_stdout": git_probe.stdout.strip(),
            "git_stderr": git_probe.stderr.strip(),
            "repo_git_stdout": repo_git.stdout.strip(),
            "repo_git_stderr": repo_git.stderr.strip(),
        },
        "blockers": blockers,
        "non_gating_note": "WSL remains a bounded side-lane for V33; Windows PowerShell stays valid even when this probe warns.",
    }
    write_outputs(payload)
    return 0 if ubuntu_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
