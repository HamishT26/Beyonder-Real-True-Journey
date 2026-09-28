#!/usr/bin/env python3
"""Saved-evidence reader for ghc_family_simplicial_x2_04; it never reruns the domain solver."""
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
rows = payload["results"]
print(json.dumps({"runner": "ghc_family_simplicial_x2_04", "stage": "x2", "saved_records": len(rows), "source": str(path.name)}, sort_keys=True))
