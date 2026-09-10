"""Closed finite bitset contracts. No world, identity or authorization decisions."""
from __future__ import annotations
from fractions import Fraction
FIELDS={'bit_shape':['bits'],'bit_insert':['bits','positions'],'membership_query':['bits','positions'],'occupancy_fraction':['bits'],'compatible_union':['left','right','profile_left','profile_right'],'intersection_bound':['left','right'],'complement_nonmembership':['bits'],'finite_confusion':['bits','queries'],'conditional_query_probability':['width','occupied','probes'],'affine_probe_schedule':['width','a','b','keys']}
class ContractError(ValueError):pass
def require(ok,code):
    if not ok:raise ContractError(code)
def closed(x,fields,code='unknown_payload_field'):
    require(type(x) is dict,'payload_type');require(not(set(x)-set(fields)),code);require(set(fields)<=set(x),'missing_payload_field')
def integer(x,low=0,high=1000000):require(type(x) is int and low<=x<=high,'integer_domain');return x
def string(x):require(type(x) is str and bool(x.strip()) and len(x)<=128,'string_domain');return x
def bits(x):
    require(type(x) is str and 1<=len(x)<=256 and set(x)<={'0','1'},'bit_vector_domain');return int(x[::-1],2),len(x)
def encode(value,width):return format(value,'0'+str(width)+'b')[::-1]
def positions(x,width):
    require(type(x) is list and 1<=len(x)<=64,'position_list_domain')
    for p in x:integer(p,0,width-1)
    return x
def mask(pos):return sum(1<<p for p in set(pos))
def compute(op,d):
    if 'bits' in d:b,n=bits(d['bits'])
    if 'positions' in d:pos=positions(d['positions'],n)
    if op=='bit_shape':return {'length':n,'ones':b.bit_count(),'zeros':n-b.bit_count()}
    if op=='bit_insert':return encode(b|mask(pos),n)
    if op=='membership_query':return {'possible':(b&mask(pos))==mask(pos),'zero_witnesses':sorted(p for p in set(pos) if not b&(1<<p)),'actual_membership_established':False}
    if op=='occupancy_fraction':return str(Fraction(b.bit_count(),n))
    if op in ['compatible_union','intersection_bound']:
        left,n=bits(d['left']);right,m=bits(d['right']);require(n==m,'width_mismatch')
        if op=='compatible_union':
            string(d['profile_left']);string(d['profile_right'])
            if d['profile_left']!=d['profile_right']:return {'refused':'profile_mismatch'}
            return encode(left|right,n)
        return {'bits':encode(left&right,n),'underlying_set_intersection_certified':False}
    if op=='complement_nonmembership':return {'bits':encode(((1<<n)-1)^b,n),'complement_set_filter_certified':False}
    if op=='finite_confusion':
        require(type(d['queries']) is list and len(d['queries'])<=64,'query_list_domain');c={'tp':0,'fp':0,'tn':0,'fn':0};labels=set()
        for q in d['queries']:
            closed(q,['label','positions','present']);label=string(q['label']);require(label not in labels,'duplicate_query');labels.add(label);require(type(q['present']) is bool,'truth_type');pm=mask(positions(q['positions'],n));possible=(b&pm)==pm
            if q['present']:c['tp' if possible else 'fn']+=1
            else:c['fp' if possible else 'tn']+=1
        den=c['fp']+c['tn'];return {**c,'false_positive_fraction':str(Fraction(c['fp'],den)) if den else None,'universe_size':len(labels),'empirical':False}
    if op=='conditional_query_probability':
        m=integer(d['width'],1,16);s=integer(d['occupied'],0,m);k=integer(d['probes'],1,5)
        return {'positive_tuples':s**k,'all_tuples':m**k,'fraction':str(Fraction(s**k,m**k)),'model':'fixed occupancy; independent uniform probes with replacement'}
    if op=='affine_probe_schedule':
        m=integer(d['width'],1,256);a=integer(d['a']);c=integer(d['b']);require(type(d['keys']) is list and len(d['keys'])<=64,'key_list_domain');keys=[integer(x,-1000000,1000000) for x in d['keys']]
        return {'positions':[(a*x+c)%m for x in keys],'cryptographic':False}
    raise ContractError('unknown_operation')
def evaluate(request):
    try:
        closed(request,['operation','payload'],'unknown_request_field');op=request['operation'];require(type(op) is str and op in FIELDS,'unknown_operation');d=request['payload'];closed(d,FIELDS[op]);value=compute(op,d)
        return {'ok':True,'operation':op,'outcome':'completed','value':value}
    except ContractError as e:return {'ok':False,'error':str(e),'original_success_credit':0}
