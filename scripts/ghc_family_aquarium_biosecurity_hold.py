#!/usr/bin/env python3
"""Family-current Caelen Ash v657-v5 bounded aquarium evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v5_runtime import ROOT, run_named_surface, write_json


SURFACES = ['aquarium-water-change-plan', 'aquarium-specimen-provenance', 'aquarium-habitat-change']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {
        "schema": "ghc.family.v657-v5.group-runner-receipt.v1",
        "runner": "ghc_family_aquarium_biosecurity_hold.py",
        "surfaces": SURFACES,
        "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "same_owner_only": True,
        "independent_reproduction": False,
        "rows": rows,
    }
    write_json(ROOT / args.output, payload)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
