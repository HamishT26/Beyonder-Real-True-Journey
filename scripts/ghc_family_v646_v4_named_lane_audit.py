#!/usr/bin/env python3
"""Audit self-test or exact local-only named-lane conditions for v646-v4."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, text=True, encoding="utf-8", capture_output=True, check=check)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--worktree", type=Path)
    parser.add_argument("--branch")
    parser.add_argument("--revision")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        checks = {
            "exactly_one_replay_required": True,
            "detached_forbidden": True,
            "upstream_forbidden": True,
            "live_remote_ref_forbidden": True,
            "same_owner_only": True,
        }
        observed = "contract self-test only; no validation worktree or branch was created"
    else:
        if not args.worktree or not args.branch or not args.revision:
            raise SystemExit("--worktree, --branch, and --revision are required outside self-test")
        worktree = args.worktree.resolve()
        head = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
        branch = git("branch", "--show-current", cwd=worktree).stdout.strip()
        status = git("status", "--porcelain=v1", cwd=worktree).stdout.strip()
        upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", cwd=worktree, check=False)
        remote = git("ls-remote", "--heads", "origin", f"refs/heads/{args.branch}", cwd=worktree, check=False)
        checks = {
            "exact_head": head == args.revision,
            "named_not_detached": branch == args.branch and bool(branch),
            "clean": not status,
            "no_upstream": upstream.returncode != 0,
            "no_live_remote_ref": remote.returncode == 0 and not remote.stdout.strip(),
            "local_only_branch": bool(git("show-ref", "--verify", f"refs/heads/{args.branch}", cwd=worktree, check=False).stdout.strip()),
        }
        observed = "exact local-only named-lane audit"
    valid = all(checks.values())
    result = {
        "schema": "ghc.family.v646-v4.named-lane-audit.v1", "mode": "self_test" if args.self_test else "exact_named_lane",
        "checks": checks, "observed": observed, "same_owner_only": True, "independent_reproduction": False,
        "passed": valid, "valid": valid,
        "boundary": "Named-lane locality is same-owner workflow evidence only, never independent-team reproduction or external audit.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
