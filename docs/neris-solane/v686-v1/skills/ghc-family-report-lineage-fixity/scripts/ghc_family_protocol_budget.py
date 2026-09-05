"""Pure accounting relations for synthetic protocol budgets and denominators."""
import argparse,json
from collections import Counter
from pathlib import Path
def nonnegative(x):return type(x) is int and x>=0
def budget(d):
    arms=d['arms'];cap=d['cap']
    if len(arms)!=2:return {'error':'two_arms_required'}
    if not nonnegative(cap) or any(not nonnegative(x) for arm in arms for x in arm):return {'error':'nonnegative_integer_required'}
    totals=[sum(a) for a in arms]
    return {'totals':totals,'matched':totals[0]==totals[1],'within_cap':all(x<=cap for x in totals)}
def allocation(d):
    seq=d['sequence']
    if any(x not in ['A','B'] for x in seq):return {'error':'unknown_arm'}
    a=seq.count('A');b=seq.count('B');return {'A':a,'B':b,'imbalance':abs(a-b)}
def separation(d):
    a=d['evaluators'];b=d['key_holders']
    if len(a)!=len(set(a)) or len(b)!=len(set(b)):return {'error':'duplicate_role_member'}
    return sorted(set(a)&set(b))
def denominator(d):
    rows=d['rows'];labels=['observed','missing','excluded']
    if any(x not in labels for x in rows):return {'error':'unknown_disposition'}
    counts=Counter(rows);return {'total':len(rows),**{k:counts[k] for k in labels}}
OPERATIONS={'budget':budget,'allocation':allocation,'separation':separation,'denominator':denominator}
def evaluate(operation,data):
    if operation not in OPERATIONS:return {'error':'unknown_operation'}
    try:return OPERATIONS[operation](data)
    except (KeyError,TypeError,ValueError,IndexError):return {'error':'malformed_input'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--operation',required=True,choices=OPERATIONS);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();text=json.dumps(evaluate(a.operation,json.loads(Path(a.input).read_text(encoding='utf8'))),ensure_ascii=False,sort_keys=True)+'\n'
    if a.output:
        with Path(a.output).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    else:print(text,end='')
if __name__=='__main__':main()
