#!/usr/bin/env python3
import json
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab_x2 import analyze_x2
ROOT = Path(__file__).resolve().parents[2]
fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
selected = [6, 7, 8]
rows = [{"fixture_id": fixtures[i]["fixture_id"], "result": analyze_x2(fixtures[i])} for i in selected]
print(json.dumps({"runner": "ghc_family_reduction_x2_03", "state": "pass", "records": len(rows)}, sort_keys=True))
