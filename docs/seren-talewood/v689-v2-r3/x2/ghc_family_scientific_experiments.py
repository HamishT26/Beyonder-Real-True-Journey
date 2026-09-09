"""Bounded capacity, decision and sequential-evidence demonstrations."""
import argparse,hashlib,itertools,json,math,pathlib,sys,time
from fractions import Fraction as F

def run(root):
    phase=root/'docs/seren-talewood/v689-v2-r3';sys.path.insert(0,str(root/'scripts'))
    from ghc_family_inference_core import evaluate
    from ghc_family_capacity_core import evaluate as capacity
    mixtures=[]
    for r in [2,3,4]:mixtures.append({'relative_astra_cost':r,**capacity({'op':'mix_cost','astra_cost':r})['value'],'new_total_cost_units':196+98*r,'old_total_cost_units':147+147*r})
    channels=[]
    for epsilon in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        matrix=[[str(1-epsilon),'0',str(epsilon)],['0',str(1-epsilon),str(epsilon)]]
        law=evaluate({'op':'channel_joint','prior':['1/2','1/2'],'channel':matrix})['value']
        risk=evaluate({'op':'bayes_risk','joint':law['joint'],'loss':[[0,1],[1,0]]})['value']
        joint=[[F(x) for x in row] for row in law['joint']];obs=list(map(F,law['observation']))
        mutual=sum(float(p)*math.log2(float(p/(F(1,2)*obs[y]))) for row in joint for y,p in enumerate(row) if p)
        assert abs(mutual-float(1-epsilon))<1e-12 and F(risk['risk'])==epsilon/2
        channels.append({'epsilon':str(epsilon),'joint':law['joint'],'observation':law['observation'],'mutual_information_bits':mutual,'bayes_error':risk['risk'],'minimizers':risk['minimizers']})
    sequential=[]
    for horizon in range(1,11):
        final_sum=F(0);cross=0
        for bits in itertools.product([0,1],repeat=horizon):
            value=evaluate({'op':'lr_path','null':'1/2','alternative':'3/4','outcomes':list(bits)})['value'];path=list(map(F,value['path']));final_sum+=path[-1];cross+=max(path)>=4
        expectation=final_sum/(2**horizon);prob=F(cross,2**horizon)
        assert expectation==1 and prob<=F(1,4)
        sequential.append({'horizon':horizon,'paths':2**horizon,'expected_final_likelihood_ratio':str(expectation),'crossing_probability':str(prob),'ville_bound':'1/4'})
    correlated=[evaluate({'op':'lr_path','null':'1/2','alternative':'3/4','outcomes':[b]*4})['value']['path'] for b in [0,1]]
    assert sum(max(map(F,p))>=4 for p in correlated)==1
    counterfeit={'paths':correlated,'probability_per_path':'1/2','crossing_probability':'1/2','would_be_bound_if_conditional_null_held':'1/4','conditional_null_holds':False,'each_time_marginally_fair':True}
    witnesses=[];uncovered=[]
    for n in range(2,501):
        if n%2==0:k=n//2;den=[k,k+1,k*(k+1)];method='even'
        elif n%3==0:k=n//3;den=[k,4*k,12*k];method='multiple_of_three'
        elif n%4==3:a=(n+1)//4;q=n*a;den=[a,q+1,q*(q+1)];method='three_mod_four'
        else:uncovered.append(n);continue
        residual=F(4,n)-sum((F(1,d) for d in den),F(0));assert residual==0 and all(type(d) is int and d>0 for d in den)
        witnesses.append({'n':n,'denominators':den,'method':method,'residual':str(residual)})
    data=(phase/'plan/new-proposals.json').read_bytes();indexes=[(i*17)%200 for i in range(50)]
    def repeated():return [json.loads(data)['proposals'][i]['proposal_id'] for i in indexes]
    def batched():
        parsed=json.loads(data)['proposals'];return [parsed[i]['proposal_id'] for i in indexes]
    before=[];after=[];parity=True
    # Alternating order limits one simple order effect; it does not establish a general performance result.
    for sample in range(5):
        outputs={};times={}
        for name,fn in ([('before',repeated),('after',batched)] if sample%2==0 else [('after',batched),('before',repeated)]):
            start=time.perf_counter();outputs[name]=fn();times[name]=time.perf_counter()-start
        parity=parity and outputs['before']==outputs['after'];before.append(times['before']);after.append(times['after'])
    comparison=evaluate({'op':'paired_gain','before':[str(F(str(x))) for x in before],'after':[str(F(str(x))) for x in after],'same_workload_and_results':parity})['value']
    return {'mixtures':mixtures,'erasure_channels':channels,'conditional_null_enumeration':sequential,'correlated_marginal_counterexample':counterfeit,'unit_fraction_classes':{'range':[2,500],'verified':witnesses,'uncovered':uncovered,'universal_conjecture_proved':False,'novel_computational_bound':False},'local_loading_benchmark':{'before_seconds':before,'after_seconds':after,'same_outputs':parity,'source_bytes_sha256':hashlib.sha256(data).hexdigest(),'comparison':comparison,'measured_scope':'fifty record selections from an existing byte buffer','disk_io_included':False,'model_token_usage_measured':False,'cache_retention_measured':False},'independent_reproduction':False,'empirical_GMUT_confirmation':False,'stage20_ready':False}

def figure(result,dest):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,2,figsize=(10,4.2),layout='constrained')
    fig.patch.set_facecolor('#f7faf9')
    r=[m['relative_astra_cost'] for m in result['mixtures']];saving=[100*float(F(m['relative_saving'])) for m in result['mixtures']]
    ax[0].bar([str(x) for x in r],saving,color='#225c73',width=.52)
    for i,v in enumerate(saving):ax[0].text(i,v+.6,f'{v:.1f}%',ha='center',fontsize=11)
    ax[0].set(ylim=(0,25),xlabel='Assumed Astra cost relative to Sol',ylabel='Relative cost saving (%)',title='Equal-workload roster scenarios')
    eps=[float(F(c['epsilon'])) for c in result['erasure_channels']]
    ax[1].plot(eps,[c['mutual_information_bits'] for c in result['erasure_channels']],marker='o',color='#225c73',label='Information retained (bits)')
    ax[1].plot(eps,[float(F(c['bayes_error'])) for c in result['erasure_channels']],marker='s',color='#a75427',label='Minimum error probability')
    ax[1].set(xlabel='Erasure probability',ylabel='Bits or probability as labeled',title='What an erasure channel loses',ylim=(-.04,1.12));ax[1].legend(frameon=False,fontsize=9)
    for a in ax:a.spines[['right','top']].set_visible(False);a.grid(axis='y',alpha=.15);a.set_axisbelow(True)
    fig.suptitle('Seren capacity and evidence models',fontsize=16,fontweight='bold')
    dest.mkdir(parents=True,exist_ok=True);fig.savefig(dest/'capacity-and-information.png',dpi=180);fig.savefig(dest/'capacity-and-information.svg');plt.close(fig)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--out',required=True);ap.add_argument('--figures');a=ap.parse_args();r=run(pathlib.Path(a.root))
    with pathlib.Path(a.out).open('x',encoding='utf-8',newline='\n') as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
    if a.figures:figure(r,pathlib.Path(a.figures))
    print(json.dumps({'conditional_paths':sum(x['paths'] for x in r['conditional_null_enumeration']),'largest_horizon_crossing':r['conditional_null_enumeration'][-1]['crossing_probability'],'unit_fraction_witnesses':len(r['unit_fraction_classes']['verified']),'uncovered':len(r['unit_fraction_classes']['uncovered']),'local_benchmark_output_parity':r['local_loading_benchmark']['same_outputs']},indent=2))
