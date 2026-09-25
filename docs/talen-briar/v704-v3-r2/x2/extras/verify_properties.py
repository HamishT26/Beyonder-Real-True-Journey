from pathlib import Path
from fractions import Fraction as F
import json
import pytest
ROOT=Path(__file__).parent
PLAN=json.loads((ROOT/'frozen-plan.json').read_text(encoding='utf8'))
ROWS=json.loads((ROOT/'results.json').read_text(encoding='utf8'))['cases']
@pytest.mark.parametrize('index',range(64))
def test_retained_value_envelope(index):
    lower=ROWS[2*index];upper=ROWS[2*index+1]
    data=PLAN['cases'][2*index]['request']['input']
    assert lower['pass'] and upper['pass']
    assert lower['input_unchanged'] and upper['input_unchanged']
    lo=lower['actual']['value']['layers'];hi=upper['actual']['value']['layers']
    assert lo[0]==data['terminal']==hi[0]
    assert len(lo)==len(hi)==data['horizon']+1
    assert all(F(a)<=F(b) for ls,hs in zip(lo,hi) for a,b in zip(ls,hs))
    if data['discount']=='0':
        expected=[str(max(map(F,r))) for r in data['rewards']]
        assert all(layer==expected for layer in lo[1:]+hi[1:])
