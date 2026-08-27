#!/usr/bin/env python3
"""Build the exact final owner manifest from the Git index."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "docs/sable-rook/v672-v3/closeout/owner-manifest.json"
EXCLUSIONS = [
    MANIFEST,
    "docs/sable-rook/v672-v3/validation/final-staged-manifest.json",
    "docs/sable-rook/v672-v3/validation/final-staged-review.json",
]


def git(*args: str, text: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        check=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return completed.stdout


def is_owner_path(path: str) -> bool:
    return (
        path.startswith("docs/sable-rook/v672-v3/")
        or path == "scripts/build_ghc_family_sable_rook_v672_v3.py"
        or path.startswith("scripts/ghc_family_sable_v672_v3_")
        or path == "scripts/validate_ghc_family_sable_rook_v672_v3_final.py"
        or path.startswith("tests/test_ghc_family_sable_rook_v672_v3_")
    )


def main() -> None:
    paths = sorted(path for path in git("ls-files", text=True).splitlines() if is_owner_path(path))
    entries = []
    for path in paths:
        if path in EXCLUSIONS:
            continue
        blob = git("show", f":{path}")
        entries.append(
            {
                "path": path,
                "git_blob_oid": git("rev-parse", f":{path}", text=True).strip(),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "bytes": len(blob),
            }
        )
    output = {
        "schema": "ghc.family.sable.v672-v3.final-owner-manifest.v1",
        "hash_domain": "exact_git_index_blobs_for_prospective_final_tree",
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": EXCLUSIONS,
        "owner_path_count": len(paths),
        "expected_owner_path_count": len(entries) + len(EXCLUSIONS),
    }
    path = ROOT / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
