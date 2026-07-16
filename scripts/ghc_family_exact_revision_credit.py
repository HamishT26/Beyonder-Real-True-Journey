#!/usr/bin/env python3
"""Bind a bounded receipt to the exact revision actually inspected."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    requested = args.revision or head
    resolved = git("rev-parse", f"{requested}^{{commit}}")
    checks = [len(requested) == 40, resolved == requested, head == requested]
    payload = {
        "schema": "ghc.family.exact-revision-credit.v1", "checks": len(checks), "passed": all(checks),
        "requested_revision": requested, "resolved_revision": resolved, "observed_head": head,
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Exact revision binding covers the invoked checkout only; it is not independent reproduction or domain confirmation.",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
