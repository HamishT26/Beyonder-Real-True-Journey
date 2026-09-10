"""Exercise current packages on explicit finite inputs, without performance claims."""
import json
from bitarray import bitarray
import mmh3,xxhash
from ghc_family_ilyan_v689_v8_io import read,write
def main():
    examples=read('plan/new-proposals.json')['proposals'][:10];rows=[]
    for i,p in enumerate(examples):
        s=p['request']['payload']['bits'];b=bitarray(s,endian='big');rows.append({'package':'bitarray','case':i+1,'input':s,'output':{'bits':b.to01(),'ones':b.count()},'passed':b.to01()==s and b.count()==p['expected']['value']['ones']})
        text='synthetic membership '+str(i)+' φ';data=text.encode('utf8');a=mmh3.hash(text,seed=i,signed=False);c=mmh3.hash(data,seed=i,signed=False);rows.append({'package':'mmh3','case':i+1,'utf8_sha256_not_recorded_as_identity':True,'text_value':a,'byte_value':c,'passed':a==c,'cryptographic':False})
        h=xxhash.xxh64(seed=i);h.update(data[:i]);h.update(data[i:]);stream=h.hexdigest();direct=xxhash.xxh64(data,seed=i).hexdigest();rows.append({'package':'xxhash','case':i+1,'stream_digest':stream,'one_shot_digest':direct,'passed':stream==direct,'cryptographic':False})
    write('x2/toolchain-comparisons.json',{'task':'IR6898-EXTRA-06','rows':rows,'passing':sum(r['passed'] for r in rows),'tests':len(rows),'same_owner_only':True,'independent_reproduction':False,'timing_claim':False});print(json.dumps({'checks':len(rows),'passing':sum(r['passed'] for r in rows)}));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
