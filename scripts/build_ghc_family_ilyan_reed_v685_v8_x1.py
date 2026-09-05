"""Freeze Ilyan's prospective protocol contracts. This file executes no x2 contract."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/ilyan-reed/v685-v8'
SOURCE='f5464f56d095e9c691707f669668b86ff70468a6'
OWNER='Ilyan Reed'
PHASE='v685-v8'
BOUNDARY='Ilyan Reed, they/them, continuity steward, the hope to make each handoff clearer and easier to verify, family and continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific, operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.'
GATES=['real participants and governed evaluation','GMUT empirical observable likelihood and confirmation','THOS real matched-budget blind arms and independent review','Freed ID production keys proofs lifecycle and trust governance','CBR legal cultural affected-party and Māori authority','complete privacy accessibility exhaustive security independent reproduction','AGI ASI consciousness personhood Theory of Everything canon Stage 20','deployment accounts credentials purchase and destructive or sibling mutation']
PRACTICES=['experimental protocol auditor','event-log data engineer','uncertainty-model reviewer','accessible evidence editor']
FAMILIES=[]

def family(name,runner,op,mission,cases,source,disposition='completed'):
    assert len(cases)==10,(name,len(cases))
    FAMILIES.append(dict(name=name,runner=runner,operation=op,mission=mission,cases=cases,source=source,expected_execution_disposition=disposition))

SIMPY='https://simpy.readthedocs.io/en/stable/topical_guides/time_and_scheduling.html'
FSM='https://github.com/pytransitions/transitions'
CSP='https://python-constraint.github.io/python-constraint/'
STATS='https://docs.python.org/3.12/library/statistics.html'
PROV='https://www.w3.org/TR/prov-o/'
WCAG='https://www.w3.org/TR/WCAG22/'
VC='https://www.w3.org/TR/vc-data-model-2.0/'

# Every expected result below is a prospective, hand-specified oracle. Error results
# are expected refusals, not exceptions suppressed by an outcome collector.
family('event_calendar','trace','schedule','Distinguish deterministic event order from observed concurrency.',[
 ('scrambled insertion is ordered by tick',{'events':[['late',8,0],['early',2,0]]},['early','late']),
 ('equal ticks retain insertion order',{'events':[['first',2,0],['second',2,0]]},['first','second']),
 ('priority resolves a same-tick tie',{'events':[['normal',2,1],['urgent',2,0]]},['urgent','normal']),
 ('priority never moves an event before its tick',{'events':[['later',4,-9],['earlier',1,9]]},['earlier','later']),
 ('an empty calendar yields no fabricated event',{'events':[]},[]),
 ('tick zero is a schedulable boundary',{'events':[['zero',0,0],['one',1,0]]},['zero','one']),
 ('an exclusive horizon omits its endpoint',{'events':[['at',5,0],['before',4,0]],'until':5},['before']),
 ('a future-only calendar is empty at cutoff',{'events':[['future',8,0]],'until':3},[]),
 ('duplicate event labels are refused',{'events':[['dup',1,0],['dup',2,0]]},{'error':'duplicate_event'}),
 ('negative delay is refused before scheduling',{'events':[['past',-1,0]]},{'error':'invalid_tick'})],SIMPY)

family('trial_state_trace','trace','transition','Audit a synthetic trial state trace against its declared transition relation.',[
 ('planned start finish reaches recorded',{'events':['start','finish']},'recorded'),
 ('an untouched trial stays planned',{'events':[]},'planned'),
 ('a started trial stays running until finish',{'events':['start']},'running'),
 ('pause resume preserves a running trial',{'events':['start','pause','resume']},'running'),
 ('pause without resume does not finish',{'events':['start','pause']},'paused'),
 ('cancellation before start is terminal',{'events':['cancel']},'cancelled'),
 ('cancellation after pause is terminal',{'events':['start','pause','cancel']},'cancelled'),
 ('finish before start is refused',{'events':['finish']},{'error':'invalid_transition'}),
 ('a recorded trial cannot restart',{'events':['start','finish','start']},{'error':'invalid_transition'}),
 ('an unknown trigger is refused',{'events':['start','promote']},{'error':'invalid_transition'})],FSM)

family('resource_queue','trace','queue','Explain deterministic queue waiting from synthetic arrivals and service durations.',[
 ('two simultaneous arrivals use FIFO',{'jobs':[['a',0,3],['b',0,2]]},[['a',0,3],['b',3,5]]),
 ('idle gaps do not create waiting time',{'jobs':[['a',0,1],['b',5,2]]},[['a',0,1],['b',5,7]]),
 ('an overlapping arrival waits for release',{'jobs':[['a',0,4],['b',2,1]]},[['a',0,4],['b',4,5]]),
 ('zero service consumes no simulated duration',{'jobs':[['a',0,0],['b',0,2]]},[['a',0,0],['b',0,2]]),
 ('unsorted jobs are normalized by arrival',{'jobs':[['b',4,1],['a',0,2]]},[['a',0,2],['b',4,5]]),
 ('an empty queue performs zero service',{'jobs':[]},[]),
 ('arrival exactly at release starts immediately',{'jobs':[['a',1,3],['b',4,2]]},[['a',1,4],['b',4,6]]),
 ('three queued jobs preserve cumulative waiting',{'jobs':[['a',0,2],['b',1,3],['c',1,1]]},[['a',0,2],['b',2,5],['c',5,6]]),
 ('negative service duration is refused',{'jobs':[['a',0,-1]]},{'error':'invalid_job'}),
 ('repeated job labels are refused',{'jobs':[['a',0,1],['a',2,1]]},{'error':'duplicate_job'})],SIMPY)

family('checkpoint_replay','trace','replay','Keep replayed event identities idempotent and conflicting events visible.',[
 ('a repeated identical event is applied once',{'events':[['e1',2],['e1',2]]},2),
 ('distinct events accumulate in order',{'events':[['e1',2],['e2',3]]},5),
 ('conflicting duplicate payload is refused',{'events':[['e1',2],['e1',3]]},{'error':'conflicting_replay'}),
 ('checkpoint state is the initial accumulator',{'initial':7,'events':[['e1',2]]},9),
 ('empty replay preserves the checkpoint',{'initial':7,'events':[]},7),
 ('a negative delta is retained as a correction',{'events':[['e1',5],['e2',-2]]},3),
 ('zero delta remains a distinct event',{'events':[['zero',0],['one',1]]},1),
 ('nonadjacent duplicate does not accumulate twice',{'events':[['a',2],['b',3],['a',2]]},5),
 ('an already seen checkpoint event is ignored',{'initial':4,'seen':{'a':4},'events':[['a',4],['b',2]]},6),
 ('checkpoint conflict refuses the entire replay',{'initial':4,'seen':{'a':4},'events':[['a',5]]},{'error':'conflicting_replay'})],PROV)

family('matched_resource_budget','budget','budget','Compute resource totals before deciding whether an offline comparison matches its cap.',[
 ('equal arm totals match within the cap',{'arms':[[2,3],[1,4]],'cap':5},{'totals':[5,5],'matched':True,'within_cap':True}),
 ('unequal totals remain unmatched',{'arms':[[2,3],[2,2]],'cap':5},{'totals':[5,4],'matched':False,'within_cap':True}),
 ('matched overspend still violates the cap',{'arms':[[3,3],[2,4]],'cap':5},{'totals':[6,6],'matched':True,'within_cap':False}),
 ('empty arm totals are zero',{'arms':[[],[]],'cap':0},{'totals':[0,0],'matched':True,'within_cap':True}),
 ('one arm cannot establish a matched comparison',{'arms':[[1]],'cap':2},{'error':'two_arms_required'}),
 ('negative cost cannot conceal consumption',{'arms':[[4,-1],[3]],'cap':3},{'error':'nonnegative_integer_required'}),
 ('boolean cost cannot masquerade as one token',{'arms':[[True],[1]],'cap':2},{'error':'nonnegative_integer_required'}),
 ('exact cap equality is permitted',{'arms':[[7],[7]],'cap':7},{'totals':[7,7],'matched':True,'within_cap':True}),
 ('uneven granularity does not change total comparison',{'arms':[[1,1,1,1],[4]],'cap':4},{'totals':[4,4],'matched':True,'within_cap':True}),
 ('an overspent single arm blocks budget acceptance',{'arms':[[5],[3]],'cap':4},{'totals':[5,3],'matched':False,'within_cap':False})],CSP)

family('allocation_balance','budget','allocation','Expose arm balance and sequence gaps without claiming randomization or blinding.',[
 ('an alternating allocation is balanced',{'sequence':['A','B','A','B']},{'A':2,'B':2,'imbalance':0}),
 ('one extra A is explicitly imbalanced',{'sequence':['A','B','A']},{'A':2,'B':1,'imbalance':1}),
 ('an empty allocation reports zero assignments',{'sequence':[]},{'A':0,'B':0,'imbalance':0}),
 ('all-A allocation reports its full imbalance',{'sequence':['A','A','A']},{'A':3,'B':0,'imbalance':3}),
 ('all-B allocation reports its full imbalance',{'sequence':['B','B']},{'A':0,'B':2,'imbalance':2}),
 ('blocked ordering can still have balanced totals',{'sequence':['A','A','B','B']},{'A':2,'B':2,'imbalance':0}),
 ('unknown arm label is refused',{'sequence':['A','C']},{'error':'unknown_arm'}),
 ('a missing assignment is not silently dropped',{'sequence':['A',None]},{'error':'unknown_arm'}),
 ('case drift is not an arm alias',{'sequence':['a','B']},{'error':'unknown_arm'}),
 ('equal counts do not supply a randomness test',{'sequence':['B','A','A','B','B','A']},{'A':3,'B':3,'imbalance':0})],CSP)

family('masking_separation','budget','separation','Detect overlap between synthetic evaluator and allocation-key access sets.',[
 ('disjoint evaluator and key-holder sets remain separated',{'evaluators':['e1'],'key_holders':['k1']},[]),
 ('a shared evaluator is reported',{'evaluators':['e1','e2'],'key_holders':['e2']},['e2']),
 ('multiple overlaps are sorted reproducibly',{'evaluators':['z','a'],'key_holders':['z','a']},['a','z']),
 ('no assigned evaluator supplies no overlap evidence',{'evaluators':[],'key_holders':['k1']},[]),
 ('no key holder leaves the relation empty',{'evaluators':['e1'],'key_holders':[]},[]),
 ('duplicate evaluator entry is refused',{'evaluators':['e1','e1'],'key_holders':[]},{'error':'duplicate_role_member'}),
 ('duplicate key-holder entry is refused',{'evaluators':[],'key_holders':['k1','k1']},{'error':'duplicate_role_member'}),
 ('role aliases are not resolved implicitly',{'evaluators':['E1'],'key_holders':['e1']},[]),
 ('unassigned roles stay visibly vacant',{'evaluators':[],'key_holders':[]},[]),
 ('partial overlap does not clear the remaining conflict',{'evaluators':['e1','e2','e3'],'key_holders':['e1','e3','k']},['e1','e3'])],PROV)

family('missingness_denominator','budget','denominator','Count every planned row in exactly one declared disposition before reporting a denominator.',[
 ('observed and missing rows both remain in the denominator',{'rows':['observed','missing']},{'total':2,'observed':1,'missing':1,'excluded':0}),
 ('exclusions remain explicit',{'rows':['observed','excluded']},{'total':2,'observed':1,'missing':0,'excluded':1}),
 ('empty planned cohort reports zero rows',{'rows':[]},{'total':0,'observed':0,'missing':0,'excluded':0}),
 ('all-missing data never becomes an observed cohort',{'rows':['missing','missing']},{'total':2,'observed':0,'missing':2,'excluded':0}),
 ('all-excluded rows remain countable',{'rows':['excluded','excluded']},{'total':2,'observed':0,'missing':0,'excluded':2}),
 ('all-observed fixture retains full count',{'rows':['observed','observed','observed']},{'total':3,'observed':3,'missing':0,'excluded':0}),
 ('unknown disposition is refused',{'rows':['lost']},{'error':'unknown_disposition'}),
 ('null disposition is not imputed',{'rows':[None]},{'error':'unknown_disposition'}),
 ('mixed dispositions sum to the planned total',{'rows':['observed','missing','excluded','observed']},{'total':4,'observed':2,'missing':1,'excluded':1}),
 ('case changes do not alter the disposition vocabulary',{'rows':['Observed']},{'error':'unknown_disposition'})],STATS)

family('exact_summary_statistics','analysis','summary','Calculate exact rational summaries of wholly invented values with empty-data refusal.',[
 ('odd sample median is an observed fixture member',{'values':[1,3,5],'stat':'median'},'3'),
 ('even median is the exact middle-pair mean',{'values':[1,3,5,7],'stat':'median'},'4'),
 ('fractional mean retains its denominator',{'values':[1,2,2],'stat':'mean'},'5/3'),
 ('signed values retain cancellation',{'values':[-2,0,2],'stat':'mean'},'0'),
 ('sample variance uses n minus one',{'values':[1,2,3],'stat':'sample_variance'},'1'),
 ('population variance uses n',{'values':[1,2,3],'stat':'population_variance'},'2/3'),
 ('empty mean is refused',{'values':[],'stat':'mean'},{'error':'insufficient_data'}),
 ('singleton sample variance is refused',{'values':[3],'stat':'sample_variance'},{'error':'insufficient_data'}),
 ('singleton population variance is zero',{'values':[3],'stat':'population_variance'},'0'),
 ('an outlier changes the mean without changing the median',{'values':[1,2,99],'stat':'median'},'2')],STATS)

family('paired_result_alignment','analysis','paired','Match synthetic pair labels before computing a directionally defined A-minus-B difference.',[
 ('aligned pair labels yield A-minus-B differences',{'a':[['p1',4],['p2',7]],'b':[['p1',1],['p2',5]]},[['p1','3'],['p2','2']]),
 ('reordered B rows align by label',{'a':[['p1',4],['p2',7]],'b':[['p2',5],['p1',1]]},[['p1','3'],['p2','2']]),
 ('unpaired A label refuses silent dropping',{'a':[['p1',4]],'b':[]},{'error':'pair_set_mismatch'}),
 ('unpaired B label refuses silent expansion',{'a':[],'b':[['p1',1]]},{'error':'pair_set_mismatch'}),
 ('duplicate A labels are refused',{'a':[['p1',1],['p1',2]],'b':[['p1',1]]},{'error':'duplicate_pair'}),
 ('duplicate B labels are refused',{'a':[['p1',1]],'b':[['p1',1],['p1',2]]},{'error':'duplicate_pair'}),
 ('negative difference retains its sign',{'a':[['p1',1]],'b':[['p1',4]]},[['p1','-3']]),
 ('zero difference is retained',{'a':[['p1',4]],'b':[['p1',4]]},[['p1','0']]),
 ('empty pair sets produce zero comparisons',{'a':[],'b':[]},[]),
 ('A input order defines the output order',{'a':[['p2',5],['p1',2]],'b':[['p1',1],['p2',3]]},[['p2','2'],['p1','1']])],STATS)

family('histogram_boundaries','analysis','histogram','Preserve lower-inclusive upper-exclusive binning with an explicitly inclusive final edge.',[
 ('interior values fall into their declared bins',{'values':[1,3],'edges':[0,2,4]},[1,1]),
 ('an interior boundary belongs to the following bin',{'values':[2],'edges':[0,2,4]},[0,1]),
 ('the first edge is included',{'values':[0],'edges':[0,2,4]},[1,0]),
 ('the last edge is included once',{'values':[4],'edges':[0,2,4]},[0,1]),
 ('out-of-range values are refused',{'values':[-1],'edges':[0,2,4]},{'error':'outside_edges'}),
 ('repeated edges are refused',{'values':[1],'edges':[0,2,2]},{'error':'invalid_edges'}),
 ('descending edges are refused',{'values':[1],'edges':[4,2,0]},{'error':'invalid_edges'}),
 ('empty values retain zero-count bins',{'values':[],'edges':[0,2,4]},[0,0]),
 ('one bin retains both endpoints',{'values':[0,1,2],'edges':[0,2]},[3]),
 ('irregular widths do not imply density normalization',{'values':[0,1,2,3,4],'edges':[0,1,4]},[1,4])],STATS)

family('preregistered_stopping','analysis','stop','Classify stop triggers by a frozen precedence relation without optional result-dependent peeking.',[
 ('safety flag stops before resource accounting',{'safety':True,'spent':1,'cap':5,'done':False},'safety_stop'),
 ('exhausted cap stops an unfinished run',{'safety':False,'spent':5,'cap':5,'done':False},'budget_stop'),
 ('a completed run is recorded below its cap',{'safety':False,'spent':4,'cap':5,'done':True},'record'),
 ('an unfinished below-cap run continues',{'safety':False,'spent':4,'cap':5,'done':False},'continue'),
 ('safety dominates simultaneous completion',{'safety':True,'spent':4,'cap':5,'done':True},'safety_stop'),
 ('budget dominates simultaneous completion',{'safety':False,'spent':5,'cap':5,'done':True},'budget_stop'),
 ('overspend is retained as budget stop',{'safety':False,'spent':6,'cap':5,'done':False},'budget_stop'),
 ('zero cap stops before the first unit',{'safety':False,'spent':0,'cap':0,'done':False},'budget_stop'),
 ('negative resource count is refused',{'safety':False,'spent':-1,'cap':5,'done':False},{'error':'invalid_budget'}),
 ('unregistered result peeking is refused',{'safety':False,'spent':1,'cap':5,'done':False,'peek':True},{'error':'unregistered_peek'})],STATS)

family('derivation_graph','provenance','lineage','Resolve a finite provenance DAG while retaining missing parents and cycles as failures.',[
 ('a single source has a one-node order',{'nodes':['a'],'edges':[]},['a']),
 ('direct derivation puts source before report',{'nodes':['a','b'],'edges':[['a','b']]},['a','b']),
 ('diamond derivation preserves both branches',{'nodes':['a','b','c','d'],'edges':[['a','b'],['a','c'],['b','d'],['c','d']]},['a','b','c','d']),
 ('a self-cycle is refused',{'nodes':['a'],'edges':[['a','a']]},{'error':'cycle'}),
 ('a two-node cycle is refused',{'nodes':['a','b'],'edges':[['a','b'],['b','a']]},{'error':'cycle'}),
 ('unknown parent cannot be invented',{'nodes':['b'],'edges':[['a','b']]},{'error':'missing_node'}),
 ('unknown child cannot be invented',{'nodes':['a'],'edges':[['a','b']]},{'error':'missing_node'}),
 ('duplicate nodes are refused',{'nodes':['a','a'],'edges':[]},{'error':'duplicate_node'}),
 ('disconnected components receive deterministic ordering',{'nodes':['z','a'],'edges':[]},['a','z']),
 ('an empty graph supplies no lineage',{'nodes':[],'edges':[]},[])],PROV)

family('byte_domain_fixity','provenance','fixity','Compare declared text domains without making content hashes into identity or authorization.',[
 ('identical UTF-8 text has equal bytes',{'left':'alpha','right':'alpha','domain':'utf8'},True),
 ('case changes alter UTF-8 bytes',{'left':'alpha','right':'Alpha','domain':'utf8'},False),
 ('raw line endings remain distinct',{'left':'a\r\nb','right':'a\nb','domain':'utf8'},False),
 ('normalized-LF domain resolves CRLF',{'left':'a\r\nb','right':'a\nb','domain':'normalized_lf_utf8'},True),
 ('a final newline remains significant',{'left':'a','right':'a\n','domain':'normalized_lf_utf8'},False),
 ('empty strings compare without fabricated content',{'left':'','right':'','domain':'utf8'},True),
 ('composed and decomposed Unicode remain distinct',{'left':'é','right':'e\u0301','domain':'utf8'},False),
 ('whitespace is not silently trimmed',{'left':'a ','right':'a','domain':'utf8'},False),
 ('unknown byte domain is refused',{'left':'a','right':'a','domain':'implicit'},{'error':'unknown_domain'}),
 ('lone CR is preserved by the declared LF conversion',{'left':'a\rb','right':'a\nb','domain':'normalized_lf_utf8'},False)],PROV)

family('immutable_correction_merge','provenance','merge','Merge synthetic records only where identical labels retain identical payloads.',[
 ('disjoint records merge additively',{'left':{'a':1},'right':{'b':2}},{'a':1,'b':2}),
 ('identical repeated content is idempotent',{'left':{'a':1},'right':{'a':1}},{'a':1}),
 ('conflicting payload remains quarantined',{'left':{'a':1},'right':{'a':2}},{'error':'conflict'}),
 ('an empty incoming set preserves history',{'left':{'a':1},'right':{}},{'a':1}),
 ('an empty history accepts the incoming set',{'left':{},'right':{'b':2}},{'b':2}),
 ('two empty sets remain empty',{'left':{},'right':{}},{}),
 ('nested record equality is deterministic',{'left':{'a':{'x':1,'y':2}},'right':{'a':{'y':2,'x':1}}},{'a':{'x':1,'y':2}}),
 ('boolean and integer payloads do not coalesce',{'left':{'a':True},'right':{'a':1}},{'error':'conflict'}),
 ('a null tombstone does not erase old content',{'left':{'a':1},'right':{'a':None}},{'error':'conflict'}),
 ('same text with different case is a conflict',{'left':{'a':'value'},'right':{'a':'Value'}},{'error':'conflict'})],PROV)

family('minimal_public_projection','export','export','Project an explicit field allowlist and refuse absent required fields in a synthetic report.',[
 ('allowlist discards an unrelated note',{'record':{'title':'trial','note':'synthetic'},'allow':['title'],'required':['title']},{'title':'trial'}),
 ('a required absent title refuses export',{'record':{'note':'synthetic'},'allow':['title'],'required':['title']},{'error':'missing_required'}),
 ('an optional absent field stays absent',{'record':{'title':'trial'},'allow':['title','summary'],'required':['title']},{'title':'trial'}),
 ('empty explicit projection produces an empty object',{'record':{'title':'trial'},'allow':[],'required':[]},{}),
 ('required fields must appear in the allowlist',{'record':{'title':'trial'},'allow':[],'required':['title']},{'error':'required_not_allowed'}),
 ('zero remains a valid declared count',{'record':{'count':0},'allow':['count'],'required':['count']},{'count':0}),
 ('null remains explicit rather than inferred',{'record':{'measure':None},'allow':['measure'],'required':['measure']},{'measure':None}),
 ('duplicate allowed fields are refused',{'record':{'title':'trial'},'allow':['title','title'],'required':[]},{'error':'duplicate_allowlist'}),
 ('top-level export does not flatten nested provenance',{'record':{'source':{'label':'synthetic'}},'allow':['source'],'required':['source']},{'source':{'label':'synthetic'}}),
 ('field-name case is preserved',{'record':{'Title':'trial'},'allow':['title'],'required':['title']},{'error':'missing_required'})],VC)

family('accessible_evidence_table','export','table','Validate structural table relations while reserving browser and affected-user accessibility review.',[
 ('rectangular rows have a matching header count',{'headers':['claim','state'],'rows':[['a','open_gap']]},True),
 ('a short row fails rectangularity',{'headers':['claim','state'],'rows':[['a']]},False),
 ('a long row fails rectangularity',{'headers':['claim'],'rows':[['a','b']]},False),
 ('duplicate headers do not identify columns uniquely',{'headers':['claim','claim'],'rows':[['a','b']]},False),
 ('a vacant header is not a column description',{'headers':[''],'rows':[['a']]},False),
 ('a header-only table explicitly has zero rows',{'headers':['claim'],'rows':[]},True),
 ('a table with no headers is refused',{'headers':[],'rows':[]},False),
 ('visible unknown text remains a valid cell',{'headers':['value'],'rows':[['unknown']]},True),
 ('blank cell text is not silently inferred',{'headers':['value'],'rows':[['']]},False),
 ('numeric zero can be rendered as an explicit cell',{'headers':['value'],'rows':[['0']]},True)],WCAG)

for name,disposition,labels,src in [
 ('governed_trial_vacancies','represented',['allocation concealment custodian','independent safety monitor','real operator recruitment','blind matched-budget comparator','prospective ethics assessment','real adverse-event process','preregistered empirical outcome','participant withdrawal mechanism','independent protocol review','real environment description'],PROV),
 ('gmut_observation_obligations','open_gap',['clock-to-observable map','field-to-event likelihood','dimensioned resource coupling','identifiable latent parameter','finite-resolution discrepancy term','boundary-condition specification','measurement-error covariance','external empirical dataset','independent rival-model comparison','unique falsifiable physical prediction'],STATS),
 ('cbr_authority_reservations','exact_gate',['affected-person consent determination','legitimate access controller','contested rights resolution','legal publication permission','cultural description ratification','Māori wording review','Māori data-governance relationship','tangata whenua authority','iwi and hapū decision','competent remedy determination'],VC)]:
    family(name,'export','reservation','Keep an individually named prerequisite unresolved despite a valid local record.',[(label,{'obligation':label,'evidence':None,'authority':None,'disposition':disposition},disposition) for label in labels],src,disposition)

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(value,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n')

def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--package-metadata',required=True);a=ap.parse_args()
    assert git('rev-parse','HEAD').decode().strip()==SOURCE
    prior=json.loads(git('show',SOURCE+':docs/elaren-kestrel/v685-v7/x1/new-proposals.json'))
    prior_rows=prior if isinstance(prior,list) else prior.get('proposals',prior.get('rows',[]))
    assert len(prior_rows)==200, list(prior) if isinstance(prior,dict) else len(prior_rows)
    inherited=[{'source_commit':SOURCE,'source_path':'docs/elaren-kestrel/v685-v7/x1/new-proposals.json','source_record':r,'source_record_sha256':digest(r),'novelty_credit':0,'execution_credit':0} for r in prior_rows]
    proposals=[]
    for fi,f in enumerate(FAMILIES):
        for title,data,expected in f['cases']:
            pid=f'IR6858-N{len(proposals)+1:03d}'
            proposals.append({'proposal_id':pid,'family':f['name'],'runner':f['runner'],'operation':f['operation'],'title':title,'mission':f['mission'],'practice':PRACTICES[min(fi//5,3)],'pillar':'GMUT Mind' if fi==18 else 'Freed ID and CBR Heart' if fi==19 else 'THOS Body','source_refs':[f['source']],'source_status':'current' if f['source'] in [SIMPY,FSM,CSP,STATS] else 'stable','hypothesis':'The named offline relation yields the preregistered result for this exact synthetic input and rejects a fabricated report.','null_or_failure':'Computed result differs, fabricated result is accepted, input is mutated, or evidence is promoted outside the named scope.','falsifier':'Compare canonical JSON of computed and reported values, including exact types; reject each of five preregistered mutations.','rollback':'Quarantine this proposal and preserve its original input, expected result, failed witness, and any separately attributable correction.','expected_execution_disposition':f['expected_execution_disposition'],'approval_class':'safe_now' if fi<17 else 'candidate','lane':'x2_build_task','input':data,'expected_result':expected,'preregistered_mutations':['fabricated_report','stale_definition_digest','phase_epoch_inversion','empirical_promotion','authority_promotion'],'protected_gates':GATES})
    assert len(proposals)==200
    profile=json.loads(git('show',SOURCE+':docs/elaren-kestrel/v685-v7/x1/workflow-profile.json'))
    dump(BASE/'x1/workflow-profile.json',profile)
    dump(BASE/'x1/inherited-selection.json',{'schema':'ghc.family.ilyan.inherited.v1','rows':inherited})
    dump(BASE/'x1/new-proposals.json',{'schema':'ghc.family.ilyan.proposals.v1','planning_only':True,'proposals':proposals})
    plans={}
    for name,count,action in [('safe_now',300,'evaluate_report' ),('candidates',250,'alternate_serialization_review'),('clean_fix_refine',300,'additive_projection'),('exact_packets',50,'preserve_exact_prerequisite'),('blocked_packets',30,'preserve_missing_evidence')]:
        rows=[]
        for i in range(count):
            p=proposals[i%200];r={'packet_id':f'IR6858-{name.upper()}-{i+1:03d}','proposal_id':p['proposal_id'],'action':action,'title':p['title'],'expected_execution_disposition':'exact_gate' if name=='exact_packets' else 'open_gap' if name=='blocked_packets' else p['expected_execution_disposition'],'lane':'x2_build_task','execution_credit':0}
            if name=='safe_now' and i>=200:r['action']='verify_roundtrip_and_input_nonmutation'
            if name=='candidates':r['action']='review_sorted_serialization' if i<200 else 'review_missing_definition_refusal'
            if name=='clean_fix_refine':r.update(category=['CLEAN','FIX','REFINE'][i//100],action=['allowlist_projection','retain_and_correct_false_report','derive_readable_protocol_explanation'][i//100])
            if name in ['exact_packets','blocked_packets']:
                obligation=proposals[170+(i%30)];r.update(proposal_id=obligation['proposal_id'],title=obligation['title'],required_evidence=('competent action-specific authority and exact target' if name=='exact_packets' else 'preregistered observation and independent review'),operation_executed=False)
            if name=='exact_packets':
                q=proposals[190+i%10];surface=['proposed wording','future collection scope','contested amendment','public export scope','retention and remedy'][i//10]
                r.update(proposal_id=q['proposal_id'],title=q['title']+' for '+surface,exact_target_class=surface)
            if name=='blocked_packets':
                q=proposals[170+i%10];surface=['protocol preparation','future execution','independent evaluation'][i//10]
                r.update(proposal_id=q['proposal_id'],title=q['title']+' during '+surface,missing_evidence_context=surface)
            rows.append(r)
        plans[name]=rows
    dump(BASE/'x1/portfolio-plan.json',{'schema':'ghc.family.ilyan.portfolio.v1','planning_only':True,**plans})
    skills=[{'name':'ghc-family-protocol-'+f['name'].replace('_','-'),'family':f['name'],'mission':f['mission'],'source_refs':[f['source']],'runner':'ghc_family_protocol_'+f['runner']+'.py'} for f in FAMILIES]
    next_skills=[{'name':s['name']+'-review','purpose':'Challenge '+s['mission'].lower(),'evidence_needed':'A new counterexample or materially different caller; no automatic build credit.'} for s in skills[:10]]
    next_runners=[{'idea':n,'boundary':'Prospective owner-local software work only; no real-world authority.'} for n in ['trace watermark validator','counterbalanced assignment auditor','censoring reason classifier','rational unit conversion auditor','sequential-look budget ledger','snapshot epoch comparator','event causality explanation','missingness export checker','role-access relation reviewer','protocol amendment comparator']]
    dump(BASE/'x1/skill-runner-plan.json',{'skills':skills,'runners':[{'name':'ghc_family_protocol_'+n+'.py','families':[f['name'] for f in FAMILIES if f['runner']==n]} for n in ['trace','budget','analysis','provenance','export']],'promotion_pairs':[[skills[i]['name'],skills[i+1]['name']] for i in range(0,20,2)],'next_owner_skills':next_skills,'next_owner_runners':next_runners})
    dump(BASE/'x1/identity-and-practice.json',{'owner':OWNER,'phase':PHASE,'pronouns':'they/them','role':'continuity steward','hope':'to make each handoff clearer and easier to verify','identity_boundary':BOUNDARY,'priority_pillar':'THOS Body','practices':PRACTICES,'next_practice_recommendation':'data-quality investigator','protected_gates':GATES})
    pkgs=json.loads(Path(a.package_metadata).read_text(encoding='utf8'))
    dump(BASE/'x1/package-plan.json',{'direct_additions':3,'packages':pkgs,'install_after_x1_equality':True,'wheel_only':True,'require_hashes':True,'expected_runtime_dependencies':['six'],'bootstrap':'hash-verified pip in isolated D environment','rollback_token':'IR6858-TOOLS-01','rollback':'Retain the isolated environment and receipts; select a prior environment. No deletion, system Python, PATH, npm prefix, or sibling environment mutation.','smokes':{'simpy':['FIFO at equal time','negative timeout refusal'],'transitions':['planned-running-recorded','finish before start refusal'],'python-constraint2':['finite distinct assignments sum to four','inconsistent singleton domains have zero solutions']}})
    repository={'effective_negatives':64405,'effective_methods':80970,'failed_witnesses':35253,'bounded_passing_witnesses':62815,'open_gaps':582,'exact_gates':569}
    baseline={k:v+(5 if k not in ['open_gaps','exact_gates'] else 0) for k,v in repository.items()}
    latest={k:v+(2 if k not in ['open_gaps','exact_gates'] else 0) for k,v in baseline.items()}
    dump(BASE/'x1/activation-source.json',{'source':SOURCE,'source_branch':'codex/GHC-Family/elaren-kestrel-v685-v7-full-tools','source_x1':'0902e28aa1006b44a247e3d480797a4472bc1e58','source_evidence':'0eba230431e652b9907edb5e86f11924d32c1d1d','source_terminal_state':'VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT','source_canonical_success_credit':0,'canonical_receipt_sha256':'be838dd58bf26f87b5153392bdb9dd7721fdebba991dbca501f6c92acf6ecc99','recovery_receipt_sha256':'c473954e1a22bb0dd92e80c51d53a76b5ce74db4c85928eb407c222705c15457','composite_receipt_sha256':'efa655311c8e5368fea9559f1810369aec20f2023a13a8281f87b94f705bd0d5','repository_seal':repository,'initial_activation_overlay_count':5,'initial_activation_baseline':baseline,'later_source_report_overlay_count':2,'later_source_report_events':['creation-result outer-text parser','progress summary selected a completed tool marker instead of active turn'],'latest_source_working_baseline':latest,'source_aggregate_replayed':False,'source_manifest_entries_reverified':914,'source_manifest_failures':0,'source_four_way_equal':True,'source_clean':True,'main_task_creation':'This activation created exactly one main task; its current title is Ilyan Reed. Later source report confirms ready acknowledgement and no duplicate creation.','induction_read':{'lines':2913,'words':37724,'sections':13,'worktree_sha256':'3acdfb0a2317cffe8cc24c3369c5b22d50b256e0d7c0a43e2c7579be26bd193a','method':'Full text read through EOF, lossless factoring of all 200 repeated appendix blocks with exact reconstruction, untruncated recovery reads for hidden output.'}})
    dump(BASE/'x1/route-plan.json',{'owner':OWNER,'phase':PHASE,'endpoint_kind':'main_task','seat':2,'main_task_reused_on_future_cycles':True,'next_owner':'Neris Solane','next_phase':'v686-v1','next_endpoint_kind':'main_task','next_creates_seat':3,'next_new_seat_phase':'v686-v2','delivery_state':'PREPARED_NOT_SENT','terminal_gate_required':True,'send_count':0,'creation_count_this_task':0,'subagents':0,'horizon':'v725-v8','reset_redemption_authorized':False})
    dump(BASE/'x1/phase-truth.json',{'owner':OWNER,'phase':PHASE,'source':SOURCE,'state':'PLANNING_ONLY','expected_outcomes':{'completed':170,'represented':10,'open_gap':10,'exact_gate':10},'x2_execution_started':False,'declared_proposal_chain_before':12030,'declared_proposal_chain_after_if_executed':12230,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    # Bounded title screening is advisory; different wording never establishes
    # universal novelty. Compare mission/falsifier/input semantics in family review.
    old=[]
    for r in prior_rows:old.append((r.get('proposal_id',r.get('id','unknown')),r.get('title','')))
    tok=lambda s:set(re.findall(r'[a-z0-9]+',s.lower()))
    comparisons=[]
    for p in proposals:
        t=tok(p['title']);rank=[]
        for pid,title in old:
            u=tok(title);rank.append((len(t&u)/len(t|u) if t|u else 1,pid,title))
        score,pid,title=max(rank)
        comparisons.append({'proposal_id':p['proposal_id'],'nearest_inherited':pid,'nearest_title':title,'jaccard':score,'exact_collision':p['title'].lower()==title.lower(),'quarantine':score>=0.80})
    dump(BASE/'x1/novelty-audit.json',{'scope':'200 exact Elaren source records only; bounded lexical review with family semantic comparison','comparisons':40000,'rows':comparisons,'universal_novelty_claimed':False,'family_review':[{'family':f['name'],'new_distinction':f['mission'],'changed_evidence':'Explicit executable input and independently specified expected report; positive and contrary protocol scenarios, rather than metadata assertions about a synthesizer patch.','null':'Equivalent mission, falsifier, evidence, and recovery to an inherited row would remove novelty credit.','disposition':'candidate_for_x2'} for f in FAMILIES]})
    dump(BASE/'x1/source-ledger.json',{'sources':[{'url':u,'status':'current' if u in [SIMPY,FSM,CSP,STATS] else 'stable','checked_on':'2026-09-06','use':'Narrow software vocabulary, arithmetic, provenance or structural reservation. No empirical observation or authority grant.'} for u in [SIMPY,FSM,CSP,STATS,PROV,WCAG,VC]],'same_owner_only':True})
    dump(BASE/'x1/startup-methods.json',{'startup_failures':[{'id':'IR6858-START-001','signature':'Fresh no-checkout worktree index absent caused inherited staged-deletion display','success_credit':0,'recovery':'Verified empty owner lane and exact HEAD, then read-tree under the already installed sparse patterns','witness':'Clean status, zero materialized source files, initialized index','state':'validated'},{'id':'IR6858-START-002','signature':'Combined tool output exceeded display token budget','success_credit':0,'recovery':'Stored independent results separately, reduced projections, and reread omitted source content','witness':'Full source packet reconstruction and EOF tail consumed','state':'validated'}],'source_failure_overlay_preserved':True})
    print(json.dumps({'planning_proposals':len(proposals),'families':len(FAMILIES),'files':len(list(BASE.rglob('*.*'))),'novelty_quarantine':sum(r['quarantine'] for r in comparisons)}))

if __name__=='__main__':main()
