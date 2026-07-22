#!/usr/bin/env python3
"""Phase-local wrapper for the `rollover` bounded contract."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if __name__ == "__main__":
    command = [sys.executable, str(ROOT / "scripts/ghc_family_v651_v8_special_runner_runtime.py"), "--contract", "rollover", *sys.argv[1:]]
    raise SystemExit(subprocess.run(command, cwd=ROOT, check=False).returncode)
