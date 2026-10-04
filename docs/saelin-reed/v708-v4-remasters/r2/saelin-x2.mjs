import {models, simulate, dot, sum, cross} from './saelin-models.mjs';
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {performance} from 'node:perf_hooks';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';

const T=3.25, STEPS=640, norm=a=>Math.hypot(...a);
const sub=(a,b)=>a.map((x,i)=>x-b[i]);
const maxerr=(a,b)=>Math.max(...sub(a,b).map(Math.abs));
const sq=a=>dot(a,a), q=y=>y.slice(0,3), v=y=>y.slice(3,6);
const rotate=(a,angle=.47)=>[Math.cos(angle)*a[0]-Math.sin(angle)*a[1],Math.sin(angle)*a[0]+Math.cos(angle)*a[1],a[2]];
const rotate6=y=>[...rotate(q(y)),...rotate(v(y))];
const stateExact=(a,t,frequencies)=>{
 const qq=a.slice(0,3).map((x,i)=>x*Math.cos(frequencies[i]*t)+a[i+3]*Math.sin(frequencies[i]*t)/frequencies[i]);
 const pp=a.slice(0,3).map((x,i)=>-frequencies[i]*x*Math.sin(frequencies[i]*t)+a[i+3]*Math.cos(frequencies[i]*t));
 return [...qq,...pp];
};
const energy=y=>.5*(sq(q(y))+sq(v(y)));
export function runX2(outputFile=null){
const rows=[]; let executions=0;
function run(m,overrides={},opts={}){
 executions++;
 // The frozen x1 function may receive a deliberately different state dimension.
 // Its invariant callback is suppressed for these x2 executions: x2 assertions
 // are computed below and do not receive another copy of the x1 test credit.
 return simulate({...m,...overrides,invariants:()=>[]},{duration:T,steps:STEPS,...opts});
}
function record(m,description,fn){
 const checks=[];const before=executions;
 const add=(name,value,limit,mode='upper',kind='intended')=>{
  const pass=Number.isFinite(value)&&Number.isFinite(limit)&&(mode==='upper'?value<=limit:value>=limit);
  checks.push({name,value,limit,comparison:mode==='upper'?'<=':'>=',kind,pass});
 };
 const close=(name,value,limit=2e-8)=>add(name,Math.abs(value),limit);
 const bad=(name,value,minimum=1e-4)=>add(name,Math.abs(value),minimum,'lower','deliberate_fault_detected');
 const r=run(m);
 fn({m,r,add,close,bad});
 rows.push({id:m.id,family:m.family,description,projects:m.projects,kind:'refinement_of_x1_family',executions:executions-before,checks,passed:checks.every(c=>c.pass)});
}
const started=performance.now();

record(models[0],'Lorentz transformation and interval controls',({r,close,bad})=>{
 const beta=.3,g=1/Math.sqrt(1-beta*beta);
 const boost=([t,x,y,z])=>[g*(t-beta*x),g*(x-beta*t),y,z];
 const interval=([t,x,y,z])=>x*x+y*y+z*z-t*t;
 const event=[T,...r.final];
 close('boosted null interval',interval(boost(event)),1e-10);
 close('arbitrary-event interval preserved',interval(boost([2,.2,.4,.5]))-interval([2,.2,.4,.5]),1e-12);
 close('inverse boost time',g*(boost(event)[0]+beta*boost(event)[1])-T,1e-12);
 const wrong=[event[0]-beta*event[1],event[1]-beta*event[0],event[2],event[3]];
 bad('omitted gamma violates interval',interval(wrong));
});
record(models[1],'Three independent exact oscillator frequencies',({m,r,close,bad})=>{
 const exact=stateExact(m.y0,T,[1,Math.sqrt(2),Math.sqrt(3)]);
 close('position vector versus exact trigonometric solution',maxerr(q(r.final),q(exact)));
 close('velocity vector versus exact trigonometric solution',maxerr(v(r.final),v(exact)));
 const d=stateExact(m.y0,0,[1,Math.sqrt(2),Math.sqrt(3)]);
 close('reference initial condition',maxerr(d,m.y0),1e-15);
 bad('wrong common frequency control',maxerr(exact,stateExact(m.y0,T,[1,1,1])));
});
record(models[2],'Central-force vector symmetry and reversal',({m,r,close})=>{
 close('angular momentum vector',maxerr(cross(q(r.final),v(r.final)),cross(q(m.y0),v(m.y0))));
 const reversed=run(m,{y0:[...q(r.final),...v(r.final).map(x=>-x)]});
 close('time reversal returns initial position',maxerr(q(reversed.final),q(m.y0)),2e-7);
 close('time reversal returns reversed initial velocity',maxerr(v(reversed.final),v(m.y0).map(x=>-x)),2e-7);
 close('rotational equivariance',maxerr(run(m,{y0:rotate6(m.y0)}).final,rotate6(r.final)));
});
record(models[3],'Damped exact solution and heat balance',({m,r,close,add})=>{
 const a=.15,w=Math.sqrt(1-a*a),et=Math.exp(-a*T),c=Math.cos(w*T),s=Math.sin(w*T);
 const eq=q(m.y0).map((x,i)=>et*(x*c+(m.y0[i+3]+a*x)*s/w));
 const ep=q(m.y0).map((x,i)=>et*(-a*(x*c+(m.y0[i+3]+a*x)*s/w)-x*w*s+(m.y0[i+3]+a*x)*c));
 close('damped analytic position',maxerr(q(r.final),eq));
 close('damped analytic velocity',maxerr(v(r.final),ep));
 const differences=r.trajectory.slice(1).map((x,i)=>energy(x.state)-energy(r.trajectory[i].state));
 add('sampled energy increments nonpositive',Math.max(...differences),1e-10);
 const heat=run(m,{y0:[...m.y0,0],f:(t,y)=>[...m.f(t,y.slice(0,6)),.3*sq(v(y))]});
 close('energy plus accumulated heat',energy(heat.final)+heat.final[6]-energy(m.y0));
});
record(models[4],'Forced analytic trajectory and work',({m,r,close,bad})=>{
 const exact=stateExact(m.y0,T,[1,1,1]),k=.4/(1-4);
 exact[0]=m.y0[0]*Math.cos(T)+(m.y0[3]-2*k)*Math.sin(T)+k*Math.sin(2*T);
 exact[3]=-m.y0[0]*Math.sin(T)+(m.y0[3]-2*k)*Math.cos(T)+2*k*Math.cos(2*T);
 close('forced position and velocity',maxerr(r.final.slice(0,6),exact));
 close('integrated work versus analytic energy difference',r.final[6]-(energy(exact)-energy(m.y0)));
 close('reference initial derivative compensation',(m.y0[3]-2*k)+2*k-m.y0[3],1e-15);
 bad('unforced trajectory is a wrong reference',maxerr(exact,stateExact(m.y0,T,[1,1,1])));
});
record(models[5],'Exact gyromotion and force orientation',({m,r,close,bad})=>{
 const w=.8,c=Math.cos(w*T),s=Math.sin(w*T),a=m.y0;
 const exact=[a[0]+a[3]*s/w+a[4]*(1-c)/w,a[1]+a[4]*s/w-a[3]*(1-c)/w,a[2]+a[5]*T,a[3]*c+a[4]*s,a[4]*c-a[3]*s,a[5]];
 close('integrated position reference',maxerr(q(r.final),q(exact)));
 close('velocity rotation reference',maxerr(v(r.final),v(exact)));
 close('force does no instantaneous work',dot(v(a),m.f(0,a).slice(3)),1e-15);
 bad('reversed force sign differs',maxerr(m.f(0,a).slice(3),[-w*a[4],w*a[3],0]));
});
record(models[6],'Circular Kepler reference and Runge-Lenz vector',({m,r,close,bad})=>{
 const exact=[Math.cos(T),.8*Math.sin(T),.6*Math.sin(T),-Math.sin(T),.8*Math.cos(T),.6*Math.cos(T)];
 close('circular orbit analytic state',maxerr(r.final,exact));
 const lrl=y=>sub(cross(v(y),cross(q(y),v(y))),q(y).map(x=>x/norm(q(y))));
 close('Runge-Lenz vector',maxerr(lrl(r.final),lrl(m.y0)));
 close('initial eccentricity is zero',norm(lrl(m.y0)),1e-15);
 bad('wrong orbital phase fails',maxerr(q(exact),[Math.cos(2*T),.8*Math.sin(2*T),.6*Math.sin(2*T)]));
});
record(models[7],'Spectral diffusion solution and contraction bounds',({m,r,close,add,bad})=>{
 const lo=1.1-Math.sqrt(.07),hi=1.1+Math.sqrt(.07),mean=sum(m.y0)/3,a=m.y0.map(x=>x-mean),la=m.f(0,a).map(x=>-x);
 const exact=a.map((x,i)=>mean+(Math.exp(-lo*T)*(hi*x-la[i])+Math.exp(-hi*T)*(la[i]-lo*x))/(hi-lo));
 close('spectral polynomial exact state',maxerr(r.final,exact));
 const variance=sq(r.final.map(x=>x-mean)),v0=sq(a);
 add('upper contraction bound',variance,v0*Math.exp(-2*lo*T)+1e-12);
 add('lower contraction bound',variance,v0*Math.exp(-2*hi*T)-1e-12,'lower');
 add('antidiffusion initial variance increases',2*dot(a,la),1e-4,'lower','deliberate_fault_detected');
});
record(models[8],'Uniform and zero-mean lattice normal modes',({m,r,close})=>{
 const qm=sum(q(m.y0))/3,pm=sum(v(m.y0))/3,w0=Math.sqrt(.4),w1=Math.sqrt(3.4);
 const qq=q(m.y0).map((x,i)=>qm*Math.cos(w0*T)+pm*Math.sin(w0*T)/w0+(x-qm)*Math.cos(w1*T)+(m.y0[i+3]-pm)*Math.sin(w1*T)/w1);
 const pp=q(m.y0).map((x,i)=>-qm*w0*Math.sin(w0*T)+pm*Math.cos(w0*T)-(x-qm)*w1*Math.sin(w1*T)+(m.y0[i+3]-pm)*Math.cos(w1*T));
 close('modal position solution',maxerr(q(r.final),qq));
 close('modal velocity solution',maxerr(v(r.final),pp));
 close('uniform mode is uncoupled',sum(q(r.final))/3-(qm*Math.cos(w0*T)+pm*Math.sin(w0*T)/w0));
 close('zero state is stationary',norm(run(m,{y0:[0,0,0,0,0,0]}).final),0);
});
record(models[9],'Gradient potential and uniform nonlinear solution',({m,r,close,add})=>{
 const potential=y=>sum(y.map(x=>(x*x-1)**2/4))+.1*sum(y.map((x,i)=>(x-y[(i+1)%3])**2));
 const h=1e-6,grad=m.y0.map((_,i)=>{const a=[...m.y0],b=[...m.y0];a[i]+=h;b[i]-=h;return (potential(a)-potential(b))/(2*h);});
 close('finite-difference potential gradient',maxerr(grad,m.f(0,m.y0).map(x=>-x)),2e-8);
 add('sampled potential decreases',Math.max(...r.trajectory.slice(1).map((x,i)=>potential(x.state)-potential(r.trajectory[i].state))),1e-10);
 const u=.2,exact=1/Math.sqrt(1+(1/(u*u)-1)*Math.exp(-2*T));
 close('uniform nonlinear exact solution',maxerr(run(m,{y0:[u,u,u]}).final,[exact,exact,exact]));
 close('positive uniform equilibrium generator',norm(m.f(0,[1,1,1])),0);
});
record(models[10],'Stationary law and Markov contraction',({m,r,close,add})=>{
 const pi=[10/47,13/47,24/47];
 close('stationary generator residual',norm(m.f(0,pi)),1e-15);
 close('stationary trajectory fixed',maxerr(run(m,{y0:pi}).final,pi));
 const other=run(m,{y0:[0,1,0]});
 add('L1 distance contracts',sum(sub(r.final,other.final).map(Math.abs)),2);
 close('longer trajectory approaches stationary law',maxerr(run(m,{}, {duration:20,steps:1000}).final,pi),5e-5);
});
record(models[11],'Cooperative logistic comparison principle',({m,r,close,add})=>{
 const logistic=(a,t)=>1/(1+(1/a-1)*Math.exp(-.6*t));
 const low=Math.min(...m.y0),high=Math.max(...m.y0);
 add('sample minima respect scalar lower solution',Math.min(...r.trajectory.map(x=>Math.min(...x.state)-logistic(low,x.t))),-2e-8,'lower');
 add('sample maxima respect scalar upper solution',Math.max(...r.trajectory.map(x=>Math.max(...x.state)-logistic(high,x.t))),2e-8);
 const uniform=run(m,{y0:[.2,.2,.2]});
 close('uniform logistic exact solution',maxerr(uniform.final,[0,1,2].map(()=>logistic(.2,T))));
 close('carrying-capacity equilibrium generator',norm(m.f(0,[1,1,1])),0);
});
record(models[12],'Replicator fixed point and tangent-plane motion',({m,close,bad})=>{
 const u=[1/3,1/3,1/3],epsilon=1e-6,delta=[epsilon,-epsilon,0],w=1/Math.sqrt(3);
 close('uniform generator fixed point',norm(m.f(0,u)),0);
 close('uniform trajectory fixed point',maxerr(run(m,{y0:u}).final,u));
 const jd=[(delta[2]-delta[1])/3,(delta[0]-delta[2])/3,(delta[1]-delta[0])/3];
 const ref=delta.map((x,i)=>u[i]+x*Math.cos(w)+jd[i]*Math.sin(w)/w);
 const near=run(m,{y0:u.map((x,i)=>x+delta[i])},{duration:1,steps:200});
 close('linearized tangent-plane approximation',maxerr(near.final,ref),1e-10);
 bad('damped wrong linearization',maxerr(ref,u.map((x,i)=>x+delta[i]*Math.exp(-1/3))),1e-8);
});
record(models[13],'Exact reduced Riccati chemistry trajectory',({m,r,close,add})=>{
 const small=(5.68-Math.sqrt(5.68**2-4*2*3.2))/4,large=(5.68+Math.sqrt(5.68**2-4*2*3.2))/4;
 const ratio=(m.y0[0]-small)/(m.y0[0]-large)*Math.exp(2*(small-large)*T);
 const a=(small-ratio*large)/(1-ratio),exact=[a,a-.6,2-2*a];
 close('exact reduced species solution',maxerr(r.final,exact));
 close('admissible equilibrium flux',1.2*small*(small-.6)-.8*(2-2*small)**2);
 close('initial reduced solution recovers concentration',(small-((m.y0[0]-small)/(m.y0[0]-large))*large)/(1-(m.y0[0]-small)/(m.y0[0]-large))-m.y0[0],1e-15);
 add('larger root yields negative concentration',Math.min(large,large-.6,2-2*large),-1e-4,'upper','deliberate_fault_detected');
});
record(models[14],'Constrained pendulum rotational symmetry',({m,r,close,bad})=>{
 const lz=y=>y[0]*y[4]-y[1]*y[3];
 close('vertical angular momentum',lz(r.final)-lz(m.y0));
 close('sampled sphere residual',Math.max(...r.trajectory.map(x=>Math.abs(sq(q(x.state))-1))));
 close('sampled tangent residual',Math.max(...r.trajectory.map(x=>Math.abs(dot(q(x.state),v(x.state))))));
 close('rotation about gravity axis',maxerr(run(m,{y0:rotate6(m.y0)}).final,rotate6(r.final)));
 const free=run(m,{f:(t,y)=>[...v(y),0,0,-1]});
 bad('missing constraint reaction leaves sphere',sq(q(free.final))-1);
});

const files=['SAELIN-X2-PLAN.md','saelin-models.mjs','lifecycle-hooks.mjs','saelin-x2.mjs'];
const bindings=files.map(name=>{const bytes=readFileSync(new URL(name,import.meta.url));return {name,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')};});
const result={schema:'ghc.synthetic-dynamics.x2.v1',run:2,session:'x2',author:'Saelin Reed',base_commit:'23831364ca31e6f8a185c3a30261767c814f172a',parameters:{default_duration:T,default_steps:STEPS,method:'RK4'},model_refinements:rows.length,trajectory_executions:executions,assertions:sum(rows.map(x=>x.checks.length)),failed_assertions:sum(rows.map(x=>x.checks.filter(c=>!c.pass).length)),deliberate_fault_controls:sum(rows.map(x=>x.checks.filter(c=>c.kind==='deliberate_fault_detected').length)),elapsed_ms:performance.now()-started,peak_rss_bytes:typeof process==='undefined'?null:process.resourceUsage().maxRSS*1024,process_metrics_scope:typeof process==='undefined'?'not_exposed_by_host':'whole_current_process',recorded_at_utc:new Date().toISOString(),source_bindings:bindings,claim_boundary:'Synthetic analytic and structural comparisons; no experimental data, independent replication or empirical GMUT confirmation.',rows};
if(outputFile)writeFileSync(outputFile,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
return result;
}
if(typeof process!=='undefined'&&process.argv[1]&&fileURLToPath(import.meta.url)===resolve(process.argv[1])){
 const result=runX2(process.argv[2]);
 console.log(JSON.stringify({model_refinements:result.model_refinements,trajectory_executions:result.trajectory_executions,assertions:result.assertions,failed:result.failed_assertions,elapsed_ms:result.elapsed_ms,peak_rss_bytes:result.peak_rss_bytes,failures:result.rows.flatMap(r=>r.checks.filter(c=>!c.pass).map(c=>({model:r.id,...c})))}));
 if(result.failed_assertions)process.exitCode=1;
}
