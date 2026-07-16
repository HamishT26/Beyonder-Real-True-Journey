#!/usr/bin/env python3
"""Verify a v647-v1 manifest against exact Git commit blob bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--manifest-path", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    manifest_spec = f"{args.commit}:{args.manifest_path}"
    manifest = json.loads(git_bytes("cat-file", "blob", manifest_spec).decode("utf-8"))
    mismatches = []
    checked = []
    for entry in manifest["entries"]:
        spec = f"{args.commit}:{entry['path']}"
        try:
            blob = git_bytes("cat-file", "blob", spec)
        except subprocess.CalledProcessError:
            mismatches.append({"path": entry["path"], "reason": "missing_blob"})
            continue
        digest = hashlib.sha256(blob).hexdigest()
        if digest != entry["sha256"]:
            mismatches.append({"path": entry["path"], "reason": "sha256_mismatch", "observed": digest})
        checked.append(entry["path"])
    result = {
        "schema": "ghc.family.v647-v1.commit-manifest-parity.v1",
        "commit": args.commit,
        "manifest_path": args.manifest_path,
        "manifest_entry_count": manifest["entry_count"],
        "checked_count": len(checked),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "valid": len(mismatches) == 0 and len(checked) == manifest["entry_count"],
        "hash_domain": "sha256 of exact Git commit blob bytes",
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checked": len(checked), "mismatches": len(mismatches)}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
