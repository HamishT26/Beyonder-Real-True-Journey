#!/usr/bin/env python3
"""Audit future CLI route coverage while preserving submitted/candidate differences."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    register = load(args.register)
    seats = register.get("seats", [])
    differences = [
        {
            "seat": row.get("seat"),
            "submitted_phase_mention": row.get("submitted_phase_mention"),
            "normalized_candidate_phase": row.get("normalized_candidate_phase"),
        }
        for row in seats
        if row.get("submitted_phase_mention") != row.get("normalized_candidate_phase")
    ]
    placeholders = [row.get("seat") for row in seats]
    payload = {
        "schema": "ghc.family.cli-route-coverage.receipt.v1",
        "valid": len(seats) == 8 and len(set(placeholders)) == 8,
        "seat_count": len(seats),
        "unique_placeholders": len(set(placeholders)),
        "submitted_candidate_differences": differences,
        "difference_count": len(differences),
        "raw_truth_preserved": bool(differences),
        "candidate_is_advisory": True,
        "boundary": "Coverage does not confirm a future launch schedule or normalize conflicting ownership silently.",
    }
    write(args.receipt, payload)
    print(json.dumps({"valid": payload["valid"], "seats": len(seats), "differences": len(differences)}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
