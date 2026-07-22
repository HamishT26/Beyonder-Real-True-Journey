#!/usr/bin/env python3
"""Build deterministic phase-local manifests for Vesper v651-v7 special CLI prep."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--domain", choices=("worktree", "index", "head"), default="worktree")
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    exclusions = {output.relative_to(ROOT).as_posix(), *[Path(value).as_posix() for value in args.exclude]}
    rows = []
    if args.domain == "worktree":
        paths = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()]
    else:
        paths = subprocess.run(
            ["git", "ls-files", "--cached", "--", PHASE.relative_to(ROOT).as_posix()],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.splitlines()
    for relative in sorted(path for path in paths if path not in exclusions):
        if args.domain == "worktree":
            data = (ROOT / relative).read_bytes()
        else:
            spec = f":{relative}" if args.domain == "index" else f"HEAD:{relative}"
            data = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, check=True).stdout
        rows.append(
            {
                "path": relative,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = {
        "schema": "ghc.family.v651-v7-special.manifest.v1",
        "phase": "v651-v7-special-cli-prep",
        "entry_count": len(rows),
        "domain": args.domain,
        "self_exclusions": sorted(exclusions),
        "entries": rows,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": True, "entries": len(rows), "output": output.relative_to(ROOT).as_posix()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
