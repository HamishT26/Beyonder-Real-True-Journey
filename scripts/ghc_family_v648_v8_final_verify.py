#!/usr/bin/env python3
"""Read-only exact-head verifier for Sylven v648-v8 commit-local manifests and history."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"
SOURCE = "33c8f87a4037c81c3abca540b8c5db1d91328420"
X1 = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"
EVIDENCE = "1e85a9e714ac2509095fac03aedf704b4892d8b3"
MANIFEST_PATHS = {
    "x1": "docs/sylven-arc/v648-v8/validation/x1-staged-manifest.json",
    "evidence": "docs/sylven-arc/v648-v8/validation/evidence-staged-manifest.json",
    "closeout": "docs/sylven-arc/v648-v8/validation/final-staged-manifest.json",
    "final": "docs/sylven-arc/v648-v8/validation/final-staged-manifest.json",
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def manifest_receipt(stage: str, commit: str) -> dict:
    manifest = json.loads(git("show", f"{commit}:{MANIFEST_PATHS[stage]}"))
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    actual = set(filter(None, git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()))
    mismatches = [row["path"] for row in manifest["entries"] if git("rev-parse", f"{commit}:{row['path']}") != row["git_blob"]]
    return {"stage":stage,"commit":commit,"entries":len(manifest["entries"]),"self_exclusions":len(manifest["self_exclusions"]),"path_parity":expected == actual,"blob_mismatches":mismatches}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", default="HEAD")
    parser.add_argument("--closeout")
    args = parser.parse_args()
    final = git("rev-parse", args.final)
    anchors = [("x1", X1), ("evidence", EVIDENCE)]
    if args.closeout:
        closeout = git("rev-parse", args.closeout)
        anchors.append(("closeout", closeout))
    anchors.append(("final", final))
    receipts = [manifest_receipt(stage, commit) for stage, commit in anchors]
    issues = []
    for row in receipts:
        if not row["path_parity"] or row["blob_mismatches"]:
            issues.append(f"manifest failure: {row['stage']}")
    for anchor in [SOURCE, X1, EVIDENCE]:
        if subprocess.run(["git", "merge-base", "--is-ancestor", anchor, final], cwd=ROOT).returncode:
            issues.append(f"non-ancestral anchor: {anchor}")
    parent_values = git("show", "-s", "--format=%P", final).split()
    expected_commits = 4 if args.closeout else 3
    expected_parent = git("rev-parse", args.closeout) if args.closeout else EVIDENCE
    if len(parent_values) != 1 or parent_values[0] != expected_parent:
        issues.append("final parent mismatch")
    if int(git("rev-list", "--count", f"{SOURCE}..{final}")) != expected_commits:
        issues.append("phase commit count mismatch")
    if int(git("rev-list", "--merges", "--count", f"{SOURCE}..{final}")) != 0:
        issues.append("merge count mismatch")
    json_files = sorted(PHASE.rglob("*.json"))
    if final == git("rev-parse", "HEAD"):
        for path in json_files:
            json.loads(path.read_text(encoding="utf-8"))
    payload = {"schema":"ghc.family.v648-v8.exact-final-readonly.external.v1","final":final,"closeout":git("rev-parse", args.closeout) if args.closeout else final,"commit_local_manifests":receipts,"json_parses":len(json_files),"source_to_final_commits":int(git("rev-list", "--count", f"{SOURCE}..{final}")),"source_to_final_merges":int(git("rev-list", "--merges", "--count", f"{SOURCE}..{final}")),"final_parent_count":len(parent_values),"final_parent":parent_values[0] if parent_values else None,"issues":issues,"passed":not issues,"tests_rerun":False,"privacy_scan_rerun":False,"replay":False}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
