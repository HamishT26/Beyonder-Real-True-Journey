import copy,json,pathlib,sys
ROOT=pathlib.Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_weave_draft_core import evaluate
BASE=ROOT/'docs/elaren-kestrel/v689-v4'
def load(rel): return json.loads((BASE/rel).read_text(encoding='utf-8'))
def test_x1_frozen_contracts():
    for p in load('plan/new-proposals.json')['proposals'][:100]:
        request=copy.deepcopy(p['request']); before=json.dumps(request,sort_keys=True)
        assert evaluate(request)==p['expected']; assert json.dumps(request,sort_keys=True)==before
def test_x1_candidates_and_refinements():
    assert all(x['validator_passed'] for x in load('x1/candidate-results.json')['candidates'])
    assert all(x['exact_reconstruction'] for x in load('x1/inherited-refinements.json')['actions'])
def test_x1_counts():
    s=load('x1/summary.json'); assert s['safe_now']==s['candidate']==s['clean_fix_refine']==100
def test_package_composite():
    p=load('x1/package-receipt.json'); assert p['valid'] and p['direct_count']==3 and p['closure_count']==4
    assert p['positive_smokes']==p['rejecting_smokes']==3 and p['failed_plan_digest_count']==2
def test_skill_runner_receipts():
    assert load('x1/skill-validation.json')['valid']; assert load('x1/runner-validation.json')['valid']
