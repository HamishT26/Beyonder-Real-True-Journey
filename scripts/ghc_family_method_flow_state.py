#!/usr/bin/env python3
"""Repository entrypoint for the GHC Family Method Flow State skill runner."""

from __future__ import annotations

import os
import runpy
from pathlib import Path


def resolve_skill_runner() -> Path:
    roots: list[Path] = []
    if os.environ.get("CODEX_HOME"):
        roots.append(Path(os.environ["CODEX_HOME"]))
    roots.append(Path.home() / ".codex")
    for root in roots:
        candidate = (
            root
            / "skills"
            / "ghc-family-method-flow-state"
            / "scripts"
            / "ghc_family_method_flow_state.py"
        )
        if candidate.is_file():
            return candidate
    raise SystemExit(
        "ghc-family-method-flow-state is not installed; install or restore the family skill before using this wrapper"
    )


if __name__ == "__main__":
    runpy.run_path(str(resolve_skill_runner()), run_name="__main__")
