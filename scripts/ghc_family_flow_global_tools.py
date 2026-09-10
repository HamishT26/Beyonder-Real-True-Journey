"""Prepare and validate five merged capabilities before one additive promotion."""
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
from scripts.ghc_family_flow_common import canonical
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/mira-fenwick/v690-v3';CANDIDATES=BASE/'x2/global-candidates'
def read(path):return json.loads((BASE/path).read_text(encoding='utf-8'))
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write((json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def load_helper(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def smoke(root,group,rows,out):
    out.mkdir(parents=True,exist_ok=False);checks=[]
    selected=[next(r for r in rows if r['operation']==op) for op in group['operations']]
    outside=next(r for r in rows if r['operation'] not in group['operations'])
    for n,row in enumerate(selected+[outside]):
        request=out/f'input-{n}.json';output=out/f'output-{n}.json';write(request,row['request'])
        proc=subprocess.run([sys.executable,'-X','utf8','-m','scripts.'+Path(group['runner']).stem,'--input',str(request),'--output',str(output)],cwd=root,capture_output=True)
        value=json.loads(output.read_text(encoding='utf-8'));expected=row['expected_envelope'] if n<4 else {'accepted':False,'result':None,'error':'outside_runner_group'}
        correct=proc.returncode==(0 if n<4 else 2) and canonical(value)==canonical(expected)
        checks.append({'operation':row['operation'],'expected':expected,'observed':value,'returncode':proc.returncode,'pass':correct,'subject_original_success_credit':1 if n<4 else 0,'outside_group':n==4})
    write(out/'receipt.json',{'runner':group['runner'],'checks':checks,'pass':all(x['pass'] for x in checks),'same_owner_only':True});assert all(x['pass'] for x in checks)
    return {'runner':group['runner'],'pass':True,'accepting_checks':4,'rejected_subjects':1,'receipt':(out/'receipt.json').relative_to(BASE).as_posix()}

def prepare():
    groups=read('plan/skills-runners.json')['global_groups'];rows=read('plan/new-proposals.json')['proposals'];identity=read('plan/identity-practices.json')
    CANDIDATES.mkdir(parents=True,exist_ok=False);(CANDIDATES/'scripts').mkdir()
    for name in ['__init__.py','ghc_family_flow_common.py','ghc_family_flow_x1.py','ghc_family_flow_x2.py']:
        shutil.copyfile(ROOT/'scripts'/name,CANDIDATES/'scripts'/name)
    for group in groups:
        text=f'''"""Bounded flow capability: {group['skill']}."""
from scripts.ghc_family_flow_common import cli
from scripts.ghc_family_flow_x1 import evaluate as first, REQUIRED
from scripts.ghc_family_flow_x2 import evaluate as second

def evaluate(request):
    return first(request) if request.get('op') in REQUIRED else second(request)

if __name__ == '__main__':
    raise SystemExit(cli(evaluate, {tuple(group['operations'])!r}))
'''
        (CANDIDATES/'scripts'/group['runner']).write_bytes(text.encode())
    quick=Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py';validations=[];smokes=[]
    for group in groups:
        folder=CANDIDATES/'skills'/group['skill'];folder.mkdir(parents=True);sources=[]
        for op in group['operations']:
            local=next(s for s in read('plan/skills-runners.json')['local_skills'] if s['operation']==op)
            path=BASE/local['session']/'skills'/local['name']/'SKILL.md';raw=path.read_bytes()
            sources.append({'operation':op,'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'source_guide':raw.decode(),'source_credit':0})
        text=f'''---
name: {group['skill']}
description: Review finite flow operations {', '.join(group['operations'])} with exact scope and retained refusal evidence.
---

# {group['skill'].removeprefix('ghc-family-').replace('-',' ').capitalize()}

This package combines four retained owner-local guides. Read [the source guides and operation map](references/source-guides.json) and select the operation matching the actual request. Its public runner is `{group['runner']}` in the archive-relative root `global-tools/family-flow-certificates`.

From that root, run `python -X utf8 -m scripts.{Path(group['runner']).stem} --input OWNED_INPUT.json --output FRESH_OUTPUT.json`. The adjacent `scripts` package and all three core modules are required. Rootless direct-file execution is outside this caller contract. No third-party solver package is required by this public runner.

The public operations are `{', '.join(group['operations'])}`. Requests use explicit directed arcs and integer capacities; undeclared fields and unsupported groups are refused. The finite profile has at most eight vertices, twelve arcs, capacities through eight, and at most fifty thousand enumerated flow candidates. Internal helpers assume already validated values; use the closed evaluator or runner boundary.

Compare complete typed envelopes and source-input nonmutation. Preserve a failed subject at zero original credit even when its guard passes. Retain failed definitions and add separately bound corrections. A matching digest, feasible flow or optimum value does not supply consent, identity, fairness, professional judgment, legal or cultural legitimacy, affected-party standing, Māori authority or permission for a real action.

Roll back by selecting retained prior tooling; preserve this package and its evidence. Global presence is discoverability, not evidence that an active task has reloaded it. Keep completed, represented, open_gap and exact_gate separate. NOT_READY_FOR_STAGE_20.
'''
        (folder/'SKILL.md').write_bytes(text.encode())
        (folder/'agents').mkdir();label=group['skill'].removeprefix('ghc-family-').replace('-',' ').title()
        yaml=f'interface:\n  display_name: {json.dumps(label)}\n  short_description: "Review bounded flow evidence and refusal conditions"\n  default_prompt: {json.dumps("Use $"+group['skill']+" to inspect an exact synthetic flow request and its evidence limits.")}\n'
        (folder/'agents/openai.yaml').write_bytes(yaml.encode());write(folder/'references/source-guides.json',{'sources':sources,'archive_relative_runner_root':'global-tools/family-flow-certificates','operations':group['operations']})
        result=subprocess.run([sys.executable,'-X','utf8',str(quick),str(folder)],capture_output=True);assert result.returncode==0,'Merged metadata validation failed.'
        validations.append({'skill':group['skill'],'official_metadata_pass':True,'retained_local_guides':4})
        smokes.append(smoke(CANDIDATES,group,rows,BASE/'x2/global-local-smokes'/group['skill']))
    write(BASE/'x2/global-preflight.json',{'skills':validations,'runners':smokes,'pass':True,'actual_global_mutation':False})
    cards=[]
    def card(name,kind,path,operations,caller,status='current'):
        cards.append({'card_id':kind+':'+name,'name':name,'kind':kind,'source_path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'status':status,'evidence_state':'validated','owner_scope':'Mira Fenwick v690-v3 exact owner delta','triggers':operations,'caller_paths':[caller],
          'rollback':'Stop selecting the exact additive capability and preserve its bytes and receipts.','protected_gates':identity['protected_gates'],
          'execution_authority':'owner_self_scoped_delta','repository_scan':False,'module_scan':kind=='runner','cross_lane_scan':False,'unchanged_history_scan':False,'sibling_lane_mutation':False,
          'supported_endpoint_kinds':['not_applicable'],'route_controller_scope':'not_applicable','delivery_ack_required':False})
    plan=read('plan/skills-runners.json')
    for s in plan['local_skills']:card(s['name'],'skill',BASE/s['session']/'skills'/s['name']/'SKILL.md',[s['operation']],f'docs/mira-fenwick/v690-v3/{s["session"]}/skill-validation.json')
    for r in plan['local_runners']:card(r['name'],'runner',ROOT/'scripts'/r['name'],r['operations'],f'docs/mira-fenwick/v690-v3/{r["session"]}/execution-summary.json')
    for g in groups:
        card(g['skill'],'skill',CANDIDATES/'skills'/g['skill']/'SKILL.md',g['operations'],'docs/mira-fenwick/v690-v3/x2/global-preflight.json')
        card(g['runner'],'runner',CANDIDATES/'scripts'/g['runner'],g['operations'],'docs/mira-fenwick/v690-v3/x2/global-preflight.json')
    catalogue={'schema':'ghc.family.meta-tool-box.catalogue.v2','owner':'Mira Fenwick','phase':'v690-v3','cards':cards,'card_count':len(cards),'boundary':identity['boundary']}
    tool=load_helper('family_meta',Path.home()/'.codex/skills/ghc-family-meta-tool-box/scripts/ghc_family_meta_tool_box.py')
    validation=tool.validate(catalogue);collisions=tool.collisions(catalogue);assert validation['valid']
    write(BASE/'x2/meta-tool-catalogue.json',catalogue);write(BASE/'x2/meta-tool-validation.json',validation);write(BASE/'x2/meta-tool-collisions.json',collisions)
    promotions=[tool.promotion(catalogue,'skill:'+g['skill']) for g in groups]
    assert all(p['state']=='ready' for p in promotions)
    write(BASE/'x2/promotion-policy-preflight.json',{'checks':promotions,'all_ready':True,'global_mutation_performed':False})
    print(json.dumps({'catalogue_cards':len(cards),'merged_skills':5,'public_runners':5,'local_smokes_passed':True,'promotion_policies_ready':True,'collision_findings':collisions.get('finding_count')}))

def promote(destination):
    plan=read('plan/skills-runners.json');groups=plan['global_groups'];rows=read('plan/new-proposals.json')['proposals']
    assert read('x2/global-preflight.json')['pass'] and read('x2/promotion-policy-preflight.json')['all_ready']
    skill_root=Path.home()/'.codex/skills'
    assert not destination.exists() and all(not (skill_root/g['skill']).exists() for g in groups),'Existing destination; no overwrite allowed.'
    destination.mkdir(parents=True);shutil.copytree(CANDIDATES/'scripts',destination/'scripts');records=[]
    quick=Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py'
    for group in groups:
        src=CANDIDATES/'skills'/group['skill'];dst=skill_root/group['skill'];shutil.copytree(src,dst)
        for file in sorted(src.rglob('*')):
            if file.is_file():
                relative=file.relative_to(src);raw=file.read_bytes();assert (dst/relative).read_bytes()==raw
                records.append({'kind':'skill','name':group['skill'],'path':relative.as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        result=subprocess.run([sys.executable,'-X','utf8',str(quick),str(dst)],capture_output=True);assert result.returncode==0
    for file in sorted((CANDIDATES/'scripts').iterdir()):
        if file.is_file():
            raw=file.read_bytes();assert (destination/'scripts'/file.name).read_bytes()==raw
            records.append({'kind':'public_runner_or_dependency','path':'scripts/'+file.name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    smokes=[smoke(destination,g,rows,BASE/'x2/global-installed-smokes'/g['skill']) for g in groups]
    write(BASE/'x2/global-promotion.json',{'skills':5,'public_runners':5,'core_modules':3,'package_initializer':1,'dependency_runner_credit':0,'global_skill_files':15,'public_files':9,'records':records,
          'all_byte_parity':True,'official_global_metadata_pass':True,'installed_smokes':smokes,'destination_absence_preflight':True,'overwrites':0,'archive_relative_public_root':'global-tools/family-flow-certificates','rollback':'Select prior tooling while preserving these exact additive files.'})
    print(json.dumps({'promoted_skills':5,'public_runners':5,'files_byte_verified':len(records),'installed_smokes_passed':True}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--promote-to',type=Path);a=p.parse_args()
    promote(a.promote_to) if a.promote_to else prepare()
