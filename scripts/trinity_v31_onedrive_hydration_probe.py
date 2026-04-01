#!/usr/bin/env python3
"""Probe the degraded OneDrive repo and the stable local clone for V31 hydration truth."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONEDRIVE_ROOT = Path.home() / "OneDrive"
BROKEN_REPO = ONEDRIVE_ROOT / "Documents" / "GitHub" / "Beyonder-Real-True-Journey"
STABLE_REPO = ROOT
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v31-onedrive-repo-hydration-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v31-onedrive-repo-hydration-proof-v1.md"
SAMPLE_FILES = [
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run(command: list[str], timeout: int = 30) -> dict[str, object]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"Timed out after {timeout}s",
        }
    except Exception as exc:  # pragma: no cover - defensive wrapper
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
        }


def powershell_get_content(path: Path) -> dict[str, object]:
    return run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Content -Path '{path}' -TotalCount 1",
        ],
        timeout=20,
    )


def python_read(path: Path) -> dict[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
        return {"ok": True, "bytes": len(text.encode('utf-8')), "error": ""}
    except Exception as exc:  # pragma: no cover - filesystem health probe
        return {"ok": False, "bytes": 0, "error": str(exc)}


def git_status(path: Path) -> dict[str, object]:
    return run(["git", "-C", str(path), "status", "--short"], timeout=45)


def wsl_status(path: Path) -> dict[str, object]:
    wsl_path = "/mnt/" + path.drive[0].lower() + path.as_posix()[2:]
    return run(
        ["wsl.exe", "bash", "-lc", f"cd {wsl_path!s} && git status --short"],
        timeout=45,
    )


def attrib(path: Path) -> str:
    result = run(["attrib", str(path)], timeout=10)
    if result["ok"]:
        return str(result["stdout"]).strip()
    return str(result["stderr"]).strip()


def find_candidates() -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for rel in (".local-archives", "docs/memory-archives"):
        base = ROOT / rel
        if not base.exists():
            continue
        for child in sorted(base.rglob("*")):
            if child.is_file():
                stat = child.stat()
                candidates.append(
                    {
                        "path": child.relative_to(ROOT).as_posix(),
                        "bytes": stat.st_size,
                    }
                )
    return candidates


def count_onedrive_offline_files() -> int:
    if not BROKEN_REPO.exists():
        return 0
    result = run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            (
                "$count = (Get-ChildItem -LiteralPath "
                f"'{BROKEN_REPO}' -Recurse -File -ErrorAction SilentlyContinue "
                "| Where-Object { $_.Attributes.ToString().Contains('Offline') }).Count; "
                "Write-Output $count"
            ),
        ],
        timeout=60,
    )
    try:
        return int(str(result["stdout"]).strip() or "0")
    except ValueError:
        return 0


def disk_free_gib(path: Path) -> float:
    usage = shutil.disk_usage(path)
    return round(usage.free / (1024 ** 3), 2)


def file_probe(repo_root: Path, rel: str) -> dict[str, object]:
    path = repo_root / rel
    py_result = python_read(path)
    ps_result = powershell_get_content(path)
    return {
        "relative_path": rel,
        "exists": path.exists(),
        "python_read_ok": py_result["ok"],
        "python_read_error": py_result["error"],
        "powershell_read_ok": ps_result["ok"],
        "powershell_read_error": ps_result["stderr"],
        "attrib": attrib(path) if path.exists() else "",
    }


def classify_health(onedrive_probes: list[dict[str, object]], onedrive_git: dict[str, object]) -> tuple[str, str]:
    probe_failures = [
        probe for probe in onedrive_probes if not probe["python_read_ok"] or not probe["powershell_read_ok"]
    ]
    if probe_failures or not onedrive_git["ok"]:
        return "degraded_cloud_provider_io", "degraded"
    return "healthy", "healthy"


def main() -> int:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    stable_probes = [file_probe(STABLE_REPO, rel) for rel in SAMPLE_FILES]
    onedrive_probes = [file_probe(BROKEN_REPO, rel) for rel in SAMPLE_FILES]
    stable_git = git_status(STABLE_REPO)
    stable_wsl = wsl_status(STABLE_REPO)
    onedrive_git = git_status(BROKEN_REPO) if BROKEN_REPO.exists() else {"ok": False, "stderr": "Repo path missing"}
    onedrive_health, cloud_health = classify_health(onedrive_probes, onedrive_git)
    migration_candidates = find_candidates()
    free_gib = disk_free_gib(STABLE_REPO)

    payload = {
        "generated_utc": now_iso(),
        "phase": "v31_omega",
        "authority_model": "repo_first",
        "authoritative_repo_path": str(STABLE_REPO),
        "onedrive_repo_path": str(BROKEN_REPO),
        "onedrive_repo_hydration_state": "stable_local_clone_primary",
        "onedrive_repo_path_state": onedrive_health,
        "onedrive_migration_state": "phase_a_authority_hydrated_phase_b_guided_non_authoritative_only",
        "cloud_provider_health": cloud_health,
        "disk_free_gib": free_gib,
        "stable_repo": {
            "windows_git_status_ok": stable_git["ok"],
            "windows_git_status_stderr": stable_git["stderr"],
            "wsl_git_status_ok": stable_wsl["ok"],
            "wsl_git_status_stderr": stable_wsl["stderr"],
            "file_probes": stable_probes,
        },
        "onedrive_repo": {
            "exists": BROKEN_REPO.exists(),
            "windows_git_status_ok": onedrive_git.get("ok", False),
            "windows_git_status_stderr": onedrive_git.get("stderr", ""),
            "offline_file_count": count_onedrive_offline_files(),
            "file_probes": onedrive_probes,
        },
        "migration_candidates": {
            "count": len(migration_candidates),
            "sample": migration_candidates[:20],
            "recommended_target_root": str(ONEDRIVE_ROOT / "Beyonder-Working-Mirror"),
            "policy": [
                "Keep the stable workspace repo authoritative and fully local.",
                "Only mirror non-authoritative archives and generated outputs into OneDrive during V31.",
                "Do not make repo-tracked runtime truth files cloud-only.",
            ],
        },
        "guided_actions": [
            {
                "phase": "A",
                "title": "Keep authority local",
                "command": "Use the stable local clone outside OneDrive as the active repo until cloud-provider read failures stop.",
            },
            {
                "phase": "B",
                "title": "Mirror non-authoritative archives",
                "command": (
                    "Create or reuse a OneDrive mirror folder such as "
                    f"'{ONEDRIVE_ROOT / 'Beyonder-Working-Mirror'}' and copy only archives, zips, and exported reports there."
                ),
            },
            {
                "phase": "B",
                "title": "Verify before pruning",
                "command": "After each mirror sync, verify file counts and hashes before deleting any local non-authoritative copies.",
            },
        ],
        "notes": [
            "The OneDrive-hosted working copy remains degraded because file reads and git indexing are failing through the cloud provider.",
            "The stable local clone is readable from Windows and remains the authoritative V31 worktree.",
            "Native WSL git should be treated as healthy only if its status probe succeeds within the timeout; otherwise the Windows-git bridge remains the fallback.",
        ],
    }

    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# V31 OneDrive Repo Hydration Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Authoritative repo path: `{payload['authoritative_repo_path']}`",
        f"- OneDrive repo path state: `{payload['onedrive_repo_path_state']}`",
        f"- Cloud provider health: `{payload['cloud_provider_health']}`",
        f"- Stable Windows git status OK: `{payload['stable_repo']['windows_git_status_ok']}`",
        f"- Stable WSL git status OK: `{payload['stable_repo']['wsl_git_status_ok']}`",
        f"- OneDrive Windows git status OK: `{payload['onedrive_repo']['windows_git_status_ok']}`",
        f"- OneDrive offline file count: `{payload['onedrive_repo']['offline_file_count']}`",
        f"- Local free space: `{payload['disk_free_gib']} GiB`",
        "",
        "## Decision",
        "",
        "- Keep the stable local clone outside OneDrive as the authoritative V31 worktree.",
        "- Treat the OneDrive-hosted repo as degraded until cloud-provider read failures clear.",
        "- Limit V31 OneDrive usage to guided, verified mirroring of non-authoritative archives and exports.",
        "",
        "## Guided Actions",
        "",
    ]
    for action in payload["guided_actions"]:
        lines.append(f"- Phase {action['phase']}: {action['title']} — {action['command']}")
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
