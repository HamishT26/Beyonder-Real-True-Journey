#!/usr/bin/env python3
"""Minimal bounded validator runner for Ilyra v651-v8 evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
out=load("outcomes/x2-outcome-ledger.json"); truth=load("truth/evidence-phase-truth.json"); mut=load("validation/mutation-execution.json")
checks={"thirty_proposals":out["count"]==30,"four_labels":set(out["counts"])=={"completed","represented","open_gap","exact_gate"},"distribution":out["counts"]=={"completed":23,"represented":5,"open_gap":1,"exact_gate":1},"mutations":mut["rejected"]==150,"verdict":truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20","same_owner":truth["same_owner_only"] and not truth["independent_reproduction_claimed"]}
payload={"schema":"ghc.family.v651-v8.minimal-validator.v1","check_count":len(checks),"passed":sum(checks.values()),"issues":[k for k,v in checks.items() if not v],"checks":checks}
print(json.dumps(payload,sort_keys=True)); raise SystemExit(0 if not payload["issues"] else 1)
