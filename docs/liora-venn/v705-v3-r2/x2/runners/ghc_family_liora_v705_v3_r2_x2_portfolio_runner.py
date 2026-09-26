from __future__ import annotations
import json,sys
from pathlib import Path
sys.dont_write_bytecode=True;X2=Path(__file__).resolve().parents[1];sys.path.insert(0,str(X2/"code"));import event_workflow_x2 as ew
counts={k:len(ew.execute_portfolio("x2",k)) for k in ("safe","candidate","clean_fix_refine")};print(json.dumps({"runner":"portfolio","counts":counts}));raise SystemExit(0 if counts=={"safe":400,"candidate":300,"clean_fix_refine":300} else 1)
