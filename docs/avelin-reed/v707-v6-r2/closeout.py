"""Owner metadata closeout; canonical is single-use and never executes domain tests."""
from pathlib import Path
import ast, datetime, hashlib, importlib.util, json, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[3];DOC=Path(__file__).resolve().parent
BANK=Path("D:/GHC-Archives/phase-banks/avelin-reed-v707-v6-r2")
BASE=DOC.relative_to(ROOT).as_posix()
BRANCH="codex/GHC-Family/avelin-reed-main-1"
SOURCE="06f54492a7da636205b0e85184d2d2fa33286134"
X1="9c1600caec5b5beda39b6be01fbf9de4b03b80ad"
BOUNDARY="Finite synthetic same-owner evidence only. NOT_READY_FOR_STAGE_20."
NODE="D:/GHC-Archives/global-tools/node/26.10.0/node-v26.10.0-win-x64/node.exe"
def put(p,x,exclusive=False):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("x" if exclusive else "w",encoding="utf-8",newline="\n") as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write("\n")
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 r=subprocess.run(["git","-C",str(ROOT),*args],capture_output=True,timeout=120)
 if r.returncode:raise RuntimeError("Git operation failed: "+args[0])
 return r.stdout.decode("utf-8").strip()
def files():return sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix!=".pyc")
def manifest(name):
 excluded=BASE+"/"+name
 return {"schema":"ghc.owner-manifest.v20","entries":[{"path":p.relative_to(ROOT).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p.read_bytes())} for p in files() if p.relative_to(ROOT).as_posix()!=excluded],"self_exclusions":[excluded]}
def blob_map(refs):
 process=subprocess.Popen(["git","-C",str(ROOT),"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out={}
 for ref in dict.fromkeys(refs):
  process.stdin.write((ref+"\n").encode());process.stdin.flush()
  header=process.stdout.readline().decode().strip().split()
  if len(header)!=3 or header[1]!="blob":raise ValueError("Missing exact Git blob")
  count=int(header[2]);assert count<16000000
  out[ref]=process.stdout.read(count);assert process.stdout.read(1)==b"\n"
 process.stdin.close();assert process.wait(timeout=30)==0
 return out
def strict_json(b):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError("Duplicate JSON key")
   d[k]=v
  return d
 return json.loads(b.decode("utf-8-sig"),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError("Nonfinite JSON")))
def finalize():
 commits=git("rev-list","--reverse","HEAD").splitlines();assert len(commits)==3 and commits[1]==X1
 accounting=read(DOC/"accounting.json");handoff=(DOC/"handoff.md").read_bytes()
 final={"schema":"ghc.avelin.remaster-final.v20","owner":"Avelin Reed","phase":"v707-v6-r2","source":SOURCE,"branch":BRANCH,
 "lifecycle":{"planning":commits[0],"x1":X1,"x2":commits[2],"final":"external_after_commit","orphan_root":True,"content_provenance_is_not_git_ancestry":True},
 "accounting":accounting,"projects":{"initial":20,"cap":80,"outcomes":"project-outcomes.json"},"task_tally":"task-tally.json",
 "model_sessions":{"x1":15,"x2":15},"declared_model_tests":{"x1":75,"x2":75},"research_probes":15,"research_checks":21,
 "law_hypotheses":15,"law_status":"Labelled mathematical, engineering or normative proposals; not new fundamental discoveries",
 "skills":{"local_x1":5,"new_global_x2":6,"catalogued":2219,"semantic_equivalence_claim":False},
 "hooks":{"new_installed":5,"manual_checks":10,"live_host_observations":0},"installed_adapter_checks":12,
 "intake":{"initial_checks":8,"persistent_checks":13,"all_ready_continuation_checks":2,"ordinary_test_processes":122,"new_source_domain_credit":0},
 "integration":{"schedules":12,"checks":15,"mutant_detected":True,"empirical_validation":False},
 "consultation":{"sent":2,"replies":2,"current_x1":0,"current_x2":2,"future_each_session":1,"route":"existing authenticated ChatGPT UI"},
 "laboratories":{"source_bound":31,"prior_numbered":30,"source_domain_replays":0},"journey":{"named_files":22,"selected_windows":126,"complete_semantic_read":False},
 "cloud":{"state":"UPLOADED_AND_EXACT_BYTES_READ_BACK","bytes":135821,"receipt":"cloud-receipt.json"},
 "browser":{"record":"browser-validation.json","download_acknowledgement":"unverified","mobile_width":390},
 "method_flow":"method-flow.json","failures":"failure-ledger.json","retained_negatives":"retained-negatives.json",
 "handoff":{"file":"handoff.md","words":len(handoff.decode().split()),"sha256":sha(handoff),"modules":13,"literal_eof":"LITERAL_EOF_AVELIN_V707_V6_R2"},
 "resources":{"new_agents":0,"new_tasks":0,"forks":0,"external_paid_spend_usd":0,"spending_ceiling_usd":50,"pdfs":0},
 "route":{"state":"PREPARED_NOT_SENT","owner":"Caelen Ash","phase":"v707-v7","native_send_attempts":0,"recipient_completion":"not_observed"},
 "canonical":{"state":"PREPARED_FOR_ONE_METADATA_INVOCATION","domain_replay":False,"source_replay":False},
 "manifest":"manifest.json","boundary":BOUNDARY,"terminal_verdict":"NOT_READY_FOR_STAGE_20"}
 put(DOC/"final.json",final)
 summary=f"""# Avelin v707-v6 (2): shared laboratory outcome

The remaster delivers a D-drive shared laboratory, thirty-one source-bound historical entrypoints, fifteen model families with fifteen saved configurations in each session, and a persistent source-intake record. The authenticated Review and refine GHC Lab conversation received two messages and returned two substantive replies. Future bundles require one x1 and one x2 consultation; both current messages were in x2 because the rule arrived after x1 sealed.

The original v707-v6 remains sealed at {SOURCE}. This Main-1 branch has an explicit orphan root and content provenance, not invented ancestry. Its planning, x1 and x2 commits are {commits[0]}, {X1} and {commits[2]}. The final exact commit and one-shot canonical are external terminal records.

The sessions passed 75 model checks each. Initial intake passed 8 checks; persistent intake passed 13, with 2 further synchronized-barrier checks. The synthetic cross-pillar experiment passed 15 checks over 12 schedules and caught the deliberately broken publication-permission behavior. Research contributed 15 bounded open-problem probes and 21 checks, with no universal solution or empirical observation claim. Forty HTTP boundary checks and 12 installed-adapter checks passed.

Six main guides organize the 2,219-entry skill snapshot while preserving original callers. Five advisory hooks are installed and manually checked; live host events remain unobserved. Shared v20 policy, roster, capability pointers and hook inventory were updated. The prospective roster has 147 numbered rows covering thirty identities through Eiren v725-v8.

The portable cloud archive was uploaded to the authorized Drive bank and downloaded again: all 135,821 bytes match its local digest. This establishes an archive bridge, not a deployed cloud OS. CLI 0.158.0 and selected D-drive package updates are verified. Existing D-drive PowerShell 7.6.6 is selected for future pwsh calls. The desktop app and model/context settings remain preserved; the Windows process is unelevated.

See [the full baton](handoff.md), [task tally](task-tally.json), [separate Method Flow](method-flow.json), [retained failures](failure-ledger.json), [research](research.md), [review adoption](review-adoption.md), [current capability receipt](capabilities-v20.json), and [final machine record](final.json). The browser download acknowledgement remains unverified, mobile canvas labels are small, live hooks require a real observation, and independent/empirical claims remain open.

Only the exact existing Caelen Ash v707-v7 edge may follow a successful terminal gate. The external route receipt records whether that native send was possible; preparation is not delivery. NOT_READY_FOR_STAGE_20.
"""
 (DOC/"overview.md").write_text(summary,encoding="utf-8")
 put(DOC/"manifest.json",manifest("manifest.json"))
 print(json.dumps({"final_prepared":True,"handoff_words":final["handoff"]["words"],"files":len(files()),"x2":commits[2]}))
def validate(canonical=False,exact=None):
 checks=[]
 def check(i,ok,detail=None):checks.append({"id":i,"pass":bool(ok),"detail":None if ok else detail})
 owned=files();relative=sorted(p.relative_to(ROOT).as_posix() for p in owned);raw={p.relative_to(ROOT).as_posix():p.read_bytes() for p in owned}
 check("file-budget",len(owned)<2000);check("no-pdf",not any(p.suffix.lower()==".pdf" for p in owned))
 maxwords=0;json_count=0
 for name,b in raw.items():
  try:
   s=b.decode("utf-8-sig");maxwords=max(maxwords,len(s.split()))
   if name.endswith(".json"):strict_json(b);json_count+=1
   if name.endswith(".py"):ast.parse(s,filename=name)
  except Exception as e:check("parse-"+name,False,type(e).__name__)
 check("word-budget",maxwords<=100000,maxwords)
 js=[str(ROOT/n) for n in relative if n.endswith((".js",".txt"))]
 runner="const fs=require('fs'),vm=require('vm');for(const p of JSON.parse(fs.readFileSync(process.argv[1],'utf8')))new vm.Script(fs.readFileSync(p,'utf8'),{filename:p});"
 syntax_path=BANK/("syntax-canonical.json" if canonical else "syntax-preflight.json");put(syntax_path,js)
 result=subprocess.run([NODE,"-e",runner,str(syntax_path)],capture_output=True,text=True,timeout=60)
 check("executable-syntax",result.returncode==0,result.stderr[:600])
 f=read(DOC/"final.json");m=read(DOC/"manifest.json");ledger=read(DOC/"method-flow.json")
 check("manifest-coverage",sorted([x["path"] for x in m["entries"]]+m["self_exclusions"])==relative)
 check("manifest-current-bytes",all(len(raw[e["path"]])==e["bytes"] and sha(raw[e["path"]])==e["sha256"] for e in m["entries"]))
 for stage in ["x1","x2"]:
  d=read(DOC/(stage+"-results.json"));check(stage+"-models",len(d["models"])==15)
  check(stage+"-stored-results",all(sha(raw[x["path"]])==x["sha256"] for x in d["models"]))
  check(stage+"-checks",len(d["tests"])==75 and d["all_checks_pass"] and d["invocations"]==1 and d["replays"]==0)
 check("method-flow-schema",read(DOC/"method-flow-validation.json")["valid"])
 check("method-witness-backlinks",all(w["witness_id"] in next(m["validation_witness_ids"] for m in ledger["methods"] if m["method_id"]==w["method_id"]) for w in ledger["witnesses"]))
 check("negative-zero-credit",all(w["original_success_credit"]==0 for w in ledger["witnesses"] if w["result"]=="fail"))
 a=f["accounting"];check("one-source-fold",a["source_baseline_fold_count"]==1 and all(a["source_baseline"][k]+a["own"][k]==a["effective"][k] for k in a["own"]))
 baton=raw[BASE+"/handoff.md"];check("baton",sha(baton)==f["handoff"]["sha256"] and 2000<=len(baton.decode().split())<=100000 and len(re.findall(r"^## Module ",baton.decode(),re.M))==13 and baton.decode().strip().endswith("LITERAL_EOF_AVELIN_V707_V6_R2"))
 roster=read(DOC/"roster-v20.json");rows=roster["numbered_rows"]
 check("roster-terminal",len(rows)==147 and rows[0]["phase"]=="v707-v6" and rows[-1]["phase"]=="v725-v8" and rows[-1]["owner"]=="Eiren Kestrel")
 c=f["consultation"];check("consultation-truth",c["sent"]==2 and c["replies"]==2 and c["current_x1"]==0 and c["current_x2"]==2)
 check("stage20",f["terminal_verdict"]=="NOT_READY_FOR_STAGE_20")
 check("literal-required-tokens",all(s in baton.decode() for s in ["Caelen Ash","v707-v7","NOT_READY_FOR_STAGE_20","LITERAL_EOF_AVELIN_V707_V6_R2","method-flow.json","failure-ledger.json"]))
 histories=[(X1,BASE+"/x1-manifest.json"),(f["lifecycle"]["x2"],BASE+"/x2-manifest.json")]
 history_blobs=blob_map([commit+":"+name for commit,name in histories])
 manifests=[(commit,json.loads(history_blobs[commit+":"+name])) for commit,name in histories]
 refs=[commit+":"+e["path"] for commit,mh in manifests for e in mh["entries"]]
 if canonical:refs += [exact+":"+n for n in relative]
 blobs=blob_map(refs)
 for commit,mh in manifests:check("historical-manifest-"+commit,all(len(blobs[commit+":"+e["path"]])==e["bytes"] and sha(blobs[commit+":"+e["path"]])==e["sha256"] for e in mh["entries"]))
 privacy=[]
 for n,b in raw.items():
  s=b.decode("utf-8-sig")
  if re.search(r"C:[/\\]Users[/\\]hamis",s,re.I):privacy.append({"path":n,"class":"literal-user-home"})
  if re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",s,re.I):privacy.append({"path":n,"class":"raw-private-identifier-candidate"})
  if re.search(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----|(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{25,}",s):privacy.append({"path":n,"class":"credential-candidate"})
 check("privacy-candidates",not privacy,privacy)
 if canonical:
  check("exact-commit",git("rev-parse","HEAD")==exact)
  check("clean",git("status","--porcelain=v1","--untracked-files=all")=="")
  check("four-commits",len(git("rev-list","HEAD").splitlines())==4)
  check("exact-owner-tree",git("ls-tree","-r","--name-only",exact).splitlines()==relative)
  check("committed-byte-equality",all(blobs[exact+":"+n]==raw[n] for n in relative))
 return {"mode":"canonical" if canonical else "preflight","checks":checks,"passed":sum(c["pass"] for c in checks),"total":len(checks),"failed":[c for c in checks if not c["pass"]],"owner_files":len(owned),"json_files":json_count,"executable_files":len(js),"maximum_words":maxwords,"raw_blob_bindings":len(blobs),"domain_replayed":False,"source_canonical_replayed":False}
def canonical(exact):
 assert re.fullmatch("[0-9a-f]{40}",exact)
 directory=BANK/"canonical"
 put(directory/"invocation.json",{"state":"INVOKED_ONCE","exact_final":exact,"invocations":1,"replays":0,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()},True)
 try:
  git("fetch","origin","refs/heads/"+BRANCH+":refs/remotes/origin/"+BRANCH)
  advertised=git("ls-remote","--heads","origin","refs/heads/"+BRANCH).split()[0]
  values=[git("rev-parse","HEAD"),git("rev-parse","refs/heads/"+BRANCH),git("rev-parse","refs/remotes/origin/"+BRANCH),advertised]
  assert all(v==exact for v in values),"Fresh four-way equality required"
  r=validate(True,exact);put(directory/"validation-details.json",r,True)
  assert r["passed"]==r["total"],r["failed"]
  result={"state":"VALID_EXACT_FINAL_OWNER_SCOPED_METADATA_CANONICAL","exact_final":exact,"invocations":1,"successes":1,"replays":0,"checks_passed":r["passed"],"checks_total":r["total"],"owner_files":r["owner_files"],"json_files":r["json_files"],"raw_blob_bindings":r["raw_blob_bindings"],"maximum_words":r["maximum_words"],"fresh_four_way_equal":True,"clean":True,"domain_replayed":False,"source_canonical_replayed":False,"external_native_send_attempts":0,"boundary":BOUNDARY}
 except Exception as e:result={"state":"FAILED_CANONICAL_ZERO_SUCCESS_CREDIT","exact_final":exact,"invocations":1,"successes":0,"replays":0,"error":str(e),"boundary":BOUNDARY}
 put(directory/"payload.json",result,True)
 put(directory/"receipt.json",{"state":result["state"],"exact_final":exact,"invocations":1,"successes":result["successes"],"replays":0,"payload_sha256":sha((directory/"payload.json").read_bytes())},True)
 if result["successes"]:put(directory/"success-latch.json",{"state":"SUCCESS_NO_REPLAY","exact_final":exact},True)
 print(json.dumps(result));return 0 if result["successes"] else 1
if __name__=="__main__":
 command=sys.argv[1]
 if command=="seal-x2":
  assert not (DOC/"x2-manifest.json").exists();put(DOC/"x2-manifest.json",manifest("x2-manifest.json"));print("x2 manifest sealed")
 elif command=="final":finalize()
 elif command=="validate":
  r=validate();put(BANK/("validation-"+sys.argv[2]+".json"),r,True);print(json.dumps(r));sys.exit(0 if r["passed"]==r["total"] else 1)
 elif command=="canonical":sys.exit(canonical(sys.argv[2]))
 else:raise ValueError("Unsupported closeout operation")
