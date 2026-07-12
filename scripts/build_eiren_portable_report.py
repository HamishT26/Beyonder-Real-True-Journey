#!/usr/bin/env python3
"""Deprecated compatibility entrypoint; use build_ghc_family_portable_report.py."""

from pathlib import Path
import runpy

runpy.run_path(
    str(Path(__file__).with_name("build_ghc_family_portable_report.py")),
    run_name="__main__",
)
