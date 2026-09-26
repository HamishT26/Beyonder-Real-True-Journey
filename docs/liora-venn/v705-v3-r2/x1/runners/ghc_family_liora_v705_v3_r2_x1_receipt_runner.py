from __future__ import annotations
import json
from pathlib import Path
X1=Path(__file__).resolve().parents[1]; results=X1/"results"
expected={"contracts.json":150,"mutations.json":300,"recoveries.json":150,"safe-tasks.json":400,"candidate-tasks.json":300,"clean-fix-refine-tasks.json":300}
observed={name:len(json.loads((results/name).read_text(encoding="utf-8"))) for name in expected}
print(json.dumps({"runner":"receipt","observed":observed,"expected":expected}))
raise SystemExit(0 if observed==expected else 1)
