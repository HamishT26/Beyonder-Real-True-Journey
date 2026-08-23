#!/usr/bin/env python3
"""Bounded family-current identity runner for Caelen Morrow v667-v5."""
from __future__ import annotations
import argparse
import json
from ghc_family_caelen_morrow_v667_v5_core import runner_self_test

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    result = runner_self_test("identity")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
