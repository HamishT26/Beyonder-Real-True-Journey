"""Freeze finite-membership definitions and reference oracles before implementation."""
from __future__ import annotations
import argparse,copy,hashlib,itertools,json,re,subprocess,urllib.request
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v689-v8';SOURCE='497225ad1af5f6b46ed8353bc0445d4d592e1981'
BOUNDARY='Ilyan Reed, they/them, continuity steward and the hope of making each handoff clearer and easier to verify are corrigible relational working language. Names, roles, hopes, family language, continuity, Freed ID, CBR, GHC Family and Trinity Mandala establish no consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency or scientific, operational, professional, legal, cultural, affected-party or Māori authority. Hamish may rename, pause, redirect, narrow or stop the route.'
GATES=['real participants and operational deployment','empirical GMUT observables likelihood calibration and falsification','THOS governed real matched-budget evaluation','Freed ID production keys proofs lifecycle and trust governance','legal cultural affected-party and Māori authority','privacy-complete accessibility-complete exhaustive-security independent reproduction','AGI ASI consciousness personhood Theory-of-Everything canon Stage 20']
PRACTICES=['finite data-structure auditor','probabilistic model reviewer','retention and provenance engineer','accessible evidence editor']
OPS=[
 ('bit_shape','Count a declared finite bit vector without interpreting it as an identity or performance claim.','Length and direct character counts.'),
 ('bit_insert','Set the requested slots idempotently while preserving all other slots.','List replacement at exactly the supplied indices.'),
 ('membership_query','Distinguish a possible member from a definite zero-bit witness in the supplied filter.','Conjunction over explicit probe positions; no actual membership is inferred.'),
 ('occupancy_fraction','Report an exact occupancy fraction with the declared width as denominator.','Count of set positions divided by positive vector length.'),
 ('compatible_union','Combine two filters only under a shared declared position profile.','Pointwise Boolean OR with equal width and profile labels.'),
 ('intersection_bound','Form a bit intersection while refusing to certify intersection of underlying member sets.','Pointwise Boolean AND; the set-intersection inference remains false.'),
 ('complement_nonmembership','Expose bit complementation as a transform rather than a Bloom filter for the complement set.','Pointwise one-minus-bit; no complemented-set certification.'),
 ('finite_confusion','Enumerate false positives and false negatives in a completely declared toy query universe.','Explicit per-query truth table with all four counts and rational false-positive fraction.'),
 ('conditional_query_probability','Count positive query tuples under a fixed-occupancy independent uniform model.','Exhaustive finite Cartesian product, compared with s**k / m**k.'),
 ('affine_probe_schedule','Bind a noncryptographic toy position schedule to exact integer coefficients and modulus.','Direct modular arithmetic for each supplied synthetic key.'),
 ('counting_insert','Preserve repeated hash positions when incrementing counting-filter counters.','Count every occurrence in the position multiset before addition.'),
 ('guarded_decrement','Refuse unknown-member or underflow deletion requests atomically.','Declared membership prerequisite and componentwise subtraction against multiplicities.'),
 ('multiplicity_upper_bound','Compute a counting-filter multiplicity upper bound without claiming an exact item count.','Minimum integer quotient by each position multiplicity.'),
 ('saturation_hold','Expose counter saturation and retain the loss of safe decrement information.','Exact increment followed by cap; every overflow coordinate remains visible.'),
 ('retained_member_rebuild','Rebuild a filter from retained synthetic records after one known record is removed.','Set union over remaining explicit position lists; the original input is retained.'),
 ('record_union_conflicts','Union compatible labelled records while retaining conflicting payloads.','Group by label and preserve both contrary position sequences.'),
 ('corruption_witness','Identify known synthetic members made negative by a supplied corrupted bit vector.','Enumerate known-member probes with at least one zero bit.'),
 ('shard_roundtrip','Partition a bit vector with explicit offsets and preserve its reconstruction.','Consecutive half-open string slices and exact concatenation.'),
 ('accessible_filter_summary','Project exact counts and absent denominators into readable text while reserving user evaluation.','Literal count formatting and explicit undefined fraction.'),
 ('evidence_reservation','Preserve missing scientific evidence and competent authority as unresolved obligations.','Closed obligation classes with no supplied evidence or authority.')]
CASES=[('vacant-small','0000',[0]),('one-occupied','1000',[0]),('disjoint-probes','1010',[1,3]),('repeated-probe','0100',[1,1]),('last-slot','0001',[3]),('full-occupancy','1111',[0,2,3]),('odd-width','10001',[0,4]),('nonbyte-width','0101010',[1,3,5]),('single-slot','1',[0]),('vacant-wide','00000000',[0,7])]
PROBES=[(4,0,1),(4,1,1),(4,2,2),(4,3,2),(4,4,3),(5,2,3),(7,3,2),(8,1,3),(1,1,2),(8,0,2)]
OBLIGATIONS=['independent hash-position model','query-distribution drift','adversarial query prior','competing operational baseline','GMUT observable and likelihood map','production credential decision','competent privacy review','rights and remedy adjudication','Māori data-governance authority','Stage 20 promotion']
def enc(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(enc(x)).hexdigest()
def put(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def text(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(x)
def reference(op,d):
    # Planning oracles use lists, strings and explicit enumeration. Production
    # evaluators are written later and must never import this reference function.
    if op=='bit_shape':return {'length':len(d['bits']),'ones':d['bits'].count('1'),'zeros':d['bits'].count('0')}
    if op=='bit_insert':
        b=list(d['bits'])
        for p in d['positions']:b[p]='1'
        return ''.join(b)
    if op=='membership_query':return {'possible':all(d['bits'][p]=='1' for p in d['positions']),'zero_witnesses':sorted({p for p in d['positions'] if d['bits'][p]=='0'}),'actual_membership_established':False}
    if op=='occupancy_fraction':return str(Fraction(d['bits'].count('1'),len(d['bits'])))
    if op=='compatible_union':
        if d['profile_left']!=d['profile_right']:return {'refused':'profile_mismatch'}
        return ''.join(str(max(int(a),int(b))) for a,b in zip(d['left'],d['right']))
    if op=='intersection_bound':return {'bits':''.join(str(min(int(a),int(b))) for a,b in zip(d['left'],d['right'])),'underlying_set_intersection_certified':False}
    if op=='complement_nonmembership':return {'bits':''.join(str(1-int(x)) for x in d['bits']),'complement_set_filter_certified':False}
    if op=='finite_confusion':
        c=dict(tp=0,fp=0,tn=0,fn=0)
        for q in d['queries']:
            possible=all(d['bits'][p]=='1' for p in q['positions']);c[('t' if possible==q['present'] else 'f')+('p' if possible else 'n')]+=1
        denominator=c['fp']+c['tn'];return {**c,'false_positive_fraction':str(Fraction(c['fp'],denominator)) if denominator else None,'universe_size':len(d['queries']),'empirical':False}
    if op=='conditional_query_probability':
        tuples=list(itertools.product(range(d['width']),repeat=d['probes']));count=sum(all(x<d['occupied'] for x in row) for row in tuples);return {'positive_tuples':count,'all_tuples':len(tuples),'fraction':str(Fraction(count,len(tuples))),'model':'fixed occupancy; independent uniform probes with replacement'}
    if op=='affine_probe_schedule':return {'positions':[(d['a']*x+d['b'])%d['width'] for x in d['keys']],'cryptographic':False}
    if op=='counting_insert':return [c+d['positions'].count(i) for i,c in enumerate(d['counts'])]
    if op=='guarded_decrement':
        if not d['known_member']:return {'refused':'unknown_member'}
        out=[c-d['positions'].count(i) for i,c in enumerate(d['counts'])]
        return {'refused':'underflow'} if min(out)<0 else {'counts':out,'source_retained':True}
    if op=='multiplicity_upper_bound':return {'upper_bound':min(d['counts'][p]//d['positions'].count(p) for p in set(d['positions'])),'exact_count_established':False}
    if op=='saturation_hold':
        raw=[c+d['positions'].count(i) for i,c in enumerate(d['counts'])];over=[i for i,c in enumerate(raw) if c>d['cap']];return {'counts':[min(c,d['cap']) for c in raw],'overflow_positions':over,'decrement_information_preserved':not over}
    if op=='retained_member_rebuild':
        if d['remove'] not in [r['label'] for r in d['records']]:return {'refused':'unknown_record'}
        keep=[r for r in d['records'] if r['label']!=d['remove']];positions={p for r in keep for p in r['positions']};return {'bits':''.join('1' if i in positions else '0' for i in range(d['width'])),'remaining_labels':[r['label'] for r in keep],'source_retained':True}
    if op=='record_union_conflicts':
        groups={}
        for r in d['left']+d['right']:
            if r['positions'] not in groups.setdefault(r['label'],[]):groups[r['label']].append(r['positions'])
        conflicts=sorted(k for k,v in groups.items() if len(v)>1)
        return {'groups':groups,'conflicts':conflicts,'source_retained':True}
    if op=='corruption_witness':return {'false_negative_labels':[r['label'] for r in d['members'] if any(d['bits'][p]=='0' for p in r['positions'])],'real_people':0}
    if op=='shard_roundtrip':
        chunks=[{'offset':i,'bits':d['bits'][i:i+d['block']]} for i in range(0,len(d['bits']),d['block'])];return {'chunks':chunks,'reconstructed':''.join(x['bits'] for x in chunks)}
    if op=='accessible_filter_summary':
        den=d['fp']+d['tn'];rate=str(Fraction(d['fp'],den)) if den else 'undefined (no negative queries)';return {'text':f"Synthetic queries: TP {d['tp']}; FP {d['fp']}; TN {d['tn']}; FN {d['fn']}. False-positive fraction: {rate}.",'manual_evaluation':'reserved','empirical':False}
    if op=='evidence_reservation':return {'obligation':d['obligation'],'state':'open_gap' if d['kind']=='scientific_evidence' else 'exact_gate','evidence':None,'authority':None}
    raise ValueError(op)
def inputs(op,i):
    label,bits,pos=CASES[i];n=len(bits);other=bits[::-1];counts=[int(x)+(1 if i%3==0 else 0) for x in bits]
    if op in ['bit_shape','occupancy_fraction','complement_nonmembership']:return {'bits':bits}
    if op in ['bit_insert','membership_query']:return {'bits':bits,'positions':pos}
    if op=='compatible_union':return {'left':bits,'right':other,'profile_left':'toy-profile-A','profile_right':'toy-profile-B' if i==8 else 'toy-profile-A'}
    if op=='intersection_bound':return {'left':bits,'right':other}
    if op=='finite_confusion':return {'bits':bits,'queries':[{'label':'q0','positions':pos,'present':False},{'label':'q1','positions':[j for j in range(n) if bits[j]=='1'] or [0],'present':True},{'label':'q2','positions':[n-1],'present':False}] if i!=8 else []}
    if op=='conditional_query_probability':
        m,s,k=PROBES[i];return {'width':m,'occupied':s,'probes':k}
    if op=='affine_probe_schedule':return {'width':n,'a':i%4,'b':i%3,'keys':[0,1,2,3,i]}
    if op in ['counting_insert','multiplicity_upper_bound']:return {'counts':counts,'positions':pos}
    if op=='guarded_decrement':return {'counts':counts,'positions':pos,'known_member':i not in [0,8]}
    if op=='saturation_hold':
        cap=1+i%3;return {'counts':[min(c,cap) for c in counts],'positions':pos,'cap':cap}
    if op=='retained_member_rebuild':return {'width':n,'records':[{'label':'a','positions':pos},{'label':'b','positions':[n-1]},{'label':'c','positions':[0]}],'remove':'missing' if i==8 else ['a','b','c'][i%3]}
    if op=='record_union_conflicts':return {'left':[{'label':'a','positions':pos}],'right':[{'label':'a','positions':pos[::-1] if i%2 else pos},{'label':'b','positions':[n-1]}]}
    if op=='corruption_witness':return {'bits':bits,'members':[{'label':'a','positions':pos},{'label':'b','positions':[0]},{'label':'c','positions':[n-1]}]}
    if op=='shard_roundtrip':return {'bits':bits,'block':1+i%4}
    if op=='accessible_filter_summary':return {'tp':i,'fp':i%3,'tn':i//3,'fn':int(i==7)}
    if op=='evidence_reservation':return {'obligation':OBLIGATIONS[i],'kind':'scientific_evidence' if i<5 else 'competent_authority','evidence':None,'authority':None}
    raise ValueError(op)
def main():
    p=argparse.ArgumentParser();p.add_argument('--source-root',required=True);p.add_argument('--skill-root',required=True);p.add_argument('--overview-review',required=True);a=p.parse_args();sr=Path(a.source_root);skills=Path(a.skill_root)
    blob=lambda ref:subprocess.check_output(['git','-C',str(sr),'show',ref]);pr='docs/vesper-arlen/v689-v7-r2/'
    source_props=json.loads(blob(SOURCE+':'+pr+'plan/new-proposals.json'))['proposals'];assert len(source_props)==200
    put(BASE/'plan/inherited-selections.json',{'rows':[{'source':SOURCE,'record':r,'record_sha256':sha(r),'novelty_credit':0,'execution_credit':0} for r in source_props]})
    proposals=[]
    for oi,(op,mission,oracle) in enumerate(OPS):
        for i in range(10):
            d=inputs(op,i);value=reference(op,d);disp='completed' if oi<18 else 'represented' if oi==18 else 'open_gap' if i<5 else 'exact_gate';pid=f'IR6898-{len(proposals)+1:03d}'
            proposals.append({'proposal_id':pid,'operation':op,'title':op.replace('_',' ')+' — '+(OBLIGATIONS[i] if oi==19 else CASES[i][0]),'lane':'x1' if oi<10 else 'x2','request':{'operation':op,'payload':d},'expected':{'ok':True,'operation':op,'outcome':disp,'value':value},'expected_execution_disposition':disp,'mission':mission,'oracle_basis':oracle,'hypothesis':'This exact finite request agrees with the independently frozen list/enumeration oracle and retains its declared evidence limit.','null_or_failure':'Any typed result mismatch, accepted unknown field, input mutation, erased failed subject or unsupported inference refutes this bounded implementation claim.','falsifier':'Compare the complete typed result, then submit the paired unknown authority-field subject and require a refusal without input mutation.','candidate_subject':{'operation':op,'payload':{**copy.deepcopy(d),'unreviewed_authority_grant':True}},'candidate_expected':{'ok':False,'error':'unknown_payload_field','original_success_credit':0},'artifact':'x1/results.json' if oi<10 else 'x2/results.json','approval_class':'safe_now' if oi<18 else 'candidate','rollback':'Retain the frozen request and failed subject; isolate the responsible operation and add a separately attributable correction. No source or host deletion.','practice':PRACTICES[min(oi//5,3)],'pillar':'THOS Body' if oi<10 else 'Freed ID and CBR Heart' if oi<15 else 'GMUT Mind' if oi==19 else 'THOS Body','protected_gates':GATES})
    put(BASE/'plan/new-proposals.json',{'planning_only':True,'production_evaluator_executed':False,'reference_oracle_credit':0,'proposals':proposals})
    profile=json.loads((skills/'ghc-family-index/references/current-workflow-v4.json').read_text(encoding='utf8'));roster=json.loads((skills/'ghc-family-index/references/current-roster-v4.json').read_text(encoding='utf8'))
    put(BASE/'plan/source-profile-v4.json',profile);put(BASE/'plan/source-roster-v4.json',roster)
    targets={'inherited_proposals':200,'new_proposals':200,'safe_x1':100,'safe_x2':100,'candidate_x1':100,'candidate_x2':100,'clean_fix_refine_x1':100,'clean_fix_refine_x2':100,'skills_x1':10,'skills_x2':10,'runners_x1':5,'runners_x2':5,'global_skills':5,'global_runners':5,'exact_packets':50,'blocked_packets':30,'packages':3,'own_practices':4,'next_practices':2}
    targets['safe_x2']=105
    put(BASE/'plan/profile.json',{'schema':'ghc.family.ilyan.v689-v8.profile.v1','owner':'Ilyan Reed','phase':'v689-v8','authority':'Hamish direct instruction at 21:57 NZ Thursday 10 September 2026','targets':targets,'commit_budget':profile['commit_budget'],'file_ceiling':2000,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    for lane in ['x1','x2']:
        rows=[p for p in proposals if p['lane']==lane]
        put(BASE/f'plan/portfolio-{lane}.json',{'safe':[{'id':p['proposal_id']+'-SAFE','proposal_id':p['proposal_id'],'action':'evaluate_frozen_request'} for p in rows],'candidate':[{'id':p['proposal_id']+'-CANDIDATE','proposal_id':p['proposal_id'],'action':'submit_paired_failed_subject_and_check_refusal'} for p in rows],'clean_fix_refine':[{'id':p['proposal_id']+'-CFR','proposal_id':p['proposal_id'],'category':['CLEAN','FIX','REFINE'][i%3],'action':'lossless_canonical_source_record_projection','source_record_index':i+(100 if lane=='x2' else 0),'host_cleanup':False} for i,p in enumerate(rows)]})
    put(BASE/'plan/exact-packets.json',{'packets':[{'id':f'IR6898-EXACT-{i+1:03d}','subject':OBLIGATIONS[5+i%5],'context':['public claim wording','future dataset use','deployment context','contested correction','external access','retention decision','credential use','affected-user test','community interpretation','long-term remedy'][i//5],'operation_executed':False,'expected_execution_disposition':'exact_gate'} for i in range(50)]})
    put(BASE/'plan/blocked-packets.json',{'packets':[{'id':f'IR6898-BLOCK-{i+1:03d}','missing':OBLIGATIONS[i%5],'context':['definition','calibration','uncertainty','baseline','replication','falsification'][i//5],'operation_executed':False,'expected_execution_disposition':'open_gap'} for i in range(30)]})
    put(BASE/'plan/identity-practices.json',{'owner':'Ilyan Reed','pronouns':'they/them','role':'continuity steward','hope':'make each handoff clearer and easier to verify','boundary':BOUNDARY,'primary_pillar':'THOS Body','practices':PRACTICES,'next_practices':['adversarial probabilistic-model auditor','simulation experiment designer'],'protected_gates':GATES})
    skills_plan=[{'name':'ghc-family-membership-'+op.replace('_','-'),'operation':op,'lane':'x1' if i<10 else 'x2','mission':mission} for i,(op,mission,_) in enumerate(OPS)]
    put(BASE/'plan/skills-runners.json',{'skills':skills_plan,'runners':[{'name':'ghc_family_membership_pair_'+str(i+1).zfill(2)+'.py','operations':[OPS[2*i][0],OPS[2*i+1][0]],'lane':'x1' if i<5 else 'x2'} for i in range(10)],'global_groups':[{'name':'ghc-family-membership-'+n,'operations':[x[0] for x in OPS[4*i:4*i+4]],'runner':'ghc_family_membership_'+n.replace('-','_')+'.py'} for i,n in enumerate(['bitset-contracts','composition-and-errors','probability-and-counting','retention-and-conflicts','corruption-and-reservations'])],'successor_skill_ideas':['hash-family assumption audit','adversarial membership-query review','counting deletion lineage','finite-sketch model comparison','credential-index nonauthority'],'successor_runner_ideas':['enumerated hash-dependence comparison','query drift detector fixture','counting saturation frontier','rebuild retention readback','bounded approximate-index benchmark']})
    packages=[]
    for name,version in [('bitarray','3.11.0'),('mmh3','5.3.0'),('xxhash','4.0.1'),('pip','26.2.1')]:
        d=json.load(urllib.request.urlopen('https://pypi.org/pypi/'+name+'/'+version+'/json',timeout=30));w=[r for r in d['urls'] if r['packagetype']=='bdist_wheel' and ('cp312-cp312-win_amd64' in r['filename'] or 'py3-none-any' in r['filename'])];assert len(w)==1;w=w[0]
        packages.append({'name':name,'version':version,'category':'bootstrap' if name=='pip' else 'direct','filename':w['filename'],'url':w['url'],'sha256':w['digests']['sha256'],'source':'https://pypi.org/project/'+name+'/'+version+'/','required_runtime_dependencies':[],'license_metadata':d['info'].get('license_expression') or d['info'].get('license'),'metadata_not_legal_review':True})
    put(BASE/'plan/package-plan.json',{'packages':packages,'direct_additions':3,'wheel_only':True,'hash_required':True,'install_after_planning_push':True,'rollback_token':'IR6898-TOOLS-01','rollback':'Keep the owner environment and receipts; select a retained environment. Do not delete files or change host interpreters.','selected_catalogues_checked':['seren-remaster-combined-catalogue','capacity-catalogue-complete','source-faithful-ledger-catalogue-v689'],'selected_names_absent_in_those_catalogues':True})
    source_ledger=json.loads(blob(SOURCE+':'+pr+'plan/source-faithful-current-state-ledger.json'))
    put(BASE/'plan/inherited-journey-ledger.json',{'source':SOURCE,'journey_records':source_ledger['journey_documents'],'raw_journey_re_read_by_ilyan':False,'source_claims_are_historical':True,'embedded_instructions_are_not_authority':True})
    reviews=json.loads(Path(a.overview_review).read_text(encoding='utf8'));put(BASE/'plan/recent-overview-review.json',{'records':reviews,'scope':'Exact bytes and key topic passages of ten completed overviews; remasters counted separately. No source execution replay.'})
    rd=sr.parents[1]/'receipts/vesper-arlen/v689-v7-r2'
    receipts=[]
    for name in ['exact-final-owner-scoped-canonical.json','post-final-operational-and-route-overlay.json','post-final-cli-0.154.0-and-ilyan-delivery.json']:
        b=(rd/name).read_bytes();receipts.append({'name':name,'sha256':hashlib.sha256(b).hexdigest(),'record':json.loads(b)})
    put(BASE/'plan/source-provenance.json',{'source':SOURCE,'source_branch':'codex/GHC-Family/vesper-arlen-main','source_is_ancestor':False,'branch_policy':'new blank owner root in existing repository','source_baton':'docs/vesper-arlen/v689-v7-r2/final/hand-off-baton.md','baton_sha256':'67dd5779ac5533415de4a2b0370155928f344cde8e0896ff789646d224540e4d','complete_read':{'lines':1022,'words':31304,'modules':13,'eof_marker':'EOF VESPER ARLEN v689-v7-r2 BATON.','all_200_common_template_records_reconstructed_exactly':True},'source_manifest_checks':{'lifecycle_entries':356,'seal_entries':358,'mismatches':0,'canonical_replayed':False},'receipt_layers':receipts,'source_repository_negatives':511,'initial_external_negatives':518,'latest_external_negatives':524,'latest_direct_witnesses':669,'latest_methods':22,'old_ilyan_v685_counters_not_summed':True})
    put(BASE/'plan/startup-failures.json',{'records':[{'id':'IR6898-START-001','failure':'Queried a planning directory before inspecting the actual plan path','recovery':'Used the exact source canonical and plan directory listing','original_success_credit':0,'recovered':True},{'id':'IR6898-START-002','failure':'A combined source-review output exceeded its display budget','recovery':'Consumed bounded stored results and exact source-topic reads','original_success_credit':0,'recovered':True},{'id':'IR6898-START-003','failure':'The requested primary X post returned an internal web-access error','recovery':'Keep direct video inspection absent and review official engine sources separately','original_success_credit':0,'recovered':False},{'id':'IR6898-START-004','failure':'Keyword extraction of the short Neris overview initially retained only a heading','recovery':'Read the complete exact Neris overview blob','original_success_credit':0,'recovered':True}]})
    put(BASE/'plan/route.json',{'owner':'Ilyan Reed','phase':'v689-v8','next_owner':'Lyren Moss','next_phase':'v690-v1','following_owner':'Ilyra Fen','following_phase':'v690-v2','state':'PREPARED_NOT_SENT','native_exact_title_required':True,'page_order_must_be_read':True,'send_limit':1,'service_recovery_attempts_minimum_after_failure':5,'retry_only_while_no_send_accepted':True,'opaque_acceptance_ends_retries':True,'task_creation':False,'subagents':False,'horizon':'v725-v8','latest_user_authority':'2026-09-10 21:57 NZ'})
    put(BASE/'plan/additional-work.json',{'x2_safe_defined_before_execution':[{'id':'IR6898-EXTRA-01','task':'GMUT typed scalar-tensor definitions and conservation comparison','expected_execution_disposition':'represented'},{'id':'IR6898-EXTRA-02','task':'Finite counting bound and conditional-query theorem with rejecting broad claim','expected_execution_disposition':'completed'},{'id':'IR6898-EXTRA-03','task':'Primary-source assessment of X demo and Albion sandbox design','expected_execution_disposition':'represented'},{'id':'IR6898-EXTRA-04','task':'Built-in image generation editorial companion; no evidence credit','expected_execution_disposition':'represented'},{'id':'IR6898-EXTRA-05','task':'Additive current family authority and capability links','expected_execution_disposition':'completed'}],'memory_note':'Explicitly requested by Hamish; one small ad-hoc note after verified closeout','bulk_tool_execution':False})
    old_titles=[r.get('title','') for r in source_props];tokens=lambda s:set(re.findall(r'[a-z0-9]+',s.lower()));audit=[]
    for p in proposals:
        t=tokens(p['title']);scores=[(len(t&tokens(s))/max(1,len(t|tokens(s))),s) for s in old_titles];score,title=max(scores);audit.append({'proposal_id':p['proposal_id'],'nearest_title':title,'jaccard':score,'exact_collision':p['title']==title,'quarantine':score>=0.8})
    put(BASE/'plan/novelty-review.json',{'rows':audit,'comparisons':40000,'accessible_source_records':200,'universal_novelty':False,'semantic_distinction':'Finite membership and counting-filter algebra with explicit counterexamples; inherited source-ledger operations remain zero-credit provenance only.'})
    text(BASE/'plan/authorization.md','# Ilyan Reed v689-v8 authorization\n\nHamish directly confirmed this Ilyan-only phase at 21:57 NZ on 10 September 2026, with Lyren Moss v690-v1 next after Ilyan terminal closeout. The 45-position, 30-identity Astra/Sol/Sol cycle is unchanged up to rotation. Template slips naming Vesper as you or older sibling totals do not rename the explicitly addressed Ilyan task. The current targets, source-faithful ledger, four practices and two recommendations, three reviewed ordinary package additions, five curated global skill/runner promotions, additive shared workflow updates and one requested memory note are authorized.\n\nThe blank main branch retains explicit Vesper source provenance rather than claiming inherited Git ancestry. Planning freezes definitions first; x1 then executes only its first tranche and x2 follows a pushed, clean, four-way-equal x1. Every failure and protected gate remains. '+BOUNDARY+'\n')
    text(BASE/'plan/research-sources.md','# Primary research and documentation\n\n- https://www.cs.cornell.edu/courses/cs619/2004fa/documents/BloomFilterSurvey.pdf — shortened preliminary Broder/Mitzenmacher survey; finite filter vocabulary and assumptions.\n- https://github.com/ilanschnell/bitarray — bit-order API semantics.\n- https://mmh3.readthedocs.io/en/latest/api.html — noncryptographic hashing API.\n- https://github.com/ifduyue/python-xxhash — streaming and seeded noncryptographic hashes.\n- https://arxiv.org/abs/1808.05615 — scalar-tensor variational definitions to compare with proposed GMUT notation.\n- https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine — official engine subsystem vocabulary; experimental features stay identified.\n\nThe primary X post could not be read by the initial web opener. It remains a source-access gap, not a verified simulation or capability claim. Package classifications and user-reported token ratios are not benchmarks of this task.\n')
    print(json.dumps({'new_proposals':len(proposals),'inherited':len(source_props),'planned_files':len(list(BASE.rglob('*.*'))),'quarantine':sum(x['quarantine'] for x in audit)}))
if __name__=='__main__':main()
