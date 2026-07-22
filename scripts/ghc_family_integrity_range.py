#!/usr/bin/env python3
"""Family-current thin delegate for the v651-v7 integrity-range group."""

from __future__ import annotations

import argparse
import json

from ghc_family_v651_v7_runtime import run_group


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = run_group("integrity-range")
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
