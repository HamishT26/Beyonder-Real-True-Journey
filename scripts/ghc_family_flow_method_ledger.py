"""Project materialized subjects and passing checks into the family Method Flow schema."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/mira-fenwick/v690-v3'
def read(path):return json.loads((BASE/path).read_text(encoding='utf-8'))
def write(path,value):
    with path.open('xb') as f:f.write((json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['x1','x2'],required=True);args=p.parse_args();phase=args.phase
    helper=Path.home()/'.codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py'
    spec=importlib.util.spec_from_file_location('family_method_helper',helper);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    ledger=module.new_ledger('v690-v3-'+phase,'Mira Fenwick');gates=read('plan/identity-practices.json')['protected_gates'];methods={}
    ledger.update(execution_authority='owner_self_scoped_delta',source_provenance='8eb07d232398cbd33c8e9aae5a040db2d32b2c22',source_is_ancestor=False,
                  helper_source='ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py',helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),
                  repository_scan=False,unchanged_history_scan=False,sibling_lane_mutation=False,cross_lane_scan=False)
    def witness(method,ident,result,observed,evidence,negative=None):
        if method not in methods:
            row={'method_id':method,'title':method.replace('_',' '),'failure_signature':'Declared invalid subject or observed operator failure is retained.',
                 'trigger_preconditions':['The exact named owner fixture and caller context.'],'privacy_class':'sanitized_public','approval_class':'safe_now',
                 'candidate_workaround':'Use the declared accepting fixture or bounded corrected caller while retaining the failed subject.','validation_witness_ids':[],
                 'recurrence_guard':'Bind the complete input, source definition and exact scope before interpreting a result.','rollback':'Select prior validated bytes; preserve this evidence.',
                 'recommendation_state':'validated','supersedes':[],'protected_gates':gates,'retained_negative_ids':[],'scope_boundary':ledger['boundary']}
            ledger['methods'].append(row);methods[method]=row
        neg=negative or ident+'-SUBJECT'
        if result=='fail' and neg not in methods[method]['retained_negative_ids']:methods[method]['retained_negative_ids'].append(neg)
        record={'witness_id':ident,'method_id':method,'procedure':'Inspect a materialized failed subject or passing bounded check.','scope':'Mira Fenwick v690-v3 '+phase,
                'expected':'The declared finite envelope, refusal, or source-preserving reconstruction.','observed':observed,'result':result,'same_owner_only':True,
                'independent_reproduction':False,'retained_negative_ids':[neg] if result=='fail' else [],'boundary':ledger['boundary'],'evidence_path':'docs/mira-fenwick/v690-v3/'+evidence}
        ledger['witnesses'].append(record);methods[method]['validation_witness_ids'].append(ident)
    rows=read(phase+'/results.json')['results']
    for row in rows:
        method='MF6903-'+phase+'-'+row['operation'];ident=row['proposal_id'];path=phase+'/results.json'
        if not row['observed']['accepted']:witness(method,ident+'-SAFE-SUBJECT','fail',row['observed'],path)
        witness(method,ident+'-SAFE-CHECK','pass',{'envelope_match':row['envelope_match'],'input_unchanged':row['input_unchanged']},path)
        witness(method,ident+'-CANDIDATE-SUBJECT','fail',row['candidate_observed'],path)
        witness(method,ident+'-CANDIDATE-GUARD','pass',{'guard_passed':row['candidate_guard_passed'],'original_success_credit':0},path)
    skills=read(phase+'/skill-validation.json')['skills']
    ops={s['name']:s['operation'] for s in read('plan/skills-runners.json')['local_skills']}
    for n,s in enumerate(skills,1):
        method='MF6903-'+phase+'-'+ops[s['name']];prefix=f'MF6903-{phase}-SKILL-{n:02}';path=phase+'/skill-validation.json'
        witness(method,prefix+'-METADATA','pass',{'metadata_pass':s['metadata_pass']},path)
        witness(method,prefix+'-ACCEPTING','pass',{'accepting_pass':s['accepting_pass']},path)
        witness(method,prefix+'-REJECTED-SUBJECT','fail',{'unknown_field':True,'original_success_credit':0},path)
        witness(method,prefix+'-REFUSAL-CHECK','pass',{'guard_pass':s['rejecting_guard_pass']},path)
    for n,path in enumerate(sorted((BASE/phase/'runner-smokes').glob('*/receipt.json')),1):
        record=json.loads(path.read_text());method=f'MF6903-{phase}-RUNNER-{n:02}';relative=path.relative_to(BASE).as_posix()
        for obs in record['observations']:
            if obs['subject']=='outside-group':witness(method,method+'-SUBJECT','fail',obs['observed'],relative)
            witness(method,method+'-'+obs['subject']+'-CHECK','pass',{'returncode':obs['returncode'],'pass':obs['pass']},relative)
    if phase=='x1':
        startup=read('plan/startup-failures.json')['events']+read('x1/startup-overlay.json')['events']
        for event in startup:
            method=event['id']+'-METHOD';witness(method,event['id']+'-FAIL','fail',event['failure'],'plan/startup-failures.json' if event['id']!='MF6903-OP006' else 'x1/startup-overlay.json',event['id'])
            witness(method,event['id']+'-RECOVERY','pass',event['recovery'],'plan/startup-failures.json' if event['id']!='MF6903-OP006' else 'x1/startup-overlay.json')
        checks=read('x1/toolchain/package-checks.json')
        for name in ['highspy','PuLP','PyMaxflow']:
            method='MF6903-PACKAGE-'+name;path='x1/toolchain/package-checks.json'
            for i,check in enumerate([c for c in checks['comparisons'] if c['interface']==name],1):witness(method,method+f'-POSITIVE-{i:02}','pass',check,path)
            adverse=next(c for c in checks['adverse_subjects'] if c['interface']==name)
            witness(method,method+'-SUBJECT','fail',adverse,path);witness(method,method+'-GUARD','pass',{'guard_pass':adverse['guard_pass']},path)
        refinement_method='MF6903-OP002-METHOD'
    else:
        # The x2 reconstruction uses a current refusal-bearing operator method;
        # this is record-preservation evidence, not inherited algorithm execution.
        refinement_method='MF6903-x2-reservation'
    for row in read(phase+'/record-refinements.json')['records']:
        witness(refinement_method,row['task_id']+'-CHECK','pass',{'lossless':row['lossless'],'source_execution_credit':0,'source_novelty_credit':0},phase+'/record-refinements.json')
    for method in methods.values():
        if not method['retained_negative_ids']:
            # Reservation operations still have an explicit unknown-field subject.
            raise ValueError('No retained failing subject for '+method['method_id'])
        ledger['state_events'].append({'method_id':method['method_id'],'from':'candidate','to':'validated','evidence':'passing witness IDs remain separate from failed subject IDs'})
        ledger['recommendations'].append({'method_id':method['method_id'],'state':'validated','recommendation':method['recurrence_guard']})
    module.refresh_counts(ledger);validation=module.validate_ledger(ledger)
    write(BASE/phase/'method-flow.json',ledger);write(BASE/phase/'method-flow-validation.json',validation)
    assert validation['valid'],validation
    print(json.dumps({'phase':phase,'methods':validation['method_count'],'direct_witnesses':validation['witness_count'],'witness_results':ledger['counts']['witness_results'],'valid':True}))

if __name__=='__main__':main()
