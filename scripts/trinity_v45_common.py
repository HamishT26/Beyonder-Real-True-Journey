#!/usr/bin/env python3
"""Shared helpers for the V45 Omega PowerShell-first slot 40 gate lane."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
AUTHORITATIVE_REPO = Path(r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey")
NON_AUTHORITATIVE_WORKBENCH = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
STALE_LOCAL_MAIN_WORKTREE = AUTHORITATIVE_REPO
SOURCE_BRANCH = "origin/codex/GHC-Family/beyonder-shared-omega-line"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v45-omega-exec"
WORKTREE_BASELINE_SHA = "4b8387c32f10adf541057e604ff803b93748a720"
WORKTREE_BASELINE_STATE = "origin_4b8387c3"

DOWNLOAD_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\downloads")
ARTIFACT_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\artifacts")
WORKTREE_ARCHIVE_ROOT = Path(r"D:\GHC-Archives\worktrees")
V45_DOWNLOAD_ROOT = DOWNLOAD_ARCHIVE_ROOT / "v45-omega"
V45_ARTIFACT_ROOT = ARTIFACT_ARCHIVE_ROOT / "v45-omega"

TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
LOCAL_RUNTIME_DIR = ROOT / ".local-runtime" / "v45"
GLOBAL_CODEX_HOME = Path(r"C:\Users\hamis\.codex")
GLOBAL_CODEX_CONFIG = GLOBAL_CODEX_HOME / "config.toml"
GLOBAL_CODEX_SKILLS = GLOBAL_CODEX_HOME / "skills"
GLOBAL_CODEX_AUTH = GLOBAL_CODEX_HOME / "auth.json"
GLOBAL_CODEX_BACKUPS = GLOBAL_CODEX_HOME / "backups" / "v45"
AUTOMATIONS_DIR = GLOBAL_CODEX_HOME / "automations"
REPO_CODEX_CONFIG = ROOT / ".codex" / "config.toml"
DEFAULT_DOWNLOAD_SOURCE_DIR = Path(r"C:\Users\hamis\Downloads")
WSL_EXE_PATH = Path(r"C:\Windows\System32\wsl.exe")
UBUNTU_EXE_PATH = Path(r"C:\Users\hamis\AppData\Local\Microsoft\WindowsApps\ubuntu.exe")
STATUS_VALUES = {"PASS", "WARN", "FAIL", "TIMEOUT"}


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
    if hasattr(value, "to_dict"):
        try:
            return to_jsonable(value.to_dict())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return to_jsonable(vars(value))
        except Exception:
            pass
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_head() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return clean_text(proc.stdout).strip()


def git_branch() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return clean_text(proc.stdout).strip()


def git_status_lines() -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--short"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return [line.rstrip() for line in clean_text(proc.stdout).splitlines() if line.strip()]


def git_tracked(rel_path: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", rel_path],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return proc.returncode == 0


def normalized_status(value: object) -> str:
    return str(value or "").strip().upper()


def resolve_status(payload: dict[str, Any]) -> str:
    if not payload:
        return "MISSING"
    for key in ("overall_status", "status"):
        text = normalized_status(payload.get(key))
        if text in STATUS_VALUES:
            return text
    result = normalized_status(payload.get("result"))
    if result in STATUS_VALUES:
        return result
    if payload.get("effective_success") is True or payload.get("promotion_gate_ready") is True:
        return "PASS"
    if payload.get("blockers"):
        return "WARN"
    return "MISSING"


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def resolve_command(preferred: str) -> list[str]:
    candidates = [preferred]
    if not preferred.lower().endswith(".cmd"):
        candidates.insert(0, f"{preferred}.cmd")
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    return [preferred]


def safe_run(
    args: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(
            [*resolve_command(args[0]), *args[1:]],
            cwd=cwd or ROOT,
            env=env,
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
