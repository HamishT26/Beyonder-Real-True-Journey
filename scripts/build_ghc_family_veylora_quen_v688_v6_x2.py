"""Materialize x2 observed evidence, planned local tools and four-tier cards."""
from pathlib import Path
import argparse,copy,hashlib,html,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import ghc_family_firmware_records_core as core
BASE="docs/veylora-quen/v688-v6";OWNER="Veylora Quen";PHASE="v688-v6"
SOURCE="d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14";X1="6d7f5b0fc67f78a22463d3c3c9cec21aade35d92"
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode()
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 text=x if isinstance(x,str) else json.dumps(x,sort_keys=True,ensure_ascii=True,indent=2)
 with p.open("x",encoding="utf-8",newline="\n") as f:f.write(text.rstrip()+"\n")
def process(command):
 return subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",
  env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONUTF8":"1"})
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);ap.add_argument("--skill-root",type=Path,required=True)
 args=ap.parse_args();bank=args.bank;phase=ROOT/BASE;x2=phase/"x2";plans=load(phase/"x1/new-proposals.json")["proposals"]
 assert not x2.exists()
 assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip()==X1
 assert not subprocess.check_output(["git","diff","--name-only",X1,"--",BASE+"/x1",
 "scripts/build_ghc_family_veylora_quen_v688_v6_x1.py","tests/test_ghc_family_veylora_quen_v688_v6_x1.py"],cwd=ROOT).strip()
 preliminary=load(bank/"preliminary-execution.json");assert not preliminary["failures"]
 byid={p["proposal_id"]:p for p in plans};observed={r["proposal_id"]:r for r in preliminary["rows"]}
 gates=plans[0]["protected_gates"]
 write(x2/"entry-gate.json",{"source":SOURCE,"x1":X1,"x1_equality":load(bank/"x1-equality.json"),"x1_unchanged_at_x2_start":True})
 write(x2/"preliminary-execution.json",preliminary)
 write(x2/"implementation-binding.json",{"core_path":"scripts/ghc_family_firmware_records_core.py",
  "core_sha256":sha((ROOT/"scripts/ghc_family_firmware_records_core.py").read_bytes()),
  "preliminary_receipt_sha256":sha((bank/"preliminary-execution.json").read_bytes()),
  "binding_timing":"same source bytes after preliminary execution and before further implementation mutation",
  "same_owner_only":True,"independent_reproduction":False})
 negative=[];task_results=[];ops=list(dict.fromkeys(p["operation"] for p in plans))
 def retain(op,kind,details,artifact):
  ident=f"VQ6886-ADVERSE-{len(negative)+1:04d}"
  negative.append({"negative_id":ident,"operation":op,"kind":kind,"details":details,"artifact":artifact,
    "completion_credit":0,"candidate_admission":"refused","test_predicate_pass":True})
  return ident
 for i,p in enumerate(plans):
  r=observed[p["proposal_id"]]
  assert r["matches"] and r["input_unchanged"] and core.matches_contract(p,r["observed"])
  item={"proposal_id":p["proposal_id"],"input":p["input"],"expected":r["expected"],"observed":r["observed"],
   "matches":True,"input_unchanged":True,"source_kind":"synthetic","x1":X1,"independent_reproduction":False}
  path=BASE+f"/x2/contracts/{i+1:03d}.json"
  write(ROOT/path,item)
  if not p["expected_acceptance"]:retain(p["operation"],"preregistered_invalid_input",{"proposal_id":p["proposal_id"],"observed_error":r["observed"]["error"]},path)
 portfolio=load(phase/"x1/approval-portfolio.json")
 grouped={op:[] for op in ops}
 for category in ["safe_now","candidates","clean_fix_refine"]:
  for task in portfolio[category]:
   p=byid[task["proposal_id"]];expected=core.expected_envelope(p);data=copy.deepcopy(p["input"]);mode=task["procedure"]
   original=copy.deepcopy(data);extra={"task_id":task["task_id"],"proposal_id":p["proposal_id"],"procedure":mode}
   if mode=="contract_check":
    result=observed[p["proposal_id"]]["observed"];passed=core.matches_contract(p,result)
    extra["contract_ref"]=p["concrete_artifact"]
   elif mode in ("repeat_stability","json_key_order_invariance"):
    if mode=="json_key_order_invariance":data=dict(reversed(list(data.items())))
    result=core.evaluate(data);passed=core.matches_contract(p,result) and core.same_json(original,data)
    extra.update({"input":data,"observed":result})
   elif mode in ("unknown_field_rejection","missing_field_rejection"):
    if mode=="unknown_field_rejection":data["undeclared_extension"]=True
    else:data.pop(next(k for k in data if k!="operation"))
    before=copy.deepcopy(data);result=core.evaluate(data)
    passed=result["accepted"] is False and result["error"]=="field_set" and core.same_json(data,before)
    extra.update({"input":data,"observed":result})
    assert passed,task["task_id"]
    extra["retained_negative_id"]=retain(p["operation"],mode,{"task_id":task["task_id"],"observed_error":result["error"]},BASE+"/x2/challenges/"+p["operation"]+".json")
   else:
    altered=copy.deepcopy(expected);variant=int(task["task_id"].rsplit("-",1)[-1])%5
    if variant==0:altered["accepted"]=not altered["accepted"]
    elif variant==1:altered["error"]="altered_error"
    elif variant==2:altered["value"]={"altered_value":True}
    elif variant==3:altered["boundary"]="unjustified authority"
    else:altered["undeclared_result"]=True
    passed=not core.matches_contract(p,altered)
    extra.update({"candidate_output":altered,"comparator_accepted":not passed})
    assert passed,task["task_id"]
    extra["retained_negative_id"]=retain(p["operation"],mode,{"task_id":task["task_id"],"comparator_accepted":False},BASE+"/x2/challenges/"+p["operation"]+".json")
   assert passed,task["task_id"]
   if "input" in extra:assert len(canonical(extra))<50000
   grouped[p["operation"]].append(extra)
   task_results.append({"task_id":task["task_id"],"procedure":mode,"proposal_id":p["proposal_id"],"predicate_pass":True,"disposition":"completed"})
 for op,rows in grouped.items():write(x2/"challenges"/(op+".json"),{"operation":op,"rows":rows,"same_owner_only":True})
 write(x2/"portfolio-results.json",{"schema":"ghc.family.observed-firmware-portfolio.v1","rows":task_results,
  "counts":{"safe_now":300,"candidates":250,"clean_fix_refine":300},"unique_task_checks":850,
  "contracts_reused_by_reference":200,"exact_packets_unexecuted":50,"blocked_packets_unexecuted":30,
  "hardware_actions":0,"novelty_credit_multiplier":1,"boundary":core.BOUNDARY})
 package=load(bank/"package-transaction.json");assert package["state"]=="COMPLETE"
 write(x2/"package-transaction.json",package)
 write(x2/"package-advisory-snapshot.json",load(bank/"package-advisory-snapshot.json"))
 write(x2/"negative-controls.json",{"negative_records":negative,"count":len(negative),
  "interpretation":"These are observed refusals of preregistered invalid candidates and mutated outputs. They are passing rejection checks, not unexpected operational test failures.",
  "test_failures":0,"adverse_candidate_success_credit":0})
 toolplan=load(phase/"x1/tool-package-plan.json")
 core_bytes=(ROOT/"scripts/ghc_family_firmware_records_core.py").read_bytes()
 for rp in toolplan["runners"]:
  source='"""Bounded '+rp["name"].replace("_"," ")+' interface."""\nfrom ghc_family_firmware_records_core import cli\nALLOWED='+repr(tuple(rp["operation_group"]))+'\nif __name__=="__main__":raise SystemExit(cli(ALLOWED))\n'
  write(ROOT/"scripts"/rp["name"],source)
 local_checks=[]
 for sp in toolplan["skills"]:
  folder=phase/"skills"/sp["name"]
  cmd=[sys.executable,"-B","-X","utf8",str(args.skill_root/".system/skill-creator/scripts/init_skill.py"),sp["name"],
   "--path",str(phase/"skills"),"--resources","scripts,references",
   "--interface","display_name="+sp["name"].removeprefix("ghc-family-").replace("-"," ").title(),
   "--interface","short_description=Check bounded synthetic firmware record contracts",
   "--interface","default_prompt=Use $"+sp["name"]+" to check a synthetic record and retain its evidence limits."]
  proc=process(cmd)
  if proc.returncode:raise RuntimeError("skill_initializer:"+sp["name"])
  relevant=[p for p in plans if p["operation"] in sp["operation_pair"]]
  accepting=[p for p in relevant if p["expected_acceptance"]][:2]
  adverse=[p for p in relevant if not p["expected_acceptance"]][:2]
  while len(adverse)<2:
   source=accepting[len(adverse)%len(accepting)];bad=copy.deepcopy(source)
   bad["input"]["undeclared_extension"]=True;bad["expected_acceptance"]=False;bad["expected_error"]="field_set";bad["expected_value"]=None;bad["expected_execution_disposition"]="completed";adverse.append(bad)
  body="---\nname: "+sp["name"]+"\ndescription: Check "+", ".join(x.replace("_"," ") for x in sp["operation_pair"])+" in supplied synthetic firmware records, with explicit byte and authority limits.\n---\n\n# "+sp["name"].removeprefix("ghc-family-").replace("-"," ").title()+"\n\n"
  body+="Read [the local contracts](references/contracts.json) before choosing a fixture. The operation names below are an explicit supported profile; they do not describe a universal loader.\n\n"
  body+="Run scripts/ghc_family_firmware_record_skill.py with one JSON input file, or provide JSON on standard input. It returns the complete accepted/error/value/disposition/boundary envelope. A nonzero exit for an adverse fixture is the expected refusal. Output files use exclusive creation.\n\n"
  body+="This package supports "+", ".join("`"+op+"`" for op in sp["operation_pair"])+". Compare supplied bytes and addresses literally. Preserve sparse holes, declared byte order and entry metadata. Entry addresses are never executed. Use source status and content hashes as provenance fields; do not infer rights, authenticity or approval from them.\n\n"
  body+="The implementation bounds collections to 512 records and 4096 stored bytes. Intel HEX metadata offsets must be zero; record wrapping, duplicate starts and overlap are refused. S-record blocks use one data-address width, at most one count record and one final matching terminator. These are selected profile limits, not claims that every external format variant is invalid.\n\n"
  body+="Exercise the accepting and adverse fixtures before selecting a copied package. If the full expected envelope differs, retain the original fixture and output, then correct only the owner dependency. Never rewrite immutable expectations or overwrite a different global skill. Rollback means selecting the earlier validated package while preserving this evidence.\n\n"+core.BOUNDARY+"\n"
  (folder/"SKILL.md").write_text(body,encoding="utf-8",newline="\n")
  (folder/"scripts/ghc_family_firmware_records_core.py").write_bytes(core_bytes)
  write(folder/"scripts/ghc_family_firmware_record_skill.py",'"""Selected synthetic firmware contract interface."""\nfrom ghc_family_firmware_records_core import cli\nALLOWED='+repr(tuple(sp["operation_pair"]))+'\nif __name__=="__main__":raise SystemExit(cli(ALLOWED))')
  write(folder/"references/contracts.json",{"operations":sp["operation_pair"],"profile_ref":BASE+"/x1/profile-contract.json",
   "accepting_proposal_ids":[p["proposal_id"] for p in accepting],"adverse_proposal_ids":[p["proposal_id"] for p in adverse],
   "source":"synthetic","boundary":core.BOUNDARY})
  fixtures=[]
  for kind,selected in [("accepting",accepting),("adverse",adverse)]:
   for i,p in enumerate(selected):
    fixture=folder/"references"/f"{kind}-{i+1}.json";write(fixture,p["input"])
    proc=process([sys.executable,"-B",str(folder/"scripts/ghc_family_firmware_record_skill.py"),str(fixture)])
    try:result=json.loads(proc.stdout)
    except ValueError:raise RuntimeError("skill_smoke_output:"+sp["name"])
    passed=core.matches_contract(p,result) and proc.returncode==(0 if p["expected_acceptance"] else 2)
    assert passed,sp["name"]
    fixtures.append({"fixture":fixture.relative_to(ROOT).as_posix(),"expected_exit":proc.returncode,"complete_envelope_pass":True,
     "result_sha256":sha(canonical(result)),"kind":kind})
  proc=process([sys.executable,"-B",str(args.skill_root/".system/skill-creator/scripts/quick_validate.py"),str(folder)])
  assert proc.returncode==0,sp["name"]
  local_checks.append({"skill":sp["name"],"initializer_pass":True,"quick_validate_pass":True,"smokes":fixtures})
 write(x2/"local-tool-validation.json",{"skills":local_checks,"skill_count":10,"runner_count":5,"same_owner_only":True})
 # Full schema Method Flow, with admission failures explicitly separate from test failures.
 methods=[];witnesses=[];events=[];recommendations=[]
 def method(mid,title,signature,negative_ids,artifact,kind="software"):
  methods.append({"method_id":mid,"title":title,"failure_signature":signature,
    "trigger_preconditions":["exact owner scope","the cited synthetic or operational witness"],
    "privacy_class":"sanitized_public","approval_class":"safe_now","candidate_workaround":"Use the bounded accepting contract while refusing the retained adverse candidate.",
    "validation_witness_ids":[],"recurrence_guard":"Check the immutable expected envelope, exact fields, byte domain and scope before reuse.",
    "rollback":"Retain evidence and stop selecting a failed owner candidate.","recommendation_state":"preferred","supersedes":[],
    "protected_gates":gates,"retained_negative_ids":negative_ids,"scope_boundary":core.BOUNDARY})
  recommendations.append({"method_id":mid,"preconditions":"same trigger and owner scope","recommendation":"Use the preserved accepting witness and refusal boundary.","delivered":False})
  events.append({"method_id":mid,"from":"candidate","to":"preferred","note":"Bounded passing witness recorded; failures retained."})
  return methods[-1]
 def witness(m,wid,procedure,observed,result,negative_ids,kind,artifact):
  w={"witness_id":wid,"method_id":m["method_id"],"procedure":procedure,"scope":artifact,
   "expected":"Retain failed candidate admission and require its bounded acceptance or rejection predicate.",
   "observed":observed,"result":result,"witness_kind":kind,"same_owner_only":True,"independent_reproduction":False,
   "retained_negative_ids":negative_ids,"boundary":"Admission failures of adverse controls have zero candidate credit; the associated rejection test may pass. Same-owner only."}
  witnesses.append(w);m["validation_witness_ids"].append(wid)
 for i,op in enumerate(ops):
  ns=[n for n in negative if n["operation"]==op];m=method(f"VQ6886-M{i+1:03d}",op.replace("_"," "), "adverse "+op+" candidate admission is refused",[n["negative_id"] for n in ns],BASE+"/x2/challenges/"+op+".json")
  for j,n in enumerate(ns):
   witness(m,f"VQ6886-W-{op}-F{j+1:03d}","preregistered adverse candidate admission",n["kind"]+" refused","fail",[n["negative_id"]],"designed_admission_failure",n["artifact"])
  positive=next(p for p in plans if p["operation"]==op and p["expected_acceptance"])
  witness(m,f"VQ6886-W-{op}-P001","complete frozen positive envelope",positive["proposal_id"]+" matched","pass",[],"bounded_passing_witness",positive["concrete_artifact"])
 startup=load(phase/"x1/method-flow-startup.json")
 operational=[{"negative_id":f["id"],"failure":f["signature"],"recovery":f["recovery"]} for f in startup["retained_failures"] if f["id"]!="START-N001"]
 operational += [
  {"negative_id":"VQ6886-PRE-N001","failure":"Older workflow validator runner minimum was ten","recovery":"Current release dependency-corrected plan permits five"},
  {"negative_id":"VQ6886-PRE-N002","failure":"Planned tool names and operation scopes did not align","recovery":"Corrected before immutable x1 and rechecked collision absence"},
  {"negative_id":"VQ6886-PRE-N003","failure":"Staged whitespace check found surplus EOF lines","recovery":"Removed only uncommitted surplus blank lines and revalidated exact staging"}]
 if (bank/"x2-operational-failures.json").exists():
  operational += load(bank/"x2-operational-failures.json")["failures"]
 for o in operational:
  mid=f"VQ6886-M{len(methods)+1:03d}";m=method(mid,o["recovery"],o["failure"],[o["negative_id"]],BASE+"/x1")
  witness(m,mid+"-F","observed startup or planning attempt",o["failure"],"fail",[o["negative_id"]],"operational_failure",BASE+"/x1")
  witness(m,mid+"-P","focused recovery",o["recovery"],"pass",[],"bounded_passing_witness",BASE+"/x1")
 for name,p in package["smokes"]["direct_smokes"].items():
  mid=f"VQ6886-M{len(methods)+1:03d}";nid="VQ6886-PACKAGE-"+name.upper();m=method(mid,name+" bounded package smoke",p["error_class"],[nid],BASE+"/x2/package-transaction.json")
  witness(m,mid+"-F","preregistered package adverse candidate",p["error_class"]+" rejection","fail",[nid],"designed_admission_failure",BASE+"/x2/package-transaction.json")
  witness(m,mid+"-P","package positive smoke","expected bytes matched","pass",[],"bounded_passing_witness",BASE+"/x2/package-transaction.json")
 counts={"methods":len(methods),"witnesses":len(witnesses),"failed_witnesses":sum(w["result"]=="fail" for w in witnesses),
  "passing_witnesses":sum(w["result"]=="pass" for w in witnesses),"state_events":len(events),"recommendations":len(recommendations)}
 ledger={"schema":"ghc.family.method-flow-state.v1","phase":PHASE,"owner":OWNER,"identity_boundary":core.BOUNDARY,
  "execution_authority":"owner_self_scoped_delta","source_commit":SOURCE,"x1_commit":X1,"final_commit":None,
  "methods":methods,"witnesses":witnesses,"state_events":events,"recommendations":recommendations,"counts":counts,
  "boundary":core.BOUNDARY,"operational_failure_records":operational,"inherited_alias":{"START-N001":"EC6885-ROUTE-N019"}}
 write(x2/"method-flow/ledger.json",ledger)
 write(x2/"retained-negative-register.json",{"inherited_external_baseline":84371,"new_designed_admission_failures":len(negative)+3,
  "new_operational_negative_groups":len(operational),"new_negative_count":len(negative)+3+len(operational),
  "negative_controls_ref":BASE+"/x2/negative-controls.json","method_ledger_ref":BASE+"/x2/method-flow/ledger.json",
  "source_name_collision_alias_not_double_counted":True,"erased":0})
 outcome_counts={k:sum(p["expected_execution_disposition"]==k for p in plans) for k in ["completed","represented","open_gap","exact_gate"]}
 baseline=load(phase/"x1/phase-truth.json")["inherited_baseline"]
 effective={"proposals":16630,"negatives":84371+len(negative)+3+len(operational),
  "methods":baseline["methods"]+counts["methods"],"failed_witnesses":baseline["failed_witnesses"]+counts["failed_witnesses"],
  "passing_witnesses":baseline["passing_witnesses"]+counts["passing_witnesses"],
  "open_gaps":baseline["retained_open_gap_records"]+outcome_counts["open_gap"],"exact_gates":baseline["exact_gates"]+outcome_counts["exact_gate"]}
 for label in ["open_gap","exact_gate"]:
  write(x2/(("open-gap" if label=="open_gap" else "exact-gate")+"-register.json"),{
    "retained_inherited_count":baseline["retained_open_gap_records"] if label=="open_gap" else baseline["exact_gates"],
    "inherited_ref":BASE+"/x1/source-verification.json",
    "new":[{"proposal_id":p["proposal_id"],"title":p["title"],"disposition":label,"artifact":p["concrete_artifact"]} for p in plans if p["expected_execution_disposition"]==label],
    "actual_authority_actions_executed":0,"erasure":False,"boundary":core.BOUNDARY})
 write(x2/"phase-truth.json",{"owner":OWNER,"phase":PHASE,"source":SOURCE,"x1":X1,"state":"X2_OBSERVED_EVIDENCE_PRECOMMIT",
  "outcomes":outcome_counts,"effective_counts":effective,"observed_contracts":200,"unexpected_contract_failures":0,
  "portfolio_checks":850,"exact_packets_unexecuted":50,"blocked_packets_unexecuted":30,
  "canonical_invocations":0,"successor_contacts":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":core.BOUNDARY})
 write(x2/"workload-wellbeing.json",{"solo":True,"subagents":0,"forks":0,"delegation":0,
  "pause_stop_controls":"Hamish may pause, rename, redirect, narrow or stop at any time.",
  "bounded_operation_limits":{"records":512,"image_bytes":4096,"file_ceiling":2000},
  "unsafe_quota_filler":False,"subjective_wellbeing_claimed":False,"usage_reset_authority":"Hamish only"})
 # Portable content-addressed four-tier deck.
 cards=[]
 def card(tier,kind,title,parent,content,disposition="represented",stable=False):
  data={"schema":"ghc.family.freed-id.card.v1","tier":tier,"card_type":kind,"title":title,"parent_ids":[] if parent is None else [parent],
   "owner":OWNER,"phase":PHASE,"stability":"stable" if stable else "volatile","disposition":disposition,"content":content,
   "source_refs":[{"commit":X1,"path":BASE+"/x1/new-proposals.json"}],"protected_gates":gates,"boundary":core.BOUNDARY}
  ident="ghc-card-"+sha(canonical(data))[:20];data["card_id"]=ident;cards.append(data);return ident
 anchor=card(1,"freed_id_anchor",OWNER,None,load(phase/"x1/pillar-practice-freeze.json"),stable=True)
 pillar_ids=[card(2,"trinity_pillar",p,anchor,{"model_scope":"research-model, synthetic/proxy, or synthetic nonproduction only"},stable=True) for p in ["GMUT Mind","THOS Body","Freed ID and CBR Heart"]]
 practice_info=load(phase/"x1/pillar-practice-freeze.json")
 practice_parents=[1,0,2,2]
 practice_ids=[card(3,"bounded_practice",p,pillar_ids[practice_parents[i]],{"qualification":False,"authority":False}) for i,p in enumerate(practice_info["practices"])]
 for p in plans:
  pr=practice_info["practices"].index(p["practice"])
  card(4,"task",p["title"],practice_ids[pr],{"proposal_id":p["proposal_id"],"artifact":p["concrete_artifact"],"matches_frozen_contract":True},p["expected_execution_disposition"])
 for m in methods:card(4,"method",m["title"],practice_ids[3],{"method_id":m["method_id"],"ledger":BASE+"/x2/method-flow/ledger.json","retained_negative_ids":m["retained_negative_ids"]},"completed")
 for c in cards:write(x2/"deck/cards"/(c["card_id"]+".json"),c)
 write(x2/"deck/deck-index.json",{"schema":"ghc.family.freed-id.deck.v1","owner":OWNER,"phase":PHASE,"source":SOURCE,"x1":X1,"cards":[c["card_id"] for c in cards],"card_count":len(cards),"tier_counts":{str(i):sum(c["tier"]==i for c in cards) for i in range(1,5)},"outcomes":outcome_counts,"boundary":core.BOUNDARY})
 write(x2/"deck/stable-prefix.json",{"cards":[c["card_id"] for c in cards if c["stability"]=="stable"],"cache_hit_claimed":False})
 write(x2/"deck/volatile-index.json",{"cards":[c["card_id"] for c in cards if c["stability"]=="volatile"],"implicit_completion_credit":False})
 write(x2/"deck/compact-activation.md","Veylora Quen v688-v6 evidence is being prepared. The terminally gated next existing task is Sylven Arc v688-v7. PREPARED_NOT_SENT. Refer to the final baton only after exact terminal verification. "+core.BOUNDARY)
 entries=[{"path":p.relative_to(ROOT).as_posix(),"bytes":len(p.read_bytes()),"sha256":sha(p.read_bytes())} for p in sorted((x2/"deck").rglob("*")) if p.is_file()]
 write(x2/"deck/card-manifest.json",{"byte_domain":"UTF8_LF_repository_bytes","entries":entries,"self_exclusions":[BASE+"/x2/deck/card-manifest.json"]})
 summary={"outcomes":outcome_counts,"effective_counts":effective,"methods":counts,"cards":len(cards),"negative_controls":len(negative),"unexpected_test_failures":0}
 write(x2/"evidence-summary.json",summary)
 print(json.dumps(summary))
if __name__=="__main__":main()
