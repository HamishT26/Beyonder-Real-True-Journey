"""Finite integer flows, residual cancellation, and bounded BFS augmentation."""
import copy
from collections import deque
from scripts.ghc_family_flow_common import Refusal,accepted,rejected,closed,graph_record,flow_vector,balances,feasible,flow_value

REQUIRED={
 'normalize':{'op','graph'},'matrix':{'op','graph'},'balance':{'op','graph','flow'},'feasible':{'op','graph','flow'},
 'value':{'op','graph','flow'},'cut_capacity':{'op','graph','cut'},'residual':{'op','graph','flow'},
 'augmenting_path':{'op','graph','flow'},'augment_once':{'op','graph','flow'},'max_value':{'op','graph'}}

def capacity_matrix(graph):
    positions={v:i for i,v in enumerate(graph['nodes'])};matrix=[[0]*len(positions) for _ in positions]
    for u,v,c in graph['arcs']:matrix[positions[u]][positions[v]]=c
    return matrix

def cut_capacity(graph,cut):
    if type(cut) is not list or any(type(x) is not str for x in cut) or len(set(cut))!=len(cut):raise Refusal('invalid_cut')
    if 's' not in cut or 't' in cut or not set(cut)<=set(graph['nodes']):raise Refusal('invalid_cut')
    return sum(c for u,v,c in graph['arcs'] if u in cut and v not in cut)

def residual_map(graph,flow):
    if not feasible(graph,flow):raise Refusal('infeasible_flow')
    residual={(u,v):0 for u in graph['nodes'] for v in graph['nodes'] if u!=v}
    for (u,v,c),f in zip(graph['arcs'],flow):residual[u,v]+=c-f;residual[v,u]+=f
    return residual

def residual_arcs(graph,flow):
    residual=residual_map(graph,flow)
    return [[u,v,residual[u,v]] for u in graph['nodes'] for v in graph['nodes'] if u!=v and residual[u,v]>0]

def shortest_path(graph,flow):
    residual=residual_map(graph,flow);parents={'s':None};queue=deque(['s'])
    while queue:
        u=queue.popleft()
        for v in graph['nodes']:
            if v not in parents and residual.get((u,v),0)>0:
                parents[v]=u
                if v=='t':
                    path=['t']
                    while parents[path[-1]] is not None:path.append(parents[path[-1]])
                    return list(reversed(path))
                queue.append(v)
    return None

def augment_once(graph,flow):
    flow=flow_vector(graph,flow);path=shortest_path(graph,flow)
    if path is None:return {'flow':flow,'delta':0,'value':flow_value(graph,flow)}
    residual=residual_map(graph,flow);delta=min(residual[u,v] for u,v in zip(path,path[1:]))
    positions={(u,v):i for i,(u,v,_) in enumerate(graph['arcs'])}
    for u,v in zip(path,path[1:]):
        left=delta;reverse=positions.get((v,u))
        if reverse is not None:
            cancelled=min(left,flow[reverse]);flow[reverse]-=cancelled;left-=cancelled
        if left:
            forward=positions.get((u,v))
            if forward is None:raise Refusal('residual_inconsistency')
            flow[forward]+=left
    if not feasible(graph,flow):raise Refusal('augmentation_infeasible')
    return {'flow':flow,'delta':delta,'value':flow_value(graph,flow)}

def maximum_flow(graph):
    flow=[0]*len(graph['arcs'])
    # Integer capacities and the finite profile give a strict upper bound.
    for _ in range(sum(c for _,_,c in graph['arcs'])+1):
        result=augment_once(graph,flow)
        if result['delta']==0:return result
        flow=result['flow']
    raise Refusal('work_limit')

def evaluate(request):
    try:
        if type(request) is not dict:raise Refusal('invalid_request')
        operation=request.get('op')
        if type(operation) is not str or operation not in REQUIRED:raise Refusal('unknown_operation')
        closed(request,REQUIRED[operation]);graph=graph_record(request['graph'])
        flow=flow_vector(graph,request['flow']) if 'flow' in request else None
        if operation=='normalize':result={'nodes':graph['nodes'],'arcs':sorted(graph['arcs'])}
        elif operation=='matrix':result=capacity_matrix(graph)
        elif operation=='balance':result=balances(graph,flow)
        elif operation=='feasible':result=feasible(graph,flow)
        elif operation=='value':result=flow_value(graph,flow)
        elif operation=='cut_capacity':result=cut_capacity(graph,request['cut'])
        elif operation=='residual':result=residual_arcs(graph,flow)
        elif operation=='augmenting_path':result=shortest_path(graph,flow)
        elif operation=='augment_once':result=augment_once(graph,flow)
        else:result=maximum_flow(graph)['value']
        return accepted(copy.deepcopy(result))
    except Refusal as e:return rejected(str(e))
