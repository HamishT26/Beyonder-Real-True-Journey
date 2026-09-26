from __future__ import annotations
import json
from pathlib import Path
X2=Path(__file__).resolve().parents[1];R=X2/"results";expected={"contracts.json":150,"mutations.json":300,"recoveries.json":150,"safe-tasks.json":400,"candidate-tasks.json":300,"clean-fix-refine-tasks.json":300,"models.json":15};observed={k:len(json.loads((R/k).read_text(encoding="utf-8"))) for k in expected};print(json.dumps({"runner":"receipt","observed":observed}));raise SystemExit(0 if observed==expected else 1)
