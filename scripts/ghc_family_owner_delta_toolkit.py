#!/usr/bin/env python3
"""Bounded validation tools for one owner's exact source-to-final Git delta.

The toolkit deliberately avoids repository-wide discovery, sibling worktree
enumeration, and unchanged-history execution.  Every file operation is derived
from an exact Git range or an explicit literal allowlist.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from ast import parse as parse_python_ast
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlsplit


SCHEMA = "ghc.family.owner-delta-toolkit.v2"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
ALLOWED_BLOB_MODES = {"100644", "100755"}
DISALLOWED_BIDI = {
    "LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI",
}
UNSAFE_LINK_SCHEMES = {"app", "codex", "data", "file", "javascript", "vscode"}
PRIVATE_PATTERNS = {
    "private_absolute_path": re.compile(
        r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"
    ),
    "raw_uuid_or_task_identifier": re.compile(
        r"(?i)(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b|\"(?:task|thread|session|agent)_id\"\s*:)"
    ),
    "credential_or_private_key": re.compile(
        r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:\s*\"(?!\[REDACTED_SECRET\]))"
    ),
    "private_route": re.compile(
        r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"
    ),
    "raw_transcript_or_app_state": re.compile(
        r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"
    ),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(
        r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"
    ),
}
REMOTE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class DeltaError(RuntimeError):
    """Raised when an exact-delta contract is violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Return a deterministic UTF-8 JSON encoding for bounded receipt commitments."""
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise DeltaError(f"value is not canonically JSON encodable: {exc}") from exc
    return rendered.encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def canonical_owner(value: str) -> str:
    owner = value.strip()
    if not owner:
        raise DeltaError("canonical owner must be explicit")
    return owner


def strict_json_loads(raw: bytes | str, label: str = "JSON") -> Any:
    """Decode UTF-8 JSON while refusing duplicate object keys."""
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DeltaError(f"{label} is not UTF-8: {exc}") from exc
    else:
        text = raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        duplicates: list[str] = []
        for key, value in pairs:
            if key in result:
                duplicates.append(key)
            else:
                result[key] = value
        if duplicates:
            raise DeltaError(f"{label} contains duplicate object keys: {sorted(set(duplicates))}")
        return result

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except json.JSONDecodeError as exc:
        raise DeltaError(f"{label} parse failed: {exc}") from exc


def normalize_relative(raw: str) -> str:
    candidate = raw.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", candidate):
        raise DeltaError(f"absolute drive path rejected: {raw}")
    path = PurePosixPath(candidate)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise DeltaError(f"non-literal repository-relative path rejected: {raw}")
    return path.as_posix()


def path_security_record(raw: str) -> dict[str, Any]:
    path = normalize_relative(raw)
    nfc = unicodedata.normalize("NFC", path)
    disallowed: list[dict[str, str]] = []
    for character in path:
        category = unicodedata.category(character)
        bidi = unicodedata.bidirectional(character)
        if category == "Cc" or bidi in DISALLOWED_BIDI:
            disallowed.append(
                {
                    "codepoint": f"U+{ord(character):04X}",
                    "category": category,
                    "bidi": bidi or "NONE",
                }
            )
    return {
        "path": path,
        "nfc": nfc,
        "casefold_nfc": nfc.casefold(),
        "already_nfc": path == nfc,
        "disallowed_controls": disallowed,
        "valid": path == nfc and not disallowed,
    }


def audit_paths(paths: Iterable[str]) -> dict[str, Any]:
    records = [path_security_record(path) for path in ensure_unique(paths, "path-audit")]
    nfc_groups: dict[str, list[str]] = {}
    casefold_groups: dict[str, list[str]] = {}
    for record in records:
        nfc_groups.setdefault(record["nfc"], []).append(record["path"])
        casefold_groups.setdefault(record["casefold_nfc"], []).append(record["path"])
    nfc_collisions = [sorted(group) for group in nfc_groups.values() if len(group) > 1]
    casefold_collisions = [sorted(group) for group in casefold_groups.values() if len(group) > 1]
    issues = [record["path"] for record in records if not record["valid"]]
    return {
        "records": records,
        "nfc_collisions": sorted(nfc_collisions),
        "casefold_collisions": sorted(casefold_collisions),
        "invalid_paths": sorted(issues),
        "valid": not issues and not nfc_collisions and not casefold_collisions,
        "boundary": "Exact allowlist Unicode and collision review only; not exhaustive cross-platform path assurance.",
    }


def merkle_root(entries: Iterable[dict[str, Any]]) -> str:
    leaves: list[bytes] = []
    for entry in sorted(entries, key=lambda row: row["path"]):
        stable = {
            "path": entry["path"],
            "status": entry["status"],
            "mode": entry.get("mode"),
            "git_blob": entry.get("git_blob"),
            "sha256": entry.get("sha256"),
        }
        leaves.append(hashlib.sha256(b"\x00" + canonical_json_bytes(stable)).digest())
    if not leaves:
        return sha256_bytes(b"")
    level = leaves
    while len(level) > 1:
        if len(level) % 2:
            level = [*level, level[-1]]
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def ensure_unique(values: Iterable[str], label: str) -> list[str]:
    items = list(values)
    if len(items) != len(set(items)):
        raise DeltaError(f"duplicate {label} values rejected")
    return items


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", str(repo), *args]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and result.returncode:
        raise DeltaError(
            f"git command failed ({result.returncode}): {' '.join(args)}: {result.stderr.strip()}"
        )
    return result


def run_git_bytes(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise DeltaError(f"git command failed ({result.returncode}): {' '.join(args)}: {error}")
    return result


def resolve_commit(repo: Path, value: str) -> str:
    result = run_git(repo, "rev-parse", "--verify", "--end-of-options", f"{value}^{{commit}}")
    resolved = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", resolved):
        raise DeltaError(f"commit did not resolve to a full object id: {value}")
    return resolved


def parse_name_status_z(raw: bytes) -> list[dict[str, Any]]:
    """Parse Git's NUL-framed name-status stream without line ambiguity."""
    tokens = raw.split(b"\0")
    if not tokens or tokens[-1] != b"":
        raise DeltaError("NUL-delimited Git delta did not terminate cleanly")
    tokens.pop()
    rows: list[dict[str, Any]] = []
    index = 0
    while index < len(tokens):
        try:
            status = tokens[index].decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise DeltaError("non-ASCII Git delta status rejected") from exc
        index += 1
        path_count = 2 if status.startswith(("R", "C")) else 1
        if index + path_count > len(tokens):
            raise DeltaError(f"malformed NUL-delimited delta row: {status}")
        try:
            path_tokens = [token.decode("utf-8", errors="strict") for token in tokens[index:index + path_count]]
        except UnicodeDecodeError as exc:
            raise DeltaError(f"non-UTF-8 Git delta path rejected for status {status}") from exc
        index += path_count
        if status.startswith(("R", "C")):
            old_path = normalize_relative(path_tokens[0])
            path = normalize_relative(path_tokens[1])
        else:
            old_path = None
            path = normalize_relative(path_tokens[0])
        rows.append({"status": status, "path": path, "old_path": old_path})
    return rows


def delta_rows(repo: Path, source: str, target: str) -> list[dict[str, Any]]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    ancestor = run_git(repo, "merge-base", "--is-ancestor", source_id, target_id, check=False)
    if ancestor.returncode != 0:
        raise DeltaError("source is not an ancestor of target")
    raw = run_git_bytes(
        repo,
        "diff",
        "--name-status",
        "-z",
        "--find-renames",
        "--end-of-options",
        source_id,
        target_id,
    ).stdout
    rows = parse_name_status_z(raw)
    paths = [row["path"] for row in rows]
    ensure_unique(paths, "delta path")
    return rows


def tree_entry(repo: Path, commit: str, relative_path: str) -> dict[str, str] | None:
    path = normalize_relative(relative_path)
    raw = run_git_bytes(repo, "ls-tree", "-z", commit, "--", path).stdout
    if not raw:
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise DeltaError(f"ambiguous tree entry for {path}")
    try:
        metadata, observed_raw = records[0].split(b"\t", 1)
        mode_raw, type_raw, object_raw = metadata.split(b" ")
        observed = observed_raw.decode("utf-8", errors="strict")
        mode = mode_raw.decode("ascii", errors="strict")
        object_type = type_raw.decode("ascii", errors="strict")
        object_id = object_raw.decode("ascii", errors="strict")
    except (ValueError, UnicodeDecodeError) as exc:
        raise DeltaError(f"malformed tree entry for {path}") from exc
    if normalize_relative(observed) != path or not re.fullmatch(r"[0-9a-f]{40}", object_id):
        raise DeltaError(f"unexpected tree entry for {path}")
    return {"mode": mode, "object_type": object_type, "object_id": object_id}


def blob_object(repo: Path, object_id: str) -> bytes:
    if not re.fullmatch(r"[0-9a-f]{40}", object_id):
        raise DeltaError("invalid blob object id")
    result = run_git_bytes(repo, "cat-file", "blob", object_id)
    return result.stdout


def blob_at(repo: Path, commit: str, relative_path: str) -> bytes:
    entry = tree_entry(repo, commit, relative_path)
    if entry is None or entry["object_type"] != "blob":
        raise DeltaError(f"unable to read exact blob {relative_path} at {commit}")
    return blob_object(repo, entry["object_id"])


def manifest_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    entries: list[dict[str, Any]] = []
    for row in delta_rows(repo, source_id, target_id):
        entry = dict(row)
        prior_path = row["old_path"] or row["path"]
        old_entry = tree_entry(repo, source_id, prior_path)
        new_entry = tree_entry(repo, target_id, row["path"])
        if row["status"].startswith("D"):
            entry.update(
                {
                    "bytes": 0,
                    "sha256": None,
                    "git_blob": None,
                    "mode": None,
                    "object_type": None,
                    "old_mode": old_entry["mode"] if old_entry else None,
                    "old_object_type": old_entry["object_type"] if old_entry else None,
                }
            )
        else:
            if new_entry is None:
                raise DeltaError(f"missing target tree entry for {row['path']}")
            if new_entry["object_type"] != "blob" or new_entry["mode"] not in ALLOWED_BLOB_MODES:
                raise DeltaError(
                    f"unsupported target entry kind for {row['path']}: "
                    f"{new_entry['mode']} {new_entry['object_type']}"
                )
            content = blob_object(repo, new_entry["object_id"])
            entry.update(
                {
                    "bytes": len(content),
                    "sha256": sha256_bytes(content),
                    "git_blob": new_entry["object_id"],
                    "mode": new_entry["mode"],
                    "object_type": new_entry["object_type"],
                    "old_mode": old_entry["mode"] if old_entry else None,
                    "old_object_type": old_entry["object_type"] if old_entry else None,
                }
            )
        entries.append(entry)
    path_audit = audit_paths(row["path"] for row in entries)
    if not path_audit["valid"]:
        raise DeltaError("exact delta contains a Unicode, control-character, or collision path issue")
    stable_commitment = {
        "source_commit": source_id,
        "target_commit": target_id,
        "entries": entries,
    }
    return {
        "schema": f"{SCHEMA}.manifest",
        "generated_at_utc": utc_now(),
        "source_commit": source_id,
        "target_commit": target_id,
        "entry_count": len(entries),
        "entries": entries,
        "path_audit": path_audit,
        "merkle_root_sha256": merkle_root(entries),
        "canonical_commitment_sha256": canonical_json_sha256(stable_commitment),
        "scope": "exact source-to-target owner delta only",
        "valid": True,
    }


def write_json(path: Path | None, payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8", newline="\n")


def write_json_exclusive(path: Path, payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if os.name == "nt":
            import ctypes
            import msvcrt
            from ctypes import wintypes

            create_file = ctypes.WinDLL("kernel32", use_last_error=True).CreateFileW
            create_file.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE,
            ]
            create_file.restype = wintypes.HANDLE
            handle_value = create_file(
                os.path.abspath(path),
                0x40000000,
                0,
                None,
                1,
                0x00000080 | 0x00200000,
                None,
            )
            invalid_handle = wintypes.HANDLE(-1).value
            if handle_value == invalid_handle:
                error = ctypes.get_last_error()
                if error in {80, 183}:
                    raise FileExistsError(error, "exclusive receipt path already exists", str(path))
                raise OSError(error, "unable to create exclusive receipt", str(path))
            try:
                descriptor = msvcrt.open_osfhandle(handle_value, os.O_WRONLY | getattr(os, "O_BINARY", 0))
            except Exception:
                ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle(handle_value)
                raise
        else:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
    except FileExistsError as exc:
        raise DeltaError("canonical receipt already exists; aggregate replay is forbidden") from exc


def exact_paths(repo: Path, source: str, target: str, suffix: str | None = None) -> list[str]:
    rows = delta_rows(repo, source, target)
    paths = [row["path"] for row in rows if not row["status"].startswith("D")]
    if suffix:
        paths = [path for path in paths if path.lower().endswith(suffix.lower())]
    return paths


def json_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".json"):
        raw = blob_at(repo, target_id, path)
        try:
            parsed = strict_json_loads(raw, path)
        except DeltaError as exc:
            raise DeltaError(f"JSON parse failed for {path}: {exc}") from exc
        records.append(
            {
                "path": path,
                "bytes": len(raw),
                "top_level_type": type(parsed).__name__,
                "canonical_sha256": canonical_json_sha256(parsed),
                "duplicate_keys": 0,
            }
        )
    return {
        "schema": f"{SCHEMA}.json",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "parsed_count": len(records),
        "records": records,
        "valid": True,
    }


def markdown_target_records(repo: Path, target: str, path: str, text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
        raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(raw_target)
        scheme = parsed.scheme.lower()
        issue: str | None = None
        resolved_path: str | None = None
        if scheme in UNSAFE_LINK_SCHEMES:
            issue = f"unsafe scheme: {scheme}"
        elif scheme and scheme not in {"http", "https", "mailto"}:
            issue = f"unreviewed scheme: {scheme}"
        elif not scheme and not raw_target.startswith("#"):
            candidate = parsed.path.replace("\\", "/")
            if re.match(r"^[A-Za-z]:", candidate) or candidate.startswith("/"):
                issue = "absolute local target"
            elif candidate:
                parent = PurePosixPath(path).parent
                parts: list[str] = []
                for part in (parent / candidate).parts:
                    if part in {"", "."}:
                        continue
                    if part == "..":
                        if not parts:
                            issue = "target escapes repository root"
                            break
                        parts.pop()
                    else:
                        parts.append(part)
                if issue is None:
                    resolved_path = normalize_relative(PurePosixPath(*parts).as_posix())
                    if tree_entry(repo, target, resolved_path) is None:
                        issue = "missing committed local target"
        records.append(
            {
                "target": raw_target,
                "scheme": scheme or "relative",
                "resolved_path": resolved_path,
                "issue": issue,
                "valid": issue is None,
            }
        )
    return records


def markdown_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".md"):
        try:
            text = blob_at(repo, target_id, path).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DeltaError(f"Markdown is not UTF-8: {path}") from exc
        if not text.strip():
            raise DeltaError(f"empty Markdown file: {path}")
        targets = markdown_target_records(repo, target_id, path, text)
        records.append(
            {
                "path": path,
                "words": len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)),
                "headings": len(re.findall(r"(?m)^#{1,6}\s+", text)),
                "target_count": len(targets),
                "target_issues": [record for record in targets if not record["valid"]],
            }
        )
    issues = [
        {"path": record["path"], **target}
        for record in records
        for target in record["target_issues"]
    ]
    return {
        "schema": f"{SCHEMA}.markdown",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "checked_count": len(records),
        "records": records,
        "target_issue_count": len(issues),
        "target_issues": issues,
        "valid": not issues,
        "boundary": "Structural exact-delta Markdown target review only; not complete accessibility or external-link safety assurance.",
    }


def python_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".py"):
        raw = blob_at(repo, target_id, path)
        try:
            source_text = raw.decode("utf-8")
            compile(source_text, path, "exec", dont_inherit=True)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise DeltaError(f"Python compile failed for {path}: {exc}") from exc
        records.append({"path": path, "bytes": len(raw), "sha256": sha256_bytes(raw)})
    return {
        "schema": f"{SCHEMA}.python",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "compiled_count": len(records),
        "records": records,
        "valid": True,
    }


def privacy_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    files = 0
    candidates: list[dict[str, str]] = []
    for path in exact_paths(repo, source, target):
        raw = blob_at(repo, target_id, path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        files += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": label})
    return {
        "schema": f"{SCHEMA}.privacy",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "classes": sorted(PRIVATE_PATTERNS),
        "scanned_text_files": files,
        "candidate_count": len(candidates),
        "confirmed_hits": candidates,
        "valid": not candidates,
        "boundary": "Five-class exact-delta pattern scan only; not complete privacy assurance.",
    }


def security_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    checked = 0
    findings: list[dict[str, str]] = []
    for path in exact_paths(repo, source, target, ".py"):
        checked += 1
        text = blob_at(repo, target_id, path).decode("utf-8")
        for label, pattern in SECURITY_PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": path, "rule": label, "severity": "review"})
    return {
        "schema": f"{SCHEMA}.security",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "checked_python_files": checked,
        "finding_count": len(findings),
        "findings": findings,
        "valid": not findings,
        "boundary": "Bounded exact-delta static pattern review only; not exhaustive security assurance.",
    }


def path_audit_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    result = audit_paths(row["path"] for row in delta_rows(repo, source_id, target_id))
    return {
        "schema": f"{SCHEMA}.path-audit",
        "source_commit": source_id,
        "target_commit": target_id,
        **result,
    }


def route_payload(
    roster_path: Path,
    auth_path: Path,
    expected_current_owner: str,
    expected_next_owner: str,
) -> dict[str, Any]:
    if not expected_current_owner.strip() or not expected_next_owner.strip():
        raise DeltaError("expected current and next owners must be explicit")
    roster = strict_json_loads(roster_path.read_bytes(), roster_path.name)
    auth = strict_json_loads(auth_path.read_bytes(), auth_path.name)
    execution = roster.get("validation_scope", {}).get("execution_authority", {})
    auth_execution = auth.get("validation_scope", {}).get("execution_authority", {})
    active = roster.get("active_main_tasks", [])
    repeat = roster.get("live_route_override", {}).get("repeat_cycle", [])
    current = roster.get("current_route", {})
    issues: list[str] = []
    if active != repeat or len(active) != 15:
        issues.append("active and repeat cycle must contain the same fifteen main tasks")
    if roster.get("standby_members", [{}])[0].get("relational_name") != "Tavian Sol":
        issues.append("Tavian Sol standby record missing")
    if execution.get("policy") != "owner_self_scoped_delta" or execution != auth_execution:
        issues.append("roster and authorization validation policies differ")
    if current.get("current", {}).get("owner") != expected_current_owner:
        issues.append(f"current owner is not {expected_current_owner}")
    if current.get("next", {}).get("owner") != expected_next_owner:
        issues.append(f"next owner is not {expected_next_owner}")
    return {
        "schema": f"{SCHEMA}.route",
        "active_main_task_count": len(active),
        "standby": [row.get("relational_name") for row in roster.get("standby_members", [])],
        "current_owner": current.get("current", {}).get("owner"),
        "next_owner": current.get("next", {}).get("owner"),
        "expected_current_owner": expected_current_owner,
        "expected_next_owner": expected_next_owner,
        "validation_policy": execution.get("policy"),
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
    }


def parse_label_path(values: Iterable[str]) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    labels: list[str] = []
    for value in values:
        if "=" not in value:
            raise DeltaError("skill mapping must be LABEL=PATH")
        label, raw_path = value.split("=", 1)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", label):
            raise DeltaError(f"invalid sanitized skill label: {label}")
        path = Path(raw_path)
        if not path.is_file():
            raise DeltaError(f"skill file missing for {label}")
        labels.append(label)
        pairs.append((label, path))
    ensure_unique(labels, "skill label")
    return pairs


def skill_hash_payload(values: Iterable[str]) -> dict[str, Any]:
    records = []
    for label, path in parse_label_path(values):
        raw = path.read_bytes()
        records.append({"label": label, "bytes": len(raw), "sha256": sha256_bytes(raw)})
    return {
        "schema": f"{SCHEMA}.skill-hashes",
        "skill_count": len(records),
        "records": records,
        "paths_sanitized": True,
        "valid": True,
    }


def materialized_paths(repo: Path) -> list[str]:
    paths: list[str] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [directory for directory in dirs if directory != ".git" and directory != "__pycache__"]
        root_path = Path(root)
        for filename in files:
            candidate = root_path / filename
            paths.append(candidate.relative_to(repo).as_posix())
    return sorted(paths)


def file_budget_payload(repo: Path, source: str, target: str, threshold: int) -> dict[str, Any]:
    if threshold != 2000:
        raise DeltaError("live materialized-file threshold must be exactly 2000")
    materialized = materialized_paths(repo)
    delta = exact_paths(repo, source, target)
    return {
        "schema": f"{SCHEMA}.file-budget",
        "source_commit": resolve_commit(repo, source),
        "target_commit": resolve_commit(repo, target),
        "materialized_file_count": len(materialized),
        "owner_delta_file_count": len(delta),
        "threshold": threshold,
        "rotation_required": len(materialized) >= threshold or len(delta) >= threshold,
        "sparse_before_checkout_required": True,
        "new_remote_repository": "pending_exact_action",
        "valid": len(materialized) < threshold and len(delta) < threshold,
    }


def sparse_payload(
    repo: Path,
    source: str,
    target: str,
    threshold: int,
    expected_patterns: Iterable[str],
) -> dict[str, Any]:
    expected = ensure_unique((value.strip() for value in expected_patterns), "sparse pattern")
    if not expected or any(not value for value in expected):
        raise DeltaError("at least one non-empty sparse pattern is required")
    observed = [
        line.strip()
        for line in run_git(repo, "sparse-checkout", "list").stdout.splitlines()
        if line.strip()
    ]
    budget = file_budget_payload(repo, source, target, threshold)
    issues: list[str] = []
    if observed != expected:
        issues.append("observed sparse patterns differ from the explicit expected order")
    if not budget["valid"]:
        issues.append("materialized or owner-delta file count reached the rotation threshold")
    return {
        "schema": f"{SCHEMA}.sparse",
        "source_commit": budget["source_commit"],
        "target_commit": budget["target_commit"],
        "expected_patterns": expected,
        "observed_patterns": observed,
        "patterns_match": observed == expected,
        "materialized_file_count": budget["materialized_file_count"],
        "owner_delta_file_count": budget["owner_delta_file_count"],
        "threshold": threshold,
        "rotation_required": budget["rotation_required"],
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Current owner worktree only; no sibling-lane inventory and no separate-remote authorization.",
    }


def baton_integrity_payload(
    repo: Path,
    source: str,
    target: str,
    path: str,
    expected_sha256: str,
    minimum_words: int,
    maximum_words: int,
) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    normalized = normalize_relative(path)
    if normalized not in exact_paths(repo, source_id, target_id):
        raise DeltaError("baton path is not present in the exact owner delta")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise DeltaError("expected baton SHA-256 must be a lowercase 64-hex digest")
    if minimum_words < 1 or maximum_words < minimum_words:
        raise DeltaError("invalid baton word range")
    entry = tree_entry(repo, target_id, normalized)
    if entry is None or entry["object_type"] != "blob" or entry["mode"] not in ALLOWED_BLOB_MODES:
        raise DeltaError("baton must be a regular committed Git blob")
    raw = blob_object(repo, entry["object_id"])
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DeltaError("baton is not UTF-8") from exc
    observed_sha256 = sha256_bytes(raw)
    word_count = len(re.findall(r"\S+", text, flags=re.UNICODE))
    issues: list[str] = []
    if observed_sha256 != expected_sha256:
        issues.append("baton SHA-256 differs from the expected digest")
    if not minimum_words <= word_count <= maximum_words:
        issues.append("baton word count is outside the declared range")
    return {
        "schema": f"{SCHEMA}.baton-integrity",
        "source_commit": source_id,
        "target_commit": target_id,
        "repository_relative_path": normalized,
        "git_blob": entry["object_id"],
        "bytes": len(raw),
        "sha256": observed_sha256,
        "expected_sha256": expected_sha256,
        "word_count": word_count,
        "minimum_words": minimum_words,
        "maximum_words": maximum_words,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Committed file integrity only; not delivery acknowledgement, authorship, authority, or independent reproduction.",
    }


def canonical_digest_payload(path: Path) -> dict[str, Any]:
    parsed = strict_json_loads(path.read_bytes(), path.name)
    return {
        "schema": f"{SCHEMA}.canonical-digest",
        "label": path.name,
        "canonical_sha256": canonical_json_sha256(parsed),
        "valid": True,
        "boundary": "Deterministic payload digest only; not a digital signature or trust anchor.",
    }


def collect_outcomes(value: Any, counts: Counter[str], unknown: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"outcome", "intended_outcome", "planning_state"} and isinstance(child, str):
                if child in ALLOWED_OUTCOMES:
                    counts[child] += 1
                else:
                    unknown.add(child)
            else:
                collect_outcomes(child, counts, unknown)
    elif isinstance(value, list):
        for child in value:
            collect_outcomes(child, counts, unknown)


def data_quality_payload(paths: Iterable[Path]) -> dict[str, Any]:
    files = list(paths)
    if not files:
        raise DeltaError("at least one ledger is required")
    counts: Counter[str] = Counter()
    unknown: set[str] = set()
    records = []
    for path in files:
        parsed = strict_json_loads(path.read_bytes(), path.name)
        local_counts: Counter[str] = Counter()
        local_unknown: set[str] = set()
        collect_outcomes(parsed, local_counts, local_unknown)
        counts.update(local_counts)
        unknown.update(local_unknown)
        records.append(
            {
                "label": path.name,
                "sha256": sha256_bytes(path.read_bytes()),
                "outcome_counts": dict(sorted(local_counts.items())),
                "unknown_labels": sorted(local_unknown),
            }
        )
    return {
        "schema": f"{SCHEMA}.data-quality",
        "ledger_count": len(files),
        "records": records,
        "outcome_counts": dict(sorted(counts.items())),
        "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
        "unknown_labels": sorted(unknown),
        "valid": not unknown,
        "boundary": "Structured ledger quality only; not evidence promotion.",
    }


def normalized_test_output(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", normalized)
    normalized = re.sub(r"(?i)[A-Z]:\\[^\n\r]+?\\Temp\\tmp[^\\\s:]+", "<temp>", normalized)
    normalized = re.sub(r"/(?:tmp|var/folders)/[^\s:]+", "<temp>", normalized)
    return normalized


def python_imports(path: Path) -> list[str]:
    try:
        tree = parse_python_ast(path.read_text(encoding="utf-8"), filename=str(path))
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise DeltaError(f"unable to inspect imports for {path.name}: {exc}") from exc
    imports: set[str] = set()
    for node in getattr(tree, "body", []):
        if node.__class__.__name__ == "Import":
            imports.update(alias.name for alias in node.names)
        elif node.__class__.__name__ == "ImportFrom" and node.module:
            imports.add(node.module)
    return sorted(imports)


def declared_repository_dependencies(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeError) as exc:
        raise DeltaError(f"unable to parse test dependency declaration: {path.name}") from exc
    declaration: Any = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name)
            and target.id == "DECLARED_REPOSITORY_DEPENDENCIES"
            for target in node.targets
        ):
            try:
                declaration = ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as exc:
                raise DeltaError("test dependency declaration must be a literal sequence") from exc
    if declaration is None:
        raise DeltaError(
            f"test module lacks DECLARED_REPOSITORY_DEPENDENCIES: {path.name}"
        )
    if not isinstance(declaration, (list, tuple)) or not all(
        isinstance(value, str) for value in declaration
    ):
        raise DeltaError("test dependency declaration must contain only paths")
    return ensure_unique(
        (normalize_relative(value) for value in declaration),
        f"declared repository dependency in {path.name}",
    )


def run_exact_tests(
    repo: Path,
    modules: Iterable[str],
    dependencies: Iterable[str] = (),
) -> dict[str, Any]:
    normalized = ensure_unique((normalize_relative(value) for value in modules), "test module")
    dependency_paths = ensure_unique(
        (normalize_relative(value) for value in dependencies), "test dependency"
    )
    dependency_records: list[dict[str, Any]] = []
    for dependency in dependency_paths:
        path = repo / Path(dependency)
        if not path.is_file():
            raise DeltaError(f"materialized test dependency missing: {dependency}")
        raw = path.read_bytes()
        dependency_records.append(
            {"path": dependency, "bytes": len(raw), "sha256": sha256_bytes(raw)}
        )
    records = []
    for module in normalized:
        module_path = PurePosixPath(module)
        if (
            not module.endswith(".py")
            or len(module_path.parts) < 2
            or module_path.parts[0] != "tests"
            or not module_path.name.startswith("test_")
        ):
            raise DeltaError(f"test module must be a tests/test_*.py file: {module}")
        path = repo / Path(module)
        if not path.is_file():
            raise DeltaError(f"materialized test module missing: {module}")
        declared_dependencies = declared_repository_dependencies(path)
        if declared_dependencies != dependency_paths:
            raise DeltaError(
                f"test dependency closure differs for {module}: "
                f"{declared_dependencies} != {dependency_paths}"
            )
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        stable_output = normalized_test_output(result.stdout)
        records.append(
            {
                "module": module,
                "returncode": result.returncode,
                "module_sha256": sha256_bytes(path.read_bytes()),
                "declared_imports": python_imports(path),
                "declared_repository_dependencies": declared_dependencies,
                "normalized_output_sha256": sha256_bytes(stable_output.encode("utf-8")),
                "output_tail": result.stdout.splitlines()[-8:],
            }
        )
        if result.returncode:
            raise DeltaError(f"selected test module failed: {module}")
    stable_contract = {
        "modules": [record["module"] for record in records],
        "dependencies": dependency_records,
        "results": [
            {
                "module": record["module"],
                "returncode": record["returncode"],
                "module_sha256": record["module_sha256"],
                "normalized_output_sha256": record["normalized_output_sha256"],
            }
            for record in records
        ],
    }
    return {
        "module_count": len(records),
        "dependency_count": len(dependency_records),
        "dependencies": dependency_records,
        "records": records,
        "contract_sha256": canonical_json_sha256(stable_contract),
        "valid": True,
    }


def validate_remote_name(repo: Path, remote: str) -> str:
    if not REMOTE_NAME.fullmatch(remote):
        raise DeltaError(f"invalid configured remote name rejected: {remote}")
    run_git(repo, "remote", "get-url", "--", remote)
    return remote


def validate_branch_name(repo: Path, branch: str) -> str:
    if not branch or branch.startswith("-"):
        raise DeltaError(f"option-like or empty branch name rejected: {branch}")
    result = run_git(repo, "check-ref-format", "--branch", branch, check=False)
    if result.returncode:
        raise DeltaError(f"invalid branch name rejected: {branch}")
    return branch


def clean_and_equal_payload(repo: Path, target: str, branch: str, remote: str) -> dict[str, Any]:
    branch = validate_branch_name(repo, branch)
    remote = validate_remote_name(repo, remote)
    target_id = resolve_commit(repo, target)
    head = resolve_commit(repo, "HEAD")
    current_branch = run_git(repo, "branch", "--show-current").stdout.strip()
    unstaged = run_git(repo, "diff", "--quiet", check=False).returncode
    staged = run_git(repo, "diff", "--cached", "--quiet", check=False).returncode
    untracked = [line for line in run_git(repo, "ls-files", "--others", "--exclude-standard").stdout.splitlines() if line]
    upstream = resolve_commit(repo, "@{u}")
    tracking = resolve_commit(repo, f"refs/remotes/{remote}/{branch}")
    live_result = run_git(repo, "ls-remote", "--heads", "--end-of-options", remote, f"refs/heads/{branch}")
    live_fields = live_result.stdout.strip().split()
    live = live_fields[0] if live_fields else None
    issues = []
    if head != target_id:
        issues.append("HEAD differs from target")
    if current_branch != branch:
        issues.append("current branch differs from expected branch")
    if unstaged or staged or untracked:
        issues.append("worktree is not clean")
    if len({target_id, head, upstream, tracking, live}) != 1:
        issues.append("local, upstream, tracking, and fresh-live commits differ")
    return {
        "target": target_id,
        "head": head,
        "branch_matches": current_branch == branch,
        "unstaged_changes": bool(unstaged),
        "staged_changes": bool(staged),
        "untracked_count": len(untracked),
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": len({target_id, head, upstream, tracking, live}) == 1,
        "issues": issues,
        "valid": not issues,
    }


def canonical_payload(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    owner = canonical_owner(args.owner)
    if args.commit_limit != 8:
        raise DeltaError("live phase commit limit must be exactly 8")
    source = resolve_commit(repo, args.source)
    target = resolve_commit(repo, args.target)
    ancestry = run_git(repo, "rev-list", "--parents", f"{source}..{target}").stdout.splitlines()
    merge_count = sum(len(line.split()) > 2 for line in ancestry)
    if merge_count:
        raise DeltaError("merge commit detected in owner delta")
    if len(ancestry) > args.commit_limit:
        raise DeltaError("owner delta exceeds the declared commit limit")
    if any(len(line.split()) != 2 for line in ancestry):
        raise DeltaError("owner delta contains a non-single-parent commit")
    x1 = resolve_commit(repo, args.x1)
    x1_parents = run_git(repo, "rev-list", "--parents", "-n", "1", x1).stdout.split()
    if len(x1_parents) != 2 or x1_parents[1] != source:
        raise DeltaError("x1 is not the direct child of source")
    manifest = manifest_payload(repo, source, target)
    json_check = json_payload(repo, source, target)
    markdown_check = markdown_payload(repo, source, target)
    python_check = python_payload(repo, source, target)
    privacy = privacy_payload(repo, source, target)
    security = security_payload(repo, source, target)
    path_audit = path_audit_payload(repo, source, target)
    file_budget = file_budget_payload(repo, source, target, args.threshold)
    sparse = sparse_payload(repo, source, target, args.threshold, args.sparse_pattern)
    route = route_payload(
        args.roster,
        args.auth,
        args.expected_current_owner,
        args.expected_next_owner,
    )
    skills = skill_hash_payload(args.skill)
    quality = data_quality_payload(args.ledger)
    tests = run_exact_tests(repo, args.test_module, args.test_dependency)
    baton = baton_integrity_payload(
        repo,
        source,
        target,
        args.baton_path,
        args.baton_sha256,
        args.baton_min_words,
        args.baton_max_words,
    )
    git_gate = clean_and_equal_payload(repo, target, args.branch, args.remote)
    valid = all(
        part.get("valid", False)
        for part in (
            manifest,
            json_check,
            markdown_check,
            python_check,
            privacy,
            security,
            path_audit,
            file_budget,
            sparse,
            route,
            skills,
            quality,
            tests,
            baton,
            git_gate,
        )
    )
    payload = {
        "schema": f"{SCHEMA}.canonical",
        "invoked_at_utc": utc_now(),
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "execution_authority": "owner_self_scoped_delta",
        "owner": owner,
        "source_commit": source,
        "x1_commit": x1,
        "target_commit": target,
        "commit_count": len(ancestry),
        "commit_limit": args.commit_limit,
        "merge_count": merge_count,
        "single_parent_history": True,
        "manifest": manifest,
        "json": json_check,
        "markdown": markdown_check,
        "python": python_check,
        "privacy": privacy,
        "security": security,
        "path_audit": path_audit,
        "file_budget": file_budget,
        "sparse": sparse,
        "route": route,
        "skills": skills,
        "data_quality": quality,
        "tests": tests,
        "baton": baton,
        "git_gate": git_gate,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One same-owner exact-delta software validation pass only; not a full-repository suite, independent reproduction, empirical or professional evidence, authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.",
    }
    payload["canonical_payload_sha256"] = canonical_json_sha256(
        {key: value for key, value in payload.items() if key not in {"invoked_at_utc"}}
    )
    write_json_exclusive(args.receipt, payload)
    return payload


def add_range(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("manifest", "json", "markdown", "python", "privacy", "security", "path-audit"):
        add_range(commands.add_parser(name))
    route = commands.add_parser("route")
    route.add_argument("--roster", type=Path, required=True)
    route.add_argument("--auth", type=Path, required=True)
    route.add_argument("--expected-current-owner", required=True)
    route.add_argument("--expected-next-owner", required=True)
    route.add_argument("--output", type=Path)
    skills = commands.add_parser("skill-hashes")
    skills.add_argument("--skill", action="append", required=True)
    skills.add_argument("--output", type=Path)
    budget = commands.add_parser("file-budget")
    add_range(budget)
    budget.add_argument("--threshold", type=int, default=2000)
    sparse = commands.add_parser("sparse")
    add_range(sparse)
    sparse.add_argument("--threshold", type=int, default=2000)
    sparse.add_argument("--expected-pattern", action="append", required=True)
    baton = commands.add_parser("baton-integrity")
    add_range(baton)
    baton.add_argument("--path", required=True)
    baton.add_argument("--expected-sha256", required=True)
    baton.add_argument("--minimum-words", type=int, default=10000)
    baton.add_argument("--maximum-words", type=int, default=100000)
    digest = commands.add_parser("canonical-digest")
    digest.add_argument("--json", type=Path, required=True)
    digest.add_argument("--output", type=Path)
    quality = commands.add_parser("data-quality")
    quality.add_argument("--ledger", type=Path, action="append", required=True)
    quality.add_argument("--output", type=Path)
    canonical = commands.add_parser("canonical")
    canonical.add_argument("--repo", type=Path, required=True)
    canonical.add_argument("--owner", required=True)
    canonical.add_argument("--source", required=True)
    canonical.add_argument("--x1", required=True)
    canonical.add_argument("--target", required=True)
    canonical.add_argument("--branch", required=True)
    canonical.add_argument("--remote", default="origin")
    canonical.add_argument("--threshold", type=int, default=2000)
    canonical.add_argument("--commit-limit", type=int, default=8)
    canonical.add_argument("--roster", type=Path, required=True)
    canonical.add_argument("--auth", type=Path, required=True)
    canonical.add_argument("--expected-current-owner", required=True)
    canonical.add_argument("--expected-next-owner", required=True)
    canonical.add_argument("--skill", action="append", required=True)
    canonical.add_argument("--ledger", type=Path, action="append", required=True)
    canonical.add_argument("--test-module", action="append", required=True)
    canonical.add_argument("--test-dependency", action="append", default=[])
    canonical.add_argument("--sparse-pattern", action="append", required=True)
    canonical.add_argument("--baton-path", required=True)
    canonical.add_argument("--baton-sha256", required=True)
    canonical.add_argument("--baton-min-words", type=int, default=10000)
    canonical.add_argument("--baton-max-words", type=int, default=100000)
    canonical.add_argument("--receipt", type=Path, required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "manifest":
            payload = manifest_payload(args.repo, args.source, args.target)
        elif args.command == "json":
            payload = json_payload(args.repo, args.source, args.target)
        elif args.command == "markdown":
            payload = markdown_payload(args.repo, args.source, args.target)
        elif args.command == "python":
            payload = python_payload(args.repo, args.source, args.target)
        elif args.command == "privacy":
            payload = privacy_payload(args.repo, args.source, args.target)
        elif args.command == "security":
            payload = security_payload(args.repo, args.source, args.target)
        elif args.command == "path-audit":
            payload = path_audit_payload(args.repo, args.source, args.target)
        elif args.command == "route":
            payload = route_payload(
                args.roster,
                args.auth,
                args.expected_current_owner,
                args.expected_next_owner,
            )
        elif args.command == "skill-hashes":
            payload = skill_hash_payload(args.skill)
        elif args.command == "file-budget":
            payload = file_budget_payload(args.repo, args.source, args.target, args.threshold)
        elif args.command == "sparse":
            payload = sparse_payload(
                args.repo,
                args.source,
                args.target,
                args.threshold,
                args.expected_pattern,
            )
        elif args.command == "baton-integrity":
            payload = baton_integrity_payload(
                args.repo,
                args.source,
                args.target,
                args.path,
                args.expected_sha256,
                args.minimum_words,
                args.maximum_words,
            )
        elif args.command == "canonical-digest":
            payload = canonical_digest_payload(args.json)
        elif args.command == "data-quality":
            payload = data_quality_payload(args.ledger)
        elif args.command == "canonical":
            payload = canonical_payload(args)
            sys.stdout.write(json.dumps({"valid": payload["valid"], "target": payload["target_commit"]}) + "\n")
            return 0 if payload["valid"] else 2
        else:
            raise DeltaError(f"unsupported command: {args.command}")
        write_json(getattr(args, "output", None), payload)
        return 0 if payload.get("valid", True) else 2
    except (DeltaError, OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"OWNER_DELTA_TOOLKIT_ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
