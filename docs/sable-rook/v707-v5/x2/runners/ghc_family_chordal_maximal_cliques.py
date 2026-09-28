from __future__ import annotations
import json, sys
from pathlib import Path
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from common import FIXTURES
from x2_algorithms import evaluate_x2
print(json.dumps(evaluate_x2("maximal-cliques", FIXTURES[0]), sort_keys=True))
