#!/usr/bin/env python3
"""Build an exact Git-index-blob owner manifest for Ilyra v649-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/ilyra-fen/v649-v2/"


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text, check=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    output = Path(args.output).as_posix()
    exclusions = sorted(set([output, *[Path(item).as_posix() for item in args.exclude]]))
    rows = []
    for line in str(git("ls-files", "-s", "--", PREFIX)).splitlines():
        metadata, path = line.split("\t", 1)
        if path in exclusions:
            continue
        oid = metadata.split()[1]
        data = git("cat-file", "blob", oid, text=False)
        assert isinstance(data, bytes)
        rows.append({"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    payload = {
        "schema": "ghc.family.v649-v2.owner-manifest.final.v1",
        "hash_domain": "exact_git_index_blob",
        "entry_count": len(rows),
        "entries": rows,
        "self_exclusions": exclusions,
        "covered_path_count": len(rows) + len(exclusions),
        "boundary": "Exact same-owner Git-index coverage only; not independent reproduction or complete privacy or security assurance.",
    }
    target = ROOT / output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"entries": len(rows), "exclusions": len(exclusions), "covered": payload["covered_path_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
