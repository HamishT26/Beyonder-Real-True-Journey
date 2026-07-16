#!/usr/bin/env python3
"""Audit exact-head ancestry and history for v647-v1 canonical or named lanes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


SOURCE = "d0d2b7617a84aeed94c425cdf83214f46ffeb24b"
X1 = "d120045b586665b507d3460b254158ec28e0baa6"
EVIDENCE = "24aa0005fe3286f89201026e18fd9bcdfed74c3f"


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=check, capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip()


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer], check=False).returncode == 0


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-branch", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--expect-upstream", choices=["yes", "no"], required=True)
    args = parser.parse_args()
    head = git(args.repo, "rev-parse", "HEAD")
    branch = git(args.repo, "branch", "--show-current")
    status = [row for row in git(args.repo, "status", "--porcelain=v1").splitlines() if row]
    commits = int(git(args.repo, "rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git(args.repo, "rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parent_count = len(git(args.repo, "rev-list", "--parents", "-n", "1", head).split()) - 1
    upstream_probe = subprocess.run(["git", "-C", str(args.repo), "rev-parse", "@{u}"], check=False, capture_output=True, text=True, encoding="utf-8")
    upstream_present = upstream_probe.returncode == 0
    checks = {
        "exact_head": head == args.expected_head,
        "expected_branch": branch == args.expected_branch,
        "source_ancestor": is_ancestor(args.repo, SOURCE, head),
        "x1_ancestor": is_ancestor(args.repo, X1, head),
        "evidence_ancestor": is_ancestor(args.repo, EVIDENCE, head),
        "phase_commits_four": commits == 4,
        "zero_merges": merges == 0,
        "single_final_parent": parent_count == 1,
        "clean": not status,
        "upstream_expectation": upstream_present == (args.expect_upstream == "yes"),
    }
    result = {
        "schema": "ghc.family.v647-v1.exact-head-audit.v1",
        "valid": all(checks.values()),
        "head": head,
        "branch": branch,
        "phase_commits": commits,
        "merges": merges,
        "final_parent_count": parent_count,
        "upstream_present": upstream_present,
        "checks": checks,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": sum(checks.values()), "total": len(checks), "head": head}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
