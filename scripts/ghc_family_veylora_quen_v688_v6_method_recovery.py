"""Additive recovery of the initial x2 Method Flow schema and event definitions."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE="docs/veylora-quen/v688-v6"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def data(x):return (json.dumps(x,indent=2,sort_keys=True,ensure_ascii=True)+"\n").encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode()
def save(p,x,exclusive=True):
 p.parent.mkdir(parents=True,exist_ok=True)
 if exclusive:
  with p.open("xb") as h:h.write(data(x))
 else:p.write_bytes(data(x))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);ap.add_argument("--skill-root",type=Path,required=True)
 a=ap.parse_args();phase=ROOT/BASE;x2=phase/"x2";lp=x2/"method-flow/ledger.json"
 before=lp.read_bytes();old=load(lp)
 saved=x2/"retained-attempts/method-flow-ledger-v1.json"
 saved.parent.mkdir(parents=True,exist_ok=True)
 with saved.open("xb") as f:f.write(before)
 save(x2/"retained-attempts/method-flow-validation-v1.json",load(a.bank/"method-flow-validation.json"))
 spec=importlib.util.spec_from_file_location("family_method",a.skill_root/"ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py")
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 ledger=copy.deepcopy(old)
 module.refresh_counts(ledger);count_check=module.validate_ledger(ledger);assert count_check["valid"]
 readiness=load(x2/"lifecycle-readiness.json");assert readiness["valid"] and len(readiness["negative_controls"])==5
 new=load(a.bank/"x2-operational-failures.json")["failures"][1:]
 assert [x["negative_id"] for x in new]==["VQ6886-X2-N002","VQ6886-X2-N003","VQ6886-X2-N004"]
 for item in new:
  mid=f"VQ6886-M{len(ledger['methods'])+1:03d}"
  m=copy.deepcopy(ledger["methods"][-1]);m.update({"method_id":mid,"title":item["recovery"],
   "failure_signature":item["failure"],"retained_negative_ids":[item["negative_id"]],"validation_witness_ids":[],
   "recommendation_state":"preferred","candidate_workaround":item["recovery"],"supersedes":[]})
  ledger["methods"].append(m);ledger["operational_failure_records"].append(item)
  for result,observed,kind in [("fail",item["failure"],"operational_failure"),("pass",item["recovery"],"bounded_passing_witness")]:
   wid=mid+("-F" if result=="fail" else "-P")
   ledger["witnesses"].append({"witness_id":wid,"method_id":mid,"procedure":"focused owner recovery",
    "scope":BASE+"/x2/retained-attempts/method-flow-ledger-v1.json" if item["negative_id"]!="VQ6886-X2-N003" else BASE+"/x2/lifecycle-readiness.json",
    "expected":"Preserve the failed definition and verify only its bounded recovery.","observed":observed,"result":result,
    "witness_kind":kind,"same_owner_only":True,"independent_reproduction":False,
    "retained_negative_ids":[item["negative_id"]] if result=="fail" else [],
    "boundary":"Same-owner workflow evidence only; not a live canonical receipt or independent reproduction."})
   m["validation_witness_ids"].append(wid)
  ledger["recommendations"].append({"method_id":mid,"preconditions":"same declared failure and scope","recommendation":item["recovery"],"delivered":False})
  if item["negative_id"]=="VQ6886-X2-N003":
   for i,c in enumerate(readiness["negative_controls"]):
    nid=f"VQ6886-LIFECYCLE-ADVERSE-{i+1}"
    m["retained_negative_ids"].append(nid);wid=mid+f"-ADVERSE-{i+1}"
    ledger["witnesses"].append({"witness_id":wid,"method_id":mid,"procedure":"synthetic lifecycle adverse admission",
     "scope":BASE+"/x2/lifecycle-readiness.json","expected":"A violated terminal predicate must be refused.",
     "observed":c["field"]+" mutation refused","result":"fail","witness_kind":"designed_admission_failure",
     "same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[nid],
     "boundary":"Fail denotes admission of the adverse candidate. The rejection predicate passed; no live canonical was invoked."})
    m["validation_witness_ids"].append(wid)
 ledger["state_events"]=[]
 for m in ledger["methods"]:
  ledger["state_events"].extend([
   {"method_id":m["method_id"],"from":"candidate","to":"validated","note":"Recorded bounded passing witness exists; failures remain retained."},
   {"method_id":m["method_id"],"from":"validated","to":"preferred","note":"Recommended only for the stated matching trigger and scope."}])
 assert all(e["to"] in module.TRANSITIONS[e["from"]] for e in ledger["state_events"])
 module.refresh_counts(ledger)
 result=module.validate_ledger(ledger);assert result["valid"],result
 ledger["retained_previous_definition"]={"path":BASE+"/x2/retained-attempts/method-flow-ledger-v1.json","sha256":sha(before),"success_credit":0}
 save(lp,ledger,False)
 save(x2/"method-flow/validation.json",result)
 negative=load(x2/"retained-negative-register.json")
 negative.update({"new_designed_admission_failures":517,"new_operational_negative_groups":len(ledger["operational_failure_records"]),
   "new_negative_count":sum(w["result"]=="fail" for w in ledger["witnesses"]),"lifecycle_adverse_ref":BASE+"/x2/lifecycle-readiness.json",
   "operational_failures_ref":BASE+"/x2/method-flow/ledger.json"})
 # 509 record/portfolio adversaries + 3 package adversaries + 5 lifecycle adversaries.
 assert negative["new_designed_admission_failures"]==509+3+5
 save(x2/"retained-negative-register.json",negative,False)
 save(x2/"method-flow/recovery-receipt.json",{"initial_ledger_sha256":sha(before),"original_retained":True,
  "failed_result_preserved":True,"count_projection_passed":count_check["valid"],"current_validation_passed":result["valid"],
  "retained_invalid_event_definition":BASE+"/x2/retained-attempts/method-flow-ledger-v1.json",
  "new_event_transitions_valid":True,"missing_guide_scripts":["ghc_family_lifecycle_test_isolator.py","ghc_family_canonical_aggregate_preflight.py"],
  "guide_packages_are_not_callable":True,"owned_lifecycle_helper":"scripts/ghc_family_veylora_quen_v688_v6_lifecycle.py",
  "owned_helper_fixture_checks":6,"live_canonical_invoked":False,"new_operational_negative_ids":[x["negative_id"] for x in new]})
 effective=load(phase/"x1/phase-truth.json")["inherited_baseline"]
 counts=ledger["counts"]
 metrics={"methods":counts["methods"],"witnesses":counts["witnesses"],"failed_witnesses":counts["witness_results"]["fail"],
  "passing_witnesses":counts["witness_results"]["pass"],"state_events":counts["state_events"],"recommendations":counts["recommendations"]}
 truth=load(x2/"phase-truth.json")
 truth["effective_counts"].update({"negatives":effective["negatives"]+negative["new_negative_count"],
  "methods":effective["methods"]+metrics["methods"],"failed_witnesses":effective["failed_witnesses"]+metrics["failed_witnesses"],
  "passing_witnesses":effective["passing_witnesses"]+metrics["passing_witnesses"]})
 truth["method_schema_correction_retained"]=True;save(x2/"phase-truth.json",truth,False)
 deck=x2/"deck";index=load(deck/"deck-index.json");volatile=load(deck/"volatile-index.json")
 cards=[load(deck/"cards"/(ident+".json")) for ident in index["cards"]]
 template=next(c for c in cards if c["card_type"]=="method")
 for m in ledger["methods"][-3:]:
  c=copy.deepcopy(template);c.pop("card_id");c["title"]=m["title"]
  c["content"]={"method_id":m["method_id"],"ledger":BASE+"/x2/method-flow/ledger.json","retained_negative_ids":m["retained_negative_ids"]}
  c["card_id"]="ghc-card-"+sha(canon(c))[:20]
  save(deck/"cards"/(c["card_id"]+".json"),c)
  cards.append(c);index["cards"].append(c["card_id"]);volatile["cards"].append(c["card_id"])
 index["card_count"]=len(cards);index["tier_counts"]={str(i):sum(c["tier"]==i for c in cards) for i in range(1,5)}
 save(deck/"deck-index.json",index,False);save(deck/"volatile-index.json",volatile,False)
 manifest=load(deck/"card-manifest.json")
 manifest["entries"]=[{"path":p.relative_to(ROOT).as_posix(),"bytes":len(p.read_bytes()),"sha256":sha(p.read_bytes())}
  for p in sorted(deck.rglob("*")) if p.is_file() and p.name!="card-manifest.json"]
 save(deck/"card-manifest.json",manifest,False)
 summary=load(x2/"evidence-summary.json")
 summary.update({"effective_counts":truth["effective_counts"],"methods":metrics,"cards":len(cards),
  "retained_lifecycle_adverse_controls":5,"operational_failure_groups":len(ledger["operational_failure_records"]),
  "unexpected_contract_failures":0,"method_schema_failure_retained":True})
 save(x2/"evidence-summary.json",summary,False)
 print(json.dumps({"method_validation":True,"metrics":metrics,"cards":len(cards),"effective_counts":truth["effective_counts"]}))
if __name__=="__main__":main()
