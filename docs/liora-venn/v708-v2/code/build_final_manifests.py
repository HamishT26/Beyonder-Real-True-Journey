#!/usr/bin/env python3
"""Build the exact final staged review, delta manifest, and complete owner manifest."""

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
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, encoding="utf-8", check=False)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def entry(repo: Path, relative: str) -> dict[str, object]:
    raw = (repo / relative).read_bytes()
    return {"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--phase-root", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--source-content", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    phase = args.phase_root.replace("\\", "/")
    review_rel = f"{phase}/validation/final-staged-review.json"
    delta_rel = f"{phase}/validation/final-delta-manifest.json"
    owner_rel = f"{phase}/validation/final-owner-manifest.json"
    exclusions = {review_rel, delta_rel, owner_rel}

    tracked = git_paths(repo, "diff", "--name-only", args.parent, "--", phase)
    untracked = git_paths(repo, "ls-files", "--others", "--exclude-standard", "--", phase)
    material = sorted(path for path in set(tracked + untracked) if path not in exclusions and (repo / path).is_file())
    declared = sorted(material + list(exclusions))
    write_json(
        repo / review_rel,
        {
            "schema": "liora.final-staged-review.v708-v2.v1",
            "stage": "final",
            "parent": args.parent,
            "declared_paths": declared,
            "declared_count": len(declared),
            "path_scope": phase,
            "outside_owner_scope_allowed": False,
            "status": "PRECOMMIT_DECLARATION",
        },
    )

    delta_entries = [entry(repo, path) for path in sorted(material + [review_rel])]
    write_json(
        repo / delta_rel,
        {
            "schema": "liora.final-delta-manifest.v708-v2.v1",
            "stage": "final",
            "parent": args.parent,
            "source_content": args.source_content,
            "byte_domain": "raw Git blob with LF-authored owner files",
            "self_excluded": [delta_rel, owner_rel],
            "entries": delta_entries,
            "entry_count": len(delta_entries),
        },
    )

    owner_files = sorted(
        path.relative_to(repo).as_posix()
        for path in (repo / phase).rglob("*")
        if path.is_file() and path.relative_to(repo).as_posix() != owner_rel
    )
    owner_entries = [entry(repo, path) for path in owner_files]
    write_json(
        repo / owner_rel,
        {
            "schema": "liora.final-owner-manifest.v708-v2.v1",
            "source_content": args.source_content,
            "owner_base": "2f86f76169acfe9d9376b4400720434fa246ee7a",
            "byte_domain": "raw Git blob with LF-authored owner files",
            "self_excluded": owner_rel,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
        },
    )
    print(json.dumps({"declared":len(declared),"delta_entries":len(delta_entries),"owner_entries":len(owner_entries)},sort_keys=True))


if __name__ == "__main__":
    main()
