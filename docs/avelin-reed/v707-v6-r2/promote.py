from pathlib import Path
import json,hashlib,shutil,subprocess
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2];BANK=Path(r'D:\GHC-Archives\phase-banks\avelin-reed-v707-v6-r2');GLOBAL=Path.home()/'.codex/skills'
LAB=Path(r'D:\GHC-Family-Laboratory');RELEASE=LAB/'releases/avelin-v707-v6-r2'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def validate(p):
 r=subprocess.run([str(Path.home()/'AppData/Local/Programs/Python/Python312/python.exe'),'-X','utf8','-B',str(GLOBAL/'.system/skill-creator/scripts/quick_validate.py'),str(p)],capture_output=True,text=True,encoding='utf-8',timeout=40)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 return r.returncode
inventory=load(BANK/'skill-inventory.json');expected={r['id']:r['sha256'] for r in inventory}
names=[r['name'] for r in load(BANK/'skill-preflight-bindings.json')]+['ghc-family-index','ghc-family-meta-tool-box','ghc-family-method-flow-state','ghc-worktree-branch-rotation']
header='''
## Current workflow v20 - Hamish direct authority, 28 September 2026

Read [workflow v20](../ghc-family-index/references/current-workflow-v20.json), [the complete roster](../ghc-family-index/references/current-roster-v20.json), and [current authorization](../ghc-family-auth-permission-state/references/current-authorization-v20.json) before historical defaults below. Avelin v707-v6 is sealed; Avelin v707-v6-r2 is interstitial. Only after its terminal gate may the existing Caelen Ash chat be activated for v707-v7. Subsequent rows advance one terminal edge at a time through Eiren v725-v8. The existing Review and refine GHC Lab ChatGPT conversation receives one advisory message in each x1 and each x2 session. Allow time for replies while progressing independent work. It is not a roster seat or successor. The current late-added requirement is recorded without retroactive x1 credit. Read consultation-policy-v20.json; its private target is excluded from exports.

Use 20 initial projects within a cap of 80. Old safe, candidate and CLEAN/FIX/REFINE minima are removed. Each x1 and x2 has caps of 1000 safe, 1000 candidate, 1000 CLEAN/FIX/REFINE, 30 skills, 20 runners, 500 tests, 100 models and 2000 web searches. Each session needs at least 15 models. Each phase needs at least five hooks, fifteen labelled law hypotheses and fifteen open-problem probes, eight learning practices and four successor suggestions; recommend at least five skills and five runners. Exact packets cap at 250 and blocked packets at 100. Define work before execution and append adaptive definitions without rewriting frozen evidence.

Use the D-first GHC Family Laboratory and source-bound contribution cards. Preserve original laboratories and callers. Catalogue, local-test, installation and host-observation states are distinct. Roster membership, scheduled turn and observed activity are distinct. Inherited and failed evidence receives zero new or original success credit. Reuse owner main branches below 2000 files. JSON, MD and TXT are preferred; HTML and other formats are allowed; PDFs are prohibited. Batons remain 2000–100000 words on D with Method Flow and failures separate.

Hamish authorizes concrete safe, candidate and exact work, additive global installations, shared updates and one small memory extension. USD50 is a ceiling. The desktop app remains user-managed. Application permissions do not create a Windows administrator token. Empirical, professional, legal, cultural, Maori, affected-party and identity claims require their actual evidence and authority. Use the registered admitted-model launcher without changing model settings.

Before an unavailable-route hold, use five bounded supported recovery checks. Up to three corrected submissions apply only after definite preacceptance failure. Accepted, queued, opaque or unresolved state stops duplicates. No new task, fork, subagent, standby substitution, early successor contact or source/domain/canonical replay follows from this control. Historical sections remain preserved; their prospective defaults are superseded here.

'''
# Preflight every shared destination before the first mutation.
for name in names:
 if sha((GLOBAL/name/'SKILL.md').read_bytes())!=expected[name]:raise RuntimeError('Shared source drift: '+name)
groups=[('laboratory','catalogue','Unified family entrypoint, source library and explicit contribution cards.'),('models','model','Finite models with named quantities, units and falsifiers.'),('evidence','integrity','Source bytes, bounded intake and correction lineage.'),('governance','claim','Issuer assertions, consent, remedy and protected claims.'),('workflow','route','Current limits, weighted roster and a non-sending route guard.'),('capabilities','catalogue','Search installed skills while preserving narrow caller contracts.')]
for group,op,desc in groups:
 if (GLOBAL/('ghc-family-main-'+group+'-v20')).exists():raise RuntimeError('Global guide collision: '+group)
if RELEASE.exists() or (LAB/'current.json').exists():raise RuntimeError('Laboratory release or pointer collision')
changes=[]
for name in names:
 target=GLOBAL/name/'SKILL.md';raw=target.read_bytes();text=raw.decode('utf-8-sig');end=text.find('\n---',3)+4
 if end<4:raise RuntimeError('Frontmatter missing')
 new=(text[:end]+header+text[end:]).encode('utf-8')
 before=BANK/'shared-before'/name/'SKILL.md';before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(raw)
 mirror=ROOT/'shared-updates'/name/'SKILL.md';mirror.parent.mkdir(parents=True,exist_ok=True);mirror.write_bytes(new);target.write_bytes(new)
 changes.append({'name':name,'source_before_sha256':sha(raw),'installed_sha256':sha(new),'source_path':mirror.relative_to(ROOT).as_posix(),'validation_exit':validate(target.parent)})
 save(BANK/'promotion-progress.json',{'shared_headers':changes})
for name,dest,source in [('ghc-family-index','current-workflow-v20.json','workflow-v20.json'),('ghc-family-index','current-roster-v20.json','roster-v20.json'),('ghc-family-roster-check','current-roster-v20.json','roster-v20.json'),('ghc-family-index','consultation-policy-v20.json','consultation-policy-v20.json')]:
 p=GLOBAL/name/'references'/dest
 if p.exists():raise RuntimeError('Control destination exists: '+dest)
 obj=load(BASE/source)
 if source=='workflow-v20.json':obj['advisory_consultation']=load(BASE/'consultation-policy-v20.json')
 save(p,obj);save(ROOT/'shared-updates'/name/'references'/dest,obj)
auth={'schema':'ghc.authorization.v20','authority':'Hamish direct requests in this Avelin chat','authorized_now':['owner implementation','D-first laboratory','source-read-only intake','scoped shared controls','additive skills and hooks','selected stable tool updates','sanitized remote archive','one memory extension'],'separate_advisory_messages':{'title':'Review and refine GHC Lab','count_per_bundle':2,'x1':1,'x2':1},'terminal_successor':{'owner':'Caelen Ash','phase':'v707-v7','gate_required':True},'metadata_does_not_grant':['empirical truth','legal identity','consciousness','professional qualification','affected-party or Maori authority','Windows administrator token'],'new_tasks_or_subagents':False}
p=GLOBAL/'ghc-family-auth-permission-state/references/current-authorization-v20.json'
if p.exists():raise RuntimeError('Authorization destination exists')
save(p,auth);save(ROOT/'shared-updates/ghc-family-auth-permission-state/references/current-authorization-v20.json',auth)
curated=[]
for group,op,desc in groups:
 name='ghc-family-main-'+group+'-v20';src=ROOT/'skills'/name;dest=GLOBAL/name;src.mkdir(parents=True,exist_ok=True)
 guide=f'''---
name: {name}
description: {desc}
---

# GHC Family Main {group.title()}

{desc}

Read the current workflow v20 and the exact selected source guide before execution. The unified catalogue covers every direct installed SKILL.md at its recorded snapshot; matching metadata does not prove semantic equivalence or validate every implementation. Original guide names and callers remain available.

Run scripts/runner.txt with a request JSON file and a new output JSON file. This guide selects the {op} operation from the D-first laboratory release. It does not contact chats, issue credentials, launch cloud jobs or grant OS privileges. The main laboratory guide is the common discovery entrypoint; five narrower guides provide tested operations.

Contracts: model uses model, variant, steps and optional parameter; catalogue uses query and limit 1..50; integrity uses a repository-relative path, content, bytes and SHA-256; claim uses issuer, subject, claim, evidence and kind; route uses owner, phase and explicit boolean prerequisites. Read laboratory/operations.js for the exact field list. Unknown fields and out-of-range values are refused.

Model cards specify quantities, units, assumptions, baseline, tolerance and falsifier. Contributions preserve source, inputs, result, checks, limitations and superseded-record links. Catalogue, local test, installation and host observation are separate states. Roster membership is not activity.

Five local guides and the earlier v18 router remain compatible. All inherited inventory entries remain discovery sources and are not silently executed. Consolidation occurs through common public operations and adapters. Distinct evidence histories remain distinct.

Rollback by selecting the previous laboratory release and current pointer. This guide is additive; remove it only after accounting for its callers. Preserve prior shared bytes from the external rollback bank. Installed parity and manual smokes do not establish live hook execution.

Finite synthetic same-owner evidence only. No empirical GMUT confirmation, production assurance, consciousness, personhood, legal identity, qualification, cultural or Maori authority, or Stage 20 readiness. NOT_READY_FOR_STAGE_20.
'''
 (src/'SKILL.md').write_text(guide,encoding='utf-8');(src/'scripts').mkdir(exist_ok=True)
 wrapper="'use strict';const cp=require('child_process');const r=cp.spawnSync(process.execPath,['D:/GHC-Family-Laboratory/releases/avelin-v707-v6-r2/laboratory/runner.txt','"+op+"',...process.argv.slice(2)],{stdio:'inherit',windowsHide:true});process.exitCode=r.status??1;\n"
 (src/'scripts/runner.txt').write_text(wrapper,encoding='utf-8');validate(src);shutil.copytree(src,dest);validate(dest)
 parity=all((dest/p.relative_to(src)).read_bytes()==p.read_bytes() for p in src.rglob('*') if p.is_file())
 curated.append({'name':name,'operation':op,'source_path':(src/'SKILL.md').relative_to(ROOT).as_posix(),'sha256':sha((src/'SKILL.md').read_bytes()),'validation_exit':0,'installed_parity':parity,'installed_runner_smoke':'pending','host_observed':False})
 inventory.append({'id':name,'path':'skills/'+name+'/SKILL.md','sha256':sha((dest/'SKILL.md').read_bytes()),'bytes':(dest/'SKILL.md').stat().st_size,'description':desc,'scope':'bounded_operation_guide','legacy_callers_preserved':True,'capability_states':{'catalogued':True,'locally_tested':'structural validation','installed':'byte parity observed','host_observed':False}})
 save(BANK/'promotion-progress.json',{'shared_headers':changes,'curated':curated})
for row in inventory:
 row.setdefault('capability_states',{'catalogued':True,'locally_tested':'not_observed_in_this_run','installed':'source_file_present_at_snapshot','host_observed':False})
 if row['id'] in names:
  raw=(GLOBAL/row['id']/'SKILL.md').read_bytes();row['previous_snapshot_sha256']=row['sha256'];row['sha256']=sha(raw);row['bytes']=len(raw)
save(ROOT/'laboratory/data/skills.json',inventory)
RELEASE.mkdir(parents=True)
for directory in ['laboratory','models','runners']:shutil.copytree(ROOT/directory,RELEASE/directory)
entries=[{'path':p.relative_to(RELEASE).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(RELEASE.rglob('*')) if p.is_file()]
manifest={'schema':'ghc.lab.release.v1','entries':entries,'source_branch':'codex/GHC-Family/avelin-reed-main-1','exact_x2_commit':'bound by subsequent phase receipt','mutable_current_pointer_separate':True}
save(RELEASE/'release-manifest.json',manifest);save(LAB/'current.json',{'schema':'ghc.lab.current.v1','release':'releases/avelin-v707-v6-r2','manifest_sha256':sha((RELEASE/'release-manifest.json').read_bytes()),'source_phase':'v707-v6-r2'})
save(BASE/'global-promotion.json',{'schema':'ghc.additive-promotion.v1','shared_headers':changes,'curated':curated,'catalogue_count':len(inventory),'release_files':len(entries),'release_manifest_sha256':sha((RELEASE/'release-manifest.json').read_bytes()),'caller_deletions':0,'sibling_mutations':0,'semantic_equivalence_of_inventory_claimed':False})
save(BASE/'shared-laboratory-manifest.json',manifest)
print(json.dumps({'shared_skill_headers':len(changes),'new_global_skills':len(curated),'parity':all(r['installed_parity'] for r in curated),'catalogue_count':len(inventory),'release_files':len(entries)}))
