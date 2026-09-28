"""Pinned, transactional local evidence intake. No original experiment execution."""
from pathlib import Path
import hashlib,json,sqlite3,os,sys,time

def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def connect(db):
 con=sqlite3.connect(str(db),timeout=20,isolation_level=None)
 con.execute('PRAGMA busy_timeout=20000');con.execute('PRAGMA synchronous=FULL')
 return con
def initialize(db):
 con=connect(db);con.execute('PRAGMA journal_mode=WAL')
 con.execute('''CREATE TABLE IF NOT EXISTS receipts(
 repository TEXT NOT NULL, source_commit TEXT NOT NULL, source_path TEXT NOT NULL, contract_id TEXT NOT NULL,
 receipt_id TEXT NOT NULL UNIQUE, source_blob BLOB NOT NULL, manifest_blob BLOB NOT NULL, card_json TEXT NOT NULL,
 domain_credit INTEGER NOT NULL CHECK(domain_credit=0),
 PRIMARY KEY(repository,source_commit,source_path,contract_id))''');con.close()
def validate_blob(pin,request,blob,manifest_blob):
 required=['repository','commit','path','contract_id']
 if not isinstance(request,dict) or set(request)!=set(required) or any(not isinstance(request.get(k),str) or not request[k] for k in required):raise ValueError('required_source_identity')
 if any(request[k]!=pin[k] for k in required):raise ValueError('source_identity_mismatch')
 if not isinstance(blob,bytes) or len(blob)>4*1024*1024:raise ValueError('missing_or_oversized_evidence')
 if sha(blob)!=pin['blob_sha256'] or sha(manifest_blob)!=pin['manifest_sha256']:raise ValueError('pinned_digest_mismatch')
 manifest=json.loads(manifest_blob);binding=next((r for r in manifest['entries'] if r['path']==pin['path']),None)
 if binding is None or binding['sha256']!=sha(blob) or binding['bytes']!=len(blob):raise ValueError('manifest_binding_mismatch')
 data=json.loads(blob);rows=data['contracts'];row=next((r for r in rows if r['contract_id']==pin['contract_id']),None)
 if row is None or row['result_sha256']!=pin['result_sha256'] or sha(canon(row['actual']))!=pin['result_sha256'] or row['outcome']!=pin['original_outcome']:raise ValueError('pinned_contract_mismatch')
 identity={k:pin[k] for k in required};key=sha(canon(identity))
 return {'schema':'ghc.lab.evidence-card.v2','receipt_id':key,'owner':data['owner'],'phase':data['phase'],'source':{'repository':pin['repository'],'commit':pin['commit'],'path':pin['path'],'bytes':len(blob),'sha256':sha(blob),'manifest_sha256':sha(manifest_blob),'json_pointer':'/contracts/'+str(rows.index(row))},'contract_id':pin['contract_id'],'inputs':row['request'],'result':row['actual'],'original_outcome':row['outcome'],'original_result_sha256':row['result_sha256'],'original_negative_ids':[r['negative_id'] for r in row['mutations']],'checks':['independent pinned source expectation','same captured buffer hash parse and contract selection','transactional unique receipt','consumer readback verification'],'limitations':['Imported finite/synthetic evidence; not independently reproduced.','Zero new domain-completion credit.','Open gaps and authority limitations remain open.'],'new_domain_completion_credit':0,'source_execution_replayed':False,'lab_version_sha256':pin['lab_version_sha256'],'superseded_record_links':[]}
def ingest(db,pin,request,blob,manifest_blob,crash=None,pause=None):
 card=validate_blob(pin,request,blob,manifest_blob)
 if pause:pause()
 con=connect(db)
 try:
  con.execute('BEGIN IMMEDIATE')
  identity=[pin[k] for k in ['repository','commit','path','contract_id']]
  existing=con.execute('SELECT receipt_id FROM receipts WHERE repository=? AND source_commit=? AND source_path=? AND contract_id=?',identity).fetchone()
  if existing:
   con.rollback();con.close();readback(db,pin,existing[0]);return {'state':'duplicate','receipt_id':existing[0],'domain_credit':0}
  con.execute('INSERT INTO receipts VALUES(?,?,?,?,?,?,?,?,0)',identity+[card['receipt_id'],blob,manifest_blob,json.dumps(card,sort_keys=True,separators=(',',':'))])
  if crash=='before_commit':os._exit(71)
  con.commit()
  if crash=='after_commit':os._exit(72)
  return {'state':'accepted','receipt_id':card['receipt_id'],'domain_credit':0}
 except BaseException:
  try:con.rollback()
  except sqlite3.Error:pass
  raise
 finally:con.close()
def readback(db,pin,key):
 con=sqlite3.connect('file:'+Path(db).as_posix()+'?mode=ro',uri=True,timeout=20)
 try:row=con.execute('SELECT source_blob,manifest_blob,card_json,domain_credit FROM receipts WHERE receipt_id=?',(key,)).fetchone()
 finally:con.close()
 if row is None:raise ValueError('missing_receipt')
 request={k:pin[k] for k in ['repository','commit','path','contract_id']}
 card=validate_blob(pin,request,row[0],row[1])
 stored=json.loads(row[2])
 if stored!=card or row[3]!=0:raise ValueError('stored_card_integrity_failure')
 return stored
def worker(config):
 c=json.loads(Path(config).read_text(encoding='utf-8'));pin=json.loads(Path(c['pin']).read_text(encoding='utf-8'))
 if c.get('barrier'):
  deadline=time.monotonic()+25
  while not Path(c['barrier']).exists():
   if time.monotonic()>deadline:raise TimeoutError('barrier')
   time.sleep(0.02)
 result=ingest(c['db'],pin,{k:pin[k] for k in ['repository','commit','path','contract_id']},Path(c['blob']).read_bytes(),Path(c['manifest']).read_bytes(),crash=c.get('crash'))
 print(json.dumps(result))
if __name__=='__main__':
 if sys.argv[1]=='worker':worker(sys.argv[2])
 elif sys.argv[1]=='read':
  pin=json.loads(Path(sys.argv[3]).read_text(encoding='utf-8'));key=sha(canon({k:pin[k] for k in ['repository','commit','path','contract_id']}));print(json.dumps(readback(sys.argv[2],pin,key),ensure_ascii=False))
 else:raise SystemExit('Use worker or read')
