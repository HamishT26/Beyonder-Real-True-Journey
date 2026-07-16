#!/usr/bin/env python3
"""Read-only exact-head audit for canonical or named v646-v8 lanes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


SOURCE = "bb3a661e70f1cf9b92e5293b2f5292393bd9a60f"
X1 = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"
EVIDENCE = "64323516c35eddaa57c9be371eac327a24214a76"


def run(cwd: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, encoding="utf-8").strip()


def is_ancestor(cwd: Path, older: str, newer: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=cwd, check=False).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-branch", required=True)
    parser.add_argument("--expect-upstream", choices=["yes", "no"], required=True)
    args = parser.parse_args()
    cwd = args.repo.resolve()
    head = run(cwd, "rev-parse", "HEAD")
    branch = run(cwd, "branch", "--show-current")
    clean = run(cwd, "status", "--porcelain") == ""
    merges = int(run(cwd, "rev-list", "--merges", "--count", f"{SOURCE}..HEAD") or "0")
    commits = int(run(cwd, "rev-list", "--count", f"{SOURCE}..HEAD") or "0")
    parents = len(run(cwd, "show", "-s", "--format=%P", "HEAD").split())
    upstream_probe = subprocess.run(["git", "rev-parse", "@{upstream}"], cwd=cwd, text=True, encoding="utf-8", capture_output=True, check=False)
    checks = {
        "exact_head": head == args.expected_head,
        "expected_branch": branch == args.expected_branch,
        "clean": clean,
        "source_ancestor": is_ancestor(cwd, SOURCE, head),
        "x1_ancestor": is_ancestor(cwd, X1, head),
        "evidence_ancestor": is_ancestor(cwd, EVIDENCE, head),
        "three_phase_commits": commits == 3,
        "zero_merges": merges == 0,
        "single_parent": parents == 1,
        "upstream_expectation": (upstream_probe.returncode == 0) == (args.expect_upstream == "yes"),
    }
    payload = {"schema": "ghc.family.v646-v8.exact-head-audit.v1", "head": head, "branch": branch, "checks": checks, "check_count": len(checks), "issue_count": sum(not value for value in checks.values()), "result": "pass" if all(checks.values()) else "fail", "same_owner_only": True, "independent_reproduction": False}
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
