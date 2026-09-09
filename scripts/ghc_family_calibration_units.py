#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ghc_family_measurement_design_core import cli

if __name__ == "__main__":
    cli({'unit_scale', 'affine_correction'})
