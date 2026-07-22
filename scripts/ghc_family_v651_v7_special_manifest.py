#!/usr/bin/env python3
"""Build deterministic phase-local manifests for Vesper v651-v7 special CLI prep."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    receipt = PHASE / "validation/x1-validation-receipt.json"
    exclusions = {output.resolve(), receipt.resolve()}
    rows = []
    for path in sorted(p for p in PHASE.rglob("*") if p.is_file() and p.resolve() not in exclusions):
        data = path.read_bytes()
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = {
        "schema": "ghc.family.v651-v7-special.manifest.v1",
        "phase": "v651-v7-special-cli-prep",
        "entry_count": len(rows),
        "self_exclusions": [output.relative_to(ROOT).as_posix(), receipt.relative_to(ROOT).as_posix()],
        "entries": rows,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": True, "entries": len(rows), "output": output.relative_to(ROOT).as_posix()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
