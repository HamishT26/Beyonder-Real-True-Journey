#!/usr/bin/env python3
"""Build an additive local lean companion from the recent GHC active surface."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def recent_paths(repo: Path, baseline: str) -> set[str]:
    output = run(["git", "diff", "--name-only", baseline, "--"], repo).stdout
    selected = {line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()}
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"], repo).stdout
    selected.update(
        line.strip().replace("\\", "/")
        for line in untracked.splitlines()
        if line.strip()
    )
    phase_root = repo / "docs/eiren-kestrel/v644-v5"
    if phase_root.is_dir():
        selected.update(
            path.relative_to(repo).as_posix()
            for path in phase_root.rglob("*")
            if path.is_file()
        )
    for pattern in ["scripts/*v644_v5*.py", "tests/*v644_v5*.py"]:
        selected.update(
            path.relative_to(repo).as_posix()
            for path in repo.glob(pattern)
            if path.is_file()
        )
    method_wrapper = repo / "scripts/ghc_family_method_flow_state.py"
    if method_wrapper.is_file():
        selected.add(method_wrapper.relative_to(repo).as_posix())
    for fixed in [".gitattributes", ".gitignore", "tests/__init__.py"]:
        if (repo / fixed).is_file():
            selected.add(fixed)
    return {rel for rel in selected if (repo / rel).is_file()}


def local_python_dependencies(repo: Path, selected: set[str]) -> set[str]:
    added: set[str] = set()
    for rel in list(selected):
        path = repo / rel
        if path.suffix != ".py":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
        for module in modules:
            for candidate in [f"scripts/{module}.py", f"tests/{module}.py", f"{module}.py"]:
                if (repo / candidate).is_file():
                    added.add(candidate)
    return added


def path_references(repo: Path, selected: set[str]) -> set[str]:
    references: set[str] = set()

    def walk(value: object) -> Iterable[str]:
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                yield from walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                yield from walk(item)

    for rel in list(selected):
        path = repo / rel
        if path.suffix != ".json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for value in walk(data):
            normalized = value.replace("\\", "/")
            if normalized.startswith("docs/eiren-kestrel/v644-v5/") and (repo / normalized).is_file():
                references.add(normalized)
    return references


def close_dependencies(repo: Path, selected: set[str]) -> set[str]:
    while True:
        expanded = selected | local_python_dependencies(repo, selected) | path_references(repo, selected)
        if expanded == selected:
            return selected
        selected = expanded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--file-limit", type=int, default=15000)
    args = parser.parse_args()

    repo = args.repo.resolve()
    destination = args.destination.resolve()
    if destination.exists():
        raise SystemExit("destination already exists; choose a fresh additive companion path")
    source_head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    if source_head != args.source_revision:
        raise SystemExit(f"expected source revision {args.source_revision}, found {source_head}")

    selected = close_dependencies(repo, recent_paths(repo, args.baseline))
    if not selected:
        raise SystemExit("no recent active files selected")
    if len(selected) >= args.file_limit:
        raise SystemExit(f"selected file count {len(selected)} meets or exceeds limit {args.file_limit}")

    destination.mkdir(parents=True)
    entries = []
    for rel in sorted(selected):
        source = repo / rel
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entries.append(
            {
                "path": rel,
                "sha256": sha256(target),
                "bytes": target.stat().st_size,
            }
        )

    run(["git", "init", "-b", "main"], destination)
    run(["git", "config", "user.name", "GHC Family Lean Companion"], destination)
    run(["git", "config", "user.email", "noreply@example.invalid"], destination)
    run(["git", "add", "."], destination)
    run(["git", "commit", "-m", "Initialize bounded GHC active-surface companion"], destination)
    companion_head = run(["git", "rev-parse", "HEAD"], destination).stdout.strip()
    companion_status = run(["git", "status", "--porcelain"], destination).stdout.splitlines()
    tracked = run(["git", "ls-files"], destination).stdout.splitlines()

    test_result = run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_v644_v5_x1",
            "tests.test_ghc_family_v644_v5.TestV644V5Models",
        ],
        destination,
        check=False,
    )
    payload = {
        "schema": "ghc.family.v644-v5.lean-companion-validation.v1",
        "source_revision": source_head,
        "baseline_revision": args.baseline,
        "storage_class": "D-first additive local companion",
        "public_remote_configured": False,
        "canonical_repository_replaced": False,
        "canonical_history_preserved": True,
        "snapshot_only_history": True,
        "dependency_closure_method": [
            "recent baseline-to-working-tree changed paths",
            "current untracked owner-generated paths",
            "complete current-phase artifact root and phase-specific scripts/tests",
            "local Python import closure",
            "current-phase-only JSON path-reference closure",
            "fixed Git attributes, ignore rules, and tests package marker",
        ],
        "file_limit": args.file_limit,
        "selected_file_count": len(entries),
        "tracked_file_count": len(tracked),
        "under_limit": len(tracked) < args.file_limit,
        "entries": entries,
        "local_companion_head": companion_head,
        "clean": not companion_status,
        "targeted_test_returncode": test_result.returncode,
        "targeted_test_passed": test_result.returncode == 0,
        "targeted_test_scope": [
            "tests.test_ghc_family_v644_v5_x1",
            "tests.test_ghc_family_v644_v5.TestV644V5Models",
        ],
        "same_owner_only": True,
        "independent_reproduction": False,
        "rollback": "Discard or ignore only the additive companion and continue from the unchanged canonical repository.",
        "public_cutover_gate": "A public remote name, consumer compatibility, successor ancestry policy, and exact authorization remain required.",
        "valid": (
            len(entries) == len(tracked)
            and len(tracked) < args.file_limit
            and not companion_status
            and test_result.returncode == 0
        ),
        "boundary": "This proves a bounded local active-surface companion and targeted same-owner replay. It is not a full-history clone, canonical cutover, complete dependency proof, security certification, or independent reproduction.",
    }
    write_json(args.manifest_output, payload)
    print(
        json.dumps(
            {
                "valid": payload["valid"],
                "selected_file_count": payload["selected_file_count"],
                "tracked_file_count": payload["tracked_file_count"],
                "targeted_test_returncode": payload["targeted_test_returncode"],
                "clean": payload["clean"],
                "public_remote_configured": False,
            }
        )
    )
    raise SystemExit(0 if payload["valid"] else 1)


if __name__ == "__main__":
    main()
