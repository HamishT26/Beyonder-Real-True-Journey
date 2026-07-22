#!/usr/bin/env python3
"""Measure a sparse owner lane without confusing materialization with Git history."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(*args: str, cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=True)
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--limit", type=int, default=2000)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    materialized = sum(1 for path in repo.rglob("*") if path.is_file())
    tracked = len(git("ls-files", cwd=repo).splitlines())
    sparse = git("config", "--bool", "core.sparseCheckout", cwd=repo).lower() == "true"
    payload = {
        "schema": "ghc.family.sparse-lane-guard.receipt.v1",
        "valid": sparse and materialized < args.limit,
        "sparse_checkout": sparse,
        "materialized_files": materialized,
        "materialized_limit": args.limit,
        "full_tracked_history_files": tracked,
        "head": git("rev-parse", "HEAD", cwd=repo),
        "clean": not bool(git("status", "--porcelain", cwd=repo)),
        "boundary": "The ceiling applies to the materialized owner working surface; sparse checkout does not sever immutable Git history.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "materialized": materialized, "tracked": tracked}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
