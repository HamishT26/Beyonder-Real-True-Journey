"""Owner-local structural fixture tribunal; not the historical global implementation."""
import json,re,sys,copy

def review(x):
    issues=[]
    if x.get('owner')!='Orren Pike':issues.append('OWNER')
    if x.get('outcomes')!=['completed','represented','open_gap','exact_gate']:issues.append('OUTCOMES')
    if x.get('canonical_successes')!=0:issues.append('REPLAY_LATCH')
    for p in x.get('paths',[]):
        if not p.startswith('docs/orren-pike/v705-v1/') or '..' in p.split('/'):issues.append('SCOPE')
    if re.search(r'(?i)[a-z]:[\\/]',json.dumps(x)):issues.append('PRIVATE_PATH')
    if not x.get('paths'):issues.append('EMPTY_SCOPE')
    return {'valid':not issues,'issues':sorted(set(issues)),'fixture_only':True}

def main():
    x=json.load(sys.stdin);json.dump(review(x),sys.stdout);print()

if __name__=='__main__':main()
