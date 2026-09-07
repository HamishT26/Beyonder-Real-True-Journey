"""Finite synthetic migration profiles. No network, real authority, or production action."""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

import jsonpatch
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from referencing.exceptions import Unresolvable

DIALECT='https://json-schema.org/draft/2020-12/schema'

def strict_equal(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(strict_equal(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b

def canonical_local(value):
    """Local JSON encoding for equality witnesses, not RFC 8785 canonicalization."""
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)

def pointer(value):
    if not isinstance(value,str) or (value and not value.startswith('/')) or re.search(r'~(?![01])',value):
        raise ValueError('INVALID_POINTER')
    return tuple(p.replace('~1','/').replace('~0','~') for p in value[1:].split('/')) if value else ()

def prefix(a,b): return len(a)<=len(b) and b[:len(a)]==a
def overlap(a,b): return prefix(a,b) or prefix(b,a)
def esc(s): return str(s).replace('~','~0').replace('/','~1')

def schema_transition_matrix(p):
    old,new=p['old_schema'],p['new_schema'];value=p['instance']
    Draft202012Validator.check_schema(old);Draft202012Validator.check_schema(new)
    registry=Registry()
    before=Draft202012Validator(old,registry=registry).is_valid(value)
    after=Draft202012Validator(new,registry=registry).is_valid(value)
    decision={(True,True):'BOTH_ACCEPT_SAMPLE',(True,False):'NEW_REJECTS_SAMPLE',(False,True):'NEW_ACCEPTS_SAMPLE',(False,False):'BOTH_REJECT_SAMPLE'}[before,after]
    return decision,dict(old_valid=before,new_valid=after,universal_compatibility=False)

def atomic_patch_preview(p):
    original=copy.deepcopy(p['document']);current=copy.deepcopy(original)
    def held(reason):return 'HOLD',dict(document=original,reason=reason)
    shapes={'add':{'op','path','value'},'replace':{'op','path','value'},'test':{'op','path','value'},'remove':{'op','path'},'move':{'op','path','from'},'copy':{'op','path','from'}}
    try:
        writes=[pointer(x) for x in p['write_allowlist']];reads=[pointer(x) for x in p['read_allowlist']];protected=[pointer(x) for x in p['protected_paths']]
        prepared=[]
        for operation in p['patch']:
            if not isinstance(operation,dict) or operation.get('op') not in shapes or set(operation)!=shapes[operation['op']]:return held('INVALID_OPERATION')
            kind=operation['op'];path=pointer(operation['path']);source=pointer(operation['from']) if 'from' in operation else None
            accessed_reads=([path] if kind=='test' else [])+([source] if source is not None else [])
            accessed_writes=([] if kind=='test' else [path])+([source] if kind=='move' else [])
            if any(not any(prefix(a,x) for a in reads) for x in accessed_reads):return held('READ_OUTSIDE_ALLOWLIST')
            if any(not any(prefix(a,x) for a in writes) for x in accessed_writes):return held('WRITE_OUTSIDE_ALLOWLIST')
            if any(overlap(x,y) for x in accessed_writes for y in protected):return held('PROTECTED_PATH')
            if kind=='move' and len(path)>len(source) and prefix(source,path):return held('DESCENDANT_MOVE')
            prepared.append((operation,path,source))
    except ValueError:return held('INVALID_POINTER')
    def at(doc,parts):
        value=doc
        for part in parts:
            if isinstance(value,list):
                if not part.isdigit() or (len(part)>1 and part.startswith('0')):raise ValueError('INVALID_ARRAY_INDEX')
                value=value[int(part)]
            else:value=value[part]
        return value
    for operation,path,source in prepared:
        try:
            for parts in [path]+([source] if source is not None else []):
                cursor=current
                for part in parts:
                    if isinstance(cursor,list):
                        if part!='-' and (not part.isdigit() or (len(part)>1 and part.startswith('0'))):return held('INVALID_ARRAY_INDEX')
                        if part=='-' or int(part)>=len(cursor):break
                        cursor=cursor[int(part)]
                    elif isinstance(cursor,dict) and part in cursor:cursor=cursor[part]
                    else:break
            if operation['op']=='test':
                if not strict_equal(at(current,path),operation['value']):return held('TEST_FAILED')
            else:current=jsonpatch.apply_patch(current,[operation],in_place=False)
        except (jsonpatch.JsonPatchException,KeyError,IndexError,TypeError):return held('PATCH_CONFLICT')
        except ValueError as e:return held(str(e))
    return 'PREVIEW_ONLY',dict(document=current,reason=None)

def offline_reference_snapshot(p):
    def held(reason):return 'HOLD',dict(resolved=None,reason=reason,network_requests=0)
    registry=Registry();seen=set()
    for item in p['resources']:
        uri=item['uri'];contents=item['contents']
        if uri in seen:return held('DUPLICATE_URI')
        seen.add(uri)
        if not urlsplit(uri).scheme:return held('ABSOLUTE_BASE_REQUIRED')
        if not isinstance(contents,(dict,bool)):return held('INVALID_SCHEMA')
        if isinstance(contents,dict):
            if '$schema' in contents and contents['$schema']!=DIALECT:return held('UNSUPPORTED_DIALECT')
            if '$id' in contents and contents['$id']!=uri:return held('IDENTIFIER_MISMATCH')
        registry=registry.with_resource(uri,Resource(contents=copy.deepcopy(contents),specification=DRAFT202012))
    ref=p['ref'];base=p['base']
    if not urlsplit(ref).scheme and not urlsplit(base).scheme:return held('ABSOLUTE_BASE_REQUIRED')
    try:resolved=registry.crawl().resolver(base_uri=base).lookup(ref).contents
    except (Unresolvable,KeyError,ValueError):return held('UNRESOLVED')
    return 'RESOLVED_OFFLINE',dict(resolved=copy.deepcopy(resolved),reason=None,network_requests=0)

def lossless_field_migration(p):
    original=p['record'];rules=p['rules']
    def held(reason):return 'HOLD',dict(record=copy.deepcopy(original),reason=reason)
    if not isinstance(original,dict) or not isinstance(rules,list):return held('INVALID_RULE')
    for rule in rules:
        if not isinstance(rule,dict) or set(rule)!={'source','target','required'} or type(rule['required']) is not bool or not isinstance(rule['source'],str) or not isinstance(rule['target'],str):return held('INVALID_RULE')
    sources=[r['source'] for r in rules];targets=[r['target'] for r in rules]
    if len(set(sources))!=len(sources):return held('DUPLICATE_SOURCE')
    if len(set(targets))!=len(targets):return held('DUPLICATE_TARGET')
    if any(r['required'] and r['source'] not in original for r in rules):return held('MISSING_SOURCE')
    active=[r for r in rules if r['source'] in original];consumed={r['source'] for r in active}
    if any(r['target'] in original and r['target'] not in consumed for r in active):return held('OCCUPIED_TARGET')
    result={k:copy.deepcopy(v) for k,v in original.items() if k not in consumed}
    for rule in active:result[rule['target']]=copy.deepcopy(original[rule['source']])
    return 'MIGRATED_VIEW',dict(record=result,reason=None)

def migration_obligation_graph(p):
    def invalid(reason):return 'HOLD',dict(order=[],ready=[],held={},reason=reason)
    nodes=p['nodes'];available=p['available_artifacts']
    if len(set(available))!=len(available):return invalid('DUPLICATE_ARTIFACT')
    for node in nodes:
        if not isinstance(node,dict) or set(node)!={'id','dependencies','artifacts','disposition'} or not isinstance(node['id'],str) or not node['id'] or node['disposition'] not in {'completed','represented','open_gap','exact_gate'} or not isinstance(node['dependencies'],list) or not isinstance(node['artifacts'],list) or any(not isinstance(x,str) for x in node['dependencies']+node['artifacts']):return invalid('INVALID_NODE')
    by_id={x['id']:x for x in nodes}
    if len(by_id)!=len(nodes):return invalid('DUPLICATE_NODE')
    if any(len(set(x['dependencies']))!=len(x['dependencies']) for x in nodes):return invalid('DUPLICATE_DEPENDENCY')
    if any(d not in by_id for x in nodes for d in x['dependencies']):return invalid('MISSING_DEPENDENCY')
    remaining=set(by_id);order=[]
    while remaining:
        eligible=sorted(x for x in remaining if set(by_id[x]['dependencies']).issubset(order))
        if not eligible:return invalid('CYCLE')
        chosen=eligible[0];order.append(chosen);remaining.remove(chosen)
    ready=[];held={};labels={'represented':'REPRESENTED_ONLY','open_gap':'OPEN_GAP','exact_gate':'EXACT_GATE'}
    for label in order:
        node=by_id[label];reasons=[]
        if node['disposition']!='completed':reasons.append(labels[node['disposition']])
        elif not node['artifacts']:reasons.append('EVIDENCE_REQUIRED')
        elif not set(node['artifacts']).issubset(available):reasons.append('MISSING_ARTIFACT')
        if any(x not in ready for x in node['dependencies']):reasons.append('DEPENDENCY_HELD')
        if reasons:held[label]=reasons
        else:ready.append(label)
    return 'PLANNING_PROJECTION',dict(order=order,ready=ready,held=held,reason=None)

def schema_annotation_quarantine(p):
    annotations={'title','description','default','examples','deprecated','readOnly','writeOnly','$comment','contentEncoding','contentMediaType'}
    maps={'properties','patternProperties','$defs','dependentSchemas'}
    arrays={'allOf','anyOf','oneOf','prefixItems'}
    singles={'if','then','else','not','items','contains','additionalProperties','unevaluatedProperties','unevaluatedItems','propertyNames','contentSchema'}
    removed=[]
    def visit(schema,path):
        if isinstance(schema,bool):return schema
        if not isinstance(schema,dict):raise ValueError('Schema position must be object or boolean')
        out={}
        for key,value in schema.items():
            child=path+'/'+esc(key)
            if key in annotations or key.startswith('x-'):removed.append(child)
            elif key in maps:out[key]={k:visit(v,child+'/'+esc(k)) for k,v in value.items()}
            elif key in arrays:out[key]=[visit(v,child+'/'+str(i)) for i,v in enumerate(value)]
            elif key in singles:out[key]=visit(value,child)
            else:out[key]=copy.deepcopy(value)
        return out
    view=visit(p['schema'],'')
    return 'STRUCTURAL_VIEW',dict(assertion_view=view,quarantined_paths=sorted(removed),annotations_are_evidence=False)

def migration_interference(p):
    def held(reason):return 'HOLD',dict(conflicts=[],reason=reason,execution_permitted=False)
    converted={}
    try:
        for side in ['left','right']:
            converted[side]={}
            for kind in ['reads','writes']:
                converted[side][kind]=[pointer(x) for x in p[side][kind]]
                for parts in converted[side][kind]:
                    if '*' in parts:return held('WILDCARD_UNSUPPORTED')
                    if '-' in parts:return held('ARRAY_SHIFT_SCOPE_REQUIRED')
    except ValueError:return held('INVALID_POINTER')
    left,right=converted['left'],converted['right'];conflicts=[]
    for kind,a,b in [('WRITE_WRITE',left['writes'],right['writes']),('LEFT_WRITE_RIGHT_READ',left['writes'],right['reads']),('RIGHT_WRITE_LEFT_READ',right['writes'],left['reads'])]:
        if any(overlap(x,y) for x in a for y in b):conflicts.append(kind)
    return 'STATIC_CONFLICT_VIEW',dict(conflicts=sorted(conflicts),reason=None,execution_permitted=False)

def dual_reader_equivalence(p):
    differences=[]
    def visit(a,b,path):
        if type(a) is not type(b):differences.append(dict(path=path,kind='TYPE'))
        elif isinstance(a,dict):
            for key in sorted(a.keys()|b.keys()):
                child=path+'/'+esc(key)
                if key not in b:differences.append(dict(path=child,kind='LEFT_ONLY'))
                elif key not in a:differences.append(dict(path=child,kind='RIGHT_ONLY'))
                else:visit(a[key],b[key],child)
        elif isinstance(a,list):
            for i in range(max(len(a),len(b))):
                child=path+'/'+str(i)
                if i>=len(b):differences.append(dict(path=child,kind='LEFT_ONLY'))
                elif i>=len(a):differences.append(dict(path=child,kind='RIGHT_ONLY'))
                else:visit(a[i],b[i],child)
        elif a!=b:differences.append(dict(path=path,kind='VALUE'))
    visit(p['left'],p['right'],'')
    return 'SAMPLE_COMPARISON',dict(differences=differences,equivalent=not differences,relation='LOCAL_TYPE_STRICT_JSON')

def gmut_dimension_migration(p):
    def held(reason):return 'HOLD',dict(value=None,uncertainty=None,reason=reason,empirical=False)
    if p['claim']!='representation':return held('EXTERNAL_CLAIM_HELD')
    if p['model_family']!='scalar_tensor_eft':return held('MODEL_FAMILY_OUTSIDE_PROFILE')
    units={'m':('L',Fraction(1)),'cm':('L',Fraction(1,100)),'mm':('L',Fraction(1,1000)),'s':('T',Fraction(1)),'ms':('T',Fraction(1,1000)),'min':('T',Fraction(60)),'kg':('M',Fraction(1)),'g':('M',Fraction(1,1000)),'m/s':('L/T',Fraction(1)),'km/h':('L/T',Fraction(5,18)),'1':('1',Fraction(1))}
    source,target=p['source_unit'],p['target_unit']
    if source in {'degC','K'} or target in {'degC','K'}:return held('AFFINE_OUTSIDE_PROFILE')
    if source not in units or target not in units:return held('UNKNOWN_UNIT')
    if units[source][0]!=units[target][0]:return held('DIMENSION_MISMATCH')
    factor=units[source][1]/units[target][1]
    def shape(value):
        if not isinstance(value,list):return []
        children=[shape(x) for x in value]
        if children and any(x!=children[0] for x in children):raise ValueError('RAGGED_TENSOR')
        return [len(value)]+(children[0] if children else [])
    def rational(value):
        if not isinstance(value,str):raise ValueError('RATIONAL_STRING_REQUIRED')
        if len(value)>1000:raise ValueError('INVALID_RATIONAL')
        try:return Fraction(value)
        except (ValueError,ZeroDivisionError):raise ValueError('INVALID_RATIONAL') from None
    def convert(value):return [convert(x) for x in value] if isinstance(value,list) else str(rational(value)*factor)
    try:
        if shape(p['value'])!=p['shape']:return held('SHAPE_MISMATCH')
        converted=convert(p['value']);u=p['uncertainty']
        if u is not None:
            u=rational(u)
            if u<0:return held('NEGATIVE_UNCERTAINTY')
            u=str(u*abs(factor))
    except ValueError as e:return held(str(e))
    return 'REPRESENTATION_ONLY',dict(value=converted,uncertainty=u,reason=None,empirical=False)

def claim_binding_join(p):
    claim=p['claim'];receipt=p['receipt'];observed=p['observed']
    def held(reason):return 'HOLD',dict(binding_match=False,reason=reason,authority_granted=False)
    if receipt['state']!='passed':return held('RECEIPT_NOT_PASSED')
    if receipt['revoked']:return held('RECEIPT_REVOKED')
    if not receipt['revocation_observed']:return held('REVOCATION_UNOBSERVED')
    if receipt['issued']>observed:return held('RECEIPT_NOT_YET_ISSUED')
    if receipt['expires']<=observed:return held('RECEIPT_EXPIRED')
    for key in ['artifact','head','owner','phase','scope','byte_domain','digest','profile','evidence_class']:
        if not strict_equal(claim['binding'].get(key),receipt['binding'].get(key)):return held('BINDING_MISMATCH:'+key)
    if claim['kind']!='software':
        if receipt['reviewer_class']=='same_owner':return held('INDEPENDENT_REVIEW_ABSENT')
        if receipt['signature_evidence']=='absent':return held('SIGNATURE_EVIDENCE_ABSENT')
        if receipt['signature_evidence']!='verified_external_declared':return held('SIGNATURE_NOT_VERIFIED')
        if receipt['authority_scope']!=claim['binding']['scope']:return held('AUTHORITY_SCOPE_MISMATCH')
        if not receipt.get('approval_document_digest'):return held('APPROVAL_DOCUMENT_UNBOUND')
        if receipt.get('affected_party_evidence'):return held('AFFECTED_PARTY_EVIDENCE_UNVERIFIED')
        return held('COMPETENT_AUTHORITY_RESERVED')
    return 'DECLARED_BINDING_MATCH',dict(binding_match=True,reason=None,authority_granted=False)

OPERATIONS={f.__name__:f for f in [schema_transition_matrix,atomic_patch_preview,offline_reference_snapshot,lossless_field_migration,migration_obligation_graph,schema_annotation_quarantine,migration_interference,dual_reader_equivalence,gmut_dimension_migration,claim_binding_join]}

def run(operation,payload):
    if operation not in OPERATIONS:raise ValueError('Unknown bounded operation')
    if type(payload) is not dict:raise TypeError('Payload must be a JSON object')
    before=canonical_local(payload)
    decision,result=OPERATIONS[operation](payload)
    preserved=before==canonical_local(payload)
    if not preserved:raise RuntimeError('Input mutation violates profile')
    return dict(decision=decision,result=result,source_preserved=preserved,external_credit=False)

def mutated_results(expected):
    values=[]
    x=copy.deepcopy(expected);del x['decision'];values.append(x)
    x=copy.deepcopy(expected);x['authority_granted']=True;values.append(x)
    x=copy.deepcopy(expected);x['result']=[];values.append(x)
    x=copy.deepcopy(expected);x['source_preserved']=False;values.append(x)
    x=copy.deepcopy(expected);x['external_credit']=True;values.append(x)
    return values

def strict_load(path):
    def unique(pairs):
        obj={}
        for key,value in pairs:
            if key in obj:raise ValueError('Duplicate JSON key')
            obj[key]=value
        return obj
    def invalid(value):raise ValueError('Non-finite JSON constant: '+value)
    return json.loads(Path(path).read_text(encoding='utf8'),object_pairs_hook=unique,parse_constant=invalid)

def cli(fixed_operation=None):
    parser=argparse.ArgumentParser(description=__doc__)
    if fixed_operation is None:parser.add_argument('--operation',choices=sorted(OPERATIONS),required=True)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=run(fixed_operation or args.operation,strict_load(args.input))
    # Exclusive output avoids replacing an earlier witness, including a failure.
    with args.output.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n')

if __name__=='__main__':cli()
