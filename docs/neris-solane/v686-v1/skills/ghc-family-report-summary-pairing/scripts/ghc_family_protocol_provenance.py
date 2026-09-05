"""Finite derivation graphs, explicit byte domains, and non-destructive merges."""
import argparse,hashlib,heapq,json
from pathlib import Path
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def lineage(d):
    nodes=d['nodes'];edges=d['edges']
    if len(nodes)!=len(set(nodes)):return {'error':'duplicate_node'}
    if any(a not in nodes or b not in nodes for a,b in edges):return {'error':'missing_node'}
    indegree={n:0 for n in nodes};children={n:set() for n in nodes}
    for a,b in edges:
        if b not in children[a]:children[a].add(b);indegree[b]+=1
    ready=[n for n in nodes if indegree[n]==0];heapq.heapify(ready);result=[]
    while ready:
        n=heapq.heappop(ready);result.append(n)
        for c in sorted(children[n]):
            indegree[c]-=1
            if indegree[c]==0:heapq.heappush(ready,c)
    return result if len(result)==len(nodes) else {'error':'cycle'}
def fixity(d):
    domain=d['domain']
    if domain not in ['utf8','normalized_lf_utf8']:return {'error':'unknown_domain'}
    def b(x):return (x.replace('\r\n','\n') if domain=='normalized_lf_utf8' else x).encode('utf8')
    return hashlib.sha256(b(d['left'])).digest()==hashlib.sha256(b(d['right'])).digest()
def merge(d):
    left=d['left'];right=d['right']
    if any(canonical(left[k])!=canonical(right[k]) for k in set(left)&set(right)):return {'error':'conflict'}
    return {**left,**right}
OPERATIONS={'lineage':lineage,'fixity':fixity,'merge':merge}
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
