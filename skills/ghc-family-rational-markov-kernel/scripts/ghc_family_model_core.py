"""Finite probability, review-record and number-theory computations; no external actions."""
import math
import re
import sys
from fractions import Fraction
from ghc_family_workflow_core import (ContractError, OUTCOMES, array, boolean,
    integer, labels, record, require, text, cli as base_cli)

def rational(value):
    if type(value) is int:
        integer(value,-1_000_000_000,1_000_000_000)
        return Fraction(value)
    require(type(value) is str,'type')
    require(len(value)<=32 and re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?',value) is not None)
    result=Fraction(value)
    require(abs(result.numerator)<=1_000_000_000 and result.denominator<=1_000_000_000)
    return result

def probability(values,size=None):
    values=array(values,8)
    require(bool(values) and (size is None or len(values)==size),'shape')
    result=[rational(v) for v in values]
    require(all(v>=0 for v in result) and sum(result)==1)
    return result

def kernel(values):
    values=array(values,8);require(bool(values),'shape');size=len(values);result=[]
    for row in values:
        row=array(row,8);require(len(row)==size,'shape')
        parsed=[rational(v) for v in row]
        require(all(v>=0 for v in parsed) and sum(parsed)==1)
        result.append(parsed)
    return result

def multiply(distribution,matrix):
    return [sum(distribution[i]*matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix))]

def stringify(value):
    if isinstance(value,Fraction):return str(value)
    if isinstance(value,list):return [stringify(v) for v in value]
    if isinstance(value,dict):return {k:stringify(v) for k,v in value.items()}
    return value

def decimal(value):
    require(math.isfinite(value))
    result=f'{value:.12f}'
    return '0.000000000000' if result=='-0.000000000000' else result

def solve(matrix,rhs):
    """Exact Gaussian elimination with uniqueness and consistency checks."""
    size=len(matrix)
    if not size:return []
    rows=[list(row)+[value] for row,value in zip(matrix,rhs)]
    require(len(rhs)==size and all(len(row)==size for row in matrix),'shape')
    rank=0;pivots=[]
    for col in range(size):
        pivot=next((r for r in range(rank,size) if rows[r][col]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        divisor=rows[rank][col]
        rows[rank]=[v/divisor for v in rows[rank]]
        for other in range(size):
            if other==rank:continue
            factor=rows[other][col]
            if factor:rows[other]=[a-factor*b for a,b in zip(rows[other],rows[rank])]
        pivots.append(col);rank+=1
    require(all(any(row[:-1]) or row[-1]==0 for row in rows),'domain')
    require(rank==size,'non_unique')
    answer=[Fraction(0)]*size
    for row,col in enumerate(pivots):answer[col]=rows[row][-1]
    return answer

def stationary_inputs(r,positive=False):
    matrix=kernel(r['matrix']);pi=probability(r['stationary'],len(matrix))
    require(multiply(pi,matrix)==pi)
    if positive:require(all(v>0 for v in pi))
    return matrix,pi

def stochastic_matrix(r):
    matrix=kernel(r['matrix'])
    return {'states':len(matrix),'row_sums':[str(sum(row)) for row in matrix]}

def markov_step(r):
    matrix=kernel(r['matrix']);p=probability(r['distribution'],len(matrix))
    return stringify(multiply(p,matrix))

def stationary_distribution(r):
    matrix=kernel(r['matrix']);n=len(matrix)
    equations=[[matrix[j][i]-Fraction(i==j) for j in range(n)] for i in range(n-1)]
    equations.append([Fraction(1)]*n)
    pi=solve(equations,[Fraction(0)]*(n-1)+[Fraction(1)])
    require(all(v>=0 for v in pi) and sum(pi)==1 and multiply(pi,matrix)==pi)
    return stringify(pi)

def detailed_balance(r):
    matrix,pi=stationary_inputs(r);n=len(matrix)
    return all(pi[i]*matrix[i][j]==pi[j]*matrix[j][i] for i in range(n) for j in range(n))

def time_reversal(r):
    matrix,pi=stationary_inputs(r,positive=True);n=len(matrix)
    return stringify([[pi[j]*matrix[j][i]/pi[i] for j in range(n)] for i in range(n)])

def probability_current(r):
    matrix,pi=stationary_inputs(r);n=len(matrix)
    return stringify([[pi[i]*matrix[i][j]-pi[j]*matrix[j][i] for j in range(n)] for i in range(n)])

def entropy(r):
    p=probability(r['distribution'])
    return decimal(-sum(float(v)*math.log(float(v)) for v in p if v))

def paired(r):
    p=probability(r['p']);q=probability(r['q'],len(p))
    return p,q

def relative_entropy(r):
    p,q=paired(r);mismatch=[i for i,(a,b) in enumerate(zip(p,q)) if a>0 and b==0]
    value=None if mismatch else decimal(sum(float(a)*math.log(float(a/b)) for a,b in zip(p,q) if a))
    return {'nats':value,'support_mismatch':mismatch}

def entropy_production(r):
    matrix,pi=stationary_inputs(r);n=len(matrix)
    flow=[[pi[i]*matrix[i][j] for j in range(n)] for i in range(n)]
    one_way=[[i,j] for i in range(n) for j in range(n) if flow[i][j]>0 and flow[j][i]==0]
    value=None if one_way else decimal(sum(float(flow[i][j])*math.log(float(flow[i][j]/flow[j][i]))
                for i in range(n) for j in range(n) if flow[i][j]))
    return {'nats_per_step':value,'one_way_edges':one_way}

def coarse_grain(r):
    matrix,pi=stationary_inputs(r);n=len(matrix);groups=array(r['groups'],8)
    require(bool(groups));flat=[]
    for group in groups:
        group=array(group,8);require(bool(group))
        for state in group:integer(state,0,n-1);flat.append(state)
    require(len(flat)==len(set(flat)),'duplicate')
    require(set(flat)==set(range(n)))
    weights=[sum(pi[i] for i in group) for group in groups]
    require(all(weight>0 for weight in weights))
    projected=[[sum(pi[i]*matrix[i][j] for i in left for j in right)/weight
                 for right in groups] for left,weight in zip(groups,weights)]
    lumpable=all(all(sum(matrix[i][j] for j in right)==sum(matrix[left[0]][j] for j in right)
                  for i in left for right in groups) for left in groups)
    return stringify({'weights':weights,'matrix':projected,'lumpable':lumpable})

def target_inputs(r):
    matrix=kernel(r['matrix']);targets=array(r['targets'],8)
    require(bool(targets))
    for target in targets:integer(target,0,len(matrix)-1)
    require(len(targets)==len(set(targets)),'duplicate')
    return matrix,targets

def first_hit(matrix,targets):
    n=len(matrix);reachable=set(targets)
    while True:
        enlarged=reachable|{i for i in range(n) if any(matrix[i][j]>0 for j in reachable)}
        if enlarged==reachable:break
        reachable=enlarged
    transient=sorted(reachable-set(targets))
    a=[[Fraction(i==j)-matrix[i][j] for j in transient] for i in transient]
    result=[[Fraction(0)]*len(targets) for _ in range(n)]
    for col,target in enumerate(targets):
        result[target][col]=Fraction(1)
        solution=solve(a,[matrix[i][target] for i in transient])
        for i,value in zip(transient,solution):result[i][col]=value
    require(all(all(v>=0 for v in row) and sum(row)<=1 for row in result))
    return result

def absorption_probabilities(r):
    matrix,targets=target_inputs(r)
    return stringify(first_hit(matrix,targets))

def hitting_times(r):
    matrix,targets=target_inputs(r);n=len(matrix);probabilities=first_hit(matrix,targets)
    finite=[i for i in range(n) if i not in targets and sum(probabilities[i])==1]
    equations=[[Fraction(i==j)-matrix[i][j] for j in finite] for i in finite]
    values=solve(equations,[Fraction(1)]*len(finite))
    result=[None]*n
    for i in targets:result[i]=Fraction(0)
    for i,value in zip(finite,values):require(value>=0);result[i]=value
    return stringify(result)

def distribution_distance(r):
    p,q=paired(r);l1=sum(abs(a-b) for a,b in zip(p,q))
    return stringify({'l1':l1,'tv':l1/2})

def coupling_bounds(r):
    p,q=paired(r)
    return stringify({'minimum_disagreement':sum(abs(a-b) for a,b in zip(p,q))/2,
                      'independent_disagreement':1-sum(a*b for a,b in zip(p,q))})

def risk_register_projection(r):
    rows=array(r['rows']);ids=[];result=[]
    for row in rows:
        record(row,{'id','likelihood','impact','evidence'});ids.append(text(row['id']))
        likelihood=integer(row['likelihood'],1,5);impact=integer(row['impact'],1,5)
        evidence=text(row['evidence']);require(evidence in OUTCOMES)
        result.append({'id':row['id'],'score':likelihood*impact,'evidence':evidence})
    require(len(ids)==len(set(ids)),'duplicate')
    return sorted(result,key=lambda row:(-row['score'],row['id']))

def consent_scope_check(r):
    grant=record(r['grant'],{'actions','resources','purpose','expires','revoked'})
    actions=labels(grant['actions']);resources=labels(grant['resources']);purpose=text(grant['purpose'])
    expires=integer(grant['expires']);revoked=boolean(grant['revoked']);now=integer(r['now'])
    action=text(r['action']);resource=text(r['resource']);requested_purpose=text(r['purpose'])
    matches=not revoked and now<expires and action in actions and resource in resources and requested_purpose==purpose
    return {'matches':matches,'authority_granted':False}

def remedy_queue(r):
    rows=array(r['rows']);ids=[]
    for row in rows:
        record(row,{'id','urgency','ordinal'});ids.append(text(row['id']))
        integer(row['urgency'],0,3);integer(row['ordinal'])
    require(len(ids)==len(set(ids)),'duplicate')
    ordered=sorted(rows,key=lambda row:(-row['urgency'],row['ordinal'],row['id']))
    return {'order':[row['id'] for row in ordered],'decisions_taken':0}

def review_coverage(r):
    required=labels(r['required']);observed=array(r['observed']);areas=[];covered=[]
    for row in observed:
        record(row,{'area','state'});area=text(row['area']);state=text(row['state'])
        require(area in required and state in OUTCOMES);areas.append(area)
        if state=='completed':covered.append(area)
    require(len(areas)==len(set(areas)),'duplicate')
    missing=sorted(set(required)-set(covered))
    return {'covered':sorted(covered),'missing':missing,'complete':not missing}

def egyptian_fraction_search(r):
    n=integer(r['n'],2,1000);maximum=integer(r['max_denominator'],1,1_000_000);budget=integer(r['max_pairs'],1,100000)
    pairs=0
    for x in range(n//4+1,min(3*n//4,maximum)+1):
        residual=Fraction(4,n)-Fraction(1,x)
        lower=max(x,residual.denominator//residual.numerator+1)
        upper=min(maximum,(2*residual.denominator)//residual.numerator)
        for y in range(lower,upper+1):
            if pairs>=budget:return {'witness':None,'coverage':'pair_budget_exhausted'}
            pairs+=1
            rest=residual-Fraction(1,y)
            if rest<=0:continue
            z=1/rest
            if z.denominator==1 and y<=z<=maximum:
                return {'witness':[x,y,z.numerator],'coverage':'found_within_bounds'}
    return {'witness':None,'coverage':'bounded_no_witness'}

def egyptian_fraction_verify(r):
    n=integer(r['n'],2,1000);denominators=array(r['denominators'],3)
    require(len(denominators)==3,'shape')
    for denominator in denominators:integer(denominator,1,1_000_000_000)
    residual=Fraction(4,n)-sum(Fraction(1,d) for d in denominators)
    return {'valid':residual==0,'residual':str(residual)}

FIELDS={
 'stochastic_matrix':{'matrix'},'markov_step':{'matrix','distribution'},
 'stationary_distribution':{'matrix'},'detailed_balance':{'matrix','stationary'},
 'time_reversal':{'matrix','stationary'},'probability_current':{'matrix','stationary'},
 'entropy':{'distribution'},'relative_entropy':{'p','q'},
 'entropy_production':{'matrix','stationary'},'coarse_grain':{'matrix','stationary','groups'},
 'absorption_probabilities':{'matrix','targets'},'hitting_times':{'matrix','targets'},
 'distribution_distance':{'p','q'},'coupling_bounds':{'p','q'},
 'risk_register_projection':{'rows'},'consent_scope_check':{'grant','action','resource','purpose','now'},
 'remedy_queue':{'rows'},'review_coverage':{'required','observed'},
 'egyptian_fraction_search':{'n','max_denominator','max_pairs'},'egyptian_fraction_verify':{'n','denominators'}}
OPERATIONS={name:globals()[name] for name in FIELDS}

def evaluate(request,allowed=None):
    try:
        require(type(request) is dict,'type');op=text(request.get('op'))
        require(op in FIELDS and (allowed is None or op in allowed))
        record(request,FIELDS[op]|{'op'})
        return {'ok':True,'value':OPERATIONS[op](request),'error':None}
    except ContractError as error:
        return {'ok':False,'value':None,'error':str(error)}

def cli(allowed=None):return base_cli(allowed,evaluator=evaluate)

if __name__=='__main__':sys.exit(cli())
