#!/usr/bin/env python3
"""Family-current bounded runner for V6485-P02."""
from pathlib import Path
from ghc_family_v648_v5_runtime import runner_main

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v648-v5"

if __name__ == "__main__":
    runner_main("V6485-P02", PHASE)
