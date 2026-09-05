"""Exact finite-fixture arithmetic; no inference about real-world populations."""
import argparse,json
from fractions import Fraction
from pathlib import Path
def numbers(seq):
    if any(type(v) not in [int,str] for v in seq):raise ValueError('Exact integers or rational strings required')
    return [Fraction(v) for v in seq]
def summary(d):
    x=numbers(d['values']);n=len(x);stat=d['stat']
    if not n or (stat=='sample_variance' and n<2):return {'error':'insufficient_data'}
    mean=sum(x)/n
    if stat=='mean':v=mean
    elif stat=='median':
        x=sorted(x);v=x[n//2] if n%2 else (x[n//2-1]+x[n//2])/2
    elif stat in ['sample_variance','population_variance']:v=sum((a-mean)**2 for a in x)/(n-1 if stat=='sample_variance' else n)
    else:return {'error':'unknown_statistic'}
    return str(v)
def paired(d):
    a=d['a'];b=d['b'];left=dict(a);right=dict(b)
    if len(left)!=len(a) or len(right)!=len(b):return {'error':'duplicate_pair'}
    if set(left)!=set(right):return {'error':'pair_set_mismatch'}
    return [[label,str(numbers([value])[0]-numbers([right[label]])[0])] for label,value in a]
def histogram(d):
    values=numbers(d['values']);edges=numbers(d['edges'])
    if len(edges)<2 or any(a>=b for a,b in zip(edges,edges[1:])):return {'error':'invalid_edges'}
    counts=[0]*(len(edges)-1)
    for x in values:
        if x<edges[0] or x>edges[-1]:return {'error':'outside_edges'}
        for i,(a,b) in enumerate(zip(edges,edges[1:])):
            if a<=x<b or (i==len(counts)-1 and x==b):counts[i]+=1;break
    return counts
def stop(d):
    spent=d['spent'];cap=d['cap']
    if type(spent) is not int or type(cap) is not int or min(spent,cap)<0:return {'error':'invalid_budget'}
    if type(d['safety']) is not bool or type(d['done']) is not bool:return {'error':'invalid_flag'}
    if d.get('peek',False):return {'error':'unregistered_peek'}
    if d['safety']:return 'safety_stop'
    if spent>=cap:return 'budget_stop'
    if d['done']:return 'record'
    return 'continue'
OPERATIONS={'summary':summary,'paired':paired,'histogram':histogram,'stop':stop}
def evaluate(operation,data):
    if operation not in OPERATIONS:return {'error':'unknown_operation'}
    try:return OPERATIONS[operation](data)
    except (KeyError,TypeError,ValueError,IndexError,ZeroDivisionError):return {'error':'malformed_input'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--operation',required=True,choices=OPERATIONS);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();text=json.dumps(evaluate(a.operation,json.loads(Path(a.input).read_text(encoding='utf8'))),ensure_ascii=False,sort_keys=True)+'\n'
    if a.output:
        with Path(a.output).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    else:print(text,end='')
if __name__=='__main__':main()
