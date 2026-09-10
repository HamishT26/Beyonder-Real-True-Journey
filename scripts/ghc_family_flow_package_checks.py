"""Frozen bounded interfaces; PuLP and highspy use the same HiGHS backend."""
import copy,json,sys
from pathlib import Path
import highspy
import pulp
import maxflow

def highs_value(graph):
    model=highspy.Highs();model.setOptionValue('output_flag',False);model.setOptionValue('threads',1);model.setOptionValue('time_limit',5.0)
    variables=[model.addVariable(lb=0,ub=c,name=f'e{i}') for i,(_,_,c) in enumerate(graph['arcs'])]
    def balance(v):return sum((variables[i] for i,(a,_,_) in enumerate(graph['arcs']) if a==v),0)-sum((variables[i] for i,(_,b,_) in enumerate(graph['arcs']) if b==v),0)
    for vertex in graph['nodes']:
        if vertex not in ('s','t'):
            expression=balance(vertex)
            if not isinstance(expression,int):model.addConstr(expression==0)
    objective=balance('s')
    if isinstance(objective,int):objective=model.addVariable(lb=0,ub=0,name='constant_zero')
    model.addConstr(objective>=0);model.maximize(objective)
    assert model.getModelStatus()==highspy.HighsModelStatus.kOptimal
    value=model.getObjectiveValue();assert abs(value-round(value))<1e-9;return round(value)

def pulp_value(graph):
    model=pulp.LpProblem('synthetic_flow',pulp.LpMaximize)
    variables=[pulp.LpVariable(f'e{i}',lowBound=0,upBound=c) for i,(_,_,c) in enumerate(graph['arcs'])]
    def balance(v):return pulp.lpSum(variables[i] for i,(a,_,_) in enumerate(graph['arcs']) if a==v)-pulp.lpSum(variables[i] for i,(_,b,_) in enumerate(graph['arcs']) if b==v)
    for vertex in graph['nodes']:
        if vertex not in ('s','t'):model+=balance(vertex)==0
    objective=balance('s')
    if not graph['arcs']:objective=pulp.LpVariable('constant_zero',lowBound=0,upBound=0)
    model+=objective;model+=objective>=0
    status=model.solve(pulp.HiGHS(msg=False,threads=1,timeLimit=5));assert status==pulp.LpStatusOptimal
    value=pulp.value(objective)
    if value is None and not graph['arcs']:return 0
    assert value is not None and abs(value-round(value))<1e-9;return round(value)

def maxflow_value(graph):
    network=maxflow.Graph[int]();network.add_nodes(len(graph['nodes']));position={v:i for i,v in enumerate(graph['nodes'])}
    for u,v,c in graph['arcs']:network.add_edge(position[u],position[v],c,0)
    bound=sum(c for _,_,c in graph['arcs'])+1;network.add_tedge(position['s'],bound,0);network.add_tedge(position['t'],0,bound)
    return int(network.maxflow())

def main():
    base=Path(__file__).resolve().parents[1]/'docs/mira-fenwick/v690-v3'
    plan=json.loads((base/'x1/package-smoke-plan.json').read_text());assert plan['frozen_before_installation']
    rows=json.loads((base/'plan/new-proposals.json').read_text(encoding='utf-8'))['proposals']
    samples=[r for r in rows if r['operation']=='summary'];checks=[]
    for name,fn in [('highspy',highs_value),('PuLP',pulp_value),('PyMaxflow',maxflow_value)]:
        for row in samples:
            graph=copy.deepcopy(row['request']['graph']);original=copy.deepcopy(graph);value=fn(graph);expected=row['expected_envelope']['result']['flow_value']
            checks.append({'interface':name,'sample_reference':row['proposal_id'],'core_proposal_credit':0,'sample_role':'frozen shared graph input; future operation not executed','expected':expected,'observed':value,'pass':value==expected and graph==original,'same_owner_only':True,'numeric_comparison':'HiGHS values must lie within absolute 1e-9 of an integer; PyMaxflow uses integer capacities.'})
    adverse=[]
    model=highspy.Highs();model.setOptionValue('output_flag',False);model.setOptionValue('threads',1);x=model.addVariable(lb=0,ub=1);model.addConstr(x>=2);model.run()
    adverse.append({'interface':'highspy','subject':'contradictory bounded linear constraints','observed':'kInfeasible' if model.getModelStatus()==highspy.HighsModelStatus.kInfeasible else str(model.getModelStatus()),'guard_pass':model.getModelStatus()==highspy.HighsModelStatus.kInfeasible,'original_success_credit':0})
    try:pulp.LpVariable('nonfinite',lowBound=float('nan'));adverse.append({'interface':'PuLP','guard_pass':False,'original_success_credit':0})
    except pulp.PulpError:adverse.append({'interface':'PuLP','subject':'nonfinite lower bound','observed':'PulpError','guard_pass':True,'original_success_credit':0})
    try:maxflow.Graph[object];adverse.append({'interface':'PyMaxflow','guard_pass':False,'original_success_credit':0})
    except KeyError:adverse.append({'interface':'PyMaxflow','subject':'unsupported object dtype','observed':'KeyError','guard_pass':True,'original_success_credit':0})
    result={'comparisons':checks,'adverse_subjects':adverse,'comparison_count':len(checks),'pass':all(c['pass'] for c in checks) and all(c['guard_pass'] for c in adverse),
            'same_owner_only':True,'independent_reproduction':False,'backend_count':2,'interface_count':3,'shared_backend_notice':plan['shared_backend_notice']}
    with (base/'x1/toolchain/package-checks.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({'comparisons':len(checks),'adverse_subjects':len(adverse),'pass':result['pass']}));return 0 if result['pass'] else 1

if __name__=='__main__':raise SystemExit(main())
