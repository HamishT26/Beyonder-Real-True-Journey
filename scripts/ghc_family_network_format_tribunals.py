#!/usr/bin/env python3
"""Family-current bounded witness runner for Orin v652-v2."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v652_v2_core import group_self_test

PROPOSAL_IDS = ['V6522-P15', 'V6522-P16', 'V6522-P17', 'V6522-P22']

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = group_self_test(PROPOSAL_IDS)
    receipt["runner"] = "ghc_family_network_format_tribunals.py"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runner": "ghc_family_network_format_tribunals.py", "proposals": len(PROPOSAL_IDS), "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
