"""Exclusive, byte-preserving promotion of ten validated skills and five runners."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/thalen-reed/v687-v8')
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_thalen_reed_v687_v8_x1_audit import privacy

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skill-root',type=Path,required=True);ap.add_argument('--runner-root',type=Path,required=True);ap.add_argument('--bank',type=Path,required=True);a=ap.parse_args()
    plan=json.loads((ROOT/BASE/'x1/skill-runner-plan.json').read_text());members=[]
    assert not a.runner_root.exists(),'Runner bank collision'
    for item in plan['skills']:
        source=ROOT/BASE/'skills'/item['name'];dest=a.skill_root/item['name'];assert not dest.exists(),item['name']
        manifest=json.loads((source/'manifest.json').read_text());expected={r['relative'] for r in manifest['members']}|{'manifest.json'}
        actual={p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()};assert expected==actual
        for row in manifest['members']:assert hashlib.sha256((source/row['relative']).read_bytes()).hexdigest()==row['sha256']
        for rel in sorted(actual):members.append({'kind':'skill','name':item['name'],'relative':rel,'source':(BASE/'skills'/item['name']/rel).as_posix()})
    for name in [r['name'] for r in plan['runners']]+[plan['core']]:members.append({'kind':'runner','name':name,'relative':name,'source':'scripts/'+name})
    assert len(members)==56
    data={m['source']:(ROOT/m['source']).read_bytes() for m in members};scan=privacy(data);assert scan['confirmed_hits']==0,scan
    out=ROOT/BASE/'x2';(out/'prepromotion-privacy.json').write_text(json.dumps(scan,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
    for item in plan['skills']:(a.skill_root/item['name']).mkdir()
    a.runner_root.mkdir(parents=True)
    for row in members:
        dest=(a.skill_root/row['name']/row['relative']) if row['kind']=='skill' else (a.runner_root/row['relative'])
        bank=(a.skill_root/row['name']).resolve() if row['kind']=='skill' else a.runner_root.resolve()
        assert dest.resolve().is_relative_to(bank)
        dest.parent.mkdir(parents=True,exist_ok=True)
        raw=data[row['source']]
        with dest.open('xb') as handle:handle.write(raw)
        assert dest.read_bytes()==raw
        row.update({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1');validations=[]
    for item in plan['skills']:
        result=subprocess.run([sys.executable,'-X','utf8',str(a.skill_root/'.system/skill-creator/scripts/quick_validate.py'),str(a.skill_root/item['name'])],capture_output=True,text=True,encoding='utf-8',env=env)
        assert result.returncode==0,item['name'];validations.append({'name':item['name'],'global_quick_validate_pass':True})
    cases=json.loads((ROOT/BASE/'x1/new-proposals.json').read_text())['proposals'];global_smokes=[]
    for item in plan['runners']:
        for op in item['operations']:
            fixture=a.bank/'smoke-inputs'/(op+'.json')
            c=next(c for c in cases if c['operation']==op and c['expected_output']['accepted'])
            result=subprocess.run([sys.executable,'-X','utf8',str(a.runner_root/item['name']),str(fixture)],capture_output=True,text=True,encoding='utf-8',env=env)
            assert result.returncode==0 and json.loads(result.stdout)==c['expected_output'],(item['name'],op)
            global_smokes.append({'runner':item['name'],'operation':op,'fixture':c['proposal_id'],'pass':True,'duplicate_witness_credit':0})
    for row in members:
        dest=(a.skill_root/row['name']/row['relative']) if row['kind']=='skill' else a.runner_root/row['relative']
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==row['sha256']
    receipt={'schema':'ghc.family.exclusive-promotion.v1','skill_count':10,'runner_count':5,'shared_dependencies':1,'file_count':56,'members':members,'global_skill_validation':validations,'global_runner_operation_smokes':global_smokes,'overwrites':0,'source_global_byte_equal':True,'caches_copied':0,'source_compatibility_preserved':True,'runner_bank_label':'thalen-reed-v687-v8 global tools','rollback':'Stop selecting these additive packages; retain all source, receipts, and older callers. No deletion is performed.'}
    target=out/'promotion-receipt.json'
    with target.open('x',encoding='utf-8',newline='\n') as h:h.write(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'promoted_skills':10,'promoted_runners':5,'parity_files':56,'global_runner_operation_smokes':10,'overwrites':0}))

if __name__=='__main__':main()
