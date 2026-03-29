#!/usr/bin/env python3
"""Probe Ubuntu WSL readiness for Trinity v27."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "v27-linux-readiness-matrix-v1.json"
OUTPUT_MD = ROOT / "docs" / "v27-linux-readiness-matrix-v1.md"
REPO_MOUNT = "/mnt/c/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=(exc.stdout or "").replace("\x00", ""),
            stderr=(exc.stderr or "").replace("\x00", "") + f"\ncommand timed out after {timeout} seconds",
        )


def run_wsl(args: list[str], timeout: int = 30, linux_cwd: str | None = None) -> subprocess.CompletedProcess[str]:
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_wsl_inventory() -> list[dict[str, Any]]:
    proc = run(["wsl.exe", "-l", "-v"], timeout=20)
    raw = (proc.stdout or "").replace("\x00", "")
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("name"):
            continue
        if line.startswith("*"):
            line = line[1:].strip()
        parts = line.split()
        if len(parts) < 3:
            continue
        version = parts[-1]
        state = parts[-2]
        name = " ".join(parts[:-2])
        row: dict[str, Any] = {"name": name, "state": state}
        try:
            row["version"] = int(version)
        except ValueError:
            row["version"] = version
        rows.append(row)
    return rows


def main() -> int:
    inventory = parse_wsl_inventory()
    launch_probe = run_wsl(
        ["bash", "-lc", "printf ready"],
        timeout=20,
    )
    mount_probe = run_wsl(["pwd"], timeout=20, linux_cwd=REPO_MOUNT)
    node_probe = run_wsl(["node", "-v"], timeout=20)
    npm_probe = run_wsl(["npm", "-v"], timeout=20)
    python_probe = run_wsl(["python3", "--version"], timeout=20)
    git_probe = run_wsl(["git", "--version"], timeout=20)
    repo_git_probe = run_wsl(
        ["git", "status", "--short", "--untracked-files=all"],
        timeout=120,
        linux_cwd=REPO_MOUNT,
    )
    temp_probe = run_wsl(
        [
            "python3",
            "-c",
            "from pathlib import Path; p=Path('/tmp/v27-smoke.txt'); p.write_text('v27 smoke\\n'); print(p.read_text().strip()); p.unlink()",
        ],
        timeout=20,
    )
    launch_ok = launch_probe.returncode == 0 or any(
        probe.returncode == 0 for probe in [mount_probe, node_probe, npm_probe, python_probe, git_probe, temp_probe]
    )

    blocking_gaps: list[str] = []
    if not launch_ok:
        blocking_gaps.append("Ubuntu did not launch noninteractively from PowerShell.")
    if mount_probe.returncode != 0 or mount_probe.stdout.strip() != REPO_MOUNT:
        blocking_gaps.append("The repo mount under /mnt/c is not readable from Ubuntu.")
    if node_probe.returncode != 0:
        blocking_gaps.append("node is not available in Ubuntu PATH.")
    if npm_probe.returncode != 0:
        blocking_gaps.append("npm is not available in Ubuntu PATH.")
    if python_probe.returncode != 0:
        blocking_gaps.append("python3 is not available in Ubuntu PATH.")
    if git_probe.returncode != 0:
        blocking_gaps.append("git is not available in Ubuntu PATH.")
    if repo_git_probe.returncode == 124:
        blocking_gaps.append("Bounded git status timed out against the OneDrive-mounted repo inside Ubuntu.")
    elif repo_git_probe.returncode != 0:
        detail = repo_git_probe.stderr.strip() or repo_git_probe.stdout.strip() or "unknown error"
        blocking_gaps.append(f"Bounded git status failed inside Ubuntu: {detail}")
    if temp_probe.returncode != 0:
        detail = temp_probe.stderr.strip() or temp_probe.stdout.strip() or "unknown error"
        blocking_gaps.append(f"Temp-file smoke check failed inside Ubuntu: {detail}")

    pass_gate = not blocking_gaps
    payload = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if pass_gate else "WARN",
        "phase": "v27_omega",
        "authority_model": "repo_first",
        "docker_runtime_role": "fallback_only",
        "current_shell": "ubuntu" if pass_gate else "powershell",
        "linux_switch_recommended_now": pass_gate,
        "readiness_state": "ubuntu_validated_primary" if pass_gate else "ubuntu_probe_blocked",
        "current_wsl_inventory": inventory,
        "probe_results": {
            "ubuntu_launch_noninteractive": "pass" if launch_ok else status_for(launch_probe),
            "repo_mount_visibility": status_for(mount_probe),
            "node_probe": status_for(node_probe),
            "npm_probe": status_for(npm_probe),
            "python3_probe": status_for(python_probe),
            "git_probe": status_for(git_probe),
            "repo_git_status_probe": status_for(repo_git_probe),
            "tempfile_smoke_probe": status_for(temp_probe),
            "docker_probe": "fallback_only_not_required",
            "kubectl_probe": "fallback_only_not_required",
        },
        "probe_details": {
            "launch_stdout": launch_probe.stdout.strip(),
            "launch_stderr": launch_probe.stderr.strip(),
            "launch_basis": (
                "direct_probe"
                if launch_probe.returncode == 0
                else "inferred_from_successful_downstream_ubuntu_commands"
                if launch_ok
                else "probe_failed"
            ),
            "mount_stdout": mount_probe.stdout.strip(),
            "mount_stderr": mount_probe.stderr.strip(),
            "node_stdout": node_probe.stdout.strip(),
            "npm_stdout": npm_probe.stdout.strip(),
            "python3_stdout": python_probe.stdout.strip(),
            "git_stdout": git_probe.stdout.strip(),
            "repo_git_status_stdout": repo_git_probe.stdout.strip(),
            "repo_git_status_stderr": repo_git_probe.stderr.strip(),
            "tempfile_smoke_stdout": temp_probe.stdout.strip(),
            "tempfile_smoke_stderr": temp_probe.stderr.strip(),
        },
        "blocking_gaps": blocking_gaps,
        "recommendation": {
            "keep_current_shell": "ubuntu" if pass_gate else "powershell",
            "reason": (
                "Ubuntu met the bounded v27 toolchain and repo-parity gate."
                if pass_gate
                else "PowerShell remains primary because Ubuntu still has at least one bounded parity blocker."
            ),
        },
    }

    write_json(OUTPUT_JSON, payload)
    write_text(
        OUTPUT_MD,
        "\n".join(
            [
                "# V27 Linux Readiness Matrix",
                "",
                f"- overall_status: `{payload['overall_status']}`",
                f"- current_shell: `{payload['current_shell']}`",
                f"- readiness_state: `{payload['readiness_state']}`",
                f"- docker_runtime_role: `{payload['docker_runtime_role']}`",
                "",
                "## Probe Results",
                *[
                    f"- {key}: `{value}`"
                    for key, value in payload["probe_results"].items()
                ],
                "",
                "## Blocking Gaps",
                *([f"- {item}" for item in blocking_gaps] or ["- none"]),
                "",
            ]
        )
        + "\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
