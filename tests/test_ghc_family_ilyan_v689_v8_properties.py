"""Generated finite input checks using already installed Hypothesis."""
from hypothesis import given,settings,strategies as st
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ghc_family_membership_x1 import evaluate as x1
from ghc_family_membership_x2 import evaluate as x2
S=settings(max_examples=60,derandomize=True,database=None)
@st.composite
def vectors(draw):
    n=draw(st.integers(1,16));bits=draw(st.lists(st.integers(0,1),min_size=n,max_size=n));pos=draw(st.lists(st.integers(0,n-1),min_size=1,max_size=32));return ''.join(map(str,bits)),pos
@S
@given(vectors())
def test_insert_never_clears_a_bit(case):
    bits,pos=case;r=x1({'operation':'bit_insert','payload':{'bits':bits,'positions':pos}})['value'];assert all(a=='0' or b=='1' for a,b in zip(bits,r));assert all(r[p]=='1' for p in pos)
@S
@given(vectors())
def test_counting_inverse_with_exact_counters(case):
    bits,pos=case;counts=[int(x)*3 for x in bits];after=x2({'operation':'counting_insert','payload':{'counts':counts,'positions':pos}})['value'];back=x2({'operation':'guarded_decrement','payload':{'counts':after,'positions':pos,'known_member':True}})['value']['counts'];assert back==counts
@S
@given(vectors(),st.integers(1,7))
def test_saturation_flag_matches_lost_increment(case,cap):
    bits,pos=case;counts=[min(cap,int(x)) for x in bits];r=x2({'operation':'saturation_hold','payload':{'counts':counts,'positions':pos,'cap':cap}})['value'];lost=[i for i,c in enumerate(counts) if c+pos.count(i)>cap];assert r['overflow_positions']==lost;assert r['decrement_information_preserved']==(not lost)
@S
@given(vectors(),st.integers(1,20))
def test_shards_cover_each_position_once(case,block):
    bits,_=case;r=x2({'operation':'shard_roundtrip','payload':{'bits':bits,'block':block}})['value'];assert r['reconstructed']==bits;covered=[i for c in r['chunks'] for i in range(c['offset'],c['offset']+len(c['bits']))];assert covered==list(range(len(bits)))
@S
@given(vectors())
def test_unknown_member_deletion_is_refused(case):
    bits,pos=case;r=x2({'operation':'guarded_decrement','payload':{'counts':[99]*len(bits),'positions':pos,'known_member':False}});assert r['value']=={'refused':'unknown_member'}
