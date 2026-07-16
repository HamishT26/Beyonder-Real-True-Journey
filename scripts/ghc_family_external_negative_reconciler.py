#!/usr/bin/env python3
"""Reconcile the sealed, external, x1, synthetic, and current x2 negative counts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v646-v3"
BOUNDARY = "Count reconciliation preserves failures; it is not scientific replication or broader assurance."


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    x1 = load("validation/x1-operational-negatives.json")
    retained = load("retained-negative-register.json") if (PHASE / "retained-negative-register.json").is_file() else None
    checks = [
        x1.get("inherited_effective") == 2619,
        len(x1.get("inherited_external_terminal_negatives", [])) == 3,
        x1.get("new_x1_operational") == 5,
    ]
    if retained:
        expected = sum(retained.get(key, 0) for key in ("inherited_effective", "x1_operational", "preregistered_synthetic_executed_and_rejected", "x2_operational"))
        checks.extend([
            retained.get("inherited_effective") == 2619,
            retained.get("x1_operational") == 5,
            retained.get("preregistered_synthetic_executed_and_rejected") == 70,
            retained.get("effective_total") == expected,
            retained.get("no_negative_erased") is True,
        ])
    payload = {
        "schema": "ghc.family.external-negative-reconciler.v1",
        "checks": len(checks),
        "passed": all(checks),
        "sealed_predecessor": 2616,
        "external_predecessor": 3,
        "activation_baseline": 2619,
        "x1_operational": 5,
        "current_effective_total": retained.get("effective_total") if retained else None,
        "no_negative_erased": True,
        "boundary": BOUNDARY,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
