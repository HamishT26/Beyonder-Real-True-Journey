#!/usr/bin/env python3
"""Detailed validator for the Eiren v646-v1 evidence and lifecycle heads."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v646-v1")
PHASE = ROOT / PHASE_REL
SOURCE = "6dc3311e3c4c390c945d001f75fb17d320c0a548"
X1 = "7b7824b7643bfb3a80cf778a10ca65055554b5db"
OUTCOMES = {"completed","represented","open_gap","exact_gate"}
PRIVATE = {
    "raw_uuid":re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup":re.compile(r"(?i)<\/?codex_delegation>|<source_thread_id>"),
    "private_uri":re.compile(r"(?i)\b(?:app|plugin)://"),
    "private_local_path":re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+"),
    "credential_assignment":re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> str:
    result=subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True)
    if check and result.returncode: raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def logical_hash(path: Path) -> str:
    data=path.read_bytes()
    try: data.decode("utf-8")
    except UnicodeDecodeError: normalized=data
    else: normalized=data.replace(b"\r\n",b"\n")
    return hashlib.sha256(normalized).hexdigest()


def privacy(files: list[Path]) -> dict[str, Any]:
    candidates=[]
    for path in files:
        try: text=path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for kind,pattern in PRIVATE.items():
            for match in pattern.finditer(text): candidates.append({"path":path.relative_to(ROOT).as_posix(),"class":kind,"offset":match.start()})
    return {"pattern_classes":sorted(PRIVATE),"scanned_files":len(files),"confirmed_hits":candidates,"confirmed_hit_count":len(candidates),"valid":not candidates}


def validate(mode: str, expected_head: str | None, require_clean: bool) -> dict[str, Any]:
    issues=[]; checks=0
    files=sorted(p for p in PHASE.rglob("*") if p.is_file())
    required=["x1-proposals.json","x2-proposal-ledger.json","phase-truth.json","v646-v1-integrated-overview.md","deliverables/v646-v1-evidence-report.html","approval-packets/x2-execution-ledger.json","prototypes/skill-build-receipt.json","prototypes/runner-build-receipt.json","maintenance/x2-clean-refine-receipt.json","validation/runtime-smoke-results.json","validation/evidence-manifest.json","threat-model.json","complete-incomplete-checklist.json","retained-negative-register.json","open-exact-gate-register.json"]
    for name in required:
        checks+=1
        if not (PHASE/name).is_file(): issues.append(f"missing {name}")
    json_files=[p for p in files if p.suffix==".json"]
    parse_fail=[]
    for path in json_files:
        checks+=1
        try: load(path)
        except Exception as exc: parse_fail.append({"path":path.relative_to(ROOT).as_posix(),"error":str(exc)})
    if parse_fail: issues.append(f"JSON parse failures: {parse_fail}")

    if not issues:
        proposals=load(PHASE/"x1-proposals.json"); outcomes=load(PHASE/"x2-proposal-ledger.json"); truth=load(PHASE/"phase-truth.json")
        checks+=12
        if proposals.get("frozen_chain_count_after_x1")!=400 or len(proposals.get("proposals",[]))!=10: issues.append("proposal count mismatch")
        rows=outcomes.get("outcomes",[])
        if len(rows)!=10 or {x.get("outcome") for x in rows}-OUTCOMES: issues.append("outcome vocabulary or count mismatch")
        dist={state:sum(x.get("outcome")==state for x in rows) for state in OUTCOMES}
        if dist!={"completed":6,"represented":2,"open_gap":1,"exact_gate":1}: issues.append(f"outcome distribution mismatch: {dist}")
        if truth.get("terminal_verdict")!="NOT_READY_FOR_STAGE_20": issues.append("terminal verdict mismatch")
        if truth.get("real_data_rows_ingested")!=0 or truth.get("real_participants")!=0 or truth.get("real_keys_or_proofs")!=0: issues.append("real evidence count overstated")

        approval=load(PHASE/"approval-packets/x2-execution-ledger.json")
        if approval.get("safe_now_executed")!=30 or approval.get("candidates_executed")!=20: issues.append("expanded approval execution count mismatch")
        if approval.get("exact_or_external_packets_executed")!=0 or approval.get("blocked_packets_executed")!=0: issues.append("exact or blocked packet executed")
        skills=load(PHASE/"prototypes/skill-build-receipt.json"); runners=load(PHASE/"prototypes/runner-build-receipt.json"); clean=load(PHASE/"maintenance/x2-clean-refine-receipt.json")
        if not skills.get("valid") or skills.get("skill_count")!=20 or skills.get("validated_count")!=20 or skills.get("smoke_use_pass_count")!=20: issues.append("skill build receipt failed")
        if not runners.get("valid") or runners.get("runner_count")!=10 or runners.get("used_count")!=10: issues.append("runner build receipt failed")
        if not clean.get("valid") or clean.get("completed_count")!=30 or clean.get("destructive_action_count")!=0: issues.append("cleanup receipt failed")
        runtime=load(PHASE/"validation/runtime-smoke-results.json")
        if len(runtime)!=10 or any(not x.get("passed") for x in runtime.values()): issues.append("runtime smoke suite failed")
        negatives=load(PHASE/"retained-negative-register.json")
        if negatives.get("inherited_effective")!=2432 or negatives.get("preregistered_synthetic")!=70 or negatives.get("new_operational_count")!=4 or negatives.get("effective_total")!=2506: issues.append("retained-negative accounting mismatch")
        gates=load(PHASE/"open-exact-gate-register.json")
        if gates.get("inherited_open_gap_count")!=10 or gates.get("inherited_exact_gate_count")!=11 or gates.get("silently_closed_count")!=0: issues.append("gate preservation mismatch")

        overview=(PHASE/"v646-v1-integrated-overview.md").read_text(encoding="utf-8")
        words=len(overview.split())
        if not 1500<=words<=6000: issues.append(f"overview word count outside 1500..6000: {words}")
        report=(PHASE/"deliverables/v646-v1-evidence-report.html").read_text(encoding="utf-8").casefold()
        for token in ("<html","<title","<main","<table","<caption","scope=","not_ready_for_stage_20","manual"):
            if token not in report: issues.append(f"report missing {token}")

        manifest=load(PHASE/"validation/evidence-manifest.json")
        entries=manifest.get("entries",[])
        if not entries: issues.append("evidence manifest empty")
        for row in entries:
            checks+=1
            path=ROOT/row["path"]
            if not path.is_file(): issues.append(f"manifest missing {row['path']}")
            elif logical_hash(path)!=row["logical_sha256"]: issues.append(f"manifest mismatch {row['path']}")

    scan=privacy(files); checks+=scan["scanned_files"]*len(PRIVATE)
    if not scan["valid"]: issues.append(f"privacy hits: {scan['confirmed_hits']}")
    head=git("rev-parse","HEAD")
    checks+=8
    if expected_head and head!=expected_head: issues.append(f"head mismatch {head} != {expected_head}")
    if subprocess.run(["git","merge-base","--is-ancestor",SOURCE,head],cwd=ROOT).returncode: issues.append("source is not ancestral")
    if subprocess.run(["git","merge-base","--is-ancestor",X1,head],cwd=ROOT).returncode: issues.append("x1 is not ancestral")
    merge_count=int(git("rev-list","--merges","--count",f"{SOURCE}..{head}") or "0")
    phase_commits=int(git("rev-list","--count",f"{SOURCE}..{head}") or "0")
    if merge_count!=0: issues.append("merge commit present")
    if phase_commits>4: issues.append(f"commit cap exceeded: {phase_commits}")
    dirty=git("status","--porcelain=v1","-uno")
    if require_clean and dirty: issues.append("worktree is not clean")
    branch=git("rev-parse","--abbrev-ref","HEAD")
    return {"schema":"ghc.family.v646-v1.validation.v1","mode":mode,"head":head,"branch":branch,"expected_head":expected_head,"file_count":len(files),"json_parse_count":len(json_files),"privacy":scan,"check_count":checks,"merge_count":merge_count,"phase_commit_count":phase_commits,"clean_required":require_clean,"clean":not bool(dirty),"issues":issues,"valid":not issues,"boundary":"Validation is owner-scoped structural and executable evidence only; same-owner replay is not independent reproduction."}


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--mode",choices=["evidence","closeout","seal","final","replay"],default="evidence"); parser.add_argument("--expected-head"); parser.add_argument("--require-clean",action="store_true"); parser.add_argument("--output",type=Path); args=parser.parse_args()
    result=validate(args.mode,args.expected_head,args.require_clean)
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(payload,encoding="utf-8",newline="\n")
    else: print(payload,end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__": raise SystemExit(main())
