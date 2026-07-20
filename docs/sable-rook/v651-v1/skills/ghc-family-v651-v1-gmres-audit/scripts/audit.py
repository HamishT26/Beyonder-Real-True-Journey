#!/usr/bin/env python3
import argparse,json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument("--contract",required=True); args=parser.parse_args()
data=json.loads(Path(args.contract).read_text(encoding="utf-8"))
required={"schema","proposal_id","slug","required_fields","expected_disposition","protected_gates","boundary"}
issues=[]
if not required <= set(data): issues.append("missing_contract_keys")
if not isinstance(data.get("required_fields"),list) or not data.get("required_fields"): issues.append("empty_obligations")
if data.get("expected_disposition") not in {"completed","represented","open_gap","exact_gate"}: issues.append("outcome_vocabulary")
result={"valid":not issues,"issues":issues,"slug":data.get("slug"),"boundary":"Phase-local structural smoke use only."}
print(json.dumps(result,ensure_ascii=False,sort_keys=True)); raise SystemExit(0 if result["valid"] else 2)
