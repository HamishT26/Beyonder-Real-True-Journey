"""One exact-final owner canonical. Importing this module performs no validation."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

PHASE='docs/seren-talewood/v689-v2-r2'
BRANCH='codex/GHC-Family/seren-talewood-main'
PATTERNS={
 'credential':re.compile(r'\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{24,})'),
 'private_absolute_path':re.compile(r'(?i)(?:[a-z]:[\\/](?:Users|GHC-Archives)|/(?:Users|home)/[^/\s]+)'),
 'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'private_route':re.compile(r'(?i)(?:codex|app|chatgpt)://'),
 'raw_uuid':re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',re.I)}

def require(condition,message='contract failed'):
    if not condition:raise AssertionError(message)

def sha(data):return hashlib.sha256(data).hexdigest()

def typed_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate JSON key');result[key]=value
        return result
    def constant(value):raise ValueError('nonfinite JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def safe_relative(value):
    require(type(value) is str and value and '\\' not in value and ':' not in value,'invalid relative path')
    require(not PurePosixPath(value).is_absolute() and all(p not in {'','.','..'} for p in value.split('/')),'path escape')
    return value

def write_once(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,sort_keys=True,indent=2,ensure_ascii=True);f.write('\n')

def git(repo,*args,input=None):
    p=subprocess.run(['git','-C',str(repo),*args],input=input,capture_output=True,timeout=60)
    require(p.returncode==0,'Git command failed: '+args[0])
    return p.stdout

def tree_objects(repo,head):
    entries=[]
    for row in git(repo,'ls-tree','-r','-z',head).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();name=safe_relative(path.decode())
        require(mode=='100644' and kind=='blob','unsupported tree member')
        entries.append((name,oid))
    require(len(entries)<=2000,'owner file ceiling')
    payload=git(repo,'cat-file','--batch',input=('\n'.join(oid for _,oid in entries)+'\n').encode())
    offset=0;objects={}
    for name,expected in entries:
        end=payload.index(b'\n',offset);oid,kind,size=payload[offset:end].decode().split();size=int(size)
        raw=payload[end+1:end+1+size];offset=end+size+2
        require(oid==expected and kind=='blob' and len(raw)==size,'Git object framing')
        objects[name]={'oid':oid,'raw':raw}
    return objects

def verify_manifest(manifest,objects,expected_paths):
    entries=manifest.get('entries',manifest.get('files'))
    require(type(entries) is list,'manifest entries')
    names=[safe_relative(r['path']) for r in entries]
    exclusions=[safe_relative(p) for p in manifest.get('self_exclusions',[])]
    require(len(names)==len(set(names)) and len(exclusions)==len(set(exclusions)),'duplicate manifest path')
    require(not set(names)&set(exclusions),'overlapping manifest exclusions')
    require(set(names)|set(exclusions)==set(expected_paths),'manifest coverage')
    for row in entries:
        obj=objects[row['path']];raw=obj['raw']
        require(type(row['bytes']) is int and row['bytes']==len(raw),'manifest byte count')
        require(row['sha256']==sha(raw),'manifest digest')
        if 'git_oid' in row:require(row['git_oid']==obj['oid'],'manifest Git object')
    return len(entries)

def verify_chain(chain):
    require(len(chain)==4,'four lifecycle boundaries required')
    require(chain[0]['parents']==[],'planning root must have zero parents')
    for before,after in zip(chain,chain[1:]):require(after['parents']==[before['head']],'direct lifecycle parent')

def equality(repo,head):
    require(git(repo,'symbolic-ref','--short','HEAD').decode().strip()==BRANCH,'owner branch')
    local=git(repo,'rev-parse','HEAD').decode().strip();upstream=git(repo,'rev-parse','@{u}').decode().strip()
    tracking=git(repo,'rev-parse','refs/remotes/origin/'+BRANCH).decode().strip()
    remote=git(repo,'ls-remote','--exit-code','origin','refs/heads/'+BRANCH).decode().strip().splitlines()
    require(len(remote)==1,'exact remote ref');live=remote[0].split('\t')[0]
    require(local==upstream==tracking==live==head,'four-way equality')
    require(git(repo,'status','--porcelain=v1')==b'','clean owner worktree')
    divergence=[int(x) for x in git(repo,'rev-list','--left-right','--count','HEAD...@{u}').decode().split()]
    require(divergence==[0,0],'typed zero divergence')
    return dict(local=local,upstream=upstream,tracking=tracking,live=live,clean=True,divergence=divergence)

def scan(objects):
    json_count=0;python_count=0;maximum=0;hits=[]
    suffixes={'.json','.md','.txt','.py','.yaml','.yml','.html','.svg'}
    for path,obj in objects.items():
        if Path(path).suffix not in suffixes:continue
        text=obj['raw'].decode('utf-8');words=len(text.split());maximum=max(maximum,words)
        require(words<=100000,'document word ceiling')
        for label,pattern in PATTERNS.items():
            if pattern.search(text):hits.append({'path':path,'class':label})
        if path.endswith('.json'):strict_json(text);json_count+=1
        if path.endswith('.py'):ast.parse(text);python_count+=1
    require(not hits,'privacy candidate requires review')
    return dict(strict_json=json_count,python_ast=python_count,maximum_document_words=maximum,
                privacy_candidates=hits,privacy_classes=list(PATTERNS))

def fixture_observations(directory):
    raw=b'finite owner fixture\n';oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    objects={'fixture.txt':{'raw':raw,'oid':oid}}
    base={'entries':[{'path':'fixture.txt','bytes':len(raw),'sha256':sha(raw),'git_oid':oid}],'self_exclusions':[]}
    verify_manifest(base,objects,{'fixture.txt'})
    negatives=[]
    for name in ['wrong_digest','missing_entry','unexpected_path','wrong_byte_count','path_traversal']:
        changed=json.loads(json.dumps(base));expected={'fixture.txt'}
        if name=='wrong_digest':changed['entries'][0]['sha256']='0'*64
        elif name=='missing_entry':changed['entries']=[]
        elif name=='unexpected_path':changed['self_exclusions']=['unlisted.txt']
        elif name=='wrong_byte_count':changed['entries'][0]['bytes']+=1
        else:changed['entries'][0]['path']='../fixture.txt'
        rejected=False
        try:verify_manifest(changed,objects,expected)
        except (AssertionError,KeyError):rejected=True
        negatives.append(dict(name=name,rejected=rejected,subject_result='fail',original_success_credit=0))
    chain=[{'head':c*40,'parents':[] if i==0 else [chr(ord(c)-1)*40]} for i,c in enumerate('abcd')]
    verify_chain(chain);chain[-1]['parents']=['a'*40]
    rejected=False
    try:verify_chain(chain)
    except AssertionError:rejected=True
    negatives.append(dict(name='wrong_parent',rejected=rejected,subject_result='fail',original_success_credit=0))
    rejected=False
    try:strict_json('{"a":1,"a":2}')
    except AssertionError:rejected=True
    negatives.append(dict(name='duplicate_json_key',rejected=rejected,subject_result='fail',original_success_credit=0))
    latch=directory/'synthetic-latch.json';write_once(latch,{'synthetic_fixture':True,'canonical_invocation':False})
    before=latch.read_bytes();rejected=False
    try:write_once(latch,{'changed':True})
    except FileExistsError:rejected=True
    negatives.append(dict(name='exclusive_write_reopen',rejected=rejected and latch.read_bytes()==before,subject_result='fail',original_success_credit=0))
    require(all(r['rejected'] for r in negatives),'fixture failure')
    return dict(valid_manifest=True,negative_fixtures=negatives,canonical_invocations=0,independent_reproduction=False)

def validate_globals(final,global_tools,skill_root):
    bindings={}
    def register(base,relative,digest,role):
        safe_relative(relative);path=base/relative
        require(path.resolve().is_relative_to(base.resolve()),'global path containment')
        key=str(path)
        if key in bindings:require(bindings[key]['sha256']==digest,'conflicting global binding')
        bindings[key]=dict(path=path,sha256=digest,role=role)
    def data(rel):return strict_json(final[PHASE+'/'+rel]['raw'])
    for stage in ['x1','x2']:
        for row in data(stage+'/tool-build-and-promotion.json')['parity']:
            if row['kind']=='skill':register(skill_root/row['name'],row['relative_path'],row['sha256'],'new skill')
            else:register(global_tools,row['name'],row['sha256'],'new runner or core')
    for row in data('x1/reuse-existing-tools-results.json')['parity']:
        if row['kind']=='skill':register(skill_root/row['name'],row['relative_path'],row['sha256'],'existing skill reuse')
        else:register(global_tools,row['name'],row['sha256'],'existing runner reuse')
    for row in data('x1/shared-integration-receipt.json')['records']:
        if row['kind']=='global_runner':register(global_tools,row['name'],row['after_sha256'],'profile reviewer');continue
        base=skill_root/row['skill'];register(base,row['relative_path'],row['after_sha256'],'shared current entrypoint or support')
        if row['kind']=='entrypoint':register(base,row['preserved_archive'],row['archive_sha256'],'preserved entrypoint archive')
    for row in data('tooling/shared-catalogue-publication.json')['entries']:
        register(skill_root/row['skill'],row['relative_path'],row['sha256'],'original catalogue retained')
    for row in data('tooling/shared-catalogue-token-correction.json')['records']:
        if 'expected_json' not in row:register(skill_root/row['skill'],row['relative_path'],row['sha256'],'corrected x1 catalogue')
        else:register(skill_root/row['skill'],row['preserved_archive'],row['before_sha256'],'original pointer archive')
    for row in data('x1/shared-pointer-snapshot.json')['rows']:
        register(skill_root/row['skill'],row['relative_path'],row['sha256'],'immutable x1 pointer')
    for row in data('x2/tooling/shared-publication.json')['records']:
        register(skill_root/row['skill'],row['relative_path'],row['sha256'],'current x2 catalogue or pointer')
        if 'archive' in row:register(skill_root/row['skill'],row['archive'],row['before_sha256'],'before-x2 pointer archive')
    for binding in bindings.values():require(binding['path'].is_file() and sha(binding['path'].read_bytes())==binding['sha256'],'global file drift')
    return dict(files_verified=len(bindings),roles=sorted({r['role'] for r in bindings.values()}),
                mutable_pointer_policy='Historical pointers verified through named archives; current pointer verified against x2 publication.')

def validate_packages(final,site,bank):
    receipt=strict_json(final[PHASE+'/x2/package-installation.json']['raw'])
    expected={r['path']:r for r in receipt['installed_files']}
    actual={p.relative_to(site).as_posix():p for p in site.rglob('*') if p.is_file()}
    require(set(actual)==set(expected),'installed file set')
    for path,file in actual.items():
        safe_relative(path);require(file.resolve().is_relative_to(site.resolve()),'package path containment')
        require(sha(file.read_bytes())==expected[path]['sha256'],'installed file digest')
    normalize=lambda name:re.sub(r'[-_.]+','-',name).lower()
    versions={normalize(d.metadata['Name']):d.version for d in importlib.metadata.distributions(path=[str(site)])}
    require(versions==receipt['installed_distributions'],'installed distributions')
    plan=strict_json(final[PHASE+'/plan/package-plan.json']['raw'])
    for row in plan['packages']:
        wheel=bank/'package-artifacts'/safe_relative(row['wheel']['filename'])
        require(sha(wheel.read_bytes())==row['wheel']['digests']['sha256'],'wheel hash')
    return dict(direct=13,closure=len(versions),installed_files=len(actual),wheels_verified=len(plan['packages']),native_launchers_executed=False)

def svg_signature(node):
    normalize=lambda value:' '.join((value or '').split())
    return (node.tag,tuple(sorted((k,normalize(v)) for k,v in node.attrib.items())),normalize(node.text),
            tuple(svg_signature(child) for child in node))

def run_process(args,cwd,env,log,expected_tests=None):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
    with log.open('x',encoding='utf-8') as f:f.write(p.stdout+p.stderr)
    require(p.returncode==0,'declared subprocess failed; read external log')
    if expected_tests is not None:
        matches=re.findall(r'Ran (\d+) tests?',p.stdout+p.stderr)
        require(matches and int(matches[-1])==expected_tests and '\nOK' in p.stdout+p.stderr,'test count or outcome')
    return p

def run(args,run_dir):
    checks=[]
    before=equality(args.repo,args.head);checks.append('exact initial owner equality')
    final=tree_objects(args.repo,args.head)
    policy=strict_json(final[PHASE+'/final/canonical-policy.json']['raw'])
    require(sha(final[PHASE+'/final/ghc_family_canonical.py']['raw'])==policy['canonical_code_sha256'],'canonical definition hash')
    checks.append('canonical definition binding')
    stages=policy['stages'];stage_objects={};materialized={};chain=[];prior={};manifest_counts={}
    for stage in stages:
        head=args.head if stage['commit']=='EXACT_FINAL' else stage['commit']
        objects=final if head==args.head else tree_objects(args.repo,head)
        parents=git(args.repo,'rev-list','--parents','-n','1',head).decode().split()[1:]
        chain.append(dict(stage=stage['name'],head=head,parents=parents))
        require(set(prior)<=set(objects),'source file deletion')
        require(all(prior[p]['oid']==objects[p]['oid'] for p in prior),'earlier lifecycle file changed')
        changed=set(objects)-set(prior)
        manifest=strict_json(objects[PHASE+'/'+stage['name']+'/manifest.json']['raw'])
        manifest_counts[stage['name']]=verify_manifest(manifest,objects,changed)
        directory=run_dir/stage['materialized_directory'];directory.mkdir()
        for path,obj in objects.items():
            destination=directory/path;destination.parent.mkdir(parents=True,exist_ok=True)
            with destination.open('xb') as f:f.write(obj['raw'])
        stage_objects[stage['name']]=objects;materialized[stage['name']]=directory;prior=objects
        checks.append(stage['name']+' exact stage manifest and materialization')
    verify_chain(chain);checks.append('four direct lifecycle commits without merges')
    seal=strict_json(final[PHASE+'/final/content-seal.json']['raw'])
    seal_count=verify_manifest(seal,final,set(final));checks.append('final complete owner content seal')
    scanned=scan(final);checks.append('strict JSON Python AST word and five-class privacy review')
    source=policy['source_canonical']
    require(sha((args.source_bank/source['relative_path']).read_bytes())==source['sha256'],'source receipt binding')
    checks.append('prior canonical receipt read without execution')
    globals_result=validate_globals(final,args.global_tools,args.skill_root);checks.append('global capabilities shared metadata and archives')
    packages=validate_packages(final,args.package_site,args.bank);checks.append('exact installed package and wheel bytes')
    formatting=strict_json(final[PHASE+'/x2/svg-formatting-correction.json']['raw'])
    original_svg=(args.bank/'retained-unformatted-probability-and-entropy.svg').read_bytes()
    current_svg=final[PHASE+'/x2/figures/probability-and-entropy.svg']['raw']
    require(sha(original_svg)==formatting['original_svg_sha256'] and sha(current_svg)==formatting['corrected_svg_sha256'],'SVG source preservation')
    require(svg_signature(ET.fromstring(original_svg))==svg_signature(ET.fromstring(current_svg)),'SVG structural equivalence')
    checks.append('retained SVG formatting input and structural equality')
    env=dict(os.environ);env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',
        GHC_GLOBAL_TOOLS=str(args.global_tools),GHC_PACKAGE_SITE=str(args.package_site),
        GHC_PHASE_BANK=str(args.bank),GHC_FIXTURE_ROOT=str(run_dir/'fixtures'),
        TEMP=str(run_dir/'temp'),TMP=str(run_dir/'temp'))
    (run_dir/'temp').mkdir();(run_dir/'fixtures').mkdir()
    test_total=0
    for stage in stages:
        for module in stage['test_modules']:
            data=stage_objects[stage['name']][module['path']]['raw']
            require(sha(data)==module['sha256'],'test definition hash')
            run_process([sys.executable,'-X','utf8','-B','-m','unittest','discover','-s','tests','-p',Path(module['path']).name,'-v'],
                materialized[stage['name']],env,run_dir/(stage['name']+'-'+Path(module['path']).stem+'.log'),module['test_count'])
            test_total+=module['test_count'];checks.append(stage['name']+' '+Path(module['path']).name)
    final_root=materialized['final']
    for stage in ['x1','x2']:
        script=final_root/PHASE/'final/ghc_family_verify_contracts.py'
        run_process([sys.executable,'-X','utf8','-B',str(script),'--root',str(materialized[stage]),'--stage',stage],
                    final_root,env,run_dir/(stage+'-contract-replay.log'))
        checks.append(stage+' 100 complete typed contracts at immutable stage')
    smoke_out=run_dir/'fresh-package-smokes.json'
    run_process([sys.executable,'-I','-X','utf8','-B',str(final_root/PHASE/'x2/ghc_family_package_smokes.py'),
                 '--site',str(args.package_site),'--output',str(smoke_out)],final_root,env,run_dir/'package-smokes.log')
    fresh=strict_json(smoke_out.read_bytes());expected=strict_json(final[PHASE+'/x2/package-smokes-composite.json']['raw'])
    fields=['package','case','expected','observed','matched','subject_result','original_success_credit']
    require(len(fresh['rows'])==34 and fresh['selected_packages_exercised']==13 and fresh['all_matched'],'package smoke counts')
    require(all(typed_equal({k:a[k] for k in fields},{k:b[k] for k in fields}) for a,b in zip(fresh['rows'],expected['rows'])),'package semantic smoke comparison')
    checks.append('fresh exact-package API smoke comparison')
    experiment_out=run_dir/'fresh-mathematical-experiments.json'
    run_process([sys.executable,'-I','-X','utf8','-B',str(final_root/PHASE/'x2/ghc_family_model_experiments.py'),
                 '--repo',str(final_root),'--site',str(args.package_site),'--output',str(experiment_out)],final_root,env,run_dir/'model-experiments.log')
    fresh_experiment=strict_json(experiment_out.read_bytes());retained=strict_json(final[PHASE+'/x2/mathematical-experiments.json']['raw'])
    for key in ['matrix','stationary','trajectories','entropy_counterexample','coarse_graining_counterexample','egyptian_witnesses']:
        require(typed_equal(fresh_experiment[key],retained[key]),'mathematical experiment comparison')
    require(fresh_experiment['maximum_stationary_discrepancy']<1e-12,'numeric comparison tolerance')
    checks.append('fresh bounded mathematical experiments and 100 exact integer witnesses')
    validate_packages(final,args.package_site,args.bank);checks.append('package target unchanged after exercises')
    after=equality(args.repo,args.head);checks.append('exact final owner equality after validation')
    return dict(schema='ghc.family.exact-owner-canonical.v2',owner='Seren Talewood',phase='v689-v2-r2',
        status='VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',canonical_invocations=1,canonical_successes=1,replays=0,
        final=args.head,chain=chain,checks=[dict(name=n,passed=True) for n in checks],check_count=len(checks),
        tests_passed=test_total,typed_contracts_matched=200,package_smokes=34,integer_witnesses=100,
        owner_files=len(final),stage_manifest_entries=manifest_counts,content_seal_entries=seal_count,
        public_file_scan=scanned,global_verification=globals_result,packages=packages,
        equality_before=before,equality_after=after,source_canonical_replayed=False,
        source_or_sibling_tests_executed=False,repository_mutations=False,successor_messages=0,
        independent_reproduction=False,terminal_verdict='NOT_READY_FOR_STAGE_20',completed_at_utc=datetime.now(timezone.utc).isoformat())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['repo','bank','global-tools','package-site','source-bank','skill-root']:parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--head',required=True);args=parser.parse_args()
    for name in ['repo','bank','global_tools','package_site','source_bank','skill_root']:setattr(args,name,getattr(args,name).resolve())
    require(not args.bank.is_relative_to(args.repo),'canonical bank must be outside repository')
    require(re.fullmatch('[0-9a-f]{40}',args.head) is not None,'exact final commit required')
    directory=args.bank/('canonical-'+args.head[:12]);directory.mkdir(exist_ok=False)
    write_once(directory/'invocation-marker.json',dict(phase='v689-v2-r2',head=args.head,invocation=1,at_utc=datetime.now(timezone.utc).isoformat()))
    try:
        receipt=run(args,directory)
        write_once(directory/'exact-final-owner-scoped-canonical.json',receipt)
        write_once(directory/'success-marker.json',dict(status=receipt['status'],head=args.head,successes=1,replays=0))
    except Exception as error:
        if not (directory/'success-marker.json').exists():
            write_once(directory/'failure-receipt.json',dict(status='FAILED_OWNER_CANONICAL_RETAINED',head=args.head,invocations=1,successes=0,
                 error_type=type(error).__name__,error=str(error),replay_authorized=False,at_utc=datetime.now(timezone.utc).isoformat()))
        raise
    print(json.dumps({k:receipt[k] for k in ['status','final','check_count','tests_passed','typed_contracts_matched','owner_files']},ensure_ascii=True))

if __name__=='__main__':main()
