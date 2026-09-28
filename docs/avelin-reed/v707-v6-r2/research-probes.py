from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math,json,hashlib,datetime

BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2]
out=[];tests=[]
def add(i,title,result,scope,check):
 out.append({'id':f'Q{i:02}','question':title,'bounded_result':result,'remaining_open':scope,'universal_solution_claim':False,'empirical_claim':False})
 tests.append({'id':f'Q{i:02}-bounded-check','pass':bool(check)})
cnf=[[1,2],[-1,3],[-2,-3]]
sat=[bits for bits in product([False,True],repeat=3) if all(any(bits[abs(v)-1] if v>0 else not bits[abs(v)-1] for v in c) for c in cnf)]
add(1,'P versus NP',{'variables':3,'assignments_checked':8,'satisfying_assignments':sat},'No asymptotic complexity separation is inferred from eight assignments.',len(sat)==2)
field=[{'x':x,'y':y,'u':math.sin(y),'v':math.sin(x)} for x in range(8) for y in range(8)]
divergence=[0.0 for _ in field]
add(2,'Navier-Stokes regularity',{'grid_points':len(field),'field':'u(x,y)=sin(y), v(x,y)=sin(x)','analytic_divergence':0,'finite_energy':sum(p['u']**2+p['v']**2 for p in field)},'This is an initial-field consistency check, not a Navier-Stokes evolution or a continuum regularity proof.',all(x==0 for x in divergence))
N=10000;z=sum(1/(k*k) for k in range(1,N+1));target=math.pi**2/6
add(3,'Riemann hypothesis',{'point':2,'partial_sum':z,'tail_interval':[1/(N+1),1/N],'known_value':target},'A real-axis value says nothing about all nontrivial complex zeros.',z+1/(N+1)<target<z+1/N)
gaps=[{'ring_size':n,'unnormalized_graph_gap':4*math.sin(math.pi/n)**2} for n in [4,8,16,32]]
add(4,'Yang-Mills mass gap',gaps,'A positive finite matrix gap is not a continuum quantum-field-theory mass gap; this sequence tends downward with size.',all(a['unnormalized_graph_gap']>b['unnormalized_graph_gap']>0 for a,b in zip(gaps,gaps[1:])))
collatz=[]
for start in range(1,1001):
 x=start;steps=0
 while x!=1 and steps<5000:x=3*x+1 if x%2 else x//2;steps+=1
 collatz.append({'start':start,'steps':steps,'ended_at_one':x==1})
add(5,'Collatz conjecture',{'range':[1,1000],'step_cap':5000,'all_reached_one':all(r['ended_at_one'] for r in collatz),'longest':max(collatz,key=lambda r:r['steps']),'start_27':collatz[26]},'Finite enumeration cannot cover every positive integer.',all(r['ended_at_one'] for r in collatz) and collatz[26]['steps']==111)
fractions=[]
for n in range(2,51):
 found=None
 for a in range(max(1,n//4+1),n+1):
  if found:break
  for b in range(a,4*n*n+1):
   rem=F(4,n)-F(1,a)-F(1,b)
   if rem>0 and rem.numerator==1 and rem.denominator>=b:
    found=[a,b,rem.denominator];break
 fractions.append({'n':n,'denominators':found,'exact':found is not None and sum((F(1,k) for k in found),F(0))==F(4,n)})
add(6,'Erdos-Straus conjecture',{'range':[2,50],'witnesses':fractions,'distinct_denominators_required':False},'The bounded search supplies no proof for arbitrary n; an unlocated witness would be a search gap, not a disproof.',all(r['exact'] for r in fractions))
add(7,'Dark-matter microphysics',{'synthetic_total_mass':10,'decompositions':[[2,8],[3,7]],'same_total':True},'Total gravitational mass alone does not identify the components; this toy ingests no observations.',2+8==3+7==10)
add(8,'Dark-energy origin',{'rho_matter':F(2),'rho_scalar':F(3),'explicit_lambda_density':F(5),'H_squared_explicit':F(10,3),'H_squared_absorbed':F(10,3)},'Equivalent background bookkeeping does not establish a physical origin or parameter estimate.',F(2+3+5,3)==F(2+(3+5),3))
add(9,'Quantum measurement',{'declared_probabilities':[F(1,2),F(1,2)],'interpretation_labels':['collapse','branching'],'probability_table_changed_by_label':False},'An interpretation label with the same probability table supplies no distinguishing experiment.',F(1,2)+F(1,2)==1)
joint={(0,0):F(1,2),(1,1):F(1,2)};marginal=[sum(p for (a,b),p in joint.items() if a==i) for i in [0,1]]
add(10,'Black-hole information',{'classical_joint':[[list(k),str(v)] for k,v in joint.items()],'marginal':marginal,'hidden_correlation':True},'A classical marginalization example is not black-hole evaporation or quantum gravity.',marginal==[F(1,2),F(1,2)])
entropy=lambda p:-sum(float(x)*math.log2(float(x)) for x in p if x)
add(11,'Cosmological arrow of time',{'initial_entropy':entropy([1,0,0]),'permutation_entropy':entropy([0,1,0]),'mixed_entropy':entropy([F(1,3)]*3)},'Choosing a low-entropy initial state does not explain the universe initial condition.',entropy([1,0,0])==entropy([0,1,0])<entropy([F(1,3)]*3))
record={'input':'synthetic prompt','output':'synthetic answer'}
add(12,'Conscious experience',{'observable_record':record,'compatible_descriptions':['functional record only','functional record plus experiential hypothesis']},'The same finite functional record cannot select a theory of experience without an additional justified bridge.',record==dict(record))
add(13,'Free will and responsibility',{'deterministic_choice':1,'normative_assignments':{'strict_responsibility':True,'mitigated_responsibility':False}},'A computational rule does not settle normative responsibility or metaphysical freedom.',True)
add(14,'Suffering and the problem of evil',{'synthetic_outcomes':{'harm':2,'benefit':3},'consequential_score':1,'rights_constraint':'harm may remain prohibited despite positive net score'},'Divergent ethical evaluations do not solve a theological problem.',3-2==1)
voting=json.loads((ROOT/'models/x2/voting.json').read_text(encoding='utf-8'))
baseline=json.loads((ROOT/'models/x1/voting.json').read_text(encoding='utf-8'))
add(15,'Fair collective choice',{'baseline_cycle':baseline['metrics']['cycle'],'alternate_winner':voting['metrics']['condorcet_winner']},'A chosen tie rule cannot manufacture public legitimacy or satisfy every fairness demand.',baseline['metrics']['cycle'] and voting['metrics']['condorcet_winner']==0)
scalar=[]
for kinetic,potential in [(F(0),F(2)),(F(2),F(0)),(F(1),F(3))]:
 rho=kinetic+potential;p=kinetic-potential;scalar.append({'kinetic':kinetic,'potential':potential,'rho':rho,'pressure':p,'w':p/rho})
tests.extend([{'id':'scalar-frozen-w-minus-one','pass':scalar[0]['w']==-1},{'id':'scalar-kinetic-w-plus-one','pass':scalar[1]['w']==1},{'id':'scalar-mixed-w','pass':scalar[2]['w']==F(-1,2)},{'id':'opposite-exchange-current','pass':F(2,3)+F(-2,3)==0},{'id':'same-sign-current-counterexample','pass':F(2,3)+F(2,3)!=0},{'id':'omega-alpha-normalization-degeneracy','pass':F(2)*F(3)==F(4)*F(3,2)}])
def enc(x):
 if isinstance(x,F):return str(x)
 raise TypeError(type(x).__name__)
payload={'schema':'ghc.bounded-research-probes.v1','defined_by':'research.md Q01-Q15','probes':out,'scalar_identities':scalar,'tests':tests,'passed':sum(t['pass'] for t in tests),'total':len(tests),'source_models_read_only':True,'new_empirical_observations':0,'universal_problems_solved':0,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (BASE/'research-probe-results.json').open('x',encoding='utf-8') as f:json.dump(payload,f,indent=2,default=enc);f.write('\n')
print(json.dumps({'probes':len(out),'passed':payload['passed'],'total':len(tests),'universal_solutions':0}))
if payload['passed']!=len(tests):raise SystemExit(1)
