#!/usr/bin/env python3
"""Family-current Caelen v658-v3 bounded archival-film evidence runner."""

from __future__ import annotations

import argparse
import json

from ghc_family_v658_v3_runtime import ROOT, run_named_surface, write_json


SURFACES = ['film-dpx-sequence', 'film-accessible-report', 'film-standards-capability']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {
        "schema": "ghc.family.v658-v3.group-runner-receipt.v1",
        "runner": "ghc_family_film_dpx_premis.py", "surfaces": SURFACES, "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "authority_actions_executed": 0, "same_owner_only": True, "independent_reproduction": False,
        "rows": rows,
    }
    write_json(ROOT / args.output, payload)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
