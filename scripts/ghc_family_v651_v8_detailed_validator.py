#!/usr/bin/env python3
"""Detailed bounded validator runner for Ilyra v651-v8 evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
checks=[]
def check(name, condition): checks.append({"name":name,"passed":bool(condition)})
out=load("outcomes/x2-outcome-ledger.json"); mut=load("validation/mutation-execution.json")
skills=load("validation/skill-validation.json"); port=load("portfolios/expanded-portfolio-execution.json")
truth=load("truth/evidence-phase-truth.json"); seats=load("provenance/future-cli-x2-invariant.json")
check("proposal_count",out["count"]==30); check("outcome_distribution",out["counts"]=={"completed":23,"represented":5,"open_gap":1,"exact_gate":1})
check("outcome_vocabulary",set(out["counts"])=={"completed","represented","open_gap","exact_gate"})
check("mutations",mut["count"]==150 and mut["rejected"]==150 and mut["all_rejected"])
check("skills",skills["count"]==20 and skills["valid"] and skills["global_install_count"]==0)
check("portfolios",port["counts"]=={"safe_now":40,"candidate":30,"skills":20,"runners":12,"clean_fix_refine":40} and port["all_resolved"])
check("negatives",truth["effective_negatives"]==7736); check("gaps",truth["effective_open_gaps"]==60); check("gates",truth["effective_exact_gates"]==61)
check("verdict",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20"); check("full_suite",truth["full_suite_state"]=="not_run_by_non_eiren_owner")
check("same_owner",truth["same_owner_only"] and not truth["independent_reproduction_claimed"])
check("future_seats",seats["prepared_count"]==8 and seats["named_count"]==0 and seats["created_count"]==0 and seats["launched_count"]==0)
payload={"schema":"ghc.family.v651-v8.detailed-validator.v1","check_count":len(checks),"passed":sum(c["passed"] for c in checks),"issues":[c["name"] for c in checks if not c["passed"]],"checks":checks}
print(json.dumps(payload,sort_keys=True)); raise SystemExit(0 if not payload["issues"] else 1)
