#!/usr/bin/env python3
"""Invoke all twelve phase-local runner wrappers on accepting and rejecting fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"


def main() -> int:
    build = json.loads((PHASE / "runners/runner-build-ledger.json").read_text(encoding="utf-8"))
    rows = []
    for row in build["rows"]:
        wrapper = PHASE / "runners" / row["name"]
        receipts = {}
        for fixture in ("accept", "reject"):
            output = PHASE / f"runners/receipts/{row['contract']}-{fixture}.json"
            relative = output.relative_to(ROOT).as_posix()
            result = subprocess.run(
                [sys.executable, str(wrapper), "--fixture", fixture, "--output", relative],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60,
                check=False,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            receipts[fixture] = {
                "exit": result.returncode,
                "receipt": relative,
                "accepted": payload["accepted"],
                "valid": result.returncode == 0 and payload["accepted"] is (fixture == "accept"),
            }
        rows.append({**row, "state": "used", "receipts": receipts})
    payload = {
        "schema": "ghc.family.v651-v8-special.runner-use.v1",
        "count": len(rows),
        "accept_passes": sum(bool(row["receipts"]["accept"]["valid"]) for row in rows),
        "reject_passes": sum(bool(row["receipts"]["reject"]["valid"]) for row in rows),
        "rows": rows,
        "boundary": "Synthetic and read-only owner-local witnesses only; no future CLI process or sibling was launched.",
    }
    path = PHASE / "runners/runner-use-ledger.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    valid = payload["count"] == 12 and payload["accept_passes"] == 12 and payload["reject_passes"] == 12
    print(json.dumps({"valid": valid, "runners": payload["count"], "accept": payload["accept_passes"], "reject": payload["reject_passes"]}))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
