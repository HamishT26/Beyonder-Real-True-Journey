#!/usr/bin/env python3
"""Family-current bounded runner: ghc_family_binary_schema_container_tribunals.py."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v652_v5_core import execute_ids

PROPOSAL_IDS = ['V6525-P01', 'V6525-P02', 'V6525-P03', 'V6525-P04']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    results = execute_ids(PROPOSAL_IDS, args.output_root)
    print(json.dumps({
        "runner": Path(__file__).name,
        "proposal_ids": PROPOSAL_IDS,
        "valid": all(row["bounded_receipt"]["valid"] for row in results),
        "mutation_count": sum(row["mutation_results"]["count"] for row in results),
        "rejected_or_quarantined": sum(row["mutation_results"]["rejected_or_quarantined_count"] for row in results),
        "boundary": "Bounded same-owner synthetic execution only."
    }, sort_keys=True))


if __name__ == "__main__":
    main()
