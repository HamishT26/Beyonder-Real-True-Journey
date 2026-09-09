"""Check a declared weighted cycle without querying or activating tasks."""
import argparse,collections,json,pathlib,re
from ghc_family_capacity_core import require,ContractError,strict_json

def review(route,profile):
    require(type(route) is dict and route.get('schema')=='ghc.family.weighted-route.v4','E_SCHEMA')
    require(type(profile) is dict and profile.get('schema')=='ghc.family.workflow-profile.v4','E_SCHEMA')
    cycle=route.get('cycle');astra=route.get('astra_identities');sol=route.get('sol_identities')
    require(type(cycle) is list and len(cycle)==45,'E_CYCLE')
    require(type(astra) is list and type(sol) is list and len(astra)==len(sol)==15,'E_IDENTITIES')
    require(all(type(x) is str and x.strip() for x in cycle+astra+sol),'E_IDENTITIES')
    require(len(set(astra+sol))==30 and set(cycle)==set(astra+sol),'E_IDENTITIES')
    counts=collections.Counter(cycle)
    require(all(counts[x]==1 for x in astra) and all(counts[x]==2 for x in sol),'E_MULTIPLICITY')
    require(all(x in (astra if i%3==0 else sol) for i,x in enumerate(cycle)),'E_CADENCE')
    rows=route.get('assignments');require(type(rows) is list and len(rows)==294,'E_WINDOW')
    for i,r in enumerate(rows):
        n=(689-1)*8+2+i;expected=f'v{n//8+1}-v{n%8+1}'
        require(type(r) is dict and r.get('phase')==expected and r.get('sequence')==i+1,'E_PHASE')
        require(r.get('owner')==cycle[(i+1)%45],'E_OWNER')
        require(r.get('model_role')==('Astra' if r['owner'] in astra else 'Sol'),'E_MODEL_ROLE')
        require(r.get('state')=='prospective','E_ACTIVATION_CLAIM')
    require(route.get('interstitial') is True and route.get('model_settings_changed') is False and route.get('activated_by_projection') is False,'E_BOUNDARY')
    require(profile.get('limits',{}).get('candidate_x1')==[100,500],'E_LIMITS')
    require(profile.get('context_window',{}).get('completed_bundles')==10,'E_LOOKBACK')
    return {'valid':True,'unique_identities':30,'cycle_positions':45,'future_assignments':294,'model_roles':dict(collections.Counter(r['model_role'] for r in rows)),'first':rows[0],'last':rows[-1],'task_transport_exercised':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--route',required=True);ap.add_argument('--profile',required=True);a=ap.parse_args()
    try:r=review(strict_json(pathlib.Path(a.route).read_text(encoding='utf-8')),strict_json(pathlib.Path(a.profile).read_text(encoding='utf-8')))
    except ContractError as ex:r={'valid':False,'error':str(ex)}
    print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['valid'] else 1)
