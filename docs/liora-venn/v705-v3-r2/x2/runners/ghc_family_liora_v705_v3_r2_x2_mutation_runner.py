from __future__ import annotations
import json,sys
from pathlib import Path
sys.dont_write_bytecode=True;X2=Path(__file__).resolve().parents[1];sys.path.insert(0,str(X2/"code"));import event_workflow_x2 as ew
rows=ew.execute_mutations();print(json.dumps({"runner":"mutation","rejected":sum(r["rejected"] for r in rows),"total":len(rows)}));raise SystemExit(0 if len(rows)==300 and all(r["rejected"] for r in rows) else 1)
