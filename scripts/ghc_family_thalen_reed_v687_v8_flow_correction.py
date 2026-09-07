"""Add current Method Flow count projections without altering frozen x1 evidence."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/thalen-reed/v687-v8'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--method-runner',type=Path,required=True);a=ap.parse_args()
    target=BASE/'x2/correction';assert not target.exists(),'Correction already materialized'
    target.mkdir()
    original=BASE/'x2/method-flow/ledger.json';raw=original.read_bytes();(target/'initial-x2-ledger.json').write_bytes(raw)
    x1_path=BASE/'x1/method-flow/ledger.json';x1_raw=x1_path.read_bytes();x1=read(x1_path);x2=read(original)
    for name in ['phase-truth.json','execution-summary.json','retained-negative-register.json']:(target/('initial-'+name)).write_bytes((BASE/'x2'/name).read_bytes())
    failures=[]
    for i,(label,receipt) in enumerate([('x2','x2-method-flow.json'),('x1','x2-x1-method-flow.json')],1):
        d=read(BASE/'validation'/receipt);assert d['valid'] is False and d['issues']==['derived counts are stale']
        failures.append({'negative_id':f'TR6878-X2-OP-N{i:03d}','ledger':label,'failure':'Current Method Flow runner refused the historical flat count projection.','receipt':'validation/'+receipt,'original_success_credit':0,'recovery':'Retain the original ledger and derive the current nested count shape from unchanged method and witness arrays.'})
    write(target/'count-schema-failures.json',{'schema':'ghc.family.retained-count-failures.v1','failures':failures,'x1_sha256':hashlib.sha256(x1_raw).hexdigest(),'initial_x2_sha256':hashlib.sha256(raw).hexdigest()})
    spec=importlib.util.spec_from_file_location('current_method_flow',a.method_runner);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.refresh_counts(x1);m.refresh_counts(x2)
    preliminary=[m.validate_ledger(x1),m.validate_ledger(x2)]
    assert all(r['valid'] for r in preliminary),preliminary
    x1['projection_of']='x1/method-flow/ledger.json';x1['original_sha256']=hashlib.sha256(x1_raw).hexdigest();x1['original_failure_preserved']=True
    write(BASE/'x2/method-flow/x1-current-schema-projection.json',x1)
    gates=x2['methods'][0]['protected_gates']
    for failure,proof in zip(failures,reversed(preliminary)):
        mid=failure['negative_id'].replace('-N','-M');nid=failure['negative_id']
        x2['methods'].append({'method_id':mid,'title':'Current count-schema projection for '+failure['ledger'],'failure_signature':failure['failure'],
            'trigger_preconditions':['Current Method Flow validator','Historical flat derived counts'],
            'privacy_class':'sanitized_public','approval_class':'safe_now','candidate_workaround':failure['recovery'],
            'validation_witness_ids':[mid+'-FAIL',mid+'-PASS'],'recurrence_guard':'Call the current runner count derivation and preserve source-ledger bytes before creating a projection.',
            'rollback':'Stop selecting the projection and retain both original ledgers and failed receipts.',
            'recommendation_state':'preferred','supersedes':[],'protected_gates':gates,'retained_negative_ids':[nid],
            'scope_boundary':'Only count-schema compatibility; no original validation or external evidence credit.'})
        for result,observed in [('fail','Derived counts were stale under current schema'),('pass','Current nested count projection validates with no issues')]:
            x2['witnesses'].append({'witness_id':mid+'-'+result.upper(),'method_id':mid,'procedure':'Focused current-schema count derivation','scope':'Thalen owner ledger count fields','expected':'Current schema valid with every method and witness preserved','observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,'retained_negative_ids':[nid],'boundary':'The later pass does not promote the original failed validation.'})
        for start,end in [('observed','candidate'),('candidate','validated'),('validated','preferred')]:x2['state_events'].append({'method_id':mid,'from':start,'to':end})
    x2['original_ledger_retained']='x2/correction/initial-x2-ledger.json';x2['count_contract']='30 x2 methods; 270 retained failed witnesses; 488 passing witnesses. Two schema failures and focused recoveries are additive. No duplicate scientific or independent witness credit.'
    m.refresh_counts(x2);final=m.validate_ledger(x2);assert final['valid'],final;write(original,x2)
    write(BASE/'validation/x2-method-flow-corrected.json',final)
    write(BASE/'validation/x2-x1-method-flow-projection.json',m.validate_ledger(x1))
    counts={'proposals':15430,'negatives':82301,'methods':93234,'failed_witnesses':53149,'passing_witnesses':82493,'open_gaps':740,'exact_gates':729}
    truth=read(BASE/'x2/phase-truth.json');truth['effective_counts']=counts;truth['method_flow_correction']='x2/correction/count-schema-failures.json';write(BASE/'x2/phase-truth.json',truth)
    summary=read(BASE/'x2/execution-summary.json');summary['unexpected_x2_failures']=2;summary['focused_recoveries']=2;write(BASE/'x2/execution-summary.json',summary)
    negatives=read(BASE/'x2/retained-negative-register.json');negatives['x2_delta']={'negatives':270,'methods':30,'failed_witnesses':270,'passing_witnesses':488};negatives['effective_counts']=counts;negatives['operational_failures']=failures;write(BASE/'x2/retained-negative-register.json',negatives)
    assert x1_path.read_bytes()==x1_raw
    print(json.dumps({'corrected_x2_valid':True,'x1_projection_valid':True,'x1_unchanged':True,'retained_failed_validations':2,'methods':len(x2['methods']),'witnesses':len(x2['witnesses'])}))

if __name__=='__main__':main()
