#!/usr/bin/env python3
"""Bounded self-healing/support utility for the V30 Ubuntu sandbox."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for raw in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        parts = raw.replace(":", "").split()
        if len(parts) >= 2 and parts[1].isdigit():
            values[parts[0]] = int(parts[1])
    return values


def main() -> int:
    sandbox_root = Path("/home/aletheon/v30-fluid-lab")
    repo_root = Path(os.environ.get("TRINITY_REPO_ROOT", "/mnt/c/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey"))
    repo_root_windows = os.environ.get(
        "TRINITY_REPO_ROOT_WINDOWS",
        "C:/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey",
    )
    temp_root = sandbox_root / "temp"
    temp_root.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    native_probe = subprocess.run(
        [
            "timeout",
            "12",
            "git",
            "-c",
            f"safe.directory={repo_root}",
            "-C",
            str(repo_root),
            "status",
            "--short",
            "-uno",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    bridge_probe = None
    if native_probe.returncode == 124:
        bridge_probe = subprocess.run(
            [
                "timeout",
                "12",
                "cmd.exe",
                "/c",
                "git",
                "-C",
                repo_root_windows,
                "status",
                "--short",
                "-uno",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    active_probe = bridge_probe if bridge_probe is not None else native_probe
    git_duration_ms = round((time.perf_counter() - started) * 1000, 3)

    meminfo = read_meminfo()
    disk = shutil.disk_usage(sandbox_root)

    removed_files = 0
    removed_bytes = 0
    for child in temp_root.rglob("*"):
        if not child.is_file():
            continue
        removed_bytes += child.stat().st_size
        child.unlink()
        removed_files += 1

    payload = {
        "generated_utc": now_iso(),
        "experiment_id": "V30-E003",
        "overall_status": "PASS" if active_probe.returncode == 0 else "WARN",
        "proof_state": "bounded_local_support_utility",
        "repo_root": str(repo_root),
        "repo_status_mode": (
            "windows_git_bridge_uno"
            if bridge_probe is not None and bridge_probe.returncode == 0
            else "native_linux_uno"
        ),
        "git_status_probe": {
            "returncode": active_probe.returncode,
            "duration_ms": git_duration_ms,
            "stdout_preview": active_probe.stdout.strip().splitlines()[:10],
            "stderr_preview": active_probe.stderr.strip().splitlines()[:10],
            "native_linux_uno": {
                "returncode": native_probe.returncode,
                "stdout_preview": native_probe.stdout.strip().splitlines()[:10],
                "stderr_preview": native_probe.stderr.strip().splitlines()[:10],
            },
            "windows_git_bridge_uno": (
                {
                    "returncode": bridge_probe.returncode,
                    "stdout_preview": bridge_probe.stdout.strip().splitlines()[:10],
                    "stderr_preview": bridge_probe.stderr.strip().splitlines()[:10],
                }
                if bridge_probe is not None
                else None
            ),
        },
        "memory": {
            "mem_total_kb": meminfo.get("MemTotal", 0),
            "mem_available_kb": meminfo.get("MemAvailable", 0),
        },
        "disk": {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        },
        "sandbox_temp_cleanup": {
            "removed_files": removed_files,
            "removed_bytes": removed_bytes,
        },
        "notes": [
            "This is a bounded observation and cleanup utility, not a resident daemon.",
            "Repo state was observed only through git status -uno with a Windows-git bridge fallback; no repo files were rewritten.",
        ],
    }

    artifact_path = sandbox_root / "artifacts" / "v30-e003-self-healing-latest.json"
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(artifact_path)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
