"""One exact-final attributable canonical attempt, with an external exclusive latch."""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,traceback
from pathlib import Path
import ghc_family_ilyan_reed_v685_v8_validation as v
def put_exclusive(path,d):
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--final',required=True);ap.add_argument('--receipt',required=True);ap.add_argument('--global-root',required=True);a=ap.parse_args();receipt=Path(a.receipt).resolve();marker=Path(str(receipt)+'.invoked')
    if receipt.is_relative_to(v.ROOT.resolve()):raise ValueError('Receipt must be external to the sealed repository')
    if receipt.exists() or marker.exists():raise FileExistsError('Canonical invocation or receipt already exists; replay refused')
    if v.git('rev-parse','HEAD').decode().strip()!=a.final:raise ValueError('Exact final argument must match HEAD before invocation')
    receipt.parent.mkdir(parents=True,exist_ok=True);put_exclusive(marker,{'owner':'Ilyan Reed','phase':'v685-v8','head':a.final,'invocations':1,'replay_permitted':False})
    result={'schema':'ghc.family.ilyan.exact-final-canonical.v1','owner':'Ilyan Reed','phase':'v685-v8','head':a.final,'source':v.SOURCE,'x1':v.X1,'canonical_invocation_count':1,'canonical_success_count':0,'canonical_replay_count':0,'same_owner_only':True,'independent_reproduction':False,'complete_repository_suite':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20','status':'INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL'}
    try:
        policy=v.read('final/validation-policy.json');e=policy['evidence'];result['evidence']=e;before=v.equality();paths=v.owner_files();scope=v.git('diff','--name-status',v.SOURCE,a.final).decode().splitlines();changes=[line.split('\t',1) for line in scope];names=sorted(x[1] for x in changes)
        checks={'exact_final':before['head']==a.final,'exact_branch':before['branch']==policy['branch'],'clean_before':before['clean'],'four_way_before':before['four_way_equal'],'zero_divergence_before':before['divergence']=='0\t0','only_owner_additions':all(x[0]=='A' for x in changes) and names==sorted(v.rel(p) for p in paths),'owner_file_ceiling':len(paths)<=2000,'three_commits':v.git('rev-list','--count',v.SOURCE+'..'+a.final).decode().strip()=='3','zero_merges':v.git('rev-list','--merges',v.SOURCE+'..'+a.final).strip()==b'','source_x1_edge':v.git('rev-parse',v.X1+'^').decode().strip()==v.SOURCE,'x1_evidence_edge':v.git('rev-parse',e+'^').decode().strip()==v.X1,'evidence_final_edge':v.git('rev-list','--parents','-n','1',a.final).decode().split()==[a.final,e]}
        # Git blobs, not a working-tree newline convention, define manifest truth.
        specs=[('x1','validation/x1-manifest.json',v.X1),('evidence','validation/evidence-manifest.json',e),('cards','x2/flashcards/card-manifest.json',e),('final_delta','validation/final-delta-manifest.json',a.final),('owner','validation/final-owner-manifest.json',a.final)]
        manifests={label:v.replay_manifest('docs/ilyan-reed/v685-v8/'+path,rev) for label,path,rev in specs};checks['manifest_replay']=all(x['valid'] for x in manifests.values())
        om=v.read('validation/final-owner-manifest.json');checks['manifest_scope_complete']=set(names)==set(x['path'] for x in om['entries'])|set(om['self_exclusions'])
        delta=v.git('diff','--name-only',e,a.final).decode().splitlines();dm=v.read('validation/final-delta-manifest.json');checks['final_delta_scope_complete']=set(delta)==set(x['path'] for x in dm['entries'])|set(dm['self_exclusions'])
        tree=v.tree_checks(paths);checks.update(json_markdown_yaml_python_html_structure=tree['structure_valid'],privacy_hits_zero=tree['privacy_confirmed_hits']==0,bounded_security_findings_zero=tree['bounded_security_findings']==0)
        deck=v.deck_check();method=v.method_check();checks['card_graph_and_addresses']=deck['valid'];checks['method_flow_links_and_counts']=method['valid']
        seal=v.read('final/content-seal.json');seal_blobs=v.blob_batch([a.final+':'+r['path'] for r in seal['targets']]);checks['ten_content_seal_targets']=len(seal_blobs)==10 and all(v.digest(b)==r['sha256'] and len(b)==r['bytes'] for r,b in zip(seal['targets'],seal_blobs))
        promotion=v.read('x2/global-promotion-installation.json');parity=True;global_files=0
        for s in promotion['skills']:
            folder=Path(a.global_root)/s['name']
            actual=sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())
            if actual!=sorted(f['path'] for f in s['files']):parity=False
            for f in s['files']:
                global_files+=1;p=folder/f['path']
                if not p.is_file() or v.digest(p.read_bytes())!=f['sha256']:parity=False
        checks['ten_global_skills_byte_parity']=len(promotion['skills'])==10 and parity;checks['five_unique_runners']=promotion['unique_shared_runners']==5
        integrity=v.read('final/baton-integrity.json');checks['baton_word_and_section_bounds']=10000<=integrity['words']<=100000 and integrity['sections']==13
        pdf=v.read('final/overview-pdf-validation.json');checks['overview_at_least_three_pages']=pdf['pages']>=3 and pdf['pdf_text_extraction_pass']
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
        run=subprocess.run([sys.executable,'-B','-X','utf8',str(v.ROOT/'tests/test_ghc_family_ilyan_reed_v685_v8_final.py'),'--include-behavior'],cwd=v.ROOT,env=env,capture_output=True,text=True,encoding='utf8')
        tests=json.loads(run.stdout.strip()) if run.stdout.strip() else {'passed':False,'tests_run':0};checks['thirty_selected_tests']=run.returncode==0 and tests['passed'] and tests['tests_run']==30
        after=v.equality();checks.update(clean_after=after['clean'],four_way_after=after['four_way_equal'],zero_divergence_after=after['divergence']=='0\t0',head_unchanged=after['head']==a.final)
        result.update(checks=checks,counts={**tree['counts'],'detailed_checks':len(checks),'passed_checks':sum(checks.values()),'tests':tests['tests_run'],'manifest_entries':sum(x['entries'] for x in manifests.values()),'global_files':global_files,'cards':deck['cards'],'baton_words':integrity['words'],'overview_words':integrity['overview_words'],'overview_pages':pdf['pages'],'privacy_confirmed_hits':tree['privacy_confirmed_hits'],'bounded_security_findings':tree['bounded_security_findings']},manifests=manifests,tests=tests,tree=tree,before=before,after=after,scope={'changed_file_allowlist':names,'test_modules':policy['test_modules'],'unchanged_history_scan':False,'sibling_lane_mutation':False,'repository_suite':False})
        if all(checks.values()):result.update(status='VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',canonical_success_count=1)
    except Exception as exc:result.update(failure_type=type(exc).__name__,failure=str(exc),canonical_success_count=0)
    result['payload_sha256']=v.digest(v.canonical(result));put_exclusive(receipt,result)
    print(json.dumps({'status':result['status'],'head':result['head'],'counts':result.get('counts',{}),'failed_checks':[k for k,b in result.get('checks',{}).items() if not b],'failure':result.get('failure'),'canonical_invocation_count':1,'canonical_success_count':result['canonical_success_count'],'canonical_replay_count':0}))
    raise SystemExit(0 if result['canonical_success_count']==1 else 1)
if __name__=='__main__':main()
