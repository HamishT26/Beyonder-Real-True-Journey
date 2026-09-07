"""Build owner-scoped x2 teaching artifacts from already observed contract results."""
from pathlib import Path
import collections,copy,hashlib,json
from build_ghc_family_teryn_halewick_v687_v4_x1 import OPS,GATES,BOUNDARY,SOURCE,BASE

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/BASE
X1='ebb7e751140388b81f0f9c28ff0337854a536ec5'

def enc(value):return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def load(path):return json.loads(path.read_bytes())
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(value.encode() if isinstance(value,str) else enc(value))

def make_ledger(name,title,negatives,witness_specs):
    mid='TH6874-'+name.upper();witnesses=[]
    for ident,result,expected,observed,negative_ids in witness_specs:
        witnesses.append(dict(witness_id=ident,method_id=mid,procedure=title,scope='Exact owner-local frozen fixture',expected=expected,observed=observed,result=result,same_owner_only=True,independent_reproduction=False,retained_negative_ids=negative_ids,boundary='Synthetic workflow only; protected gates remain.'))
    passing=[w['witness_id'] for w in witnesses if w['result']=='pass'];assert passing
    record=dict(method_id=mid,title=title,failure_signature='Invalid candidate or inadequate draft is retained at zero original credit.',trigger_preconditions=['The exact frozen case and versioned local profile apply.'],privacy_class='sanitized_public',approval_class='safe_now',candidate_workaround='Compare the complete typed result; preserve the failed candidate beside the separately witnessed rejection or correction.',validation_witness_ids=[w['witness_id'] for w in witnesses],recurrence_guard='Do not equate rejection with candidate success or extend this finite fixture to arbitrary inputs.',rollback='Stop the affected operation; retain original definitions and witnesses.',recommendation_state='preferred',supersedes=[],protected_gates=GATES,retained_negative_ids=negatives,scope_boundary=BOUNDARY)
    events=[dict(event_index=1,method_id=mid,before=None,after='candidate',reason='Declared method with retained negative linkage',witness_id=None),dict(event_index=2,method_id=mid,before='candidate',after='validated',reason='Recorded passing bounded witness',witness_id=passing[0]),dict(event_index=3,method_id=mid,before='validated',after='preferred',reason='Preferred only for this declared trigger',witness_id=passing[0])]
    return dict(schema='ghc.family.method-flow-state.v1',owner='Teryn Halewick',phase='v687-v4',identity_boundary=BOUNDARY,boundary=BOUNDARY,methods=[record],witnesses=witnesses,state_events=events,recommendations=[],counts=dict(methods=1,witnesses=len(witnesses),state_events=3,recommendations=0,states=dict(observed=0,candidate=0,validated=0,preferred=1,superseded=0,deprecated=0),witness_results=dict(collections.Counter(w['result'] for w in witnesses))))

def main():
    proposals=load(PHASE/'x1/new-proposals.json')['proposals'];results=load(PHASE/'x2/contract-results-initial.json');mutations=load(PHASE/'x2/mutation-results.json');by_id={r['proposal_id']:r for r in results};assert all(r['passed'] for r in results) and all(r['rejected'] for r in mutations)
    write(PHASE/'x2/contract-results.json',results)
    core=ROOT/'scripts/ghc_family_teryn_halewick_v687_v4_core.py';core_bytes=core.read_bytes()
    core_name=core.name
    for operation,slug,pillar,practice,neighbor,meaning in OPS:
        filename='ghc_family_teryn_halewick_v687_v4_'+operation+'.py'
        wrapper='"""Bounded '+operation+' interface."""\nfrom '+core.stem+' import cli\n\nif __name__ == "__main__":\n    cli('+repr(operation)+')\n'
        write(ROOT/'scripts'/filename,wrapper)
        skill=PHASE/'skills'/('ghc-family-'+slug)
        selected=[r for r in proposals if r['operation']==operation]
        guide='---\nname: ghc-family-'+slug+'\ndescription: '+json.dumps(meaning,ensure_ascii=False)+'\n---\n\n# '+operation.replace('_',' ').title()+'\n\n'+meaning+'\n\nUse the finite contracts in [references/contracts.json](references/contracts.json) to distinguish accepting samples from held previews. Read the input, complete expected output, and five changed-result submissions before execution. A local type-strict comparison is deliberately narrower than general JSON Schema numeric equivalence; it is not a standards conformance claim.\n\nRun `python scripts/'+filename+' --input INPUT.json --output NEW_OUTPUT.json` in an isolated environment satisfying [references/requirements.lock](references/requirements.lock). The output path must be new; preserving old witnesses is part of the interface. No external reference is fetched, and no live record is patched.\n\nCompare the complete typed output, verify the original input is unchanged, and retain every invalid submission at zero original success credit. Rejection is a separate witness. A mismatch requires an additive correction and a focused recovery; never change the frozen expectation to match the implementation.\n\n'+BOUNDARY+'\n'
        write(skill/'SKILL.md',guide);write(skill/'references/contracts.json',dict(operation=operation,source=X1,cases=selected,boundary=BOUNDARY));write(skill/'references/requirements.lock',(PHASE/'x2/requirements.lock').read_text(encoding='utf8'))
        write(skill/'scripts'/filename,wrapper);write(skill/'scripts'/core_name,core_bytes.decode('utf8'))
        members=[dict(path=p.relative_to(skill).as_posix(),bytes=len(p.read_bytes()),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(skill.rglob('*')) if p.is_file()]
        write(skill/'manifest.json',dict(entries=members,self_exclusions=['manifest.json'],scope='Exact checkout bytes; installed parity checked separately.'))
    # A separate ledger for each module keeps all documents below the word cap.
    ledger_index=[]
    for index,(operation,*_) in enumerate(OPS,1):
        selected=[r for r in results if r['operation']==operation];ids={r['proposal_id'] for r in selected};invalid=[m for m in mutations if m['proposal_id'] in ids];neg=[m['mutation_id'] for m in invalid];spec=[]
        for r in selected:spec.append((r['proposal_id']+'-POS','pass','Complete frozen typed result','Matched; original input preserved',[]))
        for m in invalid:
            spec.append((m['mutation_id']+'-F','fail','A valid complete result','Deliberately changed result is invalid; zero original credit',[m['mutation_id']]))
            spec.append((m['mutation_id']+'-R','pass','Reject this changed result','Rejected by the frozen typed oracle',[m['mutation_id']]))
        ledger=make_ledger('OP'+str(index),operation,neg,spec);rel='x2/method-flow/'+operation+'/ledger.json';write(PHASE/rel,ledger);ledger_index.append(dict(path=BASE+'/'+rel,counts=ledger['counts']))
    drafts=load(PHASE/'x1/novelty-retained-negatives.json')['original_drafts']
    for i,draft in enumerate(drafts,1):
        pid=draft['proposal_id'];nid=f'TH6874-NOVELTY-N{i:03d}';ledger=make_ledger('NOVELTY'+str(i),'Refine a shadowed planning requirement',[nid],[(nid+'-F','fail','Distinct field reaches its own refusal','The draft field was shadowed by an earlier refusal',[nid]),(nid+'-P','pass','Refined frozen input reaches its named refusal',by_id[pid]['actual']['result']['reason'],[nid])]);rel=f'x2/method-flow/novelty-{i}/ledger.json';write(PHASE/rel,ledger);ledger_index.append(dict(path=BASE+'/'+rel,counts=ledger['counts']))
    for i,row in enumerate(load(PHASE/'x2/package-smokes.json'),1):
        nid=f'TH6874-PACKAGE-N{i:03d}';ledger=make_ledger('PACKAGE'+str(i),row['name']+' bounded smoke',[nid],[(nid+'-POS','pass','Useful positive package operation','Passed',[]),(nid+'-F','fail','Valid package input','Deliberately invalid package fixture; zero original credit',[nid]),(nid+'-R','pass','Refuse invalid package fixture','Refused',[nid])]);rel=f'x2/method-flow/package-{i}/ledger.json';write(PHASE/rel,ledger);ledger_index.append(dict(path=BASE+'/'+rel,counts=ledger['counts']))
    write(PHASE/'x2/method-flow/index.json',dict(ledgers=ledger_index,methods=17,failed_witnesses=1007,passing_witnesses=1210,inherited_startup_ledger=BASE+'/x1/method-flow/ledger.json'))
    # Four distinct lenses may appear under multiple pillars; each card has one parent.
    deck=PHASE/'x2/deck';cards=[]
    def card(tier,title,parent,content,outcome='represented',stable=False):
        seed=[tier,title,parent,'v687-v4'];cid='ghc-card-'+hashlib.sha256(enc(seed)).hexdigest()[:20]
        obj=dict(schema='ghc.family.freed-card.v1',card_id=cid,tier=tier,card_type=['','freed_id_anchor','trinity_pillar','bounded_practice','task'][tier],title=title,parent_ids=[] if parent is None else [parent],owner='Teryn Halewick',phase='v687-v4',stability='stable' if stable else 'volatile',outcome=outcome,content=content,source_refs=[BASE+'/x1/new-proposals.json'],protected_gates=GATES,boundary='Relational working language and synthetic evidence only; see stable-prefix.json.')
        write(deck/'cards'/(cid+'.json'),obj);cards.append(obj);return cid
    owner=card(1,'Teryn Halewick',None,load(PHASE/'x1/identity.json'),stable=True)
    pillars={name:card(2,name,owner,dict(protected_boundary=BOUNDARY),stable=True) for name in ['GMUT Mind','THOS Body','Freed ID and CBR Heart']}
    practices={}
    for _,_,pillar,practice,_,_ in OPS:
        if (pillar,practice) not in practices:practices[pillar,practice]=card(3,practice,pillars[pillar],dict(lens=practice,qualification=False),stable=True)
    task_cards={}
    for p in proposals:
        result=by_id[p['id']];content=dict(proposal_id=p['id'],operation=p['operation'],input=p['input'],literal_result=result['actual'],result_narration=p['title']+'. The frozen complete result matched this recorded sample; its declared disposition remains '+p['expected_execution_disposition']+'.',stable_boundary_ref='stable-prefix.json',invalid_candidate_original_success_credit=0,mutation_ids=[m['mutation_id'] for m in p['mutations']],mutations_ref=BASE+'/x2/mutation-results.json',rejection_witnesses_ref=BASE+'/x2/method-flow/'+p['operation']+'/ledger.json',artifact=BASE+'/x2/contract-results.json',falsifier=p['null_or_failure_condition'],rollback=p['rollback_or_recovery'])
        cid=card(4,p['id']+' '+p['title'],practices[p['pillar'],p['practice']],content,p['expected_execution_disposition']);task_cards[p['id']]=cid
    write(deck/'deck-index.json',dict(source=SOURCE,x1=X1,cards=[c['card_id'] for c in cards],counts=dict(cards=len(cards),tiers=dict(collections.Counter(c['tier'] for c in cards)),distinct_practices=4,practice_context_cards=len(practices)),task_outcomes=dict(collections.Counter(p['expected_execution_disposition'] for p in proposals)),cache_performance_claim=False))
    write(deck/'stable-prefix.json',dict(cards=[c['card_id'] for c in cards if c['stability']=='stable'],boundary=BOUNDARY))
    write(deck/'volatile-index.json',dict(cards=[c['card_id'] for c in cards if c['stability']=='volatile'],implicit_completion=False))
    entries=[dict(path=p.relative_to(ROOT).as_posix(),bytes=len(p.read_bytes()),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(deck.rglob('*')) if p.is_file()]
    write(deck/'card-manifest.json',dict(entries=entries,self_exclusions=[BASE+'/x2/deck/card-manifest.json']))
    plan=load(PHASE/'x1/portfolio-plan.json');execution={}
    for kind in ['safe','candidates','clean_fix_refine']:
        execution[kind]=[]
        for task in plan[kind]:
            ids=task.get('proposals',[task.get('proposal')]);passed=all(by_id[x]['passed'] and by_id[x]['input_preserved'] for x in ids)
            if kind=='clean_fix_refine':
                obj=load(deck/'cards'/(task_cards[ids[0]]+'.json'))['content'];procedure=task['procedure']
                passed=passed and (obj['stable_boundary_ref']=='stable-prefix.json' if procedure.startswith('factor_') else obj['invalid_candidate_original_success_credit']==0 if procedure.startswith('show_') else obj['literal_result']==by_id[ids[0]]['actual'] and bool(obj['result_narration']))
            execution[kind].append(dict(task_id=task['id'],procedure=task['procedure'],proposals=ids,outcome='completed' if passed else 'open_gap',witnesses=[x+'-POS' for x in ids],additional_independent_witness_credit=0,combined_execution_authorized=False))
    execution['exact_packets']=[dict(t,outcome='exact_gate') for t in plan['exact_packets']];execution['blocked_packets']=[dict(t,outcome='open_gap') for t in plan['blocked_packets']]
    write(PHASE/'x2/portfolio-execution.json',execution)
    outcomes=[dict(proposal_id=p['id'],outcome=p['expected_execution_disposition'],witness=p['id']+'-POS',sample_passed=by_id[p['id']]['passed'],boundary=BOUNDARY) for p in proposals]
    write(PHASE/'x2/outcome-ledger.json',outcomes)
    write(PHASE/'x2/evidence-counts.json',dict(inherited_overlay=dict(negatives=77896,methods=93048,failed_witnesses=48744,passing_witnesses=77043,open_gaps=674,exact_gates=659,proposals=14430),owner_delta=dict(negatives=1015,methods=25,failed_witnesses=1015,passing_witnesses=1218,open_gaps=9,exact_gates=10,proposals=200),effective=dict(negatives=78911,methods=93073,failed_witnesses=49759,passing_witnesses=78261,open_gaps=683,exact_gates=669,proposals=14630),counting='Startup: 8 failed and 8 passing; planning: 4 failed and 4 passing; contracts: 200 positive, 1000 invalid candidates, 1000 rejection passes; packages: 3 invalid candidates and 6 passes. Task/editorial reuse supplies no extra witness credit.'))
    write(PHASE/'x2/phase-truth.json',dict(owner='Teryn Halewick',phase='v687-v4',source=SOURCE,x1=X1,state='X2_EVIDENCE_PREPARED',outcomes=dict(collections.Counter(x['outcome'] for x in outcomes)),contract_matches=200,changed_result_rejections=1000,skills_built=10,runners_built=10,global_promotions='PENDING_VALIDATION_AND_PARITY',canonical_invocations=0,canonical_successes=0,successor_contacted=False,terminal_verdict='NOT_READY_FOR_STAGE_20'))
    write(PHASE/'x2/accessibility-reservations.json',dict(structure='Named sections, explicit outcomes, literal inputs/results, deterministic card order and links.',reserved=['manual review','assistive-technology testing','browser review','cognitive evaluation','affected-user evaluation','Maori language and authority review'],complete_accessibility=False))
    write(PHASE/'x2/workload.json',dict(contracts=200,mutations=1000,editorial_operations=300,unique_practice_lenses=4,subjective_wellbeing_claim=False,reset_redemption_authority='Hamish only',host_security_changed=False,desktop_updated=False,rebooted=False))
    print(json.dumps(dict(skills=10,runners=10,deck_cards=len(cards),method_ledgers=len(ledger_index),outcomes=dict(collections.Counter(x['outcome'] for x in outcomes)))))

if __name__=='__main__':main()
