"""Bounded JSON Pointer selectors and strict synthetic evidence envelopes.

String pointers only; URI fragments and filesystem paths are not interpreted.
Limits are an owner software profile, not a conformance or security certificate.
"""
import argparse
import copy
import hashlib
import json
import math
import re
from pathlib import Path

class Refusal(ValueError):
    """A stable, intentional domain refusal."""

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def check_json(value, depth=0, budget=None):
    if budget is None: budget=[10000]
    budget[0]-=1
    if depth>64 or budget[0]<0: raise Refusal('input_limit')
    if value is None or type(value) in (bool,int): return
    if type(value) is float and math.isfinite(value): return
    if type(value) is str:
        try: value.encode('utf-8')
        except UnicodeEncodeError: raise Refusal('invalid_unicode') from None
        if len(value)>100000: raise Refusal('input_limit')
        return
    if type(value) is list:
        for child in value: check_json(child,depth+1,budget)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for k,v in value.items(): check_json(k,depth+1,budget);check_json(v,depth+1,budget)
        return
    raise Refusal('invalid_json_value')

def tokens(pointer):
    if type(pointer) is not str or (pointer and not pointer.startswith('/')) or re.search(r'~(?![01])',pointer):
        raise Refusal('invalid_pointer')
    result=[] if pointer=='' else [p.replace('~1','/').replace('~0','~') for p in pointer[1:].split('/')]
    if len(result)>64: raise Refusal('input_limit')
    return result

def index(token,length,append=False):
    if token=='-' and append: return length
    if not re.fullmatch(r'0|[1-9][0-9]*',token): raise Refusal('invalid_index')
    # Bound before integer conversion, including enormous attacker-supplied indices.
    if len(token)>10: raise Refusal('missing_target')
    n=int(token)
    if n>length or (n==length and not append): raise Refusal('missing_target')
    return n

def resolve(document,pointer):
    current=document
    for token in tokens(pointer):
        if type(current) is dict:
            if token not in current: raise Refusal('missing_target')
            current=current[token]
        elif type(current) is list: current=current[index(token,len(current))]
        else: raise Refusal('scalar_traversal')
    return current

def pointer_from_tokens(parts):
    return ''.join('/'+p.replace('~','~0').replace('/','~1') for p in parts)

def project(document,pointers):
    if type(pointers) is not list: raise Refusal('invalid_selectors')
    decoded=[tokens(p) for p in pointers]
    if len({tuple(p) for p in decoded})!=len(decoded): raise Refusal('duplicate_selector')
    for i,a in enumerate(decoded):
        for b in decoded[i+1:]:
            if a==b[:len(a)] or b==a[:len(b)]: raise Refusal('overlapping_selectors')
    return {p:copy.deepcopy(resolve(document,p)) for p in pointers}

def evaluate(operation,data):
    try:
        check_json(data)
        if type(data) is not dict: raise Refusal('invalid_input')
        if operation=='tokens': return tokens(data['pointer'])
        if operation=='resolve': return copy.deepcopy(resolve(data['document'],data['pointer']))
        if operation=='project': return project(data['document'],data['pointers'])
        raise Refusal('unknown_operation')
    except Refusal as exc: return {'error':str(exc)}
    except KeyError: return {'error':'missing_input_field'}

def strict_load(text):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result: raise Refusal('duplicate_json_member')
            result[k]=v
        return result
    def constant(_): raise Refusal('nonfinite_json')
    value=json.loads(text,object_pairs_hook=pairs,parse_constant=constant)
    check_json(value)
    return value

def envelope(proposal,result):
    return {'schema':'ghc.family.synthetic-result.v1','proposal_id':proposal['proposal_id'],
            'definition_sha256':proposal['definition_sha256'],'input_sha256':sha(proposal['input']),
            'result':copy.deepcopy(result),'result_sha256':sha(result),'hash_domain':'sorted-compact-UTF8-JSON',
            'empirical':False,'authority':False,'same_owner_only':True}

def verify_envelope(proposal,record,compute):
    """Recompute from the frozen input; callers cannot pass a purported answer."""
    try:
        check_json(record)
        result=compute(proposal['operation'],copy.deepcopy(proposal['input']))
        correct=envelope(proposal,result)
        issues=[]
        if type(record) is not dict or set(record)!=set(correct): issues.append('envelope_fields')
        else:
            for key in correct:
                if canonical(record[key])!=canonical(correct[key]): issues.append(key)
        return {'accepted':not issues,'issues':issues}
    except (Refusal,TypeError,ValueError,KeyError): return {'accepted':False,'issues':['malformed_envelope']}

def cli(compute):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--operation',required=True);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        if a.input.stat().st_size>1000000: raise Refusal('input_limit')
        result=compute(a.operation,strict_load(a.input.read_text(encoding='utf-8')))
    except (Refusal,ValueError) as exc: result={'error':str(exc) if isinstance(exc,Refusal) else 'invalid_json'}
    output=json.dumps({'result':result,'same_owner_only':True,'empirical':False,'authority':False},ensure_ascii=False,sort_keys=True)+'\n'
    if a.output:
        with a.output.open('x',encoding='utf-8',newline='\n') as f:f.write(output)
    else: print(output,end='')
    return 2 if type(result) is dict and 'error' in result else 0

if __name__=='__main__': raise SystemExit(cli(evaluate))
