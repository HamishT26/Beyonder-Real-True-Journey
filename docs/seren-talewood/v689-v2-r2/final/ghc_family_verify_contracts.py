"""Check exact typed contract envelopes against one immutable owner stage."""
import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True);parser.add_argument('--stage',choices=['x1','x2'],required=True)
    args=parser.parse_args();sys.path.insert(0,str(args.root/'scripts'))
    name='ghc_family_workflow_core' if args.stage=='x1' else 'ghc_family_model_core'
    spec=importlib.util.spec_from_file_location(name,args.root/'scripts'/(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=json.loads((args.root/'docs/seren-talewood/v689-v2-r2/plan/new-proposals.json').read_text())
    rows=[r for r in data['proposals'] if r['stage']==args.stage];assert len(rows)==100
    for row in rows:
        before=copy.deepcopy(row['input']);result=module.evaluate(row['input'])
        assert same(result,row['expected']) and same(before,row['input']),row['proposal_id']
    print(json.dumps(dict(stage=args.stage,typed_contracts=100,all_matched=True,input_mutations=0)))

if __name__=='__main__':main()
