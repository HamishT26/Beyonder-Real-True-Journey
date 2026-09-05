"""Build and smoke ten owner-local packages; promote only with an explicit flag."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'docs/mira-fenwick/v686-v2'
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_evidence_selectors import canonical,sha
MAP={'selectors':'evidence_selectors','patch':'evidence_patch','lineage':'correction_lineage','receipts':'receipt_binding','obligations':'obligation_projection'}
def read(p):return json.loads((BASE/p).read_text(encoding='utf-8'))
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def smoke(script,row,out):
    out.mkdir(parents=True,exist_ok=False)
    inp=out/'positive-input.json';bad=out/'duplicate-member-input.json'
    write(inp,row['input']);bad.write_text('{"a":1,"a":2}\n',encoding='utf-8',newline='\n')
    a=subprocess.run([sys.executable,'-X','utf8',str(script),'--operation',row['operation'],'--input',str(inp),'--output',str(out/'positive-output.json')],capture_output=True)
    b=subprocess.run([sys.executable,'-X','utf8',str(script),'--operation',row['operation'],'--input',str(bad),'--output',str(out/'adverse-output.json')],capture_output=True)
    expected_code=2 if type(row['expected_result']) is dict and 'error' in row['expected_result'] else 0
    actual=json.loads((out/'positive-output.json').read_text(encoding='utf-8'))
    negative=json.loads((out/'adverse-output.json').read_text(encoding='utf-8'))
    ok=a.returncode==expected_code and canonical(actual['result'])==canonical(row['expected_result']) and b.returncode==2 and negative['result']=={'error':'duplicate_json_member'}
    receipt={'proposal_id':row['proposal_id'],'positive_returncode':a.returncode,'adverse_returncode':b.returncode,'positive_pass':canonical(actual['result'])==canonical(row['expected_result']),
             'adverse_rejected':negative['result']=={'error':'duplicate_json_member'},'pass':ok,'negative_success_credit':0,'same_owner_only':True,
             'runner_sha256':hashlib.sha256(script.read_bytes()).hexdigest()}
    write(out/'smoke-receipt.json',receipt)
    assert ok,'Smoke failed; records retained.'
    return receipt

def build():
    rows=read('x1/new-proposals.json')['proposals'];plan=read('x1/skill-runner-plan.json')
    quick=Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py'
    source_scripts=[ROOT/'scripts'/r['name'] for r in plan['runners']]
    receipts=[]
    for skill in plan['skills']:
        folder=BASE/'skills'/skill['name'];folder.mkdir(parents=True,exist_ok=False)
        chosen=[x for x in rows if x['family'] in skill['families']]
        name=skill['name'];missions=' '.join(skill['triggers'])
        example=chosen[0];runner='ghc_family_'+MAP[example['runner']]+'.py'
        text=f'''---
name: {name}
description: {missions} Use for synthetic evidence records with these exact contracts.
---

# {name.removeprefix('ghc-family-').replace('-',' ').capitalize()}

Read [the frozen contracts](references/contracts.json) to choose the family and operation that matches the requested relation. The two source families are `{skill['families'][0]}` and `{skill['families'][1]}`. Their inputs and expected values are examples, not facts about a person or external system.

Work with an authorized copy of the input. Select the smallest exact operation, retain the original bytes, and compare both value and JSON type with the source-defined oracle. For example, run `python -X utf8 scripts/{runner} --operation {example['operation']} --input example.json --output new-result.json` from this package. Output is exclusive-write; choose a fresh owned filename. A structured error can be the expected answer for a deliberately invalid input.

{missions}

The patch profile reserves root removal and rejects unknown operation members. An omitted permission list and an explicit empty list differ; an explicit null list is refused. Selector matching uses decoded tokens, so textual prefixes and escaped slashes cannot broaden a subtree. Boolean values do not become numbers. Query or projection output does not establish a complete denominator.

Use the accepting case and a duplicate-member JSON adversary before adopting a changed caller. Preserve any failed definition, its content digest, the input, expected result, and a separate correction. Roll back by selecting the previous validated package; preserve this package and its records. Do not overwrite another skill to make a name available.

These checks provide same-owner synthetic software evidence only. They issue no credential, make no real amendment, resolve no empirical gap, and supply no affected-party, professional, legal, cultural, or Māori authority. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct, and retain `NOT_READY_FOR_STAGE_20`.
'''
        (folder/'SKILL.md').write_text(text,encoding='utf-8',newline='\n')
        write(folder/'references/contracts.json',{'source_x1':read('validation/x1-equality.json')['x1'],'criteria':chosen,'inherited_execution_credit':0})
        (folder/'scripts').mkdir()
        for source in source_scripts:shutil.copyfile(source,folder/'scripts'/source.name)
        validation=subprocess.run([sys.executable,'-X','utf8',str(quick),str(folder)],capture_output=True,text=True)
        # Validator output is generic; never persist a traceback or local path.
        assert validation.returncode==0,'Local skill metadata validation failed.'
        receipt=smoke(folder/'scripts'/runner,example,BASE/'tooling/skill-smokes'/name)
        receipts.append({'name':name,'metadata_validation_pass':True,'smoke':receipt,'families':skill['families']})
    runner_receipts=[]
    for key,module in MAP.items():
        row=next(x for x in rows if x['runner']==key)
        runner_receipts.append({'runner':'ghc_family_'+module+'.py','smoke':smoke(ROOT/'scripts'/('ghc_family_'+module+'.py'),row,BASE/'tooling/runner-smokes'/module)})
    write(BASE/'tooling/local-skill-validation.json',{'skills':receipts,'runners':runner_receipts,'unique_new_shared_runners':5,'same_owner_only':True})
    print(json.dumps({'skills_validated':len(receipts),'unique_shared_runners_smoked':len(runner_receipts)}))

def promote():
    validation=read('tooling/local-skill-validation.json');assert len(validation['skills'])==10
    destroot=Path.home()/'.codex/skills';entries=[]
    for item in validation['skills']:
        assert item['metadata_validation_pass'] and item['smoke']['pass']
        source=BASE/'skills'/item['name'];dest=destroot/item['name']
        assert not dest.exists(),'Global collision; no overwrite allowed.'
        shutil.copytree(source,dest)
        for path in sorted(source.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:continue
            rel=path.relative_to(source);a=path.read_bytes();b=(dest/rel).read_bytes();assert a==b
            entries.append({'skill':item['name'],'path':rel.as_posix(),'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()})
    write(BASE/'tooling/global-promotion.json',{'skills':10,'unique_new_shared_runners':5,'entries':entries,'byte_parity':True,'collision_overwrites':0,'rollback':'Select retained prior tooling; preserve these new packages and receipts.','same_owner_only':True})
    print(json.dumps({'promoted_skills':10,'global_files_verified':len(entries),'byte_parity':True}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--promote',action='store_true');args=p.parse_args()
    promote() if args.promote else build()
