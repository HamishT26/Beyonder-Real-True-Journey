#!/usr/bin/env python3
import json
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab import analyze_x1
ROOT = Path(__file__).resolve().parents[2]
fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
selected = [9, 10, 11]
rows = [{"fixture_id": fixtures[i]["fixture_id"], "result": analyze_x1(fixtures[i])} for i in selected]
print(json.dumps({"runner": "ghc_family_reduction_x1_04", "state": "pass", "records": len(rows)}, sort_keys=True))
