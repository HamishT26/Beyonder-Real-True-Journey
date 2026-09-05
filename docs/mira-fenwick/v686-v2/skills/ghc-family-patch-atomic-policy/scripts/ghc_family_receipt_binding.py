"""Exact synthetic receipt bindings, literal manifests, and scalar disclosure budgets."""
import hashlib
import re
from ghc_family_evidence_selectors import Refusal,check_json,canonical,project,cli

FIELDS={'owner','source','head','tree','phase','same_owner_only','independent_reproduction'}

def scope(expected,receipt):
    for item in (expected,receipt):
        if type(item) is not dict or set(item)!=FIELDS: raise Refusal('scope_mismatch')
        if item['same_owner_only'] is not True or item['independent_reproduction'] is not False: raise Refusal('scope_mismatch')
        if any(type(item[k]) is not str or not item[k].strip() for k in ['owner','phase']): raise Refusal('scope_mismatch')
        if any(type(item[k]) is not str or not re.fullmatch('[0-9a-f]{40}',item[k]) for k in ['source','head','tree']): raise Refusal('scope_mismatch')
    if canonical(expected)!=canonical(receipt): raise Refusal('scope_mismatch')
    return True

def literal_path(path):
    return type(path) is str and bool(path) and not path.startswith('/') and '\\' not in path and ':' not in path and all(p not in ('','.','..') for p in path.split('/'))

def manifest(files,entries):
    if type(files) is not dict or type(entries) is not list: raise Refusal('invalid_manifest')
    seen=set()
    for entry in entries:
        if type(entry) is not dict or set(entry)!={'path','bytes','sha256'}: raise Refusal('invalid_manifest')
        path=entry['path']
        if not literal_path(path): raise Refusal('unsafe_path')
        if path in seen: raise Refusal('duplicate_path')
        seen.add(path)
        if path not in files or type(files[path]) is not str: raise Refusal('coverage_mismatch')
        raw=files[path].encode('utf-8')
        if type(entry['bytes']) is not int or entry['bytes']!=len(raw): raise Refusal('size_mismatch')
        if entry['sha256']!=hashlib.sha256(raw).hexdigest(): raise Refusal('digest_mismatch')
    if seen!=set(files): raise Refusal('coverage_mismatch')
    return True

def disclose(document,pointers,budget):
    if type(budget) is not int or budget<0: raise Refusal('invalid_budget')
    selected=project(document,pointers)
    if any(type(v) in (dict,list) for v in selected.values()): raise Refusal('container_disclosure')
    if len(selected)>budget: raise Refusal('disclosure_budget')
    return selected

def evaluate(operation,data):
    try:
        check_json(data)
        if type(data) is not dict: raise Refusal('invalid_input')
        if operation=='scope': return scope(data['expected'],data['receipt'])
        if operation=='manifest': return manifest(data['files'],data['entries'])
        if operation=='disclose': return disclose(data['document'],data['pointers'],data['budget'])
        raise Refusal('unknown_operation')
    except Refusal as exc: return {'error':str(exc)}
    except KeyError: return {'error':'missing_input_field'}

if __name__=='__main__': raise SystemExit(cli(evaluate))
