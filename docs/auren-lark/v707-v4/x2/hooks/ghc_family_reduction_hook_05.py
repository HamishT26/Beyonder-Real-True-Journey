#!/usr/bin/env python3
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab_x2 import analyze_x2
MECHANISM = 'relabel-covariance'
def handle(payload):
    if not isinstance(payload, dict) or "fixture" not in payload:
        raise ValueError("invalid_hook_envelope")
    result = analyze_x2(payload["fixture"])[MECHANISM]
    return {"hook": "ghc_family_reduction_hook_05", "mechanism": MECHANISM, "state": "pass", "result": result}
