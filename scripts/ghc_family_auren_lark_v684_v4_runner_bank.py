"""Execute Auren v684-v4 phase-local runner modules in bounded synthetic mode."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Any


def load_module(path: Path, index: int):
    spec = importlib.util.spec_from_file_location(f"_auren_runner_{index:02d}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def use_runner(path: Path, index: int) -> dict[str, Any]:
    module = load_module(path, index)
    fixture = {
        "synthetic": True,
        "real_row_count": 0,
        "authority_status": "reserved",
        "claim_scope": "bounded_synthetic_structure_only",
    }
    result = module.evaluate(fixture)
    raw = path.read_bytes()
    valid = (
        isinstance(result, dict)
        and result.get("accepted") is True
        and result.get("real_world_action") is False
        and result.get("authority_status") == "reserved"
    )
    return {
        "path": path.as_posix(),
        "valid": valid,
        "result": result,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def use_all(runner_root: Path) -> list[dict[str, Any]]:
    paths = sorted(runner_root.glob("ghc_family_*_runner.py"))
    return [use_runner(path, index) for index, path in enumerate(paths, 1)]
