#!/usr/bin/env python3
"""Family-current bounded runner for V6493-P05."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_v649_v3_runtime import main_for
if __name__ == "__main__":
    raise SystemExit(main_for("V6493-P05"))
