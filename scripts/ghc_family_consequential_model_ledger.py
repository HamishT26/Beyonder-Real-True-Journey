#!/usr/bin/env python3
"""Family-current bounded delegate for Elaren v651-v6."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v651_v6_runtime import REPO, run_group


SURFACES = ['cbr-contestation-chain', 'cbr-explanation-provenance', 'cbr-model-redress-authority']


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = run_group(SURFACES)
    if args.output:
        target = REPO / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runner": Path(__file__).name, "surfaces": len(SURFACES), "valid": payload["valid"], "output": args.output}, sort_keys=True))


if __name__ == "__main__":
    main()
