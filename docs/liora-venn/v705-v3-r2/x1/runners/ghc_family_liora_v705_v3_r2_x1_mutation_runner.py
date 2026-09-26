from __future__ import annotations
import json, sys
from pathlib import Path
X1=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(X1/"code")); import event_workflow as ew
rows=ew.execute_mutations("x1"); print(json.dumps({"runner":"mutation","rejected":sum(r["rejected"] for r in rows),"total":len(rows)}))
raise SystemExit(0 if len(rows)==300 and all(r["rejected"] for r in rows) else 1)
