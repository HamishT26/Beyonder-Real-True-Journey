"""Audit only the Merrin v688-v4 delta; canonical mode has an exclusive latch."""
import argparse
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import ghc_family_reaction_core as core

SOURCE='612ec0a16fc75bd9e4dcdebd7d9bcb21432ab153'
INITIAL_X1='8c1c83b3311e8527a82ccd931b39f924a14ce328'
X1='85617b39c876177842a2ae351373da1700b48a15'
PREFIX='docs/merrin-vale/v688-v4/'
BRANCH='codex/GHC-Family/merrin-vale-v688-v4-full-tools'
PRIVATE_PATTERNS={
 'raw_uuid':r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
 'private_local_path':r'(?i)(?<![a-z0-9])(?:[A-Z]:[\\/]|/Users/|/home/)',
 'private_uri':r'(?i)(?:chatgpt\.com/c/|chat\.openai\.com/|codex://|app://)',
 'delegation_markup':r'(?i)<(?:source_thread_id|codex_delegation|task_id)>',
 'credential_assignment':r'(?i)(?:api_key|access_token|secret_key|private_key)\s*[=:]\s*["\x27]?[A-Za-z0-9+/=_-]{12,}',
}

def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(data):return json.dumps(data,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,sort_keys=True,ensure_ascii=True,indent=2);f.write('\n')

def audit(args):
 repo=args.repo.resolve();root=repo/PREFIX
 def git(*values):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*values])
 def g(*values):return git(*values).decode().strip()
 def read(path):return core.strict_loads(path.read_text(encoding='utf-8'))
 def remote():
  heads={'local':g('rev-parse','HEAD'),'upstream':g('rev-parse','@{upstream}'),'tracking':g('rev-parse','refs/remotes/origin/'+BRANCH),'fresh_live':g('ls-remote','origin','refs/heads/'+BRANCH).split()[0]}
  assert len(set(heads.values()))==1
  assert not g('status','--porcelain=v1')
  divergence=[int(v) for v in g('rev-list','--left-right','--count','HEAD...@{upstream}').split()];assert divergence==[0,0]
  return {'heads':heads,'clean':True,'divergence':divergence,'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 assert g('branch','--show-current')==BRANCH
 before=remote() if args.stage=='final' else None
 head=g('rev-parse','HEAD')
 if args.stage=='evidence':assert head==X1
 if args.stage=='final':assert args.evidence and g('rev-parse','HEAD^')==args.evidence and g('rev-parse',args.evidence+'^')==X1
 assert g('rev-parse',X1+'^')==INITIAL_X1 and g('rev-parse',INITIAL_X1+'^')==SOURCE
 assert not g('rev-list','--merges',SOURCE+'..HEAD')
 owned=[p for p in root.rglob('*') if p.is_file()]
 assert len(owned)<2000
 assert all('__pycache__' not in p.parts and p.suffix!='.pyc' for p in owned)
 parsed={};privacy=[];security=[];ast_count=0;largest_words=0
 for path in owned:
  rel=path.relative_to(repo).as_posix();text=path.read_text(encoding='utf-8');largest_words=max(largest_words,len(text.split()))
  assert len(text.split())<=100000,rel
  if path.suffix=='.json':parsed[rel]=core.strict_loads(text)
  if path.suffix=='.py':
   tree=ast.parse(text);ast_count+=1
   for node in ast.walk(tree):
    if isinstance(node,ast.Call):
     name=ast.unparse(node.func)
     if name in {'eval','exec','os.system','pickle.loads'} or any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords):security.append({'path':rel,'line':node.lineno,'call':name})
  for label,pattern in PRIVATE_PATTERNS.items():
   for match in re.finditer(pattern,text):
    line=text.count('\n',0,match.start())+1
    definition=(path.name=='ghc_family_reaction_owner_audit.py' and ("'"+label+"':") in text.splitlines()[line-1])
    privacy.append({'path':rel,'line':line,'class':label,'adjudication':'scanner_definition' if definition else 'unresolved'})
 assert not security,security
 assert not any(p['adjudication']=='unresolved' for p in privacy),privacy
 rows=read(root/'x1/new-proposals.json')['proposals'];correction=read(root/'x1/addendum/ordered-species-correction.json');rows=[correction['corrected_definition'] if r['proposal_id']=='MV6884-N195' else r for r in rows];definitions={r['proposal_id']:r for r in rows}
 assert len(rows)==len(definitions)==200 and read(root/'x1/new-proposals.json')['chain_after']==16230
 results=read(root/'x2/contract-results.json');assert len(results['results'])==200
 for row in results['results']:
  definition=definitions[row['proposal_id']]
  assert row['definition_sha256']==sha(canonical(definition))
  assert row['matched'] and row['input_unchanged']
  assert core.typed_equal(row['input'],definition['input']) and core.typed_equal(row['observed'],definition['expected_output'])
  assert row['outcome']==definition['expected_execution_disposition']
 assert len(results['ordered_correction_adverse'])==5 and all(r['matched'] for r in results['ordered_correction_adverse'])
 portfolio=read(root/'x2/portfolio-results.json')
 assert len(portfolio['safe_now'])==300 and all(r['passed'] for r in portfolio['safe_now'])
 assert len(portfolio['candidates'])==250 and all(r['candidate_rejected'] for r in portfolio['candidates'])
 assert len(portfolio['clean_fix_refine'])==300 and all(r['passed'] for r in portfolio['clean_fix_refine'])
 assert len(portfolio['exact_packets'])==50 and len(portfolio['blocked_packets'])==30
 assert all(not r['executed'] for r in portfolio['exact_packets']+portfolio['blocked_packets'])
 for candidate in portfolio['candidates']:
  if candidate['kind']=='altered_output':assert not core.typed_equal(candidate['observed']['altered_output'],definitions[candidate['proposal']]['expected_output'])
  else:
   try:core.strict_loads(candidate['observed']['mutated_json']);raise AssertionError('adverse JSON accepted')
   except core.Refusal as exc:assert str(exc)==candidate['observed']['expected_error']
 ledger=read(root/'x2/method-flow/ledger.json');methods=ledger['methods'];witnesses=ledger['witnesses'];mids={m['method_id'] for m in methods};wids={w['witness_id'] for w in witnesses}
 assert len(mids)==len(methods)==ledger['counts']['methods'] and len(wids)==len(witnesses)
 assert all(w['method_id'] in mids and not w['independent_reproduction'] for w in witnesses)
 for m in methods:
  assert set(m['validation_witness_ids'])<=wids and m['retained_negative_ids']
  assert any(w['result']=='pass' and w['method_id']==m['method_id'] for w in witnesses)
 counts=collections.Counter(w['result'] for w in witnesses);assert dict(counts)==ledger['counts']['witness_results']
 assert counts['fail']>=395 and counts['pass']>=670
 register=read(root/'x2/retained-negative-register.json');assert len(register['owner_failed_witnesses'])==len(set(register['owner_failed_witnesses']))==counts['fail']
 outcomes=dict(collections.Counter(r['outcome'] for r in results['results']));assert outcomes=={'completed':165,'represented':26,'open_gap':3,'exact_gate':6}
 truth=read(root/'x2/phase-truth.json');assert truth['outcomes']==outcomes and truth['terminal_verdict']=='NOT_READY_FOR_STAGE_20'
 expected_effective={'proposals':16230,'negatives':83455+counts['fail'],'methods':93450+len(methods),'failed_witnesses':54303+counts['fail'],'passing_witnesses':84881+counts['pass'],'open_gaps':752+outcomes['open_gap'],'exact_gates':753+outcomes['exact_gate']}
 assert truth['effective_counts']==register['effective_counts']==expected_effective
 deck=root/'x2/deck';index=read(deck/'deck-index.json');cards=[read(p) for p in (deck/'cards').glob('*.json')];by_card={c['card_id']:c for c in cards};assert len(by_card)==len(cards)==index['card_count']==208+len(methods)
 assert set(index['order'])==set(by_card)
 for c in cards:
  value=dict(c);identifier=value.pop('card_id');assert identifier=='ghc-card-'+sha(canonical(value))[:24]
  if c['tier']==1:assert c['parent_ids']==[]
  else:
   assert len(c['parent_ids'])==1;parent=by_card[c['parent_ids'][0]];assert parent['tier']==c['tier']-1
  assert c['outcome'] in {'completed','represented','open_gap','exact_gate'}
  for ref in c['source_refs']:assert (root/ref).is_file()
 card_manifest=read(deck/'card-manifest.json')
 for entry in card_manifest['entries']:
  value=(repo/entry['path']).read_bytes();assert len(value)==entry['bytes'] and sha(value)==entry['sha256']
 assert card_manifest['entry_count']==len(card_manifest['entries'])==len(cards)+6
 assert all(read(root/'x2'/p)['all_matched'] for p in ['skill-use.json','runner-use.json'])
 promotion=read(root/'x2/promotion-receipt.json');assert promotion['skills_promoted']==10 and promotion['runners_promoted']==5 and promotion['parity_files']==96 and promotion['overwrites']==0
 for entry in promotion['files']:
  source=repo/entry['source'];target=entry['global_target']
  if target.startswith('family-current-runners/'):destination=args.global_runners/target.split('/',1)[1]
  else:destination=args.global_skills/target
  data=source.read_bytes();assert data==destination.read_bytes() and sha(data)==entry['sha256_raw_bytes']
 package=read(root/'x2/package-installation.json');expected_packages={p['name']:p['version'] for p in read(root/'x1/package-plan.json')['packages']}
 assert package['installed_distributions']==expected_packages and package['direct_additions']==3 and package['dependency_distributions']==2
 actual=json.loads(subprocess.check_output([str(args.environment/'Scripts/python.exe'),'-c','import importlib.metadata as m,json;print(json.dumps({d.metadata["Name"].lower():d.version for d in m.distributions()}))'],text=True))
 assert actual==expected_packages
 assert len(read(root/'x2/package-smokes.json')['smokes'])==3
 assert all(r['positive_passed'] and r['adverse_rejected'] for r in read(root/'x2/package-smokes.json')['smokes'])
 assert read(root/'x2/package-audit.json')['known_advisories']==0
 test_receipt=read(root/'x2/validation/owner-test-receipt.json');assert test_receipt['tests_passed']==28 and test_receipt['tests_failed']==0
 manifest_specs=[(INITIAL_X1,'validation/x1-manifest.json'),(X1,'x1/addendum/manifest.json')]
 if args.stage=='final':manifest_specs.extend([(args.evidence,'x2/validation/evidence-manifest.json'),(head,'validation/final-delta-manifest.json'),(head,'validation/final-owner-manifest.json')])
 manifest_results=[]
 for ref,relative in manifest_specs:
  manifest=json.loads(git('show',ref+':'+PREFIX+relative));assert manifest['entry_count']==len(manifest['entries'])
  specs=[ref+':'+e['path'] for e in manifest['entries']]
  raw=subprocess.run(['git','--no-optional-locks','-C',str(repo),'cat-file','--batch'],input=('\n'.join(specs)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout;offset=0
  for entry in manifest['entries']:
   end=raw.index(b'\n',offset);header=raw[offset:end].split();assert header[1]==b'blob';size=int(header[2]);data=raw[end+1:end+1+size].replace(b'\r\n',b'\n');offset=end+size+2
   assert sha(data)==entry['sha256_normalized_lf'] and len(data)==entry['bytes_normalized_lf']
   if ref in {INITIAL_X1,X1}:assert (repo/entry['path']).read_bytes().replace(b'\r\n',b'\n')==data
  assert offset==len(raw)
  manifest_results.append({'manifest':PREFIX+relative,'anchor':ref,'bindings':len(specs),'self_exclusions':manifest['declared_self_exclusions']})
 tests_passed=28;test_log_sha=None;seal_targets=0;baton=None
 if args.stage=='final':
  changed=g('diff','--name-status',SOURCE,head).splitlines();assert len(changed)==len(owned) and all(line.startswith('A\t'+PREFIX) for line in changed)
  assert int(g('rev-list','--count',SOURCE+'..HEAD'))==4
  seal=read(root/'final/content-seal.json')
  for target in seal['targets']:
   data=git('show',head+':'+target['path']);assert sha(data)==target['sha256'] and len(data)==target['bytes']
  seal_targets=len(seal['targets']);baton=read(root/'final/baton-index.json');data=git('show',head+':'+baton['path']);assert sha(data)==baton['sha256'] and 10000<=len(data.decode().split())<=100000 and data.decode().rstrip().endswith(baton['eof'])
  assert len(re.findall(r'^## Module ',data.decode(),re.M))==13
  final_truth=read(root/'final/phase-truth.json');assert final_truth['evidence']==args.evidence and final_truth['x1']==X1 and final_truth['effective_counts']==expected_effective
  if args.run_tests or args.canonical:
   run=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(root/'tests'),'-p','test_reaction_contracts.py','-v'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=None)
   assert run.returncode==0 and b'Ran 28 tests' in run.stdout and b'OK' in run.stdout
   test_log_sha=sha(run.stdout)
   if args.canonical:(args.bank/'owner-tests.log').write_bytes(run.stdout)
 after=remote() if args.stage=='final' else None
 return {'schema':'ghc.family.reaction-owner-audit.v1','status':'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if args.canonical else 'VALID_OWNER_'+args.stage.upper()+'_PREFLIGHT','owner':'Merrin Vale','phase':'v688-v4','source':SOURCE,'initial_x1':INITIAL_X1,'x1':X1,'evidence':args.evidence,'exact_final':head if args.stage=='final' else None,'branch':BRANCH,'phase_commits':4 if args.stage=='final' else 2,'merge_commits':0,'owner_files':len(owned),'strict_json':len(parsed),'python_ast':ast_count,'largest_document_words':largest_words,'privacy_classes':list(PRIVATE_PATTERNS),'privacy_candidates':privacy,'confirmed_privacy_hits':0,'bounded_security_findings':security,'tests_passed':tests_passed,'test_log_sha256':test_log_sha,'complete_contracts':200,'outcomes':outcomes,'safe_procedures':300,'candidate_rejections':250,'cfr_procedures':300,'method_flow':ledger['counts'],'effective_counts':expected_effective,'deck_cards':len(cards),'deck_manifest_entries':len(card_manifest['entries']),'promotion_parity_files':96,'distributions':actual,'manifests':manifest_results,'manifest_bindings':sum(m['bindings'] for m in manifest_results),'content_seal_targets':seal_targets,'baton':baton,'remote_before':before,'remote_after':after,'canonical_invocation_count':1 if args.canonical else 0,'canonical_success_count':1 if args.canonical else 0,'canonical_replay_count':0,'route_state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED','same_owner_only':True,'independent_reproduction':False,'full_repository_suite':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--stage',choices=['evidence','final'],required=True);parser.add_argument('--evidence');parser.add_argument('--environment',type=Path,required=True);parser.add_argument('--global-skills',type=Path,required=True);parser.add_argument('--global-runners',type=Path,required=True);parser.add_argument('--output',type=Path);parser.add_argument('--bank',type=Path);parser.add_argument('--canonical',action='store_true');parser.add_argument('--run-tests',action='store_true')
 args=parser.parse_args()
 if args.canonical:
  assert args.stage=='final' and args.bank is not None
  args.bank.mkdir(parents=True,exist_ok=True)
  marker=args.bank/'invocation.json';receipt=args.bank/'exact-final-owner-scoped-canonical.json'
  assert not marker.exists() and not receipt.exists(),'CANONICAL_LATCH_EXISTS_NO_REPLAY'
  write(marker,{'owner':'Merrin Vale','phase':'v688-v4','invocations':1,'replay_permitted':False})
 payload=audit(args)
 if args.canonical:
  write(receipt,{'payload':payload,'payload_sha256':sha(canonical(payload))})
  print(json.dumps({'status':payload['status'],'exact_final':payload['exact_final'],'receipt_sha256':sha(receipt.read_bytes()),'payload_sha256':sha(canonical(payload)),'tests':payload['tests_passed'],'manifest_bindings':payload['manifest_bindings'],'canonical_replays':0}))
 else:
  if args.output:write(args.output,payload)
  print(json.dumps({k:payload[k] for k in ['status','owner_files','strict_json','python_ast','largest_document_words','confirmed_privacy_hits','manifest_bindings','deck_cards']}))

if __name__=='__main__':main()
