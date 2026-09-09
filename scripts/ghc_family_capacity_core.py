"""Pure finite capacity models. No task transport or host configuration actions."""
from __future__ import annotations
import argparse
import copy
import json
import pathlib
import re
from fractions import Fraction

class ContractError(ValueError):
    """A stable, public domain rejection code."""

def require(condition,code):
    if not condition: raise ContractError(code)

def integer(value,minimum=0,maximum=1000):
    require(type(value) is int and value>=minimum,'E_INTEGER')
    require(value<=maximum,'E_LIMIT')
    return value

def rational(value):
    require(type(value) in (int,str),'E_RATIONAL')
    text=str(value)
    require(len(text)<=80,'E_LIMIT')
    require(bool(re.fullmatch(r'[+-]?\d+(?:/\d+)?',text)),'E_RATIONAL')
    try: result=Fraction(text)
    except (ValueError,ZeroDivisionError): raise ContractError('E_RATIONAL') from None
    require(max(abs(result.numerator),result.denominator)<=10**30,'E_LIMIT')
    return result

def nonnegative(value):
    result=rational(value);require(result>=0,'E_NONNEGATIVE');return result

def positive(value):
    result=rational(value);require(result>0,'E_POSITIVE');return result

def sequence(value,maximum=1000):
    require(type(value) is list,'E_SHAPE');require(len(value)<=maximum,'E_LIMIT');return value

def label(value):
    require(type(value) is str and bool(value.strip()) and len(value)<=200,'E_LABEL');return value

def fields(value,names):
    require(type(value) is dict and set(value)==set(names),'E_FIELDS')

def pair(value):
    require(type(value) is list and len(value)==2,'E_SHAPE');return value

def typed_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def cycle_slice(cycle,start,count):
    sequence(cycle);require(bool(cycle) and all(type(x) is str and x.strip() for x in cycle),'E_CYCLE')
    integer(start,maximum=10**9);integer(count)
    return [cycle[(start+i)%len(cycle)] for i in range(count)]

def mix_cost(astra_cost):
    a=positive(astra_cost);old=(1+a)/2;new=(2+a)/3
    return dict(old_average=str(old),new_average=str(new),relative_saving=str(1-new/old),measured=False)

def fcfs(jobs):
    sequence(jobs);clock=Fraction(0);prior=Fraction(0);wait=Fraction(0);starts=[];finishes=[]
    for item in jobs:
        a,s=pair(item);a=nonnegative(a);s=nonnegative(s);require(a>=prior,'E_ORDER');prior=a
        start=max(clock,a);clock=start+s;wait+=start-a
        starts.append(str(start));finishes.append(str(clock))
    return dict(starts=starts,finishes=finishes,total_wait=str(wait))

def edd(jobs):
    sequence(jobs);parsed=[]
    for i,item in enumerate(jobs):
        s,d=pair(item);parsed.append((rational(d),i,nonnegative(s)))
    parsed.sort();clock=Fraction(0);late=[];order=[]
    for deadline,i,service in parsed:clock+=service;late.append(clock-deadline);order.append(i)
    return dict(order=order,maximum_lateness=str(max(late,default=Fraction(0))),tardy_jobs=sum(x>0 for x in late))

def ffd(sizes,capacity):
    sequence(sizes);c=positive(capacity);s=[positive(v) for v in sizes]
    require(all(v<=c for v in s),'E_OVERSIZE');bins=[];loads=[]
    for index in sorted(range(len(s)),key=lambda i:(-s[i],i)):
        target=next((j for j,total in enumerate(loads) if total+s[index]<=c),len(loads))
        if target==len(loads):loads.append(Fraction(0));bins.append([])
        loads[target]+=s[index];bins[target].append(index)
    return dict(bins=bins,loads=[str(x) for x in loads],optimality_claimed=False)

def critical_path(durations,edges):
    sequence(durations,200);sequence(edges);d=[nonnegative(x) for x in durations];n=len(d)
    parents=[set() for _ in d];seen=set()
    for item in edges:
        a,b=pair(item);require(type(a) is int and type(b) is int and 0<=a<n and 0<=b<n,'E_VERTEX')
        require((a,b) not in seen,'E_DUPLICATE');seen.add((a,b));parents[b].add(a)
    finished={}
    while len(finished)<n:
        ready=[i for i in range(n) if i not in finished and parents[i]<=finished.keys()]
        require(bool(ready),'E_CYCLE')
        for i in ready:finished[i]=d[i]+max((finished[p] for p in parents[i]),default=Fraction(0))
    return dict(finishes=[str(finished[i]) for i in range(n)],makespan=str(max(finished.values(),default=Fraction(0))))

def token_cost(input_tokens,cached_tokens,output_tokens,rates):
    i=integer(input_tokens,maximum=10**12);c=integer(cached_tokens,maximum=10**12);o=integer(output_tokens,maximum=10**12)
    require(c<=i,'E_CACHE');sequence(rates);require(len(rates)==3,'E_SHAPE');r=[nonnegative(x) for x in rates]
    return dict(cost_units=str((i-c)*r[0]+c*r[1]+o*r[2]),billing_verified=False)

def context_batches(sizes,prefix,limit):
    sequence(sizes);p=integer(prefix,maximum=10**9);l=integer(limit,minimum=1,maximum=10**9)
    require(p<l,'E_CAPACITY');s=[integer(x,minimum=1,maximum=10**9) for x in sizes]
    require(all(p+x<=l for x in s),'E_OVERSIZE');batches=[];totals=[]
    for i,v in enumerate(s):
        if not batches or totals[-1]+v>l:batches.append([]);totals.append(p)
        batches[-1].append(i);totals[-1]+=v
    return dict(batches=batches,totals=totals,truncated=False)

def coverage(intervals,window):
    sequence(intervals);a,b=pair(window);a=rational(a);b=rational(b);require(a<b,'E_WINDOW');segments=[]
    for item in intervals:
        x,y=pair(item);x=rational(x);y=rational(y);require(x<=y,'E_ORDER');x=max(a,x);y=min(b,y)
        if x<y:segments.append((x,y))
    segments.sort();merged=[]
    for x,y in segments:
        if merged and x<=merged[-1][1]:merged[-1]=(merged[-1][0],max(y,merged[-1][1]))
        else:merged.append((x,y))
    gaps=[];cursor=a
    for x,y in merged:
        if cursor<x:gaps.append([str(cursor),str(x)])
        cursor=y
    if cursor<b:gaps.append([str(cursor),str(b)])
    return dict(covered_duration=str(sum((y-x for x,y in merged),Fraction(0))),gaps=gaps)

def fair_quota(weights,total):
    sequence(weights);n=integer(total,maximum=10**9);w=[nonnegative(x) for x in weights]
    require(bool(w) and sum(w)>0,'E_WEIGHT');q=[x*n/sum(w) for x in w];allocation=[x.numerator//x.denominator for x in q]
    for i in sorted(range(len(w)),key=lambda i:(-(q[i]-allocation[i]),i))[:n-sum(allocation)]:allocation[i]+=1
    return dict(allocation=allocation,tie_policy='input_index',rights_determined=False)

OPERATIONS={f.__name__:f for f in [cycle_slice,mix_cost,fcfs,edd,ffd,critical_path,token_cost,context_batches,coverage,fair_quota]}
PARAMETERS={name:tuple(f.__code__.co_varnames[:f.__code__.co_argcount]) for name,f in OPERATIONS.items()}

def evaluate(request,operations=None,parameters=None):
    ops=OPERATIONS if operations is None else operations;params=PARAMETERS if parameters is None else parameters
    try:
        require(type(request) is dict,'E_FIELDS');op=request.get('op');require(type(op) is str and op in ops,'E_OP')
        fields(request,('op',*params[op]));value=ops[op](**{k:copy.deepcopy(request[k]) for k in params[op]})
        return dict(ok=True,value=value,error=None)
    except ContractError as ex:return dict(ok=False,value=None,error=str(ex))

def strict_json(text):
    def object_pairs(pairs):
        result={}
        for k,v in pairs:
            if k in result:raise ContractError('E_DUPLICATE_KEY')
            result[k]=v
        return result
    def invalid_constant(_):raise ContractError('E_NONFINITE')
    return json.loads(text,object_pairs_hook=object_pairs,parse_constant=invalid_constant)

def cli(allowed,evaluator=evaluate):
    ap=argparse.ArgumentParser(description='Bounded local model; no task submission.');ap.add_argument('--input',required=True);ap.add_argument('--output');args=ap.parse_args()
    raw=pathlib.Path(args.input).read_bytes();require(len(raw)<=4_000_000,'E_LIMIT')
    request=strict_json(raw.decode('utf-8-sig'));batch=request if type(request) is list else [request];sequence(batch)
    result=[evaluator(r) if type(r) is dict and type(r.get('op')) is str and r['op'] in allowed else dict(ok=False,value=None,error='E_OP') for r in batch]
    result=result if type(request) is list else result[0];text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'
    if args.output:
        with pathlib.Path(args.output).open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    else:print(text,end='')
