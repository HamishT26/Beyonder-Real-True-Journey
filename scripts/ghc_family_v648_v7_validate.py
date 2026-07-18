#!/usr/bin/env python3
"""Single successful canonical scoped validator for the assembled v648-v7 candidate."""

import argparse, json, re, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHASE=ROOT/'docs/tamar-vey/v648-v7'; sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'scripts'))
from build_ghc_family_v648_v7_evidence import git
import ghc_family_v648_v7_x2_state as x2
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    plan=load('validation/final-validation-plan.json')
    def ids(suite):
        rows=[]
        for item in suite:
            rows.extend(ids(item) if isinstance(item,unittest.TestSuite) else [item.id()])
        return rows
    selected=[name for name in ids(unittest.defaultTestLoader.loadTestsFromNames(plan['test_modules'])) if name not in set(plan['excluded_source_local_tests'])]
    if len(selected)!=plan['selected_test_count']: raise RuntimeError(f"expected {plan['selected_test_count']} selected tests, found {len(selected)}")
    cmd=[sys.executable,'-B','-m','unittest',*selected]
    tests=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8'); combined=tests.stdout+tests.stderr
    if tests.returncode: raise RuntimeError(combined[-4000:])
    m=re.search(r'Ran (\d+) tests',combined); test_count=int(m.group(1)) if m else -1
    files=[p for p in PHASE.rglob('*') if p.is_file()]; json_files=[p for p in files if p.suffix.lower()=='.json']
    for p in json_files: json.loads(p.read_text(encoding='utf-8'))
    patterns={'raw_task_or_thread_identifier':re.compile(r'(?i)(source_thread_id|thread_id)\s*[:=]'),'private_absolute_local_path':re.compile(r'(?i)[A-Z]:\\Users\\[^\s\"\']+'),'credential_or_secret':re.compile(r'(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})'),'private_route_or_callable':re.compile(r'(?i)(private_route|callable_identifier|browser_send_submitted_response_active)'),'transcript_or_session_stream':re.compile(r'(?i)(session_stream|raw_transcript|conversation_export)')}
    strict=re.compile(r'(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"\'][^\"\']{6,}[\"\']|bearer\s+[A-Za-z0-9._-]{12,}'); hits=[]
    for p in files:
        try:t=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:continue
        rel=p.relative_to(PHASE).as_posix()
        for cls,pat in patterns.items():
            if not pat.search(t):continue
            defined=rel.startswith('validation/') and ('privacy' in rel or 'canonical-validation' in rel) or rel=='approval-packets/inherited-exact-approvals.json' or rel=='validation/x1-operational-negatives.json' or (rel.startswith('method-flow/') and cls=='credential_or_secret' and not strict.search(t))
            if not defined:hits.append({'path':rel,'class':cls})
    if hits: raise RuntimeError(f'privacy hits: {hits}')
    detailed=[
        git('rev-parse','HEAD^')==x2.X1_COMMIT,git('rev-list','--count',f'38e3fe7bc710239337f831617ced97bec51d7d7a..HEAD')=='2',git('rev-list','--merges','--count',f'38e3fe7bc710239337f831617ced97bec51d7d7a..HEAD')=='0',
        load('x2/core-outcome-ledger.json')['distribution']=={'completed':6,'represented':2,'open_gap':1,'exact_gate':1},load('x2/evidence-ledger.json')['real_rows']==0,load('x2/evidence-ledger.json')['real_participants_or_operators']==0,load('x2/evidence-ledger.json')['real_keys_or_proofs']==0,load('x2/evidence-ledger.json')['authority_decisions']==0,
        load('x2/portfolio-ledger.json')['safe_completed']==30,load('x2/portfolio-ledger.json')['candidates_completed']==20,load('x2/skill-use-ledger-final.json')['completed_count']==20,load('x2/runner-use-ledger-final.json')['completed_count']==10,load('x2/portfolio-ledger.json')['clean_refine_completed']==30,load('validation/x2-synthetic-mutation-results.json')['rejected_count']==70,
        load('x2/gate-register.json')['open_gaps']==33,load('x2/gate-register.json')['exact_gates']==34,load('stage20-terminal-board.json')['ready'] is False,load('phase-truth-final-candidate.json')['terminal_route']=='PREPARED_NOT_SENT',load('validation/final-staged-review.json')['actual_staged_review'] is True,load('validation/final-staged-review.json')['actual_privacy_confirmed_hit_count']==0,
        load('closeout/closeout-build-receipt.json')['overview_three_page_equivalent'] is True,Path(PHASE/'accessible-report.html').is_file(),load('complete-incomplete-checklist.json')['incomplete'][-1]=='stage20',load('orchestration/final-phase-state.json')['subagents']==0,load('orchestration/final-phase-state.json')['cross_platform_messages']==0,
        load('validation/final-validation-plan.json')['full_repository_suite'] is False,load('validation/final-validation-plan.json')['replay_budget']==0,load('x2/evidence-ledger.json')['independent_reproduction'] is False,load('retained-negative-register-final.json')['negative_erased'] is False,load('method-flow/method-flow-validation.json')['valid'] is True,not subprocess.run(['git','diff','--cached','--check'],cwd=ROOT).returncode,git('rev-parse','@{upstream}')==git('rev-parse','HEAD')]
    minimal=[len(load('x1-proposals.json')['proposals'])==10,load('provenance/frozen-chain-proposal-index.json')['count']==630,load('x2/core-outcome-ledger.json')['count']==10,load('x2/skill-use-ledger-final.json')['skill_count']==20,load('x2/runner-use-ledger-final.json')['runner_count']==10,load('validation/x2-synthetic-mutation-results.json')['count']==70,len(patterns)==5,len(hits)==0,len(json_files)>100,len(files)<15000,load('phase-truth-final-candidate.json')['full_suite_used'] is False,load('phase-truth-final-candidate.json')['replay_used'] is False,load('stage20-terminal-board.json')['verdict']=='NOT_READY_FOR_STAGE_20',load('exact-open-gate-register-final.json')['silently_closed']==0,load('wellbeing-closeout.json')['pause_right_preserved'] is True,load('closeout/closeout-candidate.json')['x1_commit']==x2.X1_COMMIT,load('validation/final-staged-review.json')['actual_blob_mismatch_count']==0,load('validation/final-staged-review.json')['actual_checkout_byte_mismatch_count']==0,load('validation/final-staged-review.json')['actual_path_parity_passed'] is True,load('validation/final-staged-review.json')['actual_diff_hygiene_passed'] is True]
    if not all(detailed) or not all(minimal): raise RuntimeError(f'detailed={sum(detailed)}/32 minimal={sum(minimal)}/20')
    payload={'schema':'ghc.family.v648-v7.canonical-validation.external.v1','passed':True,'test_count':test_count,'detailed_passed':sum(detailed),'detailed_total':32,'minimal_passed':sum(minimal),'minimal_total':20,'json_parses':len(json_files),'privacy_scanned_files':len(files),'privacy_pattern_classes':5,'privacy_confirmed_hits':0,'full_suite':False,'replay':False,'candidate_head':git('rev-parse','HEAD'),'candidate_staged_tree':git('write-tree'),'same_owner_only':True,'independent_reproduction':False}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n'); print(json.dumps(payload,sort_keys=True))
if __name__=='__main__': main()
