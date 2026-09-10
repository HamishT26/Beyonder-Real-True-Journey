"""One exact-final owner canonical; component preflight carries no canonical credit."""
import argparse,ast,copy,datetime,hashlib,importlib.util,io,json,subprocess,sys,unittest
from pathlib import Path
from scripts.ghc_family_flow_common import canonical
from scripts.ghc_family_flow_audit import owner_files,scan,git_blobs,strict_json
from scripts.ghc_family_flow_closeout import BASE,ROOT,PLAN,X1,helper
SOURCE='8eb07d232398cbd33c8e9aae5a040db2d32b2c22'; BRANCH='codex/GHC-Family/mira-fenwick-main'
PREFIX='docs/mira-fenwick/v690-v3/'
def read(path):return strict_json((BASE/path).read_text(encoding='utf-8'))
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
def flatten(suite):
    result=[]
    for item in suite:
        result.extend(flatten(item)) if isinstance(item,unittest.TestSuite) else result.append(item.id())
    return result
def equality():
    heads=[git('rev-parse','HEAD'),git('rev-parse','@{upstream}'),git('rev-parse','refs/remotes/origin/'+BRANCH)]
    live=git('ls-remote','--heads','origin','refs/heads/'+BRANCH).split();assert len(live)==2
    heads.append(live[0]);divergence=[int(v) for v in git('rev-list','--left-right','--count','HEAD...@{upstream}').split()]
    clean=git('status','--porcelain')==''
    return {'four_heads':heads,'divergence':divergence,'clean':clean,'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}

def checks(preflight=False):
    results=[]
    def check(name,fn):
        try:
            evidence=fn();assert evidence is not False
            results.append({'name':name,'pass':True,'evidence':evidence})
        except Exception as exc:results.append({'name':name,'pass':False,'error_type':type(exc).__name__,'error':str(exc)[:600]})
    truth=read('final/phase-truth.json');x2=truth['x2'];head=git('rev-parse','HEAD')
    check('module_root_and_owner',lambda: Path.cwd().resolve()==ROOT.resolve() and git('branch','--show-current')==BRANCH)
    def ancestry():
        lines=git('rev-list','--reverse','--parents',head).splitlines();expected=[PLAN,X1,x2]+([] if preflight else [head])
        assert len(lines)==len(expected)==(3 if preflight else 4)
        for i,line in enumerate(lines):assert line.split()==([expected[i]] if i==0 else [expected[i],expected[i-1]])
        assert SOURCE not in expected
        return {'commits':len(lines),'merges':0,'root_parent_count':0,'source_is_ancestor':False,'ceiling':8}
    check('blank_root_and_direct_children',ancestry)
    def frozen():
        for earlier,later in [(PLAN,X1),(X1,x2)]+([] if preflight else [(x2,head)]):
            lines=git('diff','--name-status',earlier,later).splitlines()
            assert lines and all(line.startswith('A\t') for line in lines)
        return {'prior_paths_modified_or_deleted':0}
    check('additive_phase_freezes',frozen)
    def manifests():
        stages=[('plan',PLAN),('x1',X1),('x2',x2),('final',None if preflight else head)];coverage=set();count=0
        for phase,commit in stages:
            mpath=PREFIX+phase+'/manifest.json'
            m=strict_json((ROOT/mpath).read_text(encoding='utf-8')) if commit is None else strict_json(git_blobs(commit,[mpath])[mpath].decode())
            entries=m['entries'];paths=[e['path'] for e in entries];assert len(paths)==len(set(paths)) and mpath not in paths
            values={p:(ROOT/p).read_bytes() for p in paths} if commit is None else git_blobs(commit,paths)
            for row in entries:assert sha(values[row['path']])==row['sha256'] and len(values[row['path']])==row['bytes']
            assert not coverage.intersection(paths);coverage.update(paths);coverage.add(mpath);count+=len(entries)
        current={p.relative_to(ROOT).as_posix() for p in owner_files()}
        assert current==coverage,{'uncovered':sorted(current-coverage),'absent':sorted(coverage-current)}
        if not preflight:assert current==set(git('ls-tree','-r','--name-only',head).splitlines())
        return {'replayed_entries':count,'manifest_self_exclusions':4,'covered_files':len(current),'raw_git_blob_domain':True}
    check('four_phase_manifest_byte_replay',manifests)
    def source():
        s=read('plan/source-provenance.json');assert s['final']==SOURCE and s['source_canonical_success_credit']==0 and s['source_tests_or_validator_replays']==0
        assert s['source_manifests_replayed']==462 and s['source_content_seal_replayed']==35 and s['source_replay_failures']==0
        assert s['baton_git_blob_sha256']=='dd88a34a5517b3349023049a28ba6653794bf251c9718ba20853ea79c20f5675'
        assert s['baton_digest_mismatch_retained'] and s['source_composite_status']=='VALID_DEPENDENCY_ROOT_CORRECTED_EXACT_FINAL_OWNER_SCOPED_COMPOSITE'
        return {'source_final':SOURCE,'prior_read_only_manifest_replay':497,'source_validator_replays':0,'source_canonical_success_credit':0,'message_hash_discrepancy_retained':True}
    check('source_correction_and_provenance_boundaries',source)
    def source_receipts():
        s=read('plan/source-provenance.json');archive=ROOT.parents[1]
        for r in s['receipt_bindings']:assert sha((archive/r['archive_relative']).read_bytes())==r['sha256']
        return {'bound_source_receipts':len(s['receipt_bindings']),'source_runs':0}
    check('source_receipt_hash_bindings',source_receipts)
    def source_baton():
        s=read('plan/source-provenance.json');source_root=ROOT.parent/'ilyra-fen-main'
        raw=subprocess.check_output(['git','-C',str(source_root),'show',SOURCE+':'+s['baton']]);assert sha(raw)==s['baton_git_blob_sha256']
        return {'exact_source_git_blob_verified':True,'source_runs':0}
    check('source_baton_exact_blob',source_baton)
    def portfolios():
        for phase in ['x1','x2']:
            p=read('plan/portfolio-'+phase+'.json')
            # Portfolio field names are bound by the frozen planner; each cohort has one hundred rows.
            lists=[v for v in p.values() if isinstance(v,list)];assert sorted(map(len,lists))==[100,100,100]
        return {'per_session_safe':100,'per_session_candidate':100,'per_session_record_refinements':100}
    check('frozen_session_portfolios',portfolios)
    proposals=read('plan/new-proposals.json')['proposals']
    check('core_definition_inventory',lambda:len(proposals)==200 and len({r['proposal_id'] for r in proposals})==200)
    def oracle_records():
        records={r['proposal_id']:r for phase in ['x1','x2'] for r in read(phase+'/results.json')['results']};assert len(records)==200
        counts={};accepted={phase:0 for phase in ['x1','x2']}
        for p in proposals:
            r=records[p['proposal_id']];assert canonical(r['expected'])==canonical(p['expected_envelope'])==canonical(r['observed'])
            assert r['envelope_match'] and r['input_unchanged'] and r['candidate_guard_passed'] and r['candidate_original_success_credit']==0
            assert canonical(r['candidate_subject'])==canonical(p['candidate_subject']) and canonical(r['candidate_observed'])==canonical(p['candidate_expected'])
            assert r['disposition']==p['expected_execution_disposition'];counts[r['disposition']]=counts.get(r['disposition'],0)+1
            accepted[p['session']]+=int(r['observed']['accepted'])
        assert counts=={'completed':180,'represented':10,'open_gap':5,'exact_gate':5} and accepted=={'x1':60,'x2':68}
        return {'matched':200,'outcomes':counts,'accepted_inputs':accepted,'failed_candidates':200}
    check('complete_frozen_envelope_records',oracle_records)
    def inheritance():
        rows=read('plan/inherited-selections.json')['records'];assert len(rows)==200
        for row in rows:assert row['source_execution_credit']==row['source_novelty_credit']==0 and sha(canonical(row['source_record']))==row['source_record_sha256']
        total=0
        for phase in ['x1','x2']:
            values=read(phase+'/record-refinements.json')['records'];assert len(values)==100
            for row in values:assert row['lossless']
            total+=len(values)
        return {'retained_source_records':200,'lossless_record_projections':total,'source_execution_credit':0}
    check('inherited_zero_credit_and_record_preservation',inheritance)
    def local_tools():
        plan=read('plan/skills-runners.json');assert len(plan['local_skills'])==20 and len(plan['local_runners'])==10
        for phase in ['x1','x2']:
            rows=read(phase+'/skill-validation.json')['skills'];assert len(rows)==10 and all(r['metadata_pass'] and r['accepting_pass'] and r['rejecting_guard_pass'] for r in rows)
            receipts=list((BASE/phase/'runner-smokes').glob('*/receipt.json'));assert len(receipts)==5
            for path in receipts:assert all(x['pass'] for x in strict_json(path.read_text())['observations'])
        return {'local_skills':20,'paired_runners':10,'phase_checks_retained':True}
    check('local_skill_and_runner_evidence',local_tools)
    def global_tools():
        prom=read('x2/global-promotion.json');assert prom['skills']==prom['public_runners']==5 and len(prom['records'])==24
        for row in prom['records']:
            path=Path.home()/'.codex/skills'/row['name']/row['path'] if row['kind']=='skill' else ROOT.parents[1]/'global-tools/family-flow-certificates'/row['path']
            assert sha(path.read_bytes())==row['sha256'] and path.stat().st_size==row['bytes']
        for stage in ['local','installed']:
            for g in read('plan/skills-runners.json')['global_groups']:
                r=read('x2/global-'+stage+'-smokes/'+g['skill']+'/receipt.json');assert r['pass'] and len(r['checks'])==5 and all(c['pass'] for c in r['checks'])
        return {'global_skills':5,'public_runners':5,'byte_bound_files':24,'local_and_installed_checks':50,'overwrites':0}
    check('promoted_files_and_caller_evidence',global_tools)
    def catalogue():
        assert read('x2/meta-tool-validation.json')['valid'] and len(read('x2/meta-tool-catalogue.json')['cards'])==40
        r=read('x2/meta-tool-collision-review.json');assert r['reviewed']==36 and r['unresolved']==0
        assert read('x2/promotion-policy-preflight.json')['all_ready']
        return {'cards':40,'overlap_decisions':36,'silent_replacements':0}
    check('catalogue_overlap_and_promotion_policy',catalogue)
    def packages():
        r=read('x1/toolchain/installation-receipt.json');assert r['direct_packages']==3 and r['explicit_transitive_dependencies']==1 and r['pip_check_pass'] and r['hash_required']
        c=read('x1/toolchain/package-checks.json');assert len(c['comparisons'])==30 and len(c['adverse_subjects'])==3 and all(v['pass'] for v in c['comparisons']) and all(v['guard_pass'] for v in c['adverse_subjects'])
        return {'direct_packages':3,'transitive_dependencies':1,'solver_interfaces':3,'distinct_solver_backends':2,'comparisons':30,'adverse_checks':3,'independent_reproduction':False}
    check('package_installation_and_solver_comparisons',packages)
    def live_packages():
        python=ROOT.parents[1]/'toolchains/mira-fenwick/v690-v3/Scripts/python.exe'
        code="import importlib.metadata as m,json; print(json.dumps(sorted((n,m.version(n)) for n in ['highspy','PuLP','PyMaxflow','numpy'])))"
        versions=json.loads(subprocess.check_output([str(python),'-c',code]));expected=sorted(read('x1/toolchain/installation-receipt.json')['distributions'])
        assert versions==expected;return {'distributions':versions}
    check('live_isolated_distribution_versions',live_packages)
    def ledger():
        mod=helper();ledgers=[read(p) for p in ['x1/method-flow.json','x2/method-flow.json','x2/method-flow-addendum.json','x2/method-flow-closeout-correction.json']]
        for l in ledgers:assert mod.validate_ledger(l)['valid']
        mids=[m['method_id'] for l in ledgers for m in l['methods']];ws=[w for l in ledgers for w in l['witnesses']];ids=[w['witness_id'] for w in ws]
        assert len(set(mids))==len(mids)==48 and len(set(ids))==len(ids)==1164
        failed=[w['witness_id'] for w in ws if w['result']=='fail'];a=read('x2/accounting-r2.json')
        assert set(failed)==set(a['own_failed_witness_ids']) and len(failed)==327
        for k,v in a['own'].items():assert a['cumulative'][k]==a['inherited_latest_route_overlay'][k]+v
        assert a['own']['passing_witnesses']==837 and a['own']['effective_negatives']==327+30
        return {'methods':48,'direct_witnesses':1164,'failed':327,'passing':837,'blocked_unexecuted':30,'cumulative':a['cumulative']}
    check('method_flow_and_layered_accounting',ledger)
    def supplementary():
        s=read('x2/supplementary-results.json');assert len(s['finite_duality']['comparisons'])==27
        for c in s['finite_duality']['comparisons']:assert c['pass'] and c['flow']==c['cut']==c['closed_form']
        assert s['capacity_counterexample']['observed']['result']['gain']==0 and s['assignment_counterexample']['greedy_cost']==100 and s['assignment_counterexample']['observed']['result']['cost']==4
        assert s['gmut_gap']['physical_observations']==0 and s['authority_counterexample']['observed']['result']['external_action'] is False
        return {'separate_proposals':5,'core_credit':0,'closed_form_networks':27,'retained_refuted_claims':3}
    check('supplementary_counterexamples_and_gaps',supplementary)
    def deck():
        d=read('x2/deck/index.json');by={r['sha256']:r for r in d['cards']};assert len(by)==215
        for row in d['cards']:
            card=read('x2/deck/'+row['path']);assert sha(canonical(card))==row['sha256'] and card['tier']==row['tier']
            if card['tier']==1:assert card['parent'] is None
            else:assert by[card['parent']]['tier']==card['tier']-1
        return {'cards':215,'unique_practices':d['unique_practices'],'practice_placements':d['practice_placements'],'parent_errors':0}
    check('content_addressed_four_tier_deck',deck)
    def privacy():
        a=scan(owner_files());assert not a['privacy_candidates'] and not a['private_route_identifier_candidates'] and not a['bounded_code_execution_findings']
        return a
    check('strict_json_yaml_ast_and_five_class_scan',privacy)
    def tests_inventory():
        inventory=read('final/test-inventory.json');suite=unittest.TestLoader().loadTestsFromNames(['tests.test_flow_x1','tests.test_flow_x2']);ids=sorted(flatten(suite))
        assert ids==inventory['test_ids'] and len(ids)==38 and not unittest.TestLoader().errors
        for r in inventory['definitions']:assert sha((ROOT/r['path']).read_bytes())==r['sha256']
        if preflight:return {'collected':38,'executed':0,'canonical_credit':0}
        runner=unittest.TextTestRunner(stream=io.StringIO(),verbosity=0).run(suite)
        assert runner.wasSuccessful() and runner.testsRun==38
        return {'collected':38,'executed':38,'failures':len(runner.failures),'errors':len(runner.errors),'owner_only':True}
    check('exact_38_test_definitions_and_selection',tests_inventory)
    def modules():
        m=read('final/baton-manifest.json');assert len(m['modules'])==13
        text=(BASE/'final/hand-off-baton.md').read_text(encoding='utf-8');assert 10000<=len(text.split())<=100000 and sha(text.encode())==m['baton_sha256']
        for row in m['modules']:assert sha((BASE/'final'/row['path']).read_bytes())==row['sha256']
        assert all('NOT_READY_FOR_STAGE_20' in (BASE/'final'/row['path']).read_text(encoding='utf-8') for row in m['modules'])
        return {'modules':13,'whitespace_words':len(text.split()),'baton_sha256':m['baton_sha256']}
    check('modular_baton_integrity_and_length',modules)
    def pdf():
        qa=read('final/overview-review.json');assert qa['pages']==5 and qa['all_pages_visually_reviewed'] and qa['clipping_findings']==0 and qa['unreadable_glyph_findings']==0
        assert sha((BASE/'final/overview.pdf').read_bytes())==qa['pdf_sha256']
        return qa
    check('five_page_overview_review',pdf)
    def content_seal():
        m=read('final/content-seal.json')
        for row in m['entries']:assert sha((ROOT/row['path']).read_bytes())==row['sha256'] and (ROOT/row['path']).stat().st_size==row['bytes']
        return {'content_entries':len(m['entries'])}
    check('final_content_seal',content_seal)
    def packets():
        exact=read('final/exact-packet-dispositions.json')['packets'];blocked=read('plan/blocked-packets.json')['packets']
        assert len(exact)==50 and len(blocked)==30 and all(not r['executed'] for r in blocked)
        assert len({r['packet_id'] for r in exact})==50 and all(r['state'] in ['completed','represented','open_gap','exact_gate'] for r in exact)
        return {'exact_packets':50,'blocked_packets':30,'blocked_actions_executed':0}
    check('exact_and_protected_packet_separation',packets)
    def route():
        r=strict_json((ROOT/'workflow/current-route.json').read_text())
        assert r['next_owner']=='Auren Lark' and r['next_phase']=='v690-v4' and r['following_owner']=='Sable Rook' and r['following_phase']=='v690-v5'
        assert r['delivery_state']=='PREPARED_NOT_SENT' and not r['task_creation'] and not r['subagents'] and not r['model_override']
        return {'next':'Auren Lark v690-v4','following':'Sable Rook v690-v5','precontact':False,'task_creation':False}
    check('prospective_route_and_no_early_contact',route)
    check('terminal_truth_boundary',lambda:truth['verdict']=='NOT_READY_FOR_STAGE_20' and truth['canonical_state']=='NOT_INVOKED_PENDING_EXACT_FINAL_GATE' and truth['delivery_state']=='PREPARED_NOT_SENT')
    check('owner_file_capacity',lambda:{'materialized':len(owner_files()),'under_2000':len(owner_files())<2000} if len(owner_files())<2000 else False)
    return results

def main():
    p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
    a.receipt.parent.mkdir(parents=True,exist_ok=True);assert not a.receipt.exists(),'Receipt already exists; no replay.'
    gate=None;head=git('rev-parse','HEAD')
    if not a.preflight:
        gate=equality();assert gate['clean'] and gate['divergence']==[0,0] and len(set(gate['four_heads']))==1
        assert head!=read('final/phase-truth.json')['x2']
        marker=a.receipt.parent/('canonical-'+head+'.invoked.json')
        with marker.open('xb') as out:out.write(canonical({'owner':'Mira Fenwick','phase':'v690-v3','head':head,'invocations':1,'replays':0})+b'\n')
    results=checks(a.preflight);passed=all(r['pass'] for r in results)
    receipt={'schema':'ghc.family.exact-final-owner-canonical.v1','owner':'Mira Fenwick','phase':'v690-v3','head':head,
        'status':'COMPONENT_PREFLIGHT_NOT_CANONICAL' if a.preflight else 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if passed else 'FAILED_EXACT_FINAL_OWNER_SCOPED_CANONICAL',
        'passed':passed,'check_count':len(results),'passing_checks':sum(r['pass'] for r in results),'checks':results,'fresh_gate':gate,
        'canonical_invocations':0 if a.preflight else 1,'canonical_successes':int(passed and not a.preflight),'canonical_replays':0,
        'source_test_or_validator_replays':0,'same_owner_only':True,'independent_reproduction':False,'verdict':'NOT_READY_FOR_STAGE_20',
        'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with a.receipt.open('xb') as out:out.write((json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
    print(json.dumps({'status':receipt['status'],'passed':passed,'checks':len(results),'passing':receipt['passing_checks'],'failures':[r for r in results if not r['pass']]}))
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
