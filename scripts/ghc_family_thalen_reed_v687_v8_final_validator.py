"""Exact owner final preparation and a phase-exclusive canonical latch."""
from __future__ import annotations
import argparse
import ast
import datetime
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='docs/thalen-reed/v687-v8/'
SOURCE='7e72086683731c40b4884ee7254c864891e354a9'
X1='8f9070f01e38fa5cc330cff247ea8e32541a0387'
EVIDENCE='522065f58a27abc8105092015927255cf7c77569'
BRANCH='codex/GHC-Family/thalen-reed-v687-v8-full-tools'
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_thalen_reed_v687_v8_x1_audit import strict, privacy, normalized
from ghc_family_thalen_reed_v687_v8_x2_audit import allowed, current_paths, semantic_checks

def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()
def formatted(d):return (json.dumps(d,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
def read(p):return strict((ROOT/p).read_text(encoding='utf-8'))
def write(p,d):(ROOT/p).write_bytes(formatted(d))

def blobs(anchor,paths):
    raw=subprocess.check_output(['git','-C',str(ROOT),'cat-file','--batch'],input=''.join(anchor+':'+p+'\n' for p in paths).encode())
    offset=0;result={}
    for path in paths:
        newline=raw.index(b'\n',offset);header=raw[offset:newline].decode().split();assert len(header)==3 and header[1]=='blob',(path,header)
        size=int(header[2]);result[path]=raw[newline+1:newline+1+size];offset=newline+size+2
    assert offset==len(raw)
    return result

def scan(items):
    jsons=0;asts=0;documents=0;largest=0;security=[]
    for path,raw in items.items():
        text=raw.decode('utf-8');words=len(text.split());largest=max(largest,words);assert words<=100000,path
        if path.endswith('.json'):strict(text);jsons+=1
        if path.endswith(('.md','.html','.txt')):documents+=1
        if path.endswith('.py'):
            tree=ast.parse(text,filename=path);asts+=1
            for n in ast.walk(tree):
                if isinstance(n,ast.Call):
                    if isinstance(n.func,ast.Name) and n.func.id in ['eval','exec']:security.append({'path':path,'line':n.lineno,'rule':'dynamic_code'})
                    if any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords):security.append({'path':path,'line':n.lineno,'rule':'shell_true'})
    report=privacy(items);assert report['confirmed_hits']==0,report;assert not security,security
    return {'strict_json':jsons,'python_ast':asts,'documents':documents,'largest_document_words':largest,'security_findings':security,'privacy':report}

def prepare():
    assert git('rev-parse','HEAD')==EVIDENCE
    assert not git('diff','--name-only',EVIDENCE),'Immutable evidence changed'
    prior=set(git('diff','--name-only',SOURCE,EVIDENCE).splitlines())
    assert len(prior)==338
    final=read(BASE+'final/phase-truth.json');assert final['state']=='FINAL_PREPARED_FOR_ONE_EXTERNAL_CANONICAL' and final['canonical_invocations']==0
    index=read(BASE+'final/baton-index.json');raw=(ROOT/index['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==index['sha256'] and len(raw.decode().split())==index['words'] and raw.decode().rstrip().endswith(index['eof'])
    assert 10000<=index['words']<=100000 and raw.decode().count('## Module ')==13
    assert (ROOT/BASE/'final/integrated-overview.html').read_text(encoding='utf-8').count('<section class="page">')==3
    validation=BASE+'validation/';mf=validation+'final-delta-manifest.json';owner_mf=validation+'final-owner-manifest.json';excluded=[mf,owner_mf]
    for name in ['final-checks.json','final-privacy.json','final-security.json','final-json.json','final-staged-review.json']:write(validation+name,{'state':'pending'})
    paths=sorted(set(current_paths())|set(excluded));new=sorted(set(paths)-prior);assert len(paths)<2000 and all(allowed(p) for p in paths)
    write(validation+'final-staged-review.json',{'schema':'ghc.family.staged-allowlist.v1','source':SOURCE,'parent':EVIDENCE,'allowed_paths':new,'allowed_change_kind':'A','path_count':len(new),'owner_path_count':len(paths),'deletions':0})
    write(validation+'final-checks.json',{'schema':'ghc.family.final-preparation.v1','source':SOURCE,'x1':X1,'evidence':EVIDENCE,'prior_paths_unchanged':338,'final_baton_words':index['words'],'final_baton_modules':13,'final_overview_pages':3,'canonical_invocations':0,'same_owner_only':True,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    items={p:normalized(ROOT/p) for p in paths if p not in excluded};checks=scan(items)
    write(validation+'final-privacy.json',checks['privacy'])
    write(validation+'final-security.json',{'schema':'ghc.family.final-bounded-security.v1','findings':checks['security_findings'],'python_ast':checks['python_ast'],'scope':'Every Python path in the current owner delta, with prior bounded manual code review and exact immutable evidence. No unchanged-history or sibling module execution.','exhaustive_security':False})
    write(validation+'final-json.json',{'schema':'ghc.family.final-strict-json.v1','strict_json_before_two_manifest_writes':checks['strict_json'],'duplicate_keys_rejected':True,'nonfinite_constants_rejected':True,'maximum_document_words':checks['largest_document_words'],'documents':checks['documents']})
    def manifest(selected):
        entries=[]
        for path in selected:
            if path not in excluded:
                raw=normalized(ROOT/path);entries.append({'path':path,'bytes_normalized_lf':len(raw),'sha256_normalized_lf':hashlib.sha256(raw).hexdigest()})
        return {'schema':'ghc.family.normalized-lf-manifest.v1','byte_domain':'normalized_lf_git_blob','anchor':'PENDING_FINAL_COMMIT','source':SOURCE,'entry_count':len(entries),'entries':entries,'declared_self_exclusions':excluded}
    write(mf,manifest(new));whole=manifest(paths);whole['owner_path_count']=len(paths);write(owner_mf,whole)
    print(json.dumps({'state':'FINAL_PREPARATION_PASS','new_files':len(new),'owner_files':len(paths),'final_delta_bindings':len(new)-2,'owner_bindings':len(paths)-2,'baton_words':index['words'],'confirmed_privacy_hits':0,'bounded_security_findings':0,'canonical_invocations':0}))

def verify_manifest(anchor,path,before):
    m=strict(blobs(anchor,[path])[path].decode());entries=m['entries'];exclusions=m['declared_self_exclusions'];listed=[e['path'] for e in entries]
    delta=set(git('diff','--name-only',before,anchor).splitlines())
    assert len(listed)==len(set(listed))==m['entry_count'] and len(exclusions)==len(set(exclusions))
    assert not set(listed)&set(exclusions) and set(listed)|set(exclusions)==delta,(path,'manifest coverage')
    values=blobs(anchor,listed)
    for entry in entries:
        raw=values[entry['path']].replace(b'\r\n',b'\n').replace(b'\r',b'\n')
        assert len(raw)==entry['bytes_normalized_lf'] and hashlib.sha256(raw).hexdigest()==entry['sha256_normalized_lf'],entry['path']
    return {'manifest':path,'anchor':anchor,'entries':len(entries),'exclusions':exclusions,'mismatches':[]}

def canonical(args,head):
    checks=[]
    assert git('branch','--show-current')==BRANCH;checks.append('owner_branch')
    chain=[row.split() for row in git('rev-list','--parents','--reverse',SOURCE+'..'+head).splitlines()]
    assert chain==[[X1,SOURCE],[EVIDENCE,X1],[head,EVIDENCE]];checks.append('three_direct_single_parent_commits')
    assert not git('rev-list','--merges',SOURCE+'..'+head);checks.append('zero_merges')
    assert git('rev-list','--parents','-1',head).split()==[head,EVIDENCE];checks.append('one_final_parent')
    assert not git('status','--porcelain=v1');checks.append('clean_before')
    delta=[line.split('\t',1) for line in git('diff','--name-status',SOURCE,head).splitlines()]
    assert all(kind=='A' and allowed(path) for kind,path in delta);paths=[p for _,p in delta]
    assert len(paths)==len(set(paths)) and len(paths)<2000;checks.append('every_delta_path_allowed_addition')
    items=blobs(head,paths);policy=strict(items[BASE+'final/canonical-policy.json'].decode())
    assert policy['source']==SOURCE and policy['x1']==X1 and policy['evidence']==EVIDENCE and policy['expected_tests']==28;checks.append('frozen_canonical_policy')
    specs=[(X1,BASE+'validation/x1-manifest.json',SOURCE),(EVIDENCE,BASE+'validation/x2-manifest.json',X1),(head,BASE+'validation/final-delta-manifest.json',EVIDENCE),(head,BASE+'validation/final-owner-manifest.json',SOURCE)]
    manifests=[verify_manifest(*spec) for spec in specs];checks.append('four_lifecycle_manifests_and_exclusions')
    for anchor,before in [(X1,SOURCE),(EVIDENCE,X1)]:
        prior=git('diff','--name-only',before,anchor).splitlines();old=blobs(anchor,prior)
        assert all(items[p]==old[p] for p in prior)
    checks.append('immutable_x1_and_evidence')
    scanned=scan(items);checks.extend(['strict_json','all_document_caps','five_class_privacy_adjudication','bounded_changed_code_security'])
    evidence=semantic_checks();assert all(evidence.values());checks.append('sixteen_evidence_structure_checks')
    modpath=ROOT/policy['test_module'];spec=importlib.util.spec_from_file_location('thalen_exact_final_pcm_tests',modpath);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    suite=unittest.defaultTestLoader.loadTestsFromModule(module);count=suite.countTestCases();assert count==28
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    assert result.wasSuccessful(),stream.getvalue();checks.append('twenty_eight_owner_tests')
    index=strict(items[BASE+'final/baton-index.json'].decode());baton=items[index['path']]
    assert len(baton)==index['bytes'] and hashlib.sha256(baton).hexdigest()==index['sha256'] and len(baton.decode().split())==index['words']
    assert 10000<=index['words']<=100000 and baton.decode().count('## Module ')==13 and baton.decode().rstrip().endswith(index['eof']);checks.append('baton_digest_words_modules_eof')
    assert items[BASE+'final/integrated-overview.html'].decode().count('<section class="page">')==3;checks.append('three_final_overview_pages')
    promotion=strict(items[BASE+'x2/promotion-receipt.json'].decode());assert len(promotion['members'])==56
    for row in promotion['members']:
        src=items[row['source']];dest=args.skill_root/row['name']/row['relative'] if row['kind']=='skill' else args.runner_root/row['relative']
        assert src==dest.read_bytes() and hashlib.sha256(src).hexdigest()==row['sha256']
    for name in {r['name'] for r in promotion['members'] if r['kind']=='skill'}:
        expected={r['relative'] for r in promotion['members'] if r['kind']=='skill' and r['name']==name};actual={p.relative_to(args.skill_root/name).as_posix() for p in (args.skill_root/name).rglob('*') if p.is_file()};assert actual==expected
    assert {p.name for p in args.runner_root.iterdir() if p.is_file()}=={r['relative'] for r in promotion['members'] if r['kind']=='runner'};checks.append('fifty_six_global_parity_files')
    observed=json.loads(subprocess.check_output([str(args.environment_python),'-X','utf8','-c','import importlib.metadata as m,json;print(json.dumps({d.metadata["Name"]:d.version for d in m.distributions()},sort_keys=True))'],text=True,encoding='utf-8'))
    expected=strict(items[BASE+'x2/environment-receipt.json'].decode())['all_packages'];assert {k.lower().replace('_','-'):v for k,v in observed.items()}=={k.lower().replace('_','-'):v for k,v in expected.items()};checks.append('seven_pinned_environment_distributions')
    final=strict(items[BASE+'final/phase-truth.json'].decode());assert final['outcomes']=={'completed':160,'represented':14,'open_gap':8,'exact_gate':18} and final['terminal_verdict']=='NOT_READY_FOR_STAGE_20';checks.append('outcome_and_authority_boundaries')
    up=git('rev-parse','@{upstream}');track=git('rev-parse','refs/remotes/origin/'+BRANCH);live=git('ls-remote','--heads','origin','refs/heads/'+BRANCH).split()[0];div=[int(v) for v in git('rev-list','--left-right','--count','HEAD...@{upstream}').split()]
    assert head==up==track==live and div==[0,0];checks.extend(['fresh_four_way_equality','typed_zero_divergence'])
    assert not git('status','--porcelain=v1');checks.append('clean_after')
    return {'status':'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL','owner':'Thalen Reed','phase':'v687-v8','source':SOURCE,'x1':X1,'evidence':EVIDENCE,'exact_final':head,'branch':BRANCH,
        'canonical_invocation_count':1,'canonical_success_count':1,'canonical_replay_count':0,'checks':checks,'detailed_checks':len(checks),'selected_tests':count,'excluded_tests':[],
        'owner_files':len(paths),'manifest_bindings':sum(m['entries'] for m in manifests),'manifest_exclusions':sum(len(m['exclusions']) for m in manifests),'manifests':manifests,
        'strict_json_documents':scanned['strict_json'],'python_ast_checks':scanned['python_ast'],'document_checks':scanned['documents'],'largest_document_words':scanned['largest_document_words'],
        'confirmed_privacy_hits':0,'bounded_security_findings':0,'global_parity_files':56,'environment_distributions':7,'baton':index,'outcomes':final['outcomes'],'effective_counts':final['effective_counts'],
        'test_log_sha256':hashlib.sha256(stream.getvalue().encode()).hexdigest(),'remote':{'local':head,'upstream':up,'tracking':track,'fresh_live':live,'divergence':div,'clean':True},
        'phase_commits':3,'merge_commits':0,'final_parent':EVIDENCE,'same_owner_only':True,'full_repository_suite':False,'independent_reproduction':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20','route_state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED'}

def main():
    ap=argparse.ArgumentParser();mode=ap.add_mutually_exclusive_group(required=True);mode.add_argument('--prepare',action='store_true');mode.add_argument('--canonical',action='store_true')
    ap.add_argument('--receipt-root',type=Path);ap.add_argument('--skill-root',type=Path);ap.add_argument('--runner-root',type=Path);ap.add_argument('--environment-python',type=Path);a=ap.parse_args()
    if a.prepare:prepare();return
    assert all([a.receipt_root,a.skill_root,a.runner_root,a.environment_python])
    receipt_root=a.receipt_root.resolve();assert receipt_root.drive.upper()=='D:' and not receipt_root.is_relative_to(ROOT)
    receipt_root.mkdir(parents=True,exist_ok=True);head=git('rev-parse','HEAD');marker=receipt_root/'thalen-v687-v8.canonical-invocation.json';receipt=receipt_root/('thalen-v687-v8-'+head+'.json')
    assert not marker.exists() and not receipt.exists(),'Canonical invocation already exists; replay refused'
    fd=os.open(marker,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    with os.fdopen(fd,'wb') as f:f.write(formatted({'state':'CANONICAL_INVOKED_ONCE','owner':'Thalen Reed','phase':'v687-v8','exact_final':head,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
    try:
        payload=canonical(a,head);wrapped={'payload':payload,'payload_sha256':hashlib.sha256(formatted(payload)).hexdigest()}
        with receipt.open('xb') as f:f.write(formatted(wrapped))
        print(json.dumps({'status':payload['status'],'exact_final':head,'selected_tests':payload['selected_tests'],'detailed_checks':payload['detailed_checks'],'owner_files':payload['owner_files'],'manifest_bindings':payload['manifest_bindings'],'manifest_exclusions':payload['manifest_exclusions'],'payload_sha256':wrapped['payload_sha256'],'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'receipt':receipt.name}))
    except Exception as exc:
        failed=receipt_root/('thalen-v687-v8-'+head+'.failed.json')
        with failed.open('xb') as f:f.write(formatted({'status':'FAILED_ZERO_CANONICAL_SUCCESS_CREDIT','exact_final':head,'error_type':type(exc).__name__,'error':str(exc)}))
        raise

if __name__=='__main__':main()
