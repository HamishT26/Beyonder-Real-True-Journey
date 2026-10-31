'use strict';
const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
const reject=reason=>({status:'REJECTED',reason});
const boundedText=(v,n)=>typeof v==='string'&&v.length>0&&v.length<=n;
const only=(o,keys)=>Object.keys(o).every(k=>keys.includes(k));
function index(input){
 if(!object(input)||!only(input,['owner','records','verifiedHumanIds'])||!boundedText(input.owner,128)||!Array.isArray(input.records)||input.records.length>128||!Array.isArray(input.verifiedHumanIds)||input.verifiedHumanIds.length>128||!input.verifiedHumanIds.every(x=>boundedText(x,128)))return reject('SHAPE');
 const ids=new Set(),seqs=new Set(),trusted=new Set(input.verifiedHumanIds),rows=[];
 for(const r of input.records){
  if(!object(r))return reject('RECORD_SHAPE');
  if(r.owner!==input.owner)return reject('OWNER');
  if(r.visible!==true)return reject('HIDDEN_CONTENT');
  if(!only(r,['owner','id','sequence','atUtc','role','origin','visible','sourceSha256','sourceBytes','summary'])||!boundedText(r.id,128)||!Number.isSafeInteger(r.sequence)||r.sequence<0||
   !boundedText(r.atUtc,24)||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(r.atUtc)||!Number.isFinite(Date.parse(r.atUtc))||new Date(r.atUtc).toISOString()!==r.atUtc||
   !['user','assistant'].includes(r.role)||!['human','agent','unknown'].includes(r.origin)||typeof r.sourceSha256!=='string'||!(/^[a-f0-9]{64}$/).test(r.sourceSha256)||
   !Number.isSafeInteger(r.sourceBytes)||r.sourceBytes<0||r.sourceBytes>1048576||typeof r.summary!=='string'||r.summary.length>320)return reject('RECORD_SHAPE');
  if(ids.has(r.id))return reject('DUPLICATE_ID');if(seqs.has(r.sequence))return reject('DUPLICATE_SEQUENCE');ids.add(r.id);seqs.add(r.sequence);
  rows.push({id:r.id,sequence:r.sequence,atUtc:r.atUtc,role:r.role,origin:r.origin,sourceSha256:r.sourceSha256,sourceBytes:r.sourceBytes,summary:r.summary,sharedHumanEligible:r.role==='user'&&r.origin==='human'&&trusted.has(r.id)});
 }
 rows.sort((a,b)=>a.sequence-b.sequence);
 return{status:'OK',orderedIds:rows.map(r=>r.id),sharedHumanIds:rows.filter(r=>r.sharedHumanEligible).map(r=>r.id),count:rows.length,records:rows,trust:'External verifiedHumanIds supplied by caller; this function does not authenticate a human or read message content.'};
}
function decimal(s){
 if(typeof s!=='string'||s.length>28||!(/^(0|[1-9]\d{0,17})(\.\d{1,6})?$/).test(s))throw Error('DECIMAL');
 const [a,b='']=s.split('.');return BigInt(a)*1000000n+BigInt(b.padEnd(6,'0'));
}
const fmt=x=>(x/1000000n).toString()+'.'+(x%1000000n).toString().padStart(6,'0');
function budget(input){
 if(!object(input)||!only(input,['baseline','latest','ceiling','buffer']))return reject('SHAPE');
 let a,b,c,d;try{[a,b,c,d]=['baseline','latest','ceiling','buffer'].map(k=>decimal(input[k]));}catch{return reject('DECIMAL');}
 if(b>a)return{status:'UNKNOWN',reason:'CREDIT_INCREASE_REQUIRES_RECONCILIATION'};
 const spent=a-b,remain=c>spent?c-spent:0n,allow=remain>d?remain-d:0n;
 return{status:'OBSERVED',spent:fmt(spent),remaining:fmt(remain),dispatchAllowance:fmt(allow),ceilingReached:spent>=c};
}
function uniqueGames(input){
 if(!object(input)||!only(input,['vertices','labels','edges'])||!Number.isInteger(input.vertices)||input.vertices<1||input.vertices>8||!Number.isInteger(input.labels)||input.labels<1||input.labels>4||!Array.isArray(input.edges)||input.edges.length>32)return reject('SHAPE');
 const n=input.vertices,k=input.labels,total=k**n;if(total>4096)return reject('SEARCH_BOUND');
 for(const e of input.edges){
  if(!object(e)||!only(e,['u','v','permutation'])||!Number.isInteger(e.u)||!Number.isInteger(e.v)||e.u<0||e.v<0||e.u>=n||e.v>=n)return reject('EDGE');
  if(!Array.isArray(e.permutation)||e.permutation.length!==k||!e.permutation.every(x=>Number.isInteger(x)&&x>=0&&x<k)||new Set(e.permutation).size!==k)return reject('PERMUTATION');
 }
 let best=-1,witness=null;
 for(let state=0;state<total;state++){
  const a=Array(n).fill(0);let rest=state;for(let i=n-1;i>=0;i--){a[i]=rest%k;rest=Math.floor(rest/k);}
  let score=0;for(const e of input.edges)if(a[e.v]===e.permutation[a[e.u]])score++;
  if(score>best){best=score;witness=a;}
 }
 return{status:'EXACT_FINITE',bestSatisfied:best,totalEdges:input.edges.length,assignment:witness,evaluated:total};
}
module.exports={index,budget,uniqueGames};
