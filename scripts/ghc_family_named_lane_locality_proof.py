#!/usr/bin/env python3
"""Preflight or verify the single local-only named validation lane."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v646-v3"


def run_git(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch")
    parser.add_argument("--worktree", type=Path)
    parser.add_argument("--revision")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.branch:
        route = json.loads((PHASE / "orchestration/terminal-route-plan.json").read_text(encoding="utf-8"))
        joined = " ".join(route.get("preconditions", [])).casefold()
        checks = ["exactly one" in joined, "named-lane replay" in joined or "local-only" in joined or "local only" in joined, route.get("send_count") == 0]
        payload = {"schema": "ghc.family.named-lane-locality-proof.v1", "mode": "preflight", "checks": len(checks), "passed": all(checks), "route_state": route.get("current_state")}
    else:
        if not args.worktree or not args.revision:
            raise SystemExit("--branch verification requires --worktree and --revision")
        head = run_git("rev-parse", "HEAD", cwd=args.worktree)
        upstream = run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", cwd=args.worktree)
        remote = run_git("ls-remote", "--heads", "origin", f"refs/heads/{args.branch}", cwd=args.worktree)
        clean = run_git("status", "--porcelain=v1", cwd=args.worktree)
        checks = [head.returncode == 0 and head.stdout.strip() == args.revision, upstream.returncode != 0, remote.returncode == 0 and not remote.stdout.strip(), clean.returncode == 0 and not clean.stdout.strip()]
        payload = {"schema": "ghc.family.named-lane-locality-proof.v1", "mode": "verified", "checks": len(checks), "passed": all(checks), "branch": args.branch, "revision": args.revision, "has_upstream": upstream.returncode == 0, "remote_ref_present": bool(remote.stdout.strip()), "clean": not clean.stdout.strip()}
    payload.update({"same_owner_only": True, "independent_reproduction": False, "boundary": "A local-only lane replay is same-owner process evidence, never independent-team reproduction."})
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
