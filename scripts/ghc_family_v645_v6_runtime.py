#!/usr/bin/env python3
"""Shared bounded runtime for the Orin Thale v645-v6 phase runners."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v645-v6"
TRUTH_BOUNDARY = (
    "Bounded same-owner software and synthetic evidence only; no empirical confirmation, participant "
    "effectiveness, professional authority, production identity assurance, legal or cultural authority, "
    "Māori authority, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, "
    "consciousness or personhood, Theory of Everything, deployment, or Stage 20 readiness."
)


def read_json(relative: str | Path) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(command: list[str], cwd: Path | None = None) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd or ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
    "private_uri": re.compile(r"\b(?:" + "app" + "|" + "plugin" + ")" + "://", re.I),
    "private_markup": re.compile(r"<(?:" + "codex_" + "delegation" + "|" + "source_" + "thread_id" + ")>", re.I),
    "private_callable": re.compile(r"\b(?:" + "thread" + "Id" + "|" + "callable_" + "id" + "|" + "session_" + "stream" + r")\b", re.I),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
}


def privacy_scan(paths: list[Path] | None = None) -> dict[str, Any]:
    paths = paths or phase_files()
    hits: list[dict[str, str]] = []
    decoded = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": "invalid_utf8"})
            continue
        decoded += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    return {
        "schema": "ghc.family.v645-v6.privacy-scan.v1",
        "files_scanned": len(paths),
        "utf8_decoded": decoded,
        "pattern_classes": sorted(PRIVATE_PATTERNS),
        "hits": hits,
        "hit_count": len(hits),
        "valid": not hits,
        "boundary": "A zero-hit structural scan is not a privacy-complete assurance claim.",
    }


def parse_json_documents(paths: list[Path] | None = None) -> dict[str, Any]:
    paths = paths or sorted(PHASE.rglob("*.json"))
    failures = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append({"path": path.relative_to(ROOT).as_posix(), "error_class": type(exc).__name__})
    return {"documents": len(paths), "failures": failures, "valid": not failures}
