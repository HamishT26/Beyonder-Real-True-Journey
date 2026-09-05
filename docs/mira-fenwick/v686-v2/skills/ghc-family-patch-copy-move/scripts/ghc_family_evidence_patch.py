"""Atomic in-memory JSON corrections with explicit subtree permissions.

No filesystem, network, credentials, external documents, or live identities are
changed. Root removal and unknown operation members are reserved by this profile.
"""
import copy
from ghc_family_evidence_selectors import Refusal,check_json,tokens,index,resolve,pointer_from_tokens,cli

def equal(a,b):
    if type(a) in (int,float) and type(b) in (int,float): return a==b
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b

def modify(doc,path,kind,value=None):
    parts=tokens(path)
    if not parts:
        if kind=='remove': raise Refusal('root_removal_reserved')
        return copy.deepcopy(value)
    parent=resolve(doc,pointer_from_tokens(parts[:-1]));key=parts[-1]
    if type(parent) is dict:
        if kind!='add' and key not in parent: raise Refusal('missing_target')
        if kind=='remove': del parent[key]
        else: parent[key]=copy.deepcopy(value)
    elif type(parent) is list:
        n=index(key,len(parent),append=kind=='add')
        if kind=='add': parent.insert(n,copy.deepcopy(value))
        elif kind=='remove': parent.pop(n)
        else: parent[n]=copy.deepcopy(value)
    else: raise Refusal('scalar_traversal')
    return doc

def patch(document,operations,allowed=None):
    check_json(document)
    if type(operations) is not list: raise Refusal('invalid_operations')
    if len(operations)>500: raise Refusal('operation_limit')
    if allowed is not None and type(allowed) is not list: raise Refusal('invalid_permissions')
    prefixes=None if allowed is None else [tokens(p) for p in allowed]
    result=copy.deepcopy(document)
    for op in operations:
        if type(op) is not dict or 'op' not in op or 'path' not in op: raise Refusal('invalid_operation')
        kind=op['op']
        if kind not in ('add','remove','replace','test','copy','move'): raise Refusal('unknown_operation')
        if set(op)-{'op','path','value','from'}: raise Refusal('unknown_operation_member')
        dest=tokens(op['path'])
        if kind in ('add','replace','test') and 'value' not in op: raise Refusal('missing_value')
        if kind in ('copy','move') and 'from' not in op: raise Refusal('missing_from')
        paths=[dest]
        if kind in ('copy','move'): paths.append(tokens(op['from']))
        if prefixes is not None and any(not any(p==target[:len(p)] for p in prefixes) for target in paths):
            raise Refusal('path_not_allowed')
        if kind=='test':
            if not equal(resolve(result,op['path']),op['value']): raise Refusal('test_failed')
        elif kind in ('copy','move'):
            src=paths[1]
            value=copy.deepcopy(resolve(result,op['from']))
            if kind=='move':
                if len(dest)>len(src) and src==dest[:len(src)]: raise Refusal('move_into_descendant')
                if dest==src: continue
                result=modify(result,op['from'],'remove')
            result=modify(result,op['path'],'add',value)
        else: result=modify(result,op['path'],kind,op.get('value'))
        check_json(result)
    return result

def evaluate(operation,data):
    try:
        check_json(data)
        if type(data) is not dict: raise Refusal('invalid_input')
        if operation!='patch': raise Refusal('unknown_operation')
        if 'allowed' in data and type(data['allowed']) is not list: raise Refusal('invalid_permissions')
        return patch(data['document'],data['operations'],data.get('allowed'))
    except Refusal as exc: return {'error':str(exc)}
    except KeyError: return {'error':'missing_input_field'}

if __name__=='__main__': raise SystemExit(cli(evaluate))
