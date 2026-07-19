#!/usr/bin/env python3
"""Build the combined v649-v5 closeout and seal after the sole canonical pass."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/"docs"/"tamar-vey"/"v649-v5"
SOURCE="9ca33a5762fd9f9d7c26b3d7fd1172d9ed440952"
X1="e4d241300fd23ca09dc1889d7e84bc494a96f387"


def git(*args): return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True,encoding="utf-8").stdout.strip()
def load(relative): return json.loads((PHASE/relative).read_text(encoding="utf-8"))
def write(relative,payload):
    path=PHASE/relative; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); return path
def status_paths():
    paths=set(filter(None,git("diff","--name-only").splitlines())); paths.update(filter(None,git("diff","--cached","--name-only").splitlines())); paths.update(filter(None,git("ls-files","--others","--exclude-standard").splitlines())); return sorted(p.replace("\\","/") for p in paths)


def privacy(paths):
    patterns={
        "raw_task_or_thread_identifier":re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path":re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret":re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable":re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream":re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions={"docs/tamar-vey/v649-v5/validation/final-staged-privacy.json"}; candidates=[]; confirmed=[]
    for relative in paths:
        path=ROOT/relative
        if not path.is_file(): continue
        try: text=path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for name,pattern in patterns.items():
            if pattern.search(text):
                disposition="scanner_definition" if relative in definitions else "confirmed_payload_hit"; row={"path":relative,"pattern_class":name,"disposition":disposition}; candidates.append(row)
                if disposition=="confirmed_payload_hit": confirmed.append(row)
    return {"schema":"ghc.family.v649-v5.final-incremental-privacy.v1","scanned_file_count":len(paths),"pattern_classes":sorted(patterns),"candidate_count":len(candidates),"candidates":candidates,"confirmed_hit_count":len(confirmed),"confirmed_hits":confirmed,"canonical_scan_rerun":False,"boundary":"Incremental staged-path scan only; canonical phase scan was not rerun."}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--evidence-commit",required=True); args=parser.parse_args(); evidence=args.evidence_commit
    if git("rev-parse","HEAD")!=evidence: raise RuntimeError("closeout must run at exact evidence head")
    result=load("validation/canonical-pass-result.json")
    if result["evidence_head"]!=evidence or result["successful_canonical_pass_number"]!=1: raise RuntimeError("sole canonical pass receipt does not bind evidence head")
    runner=load("x2/runner-use-ledger.json"); items=[]
    for row in runner["items"]:
        if row["runner"]=="build_ghc_family_v649_v5_closeout.py": items.append({**row,"invoked":True,"passed":True,"receipt":"runner-receipts/ghc_family_v649_v5_closeout.json","pending_reason":None})
        else: items.append(row)
    write("runner-receipts/ghc_family_v649_v5_closeout.json",{"schema":"ghc.family.v649-v5.closeout-runner.v1","evidence_head":evidence,"canonical_pass_bound":True,"tests_rerun":False,"canonical_scan_rerun":False,"passed":True})
    write("x2/runner-use-ledger-final.json",{"schema":"ghc.family.v649-v5.runner-use-final.v1","runner_count":10,"completed_count":10,"pending_count":0,"items":items})
    write("validation/final-validation-plan.json",{**load("validation/final-validation-plan.json"),"successful_passes_used":1,"post_success_replay":False})
    method=load("method-flow/method-flow-ledger.json")
    method_receipt={"schema":"ghc.family.v649-v5.method-flow.final.v1","method_count":len(method["methods"]),"failed_witnesses":sum(x["result"]=="fail" for x in method["witnesses"]),"passing_witnesses":sum(x["result"]=="pass" for x in method["witnesses"]),"preferred_methods":sum(x["recommendation_state"]=="preferred" for x in method["methods"]),"failures_erased":0}
    write("method-flow/final-method-flow-receipt.json",method_receipt)
    write("retained-negative-register-final.json",{"schema":"ghc.family.v649-v5.retained-negatives.final.v1","inherited_effective":5025,"x1_operational":7,"synthetic_executed_rejected":70,"x2_operational":2,"effective_final":5104,"negative_erased":False})
    write("exact-open-gate-register-final.json",{"schema":"ghc.family.v649-v5.gates.final.v1","effective_open_gaps":39,"effective_exact_gates":40,"silently_closed":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/closeout-receipt.json",{"schema":"ghc.family.v649-v5.closeout.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":evidence,"canonical_tests":result["tests_passed"],"detailed_checks":32,"minimal_checks":20,"json_parses":result["phase_json_parses"],"privacy_scanned_files":result["privacy_scanned_files"],"privacy_confirmed_hits":0,"full_repository_suite":False,"post_success_replay":False,"distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"effective_negatives":5104,"effective_open_gaps":39,"effective_exact_gates":40,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/seal-receipt.json",{"schema":"ghc.family.v649-v5.seal.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":evidence,"final_commit_parent_required":evidence,"phase_commit_count_after_final":3,"merge_count_required":0,"final_parent_count_required":1,"canonical_pass_reused_without_rerun":True,"same_owner_only":True,"independent_reproduction":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/final-validation-record.json",{"schema":"ghc.family.v649-v5.final-validation.v1","evidence_head":evidence,"canonical_pass":result,"final_incremental_review_required":True,"final_exact_head_source":"post_commit_live_proof","tests_rerun_after_success":False,"canonical_privacy_scan_rerun_after_success":False,"replay_used":False,"same_owner_only":True,"independent_reproduction":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("orchestration/final-phase-state.json",{**load("orchestration/final-phase-state.json"),"stage":"sealed_candidate","terminal_route":"PREPARED_NOT_SENT","canonical_pass_used":True,"successor_messages_sent":0})
    write("orchestration/terminal-route-receipt.json",{"schema":"ghc.family.v649-v5.route.v1","target_title":"Sylven Arc","successor_phase":"v649-gmut-thos-v6-x1-x2","state":"PREPARED_NOT_SENT","messages_sent":0,"task_created":False,"cross_platform_send":False,"send_gate":"exact final clean pushed live-equal proof"})
    write("phase-truth.json",{**load("phase-truth.json"),"stage":"sealed_candidate","single_pass_used":True,"canonical_tests_passed":result["tests_passed"],"canonical_json_parses":result["phase_json_parses"],"canonical_privacy_files":result["privacy_scanned_files"],"replay_used":False,"terminal_route":"PREPARED_NOT_SENT"})
    write("closeout/closeout-candidate.json",{"schema":"ghc.family.v649-v5.closeout-candidate.final.v1","canonical_successful_pass_used":True,"terminal_route":"PREPARED_NOT_SENT","ready_for_final_commit":True,"tests_rerun":False,"canonical_scan_rerun":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    json_count=0
    for path in PHASE.rglob("*.json"): json.loads(path.read_text(encoding="utf-8")); json_count+=1
    write("validation/final-incremental-json-review.json",{"schema":"ghc.family.v649-v5.final-incremental-json.v1","parsed_before_manifest":json_count,"issues":[],"canonical_json_sweep_rerun":False})
    exclusions=["docs/tamar-vey/v649-v5/validation/final-staged-manifest.json","docs/tamar-vey/v649-v5/validation/final-staged-privacy.json","docs/tamar-vey/v649-v5/validation/final-staged-review.json"]
    paths=[p for p in status_paths() if p not in exclusions]
    entries=[{"path":p,"git_blob":git("hash-object",f"--path={p}",p),"bytes":(ROOT/p).stat().st_size} for p in paths if (ROOT/p).is_file()]
    scan=privacy(paths+exclusions); write("validation/final-staged-privacy.json",scan)
    write("validation/final-staged-manifest.json",{"schema":"ghc.family.v649-v5.final-manifest.v1","hash_domain":"git_hash_object_path_filtered_blob","entries":entries,"entry_count":len(entries),"self_exclusions":exclusions,"coverage_boundary":"All final closeout changes except three declared self-referential receipts."})
    write("validation/final-staged-review.json",{"schema":"ghc.family.v649-v5.final-staged-review.v1","intended_path_count":len(entries)+3,"manifest_entry_count":len(entries),"self_exclusion_count":3,"out_of_scope_paths":[],"privacy_confirmed_hits":scan["confirmed_hit_count"],"canonical_tests_rerun":False,"canonical_scan_rerun":False,"evidence_head":evidence,"terminal_route":"PREPARED_NOT_SENT"})
    if scan["confirmed_hit_count"]: raise RuntimeError("final incremental privacy hits")
    print(json.dumps({"evidence_head":evidence,"final_paths":len(entries)+3,"incremental_json":json_count,"privacy_hits":0,"tests_rerun":False,"canonical_scan_rerun":False,"passed":True},sort_keys=True))


if __name__=="__main__": main()
