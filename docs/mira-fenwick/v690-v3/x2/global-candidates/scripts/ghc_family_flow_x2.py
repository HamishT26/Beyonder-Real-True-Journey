"""Bounded cut enumeration, cost/assignment search and non-authorizing projections."""
import copy,itertools,math
from scripts.ghc_family_flow_common import Refusal,accepted,rejected,closed,graph_record,feasible,flow_value
from scripts.ghc_family_flow_x1 import maximum_flow,cut_capacity

REQUIRED={'min_cut':{'op','graph'},'duality':{'op','graph'},'remove_arc':{'op','graph','arc_index'},
 'increase_capacity':{'op','graph','arc_index','delta'},'lower_feasible':{'op','graph','lower','required'},
 'min_cost':{'op','graph','costs','required'},'assignment':{'op','costs'},
 'policy_gate':{'op','graph','required','consent','evidence','authority'},'summary':{'op','graph'},'reservation':{'op','kind','obligation'}}

def minimum_cut(graph):
    inner=[v for v in graph['nodes'] if v not in ('s','t')];best=None
    for mask in range(1<<len(inner)):
        selected={'s'}|{v for i,v in enumerate(inner) if mask&(1<<i)}
        cut=[v for v in graph['nodes'] if v in selected];capacity=cut_capacity(graph,cut)
        if best is None or capacity<best['capacity']:best={'capacity':capacity,'source_side':cut}
    return best

def required_value(value):
    if type(value) is not int or not 0<=value<=96:raise Refusal('invalid_required')
    return value

def flow_candidates(graph,lower=None):
    capacities=[c for _,_,c in graph['arcs']]
    if lower is None:lower=[0]*len(capacities)
    if type(lower) is not list or len(lower)!=len(capacities):raise Refusal('lower_shape')
    if any(type(x) is not int or not 0<=x<=96 for x in lower):raise Refusal('invalid_lower')
    domains=[range(a,c+1) for a,c in zip(lower,capacities)]
    if math.prod(len(d) for d in domains)>50000:raise Refusal('work_limit')
    for flow in itertools.product(*domains):
        values=list(flow)
        if feasible(graph,values):yield values

def lower_feasible(graph,lower,required):
    required_value(required)
    return any(flow_value(graph,flow)==required for flow in flow_candidates(graph,lower))

def minimum_cost(graph,costs,required):
    required_value(required)
    if type(costs) is not list or len(costs)!=len(graph['arcs']):raise Refusal('cost_shape')
    if any(type(c) is not int or abs(c)>1000 for c in costs):raise Refusal('invalid_cost')
    best=None
    for flow in flow_candidates(graph):
        if flow_value(graph,flow)!=required:continue
        cost=sum(c*f for c,f in zip(costs,flow))
        if best is None or cost<best:best=cost
    return {'feasible':best is not None,'cost':best}

def assignment(costs):
    if type(costs) is not list:raise Refusal('invalid_matrix')
    if len(costs)>8:raise Refusal('work_limit')
    if not costs:return {'columns':[],'cost':0}
    if any(type(row) is not list for row in costs):raise Refusal('invalid_matrix')
    columns=len(costs[0])
    if columns>8:raise Refusal('work_limit')
    if any(len(row)!=columns for row in costs):raise Refusal('matrix_shape')
    if any(c is not None and (type(c) is not int or abs(c)>1000) for row in costs for c in row):raise Refusal('invalid_cost')
    best=None;selected=None
    for permutation in itertools.permutations(range(columns),len(costs)):
        values=[costs[i][c] for i,c in enumerate(permutation)]
        if any(v is None for v in values):continue
        total=sum(values)
        if best is None or total<best:best=total;selected=list(permutation)
    return {'columns':selected,'cost':best}

def evaluate(request):
    try:
        if type(request) is not dict:raise Refusal('invalid_request')
        operation=request.get('op')
        if type(operation) is not str or operation not in REQUIRED:raise Refusal('unknown_operation')
        closed(request,REQUIRED[operation]);graph=graph_record(request['graph']) if 'graph' in request else None
        if operation=='min_cut':result=minimum_cut(graph)
        elif operation=='duality':
            value=maximum_flow(graph)['value'];capacity=minimum_cut(graph)['capacity'];result={'flow_value':value,'cut_capacity':capacity,'equal':value==capacity}
        elif operation in ('remove_arc','increase_capacity'):
            i=request['arc_index']
            if type(i) is not int or not 0<=i<len(graph['arcs']):raise Refusal('invalid_arc_index')
            changed=copy.deepcopy(graph);before=maximum_flow(graph)['value']
            if operation=='remove_arc':
                changed['arcs'].pop(i);after=maximum_flow(changed)['value'];result={'before':before,'after':after,'loss':before-after}
            else:
                delta=request['delta']
                if type(delta) is not int or not 0<=delta<=8:raise Refusal('invalid_delta')
                changed['arcs'][i][2]+=delta;graph_record(changed);after=maximum_flow(changed)['value'];result={'before':before,'after':after,'gain':after-before}
        elif operation=='lower_feasible':result=lower_feasible(graph,request['lower'],request['required'])
        elif operation=='min_cost':result=minimum_cost(graph,request['costs'],request['required'])
        elif operation=='assignment':result=assignment(request['costs'])
        elif operation=='policy_gate':
            required_value(request['required'])
            if any(type(request[k]) is not bool for k in ('consent','evidence','authority')):raise Refusal('invalid_flag')
            enough=maximum_flow(graph)['value']>=request['required'];missing=[] if enough else ['capacity']
            missing.extend(k for k in ('consent','evidence','authority') if not request[k]);missing.append('real_world_verification')
            result={'computationally_feasible':enough,'missing':missing,'external_action':False}
        elif operation=='summary':
            result={'flow_value':maximum_flow(graph)['value'],'cut_capacity':minimum_cut(graph)['capacity'],'node_count':len(graph['nodes']),
                    'evidence_class':'synthetic_only','manual_review':'open_gap'}
        else:
            if request['kind'] not in ('empirical','authority'):raise Refusal('invalid_kind')
            obligation=request['obligation']
            if type(obligation) is not str or not obligation.strip() or len(obligation)>160:raise Refusal('invalid_obligation')
            result={'kind':request['kind'],'obligation':obligation,'evidence_rows':0,'disposition':'open_gap' if request['kind']=='empirical' else 'exact_gate','external_action':False}
        return accepted(copy.deepcopy(result))
    except Refusal as e:return rejected(str(e))
