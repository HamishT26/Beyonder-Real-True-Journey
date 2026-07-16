#!/usr/bin/env python3
"""Audit the one clean local-only named v646-v6 validation lane."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--expected-branch", default="codex/GHC-Family/sylven-arc-v646-v6-validation-local")
    parser.add_argument("--write")
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], text=True, encoding="utf-8").splitlines()
    upstream = subprocess.run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], capture_output=True, text=True, encoding="utf-8")
    remote = subprocess.check_output(["git", "ls-remote", "--heads", "origin", f"refs/heads/{branch}"], text=True, encoding="utf-8").splitlines()
    checks = {
        "exact_head": head == args.expected_head,
        "named_non_detached_branch": branch == args.expected_branch and bool(branch),
        "clean": not status,
        "no_upstream": upstream.returncode != 0,
        "no_live_remote_ref": not remote,
    }
    payload = {
        "schema": "ghc.family.v646-v6.named-lane-audit.v1",
        "head": head,
        "branch": branch,
        "checks": checks,
        "passed": sum(checks.values()),
        "check_count": len(checks),
        "same_owner_only": True,
        "independent_reproduction": False,
        "result": "pass" if all(checks.values()) else "fail",
    }
    if args.write:
        Path(args.write).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=True))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
