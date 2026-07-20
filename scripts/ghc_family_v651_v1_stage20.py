#!/usr/bin/env python3
"""Family-current bounded validator for gmres, model-x-knockoff."""
import argparse
import json
from pathlib import Path
from ghc_family_v651_v1_runtime import validate_surface_root

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase-root", default="docs/sable-rook/v651-v1")
    args=parser.parse_args()
    result=validate_surface_root(Path(args.phase_root), ['gmres', 'model-x-knockoff'])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
