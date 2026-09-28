"""Bounded operations readback and portable archive preparation."""
from pathlib import Path
import json, hashlib, subprocess, sys, tomllib, urllib.request, urllib.error
ROOT=Path(__file__).resolve().parents[3]; DOC=Path(__file__).resolve().parent
BANK=Path("D:/GHC-Archives/phase-banks/avelin-reed-v707-v6-r2")
HOME=Path.home(); SKILLS=HOME/".codex/skills"
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def put(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(i,ok,detail=None):checks.append({"id":i,"pass":bool(ok),"detail":detail})
def http(path,method="GET",host="127.0.0.1:43177"):
    req=urllib.request.Request("http://127.0.0.1:43177/"+path,method=method,headers={"Host":host})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.read(),dict(r.headers)
    except urllib.error.HTTPError as e:return e.code,e.read(),dict(e.headers)
mounts=read(BANK/"legacy-mounts-private.json")
for m in mounts:
    status,body,headers=http("legacy/"+m["id"]+"/index.html")
    check(m["id"]+"-exact-source",status==200 and hashlib.sha256(body).hexdigest()==m["sha256"])
for p,method,host,expected in [
 ("../private/evidence.sqlite","GET","127.0.0.1:43177",400),
 ("%2e%2e/private/evidence.sqlite","GET","127.0.0.1:43177",400),
 ("intake_store.py","GET","127.0.0.1:43177",404),
 ("data/skills.json","POST","127.0.0.1:43177",405),
 ("","GET","untrusted.example",403),
 ("legacy/L999/index.html","GET","127.0.0.1:43177",404)]:
    code,_,_=http(p,method,host);check("http-refusal-"+str(len(checks)),code==expected,{"expected":expected,"observed":code})
code,body,headers=http("api/intake-card")
card=json.loads(body);check("persistent-card-readback",code==200 and card["original_outcome"]=="completed")
code,body,headers=http("")
check("loopback-csp",code==200 and "default-src 'self'" in headers.get("Content-Security-Policy",""))
index=read(ROOT/"laboratory/data/skills.json")
check("lossless-skill-shards",sum(p["rows"] for p in index["chunks"])==2219 and all(sha(ROOT/"laboratory/data"/p["file"])==p["sha256"] for p in index["chunks"]))
receipt={"schema":"ghc.lab.http-acceptance.v1","checks":checks,"passed":sum(x["pass"] for x in checks),"total":len(checks),"scope":"Read-only owner server and exact mounted HTML blob digests; no sibling domain suite or canonical replay."}
put(DOC/"http-acceptance.json",receipt)
assert receipt["passed"]==receipt["total"],receipt
coordinator=HOME/".codex/plugins/cache/openai-curated-remote/codex-coordinator/0.4.0/scripts"
coord=[]
for name,event in [("codex_coordinator_session_start.py","SessionStart"),("codex_coordinator_stop_guard.py","Stop")]:
    payload={"cwd":str(ROOT),"hook_event_name":event,"session_id":"-".join(["0"*8,"0"*4,"4"+"0"*3,"8"+"0"*3,"0"*12])}
    r=subprocess.run([sys.executable,"-X","utf8","-B",str(coordinator/name)],input=json.dumps(payload),capture_output=True,text=True,timeout=30)
    coord.append({"hook":name,"event":event,"exit":r.returncode,"quiet":r.stdout.strip()=="","source_sha256":sha(coordinator/name),"manual_fixture":True})
put(DOC/"coordinator-check.json",{"checks":coord,"fixture_identifier_not_a_live_session":True,"project_opt_in_marker_present":False,"board_enabled":False,"claims_created":0,"live_events_observed":0,"scope":"Manual supported hook entrypoints, quiet no-op without an enabled board."})
assert all(r["exit"]==0 for r in coord)
cfg=tomllib.loads((HOME/".codex/config.toml").read_text(encoding="utf-8"))
important={k:cfg.get(k) for k in ["approval_policy","sandbox_mode","model_context_window","model_auto_compact_token_limit","model","model_reasoning_effort"]}
assert important["approval_policy"]=="never" and important["sandbox_mode"]=="danger-full-access"
assert important["model_context_window"]==1000000 and important["model_auto_compact_token_limit"]==400000
put(DOC/"platform-readback.json",{
 "schema":"ghc.platform-readback.v1","configuration":important,
 "cli":{"before":"0.157.1","installed":"0.158.0","update_exit":0},
 "node":{"D_preferred":"26.10.0","system_install_changed":False},
 "powershell":{"current_session":"7.6.5","D_portable_observed":"7.6.6","latest_official_tag":"v7.6.6","existing_copy_reused":True,"duplicate_install_preflight_refused":True},
 "npm_updates":{"eslint-plugin-security":["4.0.1","4.1.0"],"vitest":["5.0.1","5.0.2"]},
 "python_updates":{"filelock":["4.0.3","4.0.5"],"identify":["2.6.19","2.6.20"],"nodeenv":["1.10.0","1.11.0"],"platformdirs":["4.11.13","4.12.1"],"virtualenv":["21.12.1","21.13.0"]},
 "pip_check_exit":0,"desktop_app_changed":False,"model_configuration_changed":False,
 "windows_admin_token":False,"new_privileges":False,"external_paid_spend_usd":0,
 "rollback":"Pin recorded previous npm and pip versions; restore the saved D profile; retain all installed portable versions."})
hook_files=list((HOME/".codex/plugins/cache").glob("*/*/*/hooks/hooks.json"))
hooks=[{"plugin":p.parents[1].name,"version":p.parent.parent.name,"sha256":sha(p),"relative":p.relative_to(HOME/".codex/plugins/cache").as_posix(),"state":"catalogued_only"} for p in hook_files]
own=read(ROOT/"plugins/ghc-family-laboratory-v20/hooks/hooks.json")
put(DOC/"hook-catalogue.json",{"schema":"ghc.hook-catalogue.v20","discovered_files":hooks,"new_plugin":"ghc-family-laboratory-v20","new_hooks":5,"manual_checks":10,"host_observed_events":0,"source":own,"duplicate_policy":"Reuse source/budget/consultation/roster/evidence advisory checks; do not create equivalent hooks merely for a quota."})
portable={"schema":"ghc.lab.cloud-archive.v1","owner":"Avelin Reed","phase":"v707-v6-r2","state":"x2 prepared archive; terminal seal recorded separately","projects":read(DOC/"projects.json"),"laboratories":read(ROOT/"laboratory/data/labs.json"),"model_contracts":read(ROOT/"laboratory/data/model-contracts.json"),"integration":read(DOC/"cross-pillar-integration.json"),"consultation_policy":read(DOC/"consultation-receipt.json"),"contains_credentials":False,"private_transcripts_included":False,"private_routes_included":False,"empirical_validation":False}
put(DOC/"cloud-archive.json",portable)
put(DOC/"operations-finish-receipt.json",{"http_passed":receipt["passed"],"http_total":receipt["total"],"coordinator_manual_entries":len(coord),"hook_catalogue_files":len(hooks),"cloud_export_sha256":sha(DOC/"cloud-archive.json")})
print(json.dumps({"http":str(receipt["passed"])+"/"+str(receipt["total"]),"coordinator":2,"hook_files":len(hooks),"cloud_bytes":(DOC/"cloud-archive.json").stat().st_size}))
