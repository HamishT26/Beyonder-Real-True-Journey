from pathlib import Path
import sys,json,subprocess,time,sqlite3,importlib.util,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2];BANK=Path(r'D:\GHC-Archives\phase-banks\avelin-reed-v707-v6-r2')
SOURCE=BANK/'intake-atomic-tests';TEST=BANK/'intake-all-ready-tests';TEST.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('intake_store',ROOT/'laboratory/intake_store.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
db=TEST/'shared.sqlite';m.initialize(db);checks=[]
for n in [1,2]:
 ready=TEST/f'ready-{n}';ready.mkdir();barrier=TEST/f'go-{n}';config=TEST/f'config-{n}.json'
 config.write_text(json.dumps({'db':str(db),'pin':str(SOURCE/'pin.json'),'blob':str(SOURCE/'source.json'),'manifest':str(SOURCE/'manifest.json'),'ready_dir':str(ready),'barrier':str(barrier)}),encoding='utf-8')
 workers=[subprocess.Popen([sys.executable,'-X','utf8','-B',str(BASE/'intake-ready-worker.py'),str(config)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)) for _ in range(30)]
 deadline=time.monotonic()+35
 while len(list(ready.iterdir()))<30:
  if time.monotonic()>deadline:raise TimeoutError('not all thirty workers ready')
  time.sleep(.05)
 ready_count=len(list(ready.iterdir()));barrier.write_text('go',encoding='utf-8');results=[]
 for w in workers:
  out,err=w.communicate(timeout=45);results.append({'exit':w.returncode,'state':json.loads(out)['state'] if out.strip() else None,'error':err[:200]})
 con=sqlite3.connect(db);count,credit=con.execute('SELECT COUNT(*),SUM(domain_credit) FROM receipts').fetchone();con.close()
 accepted=sum(r['state']=='accepted' for r in results)
 checks.append({'id':f'all-thirty-ready-round-{n}','pass':ready_count==30 and all(r['exit']==0 for r in results) and count==1 and credit==0 and accepted==(1 if n==1 else 0),'ready_before_release':ready_count,'accepted':accepted,'duplicates':sum(r['state']=='duplicate' for r in results),'stored_receipts':count,'domain_credit':credit})
payload={'schema':'ghc.shared-intake-barrier-continuation.v1','reason':'Strengthen the earlier process-start barrier by observing all thirty workers ready before release. Earlier suite remains preserved and was not rerun.','ordinary_test_processes':60,'new_agents_or_chats':0,'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(BASE/'shared-intake-barrier-acceptance.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':payload['passed'],'total':payload['total'],'ordinary_processes':60}))
if payload['passed']!=payload['total']:raise SystemExit(1)
