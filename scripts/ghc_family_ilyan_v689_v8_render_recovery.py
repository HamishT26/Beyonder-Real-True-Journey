"""Add the retained renderer fault without replaying document or phase work."""
import argparse,importlib.util,json
from pathlib import Path
import ghc_family_ilyan_v689_v8_io as io

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--method-runner',required=True);a=ap.parse_args()
    assert (io.BASE/'final/conditional-membership-model.png').is_file()
    failure={'id':'IR6898-FINAL-OP002','failure':'The bundled document runtime lacked matplotlib; the initial document builder stopped after writing the complete baton and before creating any figure or PDF.','original_success_credit':0,'prior_builder_sha256':'57c1c3e2b54175e38733314b9b8830ab03069c0c3b5df042b04184b77cd6119e','recovery':'Confirmed installed module availability in both runtimes. The already installed system plotting runtime created the deterministic figure; the confirmed bundled document runtime is selected for PDF rendering. No package installation or phase replay.','recovered_plot':True,'new_dependencies_installed':0,'baton_work_replayed':False,'prior_baton_reconstructable':True}
    io.write('final/render-runtime-correction.json',failure)
    spec=importlib.util.spec_from_file_location('method_flow',a.method_runner);mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
    ledger=io.read('final/method-flow.json');m=next(x for x in ledger['methods'] if x['method_id']=='IR6898-supplemental-operations');m['retained_negative_ids'].append(failure['id'])
    for result,procedure,expected,observed in [('fail','Initial plotting dependency','Matplotlib available in chosen runtime',False),('pass','Narrow plotting continuation','Figure from verified installed plotting runtime',True)]:
        wid=m['method_id']+'-RENDER-'+str(len(m['validation_witness_ids'])+1);m['validation_witness_ids'].append(wid);ledger['witnesses'].append({'witness_id':wid,'method_id':m['method_id'],'procedure':procedure,'scope':'Ilyan v689-v8 document runtime','expected':expected,'observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,'retained_negative_ids':[failure['id']],'boundary':io.read('plan/identity-practices.json')['protected_gates'],'evidence_ref':'docs/ilyan-reed/v689-v8/final/render-runtime-correction.json'})
    mf.refresh_counts(ledger);valid=mf.validate_ledger(ledger);assert valid['valid'];assert ledger['counts']['witnesses']==904
    io.write('final/effective-method-flow.json',ledger);io.write('final/effective-method-flow-validation.json',valid)
    summary=io.read('final/completion-ledger.json');summary.update(method_flow_current=ledger['counts'],current_effective_negatives=214,additive_effective_negatives=738,additive_direct_witnesses=1573,additive_direct_failed=449,additive_direct_passed=1124,prior_terminal_preparation_retained=True,effective_method_flow='docs/ilyan-reed/v689-v8/final/effective-method-flow.json')
    io.write('final/effective-completion-ledger.json',summary);io.write('final/effective-negative-index.json',{'current_owner_negative_ids':sorted({n for m in ledger['methods'] for n in m['retained_negative_ids']}),'current_owner_count':214,'latest_source_baseline':524,'additive_effective_negatives':738,'original_success_credit':0})
    addition='''### Additive terminal renderer recovery

After the preceding terminal-preparation snapshot, the document runtime returned a missing-matplotlib failure. The complete 74,209-word baton already existed; no phase evaluation or baton generation was replayed. The failed builder bytes, earlier baton manifest and earlier module thirteen remain in the final retained directory. A module-availability probe found plotting support in the already installed system runtime and document support in the bundled runtime. The figure was created in the former, and PDF rendering is a separate continuation in the latter. No additional package was installed.

The effective terminal records are now `final/effective-method-flow.json`, `final/effective-negative-index.json` and `final/effective-completion-ledger.json`. They add one failed dependency witness and one bounded plotting recovery to the preceding records, without changing either sealed tranche. Effective current-owner totals are 214 negatives, 27 methods and 904 direct witnesses, comprising 214 failed and 690 passing. Added to the latest source overlay, these become 738 effective negatives, 49 methods and 1,573 direct witnesses, comprising 449 failed and 1,124 passing. Earlier numbers in the preparation narrative describe the retained pre-render snapshot; this additive record controls the final current totals.

The exact final canonical will bind the complete updated baton and its document receipts. None of these local rendering operations supplies independent reproduction, empirical GMUT support or delivery credit. The route remains PREPARED_NOT_SENT until the separately gated native activation.

'''
    path=io.BASE/'final/baton/13-terminal-gates-and-recovery.md';s=path.read_text(encoding='utf8');assert s.endswith('END MODULE 13.\n');path.write_text(s[:-len('END MODULE 13.\n')]+addition+'END MODULE 13.\n',encoding='utf8',newline='\n')
    prior=io.read('final/baton-manifest.json');records=[];complete='# Ilyan Reed v689-v8 complete handoff to Lyren Moss v690-v1\n\n'
    for row in prior['modules']:
        p=io.ROOT/row['path'];body=p.read_text(encoding='utf8');complete+=body+'\n';records.append({**row,'words':len(body.split()),'sha256':io.sha(p.read_bytes())})
    complete+='EOF ILYAN REED v689-v8 BATON.\n';(io.BASE/'final/hand-off-baton.md').write_text(complete,encoding='utf8',newline='\n');updated={**prior,'modules':records,'combined_words':len(complete.split()),'combined_sha256':io.sha(complete.encode()),'prior_manifest':'docs/ilyan-reed/v689-v8/final/retained/baton-manifest-before-render-recovery.json'}
    (io.BASE/'final/baton-manifest.json').write_text(json.dumps(updated,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8',newline='\n');assert 10000<=updated['combined_words']<=100000
    print(json.dumps({'baton_words':updated['combined_words'],'effective_negatives':738,'effective_direct_witnesses':1573,'current_direct_witnesses':904}))

if __name__=='__main__':main()
