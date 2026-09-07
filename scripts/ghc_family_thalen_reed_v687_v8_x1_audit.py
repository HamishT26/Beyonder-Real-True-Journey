"""Read and bind the planning-only owner scope; never execute PCM contracts."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

BASE='docs/thalen-reed/v687-v8/'
SOURCE='7e72086683731c40b4884ee7254c864891e354a9'
PATTERNS={
    'raw_identifier':re.compile(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',re.I),
    'private_absolute_path':re.compile(r'[A-Z]:[/\\](?:Users|GHC-Archives)[/\\]',re.I),
    'private_callable_key':re.compile(r'(?:thread|task|agent|session)_id[\"\x27]?\s*[:=]',re.I),
    'credential_assignment':re.compile(r'(?:api[_-]?key|password|secret|token)[\"\x27]?\s*[:=]\s*[\"\x27]?[A-Za-z0-9_/-]{12,}',re.I),
    'private_stream':re.compile(r'(?:private_transcript|session_stream|screenshot_payload)',re.I),
}

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    def constant(_):raise ValueError('NONFINITE_JSON_CONSTANT')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def normalized(path):return path.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')

def allowed(path):
    return path.startswith(BASE) or path.startswith('scripts/build_ghc_family_thalen_reed_v687_v8_') or path.startswith('scripts/ghc_family_thalen_reed_v687_v8_') or path.startswith('tests/test_ghc_family_thalen_reed_v687_v8_')

def owner_files(root):
    paths=[]
    for dirname in [BASE,'scripts','tests']:
        p=root/dirname
        if p.exists():
            for f in p.rglob('*'):
                if f.is_file():
                    name=f.relative_to(root).as_posix()
                    if allowed(name):paths.append(name)
    return sorted(paths)

def privacy(items):
    candidates=[]
    for path,raw in items.items():
        text=raw.decode('utf-8')
        definition_lines=set()
        if path.endswith('.py'):
            tree=ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATTERNS' for t in node.targets):
                    definition_lines.update(range(node.lineno,node.end_lineno+1))
        for label,pattern in PATTERNS.items():
            for m in pattern.finditer(text):
                line=text.count('\n',0,m.start())+1
                candidates.append({'path':path,'line':line,'class':label,'adjudication':'scanner_definition' if line in definition_lines else 'confirmed_payload'})
    return {'schema':'ghc.family.five-class-privacy.v1','classes':list(PATTERNS),'files_scanned':len(items),'candidates':candidates,'confirmed_hits':sum(c['adjudication']=='confirmed_payload' for c in candidates),'scope':'Bounded owner text artifacts only; not complete privacy assurance.'}

def validate(root):
    get=lambda name:strict((root/BASE/'x1'/name).read_text(encoding='utf-8'))
    proposals=get('new-proposals.json'); rows=proposals['proposals'];prior=get('inherited-review.json');portfolio=get('portfolio-plan.json');truth=get('phase-truth.json');skills=get('skill-runner-plan.json')
    checks={
        'source':truth['source']==SOURCE,
        'planning_only':truth['state']=='PLANNING_ONLY_FREEZE' and not truth['x2_started'] and truth['x2_completion_credit']==0,
        'no_x2_directory':not (root/BASE/'x2').exists(),
        'proposal_count':len(rows)==200 and proposals['chain_after']==15430 and proposals['chain_before']==15230,
        'distinct_inputs':len({json.dumps(r['input'],sort_keys=True) for r in rows})==200,
        'ten_operation_families':len(Counter(r['operation'] for r in rows))==10 and set(Counter(r['operation'] for r in rows).values())=={20},
        'whole_expected_outputs':all(set(r['expected_output'])=={'accepted','value','error','external_credit'} and type(r['expected_output']['accepted']) is bool and r['expected_output']['external_credit'] is False for r in rows),
        'no_observed_outcomes':all('outcome' not in r and 'observed_output' not in r and r['execution_lane']=='x2_only' for r in rows),
        'inherited_zero_credit':len(prior['reviews'])==200 and all(r['new_owner_novelty_credit']==r['new_owner_completion_credit']==0 for r in prior['reviews']),
        'portfolio_counts':all(len(portfolio[k])==n for k,n in [('safe_now',300),('candidates',250),('clean_fix_refine',300),('exact_packets',50),('blocked_packets',30)]),
        'portfolio_unexecuted':all(r['executed'] is False for k in ['safe_now','candidates','clean_fix_refine','exact_packets','blocked_packets'] for r in portfolio[k]),
        'skills_and_runners':len(skills['skills'])==10 and len(skills['runners'])==5,
        'three_uninstalled_packages':len(get('package-plan.json')['direct_packages'])==3 and get('package-plan.json')['installed'] is False,
        'no_route_send':get('route-plan.json')['message_count']==0 and get('route-plan.json')['next_owner']=='Liora Venn' and get('route-plan.json')['next_phase']=='v688-v1',
        'three_overview_pages':(root/BASE/'x1/integrated-overview.html').read_text(encoding='utf-8').count('<section class="page">')==3,
        'terminal_boundary':truth['terminal_verdict']=='NOT_READY_FOR_STAGE_20',
    }
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--write',action='store_true');args=ap.parse_args();root=args.repo.resolve()
    assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==SOURCE
    checks=validate(root);assert all(checks.values()),checks
    out=root/BASE/'validation';out.mkdir(parents=True,exist_ok=True)
    def write(name,d):(out/name).write_text(json.dumps(d,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    if args.write:
        write('x1-checks.json',{'schema':'ghc.family.x1-structural-checks.v1','checks':checks,'execution_credit':0,'state':'PASS'})
        write('x1-privacy.json',{'schema':'ghc.family.five-class-privacy.v1','state':'pending_scan'})
        write('x1-staged-review.json',{'schema':'ghc.family.staged-allowlist.v1','state':'pending_scan'})
        mf=BASE+'validation/x1-manifest.json'
        paths=sorted(set(owner_files(root)+[mf]));assert len(paths)<2000
        write('x1-staged-review.json',{'schema':'ghc.family.staged-allowlist.v1','source':SOURCE,'allowed_paths':paths,'allowed_change_kind':'A','planned_path_count':len(paths),'x2_present':False})
        items={p:normalized(root/p) for p in paths if p!=mf};scan=privacy(items);assert scan['confirmed_hits']==0,scan;write('x1-privacy.json',scan)
        items={p:normalized(root/p) for p in paths if p!=mf}
        strict_count=0;ast_count=0
        for p,b in items.items():
            if p.endswith('.json'):strict(b.decode());strict_count+=1
            if p.endswith('.py'):ast.parse(b.decode(),filename=p);ast_count+=1
            if p.endswith(('.md','.html','.txt')):assert len(b.decode().split())<=100000
        entries=[{'path':p,'bytes_normalized_lf':len(b),'sha256_normalized_lf':hashlib.sha256(b).hexdigest()} for p,b in items.items()]
        write('x1-manifest.json',{'schema':'ghc.family.normalized-lf-manifest.v1','byte_domain':'normalized_lf_git_blob','source':SOURCE,'anchor':'PENDING_X1_COMMIT','entries':entries,'entry_count':len(entries),'declared_self_exclusions':[mf]})
        print(json.dumps({'state':'X1_STRUCTURAL_PASS','checks':len(checks),'manifest_entries':len(entries),'self_exclusions':1,'owner_files':len(paths),'strict_json':strict_count,'python_ast':ast_count,'confirmed_privacy_hits':0,'x2_execution_credit':0}))
    else:print(json.dumps({'state':'X1_STRUCTURAL_PASS','checks':checks}))

if __name__=='__main__':main()
