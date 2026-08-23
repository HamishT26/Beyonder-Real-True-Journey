"""Family-current Neris v667-v8 runner entrypoint."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
sys.dont_write_bytecode = True
_path = Path(__file__).with_name("build_ghc_family_neris_solane_v667_v8_x2.py")
_spec = importlib.util.spec_from_file_location("_neris_v667_v8_x2_runner", _path)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load Neris v667-v8 x2 runner surface")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
def runner_main(name: str) -> int:
    return _module.runner_main(name)
