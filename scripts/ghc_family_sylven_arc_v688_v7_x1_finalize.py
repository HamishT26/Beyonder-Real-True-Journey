#!/usr/bin/env python3
"""Bind and validate the exact Sylven Arc v688-v7 planning-only x1 surface."""
from pathlib import Path
import argparse,ast,hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"docs/sylven-arc/v688-v7"
X1=BASE/"x1"
SOURCE="e7db6f3be1327de72f93873eb6540aabfc773344"
SELF_EXCLUSIONS=[
 "docs/sylven-arc/v688-v7/x1/x1-manifest.json",
]
def sha(data):return hashlib.sha256(data).hexdigest()
def norm(data):return data.replace(b"\r\n",b"\n")
def unique(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError("duplicate_json_key:"+key)
        out[key]=value
    return out
def strict(data):return json.loads(data,object_pairs_hook=unique,
    parse_constant=lambda value:(_ for _ in()).throw(ValueError(value)))
def allowed(relative):
    return (relative.startswith("docs/sylven-arc/v688-v7/x1/") or
      relative in {"scripts/build_ghc_family_sylven_arc_v688_v7_x1.py",
                   "scripts/ghc_family_sylven_arc_v688_v7_x1_finalize.py",
                   "tests/test_ghc_family_sylven_arc_v688_v7_x1.py"})
def write(path,value,replace=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w" if replace else "x",encoding="utf-8",newline="\n") as handle:
        json.dump(value,handle,indent=2,sort_keys=True);handle.write("\n")
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--rebind",action="store_true");args=parser.parse_args()
    paths=sorted([p for p in X1.rglob("*") if p.is_file()]+[
      ROOT/"scripts/build_ghc_family_sylven_arc_v688_v7_x1.py",
      ROOT/"scripts/ghc_family_sylven_arc_v688_v7_x1_finalize.py",
      ROOT/"tests/test_ghc_family_sylven_arc_v688_v7_x1.py"])
    patterns={
      "raw_uuid":r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b",
      "private_local_path":r"\b[A-Za-z]:[\\/]",
      "private_uri":r"(?:chatgpt\.com/(?:c|g)/[A-Za-z0-9_-]{12,}|codex://[A-Za-z0-9_-]{12,})",
      "credential_value":r"(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{16,})",
      "private_material_payload":r'(?i)"(?:raw_transcript|raw_screenshot|private_execution_stream)"\s*:\s*"[^"]+"'}
    json_count=0;ast_count=0;privacy=[];security=[];max_words=0
    for path in paths:
        relative=path.relative_to(ROOT).as_posix()
        if path.is_symlink() or not allowed(relative):raise RuntimeError("owner_scope:"+relative)
        data=path.read_bytes();text=data.decode("utf-8");max_words=max(max_words,len(text.split()))
        if len(text.split())>100000:raise RuntimeError("word_cap:"+relative)
        if path.suffix==".json":strict(data);json_count+=1
        if path.suffix==".py":
            tree=ast.parse(text);ast_count+=1
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {"eval","exec","compile"}:
                    security.append({"path":relative,"finding":"dynamic_builtin_execution"})
                if isinstance(node,ast.Call) and any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords):
                    security.append({"path":relative,"finding":"shell_execution"})
        for class_name,pattern in patterns.items():
            if re.search(pattern,text):privacy.append({"path":relative,"class":class_name})
    if privacy or security:raise RuntimeError(json.dumps({"privacy":privacy,"security":security}))
    validation={"schema":"ghc.family.owner-x1-validation.v1","owner":"Sylven Arc","phase":"v688-v7",
      "source":SOURCE,"planning_only":True,"file_count_before_receipts":len(paths),
      "strict_json_count":json_count,"python_ast_count":ast_count,"maximum_document_words":max_words,
      "privacy_classes":list(patterns),"privacy_confirmed_hits":[],"configured_security_findings":[],
      "x2_paths":0,"canonical_invoked":False,"same_owner_only":True,"independent_reproduction":False,
      "valid":True,"boundary":"Planning-only owner scope; not execution, independent reproduction, authority, or Stage 20 evidence."}
    write(X1/"x1-validation.json",validation,replace=args.rebind)
    paths=sorted([p for p in X1.rglob("*") if p.is_file()]+[
      ROOT/"scripts/build_ghc_family_sylven_arc_v688_v7_x1.py",
      ROOT/"scripts/ghc_family_sylven_arc_v688_v7_x1_finalize.py",
      ROOT/"tests/test_ghc_family_sylven_arc_v688_v7_x1.py"])
    entries=[]
    for path in paths:
        relative=path.relative_to(ROOT).as_posix()
        if relative in SELF_EXCLUSIONS:continue
        data=norm(path.read_bytes())
        entries.append({"path":relative,"bytes_normalized_lf":len(data),"sha256_normalized_lf":sha(data)})
    write(X1/"x1-manifest.json",{"schema":"ghc.family.owner-delta-manifest.v1","stage":"x1","source":SOURCE,
      "byte_domain":"normalized_lf_git_blob","planning_only":True,"entries":entries,"entry_count":len(entries),
      "self_exclusions":SELF_EXCLUSIONS},replace=args.rebind)
    print(json.dumps({"valid":True,"manifest_entries":len(entries),"owner_files":len(paths),
      "json":json_count,"ast":ast_count,"privacy_confirmed":0,"security_findings":0},sort_keys=True))
if __name__=="__main__":main()
