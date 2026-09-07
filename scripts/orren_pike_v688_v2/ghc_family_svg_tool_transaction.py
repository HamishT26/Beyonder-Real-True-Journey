"""Validate and use the read local packages, then promote to fresh destinations."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,urllib.request
from build_ghc_family_svg_x1 import ROOT,BASE,BANK,SKILL_PAIRS,strict,write,canonical

def invoke(command):
 r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 return r.returncode,r.stdout.decode('utf-8'),r.stderr.decode('utf-8')
def main():
 scratch=BANK/'interface-fixtures';scratch.mkdir(exist_ok=False)
 ps=strict((BASE/'x1/new-proposals.json').read_bytes())['proposals']
 validator=pathlib.Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py'
 skill_results=[];runner_results=[]
 for name,ops in SKILL_PAIRS:
  package=BASE/'skills'/name
  guide=package.joinpath('SKILL.md').read_bytes();contracts=strict((package/'references/contracts.json').read_bytes())['contracts']
  assert {p['operation'] for p in contracts}==set(ops)
  code,out,err=invoke([sys.executable,'-X','utf8',str(validator),str(package)]);assert code==0,(name,out,err)
  p=next(p for p in contracts if p['expected_output']['accepted']);good=scratch/(name+'-accept.json');good.write_bytes(canonical(p['input']))
  evil=scratch/(name+'-duplicate.json');evil.write_text('{"operation":"'+ops[0]+'","operation":"'+ops[0]+'"}',encoding='utf-8')
  cc,oo,ee=invoke([sys.executable,'-X','utf8',str(package/'scripts/ghc_family_svg_skill.py'),str(good)]);assert cc==0 and strict(oo)==p['expected_output'],(name,oo,ee)
  nc,no,ne=invoke([sys.executable,'-X','utf8',str(package/'scripts/ghc_family_svg_skill.py'),str(evil)]);assert nc==2 and strict(no)['error']=='DUPLICATE_KEY',(name,no,ne)
  skill_results.append({'name':name,'guide_sha256':hashlib.sha256(guide).hexdigest(),'complete_guide_read_before_use':True,'validator_pass':True,'accepting_proposal':p['proposal_id'],'positive':strict(oo),'adverse':strict(no),'adverse_candidate_credit':0})
 for i in range(5):
  runner=ROOT/'scripts/orren_pike_v688_v2'/f'ghc_family_svg_group_{i+1}.py';ops=SKILL_PAIRS[2*i][1]+SKILL_PAIRS[2*i+1][1];passed=[]
  for op in ops:
   p=next(p for p in ps if p['operation']==op and p['expected_output']['accepted']);inp=scratch/(op+'-runner.json');inp.write_bytes(canonical(p['input']))
   c,o,e=invoke([sys.executable,'-X','utf8',str(runner),str(inp)]);assert c==0 and strict(o)==p['expected_output'],(op,o,e);passed.append({'operation':op,'proposal_id':p['proposal_id'],'actual_output':strict(o)})
  c,o,e=invoke([sys.executable,'-X','utf8',str(runner),str(evil)]);assert c==2 and strict(o)['error']=='DUPLICATE_KEY'
  runner_results.append({'name':runner.name,'operations':passed,'adverse':strict(o),'adverse_candidate_credit':0})
 write('x2/skill-use.json',{'rows':skill_results,'count':10,'workflow':'Current installed skill-creator guide and quick_validate.py; complete guides read before use.'})
 write('x2/runner-use.json',{'rows':runner_results,'count':5,'positive_operations':20})
 write('x2/package-smokes.json',strict((BANK/'package-smokes.json').read_bytes()))
 packages=strict((BASE/'x1/package-plan.json').read_bytes())['packages'];audit=[]
 for p in packages:
  with urllib.request.urlopen(f"https://pypi.org/pypi/{p['name']}/{p['version']}/json",timeout=25) as res:v=json.load(res)
  w=next(w for w in v['urls'] if w['filename']==p['wheel_files'][0]['filename']);assert w['digests']['sha256']==p['wheel_files'][0]['sha256'] and not w['yanked']
  audit.append({'name':p['name'],'version':p['version'],'known_advisories':v.get('vulnerabilities',[]),'yanked':w['yanked'],'wheel_sha256':w['digests']['sha256']})
 write('x2/package-audit.json',{'rows':audit,'known_advisories':sum(len(r['known_advisories']) for r in audit),'source':'Official exact-release PyPI metadata, one bounded x2 review','independent_security_review':'open_gap','exhaustive_security':False})
 write('x2/environment-receipt.json',{'versions':strict((BANK/'package-smokes.json').read_bytes())['versions'],'distribution_count':3,'host_python_mutated':False,'no_index':True,'wheel_only':True,'require_hashes':True,'base_dependencies':0,'installation_report_sha256':hashlib.sha256((BANK/'installation-report.json').read_bytes()).hexdigest(),'rollback':'Stop selecting the owner environment; retain it and the evidence.'})
 # Every mutation below targets a collision-free additive destination.
 target_skills=pathlib.Path.home()/'.codex/skills';target_runners=pathlib.Path.home()/'.codex/scripts'
 sources=[ROOT/'scripts/orren_pike_v688_v2'/f'ghc_family_svg_group_{i+1}.py' for i in range(5)]+[ROOT/'scripts/orren_pike_v688_v2/ghc_family_svg_evidence_core.py']
 for n,ops in SKILL_PAIRS:assert not (target_skills/n).exists(),n
 for p in sources:assert not (target_runners/p.name).exists(),p.name
 members=[]
 for name,ops in SKILL_PAIRS:
  src=BASE/'skills'/name;dest=target_skills/name;shutil.copytree(src,dest,ignore=shutil.ignore_patterns('__pycache__'))
  for p in sorted(src.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts:continue
   rel=p.relative_to(src);raw=p.read_bytes();assert (dest/rel).read_bytes()==raw
   members.append({'kind':'skill','name':name,'relative':rel.as_posix(),'source':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
  c,o,e=invoke([sys.executable,'-X','utf8',str(validator),str(dest)]);assert c==0,(name,o,e)
  local=next(r for r in skill_results if r['name']==name);good=scratch/(name+'-accept.json')
  c,o,e=invoke([sys.executable,'-X','utf8',str(dest/'scripts/ghc_family_svg_skill.py'),str(good)]);assert c==0 and strict(o)==local['positive']
 for p in sources:
  dst=target_runners/p.name
  with dst.open('xb') as f:f.write(p.read_bytes())
  assert dst.read_bytes()==p.read_bytes();members.append({'kind':'runner','name':p.name,'relative':p.name,'source':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 for i,r in enumerate(runner_results):
  for op in r['operations']:
   c,o,e=invoke([sys.executable,'-X','utf8',str(target_runners/r['name']),str(scratch/(op['operation']+'-runner.json'))]);assert c==0 and strict(o)==op['actual_output']
 write('x2/promotion-receipt.json',{'schema':'ghc.family.additive-promotion.v1','members':members,'file_count':len(members),'skills':10,'runners':5,'shared_core':1,'overwrites':0,'caches_copied':0,'local_skill_validations':10,'global_skill_validations':10,'local_runner_operations':20,'global_runner_operations':20,'global_skill_operations':10,'all_source_global_bytes_equal':True,'rollback':'Stop selecting the new packages and runners; retain source, prior callers, new files and evidence.','independent_reproduction':False})
 print(json.dumps({'skills_validated_and_used':10,'runners_used':5,'global_parity_files':len(members),'overwrites':0,'package_advisories':sum(len(r['known_advisories']) for r in audit)}))
if __name__=='__main__':main()
