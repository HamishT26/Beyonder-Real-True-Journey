#!/usr/bin/env python3
"""Manual uninstalled lifecycle-envelope candidate ghc_family_simplicial_hook_05."""
import json
import sys

try:
    payload = json.loads(sys.stdin.read())
except Exception:
    print(json.dumps({"hook": "ghc_family_simplicial_hook_05", "decision": "refuse", "reason": "invalid-json"}, sort_keys=True))
    raise SystemExit(2)
required = {"event", "owner", "phase", "exact_head"}
if set(payload) != required or payload.get("owner") != "Mira Fenwick" or payload.get("phase") != "v707-v3" or payload.get("event") not in {"planning", "x1", "x2", "final", "handoff"}:
    print(json.dumps({"hook": "ghc_family_simplicial_hook_05", "decision": "refuse", "reason": "invalid-envelope"}, sort_keys=True))
    raise SystemExit(2)
print(json.dumps({"hook": "ghc_family_simplicial_hook_05", "decision": "accept-manual-smoke-only", "event": payload["event"]}, sort_keys=True))
