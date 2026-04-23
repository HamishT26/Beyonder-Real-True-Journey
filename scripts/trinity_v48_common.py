#!/usr/bin/env python3
"""Shared helpers for the V48 Omega local cleanup and control-plane lane."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
SOURCE_BRANCH = f"origin/{PUBLICATION_BRANCH}"
EXECUTION_BRANCH = "codex/GHC-Family/v48-omega-exec"
WORKTREE_BASELINE_SHA = "e62358965c02fb5616f9d1ffe0d451e5848ca52d"
WORKTREE_BASELINE_STATE = "origin_verified_at_execution"
AUTHORITATIVE_REPO = Path(r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey")
V47_WORKTREE = Path(r"D:\GHC-Archives\worktrees\v47-omega")
NON_AUTHORITATIVE_WORKBENCH = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
DOWNLOAD_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\downloads")
ARTIFACT_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\artifacts")
WORKTREE_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\worktrees")
V48_DOWNLOAD_ROOT = DOWNLOAD_ARCHIVE_ROOT / "v48-omega"
V48_ARTIFACT_ROOT = ARTIFACT_ARCHIVE_ROOT / "v48-omega"
V48_CLEANUP_BACKUP_ROOT = V48_ARTIFACT_ROOT / "cleanup-backups"
LOCAL_RUNTIME_DIR = ROOT / ".local-runtime" / "v48"
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
GLOBAL_CODEX_HOME = Path(r"C:\Users\hamis\.codex")
GLOBAL_CODEX_CONFIG = GLOBAL_CODEX_HOME / "config.toml"
ADVISORY_SOURCE = Path(
    r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v41 (Aletheon - Orun - Gemini - Vesper Ion - Kai - Ari - Kimiclaw Family).txt"
)
WSL_EXE_PATH = Path(r"C:\Windows\System32\wsl.exe")
UBUNTU_EXE_PATH = Path(r"C:\Users\hamis\AppData\Local\Microsoft\WindowsApps\ubuntu.exe")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_text(value: str) -> str:
    return str(value or "").replace("\x00", "").replace("\ufeff", "")


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def resolve_command(preferred: str) -> list[str]:
    candidates = [preferred]
    if not preferred.lower().endswith(".cmd"):
        candidates.insert(0, f"{preferred}.cmd")
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    return [preferred]


def safe_run(args: list[str], *, cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(
            [*resolve_command(args[0]), *args[1:]],
            cwd=cwd or ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        proc.stdout = clean_text(proc.stdout)
        proc.stderr = clean_text(proc.stderr)
        return proc
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=clean_text(stdout),
            stderr=(clean_text(stderr) + f"\ncommand timed out after {timeout} seconds").strip(),
        )
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))


def excerpt(value: str, limit: int = 4000) -> str:
    text = clean_text(value)
    return text[-limit:] if len(text) > limit else text


def git_head(cwd: Path = ROOT) -> str:
    return safe_run(["git", "-C", str(cwd), "rev-parse", "HEAD"], timeout=30).stdout.strip()


def git_branch(cwd: Path = ROOT) -> str:
    return safe_run(["git", "-C", str(cwd), "rev-parse", "--abbrev-ref", "HEAD"], timeout=30).stdout.strip()


def git_status_lines(cwd: Path = ROOT) -> list[str]:
    proc = safe_run(["git", "-C", str(cwd), "status", "--short"], timeout=180)
    return [line.rstrip() for line in proc.stdout.splitlines() if line.strip()]


def git_tracked(rel_path: str, cwd: Path = ROOT) -> bool:
    return safe_run(["git", "-C", str(cwd), "ls-files", "--error-unmatch", rel_path], timeout=30).returncode == 0


def dir_size_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                total += item.stat().st_size
        except OSError:
            continue
    return total


def ensure_archive_roots() -> None:
    for path in (V48_DOWNLOAD_ROOT, V48_ARTIFACT_ROOT, V48_CLEANUP_BACKUP_ROOT, LOCAL_RUNTIME_DIR, TRACE_DIR):
        path.mkdir(parents=True, exist_ok=True)
