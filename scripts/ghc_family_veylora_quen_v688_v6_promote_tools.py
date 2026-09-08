"""Promote exactly ten new skill packages and five runner interfaces without overwriting."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];BASE="docs/veylora-quen/v688-v6"
sys.path.insert(0,str(ROOT/"scripts"))
import ghc_family_firmware_records_core as core
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("x",encoding="utf-8",newline="\n") as f:json.dump(x,f,indent=2,sort_keys=True);f.write("\n")
def run(cmd):
 return subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",
  env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONUTF8":"1"})
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);ap.add_argument("--skills",type=Path,required=True);ap.add_argument("--runners",type=Path,required=True)
 a=ap.parse_args();bank=a.bank.resolve();skillroot=a.skills.resolve();runnerroot=a.runners.resolve()
 if runnerroot.drive.upper()!="D:":raise RuntimeError("D_first_runner_bank")
 plan=load(ROOT/BASE/"x1/tool-package-plan.json");proposals=load(ROOT/BASE/"x1/new-proposals.json")["proposals"]
 for s in plan["skills"]:
  if (skillroot/s["name"]).exists():raise RuntimeError("global_skill_collision:"+s["name"])
 if runnerroot.exists():raise RuntimeError("runner_destination_exists")
 local=load(ROOT/BASE/"x2/local-tool-validation.json")
 assert len(local["skills"])==10 and all(s["quick_validate_pass"] for s in local["skills"])
 assert load(ROOT/BASE/"x2/method-flow/validation.json")["valid"]
 marker=bank/"promotion-invoked.json";save(marker,{"state":"STARTED","skills":10,"runners":5,"overwrite":False})
 fixture_root=bank/"promotion-fixtures";fixture_root.mkdir(exist_ok=False)
 fixtures={}
 for op in core.FIELDS:
  p=next(p for p in proposals if p["operation"]==op and p["expected_acceptance"])
  positive=fixture_root/(op+"-accept.json");bad=fixture_root/(op+"-adverse.json")
  save(positive,p["input"]);save(bad,{**p["input"],"undeclared_extension":True})
  fixtures[op]=(p,positive,bad)
 parity=[];skill_checks=[];runner_checks=[]
 def smoke(script,operations):
  results=[]
  for op in operations:
   p,good,bad=fixtures[op]
   accepted=run([sys.executable,"-B",str(script),str(good)])
   rejected=run([sys.executable,"-B",str(script),str(bad)])
   try:g=json.loads(accepted.stdout);b=json.loads(rejected.stdout)
   except ValueError:raise RuntimeError("global_smoke_output:"+op)
   if accepted.returncode!=0 or not core.matches_contract(p,g):raise RuntimeError("global_accepting_smoke:"+op)
   if rejected.returncode!=2 or b["accepted"] is not False or b["error"]!="field_set":raise RuntimeError("global_adverse_smoke:"+op)
   results.append({"operation":op,"accepting_pass":True,"adverse_rejected":True,
    "accepting_output_sha256":sha(json.dumps(g,sort_keys=True).encode()),"adverse_output_sha256":sha(json.dumps(b,sort_keys=True).encode())})
  return results
 try:
  for s in plan["skills"]:
   source=ROOT/BASE/"skills"/s["name"];target=skillroot/s["name"]
   if any(p.is_symlink() for p in source.rglob("*")):raise RuntimeError("source_symlink")
   check=run([sys.executable,"-B",str(skillroot/".system/skill-creator/scripts/quick_validate.py"),str(source)])
   if check.returncode:raise RuntimeError("local_skill_validation:"+s["name"])
   shutil.copytree(source,target,dirs_exist_ok=False)
   for path in sorted(p for p in source.rglob("*") if p.is_file()):
    other=target/path.relative_to(source);equal=path.read_bytes()==other.read_bytes()
    if not equal:raise RuntimeError("skill_parity:"+s["name"])
    parity.append({"source":path.relative_to(ROOT).as_posix(),"global_target":"skills/"+s["name"]+"/"+path.relative_to(source).as_posix(),
     "bytes":len(path.read_bytes()),"sha256":sha(path.read_bytes()),"byte_equal":True})
   check=run([sys.executable,"-B",str(skillroot/".system/skill-creator/scripts/quick_validate.py"),str(target)])
   if check.returncode:raise RuntimeError("installed_skill_validation:"+s["name"])
   skill_checks.append({"name":s["name"],"quick_validate_pass":True,"smokes":smoke(target/"scripts/ghc_family_firmware_record_skill.py",s["operation_pair"])})
   print(json.dumps({"promoted_skill":s["name"],"count":len(skill_checks)}),flush=True)
  runnerroot.mkdir(parents=True,exist_ok=False)
  names=[p["name"] for p in plan["runners"]]+["ghc_family_firmware_records_core.py"]
  for name in names:
   source=ROOT/"scripts"/name;target=runnerroot/name
   with target.open("xb") as f:f.write(source.read_bytes())
   if target.read_bytes()!=source.read_bytes():raise RuntimeError("runner_parity:"+name)
   parity.append({"source":"scripts/"+name,"global_target":"owner_runner_bank/"+name,"bytes":len(source.read_bytes()),
    "sha256":sha(source.read_bytes()),"byte_equal":True})
  for r in plan["runners"]:
   runner_checks.append({"name":r["name"],"smokes":smoke(runnerroot/r["name"],r["operation_group"])})
  result={"schema":"ghc.family.firmware-promotion.v1","owner":"Veylora Quen","phase":"v688-v6",
   "skill_count":10,"runner_interface_count":5,"shared_core_helpers":1,"source_global_parity":parity,
   "skills":skill_checks,"runners":runner_checks,"overwrites":0,"older_compatibility_files_changed":0,
   "scope":"Ten new essential global skill packages and one owner-specific D-first runner bank",
   "rollback":"Select the retained prior package; do not delete or rewrite any historical package or lane.",
   "state":"PROMOTED_VALIDATED_BYTE_EQUAL","canonical_invoked":False,"independent_reproduction":False}
  save(bank/"promotion-receipt.json",result);save(ROOT/BASE/"x2/promotion-receipt.json",result)
  print(json.dumps({"state":result["state"],"skills":10,"runners":5,"parity_files":len(parity)}),flush=True)
 except Exception as exc:
  save(bank/"promotion-failure.json",{"state":"FAILED_RETAINED","signature":str(exc),"completed_skills":skill_checks,
   "completed_runners":runner_checks,"parity":parity,"success_credit":0,"retry":"inspect exact persisted destinations before any focused recovery"})
  raise
if __name__=="__main__":main()
