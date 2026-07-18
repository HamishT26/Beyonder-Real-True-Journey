#!/usr/bin/env python3
"""Build or verify the exact Sylven v648-v8 owner manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = "docs/sylven-arc/v648-v8"
PHASE = ROOT / PHASE_REL
MANIFEST_REL = f"{PHASE_REL}/validation/final-owner-manifest.json"
EXCLUSIONS = {
    MANIFEST_REL,
    f"{PHASE_REL}/validation/final-staged-manifest.json",
    f"{PHASE_REL}/validation/final-staged-privacy.json",
    f"{PHASE_REL}/validation/final-staged-review.json",
}


def run(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def paths(revision: str | None = None) -> list[str]:
    if revision:
        output = str(run("ls-tree", "-r", "--name-only", revision, f"{PHASE_REL}/"))
    else:
        output = str(run("ls-files", f"{PHASE_REL}/"))
    return sorted(line for line in output.splitlines() if line)


def data(spec: str) -> bytes:
    value = run("show", spec, binary=True)
    assert isinstance(value, bytes)
    return value


def build() -> dict:
    owner_paths = paths()
    entries = []
    for path in owner_paths:
        if path in EXCLUSIONS:
            continue
        oid = str(run("rev-parse", f":{path}"))
        checkout = (ROOT / path).read_bytes()
        entries.append({"path":path,"git_blob":oid,"checkout_bytes":len(checkout),"checkout_sha256":hashlib.sha256(checkout).hexdigest()})
    covered = {row["path"] for row in entries} | (EXCLUSIONS & set(owner_paths))
    return {"schema":"ghc.family.v648-v8.final-owner-manifest.v1","hash_domain":"exact_git_index_blob","checkout_domain":"working_tree_after_checkout_filters","entries":entries,"entry_count":len(entries),"declared_self_exclusions":sorted(EXCLUSIONS),"owner_path_count":len(owner_paths),"covered_path_count":len(covered),"coverage_complete":covered == set(owner_paths)}


def check(revision: str) -> list[str]:
    payload = json.loads((PHASE / "validation/final-owner-manifest.json").read_text(encoding="utf-8"))
    owner_paths = set(paths(revision))
    entries = {row["path"]:row for row in payload["entries"]}
    issues: list[str] = []
    if set(entries) | (set(payload["declared_self_exclusions"]) & owner_paths) != owner_paths:
        issues.append("owner manifest coverage mismatch")
    current = str(run("rev-parse", "HEAD")) == revision
    for path, row in entries.items():
        if str(run("rev-parse", f"{revision}:{path}")) != row["git_blob"]:
            issues.append(f"git blob mismatch: {path}")
        if current:
            checkout = (ROOT / path).read_bytes()
            if len(checkout) != row["checkout_bytes"] or hashlib.sha256(checkout).hexdigest() != row["checkout_sha256"]:
                issues.append(f"checkout mismatch: {path}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-revision")
    args = parser.parse_args()
    if args.write:
        payload = build()
        target = PHASE / "validation/final-owner-manifest.json"
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({"entries":payload["entry_count"],"owner_paths":payload["owner_path_count"],"coverage":payload["coverage_complete"]}, sort_keys=True))
        return 0 if payload["coverage_complete"] else 1
    if args.check_revision:
        issues = check(args.check_revision)
        print(json.dumps({"revision":args.check_revision,"issues":issues,"result":"pass" if not issues else "fail"}, sort_keys=True))
        return 0 if not issues else 1
    parser.error("choose --write or --check-revision")


if __name__ == "__main__":
    raise SystemExit(main())
