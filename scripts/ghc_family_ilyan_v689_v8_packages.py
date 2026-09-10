"""Install the frozen three-package wheel transaction in an owner-isolated D root."""
import argparse,hashlib,json,os,subprocess,sys,urllib.request,zipfile
from pathlib import Path
from ghc_family_ilyan_v689_v8_io import BASE,read,write,sha
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--env',required=True);ap.add_argument('--wheels',required=True);ap.add_argument('--cache',required=True);a=ap.parse_args();envroot=Path(a.env).resolve();wheels=Path(a.wheels).resolve();cache=Path(a.cache).resolve()
    for p in [envroot,wheels,cache]:
        if p.drive.upper()!='D:' or 'ilyan-reed-v689-v8' not in str(p):raise ValueError('Owner-attributed D path required')
    if envroot.exists() or wheels.exists():raise FileExistsError('Inspect existing transaction state; do not replay')
    wheels.mkdir(parents=True);cache.mkdir(parents=True,exist_ok=True);rows=read('plan/package-plan.json')['packages'];inventory=[]
    for r in rows:
        b=urllib.request.urlopen(r['url'],timeout=30).read()
        if sha(b)!=r['sha256']:raise ValueError('Wheel digest mismatch')
        p=wheels/r['filename'];p.write_bytes(b)
        with zipfile.ZipFile(p) as z:
            members=z.namelist()
            if any(n.startswith(('/','\\')) or '..' in n.split('/') or ':' in n for n in members):raise ValueError('Unsafe archive member')
        inventory.append({'name':r['name'],'version':r['version'],'filename':r['filename'],'sha256':r['sha256'],'members':len(members)})
    write('x1/toolchain/wheels.json',{'wheels':inventory,'direct_packages':3,'bootstrap':1})
    lock=BASE/'x1/toolchain/requirements.lock';lock.write_text(''.join(r['name']+'=='+r['version']+' --hash=sha256:'+r['sha256']+'\n' for r in rows),encoding='utf8',newline='\n')
    subprocess.run([sys.executable,'-m','venv','--without-pip',str(envroot)],check=True);py=envroot/'Scripts/python.exe';env=os.environ.copy();env.update(PYTHONPATH=str(wheels/next(r['filename'] for r in rows if r['name']=='pip')),PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PIP_CACHE_DIR=str(cache),PIP_DISABLE_PIP_VERSION_CHECK='1')
    r=subprocess.run([str(py),'-m','pip','install','--no-index','--find-links',str(wheels),'--require-hashes','--no-compile','-r',str(lock)],env=env,capture_output=True,text=True);write('x1/toolchain/install-result.json',{'exit_code':r.returncode,'output_sha256':sha((r.stdout+r.stderr).encode()),'system_python_mutated':False})
    if r.returncode:raise RuntimeError('Installation failed; inspect retained transaction')
    env.pop('PYTHONPATH');check=subprocess.run([str(py),'-m','pip','check'],env=env,capture_output=True,text=True);installed=json.loads(subprocess.check_output([str(py),'-m','pip','list','--format=json'],env=env));write('x1/toolchain/installed.json',{'packages':installed,'pip_check':check.stdout.strip(),'pip_check_exit_code':check.returncode,'rollback_token':'IR6898-TOOLS-01'})
    if check.returncode:raise RuntimeError('Dependency check failed')
    queries=[{'package':{'name':r['name'],'ecosystem':'PyPI'},'version':r['version']} for r in rows];req=urllib.request.Request('https://api.osv.dev/v1/querybatch',data=json.dumps({'queries':queries}).encode(),headers={'Content-Type':'application/json'});response=json.load(urllib.request.urlopen(req,timeout=45));findings=sum(len(x.get('vulns',[])) for x in response['results']);write('x1/toolchain/advisory.json',{'queries':queries,'response':response,'finding_rows':findings,'date':'2026-09-10','boundary':'Dated advisory snapshot, not exhaustive security or endorsement.'});print(json.dumps({'distributions':len(installed),'direct':3,'pip_check':check.returncode,'advisories':findings}))
if __name__=='__main__':main()
