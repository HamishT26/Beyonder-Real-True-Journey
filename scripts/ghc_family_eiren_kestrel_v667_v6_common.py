#!/usr/bin/env python3
"""Shared bounded smoke surface for Eiren v667-v6 family-current runners."""
from __future__ import annotations
import argparse
import json

ALLOWED = {"contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"}

def run(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if name not in ALLOWED or not args.smoke:
        return 2
    print(json.dumps({"runner": name, "status": "completed", "scope": "bounded_phase_local_smoke", "external_writes": 0, "real_world_actions": 0}))
    return 0
