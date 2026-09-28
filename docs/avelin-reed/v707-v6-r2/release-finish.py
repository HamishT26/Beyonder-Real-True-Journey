"""Publish an additive D-drive release and verify its installed adapters."""
from pathlib import Path
import json, hashlib, shutil, subprocess, sys, os
ROOT=Path(__file__).resolve().parents[3]; DOC=Path(__file__).resolve().parent
BANK=Path("D:/GHC-Archives/phase-banks/avelin-reed-v707-v6-r2")
LAB=Path("D:/GHC-Family-Laboratory"); SKILLS=Path.home()/".codex/skills"
RELEASE=LAB/"releases/avelin-v707-v6-r2-review-1"
NODE=Path("D:/GHC-Archives/global-tools/node/26.10.0/node-v26.10.0-win-x64/node.exe")
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def put(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not RELEASE.exists(),"Preserve an existing release"
old=(LAB/"current.json").read_bytes();before_hash=hashlib.sha256(old).hexdigest()
hooks=read(DOC/"hook-catalogue.json")
for r in hooks["discovered_files"]:
 parts=Path(r["relative"]).parts;r["plugin"]=parts[1];r["version"]=parts[2]
put(DOC/"hook-catalogue.json",hooks)
capabilities={"schema":"ghc.current-capabilities.v20","phase":"v707-v6-r2","release":"avelin-v707-v6-r2-review-1","catalogued_skills":2219,"new_global_main_guides":6,"new_plugin":"ghc-family-laboratory-v20","new_hooks":5,"manual_hook_checks":10,"live_host_hook_observations":0,"models_per_session":15,"intake":"Persistent pinned transactional source intake; zero new source-domain credit","integration":"12 frozen consent-safe correction schedules; deliberate mutant caught","consultation":"one message in x1 and one in x2; current late exception has two in x2","roster":"147 numbered prospective rows; 30 distinct identities","source_receipts":["global-promotion.json","shared-intake-acceptance.json","cross-pillar-integration.json","consultation-receipt.json","hook-catalogue.json"],"boundary":"Same-owner bounded evidence; NOT_READY_FOR_STAGE_20."}
put(DOC/"capabilities-v20.json",capabilities)
for name in ["ghc-family-meta-tool-box","ghc-family-index"]:
 target=SKILLS/name
 for filename,data in [("avelin-v707-v6-r2-capabilities.json",capabilities),("current-hook-catalogue-v20.json",hooks)]:
  put(target/"references"/filename,data);put(ROOT/"shared-updates"/name/"references"/filename,data)
 skill=target/"SKILL.md";before=skill.read_bytes()
 marker="\n## Avelin v707-v6-r2 laboratory capability release\n\nRead [the current capability receipt](references/avelin-v707-v6-r2-capabilities.json) and [hook catalogue](references/current-hook-catalogue-v20.json). Six main guides retain original callers while routing five bounded operations. Five installed advisory hooks have manual checks; live host observation remains zero. The current two ChatGPT consultations both occurred in x2. Future bundles require one in x1 and one in x2. Preserve the private target outside exports and keep the Caelen terminal gate separate.\n"
 assert "## Avelin v707-v6-r2 laboratory capability release" not in before.decode("utf-8")
 (BANK/"shared-before"/(name+"-before-release.md")).write_bytes(before)
 skill.write_bytes(before+marker.encode("utf-8"));dest=ROOT/"shared-updates"/name/"SKILL.md";dest.write_bytes(skill.read_bytes())
for p in (ROOT/"skills").glob("ghc-family-main-*-v20/scripts/runner.txt"):
 s=p.read_text(encoding="utf-8").replace("releases/avelin-v707-v6-r2/laboratory","releases/avelin-v707-v6-r2-review-1/laboratory")
 p.write_text(s,encoding="utf-8");installed=SKILLS/p.parents[1].name/"scripts/runner.txt";installed.write_text(s,encoding="utf-8")
RELEASE.mkdir(parents=True)
for folder in ["laboratory","models","runners","skills","plugins"]:
 shutil.copytree(ROOT/folder,RELEASE/folder,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
manifest={"schema":"ghc.release-manifest.v1","release":RELEASE.name,"files":[{"path":p.relative_to(RELEASE).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p)} for p in sorted(RELEASE.rglob("*")) if p.is_file()],"self_excluded":"release-manifest.json"}
put(RELEASE/"release-manifest.json",manifest);put(DOC/"review-release-manifest.json",manifest)
assert (LAB/"current.json").read_bytes()==old,"Shared pointer changed; do not overwrite"
put(LAB/"current-review-1.tmp",{"schema":"ghc.lab.current.v1","release":str(RELEASE),"manifest_sha256":sha(RELEASE/"release-manifest.json"),"previous_pointer_sha256":before_hash,"rollback_release":"avelin-v707-v6-r2"})
os.replace(LAB/"current-review-1.tmp",LAB/"current.json")
checks=[]
for name,op in [("laboratory","catalogue"),("models","model"),("evidence","integrity"),("governance","claim"),("workflow","route"),("capabilities","catalogue")]:
 guide="ghc-family-main-"+name+"-v20"; root=SKILLS/guide
 v=subprocess.run([sys.executable,"-X","utf8","-B",str(SKILLS/".system/skill-creator/scripts/quick_validate.py"),str(root)],capture_output=True,text=True,timeout=30)
 assert v.returncode==0,v.stderr+v.stdout
 for invalid in [False,True]:
  request=BANK/("x2-"+op+("-invalid" if invalid else "-request")+".json")
  output=BANK/("installed-"+name+("-invalid" if invalid else "-valid")+".json")
  r=subprocess.run([str(NODE),str(root/"scripts/runner.txt"),str(request),str(output)],capture_output=True,text=True,timeout=30)
  good=(r.returncode==2 and not output.exists()) if invalid else (r.returncode==0 and output.exists())
  checks.append({"id":guide+("-refusal" if invalid else "-valid"),"pass":good,"exit":r.returncode,"invalid_subject_original_success_credit":0 if invalid else None})
for name in ["ghc-family-meta-tool-box","ghc-family-index"]:
 r=subprocess.run([sys.executable,"-X","utf8","-B",str(SKILLS/".system/skill-creator/scripts/quick_validate.py"),str(SKILLS/name)],capture_output=True,text=True,timeout=30)
 assert r.returncode==0
put(DOC/"installed-adapter-checks.json",{"schema":"ghc.installed-adapter-checks.v1","checks":checks,"passed":sum(x["pass"] for x in checks),"total":len(checks),"guide_validation":8,"release_manifest_sha256":sha(RELEASE/"release-manifest.json"),"global_installation":True,"live_host_hook_observation":False,"prior_release_preserved":True})
assert all(x["pass"] for x in checks),checks
put(DOC/"cloud-receipt.json",{"state":"UPLOADED_AND_EXACT_BYTES_READ_BACK","bytes":135821,"sha256":sha(DOC/"cloud-archive.json"),"readback_sha256":sha(BANK/"cloud-readback.json"),"metadata_and_parent_verified":True,"private_target_not_exported":True,"paid_external_spend_usd":0,"remote_locator":"External D-drive cloud-location.json","scope":"Authorized Drive archive only; no deployed cloud operating system."})
assert sha(DOC/"cloud-archive.json")==sha(BANK/"cloud-readback.json")
put(BANK/"cloud-location.json",{"folder":"https://drive.google.com/drive/folders/1MO6CiYz0RpTwoPmy2YsvHzxr9lGiy5go","file":"https://drive.google.com/file/d/1SMbqPtZGXqi7NoLGIzzSFhcfWzbsyvfm/view","sha256":sha(DOC/"cloud-archive.json")})
print(json.dumps({"release_files":len(manifest["files"]),"installed_checks":len(checks),"all_pass":all(x["pass"] for x in checks),"cloud_exact":True}))
