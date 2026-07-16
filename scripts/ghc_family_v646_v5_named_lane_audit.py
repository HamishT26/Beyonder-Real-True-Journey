#!/usr/bin/env python3
"""Audit synthetic logic or an actual local-only named validation lane for v646-v5."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, encoding="utf-8")
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


def classify(branch: str, head: str, expected: str, clean: bool, upstream: bool, remote_ref: bool) -> dict:
    checks = {
        "named_branch": bool(branch and branch != "HEAD"),
        "exact_head": head == expected,
        "clean": clean,
        "no_upstream": not upstream,
        "no_live_remote_ref": not remote_ref,
    }
    return {"checks": checks, "valid": all(checks.values())}


def self_test() -> dict:
    accepted = classify("codex/GHC-Family/tamar-vey-v646-v5-validation", "a" * 40, "a" * 40, True, False, False)
    rejected = [
        classify("HEAD", "a" * 40, "a" * 40, True, False, False),
        classify("lane", "b" * 40, "a" * 40, True, False, False),
        classify("lane", "a" * 40, "a" * 40, False, False, False),
        classify("lane", "a" * 40, "a" * 40, True, True, False),
        classify("lane", "a" * 40, "a" * 40, True, False, True),
    ]
    return {"mode": "synthetic_self_test", "positive": accepted, "negative_cases": rejected, "valid": accepted["valid"] and all(not row["valid"] for row in rejected)}


def actual(expected: str, remote: str) -> dict:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    clean = not bool(git("status", "--porcelain=v1"))
    upstream_result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=ROOT, text=True, capture_output=True)
    remote_line = git("ls-remote", "--heads", remote, branch, check=False)
    result = classify(branch, head, expected, clean, upstream_result.returncode == 0, bool(remote_line))
    result.update({"mode": "actual_named_lane", "branch": branch, "head": head, "clean": clean, "upstream_present": upstream_result.returncode == 0, "remote_ref_present": bool(remote_line), "same_owner_only": True, "independent_reproduction": False})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--expected")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = self_test() if args.self_test else actual(args.expected or "", args.remote)
    result.update({"schema": "ghc.family.v646-v5.named-lane-audit.v1", "boundary": "A same-owner local named-lane replay is not independent-team scientific reproduction, external audit, production certification, or authority."})
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": result["mode"], "valid": result["valid"]}))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
