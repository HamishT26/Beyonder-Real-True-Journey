#!/usr/bin/env python3
"""Ingest one external canonical result and build exact incremental seal receipts without rerunning it."""

import argparse, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHASE=ROOT/'docs/tamar-vey/v648-v7'; sys.path.insert(0,str(ROOT/'scripts'))
from build_ghc_family_v648_v7_evidence import git, status_paths, write
import ghc_family_v648_v7_x2_state as x2
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--external-output',type=Path,required=True); args=ap.parse_args(); result=json.loads(args.external_output.read_text(encoding='utf-8'))
    if not result.get('passed'): raise RuntimeError('canonical result did not pass')
    write('validation/canonical-validation.json',{**result,'imported_from_external_d_first_receipt':True,'external_path_persisted':False})
    write('phase-truth-final.json',{'schema':'ghc.family.v648-v7.phase-truth.final.v1','outcomes':{'completed':6,'represented':2,'open_gap':1,'exact_gate':1},'canonical_successful_passes_used':1,'full_suite_used':False,'replay_used':False,'same_owner_only':True,'independent_reproduction':False,'terminal_route':'PREPARED_NOT_SENT','terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    write('validation/final-validation-record.json',{'schema':'ghc.family.v648-v7.final-validation-record.v1','canonical_candidate':result,'failed_postpass_attempts':1,'postpass_tests_rerun':False,'postpass_canonical_privacy_rerun':False,'incremental_files_only':True,'exact_final_head':'VERIFIED_EXTERNALLY_AFTER_COMMIT','same_owner_only':True,'terminal_route':'PREPARED_NOT_SENT'})
    inherited=load('retained-negative-register-final.json')
    write('retained-negative-register-final.json',{**inherited,'x2_operational':len(x2.X2_OPERATIONAL_NEGATIVES),'effective':4482+17+len(x2.X2_OPERATIONAL_NEGATIVES)+70,'items':x2.X2_OPERATIONAL_NEGATIVES,'terminal_route':'PREPARED_NOT_SENT'})
    exclusions=['docs/tamar-vey/v648-v7/validation/final-staged-manifest.json','docs/tamar-vey/v648-v7/validation/final-staged-privacy.json','docs/tamar-vey/v648-v7/validation/final-staged-review.json']
    paths=[p for p in status_paths() if p not in exclusions]; entries=[{'path':p,'git_blob':git('hash-object',f'--path={p}',p),'bytes':(ROOT/p).stat().st_size} for p in paths if (ROOT/p).is_file()]
    incremental=['docs/tamar-vey/v648-v7/validation/canonical-validation.json','docs/tamar-vey/v648-v7/validation/final-validation-record.json','docs/tamar-vey/v648-v7/phase-truth-final.json','docs/tamar-vey/v648-v7/method-flow/v6487-m12-wpass-x2-02-witness.json','docs/tamar-vey/v648-v7/method-flow/method-flow-ledger.json','docs/tamar-vey/v648-v7/method-flow/method-flow-summary.json','docs/tamar-vey/v648-v7/method-flow/method-flow-summary.md','docs/tamar-vey/v648-v7/method-flow/method-flow-validation.json']; pats=[re.compile(r'(?i)(source_thread_id|thread_id)\s*[:=]'),re.compile(r'(?i)[A-Z]:\\Users\\'),re.compile(r'(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})'),re.compile(r'(?i)(private_route|callable_identifier|browser_send_submitted_response_active)'),re.compile(r'(?i)(session_stream|raw_transcript|conversation_export)')]; hits=[]
    for rel in ['docs/tamar-vey/v648-v7/method-flow/v6487-m03-wpass-x2-03-witness.json']:
        if rel not in incremental:
            incremental.append(rel)
    for rel in ['scripts/build_ghc_family_v648_v7_postpass.py','scripts/ghc_family_v648_v7_x2_state.py','tests/test_ghc_family_v648_v7_closeout.py','docs/tamar-vey/v648-v7/retained-negative-register-final.json','docs/tamar-vey/v648-v7/method-flow/v6487-m09-wfail-x2-01-witness.json']:
        if rel not in incremental:
            incremental.append(rel)
    for rel in ['docs/tamar-vey/v648-v7/method-flow/v6487-m09-wpass-x2-01-witness.json']:
        if rel not in incremental:
            incremental.append(rel)
    strict_secret=re.compile(r'(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"\'][^\"\']{6,}[\"\']|bearer\s+[A-Za-z0-9._-]{12,}')
    for rel in incremental:
        t=(ROOT/rel).read_text(encoding='utf-8')
        for i,p in enumerate(pats):
            if not p.search(t):
                continue
            defined=rel=='scripts/build_ghc_family_v648_v7_postpass.py' or (i==2 and rel.startswith('docs/tamar-vey/v648-v7/method-flow/') and not strict_secret.search(t))
            if not defined:
                hits.append({'path':rel,'class_index':i})
    if hits: raise RuntimeError(f'incremental privacy hits: {hits}')
    candidate=load('validation/final-staged-privacy.json'); write('validation/final-staged-privacy.json',{**candidate,'schema':'ghc.family.v648-v7.final-privacy.sealed.v1','canonical_candidate_scanned_files':result['privacy_scanned_files'],'canonical_candidate_confirmed_hits':0,'postpass_incremental_scanned_files':len(incremental),'postpass_incremental_confirmed_hits':0,'canonical_scan_rerun':False})
    write('validation/final-staged-manifest.json',{'schema':'ghc.family.v648-v7.final-manifest.sealed.v1','entries':entries,'entry_count':len(entries),'self_exclusions':exclusions,'hash_domain':'git_hash_object_path_filtered_blob','checkout_bytes_domain':'working_tree_after_checkout_filters','canonical_candidate_tree':result['candidate_staged_tree'],'postpass_incremental_files':incremental})
    write('validation/final-staged-review.json',{'schema':'ghc.family.v648-v7.final-staged-review.sealed.v1','actual_staged_review':False,'intended_path_count':len(entries)+3,'postpass_incremental':True,'tests_rerun':False,'canonical_privacy_rerun':False})
if __name__=='__main__': main()
