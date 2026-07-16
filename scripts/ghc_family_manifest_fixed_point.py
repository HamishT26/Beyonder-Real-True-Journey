#!/usr/bin/env python3
"""Verify the immutable x1 self-excluding manifest against exact Git blobs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v646-v3"
X1 = "5894a1e1fcb923b37d5ce109824b61ad24739fb5"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = json.loads((PHASE / "validation/x1-staged-manifest.json").read_text(encoding="utf-8"))
    mismatches = []
    quarantined_companions = {
        "docs/sable-rook/v646-v3/validation/x1-privacy-review.json",
        "docs/sable-rook/v646-v3/validation/x1-structural-review.json",
    }
    manifest_path = "docs/sable-rook/v646-v3/validation/x1-staged-manifest.json"
    for row in manifest.get("entries", []):
        result = subprocess.run(["git", "show", f"{X1}:{row['path']}"], cwd=ROOT, capture_output=True)
        if result.returncode or hashlib.sha256(result.stdout).hexdigest() != row.get("sha256"):
            mismatches.append(row.get("path"))
    mismatch_set = set(mismatches)
    checks = [
        manifest.get("entry_count") == len(manifest.get("entries", [])),
        manifest_path not in {row.get("path") for row in manifest.get("entries", [])},
        mismatch_set == quarantined_companions,
        manifest.get("revision") in (None, X1),
    ]
    payload = {
        "schema": "ghc.family.manifest-fixed-point.v1", "checks": len(checks), "passed": all(checks),
        "revision": X1, "entry_count": len(manifest.get("entries", [])),
        "exact_blob_match_count": len(manifest.get("entries", [])) - len(mismatches),
        "mismatches": mismatches, "quarantined_companion_drift": sorted(quarantined_companions),
        "x1_exact_fixed_point_credit": False, "successor_exact_fixed_point_required": True,
        "self_excluding": True,
        "boundary": "The two immutable x1 review companions are quarantined rather than called exact parity. Successor manifests must match exact staged Git blobs; this is not semantic completeness or independent reproduction.",
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
