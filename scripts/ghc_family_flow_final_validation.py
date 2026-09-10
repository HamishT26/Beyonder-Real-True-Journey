"""Compose retained X2 checks with the final additive receipt correction."""
import hashlib,json
from pathlib import Path
from scripts import ghc_family_flow_canonical as base
from scripts.ghc_family_flow_closeout import BASE,ROOT,read,helper
base_checks=base.checks
def checks(preflight=False):
    rows=base_checks(preflight)
    def check(name,fn):
        try:
            evidence=fn();assert evidence is not False;rows.append({'name':name,'pass':True,'evidence':evidence})
        except Exception as exc:rows.append({'name':name,'pass':False,'error_type':type(exc).__name__,'error':str(exc)[:600]})
    def correction():
        ledger=read('final/method-flow-post-x2.json');v=helper().validate_ledger(ledger)
        assert v['valid'] and v['method_count']==1 and v['witness_count']==2
        assert ledger['counts']['witness_results']=={'fail':1,'pass':1}
        assert {w['witness_id'] for w in ledger['witnesses']}=={'MF6903-OP010-FAIL','MF6903-OP010-RECOVERY'}
        return {'added_methods':1,'added_failed':1,'added_passing':1,'original_failed_attempt_credit':0}
    def bindings():
        r=read('final/post-x2-correction/receipt-bindings.json');assert len(r['receipts'])==2
        for row in r['receipts']:assert hashlib.sha256((ROOT.parents[1]/row['archive_relative']).read_bytes()).hexdigest()==row['sha256']
        f=read('final/post-x2-correction/failure.json');assert f['commit_attempts_during_failed_command']==0 and f['original_success_credit']==0
        return {'receipt_bindings':2,'failed_attempt_commits':0}
    def accounting():
        a=read('final/accounting.json');b=read('x2/accounting-r2.json')
        assert a['x2_sealed_own']==b['own'] and a['x2_sealed_cumulative']==b['cumulative']
        for k,n in {'methods':1,'direct_witnesses':2,'failed_witnesses':1,'passing_witnesses':1,'effective_negatives':1}.items():
            assert a['own'][k]==b['own'][k]+n and a['cumulative'][k]==b['cumulative'][k]+n
        assert a['operational_failures']==10 and read('final/phase-truth.json')['own']==a['own']
        assert len(set(a['own_failed_witness_ids']))==328 and a['own']['direct_witnesses']==1166 and a['own']['methods']==49
        return {'own':a['own'],'cumulative':a['cumulative'],'prior_x2_accounting_preserved':True}
    check('final_receipt_correction_method_flow',correction)
    check('final_receipt_correction_byte_bindings',bindings)
    check('final_additive_current_accounting',accounting)
    return rows
if __name__=='__main__':
    base.checks=checks
    raise SystemExit(base.main())
