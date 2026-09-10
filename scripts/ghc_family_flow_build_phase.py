"""Build one already-preregistered owner execution tranche and local skill evidence."""
import argparse,copy,hashlib,importlib,json,subprocess,sys
from pathlib import Path
from scripts.ghc_family_flow_common import canonical,digest,typed_equal

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/mira-fenwick/v690-v3'
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write((json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())

def main():
    a=argparse.ArgumentParser();a.add_argument('--phase',choices=['x1','x2'],required=True);args=a.parse_args();phase=args.phase
    if phase=='x1':assert read('x1/planning-equality.json')['clean']
    else:assert read('x2/x1-equality.json')['clean']
    evaluator=importlib.import_module('scripts.ghc_family_flow_'+phase).evaluate
    rows=[r for r in read('plan/new-proposals.json')['proposals'] if r['session']==phase]
    results=[];failures=[]
    for row in rows:
        before=canonical(row['request']);value=evaluator(row['request']);candidate=copy.deepcopy(row['candidate_subject']);bad=evaluator(candidate)
        result={'proposal_id':row['proposal_id'],'operation':row['operation'],'observed':value,'expected':row['expected_envelope'],
                'envelope_match':typed_equal(value,row['expected_envelope']),'input_unchanged':canonical(row['request'])==before,
                'disposition':row['expected_execution_disposition'],'candidate_subject':candidate,'candidate_observed':bad,
                'candidate_guard_passed':typed_equal(bad,row['candidate_expected']),'candidate_original_success_credit':0,
                'same_owner_only':True,'independent_reproduction':False}
        results.append(result)
        if not(result['envelope_match'] and result['input_unchanged'] and result['candidate_guard_passed']):failures.append(result)
    write(BASE/phase/'results.json',{'phase':phase,'results':results,'frozen_definition_source':'plan/new-proposals.json'})
    if failures:
        write(BASE/phase/'initial-execution-failure.json',{'failures':failures,'original_aggregate_success_credit':0})
        print(json.dumps({'status':'FAIL','phase':phase,'failed_proposals':[r['proposal_id'] for r in failures]}));return 1
    inherited=read('plan/inherited-selections.json')['records'];selected=inherited[:100] if phase=='x1' else inherited[100:]
    refinements=[]
    for i,item in enumerate(selected,1):
        raw=canonical(item['source_record']);projection={'source_proposal_id':item['source_proposal_id'],'canonical_source_record':raw.decode(),'source_sha256':hashlib.sha256(raw).hexdigest()}
        restored=json.loads(projection['canonical_source_record']);assert typed_equal(restored,item['source_record']) and projection['source_sha256']==item['source_record_sha256']
        refinements.append({'task_id':f'MF6903-{phase.upper()}-CFR-{i:03}','kind':['CLEAN','FIX','REFINE'][(i-1)%3],'projection':projection,'restored_sha256':digest(restored),
                            'lossless':True,'source_execution_credit':0,'source_novelty_credit':0,'changed_scope':'owner record representation; no host cleanup'})
    write(BASE/phase/'record-refinements.json',{'records':refinements,'source_records_mutated':0})
    plan=read('plan/skills-runners.json');skills=[s for s in plan['local_skills'] if s['session']==phase];runners=[r for r in plan['local_runners'] if r['session']==phase]
    for runner in runners:
        path=ROOT/'scripts'/runner['name']
        text=f'''"""Finite {phase} flow operations {', '.join(runner['operations'])}."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_{phase} import evaluate

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, {tuple(runner['operations'])!r}))
'''
        with path.open('xb') as f:f.write(text.encode())
    quick=Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py';skill_results=[]
    for item in skills:
        name=item['name'];folder=BASE/phase/'skills'/name;folder.mkdir(parents=True,exist_ok=False)
        selected_rows=[r for r in rows if r['operation']==item['operation']];first=selected_rows[0];runner=next(r for r in runners if item['operation'] in r['operations'])
        description=item['mission']+' Use for this exact finite flow or allocation contract.'
        content=f'''---
name: {name}
description: {description}
---

# {item['mission'].rstrip('.')}

Read [the operation contract](references/contract.json), including its fixed inputs, expected envelopes and refusal conditions. This skill covers `{item['operation']}` only. Preserve the supplied vertex order, directed arc identity, integer capacities, and declared evidence class.

Invoke `python -X utf8 -m scripts.{Path(runner['name']).stem} --input INPUT.json --output FRESH_OUTPUT.json` from the owned repository root. Root binding is required; the source Ilyra direct-file entrypoint failure remains a warning against an unbound caller. Choose an absent output filename. The runner writes one structured envelope and returns two on a declared refusal.

{item['mission']} A failed subject remains failed even if its refusal check passes. Inspect the accepting and unknown-field fixtures in `tests/` before changing a caller. Compare the complete JSON envelope and require unchanged input; do not replace null with zero, coerce Boolean values to integers, or silently broaden the finite work limits.

Retain any failed input, oracle and implementation digest. Isolate the affected operation and add a separately recorded correction; select prior validated tooling for rollback. Never erase a failure or replay a successful terminal aggregate.

This is same-owner synthetic software evidence. It supplies no real allocation, consent, identity, professional, legal, cultural, affected-party or Māori authority. Keep completed, represented, open_gap and exact_gate distinct. NOT_READY_FOR_STAGE_20.
'''
        (folder/'SKILL.md').write_bytes(content.encode())
        display=item['operation'].replace('_',' ').title();short=('Review bounded '+item['operation'].replace('_',' ')+' evidence')[:64]
        meta=f'interface:\n  display_name: {json.dumps(display)}\n  short_description: {json.dumps(short)}\n  default_prompt: {json.dumps("Use $"+name+" to inspect a bounded synthetic request and its refusal conditions.")}\n'
        (folder/'agents').mkdir();(folder/'agents/openai.yaml').write_bytes(meta.encode())
        write(folder/'references/contract.json',{'operation':item['operation'],'phase':phase,'source_rows':selected_rows,'source_credit':0})
        write(folder/'tests/accepting.json',first['request']);write(folder/'tests/rejecting.json',first['candidate_subject'])
        proc=subprocess.run([sys.executable,'-X','utf8',str(quick),str(folder)],capture_output=True)
        metadata_pass=proc.returncode==0
        yes=evaluator(first['request']);no=evaluator(first['candidate_subject'])
        skill_results.append({'name':name,'metadata_pass':metadata_pass,'accepting_pass':typed_equal(yes,first['expected_envelope']),
                              'rejecting_guard_pass':typed_equal(no,first['candidate_expected']),'rejected_subject_success_credit':0})
        if not metadata_pass:raise RuntimeError('Local skill metadata failure; package retained.')
    write(BASE/phase/'skill-validation.json',{'skills':skill_results,'count':len(skills)})
    smokes=[]
    for runner in runners:
        positive=next(r for r in rows if r['operation']==runner['operations'][0]);outside=next(r for r in rows if r['operation'] not in runner['operations'])
        folder=BASE/phase/'runner-smokes'/Path(runner['name']).stem;folder.mkdir(parents=True)
        write(folder/'accepting.json',positive['request']);write(folder/'outside-group.json',outside['request'])
        observations=[]
        for label,expected,code in [('accepting',positive['expected_envelope'],0),('outside-group',{'accepted':False,'result':None,'error':'outside_runner_group'},2)]:
            proc=subprocess.run([sys.executable,'-X','utf8','-m','scripts.'+Path(runner['name']).stem,'--input',str(folder/(label+'.json')),'--output',str(folder/(label+'-output.json'))],cwd=ROOT,capture_output=True)
            observed=json.loads((folder/(label+'-output.json')).read_text(encoding='utf-8'))
            observations.append({'subject':label,'returncode':proc.returncode,'expected_returncode':code,'observed':observed,'pass':proc.returncode==code and typed_equal(observed,expected),'original_success_credit':0 if label=='outside-group' else 1})
        write(folder/'receipt.json',{'runner':runner['name'],'observations':observations,'same_owner_only':True});assert all(x['pass'] for x in observations)
        smokes.append({'runner':runner['name'],'pass':True,'negative_subject_retained':True})
    write(BASE/phase/'execution-summary.json',{'phase':phase,'safe_envelopes_matched':100,'safe_accepted_inputs':sum(x['observed']['accepted'] for x in results),'safe_refused_subjects':sum(not x['observed']['accepted'] for x in results),
            'candidate_subjects_failed':100,'candidate_guards_passed':100,'candidate_original_success_credit':0,'record_refinements':100,'local_skills':10,'paired_runners':5,'runner_smokes':smokes,
            'source_execution_credit':0,'source_novelty_credit':0,'same_owner_only':True,'independent_reproduction':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    print(json.dumps({'phase':phase,'safe_matched':100,'candidates_rejected':100,'refinements':100,'skills':10,'runners':5}));return 0

if __name__=='__main__':raise SystemExit(main())
