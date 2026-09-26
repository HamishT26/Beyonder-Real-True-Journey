"use strict";
const x1=require("./semigroup-lib-x1.cjs");
function range(n){return Array.from({length:n},(_,i)=>i);}
function validateRequest(request){if(request.real_authority===true)throw new Error("AUTHORITY");const t=request.table;if(!Array.isArray(t)||t.length<2||t.length>5)throw new Error("ORDER");const n=t.length;if(!t.every(r=>Array.isArray(r)&&r.length===n))throw new Error("SQUARE");if(!t.every(r=>r.every(v=>Number.isInteger(v)&&v>=0&&v<n)))throw new Error("CLOSURE");return t;}
function permutations(values){if(values.length===0)return [[]];const out=[];for(let i=0;i<values.length;i++){const rest=[...values.slice(0,i),...values.slice(i+1)];for(const p of permutations(rest))out.push([values[i],...p]);}return out;}
function maps(n){let out=[[]];for(let i=0;i<n;i++){const next=[];for(const p of out)for(let v=0;v<n;v++)next.push([...p,v]);out=next;}return out;}
function automorphisms(t){const n=t.length,accepted=[];for(const p of permutations(range(n))){let ok=true;for(let a=0;a<n&&ok;a++)for(let b=0;b<n;b++)if(p[t[a][b]]!==t[p[a]][p[b]]){ok=false;break;}if(ok)accepted.push(p);}return {count:accepted.length,maps:accepted};}
function endomorphisms(t){const n=t.length,accepted=[];for(const m of maps(n)){let ok=true;for(let a=0;a<n&&ok;a++)for(let b=0;b<n;b++)if(m[t[a][b]]!==t[m[a]][m[b]]){ok=false;break;}if(ok)accepted.push(m);}return {count:accepted.length,maps:accepted};}
function opposite(t){const n=t.length,op=range(n).map(a=>range(n).map(b=>t[b][a])),double=range(n).map(a=>range(n).map(b=>op[b][a]));return {table:op,double_opposite_equal:x1.canonical(double)===x1.canonical(t)};}
function reesQuotient(t){const kernel=x1.minimalIdeal(t).kernel;if(!kernel.length)return {available:false,reason:"NO_UNIQUE_MINIMAL_IDEAL"};const outside=range(t.length).filter(x=>!kernel.includes(x)),zero=outside.length,index=new Map(outside.map((v,i)=>[v,i])),all=[...outside,null],table=all.map(a=>all.map(b=>a===null||b===null?zero:(kernel.includes(t[a][b])?zero:index.get(t[a][b]))));return {available:true,collapsed_ideal:kernel,representatives:outside,zero,table};}
function leftRegular(t){const n=t.length,maps=range(n).map(a=>range(n).map(x=>t[a][x]));let hom=true;for(let a=0;a<n;a++)for(let b=0;b<n;b++){const c=range(n).map(x=>maps[a][maps[b][x]]);if(x1.canonical(c)!==x1.canonical(maps[t[a][b]]))hom=false;}return {maps,homomorphism:hom,faithful:new Set(maps.map(x=>x1.canonical(x))).size===n};}
function relabel(t){const n=t.length,forward=range(n).map(x=>(x+1)%n),inverse=range(n).map(x=>(x-1+n)%n),transported=range(n).map(()=>range(n).map(()=>0));for(let a=0;a<n;a++)for(let b=0;b<n;b++)transported[forward[a]][forward[b]]=forward[t[a][b]];const restored=range(n).map(()=>range(n).map(()=>0));for(let a=0;a<n;a++)for(let b=0;b<n;b++)restored[inverse[a]][inverse[b]]=inverse[transported[a][b]];return {forward,inverse,transported,roundtrip_equal:x1.canonical(restored)===x1.canonical(t)};}
function analyze(request){const t=validateRequest(request),n=t.length;switch(request.operation){
case "automorphism_census":return automorphisms(t);
case "endomorphism_census":return endomorphisms(t);
case "opposite_semigroup":return opposite(t);
case "rees_quotient":return reesQuotient(t);
case "left_regular_representation":return leftRegular(t);
case "relabel_covariance":return relabel(t);
case "accessible_summary":{const g=x1.greens(t),ids=x1.identitiesAndZeros(t);return {text:`${request.profile_id} is an associative table of order ${n} with ${ids.two_sided_identities.length} two-sided identities and ${g.D.length} Green D-classes.`,fields:["profile_id","order","identity_count","D_class_count"]};}
case "uncertainty_annotation":return {status:"represented",known:"exact finite table",unknown:["independent implementation","external semantics"]};
case "external_evidence_gap":return {status:"open_gap",missing:["real observation","independent review","affected-user evaluation"]};
case "authority_gate":return {status:"exact_gate",held:["professional decision","legal or cultural interpretation","Maori authority"]};
default:throw new Error("OPERATION");}}
module.exports={canonical:x1.canonical,analyze};
