#!/usr/bin/env python3
"""Exact-final detailed validator for Eiren Kestrel v650-v7."""
import argparse,hashlib,json,subprocess
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/eiren-kestrel/v650-v7"
SOURCE="9b1746193488fbb025c9e387164547503494abc5"; X1="1bbbb0ae75284597ff4c03b6b2b1e79534fbeba4"; EVIDENCE="6fe9cd18f870f93c65a4a0a7992add3781d7fe01"
def git(*a): return subprocess.check_output(["git",*a],cwd=REPO).decode("utf-8").strip()
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
def main():
 p=argparse.ArgumentParser(); p.add_argument("--expected-head",required=True); p.add_argument("--receipt",required=True); a=p.parse_args(); checks=[]
 def ck(name,ok): checks.append({"name":name,"passed":bool(ok)}); return bool(ok)
 head=git("rev-parse","HEAD"); ck("exact_head",head==a.expected_head); ck("clean_state",not git("status","--porcelain=v1","--untracked-files=all")); ck("direct_child_of_evidence",git("rev-parse","HEAD^")==EVIDENCE)
 ck("three_phase_commits",int(git("rev-list","--count",f"{SOURCE}..HEAD"))==3); ck("zero_merges",int(git("rev-list","--merges","--count",f"{SOURCE}..HEAD"))==0); ck("one_parent",len(git("show","-s","--format=%P","HEAD").split())==1)
 for anchor in (SOURCE,X1,EVIDENCE): ck(f"ancestral_{anchor[:10]}",subprocess.run(["git","merge-base","--is-ancestor",anchor,"HEAD"],cwd=REPO).returncode==0)
 manifest=load("validation/final-owner-manifest.json"); issues=[]
 for row in manifest["entries"]:
  data=subprocess.check_output(["git","cat-file","blob",row["git_blob"]],cwd=REPO)
  oid=git("rev-parse",f"HEAD:{row['path']}")
  if oid!=row["git_blob"] or len(data)!=row["bytes"] or hashlib.sha256(data).hexdigest()!=row["sha256"]: issues.append(row["path"])
 ck("owner_manifest",not issues); json_files=list(ROOT.rglob("*.json")); [json.loads(q.read_text(encoding="utf-8")) for q in json_files]; ck("json_parse",True)
 ck("owner_privacy",load("validation/final-owner-privacy.json")["confirmed_hit_count"]==0); ck("staged_privacy",load("validation/final-staged-privacy.json")["confirmed_hit_count"]==0)
 suite=load("validation/full-repository-suite-recovery.json"); ck("full_suite",suite["successful"] and suite["tests_run"]==2185 and not suite["post_success_replay"])
 truth=load("final/phase-truth.json"); ck("truth",truth["effective_negatives"]==6311 and truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20")
 payload={"schema":"ghc.family.v650-v7.final-detailed-validation.external.v1","exact_head":head,"check_count":len(checks),"passed_count":sum(x["passed"] for x in checks),"checks":checks,"json_parse_count":len(json_files),"manifest_issue_count":len(issues),"manifest_issues":issues,"same_owner_only":True,"independent_reproduction":False,"valid":all(x["passed"] for x in checks),"terminal_verdict":"NOT_READY_FOR_STAGE_20"}
 Path(a.receipt).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); print(json.dumps({"checks":len(checks),"passed":payload["passed_count"],"json":len(json_files),"valid":payload["valid"]},sort_keys=True)); return 0 if payload["valid"] else 1
if __name__=="__main__": raise SystemExit(main())
