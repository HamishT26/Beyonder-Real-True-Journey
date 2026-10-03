import { performance } from 'node:perf_hooks';
import { createLifecycleHooks } from './lifecycle-hooks.mjs';
export const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
export const sum=a=>a.reduce((s,v)=>s+v,0);
export const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const sq=a=>dot(a,a), norm=a=>Math.sqrt(sq(a));
const q=y=>y.slice(0,3),v=y=>y.slice(3,6);
const lap=a=>a.map((z,i)=>a[(i+1)%3]+a[(i+2)%3]-2*z);
const mechanical=(id,title,f,y0,invariants,extras={})=>({id,title,dimension:y0.length,f,y0,invariants,axes:['q1','q2','q3'],...extras});
const close=(name,value,reference,tolerance=2e-5)=>({name,value,reference,tolerance,pass:Number.isFinite(value)&&Math.abs(value-reference)<=tolerance});
const bounded=(name,value,low,high,tolerance=2e-8)=>({name,value,low,high,tolerance,pass:Number.isFinite(value)&&value>=low-tolerance&&value<=high+tolerance});
export const models=[
mechanical('S01','Null ray in flat spacetime',()=>[0.6,0,0.8],[0,0,0],
(y,y0,t)=>[close('null interval',sq(y)-t*t,0,1e-9),close('x analytic',y[0],0.6*t,1e-10)],
{family:'affine null geodesic',projects:['P01','P02','P04'],equation:'dx/dt=(0.6,0,0.8); c=1',claim:'A flat-space kinematic limit, not a GMUT field solution.'}),
mechanical('S02','Three-axis harmonic oscillator',(t,y)=>[...v(y),-y[0],-2*y[1],-3*y[2]],[1,0.2,-0.3,0,0.4,0.1],
(y,a)=>{const e=z=>0.5*(sq(v(z))+z[0]**2+2*z[1]**2+3*z[2]**2);return [close('Hamiltonian',e(y),e(a)),bounded('energy nonnegative',e(y),0,10)];},
{family:'linear Hamiltonian flow',projects:['P05','P06'],equation:'qdot=p; pdot=-diag(1,2,3)q'}),
mechanical('S03','Coupled quartic oscillator',(t,y)=>{const r2=sq(q(y));return [...v(y),...q(y).map(z=>-z*(1+0.3*r2))];},[0.7,0.2,-0.3,0,0.4,0.1],
(y,a)=>{const e=z=>0.5*sq(v(z))+0.5*sq(q(z))+0.075*sq(q(z))**2;return [close('quartic energy',e(y),e(a)),close('angular momentum norm',norm(cross(q(y),v(y))),norm(cross(q(a),v(a))))];},
{family:'nonlinear Hamiltonian flow',projects:['P05','P08'],equation:'qdot=p; pdot=-(1+0.3|q|²)q'}),
mechanical('S04','Damped oscillator',(t,y)=>[...v(y),...q(y).map((z,i)=>-z-0.3*y[i+3])],[1,0.2,-0.3,0,0.4,0.1],
(y,a)=>{const e=z=>0.5*sq(z);return [bounded('energy decreased',e(y),0,e(a)),bounded('dissipation sign',-0.3*sq(v(y)),-10,0)];},
{family:'dissipative flow',projects:['P03','P09'],equation:'qdot=p; pdot=-q-0.3p; Hdot=-0.3|p|²'}),
mechanical('S05','Driven oscillator with work balance',(t,y)=>{const force=0.4*Math.sin(2*t);return [...v(y),-y[0]+force,-y[1],-y[2],force*y[3]];},[0.3,0.2,0.1,0,0.1,0.2,0],
(y,a)=>{const e=z=>0.5*(sq(q(z))+sq(v(z)));return [close('energy minus injected work',e(y)-y[6],e(a)-a[6]),bounded('finite work',y[6],-10,10)];},
{family:'nonautonomous driven flow',projects:['P03','P07','P09'],equation:'qddot=-q+0.4 sin(2t)e1; Wdot=0.4 sin(2t)p1',counterexample:'Energy of the driven subsystem alone is not conserved.'}),
mechanical('S06','Lorentz gyromotion',(t,y)=>[...v(y),0.8*y[4],-0.8*y[3],0],[1,0,0.3,0,1,0.2],
(y,a)=>[close('speed squared',sq(v(y)),sq(v(a))),close('guiding-centre x',y[0]+y[4]/0.8,a[0]+a[4]/0.8),close('guiding-centre y',y[1]-y[3]/0.8,a[1]-a[3]/0.8)],
{family:'antisymmetric velocity coupling',projects:['P03','P06'],equation:'qdot=v; vdot=v cross (0,0,0.8)'}),
mechanical('S07','Inclined Kepler orbit',(t,y)=>{const r=norm(q(y));if(r<0.05)throw Error('Collision boundary');return [...v(y),...q(y).map(z=>-z/r**3)];},[1,0,0,0,0.8,0.6],
(y,a)=>{const e=z=>0.5*sq(v(z))-1/norm(q(z));return [close('orbital energy',e(y),e(a)),close('angular momentum norm',norm(cross(q(y),v(y))),norm(cross(q(a),v(a)))),close('circular radius',norm(q(y)),1)];},
{family:'inverse-square central force',projects:['P04','P12'],equation:'qddot=-q/|q|³; Gm=1'}),
mechanical('S08','Three-cell diffusion',(t,y)=>[0.4*(y[1]-y[0])+0.5*(y[2]-y[0]),0.4*(y[0]-y[1])+0.2*(y[2]-y[1]),0.5*(y[0]-y[2])+0.2*(y[1]-y[2])],[1,2,0],
(y,a)=>[close('total heat proxy',sum(y),sum(a),1e-10),bounded('squared norm contracts',sq(y),0,sq(a)),bounded('minimum remains nonnegative',Math.min(...y),0,2)],
{family:'graph diffusion semigroup',projects:['P06','P13'],axes:['cell1','cell2','cell3'],equation:'udot=-L u, symmetric weighted graph Laplacian'}),
mechanical('S09','Three-cell Klein Gordon wave',(t,y)=>{const l=lap(q(y));return [...v(y),...l.map((z,i)=>z-0.4*y[i])];},[1,0,-0.5,0,0.3,-0.2],
(y,a)=>{const e=z=>0.5*sq(v(z))+0.2*sq(q(z))+0.5*sum(q(z).map((u,i)=>(u-z[(i+1)%3])**2));return [close('lattice energy',e(y),e(a)),bounded('energy positive',e(y),0,20)];},
{family:'discrete hyperbolic field',projects:['P03','P05'],axes:['phi1','phi2','phi3'],equation:'phiddot=Delta phi-0.4 phi; periodic three-cell lattice'}),
mechanical('S10','Bistable reaction diffusion',(t,y)=>{const l=lap(y);return y.map((z,i)=>z-z**3+0.2*l[i]);},[-0.8,0.2,0.9],
(y,a)=>{const e=z=>sum(z.map(u=>(u*u-1)**2/4))+0.1*sum(z.map((u,i)=>(u-z[(i+1)%3])**2));return [bounded('Lyapunov potential decreases',e(y),0,e(a)),bounded('bounded finite states',Math.max(...y.map(Math.abs)),0,1.5)];},
{family:'nonlinear gradient flow',projects:['P06','P08'],axes:['u1','u2','u3'],equation:'udot=u-u³+0.2 Delta u'}),
mechanical('S11','Continuous time Markov chain',(t,p)=>[-0.5*p[0]+0.2*p[1]+0.1*p[2],0.3*p[0]-0.6*p[1]+0.2*p[2],0.2*p[0]+0.4*p[1]-0.3*p[2]],[1,0,0],
(y)=>[close('probability normalization',sum(y),1,1e-10),bounded('nonnegative probability',Math.min(...y),0,1),bounded('maximum probability',Math.max(...y),0,1)],
{family:'probability transport',projects:['P07','P13'],axes:['p1','p2','p3'],equation:'pdot=Q^T p; rows of Q sum to zero'}),
mechanical('S12','Three-patch logistic growth',(t,y)=>{const l=lap(y);return y.map((z,i)=>0.6*z*(1-z)+0.1*l[i]);},[0.2,0.4,0.7],
(y)=>[bounded('population lower boundary',Math.min(...y),0,1),bounded('carrying-capacity upper boundary',Math.max(...y),0,1)],
{family:'bounded nonlinear population flow',projects:['P08','P46'],axes:['patch1','patch2','patch3'],equation:'ndot=0.6 n(1-n)+0.1 Delta n',claim:'Synthetic teaching model; no farm-management prediction.'}),
mechanical('S13','Rock paper scissors replicator',(t,p)=>[p[0]*(p[2]-p[1]),p[1]*(p[0]-p[2]),p[2]*(p[1]-p[0])],[0.2,0.3,0.5],
(y,a)=>[close('simplex sum',sum(y),1,1e-10),close('interior product invariant',y[0]*y[1]*y[2],a[0]*a[1]*a[2],1e-7),bounded('simplex positivity',Math.min(...y),0,1)],
{family:'frequency-dependent game flow',projects:['P07','P42'],axes:['strategy1','strategy2','strategy3'],equation:'pdot_i=p_i (Ap)_i; A antisymmetric, zero-sum'}),
mechanical('S14','Reversible mass action reaction',(t,y)=>{const flux=1.2*y[0]*y[1]-0.8*y[2]**2;return [-flux,-flux,2*flux];},[0.9,0.3,0.2],
(y,a)=>[close('stoichiometric total',sum(y),sum(a),1e-10),close('A minus B',y[0]-y[1],a[0]-a[1],1e-10),bounded('nonnegative concentrations',Math.min(...y),0,sum(a))],
{family:'nonlinear stoichiometric kinetics',projects:['P03','P13','P49'],axes:['A','B','C'],equation:'A+B <-> 2C; J=1.2AB-0.8C²'}),
mechanical('S15','Spherical pendulum',(t,y)=>{const qq=q(y),vv=v(y),coef=y[2]-sq(vv);return [...vv,coef*qq[0],coef*qq[1],-1+coef*qq[2]];},[1,0,0,0,0.6,0.2],
(y,a)=>[close('unit-sphere constraint',sq(q(y)),1),close('tangent velocity',dot(q(y),v(y)),0),close('pendulum energy',0.5*sq(v(y))+y[2],0.5*sq(v(a))+a[2])],
{family:'constrained manifold dynamics',projects:['P05','P06'],equation:'qddot=-e3+(q3-|qdot|²)q; |q|=1'})
];
export function rk4(f,t,y,h){
 const k1=f(t,y), k2=f(t+h/2,y.map((z,i)=>z+h*k1[i]/2));
 const k3=f(t+h/2,y.map((z,i)=>z+h*k2[i]/2)), k4=f(t+h,y.map((z,i)=>z+h*k3[i]));
 for(const k of [k1,k2,k3,k4])if(k.length!==y.length||k.some(z=>!Number.isFinite(z)))throw Error('Derivative shape or finite-value violation');
 const next=y.map((z,i)=>z+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6);
 if(next.some(z=>!Number.isFinite(z)))throw Error('Nonfinite trajectory');
 return next;
}
export function simulate(model,{steps=200,duration=4,hooks={}}={}){
 if(!Number.isInteger(steps)||steps<1||steps>200000||!Number.isFinite(duration)||duration<=0)throw Error('Invalid bounded integration request');
 hooks.admission?.({model:model.id,steps,duration});
 let y=[...model.y0], t=0;const h=duration/steps, trajectory=[];
 const started=performance.now();
 for(let i=0;i<=steps;i++){
   if(i%Math.max(1,Math.floor(steps/40))===0||i===steps)trajectory.push({t,state:[...y]});
   if(i===steps)break;
   hooks.beforeStep?.({model:model.id,step:i});
   y=rk4(model.f,t,y,h);t=(i+1)*h;
 }
 const checks=model.invariants(y,model.y0,duration);
 hooks.modelComplete?.({model:model.id,checks});
 const result={id:model.id,title:model.title,family:model.family,projects:model.projects,dimension:model.dimension,axes:model.axes,equation:model.equation,claim:model.claim??'Bounded synthetic dynamical model; no GMUT or empirical validation.',counterexample:model.counterexample??null,steps,duration,final:y,checks,passed:checks.every(c=>c.pass),trajectory,elapsed_ms:performance.now()-started};
 hooks.evidenceReady?.({model:model.id,passed:result.passed});
 return result;
}
export function runSuite(options={}){
 const lifecycle=createLifecycleHooks();
 const {events,hooks}=lifecycle;
 const results=models.map(m=>simulate(m,{...options,hooks}));
 hooks.publicationReview({allPassed:results.every(r=>r.passed)});
 return {schema:'ghc.synthetic-dynamics.v1',session:'x1',author:'Saelin Reed',scope:'15 distinct mathematical structures; manual lifecycle hooks; local bounded workload',model_count:results.length,distinct_families:new Set(results.map(r=>r.family)).size,check_count:sum(results.map(r=>r.checks.length)),all_passed:results.every(r=>r.passed),hooks:{kind:'manually invoked library guards',installed_host_hooks:false,events,...lifecycle.summary()},results};
}
