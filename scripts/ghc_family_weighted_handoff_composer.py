"""Compose bounded handoff evidence; never send or change a task."""
import argparse,json,pathlib
from ghc_family_capacity_core import fields,ContractError,strict_json,evaluate as capacity
from ghc_family_inference_core import evaluate as inference
from ghc_family_weighted_route_review import review

def compose(request):
    try:
        fields(request,['profile','route','relative_astra_cost','sizes','prefix','limit','events'])
        route=review(request['route'],request['profile'])
        cost=capacity({'op':'mix_cost','astra_cost':request['relative_astra_cost']})
        batches=capacity({'op':'context_batches','sizes':request['sizes'],'prefix':request['prefix'],'limit':request['limit']})
        attempts=inference({'op':'checkpoint','events':request['events']})
        for result in [cost,batches,attempts]:
            if not result['ok']:raise ContractError(result['error'])
        return {'ok':True,'value':{'route':route,'cost':cost['value'],'context':batches['value'],'checkpoint':attempts['value'],'messages_sent':0,'units':'caller supplied context units; not measured model tokens'},'error':None}
    except ContractError as ex:return {'ok':False,'value':None,'error':str(ex)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output');a=ap.parse_args()
    p=pathlib.Path(a.input)
    if p.stat().st_size>4_000_000:raise ValueError('Input exceeds four million bytes')
    result=compose(strict_json(p.read_text(encoding='utf-8-sig')));text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:
        with pathlib.Path(a.output).open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    else:print(text,end='')
