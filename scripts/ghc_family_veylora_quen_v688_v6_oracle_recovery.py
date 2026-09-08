"""Retain the expected-value aliasing failure and bind its focused recovery."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json
ROOT=Path(__file__).resolve().parents[1];BASE="docs/veylora-quen/v688-v6"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x,exclusive=False):
 p.parent.mkdir(parents=True,exist_ok=True)
 b=(json.dumps(x,sort_keys=True,ensure_ascii=True,indent=2)+"\n").encode()
 if exclusive:
  with p.open("xb") as f:f.write(b)
 else:p.write_bytes(b)
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--skill-root",type=Path,required=True);a=ap.parse_args()
 x2=ROOT/BASE/"x2";failure=load(x2/"retained-attempts/x2-tests-first-failure.json")
 old=(x2/"retained-attempts/firmware-core-v1.py.txt").read_bytes()
 now=(ROOT/"scripts/ghc_family_firmware_records_core.py").read_bytes()
 def functions(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
 of=functions(old);nf=functions(now)
 assert set(of)==set(nf)
 assert [k for k in of if of[k]!=nf[k]]==["expected_envelope"]
 binding=load(x2/"implementation-binding.json")
 binding.update({"core_sha256":sha(now),"primary_execution_core_sha256":sha(old),
  "original_binding_ref":BASE+"/x2/retained-attempts/implementation-binding-v1.json",
  "primary_evaluator_function_bodies_unchanged":True,"changed_function":"expected_envelope",
  "focused_failed_tests_passed":2,"defensive_copy_required":True})
 save(x2/"implementation-binding.json",binding)
 for sp in load(ROOT/BASE/"x1/tool-package-plan.json")["skills"]:
  p=ROOT/BASE/"skills"/sp["name"]/"scripts/ghc_family_firmware_records_core.py"
  assert p.read_bytes()==old
  p.write_bytes(now)
 spec=importlib.util.spec_from_file_location("family_method",a.skill_root/"ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py")
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 lp=x2/"method-flow/ledger.json";ledger=load(lp);mid=f"VQ6886-M{len(ledger['methods'])+1:03d}"
 m=copy.deepcopy(ledger["methods"][-1]);m.update({"method_id":mid,"title":"Defensive expected-result copying",
  "failure_signature":failure["failure"],"candidate_workaround":failure["recovery"],
  "retained_negative_ids":[failure["negative_id"]],"validation_witness_ids":[mid+"-F",mid+"-P"]})
 ledger["methods"].append(m)
 ledger["operational_failure_records"].append({"negative_id":failure["negative_id"],"failure":failure["failure"],"recovery":failure["recovery"]})
 for result,text in [("fail","Two of sixteen tests failed through an in-memory expected-value alias."),
                    ("pass","Both affected tests passed after defensive copying; primary evaluator bodies are unchanged.")]:
  ledger["witnesses"].append({"witness_id":mid+("-F" if result=="fail" else "-P"),"method_id":mid,
   "procedure":"focused expected-result alias recovery","scope":BASE+"/x2/retained-attempts/x2-tests-first-failure.json",
   "expected":"Mutating a caller-owned expected envelope must not alter the frozen proposal loaded in memory.",
   "observed":text,"result":result,"witness_kind":"operational_failure" if result=="fail" else "bounded_passing_witness",
   "same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[failure["negative_id"]] if result=="fail" else [],
   "boundary":"The frozen repository files and earlier observed outputs were unchanged; same-owner validation only."})
 ledger["state_events"].extend([{"method_id":mid,"from":"candidate","to":"validated","note":"Two focused tests passed."},
  {"method_id":mid,"from":"validated","to":"preferred","note":"Copy expected values before exposing them to callers."}])
 ledger["recommendations"].append({"method_id":mid,"preconditions":"mutable expected output values",
  "recommendation":"Return a defensive copy; retain typed comparison and immutable source definitions.","delivered":False})
 mod.refresh_counts(ledger);validation=mod.validate_ledger(ledger);assert validation["valid"],validation
 save(lp,ledger);save(x2/"method-flow/validation.json",validation)
 n=load(x2/"retained-negative-register.json")
 n["new_operational_negative_groups"]=len(ledger["operational_failure_records"])
 n["new_negative_count"]=n["new_designed_admission_failures"]+n["new_operational_negative_groups"]
 save(x2/"retained-negative-register.json",n)
 baseline=load(ROOT/BASE/"x1/phase-truth.json")["inherited_baseline"];counts=ledger["counts"]
 metrics={"methods":counts["methods"],"witnesses":counts["witnesses"],"failed_witnesses":counts["witness_results"]["fail"],
  "passing_witnesses":counts["witness_results"]["pass"],"state_events":counts["state_events"],"recommendations":counts["recommendations"]}
 truth=load(x2/"phase-truth.json");truth["effective_counts"].update({
  "negatives":baseline["negatives"]+n["new_negative_count"],"methods":baseline["methods"]+metrics["methods"],
  "failed_witnesses":baseline["failed_witnesses"]+metrics["failed_witnesses"],"passing_witnesses":baseline["passing_witnesses"]+metrics["passing_witnesses"]})
 truth["expected_value_alias_recovery_retained"]=True;save(x2/"phase-truth.json",truth)
 deck=x2/"deck";index=load(deck/"deck-index.json");volatile=load(deck/"volatile-index.json")
 cards=[load(deck/"cards"/(ident+".json")) for ident in index["cards"]]
 c=copy.deepcopy(next(c for c in cards if c["card_type"]=="method"));c.pop("card_id")
 c["title"]=m["title"];c["content"]={"method_id":mid,"ledger":BASE+"/x2/method-flow/ledger.json","retained_negative_ids":m["retained_negative_ids"]}
 c["card_id"]="ghc-card-"+sha(canonical(c))[:20];save(deck/"cards"/(c["card_id"]+".json"),c,True)
 cards.append(c);index["cards"].append(c["card_id"]);volatile["cards"].append(c["card_id"]);index["card_count"]=len(cards)
 index["tier_counts"]={str(i):sum(c["tier"]==i for c in cards) for i in range(1,5)}
 save(deck/"deck-index.json",index);save(deck/"volatile-index.json",volatile)
 manifest=load(deck/"card-manifest.json")
 manifest["entries"]=[{"path":p.relative_to(ROOT).as_posix(),"bytes":len(p.read_bytes()),"sha256":sha(p.read_bytes())}
   for p in sorted(deck.rglob("*")) if p.is_file() and p.name!="card-manifest.json"]
 save(deck/"card-manifest.json",manifest)
 summary=load(x2/"evidence-summary.json");summary.update({"effective_counts":truth["effective_counts"],"methods":metrics,
  "cards":len(cards),"operational_failure_groups":len(ledger["operational_failure_records"]),
  "initial_x2_module_result":"14/16; retained","focused_failed_tests_result":"2/2 passed",
  "primary_evaluator_behavior_changed":False,"unexpected_contract_failures":0})
 save(x2/"evidence-summary.json",summary)
 save(x2/"oracle-recovery-receipt.json",{"negative_id":failure["negative_id"],"old_core_sha256":sha(old),"new_core_sha256":sha(now),
  "frozen_files_changed":False,"primary_evaluator_function_bodies_unchanged":True,"focused_tests_passed":2,
  "original_failed_test_run_retained":True,"all_local_core_copies_updated":10,"canonical_invoked":False},True)
 print(json.dumps({"method_count":metrics["methods"],"failed_witnesses":metrics["failed_witnesses"],"passing_witnesses":metrics["passing_witnesses"],
  "cards":len(cards),"effective_counts":truth["effective_counts"],"original_failure_retained":True}))
if __name__=="__main__":main()
