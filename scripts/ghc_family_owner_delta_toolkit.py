#!/usr/bin/env python3
"""Bounded validation tools for one owner's exact source-to-final Git delta.

The toolkit deliberately avoids repository-wide discovery, sibling worktree
enumeration, and unchanged-history execution.  Every file operation is derived
from an exact Git range or an explicit literal allowlist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA = "ghc.family.owner-delta-toolkit.v1"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
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
    "recursive_delete": re.compile(r"(?i)(?:rm\s+-rf|Remove-Item\b[^\n]*-Recurse)"),
}
REMOTE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class DeltaError(RuntimeError):
    """Raised when an exact-delta contract is violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_relative(raw: str) -> str:
    candidate = raw.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", candidate):
        raise DeltaError(f"absolute drive path rejected: {raw}")
    path = PurePosixPath(candidate)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise DeltaError(f"non-literal repository-relative path rejected: {raw}")
    return path.as_posix()


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


def blob_at(repo: Path, commit: str, relative_path: str) -> bytes:
    path = normalize_relative(relative_path)
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise DeltaError(f"unable to read exact blob {path} at {commit}")
    return result.stdout


def manifest_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    source_id = resolve_commit(repo, source)
    target_id = resolve_commit(repo, target)
    entries: list[dict[str, Any]] = []
    for row in delta_rows(repo, source_id, target_id):
        entry = dict(row)
        if row["status"].startswith("D"):
            entry.update({"bytes": 0, "sha256": None, "git_blob": None, "mode": None})
        else:
            content = blob_at(repo, target_id, row["path"])
            tree_line = run_git(repo, "ls-tree", target_id, "--", row["path"]).stdout.strip()
            if not tree_line:
                raise DeltaError(f"missing target tree entry for {row['path']}")
            metadata, observed_path = tree_line.split("\t", 1)
            mode, object_type, git_blob = metadata.split()
            if normalize_relative(observed_path) != row["path"] or object_type != "blob":
                raise DeltaError(f"unexpected tree entry for {row['path']}")
            entry.update(
                {
                    "bytes": len(content),
                    "sha256": sha256_bytes(content),
                    "git_blob": git_blob,
                    "mode": mode,
                }
            )
        entries.append(entry)
    return {
        "schema": f"{SCHEMA}.manifest",
        "generated_at_utc": utc_now(),
        "source_commit": source_id,
        "target_commit": target_id,
        "entry_count": len(entries),
        "entries": entries,
        "scope": "exact source-to-target owner delta only",
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
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DeltaError(f"JSON parse failed for {path}: {exc}") from exc
        records.append({"path": path, "bytes": len(raw), "top_level_type": type(parsed).__name__})
    return {
        "schema": f"{SCHEMA}.json",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "parsed_count": len(records),
        "records": records,
        "valid": True,
    }


def markdown_payload(repo: Path, source: str, target: str) -> dict[str, Any]:
    target_id = resolve_commit(repo, target)
    records = []
    for path in exact_paths(repo, source, target, ".md"):
        text = blob_at(repo, target_id, path).decode("utf-8")
        if not text.strip():
            raise DeltaError(f"empty Markdown file: {path}")
        records.append(
            {
                "path": path,
                "words": len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)),
                "headings": len(re.findall(r"(?m)^#{1,6}\s+", text)),
            }
        )
    return {
        "schema": f"{SCHEMA}.markdown",
        "source_commit": resolve_commit(repo, source),
        "target_commit": target_id,
        "checked_count": len(records),
        "records": records,
        "valid": True,
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


def route_payload(roster_path: Path, auth_path: Path) -> dict[str, Any]:
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    auth = json.loads(auth_path.read_text(encoding="utf-8"))
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
    if current.get("current", {}).get("owner") != "Neris Solane":
        issues.append("current owner is not Neris Solane")
    if current.get("next", {}).get("owner") != "Vesper Arlen":
        issues.append("next owner is not Vesper Arlen")
    return {
        "schema": f"{SCHEMA}.route",
        "active_main_task_count": len(active),
        "standby": [row.get("relational_name") for row in roster.get("standby_members", [])],
        "current_owner": current.get("current", {}).get("owner"),
        "next_owner": current.get("next", {}).get("owner"),
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
        parsed = json.loads(path.read_text(encoding="utf-8"))
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


def run_exact_tests(repo: Path, modules: Iterable[str]) -> dict[str, Any]:
    normalized = ensure_unique((normalize_relative(value) for value in modules), "test module")
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
        records.append(
            {
                "module": module,
                "returncode": result.returncode,
                "output_sha256": sha256_bytes(result.stdout.encode("utf-8")),
                "output_tail": result.stdout.splitlines()[-8:],
            }
        )
        if result.returncode:
            raise DeltaError(f"selected test module failed: {module}")
    return {"module_count": len(records), "records": records, "valid": True}


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
    source = resolve_commit(repo, args.source)
    target = resolve_commit(repo, args.target)
    ancestry = run_git(repo, "rev-list", "--parents", f"{source}..{target}").stdout.splitlines()
    merge_count = sum(len(line.split()) > 2 for line in ancestry)
    if merge_count:
        raise DeltaError("merge commit detected in owner delta")
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
    file_budget = file_budget_payload(repo, source, target, args.threshold)
    route = route_payload(args.roster, args.auth)
    skills = skill_hash_payload(args.skill)
    quality = data_quality_payload(args.ledger)
    tests = run_exact_tests(repo, args.test_module)
    git_gate = clean_and_equal_payload(repo, target, args.branch, args.remote)
    valid = all(
        part.get("valid", False)
        for part in (json_check, markdown_check, python_check, privacy, security, file_budget, route, skills, quality, tests, git_gate)
    )
    payload = {
        "schema": f"{SCHEMA}.canonical",
        "invoked_at_utc": utc_now(),
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "execution_authority": "owner_self_scoped_delta",
        "owner": "Neris Solane",
        "source_commit": source,
        "x1_commit": x1,
        "target_commit": target,
        "commit_count": len(ancestry),
        "merge_count": merge_count,
        "manifest": manifest,
        "json": json_check,
        "markdown": markdown_check,
        "python": python_check,
        "privacy": privacy,
        "security": security,
        "file_budget": file_budget,
        "route": route,
        "skills": skills,
        "data_quality": quality,
        "tests": tests,
        "git_gate": git_gate,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One same-owner exact-delta software validation pass only; not a full-repository suite, independent reproduction, empirical or professional evidence, authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.",
    }
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
    for name in ("manifest", "json", "markdown", "python", "privacy"):
        add_range(commands.add_parser(name))
    route = commands.add_parser("route")
    route.add_argument("--roster", type=Path, required=True)
    route.add_argument("--auth", type=Path, required=True)
    route.add_argument("--output", type=Path)
    skills = commands.add_parser("skill-hashes")
    skills.add_argument("--skill", action="append", required=True)
    skills.add_argument("--output", type=Path)
    budget = commands.add_parser("file-budget")
    add_range(budget)
    budget.add_argument("--threshold", type=int, default=2000)
    quality = commands.add_parser("data-quality")
    quality.add_argument("--ledger", type=Path, action="append", required=True)
    quality.add_argument("--output", type=Path)
    canonical = commands.add_parser("canonical")
    canonical.add_argument("--repo", type=Path, required=True)
    canonical.add_argument("--source", required=True)
    canonical.add_argument("--x1", required=True)
    canonical.add_argument("--target", required=True)
    canonical.add_argument("--branch", required=True)
    canonical.add_argument("--remote", default="origin")
    canonical.add_argument("--threshold", type=int, default=2000)
    canonical.add_argument("--roster", type=Path, required=True)
    canonical.add_argument("--auth", type=Path, required=True)
    canonical.add_argument("--skill", action="append", required=True)
    canonical.add_argument("--ledger", type=Path, action="append", required=True)
    canonical.add_argument("--test-module", action="append", required=True)
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
        elif args.command == "route":
            payload = route_payload(args.roster, args.auth)
        elif args.command == "skill-hashes":
            payload = skill_hash_payload(args.skill)
        elif args.command == "file-budget":
            payload = file_budget_payload(args.repo, args.source, args.target, args.threshold)
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
