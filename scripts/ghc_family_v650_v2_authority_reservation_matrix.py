#!/usr/bin/env python3
"""Additive family-current v650-v2 wrapper for V6502-P06."""
from __future__ import annotations
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_v650_v2_runtime import runner_main

if __name__ == "__main__":
    raise SystemExit(runner_main("V6502-P06"))
