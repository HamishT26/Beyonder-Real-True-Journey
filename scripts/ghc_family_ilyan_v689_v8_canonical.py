"""One exclusive canonical at the exact pushed Ilyan owner final."""
from __future__ import annotations
import argparse,copy,datetime,importlib.util,json,os,re,subprocess,sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import ghc_family_ilyan_v689_v8_io as io
PLAN='c7d15a959610d81002c6884c6b699eccdc92ba5e';X1='e3454293b2faa60de7318758b6918a8fcd73fdc6';X2='cdd85474ca5dccca331e80579bbd45f4669908e1'

class Document(HTMLParser):
    def __init__(self):super().__init__();self.tags=[];self.language=False;self.images=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.tags.append(tag)
        if tag=='html':self.language=d.get('lang')=='en'
        if tag=='img':self.images.append(bool(d.get('alt')))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-final',required=True);ap.add_argument('--receipt-dir',required=True);ap.add_argument('--skills-root',required=True);ap.add_argument('--runner-root',required=True);ap.add_argument('--package-python',required=True);ap.add_argument('--wheel-root',required=True);ap.add_argument('--runtime-root',required=True);ap.add_argument('--method-runner',required=True);a=ap.parse_args()
    dest=Path(a.receipt_dir);dest.mkdir(parents=True,exist_ok=True);attempt=dest/'exact-final-attempt.json';receipt=dest/'exact-final-owner-scoped-canonical.json';success=dest/'exact-final-success.json'
    if receipt.exists() or success.exists():raise SystemExit('Existing canonical receipt or success latch: no replay')
    with attempt.open('x',encoding='utf8',newline='\n') as f:json.dump({'owner':'Ilyan Reed','phase':'v689-v8','expected_final':a.expected_final,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'invocations':1},f,indent=2);f.write('\n')
    checks=[];report={'owner':'Ilyan Reed','phase':'v689-v8','branch':io.BRANCH,'source':io.SOURCE,'expected_final':a.expected_final,'invocations':1,'successes':0,'replays':0,'complete_repository_suite':False,'source_tests_replayed':False,'independent_reproduction':False,'boundary':'Exact owner software and artifact checks only; no independent reproduction, empirical GMUT, production, authority or Stage 20 credit.'}
    def check(name,ok,details=None):
        checks.append({'name':name,'passed':bool(ok),'details':details})
        if not ok:raise ValueError(name)
    try:
        eq=io.equality();check('pushed_clean_four_way_equality',eq['head']==a.expected_final and eq['four_way_equal'] and eq['clean'] and eq['divergence']=='0\t0',eq)
        check('exact_owner_branch',io.git('branch','--show-current').decode().strip()==io.BRANCH)
        history=io.git('rev-list','--reverse','HEAD').decode().splitlines();check('four_commit_blank_root_history',history==[PLAN,X1,X2,a.expected_final],history)
        for i,h in enumerate(history):
            parents=io.git('show','-s','--format=%P',h).decode().strip().split();check('parent_'+str(i),parents==([] if i==0 else [history[i-1]]))
        paths=io.git('ls-tree','-r','--name-only',a.expected_final).decode().splitlines();check('owner_only_paths',all(p.startswith(('docs/ilyan-reed/v689-v8/','scripts/ghc_family_','scripts/build_ghc_family_ilyan_','tests/test_ghc_family_ilyan_')) for p in paths))
        actual=[p for p in io.ROOT.rglob('*') if p.is_file() and p.name!='.git'];check('materialized_exact_owner_inventory',set(io.rel(p) for p in actual)==set(paths));check('file_ceiling',len(paths)<2000 and len(actual)<2000,{'tracked':len(paths),'materialized':len(actual)})
        blobs=dict(zip(paths,io.batch([a.expected_final+':'+p for p in paths])));check('checkout_exact_git_bytes',all((io.ROOT/p).read_bytes()==b for p,b in blobs.items()))
        covered=set();manifest_stats=[]
        for phase,h in zip(['plan','x1','x2','final'],history):
            mp=f'docs/ilyan-reed/v689-v8/{phase}/manifest.json';manifest=json.loads(blobs[mp]);entries=manifest['entries'];at_commit=io.batch([h+':'+r['path'] for r in entries]);check(phase+'_raw_manifest',all(len(b)==r['bytes'] and io.sha(b)==r['sha256'] for r,b in zip(entries,at_commit)))
            check(phase+'_manifest_self_exclusion',manifest['self_exclusions']==[mp]);changes=io.git('diff-tree','--root','--no-commit-id','--name-status','-r',h).decode().splitlines();allow=json.loads(blobs[f'docs/ilyan-reed/v689-v8/{phase}/allowlist.json'])['paths'];check(phase+'_additive_allowlist',all(x.startswith('A\t') for x in changes) and sorted(x[2:] for x in changes)==sorted(allow) and set(allow)=={r['path'] for r in entries}|{mp})
            covered.update(r['path'] for r in entries);manifest_stats.append({'phase':phase,'commit':h,'entries':len(entries)})
        mpaths={f'docs/ilyan-reed/v689-v8/{p}/manifest.json' for p in ['plan','x1','x2','final']};check('lifecycle_manifest_coverage',covered==set(paths)-mpaths)
        seal=io.read('final/content-seal.json');excluded={'docs/ilyan-reed/v689-v8/final/content-seal.json','docs/ilyan-reed/v689-v8/final/manifest.json'};check('content_seal_scope',set(seal['self_exclusions'])==excluded and {r['path'] for r in seal['entries']}==set(paths)-excluded);check('content_seal_raw_bytes',all(len(blobs[r['path']])==r['bytes'] and io.sha(blobs[r['path']])==r['sha256'] for r in seal['entries']))
        review=io.inspect([io.ROOT/p for p in paths]);check('declared_privacy_format_security_checks',review['valid'],review)
        import yaml
        skill_paths=[p for p in paths if p.endswith('/SKILL.md')]
        for p in skill_paths:
            text=blobs[p].decode();meta=yaml.safe_load(text.split('---',2)[1]);check('skill_metadata_'+p,isinstance(meta,dict) and bool(meta.get('name')) and bool(meta.get('description')))
        for p in [p for p in paths if p.endswith('.html')]:
            d=Document();d.feed(blobs[p].decode());check('html_structure_'+p,d.language and 'title' in d.tags and 'main' in d.tags and all(d.images))
        tex=blobs['docs/ilyan-reed/v689-v8/x2/latex/grand_mandala.tex'].decode();check('latex_candidate_structure',tex.count('{')==tex.count('}') and '\\begin{document}' in tex and '\\end{document}' in tex)
        from pypdf import PdfReader
        from PIL import Image
        pdf=PdfReader(str(io.BASE/'final/overview.pdf'));check('pdf_pages_and_text',len(pdf.pages)==5 and all(len(p.extract_text() or '')>500 for p in pdf.pages),{'pages':len(pdf.pages)})
        for p in [p for p in paths if p.endswith('.png')]:
            with Image.open(io.ROOT/p) as im:im.verify()
        check('visual_review_record',io.read('final/visual-review.json')['pdf_pages_inspected']==5)
        image=io.read('x2/image-provenance.json');check('editorial_image_binding',io.sha(blobs['docs/ilyan-reed/v689-v8/'+image['project_path']])==image['sha256'] and image['evidence_role']=='non_evidentiary_editorial_illustration')
        baton=io.read('final/baton-manifest.json');joined='# Ilyan Reed v689-v8 complete handoff to Lyren Moss v690-v1\n\n';check('thirteen_baton_modules',len(baton['modules'])==13)
        for r in baton['modules']:
            b=blobs[r['path']];check('baton_module_'+str(r['number']),io.sha(b)==r['sha256'] and len(b.decode().split())==r['words']);joined+=b.decode()+'\n'
        joined+='EOF ILYAN REED v689-v8 BATON.\n';raw=blobs[baton['combined_path']];check('complete_baton_bytes',raw==joined.encode() and io.sha(raw)==baton['combined_sha256']);check('baton_word_budget',10000<=len(joined.split())<=100000 and len(joined.split())==baton['combined_words'],baton['combined_words'])
        prior=io.read('final/retained/baton-manifest-before-render-recovery.json');reconstructed='# Ilyan Reed v689-v8 complete handoff to Lyren Moss v690-v1\n\n'
        for r in prior['modules']:
            b=blobs['docs/ilyan-reed/v689-v8/final/retained/13-terminal-gates-before-render-recovery.md'] if r['number']==13 else blobs[r['path']];check('prior_baton_module_'+str(r['number']),io.sha(b)==r['sha256']);reconstructed+=b.decode()+'\n'
        reconstructed+='EOF ILYAN REED v689-v8 BATON.\n';check('failed_render_baton_retained',io.sha(reconstructed.encode())==prior['combined_sha256'])
        deck=io.read('x2/deck/deck-index.json');cards=[json.loads(blobs['docs/ilyan-reed/v689-v8/x2/deck/cards/'+cid+'.json']) for cid in deck['order']];by={c['card_id']:c for c in cards};check('deck_unique_cards',len(cards)==len(by)==215)
        check('deck_parent_graph',all((c['tier']==1 and not c['parent_ids']) or (len(c['parent_ids'])==1 and by[c['parent_ids'][0]]['tier']==c['tier']-1) for c in cards));check('deck_tier_counts',Counter(c['tier'] for c in cards)=={1:1,2:3,3:5,4:206})
        dm=io.read('x2/deck/card-manifest.json');dp={p for p in paths if p.startswith('docs/ilyan-reed/v689-v8/x2/deck/')};check('deck_manifest_coverage',{r['path'] for r in dm['entries']}==dp-set(dm['self_exclusions']));check('deck_manifest_hashes',all(io.sha(blobs[r['path']])==r['sha256'] and len(blobs[r['path']])==r['bytes'] for r in dm['entries']))
        proposals=io.read('plan/new-proposals.json')['proposals'];check('new_proposal_inventory',len(proposals)==len({p['proposal_id'] for p in proposals})==200)
        from ghc_family_membership_x1 import evaluate as x1
        from ghc_family_membership_x2 import evaluate as x2
        all_results=[]
        for lane,ev in [('x1',x1),('x2',x2)]:
            results=io.read(lane+'/results.json')['records'];adverse=io.read(lane+'/candidate-subjects.json')['records'];rows=[p for p in proposals if p['lane']==lane];check(lane+'_100_results',len(results)==len(adverse)==len(rows)==100)
            for p,r,c in zip(rows,results,adverse):
                request=copy.deepcopy(p['request']);snapshot=io.canonical(request);response=ev(request);bad=copy.deepcopy(p['candidate_subject']);bad_snapshot=io.canonical(bad);refusal=ev(bad)
                if not (r['proposal_id']==c['proposal_id']==p['proposal_id'] and io.canonical(response)==io.canonical(p['expected'])==io.canonical(r['returned']) and io.canonical(request)==snapshot and io.canonical(refusal)==io.canonical(p['candidate_expected'])==io.canonical(c['returned']) and io.canonical(bad)==bad_snapshot and c['original_success_credit']==0):raise ValueError('Frozen case mismatch '+p['proposal_id'])
            all_results.extend(results);check(lane+'_exact_frozen_cases_and_refusals',True)
        check('core_outcomes',Counter(r['outcome'] for r in all_results)=={'completed':180,'represented':10,'open_gap':5,'exact_gate':5})
        source=io.read('plan/inherited-selections.json')['rows'];refined=[r for lane in ['x1','x2'] for r in io.read(lane+'/refinements.json')['records']];check('inherited_refinement_bindings',len(source)==len(refined)==200 and all(io.sha(io.canonical(s['record']))==s['record_sha256']==r['source_record_sha256'] and io.canonical(s['record'])==io.canonical(r['source_view']) and r['lossless'] and s['novelty_credit']==0 for s,r in zip(source,refined)))
        check('packet_dispositions',len(io.read('plan/exact-packets.json')['packets'])==50 and len(io.read('plan/blocked-packets.json')['packets'])==30 and all(not p['operation_executed'] for n in ['exact','blocked'] for p in io.read('plan/'+n+'-packets.json')['packets']))
        spec=importlib.util.spec_from_file_location('method_flow',a.method_runner);mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf);ledger=io.read('final/effective-method-flow.json');check('effective_method_flow',mf.validate_ledger(ledger)['valid']);check('current_method_counts',ledger['counts']['methods']==27 and ledger['counts']['witnesses']==904 and ledger['counts']['witness_results']=={'fail':214,'pass':690})
        previous=None
        for path in ['x1/method-flow.json','x2/method-flow.json','x2/method-flow-combined.json','final/method-flow.json','final/effective-method-flow.json']:
            current=io.read(path)
            if previous is not None:check('witness_prefix_'+path,current['witnesses'][:len(previous['witnesses'])]==previous['witnesses'])
            previous=current
        negative=io.read('final/effective-negative-index.json');check('negative_index',len(set(negative['current_owner_negative_ids']))==214 and set(negative['current_owner_negative_ids'])=={n for m in ledger['methods'] for n in m['retained_negative_ids']})
        completion=io.read('final/effective-completion-ledger.json');check('additive_source_totals',completion['additive_effective_negatives']==524+214 and completion['additive_direct_witnesses']==669+904 and completion['additive_direct_failed']==235+214 and completion['additive_direct_passed']==434+690)
        check('actual_safe_task_counts',completion['safe_tasks']=={'x1':100,'x2':106} and len(io.read('x2/additional-task-results.json')['records'])==6)
        promotion=io.read('x2/global-promotion.json');skillroot=Path(a.skills_root);check('five_global_packages',len(promotion['records'])==5)
        for r,g in zip(promotion['records'],io.read('plan/skills-runners.json')['global_groups']):
            check('global_bytes_'+g['name'],all(io.sha((skillroot/g['name']/f['path']).read_bytes())==f['sha256']==io.sha(blobs['docs/ilyan-reed/v689-v8/x2/global-skills/'+g['name']+'/'+f['path']]) for f in r['files']))
        runnerroot=Path(a.runner_root);check('global_runner_and_library_bytes',len(promotion['runner_files'])==8 and all(io.sha((runnerroot/r['name']).read_bytes())==r['sha256'] for r in promotion['runner_files']))
        shared=io.read('x2/shared-workflow/installation.json');check('seven_current_entrypoints',len(shared['updates'])==7 and all(io.sha((skillroot/r['skill']/'SKILL.md').read_bytes())==r['after_sha256'] for r in shared['updates']));check('shared_authority_overlay',io.sha((skillroot/'ghc-family-index/references/ilyan-v689-v8-20260910-authority.md').read_bytes())==shared['overlay_sha256'])
        wheels=io.read('x1/toolchain/wheels.json')['wheels'];check('four_exact_wheels',len(wheels)==4 and all(io.sha((Path(a.wheel_root)/w['filename']).read_bytes())==w['sha256'] for w in wheels))
        command='import importlib.metadata as m,json;print(json.dumps({n:m.version(n) for n in ["bitarray","mmh3","xxhash","pip"]},sort_keys=True))';installed=json.loads(subprocess.check_output([a.package_python,'-B','-X','utf8','-c',command],text=True));check('installed_pinned_versions',installed=={r['name']:r['version'] for r in io.read('x1/toolchain/installed.json')['packages']},installed)
        check('source_review_scope',len(io.read('plan/recent-overview-review.json')['records'])==10 and io.read('plan/source-provenance.json')['latest_external_negatives']==524)
        route=io.read('plan/route.json');check('terminal_route_unsubmitted',route['state']=='PREPARED_NOT_SENT' and route['next_owner']=='Lyren Moss' and route['next_phase']=='v690-v1' and route['send_limit']==1)
        env=os.environ.copy();runtime=Path(a.runtime_root);runtime.mkdir(parents=True,exist_ok=True);env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',HYPOTHESIS_STORAGE_DIRECTORY=str(runtime/'hypothesis-cache'))
        testnames=['test_ghc_family_ilyan_v689_v8_'+s+'.py' for s in ['plan','x1','x2','properties']]
        test=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest','-p','hypothesis.extra.pytestplugin','-q','-o','cache_dir='+str(runtime/'canonical-pytest-cache'),*testnames],cwd=io.ROOT/'tests',env=env,capture_output=True,text=True,encoding='utf8')
        out=(test.stdout+test.stderr).replace('\r\n','\n');(dest/'explicit-tests.stdout.txt').write_text(out,encoding='utf8',newline='\n');match=re.search(r'(\d+) passed',out);check('explicit_owner_tests',test.returncode==0 and match is not None and int(match.group(1))==53,{'tests':53,'exit_code':test.returncode,'stdout_sha256':io.sha(out.encode())})
        end=io.equality();check('post_validation_clean_equality',end['four_way_equal'] and end['clean'] and end['head']==a.expected_final and end['divergence']=='0\t0');check('no_owner_caches',not (io.ROOT/'.hypothesis').exists() and not any(p.name=='__pycache__' for p in io.ROOT.rglob('*')))
        report.update(status='VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',successes=1,tracked_files=len(paths),materialized_files=len(actual),history=history,commits=4,merges=0,manifest_entries=sum(r['entries'] for r in manifest_stats),manifests=manifest_stats,content_seal_entries=len(seal['entries']),baton_words=baton['combined_words'],baton_sha256=baton['combined_sha256'],modules=13,pdf_pages=5,owner_tests=53,core_outcomes=completion['core_outcomes'],current_effective_negatives=214,additive_effective_negatives=738,current_direct_witnesses=904,additive_direct_witnesses=1573,route_state='PREPARED_NOT_SENT',terminal_verdict='NOT_READY_FOR_STAGE_20',four_way_equal=True,clean=True,divergence='0/0')
    except Exception as exc:
        report.update(status='INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',error_type=type(exc).__name__,error=str(exc),original_success_credit=0)
    report.update(checks=checks,checks_passed=sum(c['passed'] for c in checks),checks_total=len(checks),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    with receipt.open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
    if report['successes']==1:
        with success.open('x',encoding='utf8',newline='\n') as f:json.dump({'expected_final':a.expected_final,'receipt_sha256':io.sha(receipt.read_bytes()),'invocations':1,'successes':1,'replays':0},f,indent=2);f.write('\n')
    print(json.dumps({k:report[k] for k in ['status','expected_final','invocations','successes','replays','checks_passed','checks_total']},sort_keys=True));raise SystemExit(0 if report['successes']==1 else 1)

if __name__=='__main__':main()
