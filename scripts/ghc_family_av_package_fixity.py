#!/usr/bin/env python3
"""Family-current Tamar Vey v657-v8 bounded audiovisual evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v8_runtime import ROOT, run_named_surface, write_json


SURFACES = ['av-noise-dynamic-range', 'av-uncertainty-covariance', 'av-identifiability-tribunal']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {
        "schema": "ghc.family.v657-v8.group-runner-receipt.v1",
        "runner": "ghc_family_av_package_fixity.py",
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
