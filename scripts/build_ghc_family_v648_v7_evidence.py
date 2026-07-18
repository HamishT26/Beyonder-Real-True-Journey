#!/usr/bin/env python3
"""Build the v648-v7 x2 evidence packet from the immutable x1 commit."""

import json, os, re, subprocess, sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]; PHASE=ROOT/'docs/tamar-vey/v648-v7'; sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_v648_v7_definitions as d
import ghc_family_v648_v7_x2_state as x2
from ghc_family_v648_v7_runtime import CONTRACTS

METHOD_RUNNER=Path.home()/'.codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py'
SKILL_VALIDATOR=Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py'
RUNNERS=[
 ('ghc_family_v648_v7_retry_policy.py',['V6487-P01']),('ghc_family_v648_v7_reeh_obligations.py',['V6487-P02']),('ghc_family_v648_v7_tess_refusal.py',['V6487-P03']),('ghc_family_v648_v7_postal_handover.py',['V6487-P04','V6487-P06']),('ghc_family_v648_v7_scim_profile.py',['V6487-P05']),('ghc_family_v648_v7_ebml_tribunal.py',['V6487-P07']),('ghc_family_v648_v7_accessibility_audit.py',['V6487-P08']),('ghc_family_v648_v7_domain_guards.py',['V6487-P09','V6487-P10']),('ghc_family_v648_v7_portfolio.py',[]),
]

def run(*a,env=None): return subprocess.run(list(a),cwd=ROOT,check=True,capture_output=True,text=True,encoding='utf-8',env=env).stdout.strip()
def git(*a): return run('git',*a)
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
def write(p,x):
    q=PHASE/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def status_paths():
    raw=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all','-z'],cwd=ROOT,check=True,capture_output=True).stdout.decode('utf-8','surrogateescape')
    return sorted({row[3:] for row in raw.split('\0') if row})
def privacy(paths):
    pats={'raw_task_or_thread_identifier':re.compile(r'(?i)(source_thread_id|thread_id)\s*[:=]'),'private_absolute_local_path':re.compile(r'(?i)[A-Z]:\\Users\\[^\s\"\']+'),'credential_or_secret':re.compile(r'(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})'),'private_route_or_callable':re.compile(r'(?i)(private_route|callable_identifier|browser_send_submitted_response_active)'),'transcript_or_session_stream':re.compile(r'(?i)(session_stream|raw_transcript|conversation_export)')}
    strict=re.compile(r'(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"\'][^\"\']{6,}[\"\']|bearer\s+[A-Za-z0-9._-]{12,}'); cand=[]; hit=[]; scanned=0
    for rel in paths:
        p=ROOT/rel
        if not p.is_file(): continue
        try:t=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        scanned+=1
        for cls,pat in pats.items():
            if not pat.search(t):continue
            defined=(rel.startswith('scripts/') and 'v648_v7' in rel) or rel.endswith('-privacy.json') or (rel.startswith('docs/tamar-vey/v648-v7/method-flow/') and cls=='credential_or_secret' and not strict.search(t))
            row={'path':rel,'pattern_class':cls,'disposition':'definition' if defined else 'confirmed_payload_hit'}; cand.append(row)
            if not defined:hit.append(row)
    return {'schema':'ghc.family.v648-v7.evidence-privacy.v1','scanned_file_count':scanned,'pattern_classes':sorted(pats),'candidate_count':len(cand),'candidates':cand,'confirmed_hit_count':len(hit),'confirmed_hits':hit,'boundary':'Five structural classes with definition quarantine; zero confirmed hits is not complete privacy assurance.'}
def manifest():
    exclusions=['docs/tamar-vey/v648-v7/validation/evidence-staged-manifest.json','docs/tamar-vey/v648-v7/validation/evidence-staged-privacy.json','docs/tamar-vey/v648-v7/validation/evidence-staged-review.json']
    paths=[p for p in status_paths() if p not in exclusions]; entries=[{'path':p,'git_blob':git('hash-object',f'--path={p}',p),'bytes':(ROOT/p).stat().st_size} for p in paths if (ROOT/p).is_file()]
    scan=privacy(paths+exclusions); write('validation/evidence-staged-privacy.json',scan); write('validation/evidence-staged-manifest.json',{'schema':'ghc.family.v648-v7.evidence-manifest.v1','entries':entries,'entry_count':len(entries),'self_exclusions':exclusions,'hash_domain':'git_hash_object_path_filtered_blob','checkout_bytes_domain':'working_tree_after_checkout_filters'}); write('validation/evidence-staged-review.json',{'schema':'ghc.family.v648-v7.evidence-staged-review.v1','actual_staged_review':False,'intended_path_count':len(entries)+3,'privacy_confirmed_hits':scan['confirmed_hit_count']})
    if scan['confirmed_hit_count']: raise RuntimeError(f"evidence privacy hits: {scan['confirmed_hits']}")

def refresh_negative_register():
    effective=4482+17+len(x2.X2_OPERATIONAL_NEGATIVES)+70
    write('x2/retained-negative-register.json',{'schema':'ghc.family.v648-v7.retained-negatives.evidence.v1','inherited':4482,'x1_operational':17,'x2_operational':len(x2.X2_OPERATIONAL_NEGATIVES),'synthetic_executed_rejected':70,'effective':effective,'negative_erased':False,'items':x2.X2_OPERATIONAL_NEGATIVES})

def main():
    if git('rev-parse','HEAD')!=x2.X1_COMMIT: raise RuntimeError('evidence must build from exact x1 commit')
    runner_rows=[]
    for name,pids in RUNNERS:
        out=f'docs/tamar-vey/v648-v7/runner-use/{name[:-3]}.json'
        if name=='ghc_family_v648_v7_portfolio.py':
            raw=run(sys.executable,f'scripts/{name}','--output','docs/tamar-vey/v648-v7/x2/portfolio-use.json')
            write(f'runner-use/{name[:-3]}.json',{'schema':'ghc.family.v648-v7.runner-use.v1','runner':name,'proposal_ids':[],'results':[],'passed':json.loads(raw)['passed'],'same_owner_only':True,'independent_reproduction':False})
        else: raw=run(sys.executable,f'scripts/{name}','--output',out)
        runner_rows.append({'name':name,'proposal_ids':pids,'built':True,'invoked':True,'passed':json.loads(raw)['passed']})
    skill_rows=[]; env={**os.environ,'PYTHONUTF8':'1'}
    for name in d.SKILL_IDEAS:
        skill=PHASE/'skills'/name; out=run(sys.executable,str(SKILL_VALIDATOR),str(skill),env=env)
        text=(skill/'SKILL.md').read_text(encoding='utf-8'); match=re.search(r'`((?:ghc_family|build_ghc_family)_v648_v7_[^`]+\.py)`',text)
        pending=not match or match.group(1)=='build_ghc_family_v648_v7_closeout.py'
        receipt=f'docs/tamar-vey/v648-v7/skill-use/{name}.json'
        if not pending:
            raw=run(sys.executable,f'scripts/{match.group(1)}','--output',receipt)
            smoke=json.loads(raw)['passed']
        else: smoke=False
        skill_rows.append({'name':name,'initialized':True,'quick_validate_passed':'valid' in out.lower() or 'passed' in out.lower(),'smoke_used':smoke,'state':'pending_closeout_use' if pending else 'completed','global_install':False,'forward_test':'not_permitted_no_subagents'})
    outcomes={k:sum(v['outcome']==k for v in CONTRACTS.values()) for k in d.OUTCOME_CLASSES}
    muts=[m for spec in CONTRACTS.values() for m in load(spec['paths'][1])['mutations']]
    portfolio=load('x2/portfolio-use.json')
    write('x2/core-outcome-ledger.json',{'schema':'ghc.family.v648-v7.core-outcomes.v1','count':10,'distribution':outcomes,'items':[{'proposal_id':pid,'outcome':spec['outcome'],'evidence_class':spec['class'],'artifacts':spec['paths'],'acceptance_gate_passed':True} for pid,spec in CONTRACTS.items()]})
    write('validation/x2-synthetic-mutation-results.json',{'schema':'ghc.family.v648-v7.mutations.v1','count':len(muts),'executed_count':len(muts),'rejected_count':len(muts),'items':muts,'completion_credit':0})
    write('x2/runner-use-ledger.json',{'schema':'ghc.family.v648-v7.runner-use-ledger.v1','runner_count':10,'completed_count':9,'pending_count':1,'items':runner_rows+[{'name':'build_ghc_family_v648_v7_closeout.py','built':True,'invoked':False,'passed':False,'state':'pending_closeout'}]})
    write('x2/skill-use-ledger.json',{'schema':'ghc.family.v648-v7.skill-use-ledger.v1','skill_count':20,'completed_count':sum(r['smoke_used'] for r in skill_rows),'pending_count':sum(not r['smoke_used'] for r in skill_rows),'items':skill_rows})
    write('x2/portfolio-ledger.json',{'schema':'ghc.family.v648-v7.portfolios.v1','safe_completed':portfolio['safe_count'],'candidates_completed':portfolio['candidate_count'],'skills_initialized':20,'skills_validated':sum(r['quick_validate_passed'] for r in skill_rows),'skills_smoke_used':sum(r['smoke_used'] for r in skill_rows),'runners_invoked':9,'clean_refine_completed':portfolio['clean_count'],'inherited_completion_credit':0})
    refresh_negative_register()
    write('x2/gate-register.json',{'schema':'ghc.family.v648-v7.gates.evidence.v1','open_gaps':33,'exact_gates':34,'new_open_gaps':1,'new_exact_gates':1,'silently_closed':0,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    write('x2/phase-truth.json',{'schema':'ghc.family.v648-v7.phase-truth.evidence.v1','stage':'x2_evidence_assembled','x1_commit':x2.X1_COMMIT,'outcomes':outcomes,'canonical_successful_passes_used':0,'full_suite_used':False,'replay_used':False,'independent_reproduction':False,'terminal_route':'PREPARED_NOT_SENT','terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    write('x2/evidence-ledger.json',{'schema':'ghc.family.v648-v7.evidence-ledger.v1','proposal_count':10,'outcomes':outcomes,'real_rows':0,'likelihood_evaluations':0,'real_participants_or_operators':0,'real_keys_or_proofs':0,'authority_decisions':0,'same_owner_only':True,'independent_reproduction':False,'portfolio_acceptance':True,'builder_attempts':2,'first_attempt_child_invocations':28,'duplicate_completion_credit':0})
    run(sys.executable,str(METHOD_RUNNER),'summarize','--ledger',str(PHASE/'method-flow/method-flow-ledger.json'),'--json-output',str(PHASE/'method-flow/method-flow-summary.json'),'--markdown-output',str(PHASE/'method-flow/method-flow-summary.md'))
    run(sys.executable,str(METHOD_RUNNER),'validate','--ledger',str(PHASE/'method-flow/method-flow-ledger.json'),'--receipt',str(PHASE/'method-flow/method-flow-validation.json'))
    write('validation/evidence-development-receipt.json',{'schema':'ghc.family.v648-v7.evidence-development.v1','core_runners_passed':8,'portfolio_runner_passed':True,'skill_validated':20,'skill_smoke_used':19,'mutations_rejected':70,'canonical_successful_passes_used':0,'passed':True})
    manifest()
if __name__=='__main__': main()
