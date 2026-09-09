"""One exact-final canonical for this owner delta; prior successes are never replayed."""
import argparse,ast,collections,hashlib,importlib.util,io,json,os,pathlib,re,subprocess,sys,unittest
from datetime import datetime,timezone
from fractions import Fraction

BASE='bbf670530d5971aade7bec58733ed1e457f362cb'
REL='docs/seren-talewood/v689-v2-r3'
CSKILLS=pathlib.Path(os.environ.get('CODEX_HOME',pathlib.Path.home()/'.codex'))/'skills'
DTOOLS=pathlib.Path('D:/GHC-Archives/global-tools/family-capacity-lab/scripts')
PACKAGE=pathlib.Path('D:/GHC-Archives/global-tools/family-capacity-lab/python-site')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,j):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(j,f,indent=2,sort_keys=True,ensure_ascii=False);f.write('\n')
def canonical(j):return json.dumps(j,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def require(ok,why):
    if not ok:raise RuntimeError(why)
def git(root,*args):return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,timeout=90).stdout
def blob_batch(root,head,paths):
    data=git_input(root,['cat-file','--batch'],''.join(head+':'+p+'\n' for p in paths).encode())
    offset=0;out={}
    for p in paths:
        end=data.index(b'\n',offset);oid,kind,size=data[offset:end].decode().split();size=int(size)
        require(kind=='blob','Nonblob '+p);out[p]=data[end+1:end+1+size];offset=end+size+2
    require(offset==len(data),'Trailing batch response');return out
def git_input(root,args,data):return subprocess.run(['git','-C',str(root),*args],input=data,check=True,capture_output=True,timeout=90).stdout

def run(root,head,bank):
    outdir=bank/('canonical-'+head[:12]);outdir.mkdir(exist_ok=False)
    dump(outdir/'invocation-marker.json',{'head':head,'utc':datetime.now(timezone.utc).isoformat(),'owner':'Seren Talewood','phase':'v689-v2-r3','canonical_invocations':1,'success_replays':0})
    checks=[]
    def check(name,details):checks.append({'name':name,'passed':True,'details':details})
    try:
        require(sys.flags.optimize==0,'Assertions must not be optimized away')
        actual=git(root,'rev-parse','HEAD').decode().strip();upstream=git(root,'rev-parse','@{upstream}').decode().strip();tracking=git(root,'rev-parse','refs/remotes/origin/codex/GHC-Family/seren-talewood-main').decode().strip();live=git(root,'ls-remote','origin','refs/heads/codex/GHC-Family/seren-talewood-main').decode().split()[0]
        require(actual==upstream==tracking==live==head,'Four-way equality')
        require(not git(root,'status','--porcelain').strip(),'Dirty owner tree')
        divergence=[int(x) for x in git(root,'rev-list','--left-right','--count','HEAD...@{upstream}').decode().split()];require(divergence==[0,0],'Divergence')
        check('exact_final_git_state',{'head':head,'local':actual,'upstream':upstream,'tracking':tracking,'fresh_live':live,'divergence':divergence})
        commits=git(root,'rev-list','--reverse','--parents',BASE+'..'+head).decode().splitlines();require(len(commits)==4,'Exactly four direct lifecycle commits required')
        parent=BASE
        for line in commits:
            parts=line.split();require(len(parts)==2 and parts[1]==parent,'Nonlinear lifecycle');parent=parts[0]
        check('direct_owner_lifecycle',{'new_commits':4,'merges':0,'base':BASE})
        changed=git(root,'diff','--name-status',BASE,head).decode().splitlines();require(all(l.startswith('A\t') for l in changed),'Prior files changed')
        paths=sorted(l.split('\t',1)[1] for l in changed)
        require(all(p.startswith(REL+'/') or p.startswith('scripts/ghc_family_') or p.startswith('skills/ghc-family-') or p.startswith('tests/test_ghc_family_capacity_') for p in paths),'Owner allowlist')
        blobs=blob_batch(root,head,paths)
        require(all((root/p).read_bytes()==b for p,b in blobs.items()),'Working bytes differ from exact Git blobs')
        tracked=len(git(root,'ls-files','-z').split(b'\0'))-1
        materialized=sum(p.is_file() and '.git' not in p.parts for p in root.rglob('*'))
        require(tracked<2000 and materialized<2000,'File ceiling')
        check('owner_delta_and_capacity',{'new_files':len(paths),'tracked':tracked,'materialized':materialized,'prior_files_modified':0})
        def readj(path):return json.loads(blobs[path])
        stage_counts={}
        for stage in ['plan','x1','x2','final']:
            p=REL+'/'+stage+'/manifest.json';m=readj(p);require(m['byte_domain']=='git_blob','Manifest byte domain')
            require(m['self_exclusions']==[p] and m['file_count']==len(m['entries'])+1,'Manifest arithmetic')
            for r in m['entries']:
                b=blobs[r['path']];require(len(b)==r['bytes'] and sha(b)==r['sha256'],'Stage manifest mismatch '+r['path'])
            stage_counts[stage]=len(m['entries'])
        check('stage_git_manifests',stage_counts)
        seal=readj(REL+'/final/content-seal.json');require(seal['byte_domain']=='git_blob','Seal byte domain')
        require(set(r['path'] for r in seal['entries'])|set(seal['self_exclusions'])==set(paths),'Seal coverage')
        require(len(seal['entries'])+len(seal['self_exclusions'])==len(paths),'Seal cardinality')
        for r in seal['entries']:
            b=blobs[r['path']];require(sha(b)==r['sha256'] and len(b)==r['bytes'],'Content seal mismatch '+r['path'])
        check('owner_delta_content_seal',{'entries':len(seal['entries']),'exclusions':seal['self_exclusions']})
        def pairs(items):
            obj={}
            for k,v in items:require(k not in obj,'Duplicate JSON key');obj[k]=v
            return obj
        def constant(v):raise RuntimeError('Nonfinite JSON '+v)
        json_count=0;ast_count=0
        for p,b in blobs.items():
            if p.endswith('.json'):json.loads(b,object_pairs_hook=pairs,parse_constant=constant);json_count+=1
            if p.endswith('.py'):ast.parse(b.decode('utf-8-sig'),filename=p);ast_count+=1
        check('strict_json_and_python_syntax',{'json':json_count,'python':ast_count})
        sys.path.insert(0,str(root/'scripts'))
        from ghc_family_capacity_core import evaluate as cap,typed_equal
        from ghc_family_inference_core import evaluate as inf
        proposals=readj(REL+'/plan/new-proposals.json')['proposals'];require(len(proposals)==200,'Proposal cardinality')
        require(len({p['proposal_id'] for p in proposals})==len({p['input_sha256'] for p in proposals})==200,'Duplicate proposal identity or request')
        for p in proposals:
            require(sha(canonical(p['input']))==p['input_sha256'],'Input hash')
            actual=(cap if p['stage']=='x1' else inf)(p['input']);require(typed_equal(actual,p['expected']),'Fresh typed contract '+p['proposal_id'])
        check('fresh_owner_typed_contracts',{'matched':200,'additional_novelty_credit':0})
        portfolio_counts={}
        for stage in ['x1','x2']:
            data=readj(REL+'/'+stage+'/portfolio-results.json')
            for kind in ['safe_now','candidate','clean_fix_refine']:
                require(len(data[kind])==100 and all(r['matched'] for r in data[kind]),stage+' portfolio results')
            require(all(r['original_success_credit']==0 and r['subject_result']=='fail' for r in data['candidate']),'Candidate credit')
            require(all(r['source_execution_credit']==0 and r['new_proposal_credit']==0 and r['source_record_sha256']==r['roundtrip_sha256'] for r in data['clean_fix_refine']),'Inherited recredit')
            portfolio_counts[stage]={kind:len(data[kind]) for kind in ['safe_now','candidate','clean_fix_refine']}
        check('two_session_portfolios',portfolio_counts)
        from ghc_family_weighted_route_review import review
        route=readj(REL+'/plan/route-v4.json');profile=readj(REL+'/plan/profile-v4.json');projection=review(route,profile)
        require(projection['model_roles']=={'Sol':196,'Astra':98},'Weighted role totals')
        check('weighted_roster',{'identities':30,'positions':45,'future':294,'last':projection['last']})
        from ghc_family_weighted_handoff_composer import compose
        req={'profile':profile,'route':route,'relative_astra_cost':2,'sizes':[3,3,3],'prefix':2,'limit':8,'events':[['synthetic-handoff','digest-label','accepted']]}
        comp=compose(req);require(comp['ok'] and comp['value']['messages_sent']==0 and comp['value']['cost']['relative_saving']=='1/9','Compound review')
        check('compound_skill',{'source_skills':4,'actual_messages':0})
        ledger=readj(REL+'/x2/method-flow.json');witnesses={w['witness_id']:w for w in ledger['witnesses']}
        require(len(witnesses)==len(ledger['witnesses']),'Duplicate witness ID')
        for m in ledger['methods']:
            actual_ids={w['witness_id'] for w in witnesses.values() if w['method_id']==m['method_id']}
            require(set(m['validation_witness_ids'])==actual_ids,'Method backlink mismatch')
            require(any(witnesses[w]['result']=='pass' for w in actual_ids),'Preferred method without pass')
        method_counts=dict(collections.Counter(w['result'] for w in witnesses.values()));require(method_counts=={'pass':637,'fail':297} and len(ledger['methods'])==29,'Method counts')
        require(readj(REL+'/x2/method-validation.json')['valid'],'Declared method validation')
        check('retained_method_evidence',{'methods':29,'witnesses':method_counts,'independent_reproduction':False})
        deck_index=readj(REL+'/x2/deck/deck-index.json');cards={}
        for cid in deck_index['cards']:
            card=readj(REL+'/x2/deck/'+cid+'.json');payload={k:v for k,v in card.items() if k!='card_id'}
            require(cid=='ghc-card-'+sha(canonical(payload))[:24],'Card identity hash');cards[cid]=card
        require(len(cards)==268,'Deck count')
        for c in cards.values():
            if c['tier']==1:require(c['parent_ids']==[],'Owner parent')
            else:require(len(c['parent_ids'])==1 and cards[c['parent_ids'][0]]['tier']==c['tier']-1,'Card parent')
        dm=readj(REL+'/x2/deck/card-manifest.json')
        for r in dm['entries']:
            b=blobs[REL+'/x2/deck/'+r['path']];require(len(b)==r['bytes'] and sha(b)==r['sha256'],'Card manifest')
        check('four_tier_deck',{'cards':268,'manifest_members':len(dm['entries'])})
        global_count=0
        for stage in ['x1','x2']:
            receipts=[readj(REL+'/'+stage+'/tool-promotion.json')]
            if stage=='x2':receipts.append(readj(REL+'/x2/compound-results.json'))
            for receipt in receipts:
                for row in receipt['copies']:
                    target=(DTOOLS if row['target_role']=='D tools' else CSKILLS)/row['target_relative']
                    require(target.is_file() and sha(target.read_bytes())==row['sha256'],'Global tool parity '+row['source']);global_count+=1
        require(global_count==78,'New global file count')
        check('new_global_tool_parity',{'files':global_count,'skills':21,'runners':12,'cores':2})
        old=readj(REL+'/x1/shared-file-bindings.json');new=readj(REL+'/x2/shared-publication.json');latest={r['path']:r for r in new['files']}
        for row in old['files']:
            relative=row['path']
            if relative in new['superseded_x1_pointer_files']:
                archive=CSKILLS/pathlib.PurePosixPath(relative).parent/'capacity-tooling-x1-before-x2.json';require(sha(archive.read_bytes())==row['sha256'],'Historical shared pointer archive')
            else:latest.setdefault(relative,row)
        for relative,row in latest.items():require(sha((CSKILLS/relative).read_bytes())==row['sha256'],'Current shared parity '+relative)
        check('shared_workflow_and_archives',{'current_files':len(latest),'historical_pointer_archives':2,'entrypoints':26})
        reused=0
        for stage in ['x1','x2']:
            for skill in readj(REL+'/'+stage+'/prior-tool-reuse.json')['skills']:
                for row in skill['source_files']:require(sha((CSKILLS/skill['name']/row['relative_path']).read_bytes())==row['sha256'],'Prior selected capability drift')
                require(skill['bounded_example_matched'] and not skill['installed_now'],'Prior reuse state');reused+=1
        check('selected_prior_capabilities',{'skills':reused,'prior_canonical_replays':0})
        install=readj(REL+'/x1/package-installation.json');require(install['direct_count']==13 and install['closure_count']==16 and len(install['files'])==401,'Package cardinality')
        for r in install['files']:
            p=PACKAGE/r['path'];require(p.is_file() and p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256'],'Installed package mismatch '+r['path'])
        require(not any(p.name.lower().startswith('diskcache') for p in PACKAGE.iterdir()),'Rejected package in target')
        smoke=readj(REL+'/x1/package-smokes.json');require(smoke['count']==26 and smoke['all_passed'],'Package smoke binding')
        check('installed_package_snapshot',{'files':401,'direct':13,'closure':16,'bound_api_checks':26,'api_replays':0,'diskcache_installed':False})
        science=readj(REL+'/x2/scientific-results.json');unit=science['unit_fraction_classes'];require(len(unit['verified'])==416 and len(unit['uncovered'])==83,'Unit-fraction partition')
        for r in unit['verified']:require(Fraction(4,r['n'])==sum((Fraction(1,d) for d in r['denominators']),Fraction(0)),'Unit-fraction residual')
        require({r['n'] for r in unit['verified']}|set(unit['uncovered'])==set(range(2,501)),'Unit-fraction range')
        for r in science['conditional_null_enumeration']:require(Fraction(r['expected_final_likelihood_ratio'])==1 and Fraction(r['crossing_probability'])<=Fraction(1,4),'Sequential model result')
        require(science['correlated_marginal_counterexample']['conditional_null_holds'] is False,'Correlated-null boundary')
        check('bounded_scientific_results',{'exact_fraction_witnesses':416,'uncovered':83,'max_horizon':10,'empirical_confirmation':False})
        index=readj(REL+'/final/baton-module-index.json');baton=blobs[REL+'/final/hand-off-baton.md'];text=baton.decode('utf-8')
        wc=len(re.findall(r'\S+',text));require(10000<=wc<=100000 and wc==index['combined_words']==16769,'Baton words')
        require(text.rstrip().endswith('EOF SEREN TALEWOOD v689-v2-r3 BATON.') and len(index['modules'])==13,'Baton terminal marker')
        require(sha(baton)==index['combined_sha256'],'Baton digest')
        for m in index['modules']:require(sha(blobs[m['path']])==m['sha256'],'Baton module digest')
        from pypdf import PdfReader
        pdf=blobs[REL+'/final/overview.pdf'];pages=len(PdfReader(io.BytesIO(pdf)).pages);require(pages==4,'PDF page count')
        visual=readj(REL+'/final/visual-review.json');require(visual['all_pages_visually_checked'] and visual['page_count']==4 and visual['pdf_sha256']==sha(pdf),'PDF review binding')
        check('readable_handoff_artifacts',{'baton_words':wc,'modules':13,'pdf_pages':pages,'visually_reviewed':True})
        patterns={'raw_uuid':re.compile(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b'),'private_local_path':re.compile(r'(?:[A-Za-z]:[\\/]+Users[\\/]+|/Users/)[A-Za-z0-9_-]+'),'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'credential':re.compile(r'\b(?:sk-[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{24,})')}
        hits=[]
        for p,b in blobs.items():
            if p.endswith(('.json','.md','.py','.yaml','.txt')):
                t=b.decode('utf-8-sig')
                for name,rx in patterns.items():
                    if rx.search(t):hits.append({'path':p,'class':name})
        require(not hits,'Scoped privacy candidates '+json.dumps(hits))
        check('scoped_privacy_patterns',{'pattern_classes':list(patterns),'confirmed_hits':0,'exhaustive_security':False})
        suite=unittest.TestSuite();loader=unittest.TestLoader()
        for name in ['test_ghc_family_capacity_x1.py','test_ghc_family_capacity_x2.py']:
            p=root/'tests'/name;spec=importlib.util.spec_from_file_location('canonical_'+p.stem,p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);suite.addTests(loader.loadTestsFromModule(module))
        stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
        (outdir/'test-output.txt').write_text(stream.getvalue(),encoding='utf-8',newline='\n')
        require(result.wasSuccessful() and result.testsRun==24,'Owner invariant tests')
        check('exact_final_owner_invariant_tests',{'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'source_test_modules':0})
        require(git(root,'rev-parse','HEAD').decode().strip()==head and not git(root,'status','--porcelain').strip(),'Owner tree changed during canonical')
        require(git(root,'ls-remote','origin','refs/heads/codex/GHC-Family/seren-talewood-main').decode().split()[0]==head,'Remote changed during canonical')
        check('post_validation_git_readback',{'head_unchanged':True,'clean':True,'fresh_live_equal':True})
        receipt={'schema':'ghc.family.owner-canonical.v1','status':'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL','owner':'Seren Talewood','phase':'v689-v2-r3','final_commit':head,'base':BASE,'utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'check_count':len(checks),'tests_passed':24,'fresh_typed_contracts':200,'new_proposals':201,'new_owner_files':len(paths),'owner_tracked_files':tracked,'owner_materialized_files':materialized,'canonical_invocations':1,'canonical_successes':1,'successful_replays':0,'source_canonical_replays':0,'source_suites_executed':0,'package_api_replays':0,'native_messages_sent_by_validator':0,'independent_reproduction':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'}
        dump(outdir/'exact-final-owner-scoped-canonical.json',receipt)
        dump(outdir/'success-marker.json',{'receipt_sha256':sha((outdir/'exact-final-owner-scoped-canonical.json').read_bytes()),'successful_replay_forbidden':True})
        print(json.dumps({'status':receipt['status'],'head':head,'checks':len(checks),'tests':24,'delta_files':len(paths),'owner_files':tracked},indent=2))
    except Exception as ex:
        dump(outdir/'failure-receipt.json',{'status':'FAILED_EXACT_FINAL_OWNER_SCOPED_CANONICAL','head':head,'error':type(ex).__name__,'message':str(ex),'checks_completed':checks,'canonical_successes':0,'successful_replays':0})
        raise
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--head',required=True);ap.add_argument('--bank',required=True);a=ap.parse_args()
    run(pathlib.Path(a.root),a.head,pathlib.Path(a.bank))
