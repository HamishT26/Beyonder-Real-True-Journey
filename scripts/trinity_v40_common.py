#!/usr/bin/env python3
"""Shared helpers for the V40 Omega publication lanes."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
AUTHORITATIVE_REPO = r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey"
WORKBENCH_REPO = r"C:\Users\hamis\OneDrive\Documents\New project"
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"

STATUS_VALUES = {"PASS", "WARN", "FAIL", "TIMEOUT"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
    return (proc.stdout or "").strip()


def git_branch() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return (proc.stdout or "").strip()


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def normalized_status(value: object) -> str:
    text = str(value or "").strip().upper()
    return text


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
    if result == "SKIP":
        blockers = payload.get("blockers", [])
        desired = str(payload.get("desired_state") or "").strip().lower()
        actual = str(payload.get("actual_state") or "").strip().lower()
        if not blockers and desired and actual and desired == actual:
            return "PASS"
        return "WARN"

    if payload.get("effective_success") is True or payload.get("promotion_gate_ready") is True:
        return "PASS"
    if payload.get("blockers"):
        return "WARN"
    return "MISSING"


def parse_markdown_frontmatter(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter = parts[1]
    payload: dict[str, str] = {}
    for raw in frontmatter.splitlines():
        line = raw.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        payload[key.strip()] = value.strip().strip('"').strip("'")
    return payload


def read_markdown_key_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    payload = parse_markdown_frontmatter(path)
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        payload[key.strip(" `")] = value.strip().strip("`")
    return payload


def agent_truth_complete(agent: dict[str, Any]) -> bool:
    required = ("requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface")
    for field in required:
        value = agent.get(field)
        if field == "runtime_surface":
            if str(value or "").strip() not in {"app", "web", "CLI", "cloud"}:
                return False
            continue
        if not str(value or "").strip():
            return False
    return True


def env_snapshot() -> dict[str, str]:
    return {
        "CODEX_INTERNAL_ORIGINATOR_OVERRIDE": os.environ.get("CODEX_INTERNAL_ORIGINATOR_OVERRIDE", ""),
        "CODEX_THREAD_ID": os.environ.get("CODEX_THREAD_ID", ""),
    }
