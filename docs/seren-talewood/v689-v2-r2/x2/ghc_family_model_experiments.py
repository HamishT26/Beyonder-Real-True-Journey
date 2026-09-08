"""Finite mathematical exercises and explicit counterexamples, not universal proofs."""
import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--site',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    sys.path[:]=[str(args.repo/'scripts'),str(args.site)]+[p for p in sys.path if 'site-packages' not in p.lower()]
    import ghc_family_model_core as model
    import numpy as np
    p=[['3/4','1/4'],['1/2','1/2']];pi=model.stationary_distribution({'matrix':p})
    floating=np.linalg.solve(np.array([[-0.25,0.5],[1.0,1.0]]),np.array([0.0,1.0]))
    error=max(abs(float(Fraction(v))-float(w)) for v,w in zip(pi,floating))
    assert error<1e-12
    trajectories=[]
    for label,start in [('All in state A',['1','0']),('All in state B',['0','1']),('Equal initial weights',['1/2','1/2'])]:
        distribution=start[:];rows=[]
        for step in range(13):
            rows.append(dict(step=step,distribution=distribution,
                shannon_nats=model.entropy({'distribution':distribution}),
                relative_entropy_to_stationary_nats=model.relative_entropy({'p':distribution,'q':pi})['nats']))
            distribution=model.markov_step({'matrix':p,'distribution':distribution})
        assert all(float(b['relative_entropy_to_stationary_nats'])<=float(a['relative_entropy_to_stationary_nats'])+2e-12 for a,b in zip(rows,rows[1:]))
        trajectories.append(dict(label=label,rows=rows))
    reset=[[1,0],[1,0]];uniform=['1/2','1/2'];reset_after=model.markov_step({'matrix':reset,'distribution':uniform})
    entropy_counterexample=dict(matrix=reset,before=uniform,after=reset_after,
       entropy_before=model.entropy({'distribution':uniform}),entropy_after=model.entropy({'distribution':reset_after}),
       rejected_claim='Shannon entropy must increase under every stochastic kernel',
       interpretation='False for an abstract general kernel; this does not contradict the physical second law for a properly specified total system.')
    assert float(entropy_counterexample['entropy_after'])<float(entropy_counterexample['entropy_before'])
    ring=[[0,1,0],[0,0,1],[1,0,0]];groups=[[0,1],[2]]
    coarse=model.coarse_grain({'matrix':ring,'stationary':['1/3']*3,'groups':groups})
    full=model.markov_step({'matrix':ring,'distribution':[1,0,0]})
    aggregated=[str(Fraction(full[0])+Fraction(full[1])),full[2]]
    projected=model.markov_step({'matrix':coarse['matrix'],'distribution':[1,0]})
    coarse_counterexample=dict(matrix=ring,groups=groups,stationary_projection=coarse,
        true_aggregated_next=aggregated,projected_next=projected,disagree=aggregated!=projected,
        rejected_claim='A stationary-flow projection always gives closed dynamics for every initial distribution')
    assert not coarse['lumpable'] and coarse_counterexample['disagree']
    witnesses=[]
    for n in range(2,102):
        result=model.egyptian_fraction_search({'n':n,'max_denominator':1000000,'max_pairs':100000})
        assert result['witness'] is not None,(n,result)
        denominators=result['witness']
        residual=Fraction(4,n)-sum(Fraction(1,d) for d in denominators)
        assert residual==0 and all(type(d) is int and d>0 for d in denominators)
        witnesses.append(dict(n=n,denominators=denominators,residual=str(residual),verified_by_exact_substitution=True))
    batches=[dict(task_id=f'ST6892R2-X2-SAFE-{114+i:03}',start=a,end=b,
                  witness_count=sum(a<=r['n']<=b for r in witnesses),outcome='completed')
             for i,(a,b) in enumerate([(2,26),(27,51),(52,76),(77,101)])]
    output=dict(schema='ghc.family.remaster.mathematical-experiments.v1',matrix=p,stationary=pi,
       numpy_version=np.__version__,numpy_stationary=[float(v) for v in floating],maximum_stationary_discrepancy=error,
       trajectories=trajectories,entropy_counterexample=entropy_counterexample,
       coarse_graining_counterexample=coarse_counterexample,egyptian_witnesses=witnesses,search_batches=batches,
       searched_n_minimum=2,searched_n_maximum=101,universal_conjecture_proved=False,
       new_fundamental_law_established=False,physical_or_cognitive_observations=0,independent_reproduction=False,
       interpretation='Finite exact-arithmetic and cross-implementation exercises under shared infrastructure. Known mathematics supplies assumptions; these exercises do not extend the known universal result.')
    with args.output.open('x',encoding='utf-8',newline='\n') as f:json.dump(output,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(dict(verified_integer_cases=len(witnesses),stationary_discrepancy=error,
        entropy_counterexample=True,nonlumpability_counterexample=True,universal_proof=False)))

if __name__=='__main__':main()
