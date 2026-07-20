#!/usr/bin/env python3
"""Validate an arbitrary sanitized GHC workflow-plan audit without demo-packet coupling."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--audit", required=True)
    p.add_argument("--receipt", required=True)
    a=p.parse_args()
    data=json.loads(Path(a.audit).read_text(encoding="utf-8"))
    cycle=data.get("cycle",[])
    checks={
        "valid":data.get("valid") is True,
        "eight_unique_seats":len(cycle)==8 and len(set(cycle))==8,
        "current_and_next":data.get("current_phase")=="v649-v7" and data.get("next_phase")=="v649-v8",
        "next_owner":data.get("next_owner")=="Elaren Kestrel",
        "future_identity_unset":data.get("future_sibling_identity_set") is False,
        "twenty_proposal_floor":data.get("proposal_floor",0)>=20,
        "commit_cap":data.get("commit_cap",{}).get("total")<=4,
        "one_pass":data.get("successful_validation_pass_budget")==1 and data.get("post_success_replay") is False,
        "user_mediated_external":data.get("cross_platform_contact")=="user_mediated_only",
    }
    payload={"schema":"ghc.family.workflow-plan.general-validation.v1","passed":all(checks.values()),"checks":checks,"authority_credit":False,"activation_effect":False}
    Path(a.receipt).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(payload,sort_keys=True))
    return 0 if payload["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
