#!/usr/bin/env python3
"""Family-current Liora v674-v5 authority gate runner."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_liora_v674_v5_contract_core import run_batch

RUNNER_ID = "LV6745-RUNNER-07-authority_gate"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = run_batch(payload["records"], RUNNER_ID)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["expectation_matches"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
