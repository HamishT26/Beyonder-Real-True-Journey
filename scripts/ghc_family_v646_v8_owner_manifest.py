#!/usr/bin/env python3
"""Build or check exact Git-index/Git-blob owner-manifest coverage for v646-v8."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = "docs/ilyra-fen/v646-v8"
PHASE = ROOT / PHASE_REL
MANIFEST_REL = f"{PHASE_REL}/validation/final-owner-manifest.json"
EXCLUSIONS = {
    MANIFEST_REL,
    f"{PHASE_REL}/validation/final-staged-manifest.json",
    f"{PHASE_REL}/validation/final-staged-review.json",
}


def index_paths() -> list[str]:
    output = subprocess.check_output(["git", "ls-files", f"{PHASE_REL}/"], cwd=ROOT, text=True, encoding="utf-8")
    return sorted(line for line in output.splitlines() if line)


def blob(revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)


def build() -> dict:
    paths = index_paths()
    entries = [{"path": path, "sha256": hashlib.sha256(blob("", path)).hexdigest()} for path in paths if path not in EXCLUSIONS]
    return {
        "schema": "ghc.family.v646-v8.final-owner-manifest.v1",
        "hash_domain": "git_index_blob",
        "entries": entries,
        "entry_count": len(entries),
        "declared_self_exclusions": sorted(EXCLUSIONS),
        "owner_path_count": len(paths),
        "covered_path_count": len(entries) + len(EXCLUSIONS & set(paths)),
        "coverage_complete": set(paths) - {row["path"] for row in entries} == EXCLUSIONS & set(paths),
    }


def check(revision: str) -> list[str]:
    payload = json.loads((PHASE / "validation/final-owner-manifest.json").read_text(encoding="utf-8"))
    output = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", revision, f"{PHASE_REL}/"], cwd=ROOT, text=True, encoding="utf-8")
    paths = {line for line in output.splitlines() if line}
    issues = []
    entry_paths = {row["path"] for row in payload["entries"]}
    if paths - entry_paths != set(payload["declared_self_exclusions"]) & paths:
        issues.append("owner manifest coverage mismatch")
    for row in payload["entries"]:
        actual = hashlib.sha256(blob(revision, row["path"])).hexdigest()
        if actual != row["sha256"]:
            issues.append(f"manifest mismatch: {row['path']}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-revision")
    args = parser.parse_args()
    if args.write:
        payload = build()
        path = PHASE / "validation/final-owner-manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({"entries": payload["entry_count"], "owner_paths": payload["owner_path_count"], "coverage": payload["coverage_complete"], "result": "pass" if payload["coverage_complete"] else "fail"}))
        return 0 if payload["coverage_complete"] else 1
    if args.check_revision:
        issues = check(args.check_revision)
        print(json.dumps({"revision": args.check_revision, "issues": issues, "result": "pass" if not issues else "fail"}))
        return 0 if not issues else 1
    parser.error("choose --write or --check-revision")


if __name__ == "__main__":
    raise SystemExit(main())
