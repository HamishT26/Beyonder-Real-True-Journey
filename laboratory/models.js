(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.GHCModels=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const titles={heat:'Heat diffusion',wave:'Discrete wave',oscillator:'Damped oscillator',reaction:'Reaction and diffusion',entropy:'Probability mixing',queue:'Queue and backpressure',replication:'Replica reconciliation',retry:'Retry budget',graph:'Graph diffusion',coding:'Parity channel',consent:'Consent lifecycle',allocation:'Max-min allocation',voting:'Pairwise preferences',bayes:'Evidence update',remedy:'Correction lineage'};
const finite=x=>typeof x==='number'&&Number.isFinite(x);
const assert=(b,m)=>{if(!b)throw new Error(m);};
const sum=a=>a.reduce((s,x)=>s+x,0);
function validate(q){
 assert(q&&Object.getPrototypeOf(q)===Object.prototype,'object required');
 assert(Object.keys(q).every(k=>['model','variant','steps','parameter'].includes(k)),'unknown field');
 assert(Object.hasOwn(titles,q.model),'unknown model');
 assert(Number.isInteger(q.variant)&&[0,1].includes(q.variant),'variant must be 0 or 1');
 assert(Number.isInteger(q.steps)&&q.steps>=1&&q.steps<=100,'steps must be 1..100');
 if(q.parameter!==undefined)assert(finite(q.parameter)&&q.parameter>=0&&q.parameter<=0.25,'parameter must be 0..0.25');
 return {...q,parameter:q.parameter??(q.variant?0.15:0.1)};
}
function waterfill(demand,capacity){
 assert(Array.isArray(demand)&&demand.length>0&&demand.length<=100&&demand.every(x=>finite(x)&&x>=0),'invalid demand');
 assert(finite(capacity)&&capacity>=0,'invalid capacity');
 const result=demand.map(()=>0);let open=demand.map((_,i)=>i),left=capacity;
 while(open.length&&left>1e-12){const share=left/open.length;const next=[];for(const i of open){const gain=Math.min(share,demand[i]-result[i]);result[i]+=gain;left-=gain;if(result[i]+1e-12<demand[i])next.push(i);}if(next.length===open.length)break;open=next;}
 return result;
}
function compareVectors(a,b){assert(Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&a.length>0&&a.every(Number.isSafeInteger)&&b.every(Number.isSafeInteger)&&a.every(x=>x>=0)&&b.every(x=>x>=0),'invalid vectors');const le=a.every((x,i)=>x<=b[i]),ge=a.every((x,i)=>x>=b[i]);return le&&ge?'equal':le?'before':ge?'after':'concurrent';}
function consentAllows(q){assert(q&&typeof q.subject==='string'&&typeof q.scope==='string'&&finite(q.time)&&finite(q.expires)&&typeof q.withdrawn==='boolean'&&Array.isArray(q.scopes),'invalid consent');return q.subject.length>0&&!q.withdrawn&&q.time<q.expires&&q.scopes.includes(q.scope);}
function claimCheck(q){
 assert(q&&Object.getPrototypeOf(q)===Object.prototype&&Object.keys(q).every(k=>['issuer','subject','claim','evidence','kind'].includes(k)),'invalid claim envelope');
 assert(['issuer','subject','claim','evidence','kind'].every(k=>typeof q[k]==='string'&&q[k].length>0&&q[k].length<=1000),'claim fields required');
 const reserved=['consciousness','personhood','legal_identity','professional_qualification','empirical_gmut'];
 return{state:reserved.includes(q.kind)?'exact_gate':'represented',verified_credential:false,external_authority:false,reason:reserved.includes(q.kind)?'Independent evidence and competent authority are not supplied by this envelope.':'An issuer assertion was represented; its truth has not been established.'};
}
function simulate(input){
 const q=validate(input),v=q.variant,n=q.steps,a=q.parameter,rows=[],frames=[],notes=[];
 const add=(t,points)=>{const f=points.map(p=>({x:p[0],y:p[1],t,value:p[2]}));frames.push(f);rows.push(...f);};
 let metrics={};
 if(q.model==='heat'){
  const size=9;let u=Array.from({length:size*size},(_,i)=>Math.exp(-((i%size-4)**2+(Math.floor(i/size)-4)**2)/(v?6:4)));
  const initial=sum(u);for(let t=0;t<=n;t++){add(t,u.map((z,i)=>[i%size-4,Math.floor(i/size)-4,z]));const old=u;u=old.map((z,i)=>{const x=i%size,y=Math.floor(i/size);return z+a*(old[y*size+(x+1)%size]+old[y*size+(x+size-1)%size]+old[((y+1)%size)*size+x]+old[((y+size-1)%size)*size+x]-4*z);});}
  metrics={initial_mass:initial,final_mass:sum(frames.at(-1).map(p=>p.value)),maximum:Math.max(...frames.at(-1).map(p=>p.value)),boundary:'periodic',grid_size:size};
 }else if(q.model==='wave'){
  const size=16,c=0.5+v*0.1;let u=Array.from({length:size},(_,i)=>Math.sin(2*Math.PI*i/size)),prev=[...u];
  for(let t=0;t<=n;t++){add(t,u.map((z,i)=>[i,0,z]));const next=u.map((z,i)=>2*z-prev[i]+c*c*(u[(i+1)%size]+u[(i+size-1)%size]-2*z));prev=u;u=next;}
  metrics={courant:c,periodic:true};notes.push('Finite difference wave; bounded traces do not establish continuum regularity.');
 }else if(q.model==='oscillator'){
  let x=1,p=0;const dt=0.05,gamma=v?0.1:0.02;
  for(let t=0;t<=n;t++){add(t,[[x,p,(x*x+p*p)/2]]);p=(p-dt*x)/(1+gamma*dt);x+=dt*p;}
  metrics={dt,damping:gamma,initial_energy:0.5,final_energy:frames.at(-1)[0].value};
 }else if(q.model==='reaction'){
  const size=11,growth=v?0.08:0.05;let u=Array.from({length:size},(_,i)=>i===5?0.4:0.02);
  for(let t=0;t<=n;t++){add(t,u.map((z,i)=>[i,growth,z]));u=u.map((z,i)=>z+a*(u[(i+1)%size]+u[(i+size-1)%size]-2*z)+growth*z*(1-z));}
  metrics={growth,interpretation:'dimensionless reaction-diffusion toy; no biological fit'};
 }else if(q.model==='entropy'){
  let p=v?[0.7,0.2,0.1]:[1,0,0];const entropy=p=>-sum(p.filter(x=>x>0).map(x=>x*Math.log2(x)));const initial=entropy(p),trace=[];
  for(let t=0;t<=n;t++){trace.push(entropy(p));add(t,p.map((z,i)=>[i,entropy(p),z]));p=p.map((z,i)=>(1-2*a)*z+a*p[(i+1)%3]+a*p[(i+2)%3]);}
  metrics={initial_entropy:initial,final_entropy:trace.at(-1),entropy_trace:trace};
 }else if(q.model==='queue'){
  let backlog=0,totalIn=0,totalOut=0;const service=v?3:2;
  for(let t=0;t<=n;t++){const arrivals=[0,3,2,1,4][t%5];const served=Math.min(backlog+arrivals,service);backlog+=arrivals-served;totalIn+=arrivals;totalOut+=served;add(t,[[arrivals,served,backlog]]);}
  metrics={total_arrivals:totalIn,total_served:totalOut,backlog,service};
 }else if(q.model==='replication'){
  let left=[0,0],right=[0,0],concurrent=0;
  for(let t=0;t<=n;t++){if(t%2===0)left[0]++;else right[1]++;if(t%(v?5:4)===0){left=left.map((x,i)=>Math.max(x,right[i]));right=[...left];}const state=compareVectors(left,right);if(state==='concurrent')concurrent++;add(t,[[left[0],left[1],state==='concurrent'?1:0],[right[0],right[1],state==='concurrent'?1:0]]);}
  metrics={left,right,concurrent_frames:concurrent};
 }else if(q.model==='retry'){
  const probability=v?0.35:0.6;let expected=0;
  for(let t=0;t<=n;t++){const attempt=t+1,remaining=(1-probability)**attempt;expected+=(1-probability)**t;add(t,[[attempt,expected,remaining]]);}
  metrics={success_probability:probability,maximum_attempts:n+1,expected_attempts:expected,duplicate_after_ack:false};
 }else if(q.model==='graph'){
  const size=v?9:7;let mass=Array.from({length:size},(_,i)=>i===0?1:0);
  for(let t=0;t<=n;t++){add(t,mass.map((z,i)=>[Math.cos(2*Math.PI*i/size),Math.sin(2*Math.PI*i/size),z]));mass=mass.map((z,i)=>(1-2*a)*z+a*mass[(i+1)%size]+a*mass[(i+size-1)%size]);}
  metrics={vertices:size,initial_mass:1,final_mass:sum(frames.at(-1).map(p=>p.value))};
 }else if(q.model==='coding'){
  const bits=v?5:4,parity=w=>{let p=0;for(let i=0;i<bits;i++)p^=(w>>i)&1;return p;};
  for(let t=0;t<=n;t++){const mask=t%(2**bits);add(t,Array.from({length:2**bits},(_,word)=>[word,mask,parity(word)!==parity(word^mask)?1:0]));}
  metrics={bits,detects_odd_weight_errors:true,detects_all_errors:false};
 }else if(q.model==='consent'){
  const expires=v?25:20,withdrawAt=v?12:n+2;let granted=0;
  for(let t=0;t<=n;t++){const allowed=consentAllows({subject:'synthetic-subject',scope:'read',scopes:['read'],time:t,expires,withdrawn:t>=withdrawAt});if(allowed)granted++;add(t,[[expires,withdrawAt,allowed?1:0]]);}
  metrics={expires,withdraw_at:withdrawAt,granted_frames:granted};
 }else if(q.model==='allocation'){
  const demand=v?[1,2,5,8]:[2,4,6,8];
  for(let t=0;t<=n;t++){const capacity=t/n*sum(demand);add(t,waterfill(demand,capacity).map((z,i)=>[i,demand[i],z]));}
  metrics={demand,final_capacity:sum(demand),criterion:'max-min with equal weights; declared synthetic demand'};
 }else if(q.model==='voting'){
  const profiles=v?[[0,1,2],[0,2,1],[1,0,2]]:[[0,1,2],[1,2,0],[2,0,1]],edges=[];
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const margin=sum(profiles.map(p=>p.indexOf(i)<p.indexOf(j)?1:-1));edges.push([i,j,margin]);}
  for(let t=0;t<=n;t++)add(t,edges);const wins=(i,j)=>sum(profiles.map(p=>p.indexOf(i)<p.indexOf(j)?1:-1))>0;
  metrics={condorcet_winner:[0,1,2].find(i=>[0,1,2].every(j=>i===j||wins(i,j)))??null,cycle:wins(0,1)&&wins(1,2)&&wins(2,0),electorate:'three synthetic preference orders'};
 }else if(q.model==='bayes'){
  let alpha=v?2:1,beta=v?2:1;
  for(let t=0;t<=n;t++){if(t>0){if(t%3===0)beta++;else alpha++;}const mean=alpha/(alpha+beta),variance=alpha*beta/((alpha+beta)**2*(alpha+beta+1));add(t,[[alpha,beta,mean]]);metrics={alpha,beta,mean,variance};}
  notes.push('Synthetic Bernoulli observations; posterior does not measure a person, reliability or moral worth.');
 }else if(q.model==='remedy'){
  const records=[{id:'original',kind:'failure',original_success_credit:0,parent:null}];
  for(let t=0;t<=n;t++){if(t>0&&t%(v?4:5)===0)records.push({id:'correction-'+t,kind:'correction',original_success_credit:0,parent:records.at(-1).id});add(t,[[records.length,records.filter(r=>r.kind==='failure').length,records.filter(r=>r.kind==='correction').length]]);}
  metrics={records,original_preserved:records[0].kind==='failure',original_success_credit:0};
 }
 assert(rows.length>0&&rows.length<=10000&&rows.every(r=>Object.values(r).every(finite)),'invalid numerical result');
 return {schema:'ghc.finite-model.v1',request:q,title:titles[q.model],dimensions:['x','y','value','time'],configuration_dimensions:['variant','parameter','steps'],physical_spatial_dimension_claim:false,rows,frames,metrics,notes,evidence:'finite_synthetic_same_owner',empirical_claim:false};
}
return{titles,validate,simulate,waterfill,compareVectors,consentAllows,claimCheck};
});
