#!/usr/bin/env python3
"""Run all ten bounded v646-v6 core surfaces and emit a compact receipt."""

from __future__ import annotations

import json
from pathlib import Path

from ghc_family_v646_v6_runtime import PHASE, write_phase_artifacts


def main() -> int:
    result = write_phase_artifacts()
    receipt = {
        "schema": "ghc.family.v646-v6.core-runner.v1",
        **result,
        "result": "pass" if result["surface_count"] == 10 and result["synthetic_negatives"] == result["rejected"] == 70 else "fail",
    }
    path = PHASE / "validation/core-runner-summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
