#!/usr/bin/env python3
"""Validate an explicit owner-local artifact allowlist without repository scans."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA = "ghc.family.owner-artifact-allowlist.v1"
MAX_ENTRIES = 128
PRIVACY_PATTERNS = {
    "raw_uuid": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
    "credential": re.compile(
        r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
        r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
        r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
    ),
    "private_route_key": re.compile(
        r"(?:thread_id|task_id|agent_id|subagent_path|private_callable|resume_token)",
        re.IGNORECASE,
    ),
    "transcript_or_session_stream": re.compile(
        r"(?:raw transcript|session stream|private app state)", re.IGNORECASE
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_relative_path(raw: str) -> PurePosixPath:
    if not raw or "\\" in raw:
        raise ValueError("artifact path must be a non-empty POSIX relative path")
    value = PurePosixPath(raw)
    if value.is_absolute() or ".." in value.parts:
        raise ValueError(f"unsafe artifact path: {raw}")
    return value


def under_root(root: Path, relative: PurePosixPath) -> Path:
    candidate = (root / Path(*relative.parts)).resolve()
    candidate.relative_to(root)
    return candidate


def validate_entry(root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    relative = safe_relative_path(str(entry.get("path", "")))
    full = under_root(root, relative)
    issues: list[str] = []
    if not full.is_file():
        return {
            "path": relative.as_posix(),
            "valid": False,
            "issues": ["exact file is absent"],
        }

    payload = full.read_bytes()
    text = payload.decode("utf-8")
    kind = entry.get("kind")
    parsed_schema: str | None = None
    if kind == "json":
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            issues.append(f"JSON parse failed at line {exc.lineno}")
        else:
            parsed_schema = parsed.get("schema") if isinstance(parsed, dict) else None
            expected_schema = entry.get("expected_schema")
            if expected_schema and parsed_schema != expected_schema:
                issues.append("JSON schema value differs from the allowlist")
    elif kind == "markdown":
        if not text.strip():
            issues.append("Markdown file is empty")
    elif kind == "python":
        try:
            ast.parse(text, filename=relative.as_posix())
        except SyntaxError as exc:
            issues.append(f"Python parse failed at line {exc.lineno}")
    else:
        issues.append("unsupported artifact kind")

    missing_tokens = [
        token for token in entry.get("required_tokens", []) if token not in text
    ]
    if missing_tokens:
        issues.append(f"missing required tokens: {missing_tokens}")

    privacy_hits = [
        label for label, pattern in PRIVACY_PATTERNS.items() if pattern.search(text)
    ]
    if privacy_hits:
        issues.extend(f"privacy pattern hit: {label}" for label in privacy_hits)

    return {
        "path": relative.as_posix(),
        "kind": kind,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "parsed_schema": parsed_schema,
        "privacy_hits": privacy_hits,
        "issues": issues,
        "valid": not issues,
    }


def validate(root: Path, allowlist: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if allowlist.get("schema") != SCHEMA:
        issues.append("allowlist schema mismatch")
    if allowlist.get("execution_authority") != "owner_local_only":
        issues.append("allowlist execution_authority must be owner_local_only")
    for key in ("repository_scan", "module_scan", "cross_lane_scan", "remote_scan"):
        if allowlist.get(key) is not False:
            issues.append(f"{key} must be false")

    entries = allowlist.get("entries")
    if not isinstance(entries, list) or not entries:
        issues.append("entries must be a non-empty list")
        entries = []
    if len(entries) > MAX_ENTRIES:
        issues.append(f"entry count exceeds {MAX_ENTRIES}")
    raw_paths = [str(row.get("path", "")) for row in entries]
    if len(raw_paths) != len(set(raw_paths)):
        issues.append("allowlist contains duplicate paths")

    results: list[dict[str, Any]] = []
    for entry in entries:
        try:
            results.append(validate_entry(root, entry))
        except (UnicodeDecodeError, ValueError) as exc:
            results.append(
                {
                    "path": str(entry.get("path", "")),
                    "valid": False,
                    "issues": [str(exc)],
                }
            )
    invalid = [row["path"] for row in results if not row.get("valid")]
    privacy_hit_count = sum(len(row.get("privacy_hits", [])) for row in results)
    return {
        "schema": "ghc.family.owner-artifact-validation.v1",
        "owner": allowlist.get("owner"),
        "phase": allowlist.get("phase"),
        "execution_authority": "owner_local_only",
        "repository_scan": False,
        "module_scan": False,
        "cross_lane_scan": False,
        "remote_scan": False,
        "directory_enumeration": False,
        "git_invocation": False,
        "test_body_execution": False,
        "allowlist_entries": len(entries),
        "validated_entries": len(results) - len(invalid),
        "invalid_entries": invalid,
        "privacy_hit_count": privacy_hit_count,
        "top_level_issues": issues,
        "results": results,
        "valid": not issues and not invalid and privacy_hit_count == 0,
        "terminal_state": "AWAITING_EIREN_VALIDATION",
        "boundary": (
            "Exact owner-local artifact parsing only. No repository, module, "
            "worktree, branch, remote, or sibling scan; no terminal validation, "
            "independent reproduction, authority, scientific proof, or Stage 20 credit."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    allowlist = load_json(args.allowlist)
    receipt = validate(root, allowlist)
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(rendered, encoding="utf-8", newline="\n")
    sys.stdout.write(
        json.dumps(
            {
                "valid": receipt["valid"],
                "allowlist_entries": receipt["allowlist_entries"],
                "privacy_hit_count": receipt["privacy_hit_count"],
                "terminal_state": receipt["terminal_state"],
            },
            sort_keys=True,
        )
        + "\n"
    )
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
