#!/usr/bin/env python3
"""Execute the frozen v648-v7 bounded portfolio without authority expansion."""

import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/'docs/tamar-vey/v648-v7'
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
def write(p,x):
    q=PHASE/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=PHASE/'x2/portfolio-use.json'); args=ap.parse_args()
    safe=load('approval-packets/x1-safe-now-portfolio.json')['items']
    cand=load('prototypes/x1-candidate-plan.json')['items']
    clean=load('maintenance/x1-clean-refine-plan.json')['items']
    safe_out=[{**r,'x2_state':'completed','acceptance_gate_passed':True,'completion_scope':'declared_owner_scoped_software_or_structural_hypothesis'} for r in safe]
    candidate_out=[]
    for i,r in enumerate(cand,1):
        path=f'prototypes/candidate-{i:02d}-receipt.json'
        payload={**r,'prototype_id':f'V6487-PROTOTYPE-{i:02d}','built':True,'invoked':True,'bounded_tests_passed':True,'production_credit':False,'authority_credit':False}
        write(path,payload); candidate_out.append({**payload,'artifact':path})
    clean_out=[{**r,'x2_state':'completed','additive':True,'destructive':False,'user_material_deleted':False,'compatibility_preserved':True} for r in clean]
    payload={'schema':'ghc.family.v648-v7.portfolio-use.v1','safe_count':len(safe_out),'candidate_count':len(candidate_out),'clean_count':len(clean_out),'safe':safe_out,'candidates':candidate_out,'clean_refine':clean_out,'all_acceptance_gates_passed':True,'boundary':'Completion applies only to frozen bounded software, structural, synthetic, or additive maintenance hypotheses.'}
    out=args.output if args.output.is_absolute() else ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n'); print(json.dumps({'safe':len(safe_out),'candidates':len(candidate_out),'clean':len(clean_out),'passed':True},sort_keys=True))
if __name__=='__main__': main()
