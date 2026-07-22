#!/usr/bin/env python3
"""Build an exact staged-delta manifest with explicit lifecycle self-exclusions."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str, binary: bool = False):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True, text=not binary, encoding=None if binary else "utf-8").stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    exclusions = {output.relative_to(ROOT).as_posix(), *[Path(row).as_posix() for row in args.exclude]}
    staged = sorted(filter(None, git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    rows = []
    for relative in staged:
        if relative in exclusions:
            continue
        data = git("show", f":{relative}", binary=True)
        rows.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    payload = {
        "schema": "ghc.family.v651-v8-special.final-delta-manifest.v1",
        "base": git("rev-parse", "HEAD").strip(),
        "entry_count": len(rows),
        "declared_exclusions": sorted(exclusions),
        "entries": rows,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": True, "entries": len(rows), "exclusions": len(exclusions)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
