"""Owner-only exact-byte artifact and lifecycle utilities."""
from __future__ import annotations
import ast,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v689-v8';SOURCE='497225ad1af5f6b46ed8353bc0445d4d592e1981';BRANCH='codex/GHC-Family/ilyan-reed-main'
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((BASE/p).read_text(encoding='utf8'))
def write(p,x):
    p=BASE/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def text(p,x):
    p=BASE/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(x)
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def rel(p):return p.relative_to(ROOT).as_posix()
def files():
    return sorted(p for directory in [BASE,ROOT/'scripts',ROOT/'tests'] if directory.exists() for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
def batch(refs):
    if not refs:return []
    raw=subprocess.check_output(['git','-C',str(ROOT),'cat-file','--batch'],input=('\n'.join(refs)+'\n').encode());out=[];pos=0
    for ref in refs:
        end=raw.index(b'\n',pos);parts=raw[pos:end].split()
        if len(parts)!=3:raise ValueError('Missing explicit blob '+ref)
        size=int(parts[2]);out.append(raw[end+1:end+1+size]);pos=end+size+2
    return out
def inspect(paths):
    counts={};hits=[];bad=[]
    patterns={'private_uuid':r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b','local_private_path':r'(?i)[CD]:[\\/](?:Users|GHC-Archives)[\\/]','private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','credential':r'\bsk-[A-Za-z0-9]{20,}\b','private_route':r'"(?:threadId|thread_id|session_id|providerTabId)"\s*:\s*"[^"\n]+"'}
    for p in paths:
        ext=p.suffix.lower();counts[ext]=counts.get(ext,0)+1
        if ext in ['.png','.jpg','.pdf']:continue
        b=p.read_bytes();s=b.decode('utf8')
        if b'\r\n' in b:bad.append([rel(p),'unexpected_crlf'])
        for name,pat in patterns.items():
            if re.search(pat,s):hits.append({'path':rel(p),'class':name})
        if ext=='.json':json.loads(s)
        if ext=='.py':
            tree=ast.parse(s)
            for n in ast.walk(tree):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['eval','exec']:bad.append([rel(p),'dynamic_evaluation'])
        if ext=='.md' and not re.search(r'^#{1,6} ',s,re.M):bad.append([rel(p),'missing_heading'])
    return {'counts':counts,'privacy_candidates':hits,'format_or_security_findings':bad,'valid':not hits and not bad,'privacy_scope':'five declared classes on exact owner text files','security_scope':'AST syntax and direct dynamic-evaluation calls; not exhaustive security'}
def equality():
    h=git('rev-parse','HEAD').decode().strip();u=git('rev-parse','@{upstream}').decode().strip();t=git('rev-parse','refs/remotes/origin/'+BRANCH).decode().strip();l=git('ls-remote','--exit-code','origin','refs/heads/'+BRANCH).decode().split()[0]
    return {'head':h,'upstream':u,'tracking':t,'live':l,'four_way_equal':len({h,u,t,l})==1,'clean':not git('status','--porcelain').strip(),'divergence':git('rev-list','--left-right','--count','HEAD...@{upstream}').decode().strip()}
def stage(phase,tests,root_commit=False):
    current=files();tracked=set(git('ls-files').decode().splitlines());new=[p for p in current if rel(p) not in tracked]
    if tracked and git('diff','--name-only').strip():raise ValueError('An immutable earlier file changed')
    review=inspect(new)
    if not review['valid']:raise ValueError(json.dumps(review))
    write(phase+'/preflight.json',{**review,'tests':tests,'canonical_invoked':False,'source':SOURCE})
    new=[p for p in files() if rel(p) not in tracked]
    mp=BASE/phase/'manifest.json';ap=BASE/phase/'allowlist.json';paths=sorted([rel(p) for p in new]+[rel(mp),rel(ap)])
    write(phase+'/allowlist.json',{'paths':paths,'change_type':'A','earlier_files_immutable':True})
    new.append(ap);entries=[{'path':rel(p),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(new)]
    write(phase+'/manifest.json',{'schema':'ghc.family.raw-git-manifest.v1','hash_domain':'exact Git blob bytes, no binary normalization','entries':entries,'self_exclusions':[rel(mp)]})
    if len(files())>=2000:raise ValueError('Owner file ceiling reached')
    spec=BASE/phase/'allowlist.json'
    # stdin pathspec is an exact NUL-separated list, avoiding Windows argument limits.
    subprocess.run(['git','-C',str(ROOT),'add','--sparse','--pathspec-from-file=-','--pathspec-file-nul'],input=b'\0'.join(x.encode() for x in paths)+b'\0',check=True)
    staged=git('diff','--cached','--name-status').decode().splitlines()
    if sorted(x[2:] for x in staged)!=paths or any(not x.startswith('A\t') for x in staged):raise ValueError('Staged allowlist mismatch')
    blobs=batch([':'+x['path'] for x in entries])
    if any(len(b)!=e['bytes'] or sha(b)!=e['sha256'] for b,e in zip(blobs,entries)):raise ValueError('Git blob byte mismatch')
    return {'additions':len(paths),'manifest_entries':len(entries),'owner_files':len(files())}
