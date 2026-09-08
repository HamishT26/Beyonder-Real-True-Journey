"""Exact owner-file validation, manifests and immutable lifecycle materialization."""
from pathlib import Path
import argparse,ast,hashlib,json,re,subprocess
BASE="docs/veylora-quen/v688-v6"
SOURCE="d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14"
SHARED=["ghc_family_firmware_records_core.py","ghc_family_ihex_records.py","ghc_family_srec_records.py",
"ghc_family_firmware_sparse_image.py","ghc_family_firmware_record_evidence.py","ghc_family_firmware_record_suite.py"]
def sha(b):return hashlib.sha256(b).hexdigest()
def normalized(b):return b.replace(b"\r\n",b"\n")
def unique(pairs):
 result={}
 for k,v in pairs:
  if k in result:raise ValueError("duplicate_json_key")
  result[k]=v
 return result
def strict(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite_json")))
def owner_files(root):
 paths=[p for p in (root/BASE).rglob("*") if p.is_file()]
 paths += list((root/"scripts").glob("*veylora_quen_v688_v6*.py"))
 paths += list((root/"tests").glob("*veylora_quen_v688_v6*.py"))
 paths += [root/"scripts"/n for n in SHARED if (root/"scripts"/n).exists()]
 return sorted(set(paths))
def allowed_path(p):
 return (p.startswith(BASE+"/") or (p.startswith("scripts/") and p.endswith(".py") and "veylora_quen_v688_v6" in p)
  or (p.startswith("tests/") and p.endswith(".py") and "veylora_quen_v688_v6" in p) or p in {"scripts/"+n for n in SHARED})
def scan(root,paths):
 patterns={
  "raw_uuid":r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b",
  "private_local_path":r"\b[A-Za-z]:[\\/]",
  "private_uri":r"(?:chatgpt\.com/(?:c|g)/[A-Za-z0-9_-]{12,}|codex://[A-Za-z0-9_-]{12,})",
  "credential_value":r"(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{16,})",
  "private_material_payload":r'(?i)"(?:raw_transcript|raw_screenshot|private_execution_stream)"\s*:\s*"[^"]+"'}
 candidates=[];hits=[];security=[];json_count=0;ast_count=0;maxwords=0
 for p in paths:
  rel=p.relative_to(root).as_posix();b=p.read_bytes();text=b.decode("utf-8")
  if p.is_symlink() or not allowed_path(rel):raise ValueError("owner_scope")
  words=len(text.split());maxwords=max(maxwords,words)
  if words>100000:raise ValueError("document_word_cap:"+rel)
  if p.suffix==".json":strict(b);json_count+=1
  if p.suffix==".py":
   tree=ast.parse(text);ast_count+=1
   for n in ast.walk(tree):
    if isinstance(n,ast.Call):
     if isinstance(n.func,ast.Name) and n.func.id in ("eval","exec","compile"):security.append({"path":rel,"finding":"dynamic_builtin_execution"})
     if any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords):security.append({"path":rel,"finding":"shell_execution"})
  for cls,pat in patterns.items():
   found=list(re.finditer(pat,text))
   if not found:continue
   row={"path":rel,"class":cls,"count":len(found)}
   placeholder="X"+chr(58)+chr(47)
   fixture=p.name in ("test_ghc_family_veylora_quen_v688_v6_x2.py","x2-tests-v1.py.txt")
   if cls=="private_local_path" and fixture and all(m.group()==placeholder for m in found):
    row["adjudication"]="declared_synthetic_negative_path_fixture_not_private_material";candidates.append(row)
   else:row["adjudication"]="unresolved";hits.append(row)
 if len(paths)>=2000:raise ValueError("owner_file_ceiling")
 return {"file_count":len(paths),"strict_json_count":json_count,"python_ast_count":ast_count,
  "maximum_document_words":maxwords,"privacy":{"classes":list(patterns),"candidates":candidates,"confirmed_hits":hits,"valid":not hits},
  "security":{"configured_findings":security,"valid":not security,"exhaustive_security":False},
  "valid":not hits and not security,"unchanged_history_scan":False,"sibling_lane_scan":False}
def verify_manifest(root,path):
 m=strict(path.read_bytes());failures=[]
 for e in m["entries"]:
  rel=e["path"]
  if not allowed_path(rel):failures.append(rel+":scope");continue
  b=normalized((root/rel).read_bytes())
  digest=e.get("sha256_normalized_lf",e.get("sha256"));size=e.get("bytes_normalized_lf",e.get("bytes"))
  if sha(b)!=digest or len(b)!=size:failures.append(rel)
 return {"path":path.relative_to(root).as_posix(),"entries":len(m["entries"]),"failures":failures,"valid":not failures}
def verify_promotions(root,skills,runners):
 p=strict((root/BASE/"x2/promotion-receipt.json").read_bytes());failures=[]
 for e in p["source_global_parity"]:
  rel=e["global_target"]
  if rel.startswith("skills/"):target=skills/rel.removeprefix("skills/")
  elif rel.startswith("owner_runner_bank/"):target=runners/rel.removeprefix("owner_runner_bank/")
  else:raise ValueError("promotion_target_alias")
  source=root/e["source"]
  if source.read_bytes()!=target.read_bytes() or sha(source.read_bytes())!=e["sha256"]:failures.append(e["source"])
 return {"files":len(p["source_global_parity"]),"failures":failures,"valid":not failures}
def batch_blobs(root,refs):
 result=subprocess.run(["git","-C",str(root),"cat-file","--batch"],input=("\n".join(refs)+"\n").encode(),stdout=subprocess.PIPE,check=True)
 data=result.stdout;pos=0;blobs=[]
 for ref in refs:
  end=data.index(b"\n",pos);header=data[pos:end].split()
  if len(header)!=3 or header[1]!=b"blob":raise ValueError("missing_git_blob")
  n=int(header[2]);blobs.append(data[end+1:end+1+n]);pos=end+n+2
 return blobs
def materialize(root,commit,paths,destination):
 from ghc_family_veylora_quen_v688_v6_lifecycle import safe_relative_paths
 safe_relative_paths(paths)
 if destination.exists():raise ValueError("definition_destination_exists")
 if destination.resolve().drive.upper()!="D:":raise ValueError("D_first_definition_view")
 if any(not allowed_path(p) for p in paths):raise ValueError("definition_scope")
 blobs=batch_blobs(root,[commit+":"+p for p in paths]);destination.mkdir(parents=True,exist_ok=False)
 for p,b in zip(paths,blobs):
  out=destination/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 return {"definition":commit,"file_count":len(paths),"read_only_source":True,"private_paths_published":False}
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open("x",encoding="utf-8",newline="\n") as f:json.dump(value,f,indent=2,sort_keys=True);f.write("\n")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--stage",choices=["evidence","final"],required=True)
 ap.add_argument("--skills",type=Path,required=True);ap.add_argument("--runners",type=Path,required=True)
 a=ap.parse_args();root=Path(__file__).resolve().parents[1]
 results=scan(root,owner_files(root));assert results["valid"],results
 checks=[verify_manifest(root,root/BASE/"x1/x1-manifest.json"),verify_manifest(root,root/BASE/"x2/deck/card-manifest.json")]
 if a.stage=="final":checks.append(verify_manifest(root,root/BASE/"validation/evidence-manifest.json"))
 assert all(c["valid"] for c in checks),checks
 promotions=verify_promotions(root,a.skills.resolve(),a.runners.resolve());assert promotions["valid"]
 report={"schema":"ghc.family.owner-precommit-validation.v1","stage":a.stage,"source":SOURCE,
  "scan":results,"manifests":checks,"promotions":promotions,"canonical_invoked":False,"valid":True,
  "boundary":"Bounded same-owner files and configured checks only; not independent reproduction, exhaustive security, authority or Stage 20 readiness."}
 write(root/BASE/"validation"/(a.stage+"-precommit.json"),report)
 paths=owner_files(root);name=BASE+"/validation/"+a.stage+"-manifest.json"
 entries=[{"path":p.relative_to(root).as_posix(),"bytes_normalized_lf":len(normalized(p.read_bytes())),
  "sha256_normalized_lf":sha(normalized(p.read_bytes()))} for p in paths]
 write(root/name,{"schema":"ghc.family.owner-delta-manifest.v1","stage":a.stage,"source":SOURCE,
  "byte_domain":"normalized_lf_git_blob","entries":entries,"entry_count":len(entries),"self_exclusions":[name]})
 print(json.dumps({"stage":a.stage,"files":len(paths)+1,"manifest_entries":len(entries),"privacy_candidates":len(results["privacy"]["candidates"]),
  "confirmed_private_hits":len(results["privacy"]["confirmed_hits"]),"security_findings":len(results["security"]["configured_findings"]),"valid":True}))
if __name__=="__main__":main()
