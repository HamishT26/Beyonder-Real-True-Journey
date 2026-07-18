#!/usr/bin/env python3
"""Parse every v648-v6 JSON artifact and verify operational-negative parity."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"


def main() -> None:
    files = sorted(PHASE.rglob("*.json"))
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))
    operational = json.loads((PHASE / "validation/x2-operational-negatives.json").read_text(encoding="utf-8"))
    if operational["count"] != len(operational["negatives"]):
        raise RuntimeError("x2 operational-negative parity failed")
    print(json.dumps({"json_parses": len(files), "operational_negatives": operational["count"], "passed": True}, sort_keys=True))


if __name__ == "__main__":
    main()
