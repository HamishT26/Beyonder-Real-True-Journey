"""Finite inference and review models with explicit conditional assumptions."""
import copy
from fractions import Fraction
from ghc_family_capacity_core import require,integer,rational,nonnegative,positive,sequence,label,fields,pair,ContractError
from ghc_family_capacity_core import evaluate as dispatch

def binary(values):
    sequence(values,64);require(all(type(x) is int and x in (0,1) for x in values),'E_BINARY');return values

def probability(value):
    p=rational(value);require(0<=p<=1,'E_PROBABILITY');return p

def vector(values):
    sequence(values,32);require(bool(values),'E_SHAPE');p=[probability(v) for v in values]
    require(sum(p)==1,'E_PROBABILITY');return p

def matrix(values):
    sequence(values,32);require(bool(values),'E_SHAPE');rows=[]
    for row in values:sequence(row,32);require(bool(row),'E_SHAPE');rows.append([rational(x) for x in row])
    require(all(len(row)==len(rows[0]) for row in rows),'E_SHAPE');return rows

def beta_update(alpha,beta,outcomes):
    a=integer(alpha,maximum=10**9);b=integer(beta,maximum=10**9);require(a>0 and b>0,'E_POSITIVE');x=binary(outcomes)
    a+=sum(x);b+=len(x)-sum(x)
    return dict(alpha=a,beta=b,mean=str(Fraction(a,a+b)),variance=str(Fraction(a*b,(a+b)**2*(a+b+1))),empirical=False)

def lr_path(null,alternative,outcomes):
    p=rational(null);q=rational(alternative);require(0<p<1 and 0<q<1,'E_INTERIOR');x=binary(outcomes)
    value=Fraction(1);path=['1']
    for bit in x:value*=q/p if bit else (1-q)/(1-p);path.append(str(value))
    return dict(path=path,null_assumption='conditional_Bernoulli',empirical=False)

def channel_joint(prior,channel):
    p=vector(prior);k=matrix(channel);require(len(p)==len(k),'E_SHAPE')
    require(all(all(x>=0 for x in row) and sum(row)==1 for row in k),'E_PROBABILITY')
    joint=[[p[i]*x for x in row] for i,row in enumerate(k)]
    observation=[sum((row[j] for row in joint),Fraction(0)) for j in range(len(k[0]))]
    return dict(joint=[[str(x) for x in row] for row in joint],observation=[str(x) for x in observation])

def bayes_risk(joint,loss):
    j=matrix(joint);l=matrix(loss);require(len(j)==len(l),'E_SHAPE')
    require(all(x>=0 for row in j for x in row) and sum(sum(row) for row in j)==1,'E_PROBABILITY')
    require(all(x>=0 for row in l for x in row),'E_NONNEGATIVE');total=Fraction(0);choices=[]
    for observation in range(len(j[0])):
        risks=[sum((j[state][observation]*l[state][action] for state in range(len(j))),Fraction(0)) for action in range(len(l[0]))]
        minimum=min(risks);total+=minimum;choices.append([a for a,r in enumerate(risks) if r==minimum])
    return dict(minimizers=choices,risk=str(total),public_decision=False)

def checkpoint(events):
    sequence(events);digests={};states={};allowed={'prepared','accepted','failed','unknown'}
    for item in events:
        require(type(item) is list and len(item)==3,'E_SHAPE');packet,digest,state=item
        label(packet);label(digest);require(type(state) is str and state in allowed,'E_STATUS')
        require(packet not in digests or digests[packet]==digest,'E_CONFLICT')
        old=states.get(packet)
        require(old!='accepted' or state=='accepted','E_TERMINAL')
        require(old!='unknown' or state in ('unknown','accepted'),'E_TERMINAL')
        digests[packet]=digest;states[packet]=state
    return dict(states=states,messages_sent=0)

def consent_scope(subject,purpose,now,grant):
    label(subject);label(purpose);integer(now,maximum=10**12)
    fields(grant,['subject','purposes','expires','revoked']);label(grant['subject']);sequence(grant['purposes'])
    for p in grant['purposes']:label(p)
    require(len(grant['purposes'])==len(set(grant['purposes'])),'E_DUPLICATE')
    require(type(grant['revoked']) is bool,'E_BOOLEAN');integer(grant['expires'],maximum=10**12)
    eligible=grant['subject']==subject and purpose in grant['purposes'] and not grant['revoked'] and now<grant['expires']
    return dict(model_eligible=eligible,real_consent_verified=False)

def appeal_cover(decisions,reviewers,conflicts):
    sequence(decisions);sequence(conflicts)
    for d in decisions:label(d)
    require(len(decisions)==len(set(decisions)),'E_DUPLICATE');require(type(reviewers) is dict,'E_SHAPE')
    require(set(reviewers)<=set(decisions),'E_REFERENCE')
    for rs in reviewers.values():
        sequence(rs)
        for r in rs:label(r)
        require(len(rs)==len(set(rs)),'E_DUPLICATE')
    blocked=set()
    for c in conflicts:
        d,r=pair(c);label(d);label(r);require(d in decisions,'E_REFERENCE');blocked.add((d,r))
    gaps=[d for d in decisions if not any((d,r) not in blocked for r in reviewers.get(d,[]))]
    return dict(uncovered=gaps,legitimacy_verified=False)

def retry_budget(failure_probability,max_attempts,base_delay):
    p=probability(failure_probability);n=integer(max_attempts,maximum=64);d=integer(base_delay,maximum=10**9)
    return dict(expected_attempts=str(sum((p**i for i in range(n)),Fraction(0))),exhaustion_probability=str(p**n),delays=[d*2**i for i in range(max(0,n-1))],submissions=0)

def record_projection(record,path):
    sequence(path,64);value=record
    for segment in path:
        require(type(segment) in (str,int) and not (type(segment) is int and segment<0),'E_SEGMENT')
        if type(value) is dict:
            require(type(segment) is str,'E_SEGMENT');require(segment in value,'E_MISSING');value=value[segment]
        elif type(value) is list:
            require(type(segment) is int,'E_SEGMENT');require(segment<len(value),'E_MISSING');value=value[segment]
        else:raise ContractError('E_PATH')
    return dict(present=True,value=copy.deepcopy(value))

def paired_gain(before,after,same_workload_and_results):
    sequence(before);sequence(after);require(bool(before) and len(before)==len(after),'E_SHAPE')
    require(type(same_workload_and_results) is bool,'E_BOOLEAN');a=[positive(x) for x in before];b=[nonnegative(x) for x in after]
    if not same_workload_and_results:return dict(cost_ratio=None,saving=None,comparable=False)
    ratio=sum(b)/sum(a);return dict(cost_ratio=str(ratio),saving=str(1-ratio),comparable=True)

OPERATIONS={f.__name__:f for f in [beta_update,lr_path,channel_joint,bayes_risk,checkpoint,consent_scope,appeal_cover,retry_budget,record_projection,paired_gain]}
PARAMETERS={name:tuple(f.__code__.co_varnames[:f.__code__.co_argcount]) for name,f in OPERATIONS.items()}
def evaluate(request):return dispatch(request,OPERATIONS,PARAMETERS)
