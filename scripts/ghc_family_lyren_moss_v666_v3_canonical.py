#!/usr/bin/env python3
"""Terminal canonical entrypoint; a probe never invokes the aggregate."""
from __future__ import annotations
import json
import sys
if __name__ == "__main__":
    if sys.argv[1:] == ["--probe"]:
        print(json.dumps({"runner": "canonical", "interface": "available", "aggregate_invoked": False, "valid": True}, sort_keys=True))
    else:
        raise SystemExit("terminal canonical execution requires the dedicated final completion builder")
