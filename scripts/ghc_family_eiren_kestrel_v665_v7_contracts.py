#!/usr/bin/env python3
"""Eiren Kestrel v665-v7 runner: contract evaluation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_eiren_kestrel_v665_v7_runner_common import run

RUNNER_ID = 'contracts'
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description='contract evaluation')
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
