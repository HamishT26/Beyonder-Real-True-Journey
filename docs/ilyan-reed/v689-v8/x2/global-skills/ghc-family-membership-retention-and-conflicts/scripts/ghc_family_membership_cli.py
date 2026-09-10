"""Portable request dispatcher; output is exclusive and execution is offline."""
import argparse,json
from pathlib import Path
import ghc_family_membership_x1 as x1
def evaluate(request):
    if isinstance(request,dict) and request.get('operation') in x1.FIELDS:return x1.evaluate(request)
    try:import ghc_family_membership_x2 as x2
    except ModuleNotFoundError:return {'ok':False,'error':'unknown_operation','original_success_credit':0}
    return x2.evaluate(request)
def main(allowed):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();request=json.loads(Path(a.input).read_text(encoding='utf8'))
    result=evaluate(request) if isinstance(request,dict) and request.get('operation') in allowed else {'ok':False,'error':'runner_scope','original_success_credit':0}
    s=json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n'
    if a.output:
        with Path(a.output).open('x',encoding='utf8',newline='\n') as f:f.write(s)
    else:print(s,end='')
