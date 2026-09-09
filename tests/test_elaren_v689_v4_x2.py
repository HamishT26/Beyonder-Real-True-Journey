import copy,json,pathlib,sys
ROOT=pathlib.Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_weave_evidence_core import evaluate
BASE=ROOT/'docs/elaren-kestrel/v689-v4'
def load(rel): return json.loads((BASE/rel).read_text(encoding='utf-8'))
def test_x2_frozen_contracts():
    for p in load('plan/new-proposals.json')['proposals'][100:]:
        request=copy.deepcopy(p['request']); before=json.dumps(request,sort_keys=True)
        assert evaluate(request)==p['expected']; assert json.dumps(request,sort_keys=True)==before
def test_x2_candidates_and_refinements():
    assert all(x['validator_passed'] for x in load('x2/candidate-results.json')['candidates'])
    assert all(x['exact_reconstruction'] for x in load('x2/inherited-refinements.json')['actions'])
def test_x2_counts_and_outcomes():
    s=load('x2/summary.json'); assert s['safe_now']==s['candidate']==s['clean_fix_refine']==100
    assert s['combined_outcomes']=={'completed':170,'represented':20,'open_gap':5,'exact_gate':5}
def test_x2_skills_and_runners():
    assert load('x2/skill-validation.json')['valid']; assert load('x2/runner-validation.json')['valid']
