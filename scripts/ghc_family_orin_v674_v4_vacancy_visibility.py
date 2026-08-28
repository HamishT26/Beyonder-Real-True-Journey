#!/usr/bin/env python3
"""Family-current Orin v674-v4 vacancy visibility runner."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_orin_v674_v4_contract_core import run_batch

RUNNER_ID = "OR6744-RUNNER-03-vacancy_visibility"

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
