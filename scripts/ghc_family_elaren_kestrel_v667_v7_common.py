"""Shared family-current entrypoint for Elaren v667-v7 runners."""
from __future__ import annotations
import importlib.util
from pathlib import Path

_path = Path(__file__).with_name("build_ghc_family_elaren_kestrel_v667_v7_x2.py")
_spec = importlib.util.spec_from_file_location("_elaren_v667_v7_x2_runner", _path)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load Elaren v667-v7 x2 runner surface")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

def runner_main(name: str) -> int:
    return _module.runner_main(name)
