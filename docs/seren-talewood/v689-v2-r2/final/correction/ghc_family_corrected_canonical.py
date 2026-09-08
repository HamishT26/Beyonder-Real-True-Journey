"""Correct the failed byte-domain dependency while preserving the prior canonical."""
import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PHASE='docs/seren-talewood/v689-v2-r2'
CORRECTION=PHASE+'/final/correction'
BASE='bbce883aa3f4875ffcb343059a2ba2e521d62ab1'
spec=importlib.util.spec_from_file_location('retained_canonical_components',Path(__file__).resolve().parents[1]/'ghc_family_canonical.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def restore_checkout(raw,row):
    c.require(c.sha(raw)==row['git_sha256'] and len(raw)==row['git_bytes'],'exact Git byte-domain binding')
    c.require(b'\r\n' not in raw,'already CRLF input is not a Git-LF projection')
    restored=raw.replace(b'\n',b'\r\n')
    c.require(c.sha(restored)==row['working_sha256'] and len(restored)==row['working_bytes'],'exact historical checkout binding')
    c.require(restored.replace(b'\r\n',b'\n')==raw,'line-ending reversibility')
    return restored

def projected_objects(objects,bindings):
    result={p:dict(v) for p,v in objects.items()};changed=[]
    for row in bindings:
        if row['path'] not in result:continue
        result[row['path']]['raw']=restore_checkout(result[row['path']]['raw'],row)
        changed.append(row['path'])
    return result,changed

def run(args,directory):
    checks=[];initial=c.equality(args.repo,args.head);checks.append('initial exact owner equality')
    final=c.tree_objects(args.repo,args.head)
    policy=c.strict_json(final[CORRECTION+'/policy.json']['raw'])
    c.require(c.sha(final[CORRECTION+'/ghc_family_corrected_canonical.py']['raw'])==policy['corrected_definition_sha256'],'corrected definition binding')
    c.require(c.sha(final[PHASE+'/final/ghc_family_canonical.py']['raw'])==policy['retained_definition_sha256'],'retained definition binding')
    checks.append('both validator definitions bound')
    failed_dir=args.bank/'canonical-bbce883aa3f4'
    failed=(failed_dir/'failure-receipt.json').read_bytes()
    c.require(c.sha(failed)==policy['failure_receipt_sha256'],'retained failure receipt binding')
    failure=c.strict_json(failed)
    c.require(failure['successes']==0 and failure['invocations']==1 and failure['head']==BASE,'retained failed attempt state')
    c.require(not (failed_dir/'success-marker.json').exists(),'a success must not be replayed')
    c.require(c.git(args.repo,'rev-list','--parents','-n','1',args.head).decode().split()[1:]==[BASE],'correction direct parent')
    checks.append('failed first invocation retained and direct correction parent')
    diagnosis=c.strict_json(final[CORRECTION+'/byte-domain-bindings.json']['raw']);bindings=diagnosis['mismatches']
    c.require(len(bindings)==22 and all(r['working_equals_git_after_lf'] for r in bindings),'exact correction scope')
    original_policy=c.strict_json(final[PHASE+'/final/canonical-policy.json']['raw'])
    stages=[]
    for s in original_policy['stages']:
        stages.append(dict(s,commit=BASE if s['commit']=='EXACT_FINAL' else s['commit']))
    chain=[];prior={};trees={};materialized={};projection_counts={};manifest_counts={}
    for stage in stages:
        objects=c.tree_objects(args.repo,stage['commit'])
        c.require(set(prior)<=set(objects) and all(prior[p]['oid']==objects[p]['oid'] for p in prior),'earlier immutable tree drift')
        parents=c.git(args.repo,'rev-list','--parents','-n','1',stage['commit']).decode().split()[1:]
        chain.append(dict(head=stage['commit'],parents=parents,stage=stage['name']))
        manifest=c.strict_json(objects[PHASE+'/'+stage['name']+'/manifest.json']['raw'])
        manifest_counts[stage['name']]=c.verify_manifest(manifest,objects,set(objects)-set(prior))
        projected,changed=projected_objects(objects,bindings)
        place=directory/stage['materialized_directory'];place.mkdir()
        for path,obj in projected.items():
            target=place/path;target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as out:out.write(obj['raw'])
        trees[stage['name']]=objects;materialized[stage['name']]=place;projection_counts[stage['name']]=len(changed);prior=objects
        checks.append(stage['name']+' exact Git stage manifest and explicit historical checkout materialization')
    c.verify_chain(chain);checks.append('four retained direct lifecycle boundaries')
    c.require(set(prior)<=set(final) and all(prior[p]['oid']==final[p]['oid'] for p in prior),'correction changed a sealed file')
    delta=set(final)-set(prior)
    c.require(all(p.startswith(CORRECTION+'/') or p=='tests/test_ghc_family_canonical_correction.py' for p in delta),'correction owner allowlist')
    manifest_counts['correction']=c.verify_manifest(c.strict_json(final[CORRECTION+'/manifest.json']['raw']),final,delta)
    checks.append('additive correction manifest and no sealed-file mutation')
    seal=c.strict_json(final[CORRECTION+'/git-content-seal.json']['raw'])
    seal_count=c.verify_manifest(seal,final,set(final));checks.append('complete final Git-blob content seal')
    base_projected,_=projected_objects(trees['final'],bindings)
    old_seal=c.strict_json(trees['final'][PHASE+'/final/content-seal.json']['raw'])
    c.verify_manifest(old_seal,base_projected,set(base_projected))
    checks.append('old working-byte seal verified only in its corrected declared checkout domain')
    scanned=c.scan(final);checks.append('strict JSON Python AST word and privacy scan')
    source=original_policy['source_canonical']
    c.require(c.sha((args.source_bank/source['relative_path']).read_bytes())==source['sha256'],'source canonical binding')
    checks.append('original Seren source canonical read without replay')
    globals_result=c.validate_globals(final,args.global_tools,args.skill_root);checks.append('global capabilities and archive bindings')
    packages=c.validate_packages(final,args.package_site,args.bank);checks.append('package installation and reviewed wheels')
    formatting=c.strict_json(final[PHASE+'/x2/svg-formatting-correction.json']['raw'])
    original_svg=(args.bank/'retained-unformatted-probability-and-entropy.svg').read_bytes();current_svg=final[PHASE+'/x2/figures/probability-and-entropy.svg']['raw']
    c.require(c.sha(original_svg)==formatting['original_svg_sha256'] and c.sha(current_svg)==formatting['corrected_svg_sha256'],'SVG bindings')
    c.require(c.svg_signature(c.ET.fromstring(original_svg))==c.svg_signature(c.ET.fromstring(current_svg)),'SVG normalization relation')
    checks.append('retained SVG and unchanged normalized structure')
    git_place=directory/'g';git_place.mkdir()
    for path,obj in final.items():
        target=git_place/path;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as out:out.write(obj['raw'])
    (directory/'temp').mkdir();(directory/'fixtures').mkdir()
    env=dict(os.environ);env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',GHC_GLOBAL_TOOLS=str(args.global_tools),
       GHC_PACKAGE_SITE=str(args.package_site),GHC_PHASE_BANK=str(args.bank),GHC_FIXTURE_ROOT=str(directory/'fixtures'),
       TEMP=str(directory/'temp'),TMP=str(directory/'temp'))
    tests=0
    for stage in stages:
        for entry in stage['test_modules']:
            c.require(c.sha(trees[stage['name']][entry['path']]['raw'])==entry['sha256'],'retained test definition hash')
            c.run_process([sys.executable,'-X','utf8','-B','-m','unittest','discover','-s','tests','-p',Path(entry['path']).name,'-v'],
                materialized[stage['name']],env,directory/(stage['name']+'-'+Path(entry['path']).stem+'.log'),entry['test_count'])
            tests+=entry['test_count'];checks.append(stage['name']+' '+Path(entry['path']).name)
    entry=policy['correction_test']
    c.require(c.sha(final[entry['path']]['raw'])==entry['sha256'],'correction test definition hash')
    c.run_process([sys.executable,'-X','utf8','-B','-m','unittest','discover','-s','tests','-p',Path(entry['path']).name,'-v'],
        git_place,env,directory/'correction-tests.log',entry['test_count'])
    tests+=entry['test_count'];checks.append('five correction byte-domain and retention tests')
    for stage in ['x1','x2']:
        c.run_process([sys.executable,'-X','utf8','-B',str(git_place/PHASE/'final/ghc_family_verify_contracts.py'),
            '--root',str(materialized[stage]),'--stage',stage],git_place,env,directory/(stage+'-typed-contracts.log'))
        checks.append(stage+' one hundred complete typed immutable contracts')
    smoke=directory/'fresh-package-smokes.json'
    c.run_process([sys.executable,'-I','-X','utf8','-B',str(git_place/PHASE/'x2/ghc_family_package_smokes.py'),
        '--site',str(args.package_site),'--output',str(smoke)],git_place,env,directory/'package-smokes.log')
    fresh=c.strict_json(smoke.read_bytes());expected=c.strict_json(final[PHASE+'/x2/package-smokes-composite.json']['raw'])
    fields=['package','case','expected','observed','matched','subject_result','original_success_credit']
    c.require(len(fresh['rows'])==34 and fresh['selected_packages_exercised']==13 and fresh['all_matched'],'package counts')
    c.require(all(c.typed_equal({k:a[k] for k in fields},{k:b[k] for k in fields}) for a,b in zip(fresh['rows'],expected['rows'])),'package smoke semantic equality')
    checks.append('fresh package API comparison')
    experiment=directory/'fresh-mathematical-experiments.json'
    c.run_process([sys.executable,'-I','-X','utf8','-B',str(git_place/PHASE/'x2/ghc_family_model_experiments.py'),
        '--repo',str(git_place),'--site',str(args.package_site),'--output',str(experiment)],git_place,env,directory/'experiments.log')
    actual=c.strict_json(experiment.read_bytes());expected=c.strict_json(final[PHASE+'/x2/mathematical-experiments.json']['raw'])
    for key in ['matrix','stationary','trajectories','entropy_counterexample','coarse_graining_counterexample','egyptian_witnesses']:
        c.require(c.typed_equal(actual[key],expected[key]),'mathematical semantic comparison')
    c.require(actual['maximum_stationary_discrepancy']<1e-12,'floating comparison tolerance')
    checks.append('fresh exact mathematical and integer-witness comparisons')
    c.validate_packages(final,args.package_site,args.bank);checks.append('package bytes unchanged after exercises')
    ending=c.equality(args.repo,args.head);checks.append('final exact clean owner equality')
    return dict(schema='ghc.family.dependency-corrected-owner-canonical.v1',status='VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_CANONICAL',
        owner='Seren Talewood',phase='v689-v2-r2',final=args.head,prior_final=BASE,prior_attempt_status=failure['status'],
        prior_failed_attempts=1,corrected_invocations=1,total_canonical_invocations=2,canonical_successes=1,successful_canonical_replays=0,
        original_failure_erased=False,original_raw_seal_claim_corrected=True,byte_domain_projection_counts=projection_counts,
        chain=chain+[dict(head=args.head,parents=[BASE],stage='correction')],tests_passed=tests,typed_contracts_matched=200,
        checks=[dict(name=n,passed=True) for n in checks],check_count=len(checks),owner_files=len(final),
        stage_manifest_entries=manifest_counts,content_seal_entries=seal_count,public_file_scan=scanned,
        global_verification=globals_result,packages=packages,package_smokes=34,integer_witnesses=100,
        equality_before=initial,equality_after=ending,source_canonical_replayed=False,source_or_sibling_tests_executed=False,
        repository_mutations=False,successor_messages=0,independent_reproduction=False,
        terminal_verdict='NOT_READY_FOR_STAGE_20',completed_at_utc=datetime.now(timezone.utc).isoformat())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['repo','bank','global-tools','package-site','source-bank','skill-root']:parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--head',required=True);args=parser.parse_args()
    for name in ['repo','bank','global_tools','package_site','source_bank','skill_root']:setattr(args,name,getattr(args,name).resolve())
    c.require(re.fullmatch('[0-9a-f]{40}',args.head) is not None and args.head!=BASE,'new exact corrected head')
    c.require(not args.bank.is_relative_to(args.repo),'external validation bank')
    directory=args.bank/('corrected-canonical-'+args.head[:12]);directory.mkdir(exist_ok=False)
    c.write_once(directory/'invocation-marker.json',dict(head=args.head,total_attempt_number=2,corrected_invocation=1,at_utc=datetime.now(timezone.utc).isoformat()))
    try:
        receipt=run(args,directory)
        c.write_once(directory/'exact-final-owner-scoped-canonical.json',receipt)
        c.write_once(directory/'success-marker.json',dict(head=args.head,status=receipt['status'],canonical_successes=1,total_invocations=2,successful_replays=0))
    except Exception as error:
        c.write_once(directory/'failure-receipt.json',dict(status='FAILED_CORRECTED_CANONICAL_RETAINED',head=args.head,total_attempt_number=2,
            successes=0,error_type=type(error).__name__,error=str(error),replay_authorized=False,at_utc=datetime.now(timezone.utc).isoformat()))
        raise
    print(json.dumps({k:receipt[k] for k in ['status','final','check_count','tests_passed','owner_files','total_canonical_invocations','canonical_successes','successful_canonical_replays']}))

if __name__=='__main__':main()
