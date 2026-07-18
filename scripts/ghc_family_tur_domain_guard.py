#!/usr/bin/env python3
"""Family-current bounded runner for V6484-P09."""
from pathlib import Path
from ghc_family_v648_v4_runtime import runner_main

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v648-v4"

if __name__ == "__main__":
    runner_main("V6484-P09", PHASE)
