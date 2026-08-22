#!/usr/bin/env python3
"""Caelen Morrow v665-v6 runner: static structural accessibility checks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_caelen_morrow_v665_v6_runner_common import run

RUNNER_ID = 'accessibility'
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description='static structural accessibility checks')
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
