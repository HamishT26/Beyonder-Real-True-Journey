#!/usr/bin/env python3
"""Verify exact Git-blob entries in a Caelen Ash v672-v4 manifest."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True).stdout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--revision", default="HEAD")
    args = parser.parse_args()
    root = Path(args.root)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    mismatches = []
    for row in manifest["entries"]:
        spec = f":{row['path']}" if args.revision == "INDEX" else f"{args.revision}:{row['path']}"
        observed = git(root, "rev-parse", spec).decode().strip()
        if observed != row["git_blob_oid"]:
            mismatches.append(row["path"])
    print(json.dumps({"entries": len(manifest["entries"]), "mismatches": mismatches, "valid": not mismatches}))
    raise SystemExit(0 if not mismatches else 1)

if __name__ == "__main__":
    main()
