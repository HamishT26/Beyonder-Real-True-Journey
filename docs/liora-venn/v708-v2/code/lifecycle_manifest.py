#!/usr/bin/env python3
"""Create a deterministic owner-stage staged review and raw-byte manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def git_paths(repo: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--phase-root", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--source-content", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--staged-review", required=True)
    args = parser.parse_args()

    repo = Path(args.repo)
    phase_root = repo / args.phase_root
    manifest_path = repo / args.manifest
    review_path = repo / args.staged_review
    excluded = {args.manifest.replace("\\", "/"), args.staged_review.replace("\\", "/")}
    tracked_delta = git_paths(repo, "diff", "--name-only", args.parent, "--", args.phase_root)
    untracked_delta = git_paths(repo, "ls-files", "--others", "--exclude-standard", "--", args.phase_root)
    planned = sorted(
        path
        for path in set(tracked_delta + untracked_delta)
        if path not in excluded and (repo / path).is_file()
    )
    declared = sorted(planned + sorted(excluded))
    write_json(review_path, {
        "schema": "liora.staged-review.v708-v2.v1",
        "stage": args.stage,
        "declared_paths": declared,
        "declared_count": len(declared),
        "self_excluded": args.staged_review,
        "path_scope": args.phase_root,
        "outside_owner_scope_allowed": False,
        "status": "PRECOMMIT_DECLARATION",
    })
    entries = []
    for relative in declared:
        if relative == args.manifest.replace("\\", "/"):
            continue
        path = repo / relative
        raw = path.read_bytes()
        entries.append({
            "path": relative,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    write_json(manifest_path, {
        "schema": "liora.lifecycle-manifest.v708-v2.v1",
        "stage": args.stage,
        "parent": args.parent,
        "source_content": args.source_content,
        "byte_domain": "raw Git blob with LF-authored owner files",
        "self_excluded": args.manifest,
        "entries": entries,
        "entry_count": len(entries),
    })


if __name__ == "__main__":
    main()
