#!/usr/bin/env python3
"""Deprecated compatibility entrypoint; use validate_ghc_family_docx.py."""

from pathlib import Path
import runpy

runpy.run_path(
    str(Path(__file__).with_name("validate_ghc_family_docx.py")),
    run_name="__main__",
)
