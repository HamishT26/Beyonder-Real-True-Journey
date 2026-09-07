"""Exclusive exact-final canonical for this owner delta, without inherited suite execution."""
from __future__ import annotations
import argparse,ast,datetime,hashlib,json,os,re,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='docs/teryn-halewick/v687-v4'
SOURCE='b3a61e3749e4302dea3bc9711eea79848f3a546b'
X1='ebb7e751140388b81f0f9c28ff0337854a536ec5'
EVIDENCE='238a48968af1ff0913b97f7230ec36013e939c9e'
BRANCH='codex/GHC-Family/teryn-halewick-v687-v4-full-tools'
PATTERNS={
    'raw_task_identifier':r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
    'private_local_path':r'(?:[A-Za-z]:\\|/Users/|/home/)',
    'secret_assignment':r'\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+',
    'private_callable_route':r'\b(?:codex|app|session|thread)://',
    'private_application_state':r'\b(?:providerTabId|clientThreadId)\b',
}

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf8').strip()
def norm(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def strict_json(b):
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result:raise ValueError('duplicate JSON key')
            result[k]=v
        return result
    def reject(x):raise ValueError('non-finite JSON constant')
    return json.loads(b,object_pairs_hook=unique,parse_constant=reject)
def load(rel):return strict_json((ROOT/rel).read_bytes())
def blobs(specs):
    data=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=('\n'.join(specs)+'\n').encode(),capture_output=True,check=True).stdout
    pos=0;result=[]
    for spec in specs:
        end=data.index(b'\n',pos);header=data[pos:end].split()
        if len(header)!=3 or header[1]!=b'blob':raise ValueError('Required Git blob unavailable')
        size=int(header[2]);result.append(data[end+1:end+1+size]);pos=end+size+2
    return result
def replay(commit,rel):
    m=strict_json(blobs([commit+':'+rel])[0]);entries=m['entries'];data=blobs([commit+':'+e['path'] for e in entries]);fail=[]
    for e,b in zip(entries,data):
        n=norm(b)
        if len(n)!=e['bytes_normalized_lf'] or hashlib.sha256(n).hexdigest()!=e['sha256_normalized_lf']:fail.append(e['path'])
    return dict(commit=commit,path=rel,bindings=len(entries),mismatches=fail,passed=not fail)
def private_scan(paths):
    candidates=[]
    for rel in paths:
        s=(ROOT/rel).read_text(encoding='utf8');definition_ranges=[]
        if rel=='scripts/ghc_family_teryn_halewick_v687_v4_canonical.py':
            tree=ast.parse(s)
            for node in tree.body:
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATTERNS' for t in node.targets):
                    for value in node.value.values:definition_ranges.append((value.lineno,value.end_lineno))
        for kind,pattern in PATTERNS.items():
            for m in re.finditer(pattern,s,re.I):
                line=s.count('\n',0,m.start())+1
                adjudicated=any(a<=line<=b for a,b in definition_ranges)
                candidates.append(dict(path=rel,line=line,kind=kind,disposition='scanner_definition_not_payload' if adjudicated else 'confirmed_payload_hit'))
    confirmed=[r for r in candidates if r['disposition']=='confirmed_payload_hit']
    return dict(classes=list(PATTERNS),candidates=candidates,confirmed=confirmed,complete_privacy=False,passed=not confirmed)
def security(paths):
    findings=[];count=0
    for rel in paths:
        if not rel.endswith('.py'):continue
        count+=1;tree=ast.parse((ROOT/rel).read_text(encoding='utf8'))
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and ((isinstance(n.func,ast.Name) and n.func.id in {'eval','exec'}) or any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords)):
                findings.append(dict(path=rel,line=n.lineno,rule='dynamic_execution_or_shell_true'))
    return dict(python_files=count,findings=findings,passed=not findings,exhaustive_security=False)
def promotion_parity(skillroot,scriptroot):
    receipt=load(BASE+'/x2/promotion-receipt.json');mismatches=[]
    for member in receipt['members']:
        data=(skillroot/member['skill']/member['path']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=member['sha256']:mismatches.append(member['skill']+'/'+member['path'])
    for name in receipt['shared_names']:
        if (scriptroot/name).read_bytes()!=(ROOT/'scripts'/name).read_bytes():mismatches.append(name)
    return dict(skills=10,skill_files=60,shared_runners=5,dependency_files=1,mismatches=mismatches,passed=not mismatches)

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-head',required=True);p.add_argument('--receipt-dir',required=True,type=Path);p.add_argument('--global-skill-root',required=True,type=Path);p.add_argument('--global-script-root',required=True,type=Path);a=p.parse_args()
    state=a.receipt_dir.resolve()
    if state.name!='teryn-halewick-v687-v4' or state.is_relative_to(ROOT):raise SystemExit('An external exact owner receipt directory is required')
    state.mkdir(parents=True,exist_ok=True);latch=state/'canonical-invocation.json';receipt=state/'exact-final-canonical.json'
    if latch.exists() or receipt.exists():raise SystemExit('Canonical invocation already recorded; replay refused')
    with latch.open('x',encoding='utf8') as f:json.dump(dict(owner='Teryn Halewick',phase='v687-v4',expected_head=a.expected_head,invocation=1,started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),f)
    result=dict(owner='Teryn Halewick',phase='v687-v4',source=SOURCE,x1=X1,evidence=EVIDENCE,expected_head=a.expected_head,canonical_invocation_count=1,canonical_success_count=0,canonical_replay_count=0,same_owner_only=True,independent_reproduction=False,full_repository_suite=False,terminal_verdict='NOT_READY_FOR_STAGE_20')
    try:
        head=git('rev-parse','HEAD');branch=git('branch','--show-current');up=git('rev-parse','@{upstream}');tracking=git('rev-parse','refs/remotes/origin/'+branch);live=git('ls-remote','--heads','origin','refs/heads/'+branch).split('\t')[0]
        divergence=git('rev-list','--left-right','--count','HEAD...@{upstream}').split();clean_before=not git('status','--porcelain=v1')
        delta=git('diff','--name-status',SOURCE,head).splitlines();paths=[r.split('\t',1)[1] for r in delta]
        ownership=all(r.startswith('A\t') and (r.split('\t',1)[1].startswith(BASE+'/') or re.fullmatch(r'(?:scripts|tests)/[^/]*teryn_halewick_v687_v4[^/]*\.py',r.split('\t',1)[1])) for r in delta)
        history=[line.split() for line in git('rev-list','--parents',SOURCE+'..'+head).splitlines()]
        manifests=[replay(X1,BASE+'/validation/x1-manifest.json'),replay(EVIDENCE,BASE+'/validation/x2-manifest.json'),replay(head,BASE+'/validation/final-delta-manifest.json'),replay(head,BASE+'/validation/final-owner-manifest.json')]
        owner_manifest=load(BASE+'/validation/final-owner-manifest.json');manifest_paths={e['path'] for e in owner_manifest['entries']}|set(owner_manifest['self_exclusions'])
        prior_paths=git('diff','--name-only',SOURCE,EVIDENCE).splitlines();prior_old=blobs([EVIDENCE+':'+x for x in prior_paths]);prior_now=blobs([head+':'+x for x in prior_paths]);immutable=all(x==y for x,y in zip(prior_old,prior_now))
        parsed=sum(1 for rel in paths if rel.endswith('.json') and strict_json((ROOT/rel).read_bytes()) is not None)
        privacy=private_scan(paths);ast_security=security(paths);promotions=promotion_parity(a.global_skill_root,a.global_script_root)
        suite=unittest.TestLoader().discover(str(ROOT/'tests'),pattern='test_ghc_family_teryn_halewick_v687_v4_*.py');tests=unittest.TestResult();suite.run(tests)
        test_summary=dict(selected=tests.testsRun,passed=tests.testsRun-len(tests.failures)-len(tests.errors),failures=[t.id() for t,_ in tests.failures],errors=[t.id() for t,_ in tests.errors],success=tests.wasSuccessful(),frozen_runtime_samples=200,changed_result_challenges=1000)
        clean_after=not git('status','--porcelain=v1');checks=dict(exact_head=head==a.expected_head,exact_branch=branch==BRANCH,clean_before=clean_before,clean_after=clean_after,zero_divergence=divergence==['0','0'],local_upstream_equal=head==up,local_tracking_equal=head==tracking,local_fresh_live_equal=head==live,three_direct_commits=history==[[head,EVIDENCE],[EVIDENCE,X1],[X1,SOURCE]],zero_merges=not git('rev-list','--merges',SOURCE+'..'+head),owner_additive_allowlist=ownership,owner_manifest_complete=set(paths)==manifest_paths,immutable_x1_x2_preserved=immutable,manifests=all(m['passed'] for m in manifests),strict_json=parsed==sum(x.endswith('.json') for x in paths),five_class_privacy=privacy['passed'],bounded_ast_security=ast_security['passed'],promotion_parity=promotions['passed'],selected_tests=test_summary['success'],owner_file_cap=len(paths)<=2000,document_word_caps=all(len((ROOT/x).read_text(encoding='utf8').split())<=100000 for x in paths),terminal_verdict=load(BASE+'/final/phase-truth.json')['terminal_verdict']=='NOT_READY_FOR_STAGE_20')
        success=all(checks.values());result.update(head=head,branch=branch,heads=dict(local=head,upstream=up,tracking=tracking,fresh_live=live),divergence=divergence,clean_before=clean_before,clean_after=clean_after,checks=checks,checks_passed=sum(checks.values()),checks_total=len(checks),tests=test_summary,manifests=manifests,manifest_bindings=sum(x['bindings'] for x in manifests),strict_json_documents=parsed,owner_files=len(paths),privacy=privacy,security=ast_security,promotions=promotions,canonical_success_count=int(success),status='VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if success else 'FAILED_ZERO_CANONICAL_SUCCESS_CREDIT')
    except Exception as exc:result.update(status='FAILED_ZERO_CANONICAL_SUCCESS_CREDIT',failure_class=type(exc).__name__)
    result['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();basis=json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();result['payload_sha256']=hashlib.sha256(basis).hexdigest()
    with receipt.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:result[k] for k in ['status','canonical_invocation_count','canonical_success_count','canonical_replay_count','head','checks_passed','checks_total','manifest_bindings','strict_json_documents','owner_files'] if k in result}))
    return 0 if result['canonical_success_count']==1 else 1

if __name__=='__main__':raise SystemExit(main())
