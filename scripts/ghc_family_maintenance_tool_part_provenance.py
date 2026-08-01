#!/usr/bin/env python3
"""Family-current Vesper v658-v7 aircraft-maintenance assurance runner."""

from __future__ import annotations

import argparse
import json

from ghc_family_v658_v7_runtime import ROOT, run_named_surface, write_json


SURFACES = ['maintenance-component-chain','maintenance-nonroutine-finding','maintenance-ndt-boundary']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {
        "schema": "ghc.family.v658-v7.group-runner-receipt.v1",
        "runner": "ghc_family_maintenance_tool_part_provenance.py",
        "surfaces": SURFACES,
        "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "same_owner_only": True,
        "independent_reproduction": False,
        "rows": rows,
    }
    if args.output:
        write_json(ROOT / args.output, payload)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
