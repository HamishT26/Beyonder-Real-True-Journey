from __future__ import annotations
import json,sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True; X2=Path(__file__).resolve().parents[1];sys.path.insert(0,str(X2/"code"));import event_workflow_x2 as ew
rows=ew.execute_all(); outcomes=Counter(r["disposition"] for r in rows);print(json.dumps({"runner":"contract","total":len(rows),"outcomes":outcomes}))
raise SystemExit(0 if len(rows)==150 and outcomes==Counter({"completed":105,"represented":15,"open_gap":15,"exact_gate":15}) else 1)
