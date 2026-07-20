#!/usr/bin/env python3
"""Additive family-current v650-v1 wrapper for V6501-P10."""
from __future__ import annotations
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_v650_v1_runtime import runner_main

if __name__ == "__main__":
    raise SystemExit(runner_main("V6501-P10"))
