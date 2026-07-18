#!/usr/bin/env python3
"""Build the exact final owner manifest from Git-index blobs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/eiren-kestrel/v649-v1/"


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=text).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=PREFIX + "validation/final-owner-manifest.json")
    args = parser.parse_args()
    output = args.output.replace("\\", "/")
    exclusions = [
        output,
        PREFIX + "validation/final-staged-manifest.json",
        PREFIX + "validation/final-staged-privacy.json",
        PREFIX + "validation/final-staged-review.json",
    ]
    phase_files = sorted(
        path for path in str(git("ls-files", "--", PREFIX)).splitlines()
        if path and path not in exclusions
    )
    entries = []
    for path in phase_files:
        stage = str(git("ls-files", "-s", "--", path)).strip()
        if not stage:
            raise RuntimeError(f"missing index entry: {path}")
        oid = stage.split()[1]
        blob = git("cat-file", "blob", oid, text=False)
        assert isinstance(blob, bytes)
        checkout = (ROOT / path).read_bytes()
        entries.append({
            "path": path,
            "git_blob": oid,
            "git_blob_sha256": hashlib.sha256(blob).hexdigest(),
            "checkout_sha256": hashlib.sha256(checkout).hexdigest(),
            "git_blob_bytes": len(blob),
            "checkout_bytes": len(checkout),
        })
    working = sorted(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / PREFIX).rglob("*") if p.is_file()
    )
    existing_exclusions = [path for path in exclusions if (ROOT / path).is_file()]
    covered = sorted(phase_files + existing_exclusions)
    if working != covered:
        missing = sorted(set(working) - set(covered))
        extra = sorted(set(covered) - set(working))
        raise RuntimeError(f"owner coverage mismatch missing={missing} extra={extra}")
    payload = {
        "schema": "ghc.family.v649-v1.final-owner-manifest.v1",
        "hash_domain": "exact_git_index_blob_and_current_checkout",
        "entry_count": len(entries), "entries": entries,
        "self_exclusions": exclusions, "self_exclusion_count": len(exclusions),
        "owner_path_count": len(entries) + len(exclusions), "threshold": 15000,
        "within_threshold": len(entries) + len(exclusions) < 15000,
    }
    destination = ROOT / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"entries": len(entries), "exclusions": len(exclusions), "owner_paths": len(working)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
