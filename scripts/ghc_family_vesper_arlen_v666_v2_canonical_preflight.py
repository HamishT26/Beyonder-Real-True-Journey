#!/usr/bin/env python3
"""Vesper Arlen v666-v2 runner: canonical completion preflight without invoking the aggregate."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_vesper_arlen_v666_v2_runner_common import run

RUNNER_ID = 'canonical-preflight'
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description='canonical completion preflight without invoking the aggregate')
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
