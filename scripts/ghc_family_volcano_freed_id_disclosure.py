#!/usr/bin/env python3
"""Family-current Neris v656-v7 volcanic-observatory runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v656_v7_runtime import ROOT, run_named_surface, write_json


SURFACES = ['gmut-volcanic-deformation-proxy', 'thos-volcanic-multisensor-choreography', 'freed-id-volcano-sensor-capsule']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {
        "schema": "ghc.family.v656-v7.group-runner-receipt.v1",
        "runner": "ghc_family_volcano_freed_id_disclosure.py",
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
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
