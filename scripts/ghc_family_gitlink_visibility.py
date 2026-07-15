#!/usr/bin/env python3
"""Classify Git gitlinks and nested-repository visibility without fetching or mutation."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


def safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value.replace("\\", "/"))
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def classify_entry(
    *, mode: str, path: str, declared: bool, worktree_present: bool, nested_git_marker: bool
) -> dict[str, Any]:
    contained = safe_relative_path(path)
    if not contained:
        classification = "rejected_out_of_root"
    elif mode == "160000" and declared and worktree_present:
        classification = "declared_initialized_gitlink"
    elif mode == "160000" and declared:
        classification = "declared_deinitialized_gitlink"
    elif mode == "160000":
        classification = "undeclared_gitlink"
    elif nested_git_marker:
        classification = "undeclared_nested_repository"
    else:
        classification = "ordinary_tracked_entry"
    accepted = classification in {
        "declared_initialized_gitlink",
        "declared_deinitialized_gitlink",
        "ordinary_tracked_entry",
    }
    return {
        "path": path,
        "mode": mode,
        "declared": declared,
        "worktree_present": worktree_present,
        "nested_git_marker": nested_git_marker,
        "root_contained": contained,
        "classification": classification,
        "accepted": accepted,
        "network_fetch_performed": False,
    }


def _git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git exited {result.returncode}")
    return result.stdout


def declared_submodule_paths(repo: Path) -> set[str]:
    modules = repo / ".gitmodules"
    if not modules.is_file():
        return set()
    output = _git(repo, "config", "-f", str(modules), "--get-regexp", r"^submodule\..*\.path$", check=False)
    paths: set[str] = set()
    for line in output.splitlines():
        fields = line.split(maxsplit=1)
        if len(fields) == 2 and safe_relative_path(fields[1]):
            paths.add(fields[1].replace("\\", "/"))
    return paths


def scan_repository(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    declared = declared_submodule_paths(repo)
    rows: list[dict[str, Any]] = []
    for line in _git(repo, "ls-files", "--stage").splitlines():
        metadata, path = line.split("\t", 1)
        mode = metadata.split()[0]
        if mode != "160000":
            continue
        normalized = path.replace("\\", "/")
        worktree = repo / Path(normalized)
        rows.append(
            classify_entry(
                mode=mode,
                path=normalized,
                declared=normalized in declared,
                worktree_present=worktree.exists(),
                nested_git_marker=(worktree / ".git").exists() if worktree.is_dir() else False,
            )
        )
    declared_without_gitlink = sorted(declared - {row["path"] for row in rows})
    return {
        "schema": "ghc.family.gitlink-visibility.v1",
        "repository_scope": "current Git index and declared submodule paths",
        "gitlink_count": len(rows),
        "declared_submodule_count": len(declared),
        "declared_without_gitlink": declared_without_gitlink,
        "entries": rows,
        "network_fetch_performed": False,
        "repository_mutation_performed": False,
        "valid": not declared_without_gitlink and all(row["root_contained"] for row in rows),
        "boundary": "This read-only classifier detects declared index visibility states. It does not recurse into arbitrary untracked trees, fetch remotes, establish exhaustive repository integrity, or authorize mutation.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = scan_repository(args.repo)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
