"""Narrow owner manifests and five-class text scans; no whole-repository walk."""
import argparse,ast,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/mira-fenwick/v690-v3'
TEXT={'.py','.json','.md','.yaml','.yml','.html','.svg','.txt','.lock'}
def strict_json(text):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate JSON field')
            result[key]=value
        return result
    def constant(_):raise ValueError('Nonfinite JSON value')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=constant)
def owner_files():
    paths=[ROOT/'.gitattributes',ROOT/'.gitignore']
    for folder in [ROOT/'scripts',ROOT/'tests',ROOT/'workflow',BASE]:
        if folder.exists():paths += [p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    return sorted(set(paths))

def privacy_patterns():
    return {
      'local_profile_path':re.compile(r'(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]|/(?:home|Users)/)'),
      'email_address':re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}'),
      'network_address':re.compile(r'(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])'),
      'credential_like_secret':re.compile(r'(?:gh'+'p_|gl'+'pat-|sk-'+'proj-)[A-Za-z0-9_-]{16,}'),
      'contact_phone':re.compile(r'(?i)(?:phone|mobile|tel)\s*[:=]\s*[\x22\x27]?\+?[0-9][0-9 ()-]{6,}')}

def scan(paths):
    counts={k:0 for k in privacy_patterns()};hits=[];extra=[];parsed={'json':0,'yaml':0,'python_ast':0,'text_files':0};security=[]
    for path in paths:
        if path.suffix not in TEXT and path.name not in ('.gitignore','.gitattributes'):continue
        data=path.read_bytes();text=data.decode('utf-8');parsed['text_files']+=1
        if b'\r\n' in data:raise ValueError('Unexpected current CRLF text: '+path.relative_to(ROOT).as_posix())
        for label,pattern in privacy_patterns().items():
            for match in pattern.finditer(text):
                counts[label]+=1;hits.append({'path':path.relative_to(ROOT).as_posix(),'class':label,'offset':match.start()})
        if re.search(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',text):extra.append(path.relative_to(ROOT).as_posix())
        if path.suffix=='.json':strict_json(text);parsed['json']+=1
        if path.suffix in ('.yaml','.yml'):
            import yaml
            yaml.safe_load(text);parsed['yaml']+=1
        if path.suffix=='.py':
            tree=ast.parse(text);parsed['python_ast']+=1
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ('eval','exec'):security.append(path.relative_to(ROOT).as_posix())
                if isinstance(node,ast.keyword) and node.arg=='shell' and isinstance(node.value,ast.Constant) and node.value.value is True:security.append(path.relative_to(ROOT).as_posix())
    return {'privacy_classes':counts,'privacy_candidates':hits,'private_route_identifier_candidates':extra,'bounded_code_execution_findings':security,'parsed':parsed,
            'scope':'Only explicit owner roots; patterns and AST checks do not establish complete privacy, accessibility, or exhaustive security.'}

def git_blobs(commit,paths):
    refs=[(commit+':'+p) if commit!='INDEX' else ':'+p for p in paths]
    raw=subprocess.check_output(['git','-C',str(ROOT),'cat-file','--batch'],input=('\n'.join(refs)+'\n').encode());pos=0;result={}
    for path in paths:
        end=raw.index(b'\n',pos);header=raw[pos:end].split()
        if len(header)!=3 or header[1]!=b'blob':raise ValueError('Missing exact blob: '+path)
        size=int(header[2]);result[path]=raw[end+1:end+1+size];pos=end+size+2
    if pos!=len(raw):raise ValueError('Unexpected batch trailing bytes')
    return result

def manifest_entries(paths):
    return [{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['x1','x2'],required=True);parser.add_argument('--before',required=True);args=parser.parse_args()
    folder=BASE/args.phase;audit=scan(owner_files());assert not audit['privacy_candidates'] and not audit['private_route_identifier_candidates'] and not audit['bounded_code_execution_findings'],audit
    with (folder/'structural-audit.json').open('xb') as f:f.write((json.dumps(audit,sort_keys=True,indent=2)+'\n').encode())
    prior=set(subprocess.check_output(['git','-C',str(ROOT),'ls-tree','-r','--name-only',args.before]).decode().splitlines())
    paths=[p for p in owner_files() if p.relative_to(ROOT).as_posix() not in prior]
    m={'schema':'ghc.family.owner-manifest.v1','before':args.before,'hash_domain':'raw Git blob bytes; explicit LF text policy','self_excluded':f'docs/mira-fenwick/v690-v3/{args.phase}/manifest.json','entries':manifest_entries(paths)}
    with (folder/'manifest.json').open('xb') as f:f.write((json.dumps(m,sort_keys=True,indent=2)+'\n').encode())
    print(json.dumps({'phase':args.phase,'new_manifest_entries':len(paths),'owner_materialized_files':len(owner_files()),**audit['parsed'],'privacy_candidates':0,'bounded_security_findings':0}))

if __name__=='__main__':raise SystemExit(main())
