#!/usr/bin/env python3
"""Exclusive exact-final owner-scoped canonical validator for Orin v687-v7."""

from __future__ import annotations

import argparse, ast, hashlib, importlib.util, io, json, os, re, subprocess, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE="28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"; X1="7aea73908f8f41ed38473d6e30e5f1bda36588a7"; FIRST="a29be946caf963315a48f73055f0eb1cae85e482"; CORRECTED="7f9d761e54475cf82945ef31e019d043aebde282"; BRANCH="codex/GHC-Family/orin-thale-v687-v7-full-tools"
MANIFESTS=[(X1,"docs/orin-thale/v687-v7/validation/x1-manifest.json"),(FIRST,"docs/orin-thale/v687-v7/validation/x2-manifest.json"),(CORRECTED,"docs/orin-thale/v687-v7/validation/x2-correction-manifest.json"),("HEAD","docs/orin-thale/v687-v7/validation/final-delta-manifest.json"),("HEAD","docs/orin-thale/v687-v7/validation/final-owner-manifest.json")]
TESTS=[("tests/test_ghc_family_orin_thale_v687_v7_x1.py",{"OrinThaleV687V7X1Tests.test_builder_runs_at_source_before_commit"}),("tests/test_ghc_family_orin_thale_v687_v7_x2.py",{"OrinThaleV687V7X2Tests.test_lifecycle_starts_at_immutable_x1","OrinThaleV687V7X2Tests.test_x1_immutable"}),("tests/test_ghc_family_orin_thale_v687_v7_x2_correction.py",{"OrinThaleV687V7X2CorrectionTests.test_precommit_parent_is_first_evidence","OrinThaleV687V7X2CorrectionTests.test_original_x2_manifest_unchanged_at_first_evidence"}),("tests/test_ghc_family_orin_thale_v687_v7_final.py",{"OrinThaleV687V7FinalTests.test_precommit_parent_is_corrected_evidence"})]

def run(a,binary=False): return subprocess.run(a,cwd=ROOT,capture_output=True,text=not binary,encoding=None if binary else "utf-8",check=False)
def git(*a):
    r=run(["git",*a],False)
    if r.returncode: raise RuntimeError(r.stderr)
    return r.stdout.strip()
def blob(anchor,path):
    r=run(["git","show",f"{anchor}:{path}"],True)
    if r.returncode: raise RuntimeError(r.stderr.decode(errors="replace"))
    return r.stdout
def norm(b): return b.replace(b"\r\n",b"\n").replace(b"\r",b"\n")
def owner_path(p): return p.startswith("docs/orin-thale/v687-v7/") or p.startswith("scripts/build_ghc_family_orin_thale_v687_v7_") or p.startswith("scripts/ghc_family_orin_thale_v687_v7_") or p.startswith("scripts/ghc_family_spectral_archive_") or p=="scripts/ghc_family_spectral_archive_contract.py" or p.startswith("tests/test_ghc_family_orin_thale_v687_v7_")
def replay(anchor,path):
    anchor=git("rev-parse",anchor); d=json.loads(blob(anchor,path).decode()); mismatches=[]
    for e in d["entries"]:
        b=norm(blob(anchor,e["path"]));
        if len(b)!=e["bytes_normalized_lf"] or hashlib.sha256(b).hexdigest()!=e["sha256_normalized_lf"]: mismatches.append(e["path"])
    if mismatches: raise RuntimeError(f"manifest mismatch {path}: {mismatches}")
    return {"anchor":anchor,"manifest":path,"entries":len(d["entries"]),"self_exclusions":d["declared_self_exclusions"],"mismatches":[]}
def suite(path,exclusions):
    spec=importlib.util.spec_from_file_location("canonical_"+Path(path).stem,ROOT/path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); found=unittest.defaultTestLoader.loadTestsFromModule(module); flat=[]
    def visit(s):
        for item in s:
            visit(item) if isinstance(item,unittest.TestSuite) else flat.append(item)
    visit(found); selected=[]; excluded=[]
    for test in flat:
        short=".".join(test.id().split(".")[-2:])
        (excluded if short in exclusions else selected).append(test if short not in exclusions else short)
    if set(excluded)!=exclusions: raise RuntimeError(f"exclusion mismatch {path}: {excluded}")
    return unittest.TestSuite(selected),{"path":path,"discovered":len(flat),"selected":len(selected),"excluded":sorted(exclusions)}
def canonical(skill_root,runner_root):
    head=git("rev-parse","HEAD"); checks=[]
    if git("branch","--show-current")!=BRANCH: raise RuntimeError("branch")
    ancestry=[line.split() for line in git("rev-list","--parents","--reverse",f"{SOURCE}..{head}").splitlines()]
    if ancestry!=[[X1,SOURCE],[FIRST,X1],[CORRECTED,FIRST],[head,CORRECTED]]: raise RuntimeError(f"ancestry {ancestry}")
    if git("rev-list","--merges",f"{SOURCE}..{head}"): raise RuntimeError("merge")
    if git("status","--porcelain=v1"): raise RuntimeError("dirty before")
    checks += ["branch","ancestry","four_commits","zero_merges","one_final_parent","clean_before"]
    stream=io.StringIO(); combined=unittest.TestSuite(); summaries=[]
    for path,exclusions in TESTS:
        s,summary=suite(path,exclusions); combined.addTests(s); summaries.append(summary)
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(combined)
    if not result.wasSuccessful(): raise RuntimeError(stream.getvalue())
    checks.append("selected_tests")
    manifests=[replay(a,p) for a,p in MANIFESTS]; checks.append("manifests")
    owner_paths=[p for p in git("diff","--name-only",SOURCE,head).splitlines() if owner_path(p)]
    items={p:norm(blob(head,p)) for p in owner_paths}; json_count=0; document_count=0; python_count=0; confirmed=[]; security=[]
    patterns={"raw_uuid":re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",re.I),"private_absolute_path":re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)",re.I),"raw_task_identifier":re.compile(rb"(?:thread|task|agent)_id\s*[:=]",re.I),"credential_assignment":re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[:=]\s*[^\s]{8,}",re.I),"private_stream":re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)",re.I)}
    for p,b in items.items():
        if p.endswith(".json"): json.loads(b.decode(),parse_constant=lambda v:(_ for _ in()).throw(ValueError(v))); json_count+=1
        if p.endswith((".md",".html",".txt")):
            if len(b.decode().split())>100000: raise RuntimeError(f"word cap {p}")
            document_count+=1
        scanner=p.endswith(("build_ghc_family_orin_thale_v687_v7_x1.py","build_ghc_family_orin_thale_v687_v7_x2.py","build_ghc_family_orin_thale_v687_v7_x2_correction.py","build_ghc_family_orin_thale_v687_v7_final.py","ghc_family_orin_thale_v687_v7_final_validator.py"))
        for cls,pat in patterns.items():
            if not scanner and pat.search(b): confirmed.append({"path":p,"class":cls})
        if p.endswith(".py"):
            python_count+=1; tree=ast.parse(b.decode(),filename=p)
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {"eval","exec"}: security.append({"path":p,"finding":node.func.id})
    if confirmed or security: raise RuntimeError(f"privacy={confirmed} security={security}")
    checks += ["strict_json","documents","privacy","security"]
    index=json.loads(items["docs/orin-thale/v687-v7/final/baton-index.json"].decode()); baton=items[index["path"]]
    if hashlib.sha256(baton).hexdigest()!=index["sha256"] or len(baton.decode().split())!=index["words"] or not baton.decode().rstrip().endswith(index["eof"]): raise RuntimeError("baton")
    checks.append("baton")
    correction=json.loads(items["docs/orin-thale/v687-v7/x2/promotion-correction-receipt.json"].decode()); parity=0
    for e in correction["members"]:
        src=items[e["source"]]; dst=(skill_root/e["name"]/e["relative"]) if e["kind"]=="skill" else (runner_root/e["relative"])
        if dst.read_bytes()!=src or hashlib.sha256(src).hexdigest()!=e["sha256"]: raise RuntimeError(f"global parity {e['name']}")
        parity+=1
    checks.append("global_parity")
    up=git("rev-parse","@{upstream}"); tracking=git("rev-parse",f"refs/remotes/origin/{BRANCH}"); live=git("ls-remote","--heads","origin",f"refs/heads/{BRANCH}").split("\t")[0]; div=git("rev-list","--left-right","--count","HEAD...@{upstream}").split()
    if not head==up==tracking==live or div!=["0","0"]: raise RuntimeError("remote equality")
    if git("status","--porcelain=v1"): raise RuntimeError("dirty after")
    checks += ["upstream","tracking","fresh_live","zero_divergence","clean_after"]
    return {"status":"VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL","owner":"Orin Thale","phase":"v687-v7","source":SOURCE,"x1":X1,"retained_first_evidence":FIRST,"corrected_evidence":CORRECTED,"exact_final":head,"branch":BRANCH,"canonical_invocation_count":1,"canonical_success_count":1,"canonical_replay_count":0,"selected_tests":sum(x["selected"] for x in summaries),"test_selections":summaries,"detailed_checks":len(checks),"detailed_check_names":checks,"manifest_bindings":sum(x["entries"] for x in manifests),"manifest_self_exclusions":sum(len(x["self_exclusions"]) for x in manifests),"manifests":manifests,"owner_files":len(owner_paths),"strict_json_documents":json_count,"document_checks":document_count,"python_ast_checks":python_count,"confirmed_privacy_hits":0,"bounded_security_findings":0,"global_parity_files":parity,"baton":index,"lifecycle":{"phase_commits":4,"phase_merges":0,"final_parent":CORRECTED},"remote":{"local":head,"upstream":up,"tracking":tracking,"fresh_live":live,"divergence":[0,0],"clean":True},"same_owner_only":True,"independent_reproduction":False,"full_repository_suite":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20","route_state":"PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--receipt-root",type=Path,required=True); ap.add_argument("--skill-root",type=Path,required=True); ap.add_argument("--runner-root",type=Path,required=True); a=ap.parse_args(); a.receipt_root.mkdir(parents=True,exist_ok=True); head=git("rev-parse","HEAD"); latch=a.receipt_root/f"orin-v687-v7-{head}.latch.json"; receipt=a.receipt_root/f"orin-v687-v7-{head}.json"; fd=os.open(latch,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as h: json.dump({"state":"CANONICAL_INVOKED_ONCE","head":head},h,indent=2,sort_keys=True); h.write("\n")
    try:
        payload=canonical(a.skill_root,a.runner_root); raw=(json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode(); wrapper={"payload":payload,"payload_sha256":hashlib.sha256(raw).hexdigest()}; receipt.write_text(json.dumps(wrapper,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n"); print(json.dumps({"status":payload["status"],"exact_final":head,"payload_sha256":wrapper["payload_sha256"],"receipt":receipt.name},sort_keys=True)); return 0
    except Exception as exc:
        (a.receipt_root/f"orin-v687-v7-{head}.failed.json").write_text(json.dumps({"status":"FAILED_ZERO_CANONICAL_SUCCESS_CREDIT","head":head,"error_type":type(exc).__name__,"error":str(exc)},indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); raise
if __name__=="__main__": raise SystemExit(main())
