#!/usr/bin/env python3
"""Shared bounded runtime for Sylven Arc v645-v8 family tools."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_v645_v8_definitions import TRUTH_BOUNDARY


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v645-v8"


def read_json(relative: str | Path) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd or ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    return {
        "returncode": result.returncode,
        "stdout_present": bool(result.stdout.strip()),
        "stderr_present": bool(result.stderr.strip()),
    }


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def owner_files() -> list[Path]:
    files = phase_files()
    files.extend(sorted((ROOT / "scripts").glob("*v645_v8*.py")))
    files.extend(sorted((ROOT / "tests").glob("*v645_v8*.py")))
    return sorted(set(files))


PRIVATE_PATTERNS = {
    "raw_uuid_identifier": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.I,
    ),
    "private_route_or_callable": re.compile(
        "(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)",
        re.I,
    ),
    "credential_or_secret_material": re.compile(
        "(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})",
        re.I,
    ),
    "private_absolute_local_path": re.compile(
        "(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)",
        re.I,
    ),
    "private_session_artifact": re.compile(
        "(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))",
        re.I,
    ),
}


def privacy_scan(paths: list[Path] | None = None) -> dict[str, Any]:
    paths = paths or owner_files()
    candidates: list[dict[str, str | int]] = []
    hits: list[dict[str, str | int]] = []
    decoded = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": "invalid_utf8"})
            continue
        decoded += 1
        relative = path.relative_to(ROOT).as_posix()
        for label, pattern in PRIVATE_PATTERNS.items():
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                line = text.splitlines()[line_number - 1]
                scanner_definition = (
                    relative == "scripts/ghc_family_v645_v8_x1_review.py"
                    and label in line
                    and "re.compile" in line
                )
                candidate = {
                    "path": relative,
                    "pattern_class": label,
                    "line": line_number,
                    "context": "scanner_definition" if scanner_definition else "content",
                }
                candidates.append(candidate)
                if not scanner_definition:
                    hits.append(candidate)
    return {
        "schema": "ghc.family.v645-v8.privacy-scan.v1",
        "files_scanned": len(paths),
        "utf8_decoded": decoded,
        "pattern_classes": sorted(PRIVATE_PATTERNS),
        "pattern_class_count": len(PRIVATE_PATTERNS),
        "candidate_hits": candidates,
        "candidate_count": len(candidates),
        "hits": hits,
        "hit_count": len(hits),
        "valid": not hits,
        "boundary": "Five structural classes are screened. Zero hits is not privacy-complete assurance.",
    }


def parse_json_documents(paths: list[Path] | None = None) -> dict[str, Any]:
    paths = paths or sorted(PHASE.rglob("*.json"))
    failures: list[dict[str, str]] = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # receipt records only the error class
            failures.append(
                {"path": path.relative_to(ROOT).as_posix(), "error_class": type(exc).__name__}
            )
    return {
        "documents": len(paths),
        "failures": failures,
        "valid": not failures,
        "boundary": TRUTH_BOUNDARY,
    }
