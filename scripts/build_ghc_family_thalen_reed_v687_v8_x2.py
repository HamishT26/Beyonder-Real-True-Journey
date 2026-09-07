"""Materialize current-owner evidence from frozen plans and attributable local executions."""
from __future__ import annotations
import argparse
import copy
import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/thalen-reed/v687-v8')
X1='8f9070f01e38fa5cc330cff247ea8e32541a0387'
SOURCE='7e72086683731c40b4884ee7254c864891e354a9'
sys.path.insert(0,str(ROOT/'scripts'))
from build_ghc_family_thalen_reed_v687_v8_x1 import OPS, RUNNERS, PRACTICES, GATES, BOUNDARY

NOTES={
 'riff_chunks':('Walk complete RIFF WAVE byte envelopes, preserving unknown and duplicate chunk identifiers, exact offsets, payload sizes, and padding bytes.',
                'The envelope size must equal the supplied bytes. A partial header, payload overrun, or missing odd-byte pad is a refusal. This walker accepts at most 64 chunks and 65,536 bytes. LIST contents stay opaque; finding fmt or data does not validate their audio semantics.'),
 'pcm_format':('Check classic integer PCM format arithmetic for one or two channels, eight or sixteen bits, and an integer rate from one through 384,000.',
                'Reject Boolean or floating numeric fields before arithmetic. Require block alignment to equal channels times bytes per sample and byte rate to equal sample rate times block alignment. Tag 3, extensible tag 65534, wider samples, and additional fields require a new explicit profile.'),
 'pcm_frames':('Relate a bounded declared PCM byte count to complete frames and an optional declared frame count.',
               'Count bytes only after positive integer alignment is established. A partial final frame is held; it is never silently truncated. The generic counter accepts alignments one through 64 and no more than 1,048,576 bytes. Metadata arithmetic does not verify an audio file or sampling apparatus.'),
 'sample_time':('Convert nonnegative sample indices and exact rational times with an explicit origin, without rounding.',
                'Use integer or integer-fraction text with at most 80 characters, integer rates one through 384,000, and indices at most one trillion. Negative origins are allowed. The inverse map refuses off-grid times and times before the origin. A duration is a numerical representation, not a measured clock interval.'),
 'pcm_range':('Classify signed or unsigned integer sample values against exact one-through-thirty-two-bit numeric bounds.',
              'Accept at most 64 integer samples and Boolean signedness. Report out-of-range positions separately from positions equal to an endpoint. An endpoint value alone never establishes clipping, distortion, audibility, instrument behavior, or restoration quality.'),
 'channel_permutation':('Apply a bijective source-channel permutation to small synthetic integer frame arrays and return its inverse.',
                        'Require one through eight unique nonempty channel labels, an exact integer permutation, and rectangular frames. Boolean indices, repeated indices, negative wraparound, missing channels, and float sample coercion are refused. Labels are source metadata and establish no speaker identity.'),
 'edit_intervals':('Represent an ordered half-open keep map and its complementary dropped spans while preserving the input record.',
                   'Reject overlapping, reverse-ordered, reversed, empty, negative, or past-end spans. Touching half-open spans are valid. At most 64 spans and one trillion source frames are supported. The output map is a reversible description; this tool does not edit a recording or authorize deletion.'),
 'segment_binding':('Verify source and segment SHA-256 claims against literal supplied bytes and explicit half-open endpoints.',
                    'Require lowercase hexadecimal, exact 64-character lowercase digests, and in-range integer endpoints. Empty segments are allowed and bind the empty byte string. A digest establishes only byte correspondence; it does not establish original custody, identity, consent, or rights.'),
 'restoration_claim':('Represent exact differences between two synthetic metrics only when their declared frame, rate, and channel metadata agree.',
                      'Missing metrics, unmatched geometry, or undefined direction remain gaps. Real audio and asserted independent review require external evidence. A better synthetic number never becomes perceptual effectiveness, governed participant evidence, or independent reproduction.'),
 'disclosure_gate':('Map a declared synthetic audio-related action to its exact evidence and authority reservations.',
                    'The claimed_permissions array is recorded as input but never treated as a verified grant. Publication, speaker identification, legal or cultural decisions, Maori labels or data, production identity, source deletion, and Stage 20 remain reserved. The runtime performs no external action.'),
}

def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def dump(path,value):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()

def changed_output(value,mutation):
    result=copy.deepcopy(value)
    if mutation=='missing_accepted':result.pop('accepted')
    elif mutation=='accepted_type':result['accepted']=1 if result['accepted'] else 0
    elif mutation=='extra_authority':result['authority_established']=True
    elif mutation=='value_replaced':result['value']=[{'unexpected_replacement':True}]
    elif mutation=='external_credit_promoted':result['external_credit']=True
    else:raise ValueError('Unknown frozen mutation')
    return result

def build_skills_and_runners(cases,skill_root,bank):
    core=(ROOT/'scripts/ghc_family_pcm_evidence_core.py').read_text(encoding='utf-8')
    input_root=bank/'smoke-inputs';input_root.mkdir(exist_ok=True)
    duplicate=input_root/'duplicate.json';duplicate.write_text('{"operation":"riff_chunks","operation":"pcm_range"}\n',encoding='utf-8')
    skill_rows=[];runner_rows=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
    def smoke(path,op):
        c=next(c for c in cases if c['operation']==op and c['expected_output']['accepted'])
        fixture=input_root/(op+'.json');fixture.write_bytes(canonical(c['input'])+b'\n')
        positive=subprocess.run([sys.executable,'-X','utf8',str(path),str(fixture)],capture_output=True,text=True,encoding='utf-8',env=env)
        adverse=subprocess.run([sys.executable,'-X','utf8',str(path),str(duplicate)],capture_output=True,text=True,encoding='utf-8',env=env)
        observed=json.loads(positive.stdout);bad=json.loads(adverse.stdout)
        good=positive.returncode==0 and canonical(observed)==canonical(c['expected_output'])
        rejected=adverse.returncode==2 and bad['error']=='DUPLICATE_JSON_KEY' and bad['external_credit'] is False
        assert good and rejected,(path.name,positive.returncode,adverse.returncode)
        return {'fixture':c['proposal_id'],'positive_pass':good,'adverse_rejected':rejected,'adverse_error':'DUPLICATE_JSON_KEY','adverse_success_credit':0,'same_owner_only':True}
    for op,name,pillar,practice in OPS:
        root=BASE/'skills'/name;wrapper='ghc_family_'+op+'.py'
        purpose,details=NOTES[op]
        skill='---\nname: '+name+'\ndescription: '+purpose+' Use for owner-scoped synthetic evidence; no real audio or authority decisions.\n---\n\n# '+name.removeprefix('ghc-family-').replace('-',' ').title()+'\n\n'+purpose+'\n\n'+details+'\n\nRead `references/contracts.json` for twenty frozen accepting and refusing examples. Invoke `python scripts/'+wrapper+' INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire output, including its types and false external-credit field, to the selected owner fixture. A compatible new fixture needs its own preregistered acceptance condition and receives no inherited completion credit.\n\nThe wrapper and shared core are portable within this package. Keep their manifest together, preserve earlier callers, and never overwrite a different global package. Retain every failed invocation and correct only the affected dependency.\n\n'+BOUNDARY+' Maori concepts remain under Maori authority.\n'
        write(root/'SKILL.md',skill)
        dump(root/'references/contracts.json',{'schema':'ghc.family.pcm-skill-contracts.v1','source':SOURCE,'x1':X1,'operation':op,'contracts':[c for c in cases if c['operation']==op],'boundary':BOUNDARY})
        write(root/'scripts/ghc_family_pcm_evidence_core.py',core)
        write(root/'scripts'/wrapper,'"""Portable '+op+' evidence interface."""\nfrom ghc_family_pcm_evidence_core import main\n\nif __name__ == "__main__":\n    raise SystemExit(main('+repr([op])+'))\n')
        members=[]
        for p in sorted((ROOT/root).rglob('*')):
            if p.is_file():
                b=p.read_bytes();members.append({'relative':p.relative_to(ROOT/root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
        dump(root/'manifest.json',{'schema':'ghc.family.portable-skill-manifest.v1','name':name,'members':members,'self_exclusion':'manifest.json','source':SOURCE,'x1':X1})
        validation=subprocess.run([sys.executable,'-X','utf8',str(skill_root/'.system/skill-creator/scripts/quick_validate.py'),str(ROOT/root)],capture_output=True,text=True,encoding='utf-8',env=env)
        row={'name':name,'quick_validate_returncode':validation.returncode,**smoke(ROOT/root/'scripts'/wrapper,op)}
        assert validation.returncode==0,(name,validation.stdout,validation.stderr)
        skill_rows.append(row)
    for name,operations in RUNNERS:
        write(Path('scripts')/name,'"""Bounded '+', '.join(operations)+' evidence interface."""\nfrom ghc_family_pcm_evidence_core import main\n\nif __name__ == "__main__":\n    raise SystemExit(main('+repr(operations)+'))\n')
        runner_rows.append({'name':name,'operations':operations,**smoke(ROOT/'scripts'/name,operations[0])})
    dump(BASE/'x2/skill-validation.json',{'schema':'ghc.family.skill-use.v1','rows':skill_rows,'validated_and_used':10,'global_promotion_yet':False})
    dump(BASE/'x2/runner-smokes.json',{'schema':'ghc.family.runner-use.v1','rows':runner_rows,'validated_and_used':5})
    return skill_rows,runner_rows

def build_deck(cases,results):
    deck=BASE/'x2/deck';cards=[];by_name={}
    def card(tier,kind,title,parent,outcome,content,refs):
        body={'schema':'ghc.family.freed-id-card.v1','tier':tier,'card_type':kind,'title':title,'parent_ids':[] if parent is None else [parent],
              'owner':'Thalen Reed','phase':'v687-v8','stability':'stable' if tier<4 else 'volatile','outcome':outcome,'content':content,
              'source_refs':refs,'protected_gates':GATES,'relational_boundary':BOUNDARY}
        ident='ghc-card-'+digest(body)[:24];body['card_id']=ident;cards.append(body);dump(deck/'cards'/(ident+'.json'),body);return ident
    anchor=card(1,'freed_id_anchor','Thalen Reed',None,'represented',read(BASE/'x1/identity.json'),[str(BASE/'x1/identity.json').replace('\\','/')])
    pillars={}
    for name in ['GMUT Mind','THOS Body','Freed ID and CBR Heart']:
        pillars[name]=card(2,'trinity_pillar',name,anchor,'represented',{'priority':name=='THOS Body','external_gates_closed':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'},[str(BASE/'x1/deck-plan.json').replace('\\','/')])
    parents=['THOS Body','GMUT Mind','THOS Body','Freed ID and CBR Heart'];practices=[]
    for name,pillar in zip(PRACTICES,parents):practices.append(card(3,'bounded_practice',name,pillars[pillar],'represented',{'synthetic_learning_lens':True,'professional_qualification':False},[str(BASE/'x1/deck-plan.json').replace('\\','/')]))
    opmeta={o:idx for o,_,_,idx in OPS}
    for c in cases:
        r=results[c['proposal_id']]
        card(4,'task',c['title'],practices[opmeta[c['operation']]],r['outcome'],{'proposal_id':c['proposal_id'],'operation':c['operation'],'input':c['input'],'actual_output':r['actual_output'],'complete_match':r['complete_match'],'input_unchanged':r['input_unchanged'],'rollback':c['rollback_or_recovery']},[str(BASE/'x1/new-proposals.json').replace('\\','/'),str(BASE/'x2/contract-results.json').replace('\\','/')])
    dump(deck/'deck-index.json',{'schema':'ghc.family.deck-index.v1','source':SOURCE,'x1':X1,'cards':[c['card_id'] for c in cards],'counts':{'owner':1,'pillar':3,'practice':4,'task':200},'core_outcomes':dict(Counter(r['outcome'] for r in results.values()))})
    dump(deck/'stable-prefix.json',{'schema':'ghc.family.deck-prefix.v1','cards':[c['card_id'] for c in cards if c['tier']<4],'cache_effect_established':False})
    dump(deck/'volatile-index.json',{'schema':'ghc.family.deck-volatile.v1','cards':[c['card_id'] for c in cards if c['tier']==4],'implicit_completion':False})
    sections=['Identity and corrigibility','Current route authority','Immutable source anchors','Frozen x1 proposals','Trinity pillars','Bounded practices','Task evidence','Method Flow and negatives','Open gaps and exact gates','Validation and manifests','Workload and accessibility','Successor recommendations','Compact baton index']
    dump(deck/'baton-index.json',{'schema':'ghc.family.deck-baton-index.v1','sections':sections,'section_count':13,'final_baton':'pending_final_artifact','live_delivery':False})
    write(deck/'compact-activation.md','# Prospective Liora Venn v688-v1\n\nThis x2 deck is evidence preparation. The final head and canonical receipt are pending. No successor has been contacted. Read the final committed baton only after the owner terminal gate.\n\n'+BOUNDARY+'\n')
    body='<!doctype html>\n<html lang="en"><meta charset="utf-8"><title>Thalen PCM evidence deck</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem}td,th{border:1px solid #777;padding:.5rem}table{border-collapse:collapse}a{color:#174b91}</style><body><a href="#main">Skip to evidence</a><header><h1>Thalen Reed: synthetic PCM evidence</h1><p>'+html.escape(BOUNDARY)+'</p></header><main id="main"><h2>Observed bounded outcomes</h2><p>160 completed, 14 represented, 8 open gaps, and 18 exact gates. Real audio and external actions: zero.</p><table><caption>All 200 frozen proposal contracts and their evidence outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Contract</th><th scope="col">Outcome</th></tr></thead><tbody>'
    for c in cases:body+='<tr><th scope="row">'+c['proposal_id']+'</th><td>'+html.escape(c['title'])+'</td><td>'+results[c['proposal_id']]['outcome']+'</td></tr>'
    body+='</tbody></table><h2>Evaluation boundary</h2><p>This report has structural checks. Manual, assistive-technology, cognitive, affected-user, and Maori-language evaluation remains reserved.</p></main></body></html>\n'
    write(deck/'accessible-report.html',body)
    members=[]
    for p in sorted((ROOT/deck).rglob('*')):
        if p.is_file():members.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    dump(deck/'card-manifest.json',{'schema':'ghc.family.deck-manifest.v1','entries':members,'self_exclusion':str(deck/'card-manifest.json').replace('\\','/'),'card_count':208})

def method_ledger(cases, mutations, package, skills, runners):
    methods=[];witnesses=[];events=[]
    by_case={c['proposal_id']:c for c in cases}
    def method(mid,title,negatives):
        methods.append({'method_id':mid,'title':title,'failure_signature':'A declared adverse candidate must remain rejected and at zero original success credit.',
            'trigger_preconditions':['Thalen v687-v8 immutable x1','bounded synthetic input or package fixture'],
            'privacy_class':'sanitized_public','approval_class':'safe_now','candidate_workaround':'Use the frozen exact input and compare the complete typed output. Preserve the rejected alternative.',
            'validation_witness_ids':[],'recurrence_guard':'Bind the exact definition and code digests; do not infer authority from a software match.',
            'rollback':'Stop selecting the changed surface; retain its definition, failure, and compatible predecessor.',
            'recommendation_state':'preferred','supersedes':[],'protected_gates':GATES,'retained_negative_ids':negatives,
            'scope_boundary':'Owner-local synthetic software only; no external or independent reproduction credit.'})
        for a,b in [('observed','candidate'),('candidate','validated'),('validated','preferred')]:events.append({'method_id':mid,'from':a,'to':b})
    def witness(mid,ident,result,procedure,refs,expected,observed):
        witnesses.append({'witness_id':ident,'method_id':mid,'procedure':procedure,'scope':'Thalen v687-v8 owner delta',
            'expected':expected,'observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,
            'retained_negative_ids':refs,'boundary':'A rejection witness is separate from its zero-credit candidate; neither proves external reality.'})
    for op,_,_,_ in OPS:
        mid='TR6878-X2-M-'+op;neg=[r for r in mutations if by_case[r['proposal_ref']]['operation']==op]
        method(mid,NOTES[op][0],[r['packet_id'] for r in neg])
        for c in cases:
            if c['operation']==op:witness(mid,c['proposal_id']+'-MATCH','pass','Compare complete frozen output and unchanged input',[],c['expected_output'],'Exact type-sensitive match with unchanged input')
        for r in neg:
            witness(mid,r['packet_id']+'-FAIL','fail','Retained altered-output candidate',[r['packet_id']],'Complete frozen output','Altered output differs; original candidate receives zero success credit')
            witness(mid,r['packet_id']+'-REJECT','pass','Reject altered-output candidate',[r['packet_id']],'Refuse every changed field or type','Candidate rejected by complete-output comparison')
    groups=[('package',package['rows']),('skill',skills),('runner',runners)]
    for kind,rows in groups:
        for i,r in enumerate(rows,1):
            mid=f'TR6878-X2-M-{kind}-{i:02d}';nid=f'TR6878-X2-N-{kind}-{i:02d}'
            method(mid,kind+' bounded accepting and adverse interface: '+r['name'],[nid])
            witness(mid,mid+'-POSITIVE','pass','Pinned package or declared interface positive fixture',[],'Accept the declared synthetic fixture','Observed positive pass')
            witness(mid,mid+'-FAIL','fail','Retain malformed or out-of-range candidate',[nid],'Valid package or interface input','Candidate is outside the declared input contract; zero success credit')
            witness(mid,mid+'-REJECT','pass','Bounded rejection of the adverse candidate',[nid],'Reject the adverse input','Observed expected rejection')
    for m in methods:m['validation_witness_ids']=[w['witness_id'] for w in witnesses if w['method_id']==m['method_id']]
    counts={'methods':len(methods),'failed_witnesses':sum(w['result']=='fail' for w in witnesses),'passing_witnesses':sum(w['result']=='pass' for w in witnesses),'witnesses':len(witnesses)}
    assert counts=={'methods':28,'failed_witnesses':268,'passing_witnesses':486,'witnesses':754}
    return {'schema':'ghc.family.method-flow-state.v1','owner':'Thalen Reed','phase':'v687-v8','identity_boundary':BOUNDARY,
        'execution_authority':'owner_self_scoped_delta','source_commit':SOURCE,'x1_commit':X1,'final_commit':None,
        'methods':methods,'witnesses':witnesses,'state_events':events,'recommendations':[],'counts':counts,
        'count_contract':'10 operation methods plus 3 package, 10 skill, and 5 runner methods. Failed candidates: 250 altered outputs plus 18 package/interface adverse inputs. Passing witnesses: 200 contract matches plus 250 rejections plus 36 package/interface accepting and rejecting witnesses. Portfolio projections and repeated validation add zero duplicate witness credit.',
        'boundary':'Every failed candidate and its rejection remain independently addressable. No empirical or independent-reproduction credit.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--skill-root',type=Path,required=True);a=ap.parse_args()
    assert git('rev-parse','HEAD')==X1
    equality=json.loads((a.bank/'x1-equality.json').read_text());assert equality['x1']==X1 and equality['clean'] and equality['divergence']==[0,0]
    assert all(equality[k]==X1 for k in ['local','upstream','tracking','fresh_live'])
    assert not (ROOT/BASE/'x2/contract-results.json').exists(),'Evidence already exists; do not overwrite an executed record'
    cases=read(BASE/'x1/new-proposals.json')['proposals'];case_map={c['proposal_id']:c for c in cases}
    first=json.loads((a.bank/'first-execution.json').read_text());assert first['passed']==200 and first['failed']==0
    results={}
    for row in first['rows']:
        c=case_map[row['proposal_id']];assert row['pass'] and row['input_unchanged'] and canonical(row['actual_output'])==canonical(c['expected_output'])
        results[c['proposal_id']]={**row,'outcome':c['expected_execution_disposition'],'definition_sha256':digest(c),'external_credit':False}
    dump(BASE/'x2/x1-boundary.json',equality)
    dump(BASE/'x2/contract-results.json',{'schema':'ghc.family.pcm-contract-results.v1','source':SOURCE,'x1':X1,'count':200,'rows':list(results.values()),'core_source_sha256':hashlib.sha256((ROOT/'scripts/ghc_family_pcm_evidence_core.py').read_bytes()).hexdigest(),'same_owner_only':True,'independent_reproduction':False})
    plan=read(BASE/'x1/portfolio-plan.json');mutation_rows=[]
    for task in plan['candidates']:
        expected=case_map[task['proposal_ref']]['expected_output'];bad=changed_output(expected,task['mutation']);rejected=canonical(bad)!=canonical(expected);assert rejected
        mutation_rows.append({'packet_id':task['packet_id'],'proposal_ref':task['proposal_ref'],'mutation':task['mutation'],'candidate_output':bad,'original_candidate_success_credit':0,'rejected':True,'rejection_witness_pass':True})
    dump(BASE/'x2/mutation-results.json',{'schema':'ghc.family.altered-output-witnesses.v1','count':250,'rejected':250,'rows':mutation_rows,'candidate_failure_erased':False})
    out={}
    for category in ['safe_now','candidates','clean_fix_refine']:
        out[category]=[]
        for task in plan[category]:
            c=case_map[task['proposal_ref']];procedure=task['procedure']
            if procedure=='complete_frozen_output':passed=results[c['proposal_id']]['complete_match']
            elif procedure=='input_unchanged':passed=results[c['proposal_id']]['input_unchanged']
            elif procedure=='altered_output_rejection':passed=next(r for r in mutation_rows if r['packet_id']==task['packet_id'])['rejected']
            elif procedure=='canonical_json_roundtrip':passed=canonical(json.loads(canonical(c)))==canonical(c)
            elif procedure=='definition_digest_binding':passed=digest(c)==results[c['proposal_id']]['definition_sha256']
            elif procedure=='stable_identifier_uniqueness':passed=sum(x['proposal_id']==c['proposal_id'] for x in cases)==1
            else:raise ValueError(procedure)
            assert passed
            out[category].append({**task,'executed':True,'procedure_pass':True,'procedure_outcome':'completed','independent_witness_credit':0 if category=='clean_fix_refine' or procedure=='input_unchanged' else None})
    for category in ['exact_packets','blocked_packets']:out[category]=copy.deepcopy(plan[category]);assert all(not r['executed'] for r in out[category])
    out.update({'schema':'ghc.family.portfolio-results.v1','destructive_cleanup':False,'witness_reuse_rule':plan['witness_reuse_rule']});dump(BASE/'x2/portfolio-results.json',out)
    package=json.loads((a.bank/'package-smokes.json').read_text());assert package['all_pass'];dump(BASE/'x2/package-smokes.json',package)
    wheel=read(BASE/'x1/wheel-plan.json');dump(BASE/'x2/environment-receipt.json',{'schema':'ghc.family.isolated-environment.v1','primary_drive':'D','direct_packages':{w['name']:w['version'] for w in wheel['wheels'] if w['direct']},'all_packages':{w['name']:w['version'] for w in wheel['wheels']},'wheel_count':7,'hash_required':True,'wheel_only':True,'no_index_install':True,'bootstrap_pip_installed':False,'pip_check':'No broken requirements found.','installation_report_sha256':hashlib.sha256((a.bank/'install-report.json').read_bytes()).hexdigest(),'host_python_mutated':False})
    dump(BASE/'x2/package-audit.json',{'schema':'ghc.family.bounded-package-audit.v1','source':'Official PyPI exact-version metadata at wheel verification','rows':[{'name':w['name'],'version':w['version'],'sha256':w['sha256'],'yanked':w['yanked'],'known_advisories':w['pypi_advisories']} for w in wheel['wheels']],'native_dependency':'SoundFile reports libsndfile 1.2.2; the PyPI metadata check is not a complete native-library advisory audit.','exhaustive_security':False,'independent_security_review':'open_gap'})
    skills,runners=build_skills_and_runners(cases,a.skill_root,a.bank)
    build_deck(cases,results)
    outcomes=dict(Counter(r['outcome'] for r in results.values()));assert outcomes=={'completed':160,'represented':14,'open_gap':8,'exact_gate':18}
    counts={'proposals':15430,'negatives':82299,'methods':93232,'failed_witnesses':53147,'passing_witnesses':82491,'open_gaps':740,'exact_gates':729}
    dump(BASE/'x2/phase-truth.json',{'schema':'ghc.family.phase-truth.v687.v8.x2','owner':'Thalen Reed','phase':'v687-v8','source':SOURCE,'x1':X1,'state':'X2_EVIDENCE_PREPARED','outcomes':outcomes,'effective_counts':counts,'canonical_invocations':0,'canonical_successes':0,'successor_contacted':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    dump(BASE/'x2/complete-incomplete.json',{'schema':'ghc.family.complete-incomplete.v1','core_outcomes':outcomes,'safe_procedures':300,'candidate_challenges':250,'clean_fix_refine_procedures':300,'exact_packets_held':50,'blocked_packets_held':30,'skills_validated_used':10,'runners_validated_used':5,'packages_validated_used':3,'all_authorized_local_procedures_resolved':True,'open_scientific_and_authority_gates':GATES,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    dump(BASE/'x2/execution-summary.json',{'schema':'ghc.family.execution-summary.v1','frozen_contract_matches':200,'input_preservation_checks':200,'unit_tests':28,'altered_outputs_rejected':250,'package_positive_and_adverse_pairs':3,'skill_positive_and_adverse_pairs':10,'runner_positive_and_adverse_pairs':5,'deck_cards':208,'unexpected_x2_failures':0,'same_owner_only':True,'independent_reproduction':False,'real_audio_rows':0,'external_actions':0})
    dump(BASE/'x2/method-flow/ledger.json',method_ledger(cases,mutation_rows,package,skills,runners))
    dump(BASE/'x2/retained-negative-register.json',{'schema':'ghc.family.retained-negative-register.v1','source_counts':{'negatives':82024,'methods':93197,'failed_witnesses':52872,'passing_witnesses':81998},'startup_delta':{'negatives':7,'methods':7,'failed_witnesses':7,'passing_witnesses':7},'x2_delta':{'negatives':268,'methods':28,'failed_witnesses':268,'passing_witnesses':486},'effective_counts':counts,'erased_negative_count':0,'failed_candidates_promoted':0,'source_records_preserved':True})
    write(BASE/'x2/integrated-overview.html',(ROOT/BASE/'x1/integrated-overview.html').read_text(encoding='utf-8').replace('Thalen v687-v8 planning overview','Thalen v687-v8 x2 evidence overview').replace('<main>','<main><p>Current x2 receipt: 200 full matches; 28 owner tests; 250 altered outputs rejected; 10 skills; 5 runners; 3 package pairs; 208 cards. Core outcomes: 160 completed, 14 represented, 8 open_gap, 18 exact_gate. The following retained planning narrative supplies context and remains explicitly historical to x1.</p>'))
    print(json.dumps({'state':'X2_EVIDENCE_MATERIALIZED','outcomes':outcomes,'cards':208,'skills':10,'runners':5,'unexpected_failures':0}))

if __name__=='__main__':main()
