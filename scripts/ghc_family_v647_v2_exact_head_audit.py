#!/usr/bin/env python3
"""Audit exact v647-v2 head, ancestry, history, branch, upstream, and clean state."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8", check=check)
    return proc.stdout.strip()


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--x1", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--expected-branch", required=True)
    parser.add_argument("--expect-upstream", choices=["yes", "no"], required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status = git("status", "--porcelain=v1")
    parent_count = len(git("show", "-s", "--format=%P", head).split())
    phase_commits = int(git("rev-list", "--count", f"{args.source}..{head}"))
    merges = int(git("rev-list", "--count", "--merges", f"{args.source}..{head}"))
    anchors = {}
    for name, revision in (("source", args.source), ("x1", args.x1), ("evidence", args.evidence)):
        rc = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", revision, head]
        ).returncode
        anchors[name] = rc == 0
    upstream_proc = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "@{upstream}"], capture_output=True, text=True)
    upstream_present = upstream_proc.returncode == 0
    checks = {
        "exact_head": head == args.expected_head,
        "expected_branch": branch == args.expected_branch,
        "clean": status == "",
        "phase_commit_count_three": phase_commits == 3,
        "zero_merges": merges == 0,
        "one_final_parent": parent_count == 1,
        "source_ancestral": anchors["source"],
        "x1_ancestral": anchors["x1"],
        "evidence_ancestral": anchors["evidence"],
        "upstream_expectation": upstream_present == (args.expect_upstream == "yes"),
    }
    result = {
        "schema": "ghc.family.v647-v2.exact-head-audit.v1",
        "valid": all(checks.values()),
        "checks_total": len(checks),
        "checks_passed": sum(checks.values()),
        "checks": checks,
        "head": head,
        "branch": branch,
        "phase_commits": phase_commits,
        "merges": merges,
        "parent_count": parent_count,
        "upstream_present": upstream_present,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": result["checks_total"], "head": head}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
