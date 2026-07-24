#!/usr/bin/env python3
"""Family-current bounded witness runner for Caelen v654-v4."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v654_v4_core import group_self_test

PROPOSAL_IDS = ['V6544-P16', 'V6544-P17']

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = group_self_test(PROPOSAL_IDS)
    receipt["runner"] = "ghc_family_garment_notice_quarantine.py"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runner": "ghc_family_garment_notice_quarantine.py", "proposals": len(PROPOSAL_IDS), "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
