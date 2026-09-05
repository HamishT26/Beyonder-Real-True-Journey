"""Small accepting and rejecting witnesses for each new direct package."""
import json
from pathlib import Path
import simpy
from transitions import Machine,MachineError
from constraint import Problem,AllDifferentConstraint,ExactSumConstraint
def main():
    rows=[];env=simpy.Environment();seen=[]
    def job(name):yield env.timeout(2);seen.append([name,env.now])
    env.process(job('a'));env.process(job('b'));env.run();positive=seen==[['a',2],['b',2]]
    try:env.timeout(-1);adverse=False
    except ValueError:adverse=True
    rows.append({'package':'simpy','positive':positive,'adverse':adverse,'observed':seen,'real_time_used':False})
    m=Machine(states=['planned','running','recorded'],initial='planned',auto_transitions=False,transitions=[['start','planned','running'],['finish','running','recorded']])
    try:m.finish();adverse=False
    except MachineError:adverse=True
    m.start();m.finish();rows.append({'package':'transitions','positive':m.state=='recorded','adverse':adverse,'observed':m.state})
    p=Problem();p.addVariables(['a','b'],[1,2,3]);p.addConstraint(AllDifferentConstraint());p.addConstraint(ExactSumConstraint(4));solutions=sorted((s['a'],s['b']) for s in p.getSolutions())
    bad=Problem();bad.addVariables(['a','b'],[1]);bad.addConstraint(AllDifferentConstraint());none=bad.getSolutions();rows.append({'package':'python-constraint2','positive':solutions==[(1,3),(3,1)],'adverse':none==[],'observed':solutions})
    receipt={'rows':rows,'positive_passes':sum(r['positive'] for r in rows),'adverse_passes':sum(r['adverse'] for r in rows),'same_owner_only':True,'independent_reproduction':False,'real_entities':0}
    path=Path(__file__).resolve().parents[1]/'docs/ilyan-reed/v685-v8/x2/toolchain/package-smokes.json'
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(receipt));raise SystemExit(0 if all(r['positive'] and r['adverse'] for r in rows) else 1)
if __name__=='__main__':main()
