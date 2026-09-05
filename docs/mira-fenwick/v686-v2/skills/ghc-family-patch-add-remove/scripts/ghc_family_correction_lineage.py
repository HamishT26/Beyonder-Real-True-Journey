"""Digest-linked synthetic correction history and reconstructable changed paths."""
import copy
from ghc_family_evidence_selectors import Refusal,check_json,canonical,sha,pointer_from_tokens,cli

def chain(snapshots,links):
    if type(snapshots) is not list or not snapshots: raise Refusal('empty_chain')
    if type(links) is not list or len(links)!=len(snapshots)-1: raise Refusal('link_count_mismatch')
    for n,link in enumerate(links,1):
        if type(link) is not dict or set(link)!={'ordinal','parent_sha256','child_sha256','reason'}: raise Refusal('invalid_link')
        if type(link['ordinal']) is not int or link['ordinal']!=n: raise Refusal('ordinal_mismatch')
        if link['parent_sha256']!=sha(snapshots[n-1]): raise Refusal('parent_digest_mismatch')
        if link['child_sha256']!=sha(snapshots[n]): raise Refusal('child_digest_mismatch')
        if type(link['reason']) is not str or not link['reason'].strip(): raise Refusal('missing_reason')
    return {'corrections':len(links),'tip':copy.deepcopy(snapshots[-1])}

def changes(before,after,parts=()):
    if canonical(before)==canonical(after): return []
    if type(before) is dict and type(after) is dict:
        result=[]
        for k in sorted(set(before)|set(after)):
            child=parts+(k,)
            if k not in before or k not in after: result.append(pointer_from_tokens(child))
            else: result.extend(changes(before[k],after[k],child))
        return result
    if type(before) is list and type(after) is list and len(before)==len(after):
        return [p for i,(a,b) in enumerate(zip(before,after)) for p in changes(a,b,parts+(str(i),))]
    return [pointer_from_tokens(parts)]

def evaluate(operation,data):
    try:
        check_json(data)
        if type(data) is not dict: raise Refusal('invalid_input')
        if operation=='chain': return chain(data['snapshots'],data['links'])
        if operation=='changes': return changes(data['before'],data['after'])
        raise Refusal('unknown_operation')
    except Refusal as exc: return {'error':str(exc)}
    except KeyError: return {'error':'missing_input_field'}

if __name__=='__main__': raise SystemExit(cli(evaluate))
