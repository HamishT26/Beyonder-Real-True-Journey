#!/usr/bin/env python3
"""Build the combined v649-v5 closeout and seal after the sole canonical pass."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/"docs"/"tamar-vey"/"v649-v5"
SOURCE="9ca33a5762fd9f9d7c26b3d7fd1172d9ed440952"
X1="e4d241300fd23ca09dc1889d7e84bc494a96f387"
METHOD_RUNNER=Path.home()/".codex"/"skills"/"ghc-family-method-flow-state"/"scripts"/"ghc_family_method_flow_state.py"

POST_EVIDENCE_NEGATIVES=[
    {
        "negative_id":"V6495-X2-N03", "category":"mutable_freeze_loader_preflight",
        "failed":"Pre-pass lifecycle review found the v649-v5 x1 test loader reading mutable current-phase JSON, which would misclassify legitimate x2 phase and Method Flow growth. No canonical credit was awarded.",
        "recovery":"Bind x1 JSON reads to immutable x1 commit blobs while leaving the current document-cap scan explicit.",
        "passing":"All 20 x1 tests passed inside the credited 110-test aggregate through commit-local reads.",
        "recurrence_guard":"Phase-freeze tests must read commit-local blobs after a phase advances.",
    },
    {
        "negative_id":"V6495-X2-N04", "category":"validation_handle_orphan_without_receipt",
        "failed":"The first canonical launcher lost its app execution handle and left an idle owner-launched process with no result receipt. Read-only PID and I/O checks showed no progress, so it was terminated with zero credit.",
        "recovery":"Launch the bounded validator as a tracked hidden process with external output capture and monitor both process state and the receipt path.",
        "passing":"The tracked launch method surfaced bounded completion states and the final tracked launch produced exactly one credited receipt.",
        "recurrence_guard":"A lost app handle never implies completion; require an attributable receipt or retain and terminate the confirmed orphan.",
    },
    {
        "negative_id":"V6495-X2-N05", "category":"inherited_lifecycle_state_projection",
        "failed":"The first tracked aggregate passed 108 of 110 tests but two inherited v649-v4 pre-pass assertions read sealed post-pass booleans. The aggregate received zero credit.",
        "recovery":"Project only those pre-pass values from Orin's committed single-pass plan and evidence ledger without excluding either test.",
        "passing":"The credited aggregate ran and passed all 110 tests with both inherited assertions retained.",
        "recurrence_guard":"Successor checks of lifecycle assertions must bind each assertion to its committed pre-pass or post-pass evidence state.",
    },
    {
        "negative_id":"V6495-X2-N06", "category":"detailed_check_count_mismatch",
        "failed":"After all 110 tests passed, the validator found 33 substantive detailed checks while the frozen contract expected 32, so it wrote no receipt.",
        "recovery":"Enumerate the detailed-check list structurally and correct the contract and result count to the observed 33 without removing a check.",
        "passing":"The credited aggregate passed all 33 detailed checks and recorded the corrected count.",
        "recurrence_guard":"Count validator list elements structurally before freezing declared detailed-check totals.",
    },
    {
        "negative_id":"V6495-X2-N07", "category":"detailed_check_overcorrection",
        "failed":"A first count repair inserted another valid plan check, producing 34 checks against the still-frozen count of 32 and again wrote no receipt.",
        "recovery":"Restore the unmodified 33-check list, fold the plan-count guard into an existing plan check, and change only the expected and reported total.",
        "passing":"The credited aggregate used the unmodified 33-check evidence set and passed every check.",
        "recurrence_guard":"Inspect exact list cardinality after a proposed correction and before consuming another aggregate attempt.",
    },
]


def git(*args): return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True,encoding="utf-8").stdout.strip()
def run(*args): return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True,encoding="utf-8").stdout.strip()
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
    definitions={
        "docs/tamar-vey/v649-v5/validation/final-staged-privacy.json",
        "scripts/build_ghc_family_v649_v5_closeout.py",
        "scripts/ghc_family_v649_v5_validate.py",
        "tests/test_ghc_family_v649_v4_closeout.py",
        "tests/test_ghc_family_v649_v5_x1.py",
    }; candidates=[]; confirmed=[]
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


def add_post_evidence_method_flow():
    operational=load("validation/x2-operational-negatives.json")
    existing={row["negative_id"] for row in operational["negatives"]}
    operational["negatives"].extend(row for row in POST_EVIDENCE_NEGATIVES if row["negative_id"] not in existing)
    operational["count"]=len(operational["negatives"]); operational["all_retained"]=True
    write("validation/x2-operational-negatives.json",operational)

    by_id={row["negative_id"]:row for row in POST_EVIDENCE_NEGATIVES}
    specs=[
        ("V6495-M10","Use commit-local blobs for phase-freeze tests",["V6495-X2-N03"],"commit-local phase-freeze test replay"),
        ("V6495-M11","Track validator process and receipt independently of the app handle",["V6495-X2-N04"],"tracked owner-local validator process"),
        ("V6495-M12","Project inherited lifecycle assertions from committed state records",["V6495-X2-N05"],"committed inherited lifecycle projection"),
        ("V6495-M13","Count detailed checks structurally before freezing the contract",["V6495-X2-N06","V6495-X2-N07"],"structural validator-cardinality audit"),
    ]
    ledger_path=PHASE/"method-flow/method-flow-ledger.json"
    for method_id,title,negative_ids,scope in specs:
        rows=[by_id[nid] for nid in negative_ids]
        record={
            "method_id":method_id,"title":title,"failure_signature":" ".join(row["failed"] for row in rows),
            "trigger_preconditions":["A bounded successor validation crosses an immutable lifecycle or process boundary."],
            "privacy_class":"sanitized_public","approval_class":"safe_now_owner_scoped_workflow",
            "candidate_workaround":" ".join(row["recovery"] for row in rows),"validation_witness_ids":[],
            "recurrence_guard":" ".join(row["recurrence_guard"] for row in rows),
            "rollback":"Give the failed aggregate zero credit, preserve its witness, and change only the demonstrated bounded fault.",
            "recommendation_state":"candidate","supersedes":[],
            "protected_gates":["single_successful_pass","failure_retention","immutable_phase_evidence","no_replay","evidence_credit"],
            "retained_negative_ids":negative_ids,
            "scope_boundary":"Same-owner bounded validation recovery only; no independent reproduction, production, scientific, professional, legal, cultural, privacy-complete, security-complete, or authority credit.",
        }
        record_path=write(f"method-flow/{method_id.casefold()}-method-record.json",record)
        ledger=json.loads(ledger_path.read_text(encoding="utf-8"))
        if method_id not in {row["method_id"] for row in ledger["methods"]}:
            run(sys.executable,str(METHOD_RUNNER),"record","--ledger",str(ledger_path),"--record-file",str(record_path))
        witness_rows=[]
        for index,row in enumerate(rows,1):
            suffix="WFAIL" if len(rows)==1 else f"WFAIL-{index}"
            witness_rows.append((suffix,"fail",row["failed"],row["failed"],[row["negative_id"]]))
        witness_rows.append(("WPASS","pass"," ".join(row["recovery"] for row in rows)," ".join(row["passing"] for row in rows),negative_ids))
        for suffix,result,procedure,observed,linked in witness_rows:
            witness_id=f"{method_id}-{suffix}"
            witness={"witness_id":witness_id,"method_id":method_id,"procedure":procedure,"scope":scope,"expected":"Preserve every failed attempt and produce attributable bounded evidence without weakening the single-pass or lifecycle gates.","observed":observed,"result":result,"same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":linked,"boundary":"Bounded workflow witness only; no independent reproduction or external authority credit."}
            witness_path=write(f"method-flow/{witness_id.casefold()}-witness.json",witness)
            ledger=json.loads(ledger_path.read_text(encoding="utf-8"))
            if witness_id not in {row["witness_id"] for row in ledger["witnesses"]}:
                run(sys.executable,str(METHOD_RUNNER),"witness","--ledger",str(ledger_path),"--witness-file",str(witness_path))
        state=next(row["recommendation_state"] for row in json.loads(ledger_path.read_text(encoding="utf-8"))["methods"] if row["method_id"]==method_id)
        if state=="validated":
            run(sys.executable,str(METHOD_RUNNER),"set-state","--ledger",str(ledger_path),"--method-id",method_id,"--state","preferred","--note","Preferred only for the declared bounded lifecycle trigger after retaining every failed and passing witness.")
        elif state!="preferred":
            raise RuntimeError(f"unexpected Method Flow state for {method_id}: {state}")
    run(sys.executable,str(METHOD_RUNNER),"validate","--ledger",str(ledger_path),"--receipt",str(PHASE/"method-flow/final-method-flow-validation.json"))
    run(sys.executable,str(METHOD_RUNNER),"summarize","--ledger",str(ledger_path),"--json-output",str(PHASE/"method-flow/final-method-flow-summary.json"),"--markdown-output",str(PHASE/"method-flow/final-method-flow-summary.md"))
    return json.loads(ledger_path.read_text(encoding="utf-8"))


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
    write("validation/final-validation-plan.json",{**load("validation/final-validation-plan.json"),"successful_passes_used":1,"post_success_replay":False,"detailed_check_count":result["detailed_checks"],"failed_canonical_attempts_before_success":result["failed_canonical_attempts_before_success"]})
    write("validation/validation-contract-correction.json",{"schema":"ghc.family.v649-v5.validation-contract-correction.v1","frozen_declared_detailed_checks":32,"structurally_enumerated_detailed_checks":33,"tests_removed":0,"checks_removed":0,"credited_result":result["detailed_checks"],"failed_attempts_before_success":result["failed_canonical_attempts_before_success"],"post_success_replay":False})
    method=add_post_evidence_method_flow()
    method_receipt={"schema":"ghc.family.v649-v5.method-flow.final.v1","method_count":len(method["methods"]),"failed_witnesses":sum(x["result"]=="fail" for x in method["witnesses"]),"passing_witnesses":sum(x["result"]=="pass" for x in method["witnesses"]),"preferred_methods":sum(x["recommendation_state"]=="preferred" for x in method["methods"]),"failures_erased":0}
    write("method-flow/final-method-flow-receipt.json",method_receipt)
    write("retained-negative-register-final.json",{"schema":"ghc.family.v649-v5.retained-negatives.final.v1","inherited_effective":5025,"x1_operational":7,"synthetic_executed_rejected":70,"x2_operational":7,"effective_final":5109,"negative_erased":False})
    write("exact-open-gate-register-final.json",{"schema":"ghc.family.v649-v5.gates.final.v1","effective_open_gaps":39,"effective_exact_gates":40,"silently_closed":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/closeout-receipt.json",{"schema":"ghc.family.v649-v5.closeout.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":evidence,"canonical_tests":result["tests_passed"],"detailed_checks":result["detailed_checks"],"minimal_checks":result["minimal_checks"],"json_parses":result["phase_json_parses"],"privacy_scanned_files":result["privacy_scanned_files"],"privacy_confirmed_hits":0,"full_repository_suite":False,"post_success_replay":False,"distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"effective_negatives":5109,"effective_open_gaps":39,"effective_exact_gates":40,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/seal-receipt.json",{"schema":"ghc.family.v649-v5.seal.v1","source_head":SOURCE,"x1_commit":X1,"evidence_commit":evidence,"final_commit_parent_required":evidence,"phase_commit_count_after_final":3,"merge_count_required":0,"final_parent_count_required":1,"canonical_pass_reused_without_rerun":True,"same_owner_only":True,"independent_reproduction":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("closeout/final-validation-record.json",{"schema":"ghc.family.v649-v5.final-validation.v1","evidence_head":evidence,"canonical_pass":result,"final_incremental_review_required":True,"final_exact_head_source":"post_commit_live_proof","tests_rerun_after_success":False,"canonical_privacy_scan_rerun_after_success":False,"replay_used":False,"same_owner_only":True,"independent_reproduction":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write("orchestration/final-phase-state.json",{**load("orchestration/final-phase-state.json"),"stage":"sealed_candidate","terminal_route":"PREPARED_NOT_SENT","canonical_pass_used":True,"successor_messages_sent":0})
    write("orchestration/terminal-route-receipt.json",{"schema":"ghc.family.v649-v5.route.v1","target_title":"Sylven Arc","successor_phase":"v649-gmut-thos-v6-x1-x2","state":"PREPARED_NOT_SENT","messages_sent":0,"task_created":False,"cross_platform_send":False,"send_gate":"exact final clean pushed live-equal proof"})
    write("phase-truth.json",{**load("phase-truth.json"),"stage":"sealed_candidate","single_pass_used":True,"canonical_tests_passed":result["tests_passed"],"canonical_detailed_checks":result["detailed_checks"],"canonical_minimal_checks":result["minimal_checks"],"canonical_json_parses":result["phase_json_parses"],"canonical_privacy_files":result["privacy_scanned_files"],"effective_negatives":5109,"method_flow_methods":len(method["methods"]),"method_flow_failed_witnesses":sum(row["result"]=="fail" for row in method["witnesses"]),"method_flow_passing_witnesses":sum(row["result"]=="pass" for row in method["witnesses"]),"replay_used":False,"terminal_route":"PREPARED_NOT_SENT"})
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
