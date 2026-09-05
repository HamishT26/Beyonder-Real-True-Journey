"""Execute frozen protocol report contracts and build bounded owner evidence."""
from __future__ import annotations
import argparse,copy,hashlib,importlib,json,subprocess
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v685-v8';X1='ae33e7fd357e38c464677c10538a50f069b68353';SOURCE='f5464f56d095e9c691707f669668b86ff70468a6'
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
def read(p):return json.loads((BASE/p).read_text(encoding='utf8'))
def write(p,v):
    dest=BASE/p;dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf8',newline='\n') as f:f.write(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def evaluate(proposal,fixture):
    errors=[]
    expected_keys={'definition_sha256','source_x1','phase_epoch','empirical','authority','reported','input'}
    if set(fixture)!=expected_keys:errors.append('fixture_fields')
    if fixture.get('definition_sha256')!=sha(proposal):errors.append('definition_digest')
    if fixture.get('source_x1')!=X1:errors.append('source_x1')
    if type(fixture.get('phase_epoch')) is not int or fixture['phase_epoch']!=2:errors.append('epoch')
    if fixture.get('empirical') is not False:errors.append('empirical_promotion')
    if fixture.get('authority') is not False:errors.append('authority_promotion')
    if canonical(fixture.get('input'))!=canonical(proposal['input']):errors.append('input_drift')
    before=canonical(fixture.get('input'))
    module=importlib.import_module('ghc_family_protocol_'+proposal['runner'])
    computed=module.evaluate(proposal['operation'],fixture.get('input'))
    if canonical(computed)!=canonical(fixture.get('reported')):errors.append('fabricated_report')
    if canonical(fixture.get('input'))!=before:errors.append('input_mutated')
    return {'accepted':not errors,'computed':computed,'errors':errors}
def fixture(p):return {'definition_sha256':sha(p),'source_x1':X1,'phase_epoch':2,'empirical':False,'authority':False,'reported':copy.deepcopy(p['expected_result']),'input':copy.deepcopy(p['input'])}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--equality',required=True);a=ap.parse_args();eq=json.loads(Path(a.equality).read_text())
    assert eq['head']==X1 and eq['four_way_equal'] and eq['clean']
    assert subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD']).decode().strip()==X1
    write('x2/x1-equality.json',eq)
    props=read('x1/new-proposals.json')['proposals'];records=[];negative=[]
    for p in props:
        f=fixture(p);v=evaluate(p,f)
        records.append({'proposal_id':p['proposal_id'],'definition_sha256':sha(p),'fixture':f,'result':v,'outcome':p['expected_execution_disposition'] if v['accepted'] else 'open_gap','same_owner_only':True})
        for mi,kind in enumerate(p['preregistered_mutations'],1):
            bad=copy.deepcopy(f)
            if kind=='fabricated_report':bad['reported']={'fabricated_report':p['proposal_id']}
            elif kind=='stale_definition_digest':bad['definition_sha256']='0'*64
            elif kind=='phase_epoch_inversion':bad['phase_epoch']=1
            elif kind=='empirical_promotion':bad['empirical']=True
            elif kind=='authority_promotion':bad['authority']=True
            result=evaluate(p,bad)
            negative.append({'negative_id':p['proposal_id']+f'-M{mi:02d}','proposal_id':p['proposal_id'],'mutation':kind,'fixture':bad,'result':result,'failed_witness_retained':True,'completion_credit':0})
    summary={'positive_count':len(records),'positive_accepted':sum(r['result']['accepted'] for r in records),'invalid_count':len(negative),'invalid_rejected':sum(not r['result']['accepted'] for r in negative),'outcomes':dict(Counter(r['outcome'] for r in records)),'same_owner_only':True,'independent_reproduction':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'}
    write('x2/contract-results.json',{'records':records});write('x2/invalid-mutations.json',{'records':negative});write('x2/contract-summary.json',summary)
    print(json.dumps(summary))
    if summary['positive_accepted']!=200 or summary['invalid_rejected']!=1000:raise SystemExit(1)
    write('x2/portfolio-results.json',portfolio(props,records))

def portfolio(props,records):
    plans=read('x1/portfolio-plan.json');lookup={p['proposal_id']:p for p in props};by_result={r['proposal_id']:r for r in records};out={}
    for key in ['safe_now','candidates','clean_fix_refine','exact_packets','blocked_packets']:
        rows=[]
        for r in plans[key]:
            p=lookup[r['proposal_id']];action=r['action'];unit={'packet_id':r['packet_id'],'proposal_id':p['proposal_id'],'action':action,'same_owner_only':True}
            if key in ['exact_packets','blocked_packets']:
                unit.update(outcome='exact_gate' if key=='exact_packets' else 'open_gap',operation_executed=False,required_evidence=r['required_evidence']);rows.append(unit);continue
            f=fixture(p);before=canonical(f)
            if action=='evaluate_report':ok=by_result[p['proposal_id']]['result']['accepted'];artifact={'linked_result':p['proposal_id']}
            elif action in ['verify_roundtrip_and_input_nonmutation','review_sorted_serialization']:
                transformed=json.loads(json.dumps(f,sort_keys=True,ensure_ascii=False));ok=evaluate(p,transformed)['accepted'] and canonical(f)==before;artifact={'roundtrip_sha256':sha(transformed),'input_unchanged':canonical(f)==before}
            elif action=='review_missing_definition_refusal':
                bad=copy.deepcopy(f);del bad['definition_sha256'];result=evaluate(p,bad);ok=not result['accepted'];artifact=result
            elif action=='allowlist_projection':
                source={**f,'synthetic_working_note':'draft annotation excluded by the public view'};public={k:source[k] for k in f};ok=canonical(public)==before and 'synthetic_working_note' in source;artifact={'source_sha256':sha(source),'public_sha256':sha(public),'source_retained':True,'removed_field':'synthetic_working_note'}
            elif action=='retain_and_correct_false_report':
                bad=copy.deepcopy(f);bad['reported']={'incorrect_report':True};failed=evaluate(p,bad);corrected=copy.deepcopy(bad);corrected['reported']=copy.deepcopy(p['expected_result']);recovered=evaluate(p,corrected);ok=not failed['accepted'] and recovered['accepted'];artifact={'retained_false_report':bad,'failed_result':failed,'corrected_report':corrected,'recovery_result':recovered,'predecessor_sha256':sha(bad),'deletion_count':0}
            elif action=='derive_readable_protocol_explanation':
                text=p['title']+'. Input: '+canonical(p['input'])+'. Expected bounded report: '+canonical(p['expected_result'])+'. A locally consistent report cannot establish real observations or authority.';ok=bool(text) and p['title'] in text;artifact={'text':text,'definition_sha256':sha(p)}
            else:raise ValueError(action)
            # The task is a bounded transformation; its linked research disposition
            # remains separate. A formatting success never promotes that claim.
            unit.update(outcome='completed' if ok else 'open_gap',operation_executed=True,passed=ok,linked_claim_outcome=p['expected_execution_disposition'],artifact=artifact)
            rows.append(unit)
        out[key]=rows
    out['counts']={k:len(v) for k,v in out.items()};out['unit_boundary']='Portfolio transformations are distinct task units, not extra new proposals, empirical trials, or novelty credit.'
    return out
if __name__=='__main__':main()
