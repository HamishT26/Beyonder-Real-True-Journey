from __future__ import annotations
import json, sys
from pathlib import Path
X1=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(X1/"code")); import event_workflow as ew
counts={kind:len(ew.execute_portfolio("x1",kind)) for kind in ("safe","candidate","clean_fix_refine")}; print(json.dumps({"runner":"portfolio","counts":counts}))
raise SystemExit(0 if counts=={"safe":400,"candidate":300,"clean_fix_refine":300} else 1)
