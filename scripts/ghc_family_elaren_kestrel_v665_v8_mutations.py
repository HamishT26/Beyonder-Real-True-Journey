#!/usr/bin/env python3
"""Elaren Kestrel v665-v8 runner: one-hundred mutation rejection."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_elaren_kestrel_v665_v8_runner_common import run

RUNNER_ID = 'mutations'
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description='one-hundred mutation rejection')
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
