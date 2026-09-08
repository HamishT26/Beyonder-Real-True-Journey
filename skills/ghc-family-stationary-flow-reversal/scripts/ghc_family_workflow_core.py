"""Pure bounded workflow computations. No filesystem, network or task actions."""
import copy
import json
import re
import sys

OUTCOMES={'completed','represented','open_gap','exact_gate'}
MAX_INPUT_BYTES=1_048_576

class ContractError(ValueError):
    """An explicit refusal within the declared input profile."""

def require(condition,code='domain'):
    if not condition:
        raise ContractError(code)

def integer(value,minimum=0,maximum=1_000_000_000):
    require(type(value) is int,'type')
    require(minimum<=value<=maximum)
    return value

def boolean(value):
    require(type(value) is bool,'type')
    return value

def text(value,maximum=256):
    require(type(value) is str,'type')
    require(bool(value.strip()) and len(value)<=maximum)
    require(not any(ord(c)<32 for c in value))
    return value

def array(value,maximum=500):
    require(type(value) is list,'type')
    require(len(value)<=maximum)
    return value

def record(value,fields):
    require(type(value) is dict,'type')
    require(set(value)==set(fields),'schema')
    return value

def labels(value,maximum=500):
    values=array(value,maximum)
    for v in values:text(v)
    require(len(values)==len(set(values)),'duplicate')
    return values

def digest(value):
    text(value,64)
    require(re.fullmatch('[0-9a-f]{64}',value) is not None)
    return value

def ordinal(value):
    text(value)
    match=re.fullmatch(r'v([1-9][0-9]*)-v([1-8])',value)
    require(match is not None)
    version=integer(int(match[1]),1,1_000_000)
    return (version-1)*8+int(match[2])-1

def phase_name(value):
    require(value>=0)
    return f'v{value//8+1}-v{value%8+1}'

def phase_advance(r):
    return phase_name(ordinal(r['phase'])+integer(r['delta'],-1_000_000,1_000_000))

def cycle_assignments(r):
    cycle=labels(r['cycle'],60)
    require(bool(cycle))
    start=text(r['start'])
    require(start in cycle,'missing')
    begin=ordinal(r['phase']);count=integer(r['count'],0,500);pos=cycle.index(start)
    return [{'phase':phase_name(begin+i),'owner':cycle[(pos+i)%len(cycle)]} for i in range(count)]

def route_cursor(r):
    rows=array(r['rows']);positions=[]
    for row in rows:
        record(row,{'phase','owner'});text(row['owner']);positions.append(ordinal(row['phase']))
    require(len(set(positions))==len(positions),'duplicate')
    require(all(b==a+1 for a,b in zip(positions,positions[1:])),'sequence')
    ordinal(r['phase']);text(r['owner'])
    matches=[i for i,row in enumerate(rows) if row['phase']==r['phase'] and row['owner']==r['owner']]
    require(len(matches)==1,'missing')
    i=matches[0]+1
    return copy.deepcopy(rows[i]) if i<len(rows) else None

def delivery_reduce(r):
    events=array(r['events'],10)
    transitions={
        'NOT_PREPARED':{'prepared':'PREPARED_NOT_SENT'},
        'PREPARED_NOT_SENT':{'submitted':'SUBMITTED_PENDING','unavailable':'PREPARED_NOT_SENT_ROUTE_UNAVAILABLE'},
        'SUBMITTED_PENDING':{'acknowledged':'SENT_ONCE_ACKNOWLEDGED','opaque_accepted':'ACCEPTED_OPAQUE_NO_RESEND','rejected':'SUBMITTED_REJECTED_NO_RESEND'}}
    known={'prepared','submitted','unavailable','acknowledged','opaque_accepted','rejected'}
    state='NOT_PREPARED'
    for event in events:
        text(event);require(event in known)
        require(event in transitions.get(state,{}),'sequence')
        state=transitions[state][event]
    return state

def budget_check(r):
    count=integer(r['count']);low=integer(r['minimum']);high=integer(r['maximum'])
    require(low<=high)
    return {'within':low<=count<=high,'deficit':max(0,low-count),'excess':max(0,count-high)}

def quota_partition(r):
    total=integer(r['total'],0,10000);batch=integer(r['batch'],1,10000)
    complete,remainder=divmod(total,batch)
    return [batch]*complete+([remainder] if remainder else [])

def context_window(r):
    rows=array(r['rows']);count=integer(r['count'],0,500);ordinals=[];ids=[]
    for row in rows:
        record(row,{'id','ordinal','state'});ids.append(text(row['id']))
        ordinals.append(integer(row['ordinal'],0,10_000_000))
        text(row['state'])
        require(row['state'] in OUTCOMES)
    require(len(ids)==len(set(ids)) and len(ordinals)==len(set(ordinals)),'duplicate')
    completed=sorted((row for row in rows if row['state']=='completed'),key=lambda row:row['ordinal'])
    return [row['id'] for row in completed[-count:]] if count else []

def source_selection(r):
    rows=array(r['rows']);limit=integer(r['limit'],0,500);seen={};order=[]
    for row in rows:
        record(row,{'id','source','sha256'});identifier=text(row['id']);text(row['source']);digest(row['sha256'])
        if identifier in seen:require(seen[identifier]==row,'conflict')
        else:seen[identifier]=row;order.append(identifier)
    return order[:limit]

def file_budget(r):
    current=integer(r['current'],0,10_000_000);incoming=integer(r['incoming'],0,10_000_000)
    ceiling=integer(r['ceiling'],1,2000);total=current+incoming
    return {'admit':total<=ceiling,'total':total,'remaining':max(0,ceiling-total),'rotate':total>=ceiling}

def path_parts(value):
    text(value,1024)
    require(not value.startswith('/') and '\\' not in value and ':' not in value,'path')
    parts=value.split('/')
    require(all(p not in {'','.','..'} for p in parts),'path')
    return parts

def path_scope(r):
    parts=path_parts(r['path']);roots=labels(r['roots'])
    allowed=[path_parts(root) for root in roots]
    return any(parts[:len(prefix)]==prefix for prefix in allowed)

def manifest_map(rows):
    result={}
    for row in array(rows):
        record(row,{'path','bytes','sha256'});path_parts(row['path'])
        integer(row['bytes'],0,1_000_000_000);digest(row['sha256'])
        require(row['path'] not in result,'duplicate')
        result[row['path']]=(row['bytes'],row['sha256'])
    return result

def manifest_diff(r):
    before=manifest_map(r['before']);after=manifest_map(r['after']);shared=before.keys()&after.keys()
    return {'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys()),
            'changed':sorted(p for p in shared if before[p]!=after[p]),
            'unchanged':sorted(p for p in shared if before[p]==after[p])}

def staged_allowlist(r):
    staged=labels(r['staged']);allowed=labels(r['allowed'])
    for p in staged+allowed:path_parts(p)
    a=set(staged);b=set(allowed)
    return {'exact':a==b,'unexpected':sorted(a-b),'missing':sorted(b-a)}

def method_transition(r):
    states={'observed','candidate','validated','preferred','superseded','deprecated'}
    source=text(r['state']);target=text(r['to']);require(source in states and target in states)
    passes=integer(r['passing_witnesses']);successor=boolean(r['successor_validated'])
    transitions={'observed':{'candidate','deprecated'},'candidate':{'validated','deprecated'},
                 'validated':{'preferred','superseded','deprecated'},'preferred':{'superseded','deprecated'}}
    allowed=target in transitions.get(source,set())
    if target in {'validated','preferred'}:allowed=allowed and passes>0
    if target=='superseded':allowed=allowed and successor
    return allowed

def witness_accounting(r):
    rows=array(r['rows']);ids=[]
    for row in rows:
        record(row,{'id','subject','check'});ids.append(text(row['id']))
        text(row['subject']);text(row['check'])
        require(row['subject'] in {'pass','fail'} and row['check'] in {'pass','fail'})
    require(len(ids)==len(set(ids)),'duplicate')
    return {'subject_pass':sum(x['subject']=='pass' for x in rows),
            'subject_fail':sum(x['subject']=='fail' for x in rows),
            'checks_pass':sum(x['check']=='pass' for x in rows),
            'checks_fail':sum(x['check']=='fail' for x in rows),
            'original_success_credit':sum(x['subject']=='pass' and x['check']=='pass' for x in rows)}

def dependency_closure(r):
    graph=r['graph'];require(type(graph) is dict,'type');require(len(graph)<=500)
    for name,deps in graph.items():text(name);labels(deps)
    for deps in graph.values():require(all(n in graph for n in deps),'missing')
    roots=labels(r['roots']);require(all(n in graph for n in roots),'missing')
    pending=list(roots);found=set()
    while pending:
        name=pending.pop()
        if name in found:continue
        found.add(name);pending.extend(graph[name])
    return sorted(found)

def tool_select(r):
    trigger=text(r['trigger']);tools=array(r['tools']);names=[];selected=[]
    for tool in tools:
        record(tool,{'name','triggers','status','evidence'});names.append(text(tool['name']));labels(tool['triggers'])
        text(tool['status']);text(tool['evidence'])
        require(tool['status'] in {'current','compatibility','historical','candidate'})
        require(tool['evidence'] in {'observed','validated','preferred','exact_gate'})
        if tool['status']=='current' and tool['evidence'] in {'validated','preferred'} and trigger in tool['triggers']:
            selected.append(tool['name'])
    require(len(names)==len(set(names)),'duplicate')
    return sorted(selected)

def deck_map(cards):
    cards=array(cards,2000);mapping={};roots=[]
    for card in cards:
        record(card,{'id','tier','parent'});name=text(card['id']);tier=integer(card['tier'],1,4)
        require(name not in mapping,'duplicate');mapping[name]=card
        if tier==1:
            require(card['parent'] is None,'tier');roots.append(name)
        else:text(card['parent'])
    require(len(roots)==1)
    for card in cards:
        if card['tier']==1:continue
        require(card['parent'] in mapping,'missing')
        require(mapping[card['parent']]['tier']==card['tier']-1,'tier')
    return mapping

def deck_parents(r):
    mapping=deck_map(r['cards'])
    return [sum(c['tier']==tier for c in mapping.values()) for tier in range(1,5)]

def card_selection(r):
    mapping=deck_map(r['cards']);selected=labels(r['selected'],2000)
    require(all(n in mapping for n in selected),'missing');found=set()
    for name in selected:
        while name is not None:
            found.add(name);name=mapping[name]['parent']
    return sorted(found,key=lambda n:(mapping[n]['tier'],n))

def evidence_gate(r):
    approval=text(r['approval']);evidence=text(r['evidence']);available=boolean(r['prerequisites'])
    require(approval in {'authorized_now','authorized_with_terminal_conditions','pending_exact_action','outside_hamish_authority','blocked'})
    require(evidence in OUTCOMES)
    return approval=='authorized_now' and evidence=='completed' and available

def scalar_map(value):
    require(type(value) is dict,'type');require(len(value)<=500)
    for k,v in value.items():
        text(k)
        require(v is None or type(v) in {str,int,bool},'type')
        if isinstance(v,str):require(len(v)<=10000)
        if type(v) is int:integer(v,-1_000_000_000,1_000_000_000)
    return value

def overlay_fold(r):
    base=scalar_map(r['base']);current=copy.deepcopy(base);events=array(r['events']);last=-1
    for event in events:
        record(event,{'sequence','changes','reason'});number=integer(event['sequence']);text(event['reason'],10000)
        require(number>last,'sequence');last=number
        current.update(copy.deepcopy(scalar_map(event['changes'])))
    return {'current':current,'events':len(events)}

FIELDS={
 'phase_advance':{'phase','delta'},'cycle_assignments':{'cycle','start','phase','count'},
 'route_cursor':{'rows','phase','owner'},'delivery_reduce':{'events'},
 'budget_check':{'count','minimum','maximum'},'quota_partition':{'total','batch'},
 'context_window':{'rows','count'},'source_selection':{'rows','limit'},
 'file_budget':{'current','incoming','ceiling'},'path_scope':{'path','roots'},
 'manifest_diff':{'before','after'},'staged_allowlist':{'staged','allowed'},
 'method_transition':{'state','to','passing_witnesses','successor_validated'},'witness_accounting':{'rows'},
 'dependency_closure':{'graph','roots'},'tool_select':{'tools','trigger'},
 'deck_parents':{'cards'},'card_selection':{'cards','selected'},
 'evidence_gate':{'approval','evidence','prerequisites'},'overlay_fold':{'base','events'}}
OPERATIONS={name:globals()[name] for name in FIELDS}

def evaluate(request,allowed=None):
    try:
        require(type(request) is dict,'type')
        op=request.get('op');text(op)
        require(op in FIELDS and (allowed is None or op in allowed))
        record(request,FIELDS[op]|{'op'})
        value=OPERATIONS[op](request)
        return {'ok':True,'value':value,'error':None}
    except ContractError as error:
        return {'ok':False,'value':None,'error':str(error)}

def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate');result[key]=value
        return result
    def constant(value):raise ContractError('domain')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def cli(allowed=None,evaluator=evaluate):
    try:
        raw=sys.stdin.buffer.read(MAX_INPUT_BYTES+1)
        require(len(raw)<=MAX_INPUT_BYTES)
        request=strict_json(raw.decode('utf-8'))
        result=evaluator(request,allowed)
    except (ContractError,UnicodeDecodeError,json.JSONDecodeError,RecursionError) as error:
        result={'ok':False,'value':None,'error':str(error) if isinstance(error,ContractError) else 'schema'}
    sys.stdout.write(json.dumps(result,sort_keys=True,ensure_ascii=True,allow_nan=False)+'\n')
    return 0 if result['ok'] else 2

if __name__=='__main__':sys.exit(cli())
