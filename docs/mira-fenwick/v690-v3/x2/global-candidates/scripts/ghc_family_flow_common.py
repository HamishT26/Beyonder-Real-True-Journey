"""Closed finite-network input contracts and nonmutating CLI transport."""
import argparse
import copy
import hashlib
import json
import math
import re
from pathlib import Path

class Refusal(ValueError):
    """A stable refusal within the declared finite software domain."""

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def typed_equal(a,b):
    return canonical(a)==canonical(b)

def json_domain(value,depth=0,budget=None):
    if budget is None:budget=[20000]
    budget[0]-=1
    if depth>40 or budget[0]<0:raise Refusal('work_limit')
    if value is None or type(value) in (bool,int):return
    if type(value) is float:
        if not math.isfinite(value):raise Refusal('invalid_json')
        return
    if type(value) is str:
        if len(value)>100000:raise Refusal('work_limit')
        try:value.encode('utf-8')
        except UnicodeEncodeError:raise Refusal('invalid_json') from None
        return
    if type(value) is list:
        for v in value:json_domain(v,depth+1,budget)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for k,v in value.items():json_domain(k,depth+1,budget);json_domain(v,depth+1,budget)
        return
    raise Refusal('invalid_json')

def closed(request,required):
    json_domain(request)
    if type(request) is not dict:raise Refusal('invalid_request')
    if set(request)-set(required):raise Refusal('unknown_field')
    if set(required)-set(request):raise Refusal('missing_field')

def graph_record(graph):
    if type(graph) is not dict or set(graph)!={'nodes','arcs'}:raise Refusal('graph_fields')
    nodes,arcs=graph['nodes'],graph['arcs']
    if type(nodes) is not list or not 2<=len(nodes)<=8:raise Refusal('vertex_count')
    if any(type(v) is not str or not re.fullmatch(r'[a-z][a-z0-9]{0,15}',v) for v in nodes):raise Refusal('invalid_vertex')
    if len(set(nodes))!=len(nodes):raise Refusal('duplicate_vertex')
    if 's' not in nodes or 't' not in nodes:raise Refusal('terminals_required')
    if type(arcs) is not list or len(arcs)>12:raise Refusal('arc_count')
    seen=set()
    for arc in arcs:
        if type(arc) is not list or len(arc)!=3:raise Refusal('arc_shape')
        u,v,c=arc
        if type(u) is not str or type(v) is not str or u not in nodes or v not in nodes:raise Refusal('undeclared_vertex')
        if u==v:raise Refusal('self_arc_reserved')
        if type(c) is not int or not 0<=c<=8:raise Refusal('invalid_capacity')
        if (u,v) in seen:raise Refusal('duplicate_arc')
        seen.add((u,v))
    return copy.deepcopy(graph)

def flow_vector(graph,flow):
    if type(flow) is not list or len(flow)!=len(graph['arcs']):raise Refusal('flow_shape')
    if any(type(v) is not int or not 0<=v<=96 for v in flow):raise Refusal('invalid_flow')
    return list(flow)

def balances(graph,flow):
    result={v:0 for v in graph['nodes']}
    for (u,v,_),amount in zip(graph['arcs'],flow):result[u]+=amount;result[v]-=amount
    return [result[v] for v in graph['nodes']]

def feasible(graph,flow):
    flow_vector(graph,flow)
    if any(f>arc[2] for arc,f in zip(graph['arcs'],flow)):return False
    balance=dict(zip(graph['nodes'],balances(graph,flow)))
    return balance['s']>=0 and balance['t']==-balance['s'] and all(v==0 for k,v in balance.items() if k not in ('s','t'))

def flow_value(graph,flow):
    if not feasible(graph,flow):raise Refusal('infeasible_flow')
    return balances(graph,flow)[graph['nodes'].index('s')]

def accepted(value):return {'accepted':True,'result':value,'error':None}
def rejected(code):return {'accepted':False,'result':None,'error':code}

def load_json(text):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise Refusal('duplicate_json_field')
            result[k]=v
        return result
    def bad_constant(_):raise Refusal('invalid_json')
    value=json.loads(text,object_pairs_hook=pairs,parse_constant=bad_constant)
    json_domain(value)
    return value

def cli(evaluate,operations):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        if args.input.stat().st_size>1000000:raise Refusal('work_limit')
        request=load_json(args.input.read_text(encoding='utf-8'))
        if type(request) is not dict or request.get('op') not in operations:raise Refusal('outside_runner_group')
        result=evaluate(request)
    except Refusal as e:result=rejected(str(e))
    except (UnicodeError,json.JSONDecodeError):result=rejected('invalid_json')
    raw=canonical(result)+b'\n'
    if args.output:
        with args.output.open('xb') as out:out.write(raw)
    else:print(raw.decode('utf-8'),end='')
    return 0 if result['accepted'] else 2
