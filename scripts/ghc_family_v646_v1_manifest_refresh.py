#!/usr/bin/env python3
"""Refresh the exact logical manifest after bounded lifecycle mutations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v1"
MANIFEST = PHASE / "validation/evidence-manifest.json"
EXCLUDED = {
    "validation/evidence-manifest.json",
    "validation/evidence-validation.json",
    "validation/final-staged-review.json",
    "closeout-receipt.json",
    "seal-receipt.json",
    "final-validation-record.json",
}


def logical_hash(path: Path) -> str:
    data = path.read_bytes()
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        normalized = data
    else:
        normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def main() -> int:
    previous = json.loads(MANIFEST.read_text(encoding="utf-8"))
    previous_hashes = {row["path"]: row["logical_sha256"] for row in previous.get("entries", [])}
    entries = []
    for path in sorted(candidate for candidate in PHASE.rglob("*") if candidate.is_file()):
        rel = path.relative_to(PHASE).as_posix()
        if rel in EXCLUDED:
            continue
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "logical_sha256": logical_hash(path),
                "bytes": path.stat().st_size,
            }
        )
    changed = [row["path"] for row in entries if previous_hashes.get(row["path"]) != row["logical_sha256"]]
    removed = sorted(set(previous_hashes) - {row["path"] for row in entries})
    payload = {
        "schema": "ghc.family.v646-v1.evidence-manifest.v1",
        "phase": "v646-gmut-thos-v1-x1-x2",
        "entry_count": len(entries),
        "entries": entries,
        "hash_rule": "sha256 after CRLF-to-LF normalization for UTF-8 text; raw bytes otherwise",
        "excluded": sorted(EXCLUDED),
        "refresh": {
            "reason": "bounded closeout lifecycle mutation after retained V6461-CLOSE-N05",
            "changed_or_added_count": len(changed),
            "removed_count": len(removed),
            "removed": removed,
        },
        "boundary": "Manifest parity establishes content identity only, not semantic truth or independent reproduction.",
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"entries": len(entries), "changed_or_added": len(changed), "removed": len(removed), "valid": not removed}))
    return 0 if not removed else 1


if __name__ == "__main__":
    raise SystemExit(main())
