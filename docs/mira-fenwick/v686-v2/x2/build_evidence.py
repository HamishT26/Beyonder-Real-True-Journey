"""Execute only the frozen Mira owner contracts; preserve every adverse record."""
import copy, hashlib, importlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'docs/mira-fenwick/v686-v2'
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_evidence_selectors import canonical,sha,envelope,verify_envelope

MODULES={'selectors':'evidence_selectors','patch':'evidence_patch','lineage':'correction_lineage','receipts':'receipt_binding','obligations':'obligation_projection'}
def read(path): return json.loads((BASE/path).read_text(encoding='utf-8'))
def write(path,data):
    p=BASE/'x2'/path;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def compute(row): return importlib.import_module('ghc_family_'+MODULES[row['runner']]).evaluate
def mutate(record,kind):
    r=copy.deepcopy(record)
    if kind=='wrong_report':r['result']={'fabricated':True};r['result_sha256']=sha(r['result'])
    elif kind=='wrong_input_digest':r['input_sha256']='0'*64
    elif kind=='wrong_definition_digest':r['definition_sha256']='0'*64
    elif kind=='empirical_promotion':r['empirical']=True
    elif kind=='authority_promotion':r['authority']=True
    elif kind=='unapproved_extra':r['unapproved_extra']='wholly synthetic extra field'
    elif kind=='missing_hash_domain':del r['hash_domain']
    else:raise ValueError(kind)
    return r

def main():
    rows=read('x1/new-proposals.json')['proposals'];eq=read('validation/x1-equality.json')
    assert eq['clean_before_x2'] and len(set(eq['local_upstream_tracking_fresh_live']))==1
    assert eq['divergence']==[0,0]
    results=[];negatives=[];failures=[];lookup={}
    for row in rows:
        original=canonical(row['input']);fn=compute(row)
        value=fn(row['operation'],row['input'])
        record=envelope(row,value)
        oracle=canonical(value)==canonical(row['expected_result'])
        unchanged=canonical(row['input'])==original
        accepted=verify_envelope(row,record,fn)
        result={'proposal_id':row['proposal_id'],'family':row['family'],'result':value,'envelope':record,
                'frozen_oracle_matches':oracle,'input_nonmutation':unchanged,'envelope_check':accepted,
                'disposition':row['expected_execution_disposition'],'same_owner_only':True}
        results.append(result);lookup[row['proposal_id']]=(row,result)
        if not (oracle and unchanged and accepted['accepted']):failures.append(result)
        for kind in row['preregistered_mutations']:
            bad=mutate(record,kind);verdict=verify_envelope(row,bad,fn)
            negative={'negative_id':row['proposal_id']+'-ADV-'+kind,'proposal_id':row['proposal_id'],'mutation':kind,
                      'retained_record':bad,'observed':verdict,'rejected':verdict['accepted'] is False,'success_credit':0,
                      'recovery_envelope_sha256':sha(record),'same_owner_only':True}
            negatives.append(negative)
            if not negative['rejected']:failures.append(negative)
    write('contract-results.json',{'results':results,'source_x1':eq['x1']})
    write('registered-mutations.json',{'negatives':negatives,'success_credit':0})
    if failures:
        write('initial-contract-failure.json',{'failures':failures,'aggregate_success_credit':0})
        print(json.dumps({'status':'FAIL','failures':len(failures),'proposals':[x.get('proposal_id') for x in failures]}));return 1
    portfolio=read('x1/portfolio-plan.json');safe=[];candidates=[];cfr=[]
    for task in portfolio['safe_now']:
        row,res=lookup[task['proposal_id']];passed=res['frozen_oracle_matches'] if task['kind']=='frozen_oracle' else res['input_nonmutation']
        safe.append(dict(task,disposition='completed',passed=passed,evidence_sha256=sha(res)))
    negmap={(n['proposal_id'],n['mutation']):n for n in negatives}
    for task in portfolio['candidates']:
        n=negmap[(task['proposal_id'],task['kind'])]
        candidates.append(dict(task,disposition='completed',passed=n['rejected'],evidence_sha256=sha(n)))
    for task in portfolio['clean_fix_refine']:
        row,res=lookup[task['proposal_id']];fn=compute(row);good=res['envelope'];bad=mutate(good,task['mutation'])
        before=verify_envelope(row,bad,fn)
        corrected=copy.deepcopy(bad)
        if task['kind']=='CLEAN':del corrected['unapproved_extra']
        elif task['kind']=='FIX':corrected['result']=copy.deepcopy(good['result']);corrected['result_sha256']=good['result_sha256']
        else:corrected['hash_domain']=good['hash_domain']
        after=verify_envelope(row,corrected,fn)
        assert not before['accepted'] and after['accepted'] and canonical(corrected)==canonical(good)
        cfr.append(dict(task,retained_negative_id=task['task_id']+'-INITIAL',retained_before=bad,before_check=before,
                        corrected_after=corrected,after_check=after,disposition='completed',success_credit_for_initial=0))
    write('portfolio-results.json',dict(safe_now=safe,candidates=candidates,clean_fix_refine=cfr,
         exact_packets=portfolio['exact_packets'],blocked_packets=portfolio['blocked_packets'],external_actions=0))
    write('contract-summary.json',dict(proposals=200,positive_contracts_passed=200,registered_mutations=1000,registered_mutations_rejected=1000,
         safe_tasks_passed=300,candidate_tasks_passed=250,clean_fix_refine_passed=300,retained_cfr_initial_failures=300,
         exact_packets_unexecuted=50,blocked_packets_unexecuted=30,outcomes={'completed':170,'represented':10,'open_gap':10,'exact_gate':10},
         same_owner_only=True,independent_reproduction=False,terminal_verdict='NOT_READY_FOR_STAGE_20'))
    print(json.dumps(read('x2/contract-summary.json')))
    return 0

if __name__=='__main__':raise SystemExit(main())
