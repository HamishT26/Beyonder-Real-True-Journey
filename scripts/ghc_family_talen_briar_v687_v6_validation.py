"""Bounded owner lifecycle utilities; no source-owner tests or canonical replay."""
import ast,collections,hashlib,io,json,math,os,pathlib,re,subprocess,sys
REPO=pathlib.Path(__file__).resolve().parents[1]
ROOT='docs/talen-briar/v687-v6/'
SOURCE='f815c68a704065970717f8d88305489a0966cd9c'
BRANCH='codex/GHC-Family/talen-briar-v687-v6-full-tools'
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.replace(b'\r\n',b'\n')
def pairs(ps):
 d={}
 for k,v in ps:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def nonfinite(v):raise ValueError('nonfinite JSON value')
def finite(v):
 n=float(v)
 if not math.isfinite(n):nonfinite(v)
 return n
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=finite)
def read(p):return parse((REPO/p).read_bytes())
def put(p,d,exclusive=False):
 f=REPO/p;f.parent.mkdir(parents=True,exist_ok=True)
 mode='x' if exclusive else 'w'
 with f.open(mode,encoding='utf-8',newline='\n') as h:
  h.write(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n' if not isinstance(d,str) else d)
def owned(p):
 return p.startswith(ROOT) or p.startswith('tests/test_ghc_family_talen_briar_v687_v6_') or p.startswith('scripts/ghc_family_talen_briar_v687_v6_') or p in ['scripts/ghc_family_'+x+'.py' for x in ['cif_category_cardinality','symmetry_code_literal_boundary','reflection_merge_provenance','detector_distance_uncertainty','deposition_rollback_readback']]
def paths():
 a=set(git('diff','--name-only',SOURCE).decode().splitlines())
 a.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
 assert all(owned(p) for p in a),'Out-of-owner path'
 assert all((REPO/p).is_file() for p in a),'Removed or nonfile path'
 return sorted(a)
def scan(items):
 patterns={
  'raw_identifiers':r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b',
  'private_routes':r'(?:codex://|app://|"(?:thread_id|task_id|session_id|agent_id)"\s*:)',
  'credentials':r'(?:sk-[A-Za-z0-9]{24,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',
  'private_absolute_paths':r'(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/[^ ]+/|\\\\[A-Za-z0-9]+\\)',
  'private_streams':r'(?m)^\s*\{\s*"(?:session_meta|response_item|turn_context)"\s*:'}
 candidates=[];count=0
 for p,b in items.items():
  s=b.decode('utf-8');count+=1
  definition_lines=set()
  if p.endswith('.py'):
   for node in ast.walk(ast.parse(s)):
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id.lower().endswith('patterns') for t in node.targets):
     definition_lines.update(range(node.lineno,node.end_lineno+1))
  for k,pat in patterns.items():
   for m in re.finditer(pat,s):
    # Definitions are reviewed as code, not emitted private payload.
    line=s[:m.start()].count('\n')+1
    definition=line in definition_lines
    candidates.append(dict(path=p,line=line,privacy_class=k,adjudication='scanner_definition' if definition else 'confirmed_payload',matched_text_sha256=sha(m.group().encode())))
 return dict(classes=list(patterns),files_scanned=count,candidates=candidates,confirmed=sum(x['adjudication']=='confirmed_payload' for x in candidates),complete_privacy=False)
def security(items):
 findings=[];parsed=0
 for p,b in items.items():
  if not p.endswith('.py'):continue
  tree=ast.parse(b.decode('utf-8'));parsed+=1
  for n in ast.walk(tree):
   if isinstance(n,ast.Call):
    name=ast.unparse(n.func)
    if name in ['eval','exec','os.system','pickle.loads','yaml.load']:
     findings.append(dict(path=p,line=n.lineno,reason='unsafe_dynamic_execution',call=name))
    if any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords):
     findings.append(dict(path=p,line=n.lineno,reason='shell_true'))
 return dict(python_files=parsed,findings=findings,exhaustive_security=False)
def manifest(output,selection):
 entries=[dict(path=p,bytes_normalized_lf=len(norm((REPO/p).read_bytes())),sha256_normalized_lf=sha(norm((REPO/p).read_bytes()))) for p in sorted(selection) if p!=output]
 put(output,dict(schema='ghc.family.talen-manifest.v1',byte_domain='normalized_lf_git_blob',source=SOURCE,entries=entries,self_exclusions=[output]))
def git_blobs(refs):
 run=subprocess.run(['git','-C',str(REPO),'cat-file','--batch'],input=('\n'.join(refs)+'\n').encode(),capture_output=True,check=True,timeout=60)
 out=io.BytesIO(run.stdout);data={}
 for ref in refs:
  hdr=out.readline().split();assert len(hdr)==3,(ref,hdr)
  b=out.read(int(hdr[2]));assert out.read(1)==b'\n';data[ref]=b
 return data
def replay(anchor,mpath):
 m=parse(git('show',anchor+':'+mpath));refs=[anchor+':'+r['path'] for r in m['entries']];data=git_blobs(refs);bad=[]
 for row,ref in zip(m['entries'],refs):
  b=norm(data[ref])
  if sha(b)!=row['sha256_normalized_lf'] or len(b)!=row['bytes_normalized_lf']:bad.append(row['path'])
 assert not bad,bad
 return dict(anchor=anchor,manifest=mpath,entries=len(refs),mismatches=bad,self_exclusions=m['self_exclusions'])
def remote(expected=None):
 branch=git('branch','--show-current').decode().strip();assert branch==BRANCH
 head=git('rev-parse','HEAD').decode().strip()
 if expected:assert head==expected
 up=git('rev-parse','@{upstream}').decode().strip();track=git('rev-parse','refs/remotes/origin/'+BRANCH).decode().strip()
 live=git('ls-remote','--exit-code','origin','refs/heads/'+BRANCH).decode().split()[0]
 div=[int(x) for x in git('rev-list','--left-right','--count','HEAD...@{upstream}').split()]
 assert div==[0,0] and head==up==track==live
 assert not git('status','--porcelain=v1').strip()
 return dict(branch=branch,local=head,upstream=up,tracking=track,fresh_live=live,divergence=div,clean=True)
