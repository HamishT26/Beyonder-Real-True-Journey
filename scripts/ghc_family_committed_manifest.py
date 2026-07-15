#!/usr/bin/env python3
"""Build a reusable SHA-256 manifest from a Git commit or staged index."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str, text: bool = False) -> bytes | str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
    return result.stdout.decode("utf-8").strip() if text else result.stdout


def target_paths(repo: Path, target: str, roots: list[str]) -> list[str]:
    if target == "INDEX":
        raw = git(repo, "ls-files", "-z", "--", *roots)
        assert isinstance(raw, bytes)
        return sorted({item.decode("utf-8") for item in raw.split(b"\0") if item})
    raw = git(repo, "ls-tree", "-r", "-z", "--name-only", target, "--", *roots)
    assert isinstance(raw, bytes)
    return sorted({item.decode("utf-8") for item in raw.split(b"\0") if item})


def blob(repo: Path, target: str, relative: str) -> bytes:
    value = f":{relative}" if target == "INDEX" else f"{target}:{relative}"
    data = git(repo, "show", value)
    assert isinstance(data, bytes)
    return data


def build(repo: Path, target: str, roots: list[str], output_rel: str) -> dict:
    paths = [path for path in target_paths(repo, target, roots) if path != output_rel]
    entries = []
    for relative in paths:
        data = blob(repo, target, relative)
        entries.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    resolved = "INDEX" if target == "INDEX" else str(git(repo, "rev-parse", target, text=True))
    return {
        "schema": "ghc.family.committed-manifest.v1",
        "target": resolved,
        "target_kind": "staged_index" if target == "INDEX" else "commit",
        "hash_domain": "exact Git blob bytes",
        "roots": roots,
        "excluded_self": output_rel,
        "entry_count": len(entries),
        "entries": entries,
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "boundary": "This exact Git-blob manifest is change-detection evidence, not a signature, exhaustive security review, or independent reproduction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--target", default="HEAD", help="Commit-ish or INDEX")
    parser.add_argument("--root", action="append", required=True, dest="roots")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    payload = build(repo, args.target, args.roots, args.output)
    output = repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"target": payload["target"], "entries": payload["entry_count"], "output": args.output}))


if __name__ == "__main__":
    main()
