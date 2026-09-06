#!/usr/bin/env python3
"""Family-compatible runner for jcs_canonical_profile."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from ghc_family_sable_rook_v687_v3_contracts import evaluate

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a=p.parse_args()
    value=json.loads(a.input.read_text(encoding="utf-8"))
    result=evaluate("jcs_canonical_profile", value)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"operation":"jcs_canonical_profile","status":"PASS"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
