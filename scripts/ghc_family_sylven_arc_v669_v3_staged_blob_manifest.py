"""Create an exact SHA-256 manifest from staged Git blob bytes."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str, binary: bool = False):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=not binary,
    ).stdout


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--lifecycle", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--forbid-prefix", action="append", default=[])
    parser.add_argument("--all-index", action="store_true")
    parser.add_argument("--include-glob", action="append", default=[])
    parser.add_argument("--exclude-path", action="append", default=[])
    args = parser.parse_args()
    repo = args.repo.resolve()
    manifest_rel = args.manifest.replace("\\", "/")
    review_rel = args.review.replace("\\", "/")
    if args.all_index:
        names = git(repo, "ls-files", "--cached").splitlines()
        if args.include_glob:
            names = [name for name in names if any(fnmatch.fnmatch(name, pattern) for pattern in args.include_glob)]
    else:
        names = git(repo, "diff", "--cached", "--name-only", args.base).splitlines()
    exclusions = {manifest_rel, review_rel, *(path.replace("\\", "/") for path in args.exclude_path)}
    names = [name.replace("\\", "/") for name in names if name.replace("\\", "/") not in exclusions]
    forbidden = [name for name in names if any(name.startswith(prefix) for prefix in args.forbid_prefix)]
    entries = []
    for name in names:
        blob = git(repo, "show", f":{name}", binary=True)
        entries.append({"path": name, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=repo, capture_output=True, text=True)
    manifest = {
        "schema": "ghc.family.git-blob-manifest.v2",
        "lifecycle": args.lifecycle,
        "domain": "exact_staged_git_blob_bytes",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(exclusions),
    }
    review = {
        "schema": "ghc.family.git-blob-staged-review.v2",
        "lifecycle": args.lifecycle,
        "staged_entry_count_before_self": len(names),
        "forbidden_prefixes": args.forbid_prefix,
        "forbidden_paths": forbidden,
        "diff_check_returncode": diff_check.returncode,
        "diff_check_output": diff_check.stdout + diff_check.stderr,
        "passed": not forbidden and diff_check.returncode == 0,
        "self_exclusions": sorted(exclusions),
    }
    write_json(repo / manifest_rel, manifest)
    write_json(repo / review_rel, review)
    if not review["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
