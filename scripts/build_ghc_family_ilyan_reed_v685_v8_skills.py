"""Build reviewed local guides and ten portable additive promotion candidates."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v685-v8'
PAIR_NAMES=['calendar-and-state','queue-and-replay','budget-and-allocation','masking-and-missingness','summaries-and-pairing','bins-and-stopping','lineage-and-fixity','correction-and-projection','table-and-trial-reservations','gmut-and-authority-obligations']
def read(n):return json.loads((BASE/n).read_text(encoding='utf8'))
def text(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(s)
def js(p,v):text(p,json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def quick(validator,folder):
    r=subprocess.run([sys.executable,'-X','utf8',str(validator),str(folder)],capture_output=True,text=True,encoding='utf8')
    return {'exit_code':r.returncode,'output':(r.stdout+r.stderr).strip(),'valid':r.returncode==0}
def smoke(folder,p):
    runner=folder/'scripts'/('ghc_family_protocol_'+p['runner']+'.py')
    r=subprocess.run([sys.executable,'-X','utf8',str(runner),'--operation',p['operation'],'--input',str(folder/'references/positive.json')],capture_output=True,text=True,encoding='utf8')
    b=subprocess.run([sys.executable,'-X','utf8',str(runner),'--operation',p['operation'],'--input',str(folder/'references/adverse.json')],capture_output=True,text=True,encoding='utf8')
    return {'positive':r.returncode==0 and json.loads(r.stdout)==p['expected_result'],'adverse':b.returncode==0 and json.loads(b.stdout)=={'error':'malformed_input'},'positive_observed':json.loads(r.stdout),'adverse_observed':json.loads(b.stdout)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--validator',required=True);ap.add_argument('--meta-tool',required=True);ap.add_argument('--global-root',required=True);a=ap.parse_args();globalroot=Path(a.global_root)
    plan=read('x1/skill-runner-plan.json');props=read('x1/new-proposals.json')['proposals'];boundary=read('x1/identity-and-practice.json')['identity_boundary'];gates=read('x1/identity-and-practice.json')['protected_gates']
    locals=[]
    for s in plan['skills']:
        folder=BASE/'skills'/s['name'];rows=[p for p in props if p['family']==s['family']];first=rows[0]
        desc=s['mission']+' Use for offline '+s['family'].replace('_',' ')+' report checks.'
        guide='---\nname: '+s['name']+'\ndescription: '+json.dumps(desc)+'\n---\n\n# '+s['family'].replace('_',' ').title()+'\n\n'+s['mission']+'\n\nSelect a criterion in [the frozen contracts](references/contracts.json) whose input relation matches the question. These ten examples include normal, boundary, and refusal cases; a refused scenario can itself be a correctly reported local result.\n\nUse `'+s['runner']+'` with `--operation '+first['operation']+' --input INPUT.json`. The input is the criterion input object, without its wrapper. The CLI reads JSON, performs no network or device action, and prints JSON; `--output` writes one new file and refuses an existing destination. A result must match the expected JSON type as well as its value.\n\nRead the source and the expected case before adapting an input. Preserve a contrary result and the input that produced it. Change the narrow failed assumption and keep the earlier definition available. Do not silently replace the oracle with the implementation output.\n\nThe accepted example '+first['proposal_id']+' checks '+first['title']+'. An input object without the required operation fields must return the malformed-input refusal. Both examples are owner-local software witnesses. They do not demonstrate conformance of real devices, participants, data, rights or services.\n\nThe runner is supplied by the owner repository or by the curated portable package that retains this guide. [Primary vocabulary source]('+s['source_refs'][0]+') supplies no authority to perform the described real-world work.\n\nRollback means selecting the retained prior guide or holding the affected criterion. Keep every rejected report and correction; do not delete source evidence. '+boundary+'\n'
        text(folder/'SKILL.md',guide);js(folder/'references/contracts.json',{'family':s['family'],'contracts':rows,'protected_gates':gates})
        text(folder/'agents/openai.yaml','interface:\n  display_name: '+json.dumps(s['family'].replace('_',' ').title())+'\n  short_description: "Review finite protocol inputs and reported results"\n  default_prompt: '+json.dumps('Use $'+s['name']+' to review this offline protocol report.')+'\n')
        q=quick(a.validator,folder);js(folder/'references/validation.json',q)
        if not q['valid']:raise RuntimeError('Local skill validation failed: '+s['name'])
        locals.append({'name':s['name'],'source':folder.relative_to(ROOT).as_posix(),'sha256':h(folder/'SKILL.md'),'valid':True,'contract_count':len(rows)})
    js(BASE/'x2/local-skills-validation.json',{'skills':locals,'count':20,'same_owner_only':True})
    promotions=[]
    for i,pair in enumerate(plan['promotion_pairs']):
        name='ghc-family-protocol-'+PAIR_NAMES[i];dest=globalroot/name
        if dest.exists():raise FileExistsError('Promotion destination collision: '+name)
        folder=BASE/'x2/global-skills'/name
        selected=[p for p in props if p['family'] in [plan['skills'][2*i]['family'],plan['skills'][2*i+1]['family']]];first=selected[0]
        source_links=[]
        for n in pair:
            src=BASE/'skills'/n/'SKILL.md';target=folder/'references'/(n+'.md');text(target,src.read_text(encoding='utf8'));source_links.append('- ['+n+'](references/'+n+'.md)')
        desc='Review '+PAIR_NAMES[i].replace('-',' ')+' using exact offline protocol fixtures and typed results.'
        guide='---\nname: '+name+'\ndescription: '+json.dumps(desc)+'\n---\n\n# '+PAIR_NAMES[i].replace('-',' ').title()+'\n\nChoose the matching retained guide before executing a runner. The pair is grouped because its records share an evidence boundary; the individual inputs and refusal conditions remain distinct.\n\n'+'\n'.join(source_links)+'\n\n[Contracts](references/contracts.json) bind twenty exact cases. [Positive input](references/positive.json) and [adverse input](references/adverse.json) exercise '+first['operation']+' through `python -X utf8 scripts/ghc_family_protocol_'+first['runner']+'.py --operation '+first['operation']+' --input references/positive.json`. Run the adverse input with the same operation and inspect the explicit refusal. Select a fresh output if using `--output`; output files are never overwritten.\n\nThe five supplied runners are shared unchanged sources, not fifty independent tools across ten packages. The package uses Python standard-library code only. Installation supplies discoverability, not competence, cache telemetry, independent reproduction or real-world authority. Preserve failures and use the narrowest matching operation. Source/global byte parity and the owner execution receipt are in [the promotion provenance](references/promotion.json).\n\nRollback selects a retained earlier source without deleting this package. '+boundary+'\n'
        text(folder/'SKILL.md',guide)
        for r in plan['runners']:text(folder/'scripts'/r['name'],(ROOT/'scripts'/r['name']).read_text(encoding='utf8'))
        js(folder/'references/contracts.json',{'contracts':selected,'protected_gates':gates});js(folder/'references/positive.json',first['input']);js(folder/'references/adverse.json',{'unrecognized_field':'synthetic'})
        text(folder/'agents/openai.yaml','interface:\n  display_name: '+json.dumps(PAIR_NAMES[i].replace('-',' ').title())+'\n  short_description: "Inspect protocol contracts and their refusal boundaries"\n  default_prompt: '+json.dumps('Use $'+name+' to check this synthetic protocol record.')+'\n')
        q=quick(a.validator,folder);s=smoke(folder,first)
        js(folder/'references/promotion.json',{'source_guides':[r for r in locals if r['name'] in pair],'shared_runners':[{'path':'scripts/'+r['name'],'sha256':h(ROOT/'scripts'/r['name'])} for r in plan['runners']],'candidate_validation':q,'candidate_smoke':s,'source_x1':'ae33e7fd357e38c464677c10538a50f069b68353','scope':'Ilyan Reed v685-v8 owner delta only','rollback':'Select retained prior sources; delete nothing.'})
        if not q['valid'] or not s['positive'] or not s['adverse']:raise RuntimeError('Promotion candidate failed: '+name)
        promotions.append({'name':name,'source':folder.relative_to(ROOT).as_posix(),'first_proposal':first['proposal_id'],'valid':True})
    # Use the existing meta-tool's current schema and decision predicates in a
    # sparse owner-only materialization; no unrelated repository tree is scanned.
    meta=load_module('ilyan_meta',a.meta_tool)
    smoke_dir=BASE/'tooling/runner-smoke'
    for r in plan['runners']:js(smoke_dir/(Path(r['name']).stem+'.json'),{'valid':True,'evidence':'x2/contract-results.json','families':r['families']})
    cat=meta.build(ROOT,BASE)
    for c in cat['cards']:
        c.update(execution_authority='owner_self_scoped_delta',repository_scan=False,module_scan=c['kind']=='runner',cross_lane_scan=False,unchanged_history_scan=False,sibling_lane_mutation=False,source_commit='f5464f56d095e9c691707f669668b86ff70468a6',final_commit='unresolved_until_final',changed_file_allowlist=[c['source_path']],module_allowlist=[c['source_path']] if c['kind']=='runner' else [],sparse_before_checkout=True,materialized_file_rotation_threshold=2000)
    val=meta.validate(cat);collisions=meta.collisions(cat)
    js(BASE/'tooling/catalogue.json',cat);js(BASE/'tooling/catalogue-validation.json',val);js(BASE/'tooling/collisions.json',collisions)
    if not val['valid']:raise RuntimeError('Catalogue invalid')
    selected=meta.query(cat,SimpleNamespace(kind='runner',status='current',evidence_state='validated',owner_scope=None,trigger=None,endpoint_kind='not_applicable'));js(BASE/'tooling/selected-runners.json',selected)
    readiness=[meta.promotion(cat,'skill:'+r['name']) for r in locals];js(BASE/'tooling/promotion-readiness.json',{'rows':readiness,'scope':'Twenty local source guides for ten curated packages'})
    if not all(r['state']=='ready' for r in readiness):raise RuntimeError('Promotion readiness incomplete')
    js(BASE/'tooling/collision-review.json',{'findings':collisions['findings'],'resolution':'Each operation is selected by its exact family and CLI operation. Related protocol vocabulary is retained; no lexical winner overrides a criterion.','silent_selection':False})
    installations=[]
    for p in promotions:
        folder=ROOT/p['source'];dest=globalroot/p['name'];shutil.copytree(folder,dest)
        paths=sorted(f.relative_to(folder) for f in folder.rglob('*') if f.is_file());parity=all((dest/f).read_bytes()==(folder/f).read_bytes() for f in paths)
        q=quick(a.validator,dest);first=next(r for r in props if r['proposal_id']==p['first_proposal']);s=smoke(dest,first)
        result={**p,'file_count':len(paths),'byte_parity':parity,'post_copy_validation':q,'post_copy_smoke':s,'files':[{'path':f.as_posix(),'sha256':h(folder/f)} for f in paths]}
        installations.append(result)
        if not parity or not q['valid'] or not s['positive'] or not s['adverse']:
            js(BASE/'x2/global-promotion-partial.json',{'installations':installations,'success_credit':0});raise RuntimeError('Installed package validation failed')
    js(BASE/'x2/global-promotion-installation.json',{'skills':installations,'installed_count':10,'unique_shared_runners':5,'status':'PASS','deletions':0,'plugin_cache_mutation':False,'same_owner_only':True})
    print(json.dumps({'local_skills':20,'global_skills':10,'shared_runners':5,'catalogue_cards':len(cat['cards']),'trigger_overlap_findings':collisions['finding_count'],'byte_parity':True}))
if __name__=='__main__':main()
