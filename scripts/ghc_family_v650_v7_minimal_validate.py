#!/usr/bin/env python3
"""Exact-final minimal validator for Eiren Kestrel v650-v7."""
import argparse,json,subprocess
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/eiren-kestrel/v650-v7"; EVIDENCE="6fe9cd18f870f93c65a4a0a7992add3781d7fe01"
def git(*a): return subprocess.check_output(["git",*a],cwd=REPO).decode().strip()
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
def main():
 p=argparse.ArgumentParser(); p.add_argument("--expected-head",required=True); p.add_argument("--receipt",required=True); a=p.parse_args(); head=git("rev-parse","HEAD")
 checks={"exact_head":head==a.expected_head,"clean_state":not git("status","--porcelain=v1","--untracked-files=all"),"direct_parent":git("rev-parse","HEAD^")==EVIDENCE,"suite":load("validation/full-repository-suite-recovery.json")["successful"],"truth":load("final/phase-truth.json")["terminal_verdict"]=="NOT_READY_FOR_STAGE_20","route":load("orchestration/final-phase-state.json")["terminal_route"]=="PREPARED_NOT_SENT"}; payload={"schema":"ghc.family.v650-v7.final-minimal-validation.external.v1","exact_head":head,"checks":checks,"check_count":len(checks),"passed_count":sum(checks.values()),"valid":all(checks.values())}; Path(a.receipt).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); print(json.dumps(payload,sort_keys=True)); return 0 if payload["valid"] else 1
if __name__=="__main__": raise SystemExit(main())
