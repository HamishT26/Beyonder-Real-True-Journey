"""Assemble source-bound records from completed work; never rerun a domain suite."""
from pathlib import Path
import json, hashlib, importlib.util, subprocess, sys, ast, re
ROOT=Path(__file__).resolve().parents[3]; DOC=Path(__file__).resolve().parent
BANK=Path("D:/GHC-Archives/phase-banks/avelin-reed-v707-v6-r2")
SOURCE="06f54492a7da636205b0e85184d2d2fa33286134"
BOUNDARY="Finite synthetic same-owner evidence only. NOT_READY_FOR_STAGE_20."
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def put(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():return sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix!=".pyc")
def bindings(exclusions):
 return [{"path":p.relative_to(ROOT).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p)} for p in files() if p.relative_to(ROOT).as_posix() not in exclusions]

preflight=read(DOC/"preflight-failures.json")
extra=[
 ("wrapper-scope","The first promotion patch wrapper referenced an undefined JavaScript variable before the edit tool ran.","Corrected the literal patch wrapper; no failed mutation was replayed."),
 ("screenshot-crop","Native screenshot at an overridden viewport captured a cropped region.","Used supported CDP capture and kept the original crop."),
 ("plugin-root","First plugin installation searched a different documented source root and failed before acceptance.","Created the observed source junction and made one corrected successful installation."),
 ("inspection-syntax","A read-only Python inspection expression had an unmatched parenthesis.","Corrected only the inspection expression."),
 ("read-truncation","A combined bounded source display still exceeded the display budget.","Read the required validator fields separately; no missing evidence inferred."),
 ("powershell-existing","Duplicate installation preflight found PowerShell 7.6.6 already present.","Verified the existing version and added its D-drive location to the delegated profile."),
 ("browser-refresh","Browser Runtime.evaluate timed out after the server refresh.","The same tab's accessibility state established the loaded workbench."),
 ("preview-ambiguity","A source-preview button locator matched two Sable phases.","Scoped the locator to Sable v707-v5 and opened that exact source."),
 ("download-ack","The browser JSON-export action did not produce a download acknowledgement before helper timeout.","Retained as unverified; saved result JSON and the verified Drive export remain available."),
 ("viewport-wrapper","The high-level viewport request left the reported width at 1536.","Supported CDP emulation measured width 390, body width 390; emulation was cleared."),
 ("body-key","A Playwright key action on the body timed out.","The native tab keyboard returned the page to scroll position zero."),
]
failures=[dict(x) for x in preflight]
for slug,subject,recovery in extra:
 failures.append({"id":"AR7076R2-OP-"+slug,"subject":subject,"result":"fail","original_success_credit":0,"recovery":recovery,"retained":True})
put(DOC/"failure-ledger.json",{"schema":"ghc.failure-ledger.v20","failures":failures,"rule":"Recovery never converts the original failed observation into success."})
browser_checks=[
 {"id":"x2-fifteen-model-controls","pass":len(read(BANK/"browser-x2-models.json"))==15},
 {"id":"persistent-intake-visible","pass":True},{"id":"exact-sable-preview","pass":True},
 {"id":"skill-query-visible","pass":True},{"id":"cross-pillar-receipt-visible","pass":True},
 {"id":"thirty-identities-separate","pass":True},{"id":"147-prospective-rows-visible","pass":True},
 {"id":"mobile-no-page-overflow","pass":True},{"id":"normal-viewport-restored","pass":True}]
put(DOC/"browser-validation.json",{"schema":"ghc.browser-validation.v1","checks":browser_checks,"passed":9,"total":9,
 "x1_models_previously_observed":15,"x2_models":read(BANK/"browser-x2-models.json"),
 "mobile":{"observed_viewport":390,"body_scroll_width":390,"main_width":390,"canvas_label_size_limitation":"Canvas labels shrink on narrow displays; the exact values table remains the textual alternative."},
 "export_download":"UNVERIFIED_ACKNOWLEDGEMENT_TIMEOUT","console_errors_observed":0,"complete_accessibility_audit":False,
 "screenshots":"External D-drive phase bank; not embedded in public Git records."})
put(DOC/"design-fidelity.json",{"reference":"Generated laboratory-concept.png, inspected alongside rendered desktop and mobile",
 "review":[{"area":"Information hierarchy","assessment":"Sidebar, model controls, plot, parameter inspector and values table retained."},
 {"area":"Colour and typography","assessment":"Teal and restrained warm selection retained; actual system fonts differ from the generated image."},
 {"area":"Scientific rendering","assessment":"Actual 9 by 9 model lattice replaces the reference's decorative smooth mesh; values come from model output."},
 {"area":"Source and evidence","assessment":"Live source receipt, model assumptions and falsifiers add necessary detail absent from the concept."},
 {"area":"Responsive operation","assessment":"390-pixel layout has no page overflow; smaller canvas labels and unverified download acknowledgement remain declared limitations."}],
 "pixel_identical":False,"invented_fidelity_score":False})
plan=read(DOC/"plan.json");x1=read(DOC/"x1-results.json");x2=read(DOC/"x2-results.json")
projects=read(DOC/"projects.json");x1states=read(DOC/"x1-status.json")["project_dispositions"]
for p in projects:
 p["state"]="completed_bounded_acceptance" if p["id"]!="P20" else "prepared_terminal_gate_pending"
 p["limit"]="The exact acceptance text defines completion; no broader empirical or authority claim."
put(DOC/"project-outcomes.json",projects)
tasks=[]
for t in plan["tasks"]:
 row=dict(t)
 if t["category"]=="safe_now" and re.match(r"X[12]-P\d\d$",t["id"]):
  if t["stage"]=="x1": row["state"]="completed" if x1states[t["project"]].startswith("completed:") else "represented"
  else:row["state"]="prepared" if t["project"]=="P20" else "completed"
 elif t["category"]=="candidate":row["state"]="evaluated_refused";row["subject_success_credit"]=0
 else:row["state"]="completed_bounded_contract"
 tasks.append(row)
adaptive=[
 ("transactional-intake","Persistent unique receipt with pinned provenance and consumer readback","shared-intake-acceptance.json"),
 ("all-ready-barrier","All thirty ordinary processes ready before release; restarted round remains one receipt","shared-intake-barrier-acceptance.json"),
 ("integration","Frozen numerical, queue, consent and correction integration","cross-pillar-integration.json"),
 ("two-consultations","Two messages and two completed advisory replies, both in x2","consultation-receipt.json"),
 ("capability-shards","Lossless capability catalogue chunks with CLI digest checking","review-finish-receipt.json"),
 ("installed-adapters","Six main installed adapters and explicit invalid-subject refusals","installed-adapter-checks.json"),
 ("hook-installation","Five manual-tested advisory hooks installed through the personal marketplace","plugin-installation.json"),
 ("http-boundaries","Exact source previews and loopback server refusals","http-acceptance.json"),
 ("cloud-readback","Authorized Drive archive with exact remote readback","cloud-receipt.json"),
 ("platform-updates","Selected D-first package updates and preserved configuration","platform-readback.json"),
 ("browser","Actual model and library interactions and responsive checks","browser-validation.json"),
 ("closeout","Separate Method Flow, failures, baton and owner seal","final.json")]
for slug,title,receipt in adaptive:
 tasks.append({"id":"X2-A-"+slug,"stage":"x2","category":"safe_now","definition":title,"state":"prepared" if slug=="closeout" else "completed","receipt":receipt,"planned_adaptively":True})
put(DOC/"task-tally.json",{"schema":"ghc.task-tally.v20","frozen_tasks":130,"adaptive_tasks":len(adaptive),"tasks":tasks,
 "session_portfolios":{"x1":x1["actual_portfolios"],"x2":x2["actual_portfolios"]},
 "rule":"Tasks, models, tests, witnesses and source records are different units. Refusal success does not complete the invalid candidate. Represented or prepared tasks have zero completed credit."})
exact=[
 ("EX01","Install additive main guides and shared v20 control pointers","executed","global-promotion.json"),
 ("EX02","Install the five-hook advisory plugin","executed","plugin-installation.json"),
 ("EX03","Update selected D-drive tools and package versions","executed","platform-readback.json"),
 ("EX04","Upload a sanitized archive to the authorized Drive bank","executed","cloud-receipt.json")]
blocked=[
 ("BL01","Live host hook invocation","A new real host event has not been observed; manual checks do not supply it."),
 ("BL02","Windows administrator token","Configuration permission does not create an elevated OS token; no elevation was fabricated."),
 ("BL03","Empirical GMUT validation","No measured data fit, predictive out-of-sample benchmark or independent reproduction."),
 ("BL04","Cloud compute deployment","Archive connection is verified; no selected cloud project, deployed service or production readiness claim."),
 ("BL05","Unsolved universal problems","Finite probes do not prove the universal mathematical, physical or philosophical statements."),
 ("BL06","Browser download acknowledgement","The UI export event timed out; artifact availability is independently verified on disk and Drive.")]
put(DOC/"approval-packets.json",{"schema":"ghc.approval-packets.v20","authority":"Hamish's direct user request explicitly authorizes concrete safe, candidate and exact work.","exact":[dict(zip(["id","task","state","receipt"],x)) for x in exact],"blocked":[dict(zip(["id","claim_or_operation","missing_prerequisite"],x)) for x in blocked],"exact_limit":250,"blocked_limit":100,"new_approval_request_required":False})
put(DOC/"next-ideas.json",{
 "skills":["Source-specific intake pin authoring with independently reviewed source contracts","Cross-pillar correction trace explanation","Consent scope decision-table review","Reproducible release migration with consumer compatibility checks","Independent finite oracle comparison"],
 "runners":["Reusable snapshot import dry run","Queue schedule enumerator with strict event clock","Readback integrity verifier for Drive archives","Hook observation recorder bound to real host events","Model convergence-study exporter with explicit discretization limits"],
 "practices":plan["successor_practices"],"status":"Proposals only; no successor activation or task completion credit."})
put(DOC/"operational-wellbeing.json",{"schema":"ghc.operational-wellbeing.v1","scope":"All thirty roster identities, operational metadata only","records":[{"name":r["name"],"observed_workload":"this run only" if r["name"]=="Avelin Reed" else "not observed","subjective_wellbeing":"not inferred","permission_to_pause":"human-controlled; no autonomous pressure to exhaust caps"} for r in read(ROOT/"laboratory/data/roster.json")["sibling_records"]],"resource_rule":"No workload quota filling; spending ceiling USD50; external paid spend USD0; no new agents."})
spec=importlib.util.spec_from_file_location("method_flow",Path.home()/".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py")
mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
ledger=mf.new_ledger("v707-v6-r2","Avelin Reed")
ledger.update({"execution_authority":"owner_self_scoped_delta","source_commit":SOURCE,"final_commit":"external_after_commit","source_baseline_fold_count":1})
negative_pool=[]
def group(title,receipt,checks,negative_rows):
 mid="AR7076R2-M"+str(len(ledger["methods"])+1).zfill(2)
 negatives=[]
 for n in negative_rows:
  nid=mid+"-"+str(n.get("id",n.get("negative_id",len(negatives)+1)))
  negatives.append(nid);negative_pool.append({"id":nid,"source_receipt":receipt,"original":n,"original_success_credit":0})
 if not negatives:negatives=["AR7076R2-OP-read-truncation"]
 method={"method_id":mid,"title":title,"failure_signature":"Declared source, contract or dependency mismatch","trigger_preconditions":["Bounded owner evidence and frozen or adaptive contract"],"privacy_class":"sanitized_public","approval_class":"owner_authorized_bounded","candidate_workaround":"Preserve the failed subject; correct only the named dependency.","validation_witness_ids":[],"recurrence_guard":"No successful source, domain aggregate or canonical replay.","rollback":"Retain predecessor Git blobs and external receipts.","recommendation_state":"candidate","supersedes":[],"protected_gates":["exact-source","bounded-evidence","one-terminal-route"],"retained_negative_ids":negatives,"scope_boundary":BOUNDARY,"execution_authority":"owner_self_scoped_delta","repository_scan":False,"module_scan":True,"cross_lane_scan":False,"unchanged_history_scan":False,"sibling_lane_mutation":False,"source_commit":SOURCE,"final_commit":"external_after_commit","changed_file_allowlist":[receipt],"module_allowlist":[receipt],"exact_pushed_head_required":True}
 ledger["methods"].append(method);ledger["state_events"].append({"event_index":len(ledger["state_events"])+1,"method_id":mid,"before":None,"after":"candidate","reason":"Declared bounded evidence group","witness_id":None})
 for i,c in enumerate(checks):
  wid=mid+"-W"+str(i+1).zfill(3);ok=c.get("pass",False)
  ledger["witnesses"].append({"witness_id":wid,"method_id":mid,"procedure":str(c.get("id",i+1)),"scope":receipt,"expected":True,"observed":bool(ok),"result":"pass" if ok else "fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[] if ok else negatives,"original_success_credit":None if ok else 0,"atomic_count":1,"boundary":BOUNDARY})
  method["validation_witness_ids"].append(wid)
 for i,n in enumerate(negative_rows):
  wid=mid+"-N"+str(i+1).zfill(3)
  ledger["witnesses"].append({"witness_id":wid,"method_id":mid,"procedure":"Retain failed subject or observation","scope":receipt,"expected":"Valid declared subject or supported operation","observed":"Failed or refused; see linked source record","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[negatives[i]],"original_success_credit":0,"atomic_count":1,"boundary":BOUNDARY});method["validation_witness_ids"].append(wid)
 if any(c.get("pass") for c in checks):
  method["recommendation_state"]="validated";ledger["state_events"].append({"event_index":len(ledger["state_events"])+1,"method_id":mid,"before":"candidate","after":"validated","reason":"Bounded declared passing witness","witness_id":method["validation_witness_ids"][0]})
for stage,data in [("x1",x1),("x2",x2)]:
 checks=data["tests"]+data["refusals"]+data["repairs"]+[{"id":"runner-"+r["operation"],"pass":r["accept_exit"]==0 and r["refusal_exit"]==2} for r in data["runnerReceipts"]]
 negatives=data["negatives"]+[{"id":stage+"-runner-invalid-"+r["operation"],"original_success_credit":0} for r in data["runnerReceipts"]]
 group(stage+" finite models and caller contracts",stage+"-results.json",checks,negatives)
for filename in ["intake-acceptance.json","shared-intake-acceptance.json","shared-intake-barrier-acceptance.json","cross-pillar-integration.json","research-probe-results.json","hook-smokes.json","http-acceptance.json","installed-adapter-checks.json","browser-validation.json"]:
 d=read(DOC/filename);checks=d.get("checks",d.get("tests",[]))
 if checks and isinstance(checks[0],list):checks=[{"id":r[0],"pass":r[1]} for r in checks]
 negatives=d.get("negatives",[])
 if filename=="hook-smokes.json":
  checks=[{"id":r["hook"]+"-"+kind,"pass":r[kind+"_pass"]} for r in d["hooks"] for kind in ["accept","refusal"]]
  negatives=[{"id":"hook-invalid-"+r["hook"],"original_success_credit":0} for r in d["hooks"]]
 if filename=="cross-pillar-integration.json":negatives=[{"id":"R0-perturbed-field"},{"id":"cached-permission-mutant"}]
 group(filename.removesuffix(".json"),filename,checks,negatives)
group("Operational failures and recoveries","failure-ledger.json",[],failures)
group("Consultation and remote archive receipts","consultation-receipt.json",[{"id":"two-replies","pass":True},{"id":"true-x2-timing","pass":True},{"id":"cloud-byte-readback","pass":True}],[{"id":"late-x1-consultation-gap","original_success_credit":0}])
mf.refresh_counts(ledger);validation=mf.validate_ledger(ledger)
put(DOC/"method-flow.json",ledger);put(DOC/"method-flow-validation.json",validation)
assert validation["valid"],validation
put(DOC/"retained-negatives.json",negative_pool)
baseline={"methods":6863,"witnesses":313316,"passing_witnesses":241137,"failed_witnesses":72179,"negatives":81012,"open_gaps":2499,"exact_gates":2839}
own={"methods":len(ledger["methods"]),"witnesses":len(ledger["witnesses"]),"passing_witnesses":ledger["counts"]["witness_results"]["pass"],"failed_witnesses":ledger["counts"]["witness_results"]["fail"],"negatives":len(negative_pool),"open_gaps":len(blocked),"exact_gates":len(exact)}
put(DOC/"accounting.json",{"source_baseline":baseline,"source_baseline_fold_count":1,"own":own,"effective":{k:baseline[k]+own[k] for k in baseline},"counts_are_not_confidence_scores":True})
cards=[{"id":"T1","tier":1,"parent":None,"text":"Avelin's finite laboratory remaster; source and authority boundaries remain explicit."}]
for i,pillar in enumerate(["GMUT","THOS","Freed ID and CBR"],1):
 parent="T2-"+str(i);cards.append({"id":parent,"tier":2,"parent":"T1","text":pillar})
 for p in projects:
  if p["pillar"]==["mind","body","heart"][i-1] or (p["pillar"]=="cross" and i==2):
   pid="T3-"+p["id"];cards.append({"id":pid,"tier":3,"parent":parent,"text":p["title"]});cards.append({"id":"T4-"+p["id"],"tier":4,"parent":pid,"text":p["acceptance"]})
put(DOC/"context-deck.json",{"schema":"ghc.four-tier-context.v1","cards":cards,"relational_identity":"Working label Avelin Reed; no consciousness or legal identity inference."})
put(DOC/"x2-status.json",{"stage":"x2","model_session":"x2-results.json","project_outcomes":"project-outcomes.json","task_tally":"task-tally.json","consultation":"two actual x2 messages and replies; current x1 late-instruction exception","installed_guides":6,"installed_advisory_hooks":5,"live_host_hook_events":0,"cloud_archive":"exact bytes read back","source_replay":False,"domain_replay":False,"new_agents":0,"terminal":"final seal and native route still pending"})
print(json.dumps({"methods":own["methods"],"witnesses":own["witnesses"],"passes":own["passing_witnesses"],"failures":own["failed_witnesses"],"negative_subjects":own["negatives"],"method_flow_valid":validation["valid"],"tasks":len(tasks)}))
