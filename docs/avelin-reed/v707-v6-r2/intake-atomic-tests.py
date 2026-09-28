from pathlib import Path
import sys,json,subprocess,sqlite3,hashlib,importlib.util,time,os
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2];BANK=Path(r'D:\GHC-Archives\phase-banks\avelin-reed-v707-v6-r2');TEST=BANK/'intake-atomic-tests'
TEST.mkdir(exist_ok=False)
module_path=ROOT/'laboratory/intake_store.py';spec=importlib.util.spec_from_file_location('intake_store',module_path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
source='06f54492a7da636205b0e85184d2d2fa33286134';rel='docs/avelin-reed/v707-v6/x1.json';lane=r'D:\GHC-Archives\worktrees\avelin-reed-v707-v6-full-tools'
def git(p):return subprocess.check_output(['git','-C',lane,'show',source+':'+p])
blob=git(rel);manifest=git('docs/avelin-reed/v707-v6/manifest.json')
pin={'repository':'HamishT26/Beyonder-Real-True-Journey','commit':source,'path':rel,'contract_id':'AR7076-P001','blob_sha256':mod.sha(blob),'manifest_sha256':mod.sha(manifest),'result_sha256':'737552226711cf568b6d874473600266cd6f1f184104c6de18e5baa9c1892d33','original_outcome':'completed','lab_version_sha256':mod.sha(module_path.read_bytes())}
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
save(TEST/'pin.json',pin);(TEST/'source.json').write_bytes(blob);(TEST/'manifest.json').write_bytes(manifest)
request={k:pin[k] for k in ['repository','commit','path','contract_id']}
checks=[];negative=[];observations=[]
def check(name,value,detail=None):checks.append({'id':name,'pass':bool(value),'detail':detail})
def count(db):
 c=sqlite3.connect(db);r=c.execute('SELECT COUNT(*),COALESCE(SUM(domain_credit),0) FROM receipts').fetchone();c.close();return r
def config(db,**extra):return {'db':str(db),'pin':str(TEST/'pin.json'),'blob':str(TEST/'source.json'),'manifest':str(TEST/'manifest.json'),**extra}
def child(cfg):
 return subprocess.Popen([sys.executable,'-X','utf8','-B',str(module_path),'worker',str(cfg)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
db=TEST/'shared.sqlite';mod.initialize(db)
for round in [1,2]:
 barrier=TEST/f'barrier-{round}';cfg=TEST/f'round-{round}.json';save(cfg,config(db,barrier=str(barrier)))
 children=[child(cfg) for _ in range(30)];barrier.write_text('go',encoding='utf-8')
 results=[]
 for p in children:
  out,err=p.communicate(timeout=45);results.append({'exit':p.returncode,'result':json.loads(out) if out.strip() else None,'stderr':err[:300]})
 accepted=sum(r['result'] is not None and r['result']['state']=='accepted' for r in results)
 check(f'thirty-process-round-{round}',all(r['exit']==0 for r in results) and accepted==(1 if round==1 else 0) and count(db)==(1,0),{'accepted':accepted,'duplicates':sum(r['result'] is not None and r['result']['state']=='duplicate' for r in results),'database':count(db)})
 observations.extend(results)
for point,exitcode,expected in [('before_commit',71,0),('after_commit',72,1)]:
 crashdb=TEST/(point+'.sqlite');mod.initialize(crashdb);cfg=TEST/(point+'.json');save(cfg,config(crashdb,crash=point));p=child(cfg);out,err=p.communicate(timeout=30)
 check(point+'-interruption',p.returncode==exitcode and count(crashdb)==(expected,0),{'exit':p.returncode,'database':count(crashdb)})
 retry=mod.ingest(crashdb,pin,request,blob,manifest)
 check(point+'-recovery',count(crashdb)==(1,0) and retry['state']==('accepted' if expected==0 else 'duplicate'))
def refusal(name,req,b,m):
 before=count(db);error=None
 try:mod.ingest(db,pin,req,b,m)
 except ValueError as e:error=str(e)
 negative.append({'id':name,'error':error,'result':'fail','original_success_credit':0,'retained':True})
 check(name+'-refused',error is not None and count(db)==before)
refusal('other-commit',{**request,'commit':'1'*40},blob,manifest)
refusal('other-contract',{**request,'contract_id':'AR7076-P002'},blob,manifest)
changed=json.loads(blob);changed['contracts'][0]['actual']['value']['identity']=20
changed['contracts'][0]['result_sha256']=mod.sha(mod.canon(changed['contracts'][0]['actual']))
changed_blob=json.dumps(changed,separators=(',',':')).encode();changed_manifest=json.loads(manifest)
binding=next(r for r in changed_manifest['entries'] if r['path']==rel);binding['sha256']=mod.sha(changed_blob);binding['bytes']=len(changed_blob)
refusal('self-consistent-forgery',request,changed_blob,json.dumps(changed_manifest).encode())
refusal('null-key-component',{**request,'repository':None},blob,manifest)
snapshotdb=TEST/'snapshot.sqlite';mod.initialize(snapshotdb);working=TEST/'working.json';working.write_bytes(blob)
captured=working.read_bytes();response=mod.ingest(snapshotdb,pin,request,captured,manifest,pause=lambda:working.write_bytes(changed_blob))
card=mod.readback(snapshotdb,pin,response['receipt_id'])
check('verified-buffer-survives-path-replacement',card['source']['sha256']==pin['blob_sha256'] and mod.sha(working.read_bytes())!=pin['blob_sha256'])
tamperdb=TEST/'tamper.sqlite';mod.initialize(tamperdb);response=mod.ingest(tamperdb,pin,request,blob,manifest)
c=sqlite3.connect(tamperdb);c.execute('UPDATE receipts SET source_blob=?',(changed_blob,));c.commit();c.close();error=None
try:mod.readback(tamperdb,pin,response['receipt_id'])
except ValueError as e:error=str(e)
negative.append({'id':'stored-evidence-tamper','result':'fail','error':error,'original_success_credit':0,'retained':True})
check('consumer-readback-refuses-tamper',error=='pinned_digest_mismatch')
check('source-original-still-exact',git(rel)==blob)
# Production of this bounded local library record uses its own new database.
private=Path(r'D:\GHC-Family-Laboratory\private');private.mkdir(parents=True,exist_ok=True);realdb=private/'evidence.sqlite'
if realdb.exists():raise RuntimeError('Existing evidence database; do not replace')
save(private/'source-expectation.json',pin);mod.initialize(realdb);real=mod.ingest(realdb,pin,request,blob,manifest);card=mod.readback(realdb,pin,real['receipt_id'])
save(ROOT/'laboratory/data/intake-card.json',card)
payload={'schema':'ghc.shared-intake-acceptance.v1','storage':{'engine':'SQLite','version':sqlite3.sqlite_version,'journal_mode':'WAL','synchronous':'FULL','machine_scope':'local same-machine','network_filesystem_tested':False},'source_expectation':pin,'importer_sha256':mod.sha(module_path.read_bytes()),'test_sha256':mod.sha(Path(__file__).read_bytes()),'ordinary_test_processes':62,'new_agents_or_chats':0,'checks':checks,'negatives':negative,'passed':sum(r['pass'] for r in checks),'total':len(checks),'accepted_local_receipts':count(realdb)[0],'new_domain_completion_credit':0,'scope':'Bounded same-owner shared intake, not independent reproduction or a successor gate.'}
save(BASE/'shared-intake-acceptance.json',payload);save(TEST/'process-observations-private.json',observations)
print(json.dumps({'passed':payload['passed'],'total':len(checks),'ordinary_processes':62,'accepted_local_receipts':count(realdb)[0],'domain_credit':0}))
if payload['passed']!=len(checks):raise SystemExit(1)
