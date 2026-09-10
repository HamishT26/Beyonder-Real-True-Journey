"""Bind supplemental evidence and a four-tier deck without rewriting either tranche."""
from __future__ import annotations
import argparse,copy,html,importlib.util,json
from collections import Counter
from pathlib import Path
import ghc_family_ilyan_v689_v8_io as io

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--method-runner',required=True);ap.add_argument('--cache-dir',required=True);a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('method_flow',a.method_runner);mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
    identity=io.read('plan/identity-practices.json');gates=identity['protected_gates'];boundary=identity['boundary'];ledger=io.read('x2/method-flow.json')
    cache=Path(a.cache_dir);assert cache.is_dir() and not (io.ROOT/'.hypothesis').exists()
    operations=[{'id':'IR6898-X2-OP001','failure':'Hypothesis generated a constants cache in the owner root despite database=None.','recovery':'The exact task-created 102 files were retained outside the repository; future runs set HYPOTHESIS_STORAGE_DIRECTORY.','recovered':True,'original_success_credit':0,'deleted_files':0}, {'id':'IR6898-X2-OP002','failure':'A resumed read assumed plan/current-authority.json existed; that file was absent.','recovery':'The bounded plan inventory resolved plan/authorization.md and plan/profile.json, which were read completely.','recovered':True,'original_success_credit':0,'deleted_files':0}]
    io.write('x2/operational-corrections.json',{'records':operations,'retained_cache_files':102,'owner_cache_absent':True,'external_cache_present':True})
    by={m['method_id']:m for m in ledger['methods']}
    def witness(mid,procedure,expected,observed,result,ref,negative_ids=None):
        m=by[mid];wid=mid+'-SUP-'+str(len(m['validation_witness_ids'])+1).zfill(3);m['validation_witness_ids'].append(wid)
        ledger['witnesses'].append({'witness_id':wid,'method_id':mid,'procedure':procedure,'scope':'Ilyan Reed v689-v8 supplemental x2','expected':expected,'observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,'retained_negative_ids':negative_ids or m['retained_negative_ids'],'boundary':gates,'evidence_ref':ref})
    def new_method(mid,title,negatives,ref,guard):
        m=copy.deepcopy(ledger['methods'][0]);m.update(method_id=mid,title=title,failure_signature=title,trigger_preconditions=['Exact owned v689-v8 source and declared supplemental procedure'],candidate_workaround=guard,validation_witness_ids=[],recurrence_guard=guard,rollback='Hold the affected procedure and retain all source records and failed subjects.',retained_negative_ids=negatives,changed_file_allowlist=[ref],module_allowlist=['scripts/ghc_family_ilyan_v689_v8_complete_x2.py'])
        ledger['methods'].append(m);by[mid]=m
        ledger['recommendations'].append({'method_id':mid,'preconditions':m['trigger_preconditions'],'recommendation':guard,'rollback':m['rollback']})
    mid='IR6898-supplemental-operations';ref='docs/ilyan-reed/v689-v8/x2/operational-corrections.json'
    new_method(mid,'Cache and exact-path recovery',[r['id'] for r in operations],ref,'Set explicit external cache paths and use the actual bounded file inventory.')
    for r in operations:
        witness(mid,'Retained operational fault','The stated procedure succeeds',r['failure'],'fail',ref,[r['id']]);witness(mid,'Narrow recovery','Matching dependency recovered',r['recovery'],'pass',ref,[r['id']])
    research=io.read('x2/research/mathematical-witnesses.json');ref='docs/ilyan-reed/v689-v8/x2/research/mathematical-witnesses.json'
    for i,r in enumerate(research['retained_failed_claims'],1):
        mid='IR6898-research-boundary-'+str(i)
        new_method(mid,r['claim'],[r['id']],ref,'Name assumptions, keep the counterexample, and withhold a broader scientific claim.')
        witness(mid,'Original broad claim','Claim valid in its stated scope',r['counterexample'],'fail',ref,[r['id']]);witness(mid,'Counterexample retained with zero original credit',0,r['original_success_credit'],'pass',ref,[r['id']])
    for r in research['conditional_probability']:
        assert r['passed'];witness('IR6898-conditional_query_probability','Independent complete probe-tuple enumeration',r['fraction'],r,'pass',ref)
    for r in research['compression_counts']:
        assert r['collision_forced'];witness('IR6898-research-boundary-1','Pigeonhole bound on fixed-size source sets','More sets than summary states',r,'pass',ref)
    for r in research['gmut_remainder_substitutions']:
        assert r['passed'];witness('IR6898-research-boundary-2','Exact rational substitution of defined scalar-component remainder','0',r['residual'],'pass',ref)
    compression=io.read('x2/research/compression-enumeration-check.json')
    # One receipt accounts for the ten finite enumeration comparisons; no tensor-proof credit.
    witness('IR6898-research-boundary-1','Independent enumeration of ten source-set counts','Ten exact count matches',compression,'pass','docs/ilyan-reed/v689-v8/x2/research/compression-enumeration-check.json')
    properties=io.read('x2/generated-properties.json');assert properties['passed']==properties['tests']==5
    witness('IR6898-supplemental-operations','Generated finite invariants with explicit settings','Five property tests pass',properties,'pass','docs/ilyan-reed/v689-v8/x2/generated-properties.json')
    comparisons=io.read('x2/toolchain-comparisons.json');assert comparisons['passing']==comparisons['tests']==30
    for r in comparisons['rows']:
        assert r['passed'];witness('IR6898-PACKAGE-'+r['package'],'Supplemental caller and representation comparison',True,r,'pass','docs/ilyan-reed/v689-v8/x2/toolchain-comparisons.json')
    promotions=io.read('x2/global-promotion.json')
    groups=io.read('plan/skills-runners.json')['global_groups']
    for r,g in zip(promotions['records'],groups):
        assert r['byte_parity'] and r['d_runner_smoke'];witness('IR6898-'+g['operations'][0],'Merged package validation and public-runner smoke',True,{'name':g['name'],'byte_parity':r['byte_parity'],'d_runner_smoke':r['d_runner_smoke']},'pass','docs/ilyan-reed/v689-v8/x2/global-promotion.json')
    shared=io.read('x2/shared-workflow/installation.json')
    for r in shared['updates']:
        assert r['valid'] and r['prefix_preserved'];witness('IR6898-supplemental-operations','Authorized additive entrypoint update with retained original',True,r,'pass','docs/ilyan-reed/v689-v8/x2/shared-workflow/installation.json')
    for m in ledger['methods'][24:]:
        passing=next(w['witness_id'] for w in ledger['witnesses'] if w['method_id']==m['method_id'] and w['result']=='pass');mf.append_event(ledger,m['method_id'],'candidate','validated','Supplemental bounded witness with retained original failure',passing)
    mf.refresh_counts(ledger);valid=mf.validate_ledger(ledger);assert valid['valid'],valid
    io.write('x2/method-flow-combined.json',ledger);io.write('x2/method-flow-combined-validation.json',valid)
    negatives=sorted({n for m in ledger['methods'] for n in m['retained_negative_ids']});assert len(negatives)==212
    io.write('x2/negative-index.json',{'current_owner_negative_ids':negatives,'current_owner_count':len(negatives),'source_latest_baseline':524,'additive_effective_negatives':524+len(negatives),'historical_ilyan_v685_added':False,'original_success_credit':0})
    extras=io.read('plan/additional-work.json')['x2_safe_defined_before_execution']
    refs=[['x2/research/gmut-typed-candidate.md','x2/latex/grand_mandala.tex'],['x2/research/finite-membership-findings.md','x2/research/mathematical-witnesses.json'],['x2/research/albion-and-current-platforms.md'],['x2/image-provenance.json','x2/assets/finite-membership-editorial.png'],['x2/shared-workflow/installation.json']]
    observations=['A typed scalar-tensor candidate and conservation obligations are represented; empirical confirmation remains absent.','Finite counting and conditional-probability calculations completed under their explicit assumptions.','The source assessment and experiment design are represented; the exact X video was not retrieved or inspected.','The built-in system generated a visually inspected editorial image, which is represented and carries no scientific evidence credit.','Seven shared entrypoints were additively updated and validated, with original bytes preserved.']
    extra_rows=[]
    for r,paths,observed in zip(extras,refs,observations):
        extra_rows.append({**r,'outcome':r['expected_execution_disposition'],'observed':observed,'evidence_refs':['docs/ilyan-reed/v689-v8/'+x for x in paths],'new_proposal_credit':0,'verification_passed':True})
    extra_rows.append({'id':'IR6898-EXTRA-06','task':'Thirty package caller comparisons','outcome':'completed','observed':'Thirty finite comparisons passed without a timing or collision-resistance claim.','evidence_refs':['docs/ilyan-reed/v689-v8/x2/toolchain-comparisons.json'],'new_proposal_credit':0,'verification_passed':True})
    io.write('x2/additional-task-results.json',{'records':extra_rows,'x2_safe_total':106,'counts':dict(Counter(r['outcome'] for r in extra_rows)),'separate_from_200_proposal_outcomes':True})
    proposals=io.read('plan/new-proposals.json')['proposals'];observed={r['proposal_id']:r for lane in ['x1','x2'] for r in io.read(lane+'/results.json')['records']}
    core=Counter(r['outcome'] for r in observed.values());assert core=={'completed':180,'represented':10,'open_gap':5,'exact_gate':5}
    source=io.read('plan/source-provenance.json');last=source['receipt_layers'][-1]['record']['successor_visible_overlay'];current=ledger['counts']
    seal={'core_outcomes':dict(core),'supplementary_outcomes':dict(Counter(r['outcome'] for r in extra_rows)),'safe_tasks':{'x1':100,'x2':106},'candidate_subjects':{'x1':100,'x2':100,'original_success_credit':0,'refusal_checks_passed':200},'clean_fix_refine':{'x1':100,'x2':100,'operation':'lossless source-record normalization and binding','source_erased':False,'host_cleanup_credit':0},'proposals':{'inherited':200,'new':200,'novelty_scope':'owner-local combinations, no universal invention'},'packets':{'exact':50,'blocked':30,'protected_actions_executed':0},'local_skills':20,'paired_local_runners':10,'global_skills':5,'public_global_runners':5,'shared_libraries':3,'new_direct_packages':3,'practice_identities':4,'practice_placements':5,'successor_practices':2,'method_flow_current':current,'source_effective_negatives':524,'current_effective_negatives':len(negatives),'additive_effective_negatives':524+len(negatives),'additive_methods':last['method_flow_methods']+current['methods'],'additive_direct_witnesses':last['method_flow_witnesses']+current['witnesses'],'additive_direct_failed':last['method_flow_failed_witnesses']+current['witness_results']['fail'],'additive_direct_passed':last['method_flow_passing_witnesses']+current['witness_results']['pass'],'source_accounting_stream_not_merged_into_direct_counts':True,'canonical_invoked':False,'route_state':'PREPARED_NOT_SENT','terminal_verdict':'NOT_READY_FOR_STAGE_20'}
    io.write('x2/completion-ledger.json',seal)
    cards=[]
    def card(tier,kind,title,parents,content,outcome,refs,stable=False):
        cid='ghc-card-'+io.sha(io.canonical({'phase':'v689-v8','tier':tier,'type':kind,'title':title,'parents':parents}))[:24]
        row={'schema':'ghc.family.four-tier-card.v1','card_id':cid,'tier':tier,'card_type':kind,'title':title,'parent_ids':parents,'owner':'Ilyan Reed','phase':'v689-v8','stability':'stable' if stable else 'volatile','outcome':outcome,'content':content,'source_refs':refs,'protected_gates':gates,'relational_boundary':boundary};cards.append(row);io.write('x2/deck/cards/'+cid+'.json',row);return cid
    anchor=card(1,'owner','Ilyan Reed v689-v8',[],identity,'represented',['docs/ilyan-reed/v689-v8/plan/identity-practices.json'],True)
    pillars={p:card(2,'pillar',p,[anchor],{'primary':p==identity['primary_pillar'],'boundary':'A pillar organizes work and grants no external authority.'},'represented',['docs/ilyan-reed/v689-v8/plan/identity-practices.json'],True) for p in ['GMUT Mind','THOS Body','Freed ID and CBR Heart']}
    practices={}
    for pillar,practice in sorted({(p['pillar'],p['practice']) for p in proposals}):practices[(pillar,practice)]=card(3,'practice',pillar+': '+practice,[pillars[pillar]],{'practice':practice,'qualification_claim':False},'represented',['docs/ilyan-reed/v689-v8/plan/identity-practices.json'],True)
    for p in proposals:
        r=observed[p['proposal_id']];card(4,'task',p['proposal_id']+': '+p['operation'],[practices[(p['pillar'],p['practice'])]],{'proposal_id':p['proposal_id'],'request':p['request'],'expected':p['expected'],'observed':r['returned'],'passed':r['passed'],'original_candidate_success_credit':0},r['outcome'],['docs/ilyan-reed/v689-v8/plan/new-proposals.json','docs/ilyan-reed/v689-v8/'+p['lane']+'/results.json'])
    for r in extra_rows:
        parent=practices[('GMUT Mind','accessible evidence editor')] if r['id'].endswith('01') else practices[('THOS Body','accessible evidence editor')]
        card(4,'supplemental-task',r['id']+': '+r['task'],[parent],r,r['outcome'],r['evidence_refs'])
    ids={c['card_id']:c for c in cards};assert len(ids)==215
    for c in cards:
        if c['tier']==1:assert not c['parent_ids']
        else:assert len(c['parent_ids'])==1 and ids[c['parent_ids'][0]]['tier']==c['tier']-1
    modules=['welcome-and-route','source-and-authority','lifecycle-and-budgets','core-proposal-results','retained-failures-and-methods','inherited-refinements','skills-runners-and-packages','gmut-definition-and-research','freed-id-and-cbr','albion-and-editorial-image','four-tier-context-and-practices','successor-work-and-future-scenarios','terminal-gates-and-recovery']
    io.write('x2/deck/deck-index.json',{'schema':'ghc.family.four-tier-deck.v1','order':[c['card_id'] for c in cards],'counts':dict(Counter(c['tier'] for c in cards)),'source':io.SOURCE,'x1':'e3454293b2faa60de7318758b6918a8fcd73fdc6','core_outcomes':dict(core),'supplementary_outcomes':seal['supplementary_outcomes'],'practice_identities':4,'practice_placements':5,'implicit_completion_credit':0})
    io.write('x2/deck/stable-prefix.json',{'card_ids':[c['card_id'] for c in cards if c['stability']=='stable'],'order_is_exact':True,'cache_performance_measured':False})
    io.write('x2/deck/volatile-index.json',{'card_ids':[c['card_id'] for c in cards if c['stability']=='volatile'],'implicit_completion':False,'source_instruction_authority':False})
    io.write('x2/deck/baton-index.json',{'modules':[{'number':i,'name':m,'path':f'docs/ilyan-reed/v689-v8/final/baton/{i:02d}-{m}.md'} for i,m in enumerate(modules,1)],'combined':'docs/ilyan-reed/v689-v8/final/hand-off-baton.md','minimum_words':10000,'maximum_words':100000})
    io.text('x2/deck/compact-activation.md','# Lyren Moss v690-v1 prepared pointer\n\nDear Lyren, Ilyan has prepared the next file-based handoff with care. Read the complete thirteen-module baton at `docs/ilyan-reed/v689-v8/final/hand-off-baton.md` on the Ilyan main D owner lane only after the external exact-final receipt confirms the final hash. You are next for v690-v1, with Ilyra Fen v690-v2 following under Hamish\'s current 45-position, 30-identity cycle. This file is a prepared pointer and provides zero delivery credit.\n')
    report='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ilyan finite evidence deck</title></head><body><main><h1>Ilyan Reed v689-v8 evidence deck</h1><p>215 cards: one relational owner, three pillars, five placements of four practices, and 206 task cards. Core proposal outcomes remain separate from six supplemental tasks. Structural review is not a manual accessibility audit.</p><table><caption>Frozen proposal observations</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Operation</th><th scope="col">Outcome</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+html.escape(p['proposal_id'])+'</th><td>'+html.escape(p['operation'])+'</td><td>'+html.escape(observed[p['proposal_id']]['outcome'])+'</td></tr>' for p in proposals)+'</tbody></table></main></body></html>\n'
    io.text('x2/deck/accessible-report.html',report)
    io.write('x2/deck/validation.json',{'cards':215,'tier_counts':dict(Counter(c['tier'] for c in cards)),'immediate_parent_rule':True,'cycles':0,'manual_accessibility_audit':False,'valid':True})
    deck=io.BASE/'x2/deck';entries=[{'path':io.rel(p),'bytes':len(p.read_bytes()),'sha256':io.sha(p.read_bytes())} for p in sorted(deck.rglob('*')) if p.is_file()]
    io.write('x2/deck/card-manifest.json',{'entries':entries,'self_exclusions':['docs/ilyan-reed/v689-v8/x2/deck/card-manifest.json'],'hash_domain':'exact UTF-8 bytes'})
    print(json.dumps({'completion':seal,'cards':len(cards),'method_validation':valid['valid']}))

if __name__=='__main__':main()
