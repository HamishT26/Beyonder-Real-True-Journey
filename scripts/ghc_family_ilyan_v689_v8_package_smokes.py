"""Finite package witnesses with designed invalid subjects kept separately."""
import json
from bitarray import bitarray
import mmh3,xxhash
from ghc_family_ilyan_v689_v8_io import write
def main():
    rows=[];b=bitarray('10000001',endian='big');positive=b.tobytes()==bytes([129]) and b.count()==2
    try:bitarray('102');rejected=False
    except ValueError:rejected=True
    rows.append({'package':'bitarray','positive':positive,'invalid_subject':'nonbinary character in bit vector','subject_success_credit':0,'refusal_check':rejected})
    positive=mmh3.hash(b'foo',signed=False)==4138058784
    try:mmh3.hash(b'foo',seed=-1);rejected=False
    except ValueError:rejected=True
    rows.append({'package':'mmh3','positive':positive,'invalid_subject':'negative seed outside unsigned 32-bit domain','subject_success_credit':0,'refusal_check':rejected})
    positive=xxhash.xxh64(b'').hexdigest()=='ef46db3751d8e999'
    try:xxhash.xxh64([1,2]);rejected=False
    except TypeError:rejected=True
    rows.append({'package':'xxhash','positive':positive,'invalid_subject':'list object instead of supported byte or text input','subject_success_credit':0,'refusal_check':rejected})
    receipt={'rows':rows,'positive_passes':sum(r['positive'] for r in rows),'refusal_passes':sum(r['refusal_check'] for r in rows),'failed_subjects_retained':3,'cryptographic_claim':False,'same_owner_only':True};write('x1/toolchain/smokes.json',receipt);print(json.dumps(receipt));raise SystemExit(0 if all(r['positive'] and r['refusal_check'] for r in rows) else 1)
if __name__=='__main__':main()
