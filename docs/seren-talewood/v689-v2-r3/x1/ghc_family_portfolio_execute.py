"""Reproducible owner checks and lossless source-record refinement."""
import argparse,copy,hashlib,importlib,json,pathlib,sys

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def flatten(value,path=None):
    path=[] if path is None else path
    typ=type(value).__name__
    if typ not in ('dict','list','str','int','float','bool','NoneType'):raise TypeError(typ)
    result=[{'path':path,'type':typ,'value':{} if typ=='dict' else [] if typ=='list' else value}]
    if typ=='dict':
        for key in sorted(value):result.extend(flatten(value[key],path+[key]))
    elif typ=='list':
        for i,child in enumerate(value):result.extend(flatten(child,path+[i]))
    return result

def rebuild(rows):
    if not rows or rows[0]['path']!=[]:raise ValueError('Missing root')
    values={}
    for row in rows:
        path=tuple(row['path']);value=copy.deepcopy(row['value'])
        if path in values or type(value).__name__!=row['type']:raise ValueError('Duplicate or mistyped node')
        if path:
            parent=values[path[:-1]];key=path[-1]
            if type(parent) is dict and type(key) is str:parent[key]=value
            elif type(parent) is list and type(key) is int and key==len(parent):parent.append(value)
            else:raise ValueError('Invalid typed child')
        values[path]=value
    return values[()]

def execute(root,stage):
    sys.path.insert(0,str(root/'scripts'))
    from ghc_family_capacity_core import typed_equal
    evaluate=importlib.import_module('ghc_family_capacity_core' if stage=='x1' else 'ghc_family_inference_core').evaluate
    phase=root/'docs/seren-talewood/v689-v2-r3'
    definitions=json.loads((phase/'plan/new-proposals.json').read_bytes())['proposals']
    selected=[p for p in definitions if p['stage']==stage];safe=[];candidates=[]
    for p in selected:
        request=copy.deepcopy(p['input']);actual=evaluate(request);same=typed_equal(actual,p['expected']) and typed_equal(request,p['input'])
        safe.append({'task_id':'SAFE-'+p['proposal_id'][-3:],'proposal_id':p['proposal_id'],'input_sha256':digest(p['input']),'observed':actual,'expected':p['expected'],'matched':same,'input_unchanged':typed_equal(request,p['input']),'subject_result':'pass' if actual['ok'] else 'fail','outcome':'completed' if same else 'open_gap','independent_reproduction':False})
        changed={**copy.deepcopy(p['input']),'execute':True};before=copy.deepcopy(changed);bad=evaluate(changed)
        good=typed_equal(bad,{'ok':False,'value':None,'error':'E_FIELDS'}) and typed_equal(changed,before)
        candidates.append({'task_id':'CAND-'+p['proposal_id'][-3:],'proposal_id':p['proposal_id'],'request':before,'request_sha256':digest(before),'observed':bad,'matched':good,'subject_result':'fail','original_success_credit':0,'outcome':'completed' if good else 'open_gap'})
    source=json.loads((phase/'plan/inherited-proposals.json').read_bytes())['selections'];refined=[]
    for s in (r for r in source if r['stage']==stage):
        original=copy.deepcopy(s['original']);nodes=flatten(original);result=rebuild(nodes)
        same=typed_equal(result,original) and digest(result)==s['original_record_sha256']
        refined.append({'source_id':s['source_id'],'source_title':s['source_title'],'source_record_sha256':s['original_record_sha256'],'typed_nodes':nodes,'typed_representation_sha256':digest(nodes),'roundtrip_sha256':digest(result),'matched':same,'source_execution_credit':0,'new_proposal_credit':0,'outcome':'completed' if same else 'open_gap','scope':'One inherited record transformed and reconstructed; no host cleanup or inherited behavior execution.'})
    return {'stage':stage,'safe_now':safe,'candidate':candidates,'clean_fix_refine':refined,'counts':{'safe_now':len(safe),'candidate':len(candidates),'clean_fix_refine':len(refined),'accepting_subjects':sum(r['subject_result']=='pass' for r in safe),'designed_failed_subjects':sum(r['subject_result']=='fail' for r in safe)+len(candidates),'all_matched':all(r['matched'] for rows in [safe,candidates,refined] for r in rows)},'source_replayed':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--stage',choices=['x1','x2'],required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    result=execute(pathlib.Path(a.root),a.stage)
    with pathlib.Path(a.out).open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False);f.write('\n')
    print(json.dumps(result['counts'],indent=2));raise SystemExit(0 if result['counts']['all_matched'] else 1)
