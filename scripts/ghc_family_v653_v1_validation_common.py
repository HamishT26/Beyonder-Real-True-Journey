#!/usr/bin/env python3
"""Shared bounded validation helpers for Vesper Arlen v653-v1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/vesper-arlen/v653-v1"
PHASE_PREFIX = "docs/vesper-arlen/v653-v1/"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY_PATTERNS = {
    "credentials": [
        re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"(?i)(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"),
    ],
    "raw_task_or_private_route": [
        re.compile(r"thread://[0-9a-fA-F-]{20,}"),
        re.compile(r"<source_thread_id>"),
        re.compile(r"(?i)(?:private[_-]?route|callable[_-]?id)\s*[:=]\s*['\"][^'\"]+"),
    ],
    "private_local_path": [
        re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)\bD:[\\/]+GHC-Archives[\\/]+"),
        re.compile(r"(?i)\bfile://"),
    ],
    "conversation_or_session_stream": [
        re.compile(r"<codex_delegation>"),
        re.compile(r"(?i)session[_-]?stream\s*[:=]"),
        re.compile(r"(?i)['\"]role['\"]\s*:\s*['\"](?:user|assistant|system)['\"]"),
    ],
    "screenshot_or_embedded_binary": [
        re.compile(r"(?i)data:image/[a-z0-9.+-]+;base64,"),
        re.compile(r"(?i)(?:screenshot|image)[_-]?path\s*[:=]\s*['\"][^'\"]+"),
        re.compile(r"(?i)['\"]image_url['\"]\s*:\s*['\"]data:"),
    ],
}
SCANNER_DEFINITION_FILES = {
    "scripts/ghc_family_v653_v1_validation_common.py",
    "scripts/ghc_family_v653_v1_staged_review.py",
    "scripts/ghc_family_v653_v1_x1_validate.py",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*args: str, input_bytes: bytes | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        input=input_bytes,
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8").strip()


def staged_blob_map(paths: Iterable[str]) -> dict[str, str]:
    wanted = set(paths)
    result: dict[str, str] = {}
    for row in git("ls-files", "-s").splitlines():
        metadata, path = row.split("\t", 1)
        _mode, object_id, stage = metadata.split()
        if stage == "0" and path in wanted:
            result[path] = object_id
    missing = sorted(wanted - set(result))
    if missing:
        raise RuntimeError(f"staged blob map missing paths: {missing}")
    return result


def revision_blob_map(paths: Iterable[str], revision: str = "HEAD") -> dict[str, str]:
    ordered = list(paths)
    if not ordered:
        return {}
    result = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype)"],
        cwd=REPO,
        input=("\n".join(f"{revision}:{path}" for path in ordered) + "\n").encode("utf-8"),
        check=True,
        capture_output=True,
    )
    rows = result.stdout.decode("utf-8").splitlines()
    if len(rows) != len(ordered):
        raise RuntimeError("revision blob response count mismatch")
    mapping: dict[str, str] = {}
    for path, row in zip(ordered, rows, strict=True):
        parts = row.split()
        if len(parts) != 2 or parts[1] != "blob":
            raise RuntimeError(f"expected committed blob for {path}: {row}")
        mapping[path] = parts[0]
    return mapping


def batch_blob_bytes(object_ids: Iterable[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(object_ids))
    if not unique:
        return {}
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=("\n".join(unique) + "\n").encode("ascii"),
        check=True,
        capture_output=True,
    )
    output = result.stdout
    cursor = 0
    payloads: dict[str, bytes] = {}
    for requested in unique:
        header_end = output.index(b"\n", cursor)
        header = output[cursor:header_end].decode("ascii")
        actual, object_type, size_text = header.split()
        if object_type != "blob":
            raise RuntimeError(f"expected blob for {requested}, found {object_type}")
        size = int(size_text)
        start = header_end + 1
        end = start + size
        payloads[actual] = output[start:end]
        cursor = end + 1
    return payloads


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def phase_public_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (REPO / "scripts").glob("*v653_v1*.py")
        if path.is_file()
    )
    paths.extend(
        path
        for path in (REPO / "tests").glob("test_ghc_family_v653_v1*.py")
        if path.is_file()
    )
    runner_receipt = PHASE / "runners/runner-invocation-receipt.json"
    if runner_receipt.is_file():
        for row in read_json(runner_receipt)["runners"]:
            path = REPO / "scripts" / row["runner"]
            if path.is_file():
                paths.append(path)
    return sorted(set(paths))


def scan_privacy_bytes(rows: Iterable[tuple[str, bytes]]) -> dict[str, Any]:
    confirmed: list[dict[str, Any]] = []
    definition_hits: list[dict[str, Any]] = []
    files = 0
    for repository_relative, content in rows:
        files += 1
        text = content.decode("utf-8")
        for pattern_class, patterns in PRIVACY_PATTERNS.items():
            for pattern in patterns:
                matches = list(pattern.finditer(text))
                if not matches:
                    continue
                target = definition_hits if repository_relative in SCANNER_DEFINITION_FILES else confirmed
                target.append(
                    {
                        "path": repository_relative,
                        "pattern_class": pattern_class,
                        "match_count": len(matches),
                    }
                )
    return {
        "pattern_class_count": len(PRIVACY_PATTERNS),
        "files_scanned": files,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": sum(row["match_count"] for row in confirmed),
        "scanner_definition_hits": definition_hits,
        "scanner_definition_hit_count": sum(row["match_count"] for row in definition_hits),
        "valid": not confirmed,
    }


def scan_privacy_paths(paths: Iterable[Path]) -> dict[str, Any]:
    rows = [
        (path.relative_to(REPO).as_posix(), path.read_bytes())
        for path in sorted(set(paths))
    ]
    return scan_privacy_bytes(rows)
