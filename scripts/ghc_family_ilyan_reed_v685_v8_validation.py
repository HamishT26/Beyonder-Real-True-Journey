"""Bounded owner artifact checks shared by preflight and one final latch."""
from __future__ import annotations
import ast,hashlib,json,re,subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v685-v8';SOURCE='f5464f56d095e9c691707f669668b86ff70468a6';X1='ae33e7fd357e38c464677c10538a50f069b68353'
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((BASE/n).read_text(encoding='utf8'))
def owner_files():
    return sorted([*filter(Path.is_file,BASE.rglob('*')),*ROOT.glob('scripts/*ilyan_reed_v685_v8*.py'),*ROOT.glob('scripts/ghc_family_protocol_*.py'),*ROOT.glob('tests/*ilyan_reed_v685_v8*.py')])
def rel(p):return p.relative_to(ROOT).as_posix()
def blob_batch(refs):
    if not refs:return []
    raw=subprocess.check_output(['git','-C',str(ROOT),'cat-file','--batch'],input=('\n'.join(refs)+'\n').encode())
    result=[];pos=0
    for ref in refs:
        end=raw.index(b'\n',pos);head=raw[pos:end].split()
        if len(head)!=3:raise ValueError('Missing declared blob '+ref)
        n=int(head[2]);result.append(raw[end+1:end+1+n]);pos=end+n+2
    return result
def replay_manifest(path,revision=None):
    m=json.loads((ROOT/path).read_text(encoding='utf8'));entries=m['entries'];paths=[e['path'] for e in entries]
    if len(paths)!=len(set(paths)):return {'valid':False,'error':'duplicate_paths'}
    blobs=blob_batch([revision+':'+p for p in paths]) if revision else [(ROOT/p).read_bytes() for p in paths]
    bad=[e['path'] for e,b in zip(entries,blobs) if len(b)!=e['bytes'] or digest(b)!=e['sha256']]
    return {'valid':not bad,'entries':len(entries),'failures':bad}
class StructuralHTML(HTMLParser):
    def __init__(self):super().__init__();self.tags=Counter();self.lang=False;self.headers=True
    def handle_starttag(self,tag,attrs):
        self.tags[tag]+=1;d=dict(attrs)
        if tag=='html':self.lang=bool(d.get('lang'))
        if tag=='th' and d.get('scope') not in ['row','col']:self.headers=False
def tree_checks(paths=None):
    paths=paths or owner_files();counts=Counter();failures=[];privacy=[];security=[]
    patterns={'local_path':r'(?i)\b[CD]:[\\/](?:Users|GHC-Archives)[\\/]','private_uuid':r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b','private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','credential':r'\bsk-[A-Za-z0-9]{20,}\b','callable_route':r'(?i)"(?:thread_id|threadId|session_id|providerTabId)"\s*:\s*"[^"\n]+"'}
    for p in paths:
        counts['owner_files']+=1
        if p.suffix=='.pdf':counts['pdf']+=1;continue
        b=p.read_bytes();t=b.decode('utf8');name=rel(p)
        if b'\r\n' in b:failures.append([name,'not_lf'])
        for kind,pat in patterns.items():
            for match in re.finditer(pat,t):privacy.append({'path':name,'class':kind,'offset':match.start(),'length':len(match.group())})
        try:
            if p.suffix=='.json':json.loads(t);counts['json']+=1
            elif p.suffix=='.py':
                tree=ast.parse(t);counts['python_ast']+=1
                for n in ast.walk(tree):
                    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['eval','exec']:security.append([name,n.lineno,n.func.id])
            elif p.suffix in ['.yaml','.yml']:
                if not isinstance(yaml.safe_load(t),dict):raise ValueError('YAML mapping required')
                counts['yaml']+=1
            elif p.suffix=='.md':
                body=t
                if t.startswith('---\n'):
                    end=t.find('\n---\n',4)
                    if end<0:raise ValueError('Unclosed YAML frontmatter')
                    front=yaml.safe_load(t[4:end])
                    if not isinstance(front,dict) or not front.get('name') or not front.get('description'):raise ValueError('Missing frontmatter identity')
                    body=t[end+5:]
                if not re.search(r'(?m)^#{1,6} ',body):raise ValueError('Missing Markdown heading')
                counts['markdown']+=1
            elif p.suffix=='.html':
                h=StructuralHTML();h.feed(t)
                if not(h.lang and h.tags['main'] and h.tags['h1'] and h.headers and h.tags['caption']):raise ValueError('HTML structural relation')
                counts['html']+=1
        except Exception as e:failures.append([name,type(e).__name__,str(e)])
    return {'counts':dict(counts),'structure_failures':failures,'privacy_candidates':privacy,'security_findings':security,'structure_valid':not failures,'privacy_confirmed_hits':len(privacy),'bounded_security_findings':len(security),'privacy_classes':list(patterns)}
def deck_check():
    directory=BASE/'x2/flashcards/cards';cards=[json.loads(p.read_text(encoding='utf8')) for p in sorted(directory.glob('*.json'))];by={c['card_id']:c for c in cards};bad=[]
    for c in cards:
        payload={k:v for k,v in c.items() if k!='card_id'}
        if 'ghc-card-'+digest(canonical(payload))[:24]!=c['card_id']:bad.append([c['card_id'],'digest'])
        parents=c['parent_ids']
        if c['tier']==1:
            if parents:bad.append([c['card_id'],'root_parent'])
        elif len(parents)!=1 or parents[0] not in by or by[parents[0]]['tier']!=c['tier']-1:bad.append([c['card_id'],'tier_parent'])
        if c['outcome'] not in ['completed','represented','open_gap','exact_gate']:bad.append([c['card_id'],'outcome'])
    return {'valid':not bad and len(by)==len(cards)==210,'cards':len(cards),'failures':bad}
def method_check():
    d=read('x2/method-flow.json');methods=d['methods'];witnesses=d['witnesses'];by={m['method_id']:m for m in methods};wi={w['witness_id']:w for w in witnesses};neg=set(n for w in witnesses if w['result']=='fail' for n in w['retained_negative_ids']);bad=[]
    for m in methods:
        if not m['retained_negative_ids'] or not set(m['retained_negative_ids'])<=neg:bad.append([m['method_id'],'negative_links'])
        if not all(x in wi for x in m['validation_witness_ids']):bad.append([m['method_id'],'witness_links'])
        if not any(wi[x]['result']=='pass' for x in m['validation_witness_ids']):bad.append([m['method_id'],'unvalidated'])
    actual={'methods':len(methods),'failed_witnesses':sum(w['result']=='fail' for w in witnesses),'bounded_passing_witnesses':sum(w['result']=='pass' for w in witnesses),'retained_negatives':len(neg)}
    return {'valid':not bad and actual==d['counts'],'counts':actual,'failures':bad}
def equality():
    branch='codex/GHC-Family/ilyan-reed-v685-v8-full-tools';head=git('rev-parse','HEAD').decode().strip();up=git('rev-parse','@{upstream}').decode().strip();tracking=git('rev-parse','refs/remotes/origin/'+branch).decode().strip();live=git('ls-remote','--exit-code','origin','refs/heads/'+branch).decode().split()[0]
    return {'head':head,'upstream':up,'tracking':tracking,'live':live,'four_way_equal':len({head,up,tracking,live})==1,'clean':not git('status','--porcelain').strip(),'divergence':git('rev-list','--left-right','--count','HEAD...@{upstream}').decode().strip(),'branch':git('branch','--show-current').decode().strip()}
