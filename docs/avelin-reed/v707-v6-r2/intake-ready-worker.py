from pathlib import Path
import sys,os,time,json,importlib.util
c=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('intake_store',Path(__file__).resolve().parents[3]/'laboratory/intake_store.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pin=json.loads(Path(c['pin']).read_text(encoding='utf-8'));blob=Path(c['blob']).read_bytes();manifest=Path(c['manifest']).read_bytes()
(Path(c['ready_dir'])/str(os.getpid())).write_text('ready',encoding='utf-8')
deadline=time.monotonic()+40
while not Path(c['barrier']).exists():
 if time.monotonic()>deadline:raise TimeoutError('all-ready barrier')
 time.sleep(.02)
print(json.dumps(m.ingest(c['db'],pin,{k:pin[k] for k in ['repository','commit','path','contract_id']},blob,manifest)))
