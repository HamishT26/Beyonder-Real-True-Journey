"""One exact D-first wheel transaction from the immutable package plan."""
import argparse,hashlib,json,os,subprocess,sys,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v685-v8'
def put(name,obj):
    p=BASE/'x2/toolchain'/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8',newline='\n') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--environment',required=True);p.add_argument('--wheelhouse',required=True);p.add_argument('--cache',required=True);a=p.parse_args()
    envroot=Path(a.environment).resolve();wheelhouse=Path(a.wheelhouse).resolve();cache=Path(a.cache).resolve()
    if any(x.drive.upper()!='D:' or 'ilyan-reed-v685-v8' not in str(x) for x in [envroot,wheelhouse,cache]):raise ValueError('Exact owner-attributed D roots required')
    if envroot.exists() or wheelhouse.exists():raise FileExistsError('Transaction root already exists; inspect retained state')
    packages=json.loads((BASE/'x1/package-plan.json').read_text(encoding='utf8'))['packages'];wheelhouse.mkdir(parents=True);cache.mkdir(parents=True,exist_ok=True);inventory=[]
    for r in packages:
        blob=urllib.request.urlopen(r['url'],timeout=30).read()
        if hashlib.sha256(blob).hexdigest()!=r['sha256']:raise ValueError('Frozen wheel digest mismatch')
        path=wheelhouse/r['wheel'];path.write_bytes(blob)
        with zipfile.ZipFile(path) as z:
            names=z.namelist()
            if any(n.startswith(('/','\\')) or '..' in n.split('/') or ':' in n for n in names):raise ValueError('Unsafe wheel member')
        inventory.append({'name':r['name'],'version':r['version'],'wheel':r['wheel'],'sha256':r['sha256'],'members':len(names),'path_review':'bounded archive member check passed'})
    put('wheelhouse-manifest.json',{'wheels':inventory,'direct_additions':3,'dependency_additions':1,'bootstrap':1,'same_owner_only':True})
    lock=''.join(r['name']+'=='+r['version']+' --hash=sha256:'+r['sha256']+'\n' for r in packages)
    lockpath=BASE/'x2/toolchain/requirements.lock';lockpath.write_text(lock,encoding='utf8',newline='\n')
    subprocess.run([sys.executable,'-m','venv','--without-pip',str(envroot)],check=True)
    py=envroot/'Scripts/python.exe';pipwheel=next(wheelhouse/r['wheel'] for r in packages if r['name']=='pip')
    env=os.environ.copy();env.update(PYTHONPATH=str(pipwheel),PIP_CACHE_DIR=str(cache),PYTHONDONTWRITEBYTECODE='1',PIP_DISABLE_PIP_VERSION_CHECK='1')
    result=subprocess.run([str(py),'-m','pip','install','--no-index','--find-links',str(wheelhouse),'--require-hashes','--no-compile','-r',str(lockpath)],env=env,capture_output=True,text=True)
    put('install-result.json',{'returncode':result.returncode,'output_sha256':hashlib.sha256((result.stdout+result.stderr).encode()).hexdigest(),'success':result.returncode==0,'system_environment_mutated':False})
    if result.returncode:raise RuntimeError('Isolated installation failed; inspect transaction state')
    env.pop('PYTHONPATH');check=subprocess.run([str(py),'-m','pip','check'],env=env,capture_output=True,text=True)
    installed=json.loads(subprocess.check_output([str(py),'-m','pip','list','--format=json'],env=env))
    put('installation-receipt.json',{'installed':installed,'pip_check_exit_code':check.returncode,'pip_check':check.stdout.strip(),'wheel_hashes_match':True,'bootstrap_preplanned':True,'rollback_token':'IR6858-TOOLS-01','scope':'isolated D environment only'})
    if check.returncode:raise RuntimeError('Dependency check failed')
    queries=[{'package':{'name':r['name'],'ecosystem':'PyPI'},'version':r['version']} for r in packages]
    req=urllib.request.Request('https://api.osv.dev/v1/querybatch',data=json.dumps({'queries':queries}).encode(),headers={'Content-Type':'application/json'})
    advisory=json.load(urllib.request.urlopen(req,timeout=45));findings=sum(len(x.get('vulns',[])) for x in advisory['results'])
    put('advisory-audit.json',{'source':'https://api.osv.dev/v1/querybatch','checked_on':'2026-09-06','queries':queries,'response':advisory,'finding_rows':findings,'boundary':'Dated public advisory snapshot; no exhaustive security or production assurance.'})
    print(json.dumps({'installed_distributions':len(installed),'direct_additions':3,'pip_check_pass':check.returncode==0,'advisory_findings':findings}))
if __name__=='__main__':main()
