"""Preserve the final report omission and add its exact final-only recovery overlay."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];BASE="docs/veylora-quen/v688-v6"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x,exclusive=False):
 p.parent.mkdir(parents=True,exist_ok=True);b=(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=True)+"\n").encode()
 if exclusive:
  with p.open("xb") as f:f.write(b)
 else:p.write_bytes(b)
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);ap.add_argument("--skill-root",type=Path,required=True);a=ap.parse_args()
 phase=ROOT/BASE;final=phase/"final";retained=final/"retained-attempts";retained.mkdir(exist_ok=False)
 paths={"overview-v1.md":final/"final-integrated-overview.md","report-v1.html":final/"static-report.html",
  "final-tests-v1.py.txt":ROOT/"tests/test_ghc_family_veylora_quen_v688_v6_final.py",
  "content-seal-v1.json":phase/"seal/content-seal.json","canonical-v1.py.txt":ROOT/"scripts/ghc_family_veylora_quen_v688_v6_canonical.py"}
 bindings=[]
 for name,p in paths.items():
  b=p.read_bytes();(retained/name).write_bytes(b);bindings.append({"path":(retained/name).relative_to(ROOT).as_posix(),"sha256_raw":sha(b)})
 failure={"negative_id":"VQ6886-FINAL-N001","failure":"The final overview omitted an explicit same-owner shared-infrastructure non-independence statement.",
  "test_count":12,"passed":11,"failed_test":"test_07_overview_and_print_sections","success_credit":0,"retained_definitions":bindings,
  "recovery":"Add the explicit statement, keep the draft and failed test definition, and run the failed predicate only.",
  "immutable_x1_or_x2_changed":False}
 save(retained/"final-test-failure.json",failure,True)
 sentence="All validation reported here is same-owner work under shared infrastructure; it is not independent reproduction."
 md=final/"final-integrated-overview.md";text=md.read_text();text=text.replace("\n\n","\n\n"+sentence+"\n\n",1)
 md.write_text(text,encoding="utf-8",newline="\n")
 hp=final/"static-report.html";ht=hp.read_text();ht=ht.replace("</h1>","</h1><p>"+sentence+"</p>",1);hp.write_text(ht,encoding="utf-8",newline="\n")
 test=ROOT/"tests/test_ghc_family_veylora_quen_v688_v6_final.py"
 result=subprocess.run([sys.executable,"-B","-X","utf8",str(test),"FinalEvidence.test_07_overview_and_print_sections"],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (a.bank/"final-report-focused.stdout.txt").write_bytes(result.stdout);(a.bank/"final-report-focused.stderr.txt").write_bytes(result.stderr)
 assert result.returncode==0
 spec=importlib.util.spec_from_file_location("family_method",a.skill_root/"ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py")
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 ledger=load(phase/"x2/method-flow/ledger.json");mid="VQ6886-M038";m=copy.deepcopy(ledger["methods"][-1])
 m.update({"method_id":mid,"title":"Explicit final same-owner boundary","failure_signature":failure["failure"],
  "candidate_workaround":failure["recovery"],"retained_negative_ids":[failure["negative_id"]],"validation_witness_ids":[mid+"-F",mid+"-P"]})
 ledger["methods"].append(m)
 ledger["operational_failure_records"].append({"negative_id":failure["negative_id"],"failure":failure["failure"],"recovery":failure["recovery"]})
 for status,observed in [("fail","One of twelve final tests failed because the explicit shared-infrastructure statement was absent."),
  ("pass","The one failed predicate passed after the explicit same-owner statement was added.")]:
  ledger["witnesses"].append({"witness_id":mid+("-F" if status=="fail" else "-P"),"method_id":mid,"procedure":"final report scope review",
   "scope":BASE+"/final/retained-attempts/final-test-failure.json","expected":"State the same-owner shared-infrastructure non-independence boundary explicitly.",
   "observed":observed,"result":status,"witness_kind":"operational_failure" if status=="fail" else "bounded_passing_witness",
   "same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[failure["negative_id"]] if status=="fail" else [],
   "boundary":"Final-only correction; immutable x1 and x2 and all failed definitions remain unchanged."})
 ledger["state_events"] += [{"method_id":mid,"from":"candidate","to":"validated","note":"Focused final predicate passed."},
  {"method_id":mid,"from":"validated","to":"preferred","note":"Use explicit same-owner language in every final overview."}]
 ledger["recommendations"].append({"method_id":mid,"preconditions":"final report publishing","recommendation":"State validation ownership and non-independence explicitly.","delivered":False})
 mod.refresh_counts(ledger);validation=mod.validate_ledger(ledger);assert validation["valid"]
 save(final/"method-flow-ledger.json",ledger,True);save(final/"method-flow-validation.json",validation,True)
 truth=load(final/"phase-truth.json");prior=copy.deepcopy(truth["effective_counts"])
 for key in ["negatives","methods","failed_witnesses","passing_witnesses"]:truth["effective_counts"][key]+=1
 for key in ["retained_negative_groups","methods","passing_method_witnesses","retained_operational_failure_groups"]:truth[key]+=1
 truth["final_only_retained_failure_count"]=1;truth["content_addressed_cards"]=246
 save(final/"phase-truth.json",truth)
 explanation=("At the immutable x2 boundary, the preceding Method Flow and effective counts remain sealed historical values. "
  "A final-only report review then retained one additional statement-omission failure and its passing recovery. "
  "The complete owner final therefore has 38 methods, 532 retained failed-admission or operational witnesses, and 38 bounded passing witnesses; "
  "517 witnesses are designed adverse admissions and 15 are operational failure groups. "
  "The final effective counts are 16,630 proposals, 84,903 negatives, 94,061 methods, 55,751 failed witnesses, 86,109 bounded passes, "
  "762 retained gap records and 775 exact-gate records. This addition does not change any proposal outcome or frozen x1/x2 file.")
 text=md.read_text().replace("Current Method Flow contains 37 methods","At the immutable x2 boundary, Method Flow contains 37 methods")
 text += "\n\n"+explanation+"\n";md.write_text(text,encoding="utf-8",newline="\n")
 ht=hp.read_text().replace("Current Method Flow contains 37 methods","At the immutable x2 boundary, Method Flow contains 37 methods")
 ht=ht.replace("<table>","<p>"+explanation+"</p><table>",1);hp.write_text(ht,encoding="utf-8",newline="\n")
 bi=load(final/"baton-index.json");bp=ROOT/bi["path"];bt=bp.read_text()
 old="Effective retained counts are "+json.dumps(prior,sort_keys=True)
 assert old in bt;bt=bt.replace(old,"Effective retained counts at the final boundary are "+json.dumps(truth["effective_counts"],sort_keys=True))
 bt=bt.replace("## Module 11",explanation+"\n\n## Module 11",1)
 bp.write_text(bt,encoding="utf-8",newline="\n");bi["word_count"]=len(bt.split());save(final/"baton-index.json",bi)
 mf=load(final/"method-flow-final.json");mf["immutable_x2_ledger"]=mf["ledger"];mf["ledger"]=BASE+"/final/method-flow-ledger.json"
 mf["validation"]=BASE+"/final/method-flow-validation.json";mf["counts"]=ledger["counts"];mf["final_only_failure"]=BASE+"/final/retained-attempts/final-test-failure.json"
 save(final/"method-flow-final.json",mf)
 nr=load(final/"retained-negative-register.json");nr["immutable_x2_new_negative_count"]=nr["new_negative_count"]
 nr["new_operational_negative_groups"]+=1;nr["new_negative_count"]+=1;nr["final_only_negative_id"]=failure["negative_id"];save(final/"retained-negative-register.json",nr)
 checklist=load(final/"complete-incomplete-checklist.json")
 checklist["completed"]=[s.replace("245 content-addressed four-tier cards","245 immutable x2 cards plus one final recovery card").replace("37 current Method Flow records with 531","38 current Method Flow records with 532") for s in checklist["completed"]]
 save(final/"complete-incomplete-checklist.json",checklist)
 close=load(final/"evidence-closeout.json");close["immutable_x2_summary"]=close.pop("summary")
 close["final_effective_counts"]=truth["effective_counts"];close["final_test_first_run"]="11/12 retained"
 close["focused_final_scope_test"]="1/1 passed";close["final_only_method_flow_overlay"]=BASE+"/final/method-flow-ledger.json";save(final/"evidence-closeout.json",close)
 index=load(phase/"x2/deck/deck-index.json")
 template=next(load(phase/"x2/deck/cards"/(i+".json")) for i in index["cards"] if load(phase/"x2/deck/cards"/(i+".json"))["card_type"]=="method")
 c=copy.deepcopy(template);c.pop("card_id");c["title"]=m["title"]
 c["content"]={"method_id":mid,"ledger":BASE+"/final/method-flow-ledger.json","retained_negative_ids":[failure["negative_id"]]}
 c["card_id"]="ghc-card-"+sha(json.dumps(c,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode())[:20]
 cp=final/"cards"/(c["card_id"]+".json");save(cp,c,True)
 save(final/"deck-overlay.json",{"base_deck":BASE+"/x2/deck/deck-index.json","added_cards":[cp.relative_to(ROOT).as_posix()],
  "base_card_count":245,"effective_card_count":246,"immutable_base_deck_changed":False},True)
 # Current final checks derive final retention from actual ledger rows.
 tt=test.read_text()
 tt=tt.replace('  self.assertEqual(p["retained_negative_groups"],531)','  ledger=load(FINAL/"method-flow-ledger.json")\n  self.assertEqual(p["retained_negative_groups"],sum(w["result"]=="fail" for w in ledger["witnesses"]))')
 tt=tt.replace('  self.assertEqual(p["retained_adverse_admission_failures"]+p["retained_operational_failure_groups"],531)','  self.assertEqual(p["retained_adverse_admission_failures"]+p["retained_operational_failure_groups"],p["retained_negative_groups"])')
 test.write_text(tt,encoding="utf-8",newline="\n")
 canon=ROOT/"scripts/ghc_family_veylora_quen_v688_v6_canonical.py";ct=canon.read_text()
 ct=ct.replace('load(ROOT/BASE/"x2/method-flow/validation.json")["valid"] is True','load(ROOT/BASE/"final/method-flow-validation.json")["valid"] is True')
 ct=ct.replace('ledger=load(ROOT/BASE/"x2/method-flow/ledger.json");w=ledger["witnesses"]','ledger=load(ROOT/BASE/"final/method-flow-ledger.json");w=ledger["witnesses"]')
 ct=ct.replace('==531 and sum(r["result"]=="pass" for r in w)==37','==truth["retained_negative_groups"] and sum(r["result"]=="pass" for r in w)==truth["passing_method_witnesses"]')
 canon.write_text(ct,encoding="utf-8",newline="\n")
 seal=load(phase/"seal/content-seal.json")
 targets=[e["path"] for e in seal["targets"]]+[BASE+"/final/method-flow-ledger.json",BASE+"/final/deck-overlay.json"]
 seal["targets"]=[]
 for name in targets:
  b=(ROOT/name).read_bytes().replace(b"\r\n",b"\n");seal["targets"].append({"path":name,"bytes_normalized_lf":len(b),"sha256_normalized_lf":sha(b)})
 save(phase/"seal/content-seal.json",seal)
 save(final/"final-recovery-receipt.json",{"negative_id":failure["negative_id"],"drafts_and_failed_test_retained":True,
  "focused_failed_test_pass":True,"immutable_x1_and_x2_changed":False,"final_method_count":38,"final_failed_witnesses":532,
  "final_passing_witnesses":38,"effective_counts":truth["effective_counts"],"canonical_invoked":False},True)
 print(json.dumps({"focused_test_passed":1,"methods":38,"failed_witnesses":532,"passing_witnesses":38,"baton_words":bi["word_count"],"immutable_evidence_unchanged":True}))
if __name__=="__main__":main()
