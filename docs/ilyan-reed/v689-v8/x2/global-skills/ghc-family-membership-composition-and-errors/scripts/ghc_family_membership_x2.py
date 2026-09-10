"""Counting, retention and interpretation contracts for declared finite records."""
from collections import Counter
from fractions import Fraction
from ghc_family_membership_x1 import ContractError,require,closed,integer,string,bits,positions,encode,mask
FIELDS={'counting_insert':['counts','positions'],'guarded_decrement':['counts','positions','known_member'],'multiplicity_upper_bound':['counts','positions'],'saturation_hold':['counts','positions','cap'],'retained_member_rebuild':['width','records','remove'],'record_union_conflicts':['left','right'],'corruption_witness':['bits','members'],'shard_roundtrip':['bits','block'],'accessible_filter_summary':['tp','fp','tn','fn'],'evidence_reservation':['obligation','kind','evidence','authority']}
def counters(d):
    x=d['counts'];require(type(x) is list and 1<=len(x)<=256,'counter_list_domain')
    for c in x:integer(c)
    return x,Counter(positions(d['positions'],len(x)))
def records(rows,width,unique=False):
    require(type(rows) is list and len(rows)<=64,'record_list_domain');labels=set();out=[]
    for r in rows:
        closed(r,['label','positions']);label=string(r['label']);pos=positions(r['positions'],width)
        if unique:require(label not in labels,'duplicate_record')
        labels.add(label);out.append({'label':label,'positions':list(pos)})
    return out
def compute(op,d):
    if op in ['counting_insert','guarded_decrement','multiplicity_upper_bound','saturation_hold']:counts,freq=counters(d)
    if op=='counting_insert':return [c+freq[i] for i,c in enumerate(counts)]
    if op=='guarded_decrement':
        require(type(d['known_member']) is bool,'known_member_type')
        if not d['known_member']:return {'refused':'unknown_member'}
        if any(counts[p]<n for p,n in freq.items()):return {'refused':'underflow'}
        return {'counts':[c-freq[i] for i,c in enumerate(counts)],'source_retained':True}
    if op=='multiplicity_upper_bound':return {'upper_bound':min(counts[p]//n for p,n in freq.items()),'exact_count_established':False}
    if op=='saturation_hold':
        cap=integer(d['cap'],1);require(max(counts)<=cap,'initial_counter_above_cap');raw=[c+freq[i] for i,c in enumerate(counts)];overflow=[i for i,c in enumerate(raw) if c>cap];return {'counts':[min(c,cap) for c in raw],'overflow_positions':overflow,'decrement_information_preserved':not overflow}
    if op=='retained_member_rebuild':
        width=integer(d['width'],1,256);r=records(d['records'],width,True);remove=string(d['remove'])
        if remove not in [x['label'] for x in r]:return {'refused':'unknown_record'}
        remain=[x for x in r if x['label']!=remove];value=0
        for x in remain:value|=mask(x['positions'])
        return {'bits':encode(value,width),'remaining_labels':[x['label'] for x in remain],'source_retained':True}
    if op=='record_union_conflicts':
        left=records(d['left'],256);right=records(d['right'],256);groups={}
        for r in left+right:
            values=groups.setdefault(r['label'],[])
            if r['positions'] not in values:values.append(list(r['positions']))
        return {'groups':groups,'conflicts':sorted(k for k,v in groups.items() if len(v)>1),'source_retained':True}
    if op=='corruption_witness':
        b,n=bits(d['bits']);members=records(d['members'],n,True);return {'false_negative_labels':[r['label'] for r in members if b&mask(r['positions'])!=mask(r['positions'])],'real_people':0}
    if op=='shard_roundtrip':
        b,n=bits(d['bits']);block=integer(d['block'],1,256);chunks=[]
        for offset in range(0,n,block):
            width=min(block,n-offset);chunks.append({'offset':offset,'bits':encode((b>>offset)&((1<<width)-1),width)})
        return {'chunks':chunks,'reconstructed':''.join(c['bits'] for c in chunks)}
    if op=='accessible_filter_summary':
        for k in ['tp','fp','tn','fn']:integer(d[k])
        den=d['fp']+d['tn'];ratio=str(Fraction(d['fp'],den)) if den else 'undefined (no negative queries)';s='Synthetic queries: TP {tp}; FP {fp}; TN {tn}; FN {fn}. False-positive fraction: '.format(**d)+ratio+'.'
        return {'text':s,'manual_evaluation':'reserved','empirical':False}
    if op=='evidence_reservation':
        string(d['obligation']);require(d['kind'] in ['scientific_evidence','competent_authority'],'obligation_kind');require(d['evidence'] is None and d['authority'] is None,'unsupported_evidence_promotion');return {'obligation':d['obligation'],'state':'open_gap' if d['kind']=='scientific_evidence' else 'exact_gate','evidence':None,'authority':None}
    raise ContractError('unknown_operation')
def evaluate(request):
    try:
        closed(request,['operation','payload'],'unknown_request_field');op=request['operation'];require(type(op) is str and op in FIELDS,'unknown_operation');d=request['payload'];closed(d,FIELDS[op]);v=compute(op,d);outcome='represented' if op=='accessible_filter_summary' else v['state'] if op=='evidence_reservation' else 'completed';return {'ok':True,'operation':op,'outcome':outcome,'value':v}
    except ContractError as e:return {'ok':False,'error':str(e),'original_success_credit':0}
