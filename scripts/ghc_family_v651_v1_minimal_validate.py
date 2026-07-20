#!/usr/bin/env python3
"""Minimal fail-closed validator for Sable Rook v651-v1."""
import json
from pathlib import Path
ROOT=Path("docs/sable-rook/v651-v1")
checks=[]
def c(name, value): checks.append({"check":name,"passed":bool(value)})
p=json.loads((ROOT/"preregistration/proposals.json").read_text(encoding="utf-8"))
o=json.loads((ROOT/"outcomes/outcome-ledger.json").read_text(encoding="utf-8"))
t=json.loads((ROOT/"truth/evidence-phase-truth.json").read_text(encoding="utf-8"))
c("proposal_count",p["proposal_count"]==20); c("outcome_count",len(o["outcomes"])==20)
c("terminal",t["terminal_verdict"]=="NOT_READY_FOR_STAGE_20"); c("route",t["terminal_route"]=="PREPARED_NOT_SENT")
c("no_full_suite",t["full_repository_suite_claimed"] is False); c("no_independent",t["independent_reproduction_claimed"] is False)
r={"schema":"ghc.family.v651-v1.minimal-validation.v1","checks":checks,"passed":sum(x["passed"] for x in checks),"total":len(checks),"valid":all(x["passed"] for x in checks)}
print(json.dumps(r,sort_keys=True)); raise SystemExit(0 if r["valid"] else 2)
