import json, pathlib
ROOT=pathlib.Path(__file__).parents[1]
BASE=ROOT/'docs/elaren-kestrel/v689-v4'
def load(rel): return json.loads((BASE/rel).read_text(encoding='utf-8'))
def test_plan_counts_and_labels():
    p=load('plan/new-proposals.json')['proposals']; i=load('plan/inherited-selections.json')['records']
    assert len(p)==len(i)==200
    assert {x['expected_disposition'] for x in p}=={'completed','represented','open_gap','exact_gate'}
def test_plan_has_no_execution_credit():
    assert load('plan/new-proposals.json')['implementation_ran'] is False
    assert all(x['novelty_credit']==x['execution_credit_at_freeze']==0 for x in load('plan/inherited-selections.json')['records'])
def test_two_session_freezes():
    for stage in ('x1','x2'):
        p=load(f'plan/portfolio-freeze-{stage}.json')
        assert len(p['safe_now'])==len(p['candidate'])==len(p['clean_fix_refine'])==100
def test_novelty_scope():
    n=load('plan/novelty-review.json')
    assert n['exact_title_collisions']==n['exact_request_collisions']==0
    assert n['universal_novelty_claimed'] is False
