'use strict';
// Finite laboratory only. Inputs named "trusted" must be derived outside tool arguments.
const crypto=require('node:crypto');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const fail=code=>({ok:false,code});
const token=x=>typeof x==='string'&&/^[A-Za-z0-9_.:-]{1,128}$/.test(x);
function ownRecord(x,required,optional=[]){
 if(!x||typeof x!=='object'||Array.isArray(x)||![null,Object.prototype].includes(Object.getPrototypeOf(x)))return false;
 const d=Object.getOwnPropertyDescriptors(x),allowed=new Set([...required,...optional]);
 return Reflect.ownKeys(d).every(k=>typeof k==='string'&&allowed.has(k)&&Object.hasOwn(d[k],'value'))&&required.every(k=>Object.hasOwn(d,k));
}
function createReviewGate(registry,policy,context){
 if(!Array.isArray(registry)||registry.length<1||registry.length>100)throw Error('registry');
 if(!ownRecord(policy,['minimum','empirical','exploratory']))throw Error('policy');
 const rules={minimum:policy.minimum,empirical:policy.empirical,exploratory:policy.exploratory};
 if(!Object.values(rules).every(n=>Number.isSafeInteger(n)&&n>=1&&n<=100)||rules.empirical+rules.exploratory>rules.minimum)throw Error('policy');
 if(!ownRecord(context,['audience','nonce','epoch','action','notBefore','expiresAt'])||!token(context.audience)||!token(context.nonce)||!Number.isSafeInteger(context.epoch)||context.epoch<0||typeof context.action!=='string'||!/^[a-f0-9]{64}$/.test(context.action)||![context.notBefore,context.expiresAt].every(Number.isSafeInteger)||context.notBefore<0||context.expiresAt<=context.notBefore||context.expiresAt-context.notBefore>300000)throw Error('context');
 const expected=Object.freeze({...context}),actors=new Map();
 for(const r of registry){
  if(!ownRecord(r,['id','role','publicKey'],['revoked'])||!token(r.id)||actors.has(r.id)||!['empirical','exploratory'].includes(r.role)||(r.revoked!==undefined&&typeof r.revoked!=='boolean'))throw Error('registry');
  if(typeof r.publicKey!=='string'||r.publicKey.length>4096||!r.publicKey.startsWith('-----BEGIN PUBLIC KEY-----'))throw Error('key');
  let key;try{key=crypto.createPublicKey(r.publicKey);}catch{throw Error('key');}
  if(key.type!=='public'||key.asymmetricKeyType!=='ed25519')throw Error('key');
  // The exact internally parsed key supplies verification and fingerprint bytes.
  actors.set(r.id,Object.freeze({key,fingerprint:hash(key.export({format:'der',type:'spki'})),role:r.role,revoked:r.revoked===true}));
 }
 function verify(proof,now){
  try{
   if(!ownRecord(proof,['raw','signature'])||typeof proof.raw!=='string'||Buffer.byteLength(proof.raw)>4096||!proof.raw.isWellFormed()||typeof proof.signature!=='string'||!/^[A-Za-z0-9+/]{86}==$/.test(proof.signature))return fail('shape');
   const b=JSON.parse(proof.raw);
   if(!ownRecord(b,['schema','actor','nonce','audience','expires','epoch','action','decision'])||JSON.stringify(b)!==proof.raw||b.schema!=='ghc.demo-review.v1')return fail('encoding');
   if(!token(b.actor)||!token(b.audience)||!token(b.nonce)||!Number.isSafeInteger(b.epoch)||b.epoch<0||typeof b.action!=='string'||!/^[a-f0-9]{64}$/.test(b.action)||!Number.isSafeInteger(b.expires)||!['approve','reject'].includes(b.decision))return fail('meaning');
   const actor=actors.get(b.actor);if(!actor||actor.revoked)return fail('actor');
   if(!crypto.verify(null,Buffer.from(proof.raw),actor.key,Buffer.from(proof.signature,'base64')))return fail('signature');
   if(!Number.isSafeInteger(now)||now<0)return fail('time');
   if(now<expected.notBefore)return fail('not_yet_valid');
   if(now>=expected.expiresAt||b.expires<=now)return fail('expired');
   if(b.expires!==expected.expiresAt)return fail('expiry_binding');
   for(const k of ['audience','nonce','epoch','action'])if(b[k]!==expected[k])return fail(k);
   return {ok:true,actor:b.actor,decision:b.decision,role:actor.role,keyFingerprint:actor.fingerprint};
  }catch{return fail('malformed');}
 }
 function assess(proofs,now){
  if(!Array.isArray(proofs)||proofs.length>100)return fail('shape');
  const ids=new Set(),keys=new Set();let empirical=0,exploratory=0;
  for(const p of proofs){
   const v=verify(p,now);if(!v.ok)return v;
   if(ids.has(v.actor))return fail('duplicate_reviewer');if(keys.has(v.keyFingerprint))return fail('duplicate_key');
   ids.add(v.actor);keys.add(v.keyFingerprint);if(v.decision==='reject')return fail('dissent');
   if(v.role==='empirical')empirical++;if(v.role==='exploratory')exploratory++;
  }
  if(ids.size<rules.minimum||empirical<rules.empirical||exploratory<rules.exploratory)return fail('insufficient_review');
  return {ok:true,state:'eligible_for_human_review',verifiedKeys:ids.size,empirical,exploratory,executionAuthorized:false,permissionsGranted:false,independentOrganizationsEstablished:false};
 }
 return Object.freeze({verify,assess});
}
function selectMemory(records,wanted,allowedScopes){
 const scopes=['public','shared','private'];
 if(!Array.isArray(records)||records.length>1000||!Array.isArray(wanted)||wanted.length>100||!wanted.every(token)||!Array.isArray(allowedScopes)||allowedScopes.length>3||!allowedScopes.every(s=>typeof s==='string'&&scopes.includes(s)))return fail('metadata');
 const byId=new Map();
 for(const r of records){
  if(!ownRecord(r,['id','parents','scope','sha256'])||!token(r.id)||byId.has(r.id)||!Array.isArray(r.parents)||r.parents.length>32||!r.parents.every(token)||typeof r.scope!=='string'||!scopes.includes(r.scope)||typeof r.sha256!=='string'||!/^[a-f0-9]{64}$/.test(r.sha256))return fail('metadata');
  byId.set(r.id,{id:r.id,parents:[...r.parents],scope:r.scope,sha256:r.sha256});
 }
 const done=new Set(),visiting=new Set(),order=[];
 function visit(id){if(done.has(id))return;if(visiting.has(id))throw Error('cycle');const r=byId.get(id);if(!r)throw Error('missing_record');if(!allowedScopes.includes(r.scope))throw Error('scope_denied');visiting.add(id);for(const parent of r.parents)visit(parent);visiting.delete(id);done.add(id);order.push(id);}
 try{for(const id of wanted)visit(id);return {ok:true,ids:order,sourceHistoryMutated:false,identityTransferProved:false};}catch(e){return fail(e.message);}
}
function admitBudget(total,baselineUsed,currentUsed,reserved,requested,programmeAllowance=null){
 if([total,baselineUsed,currentUsed,reserved,requested].some(x=>!Number.isSafeInteger(x)||x<0)||total===0||currentUsed<baselineUsed||currentUsed>total)return false;
 if(programmeAllowance!==null&&(!Number.isSafeInteger(programmeAllowance)||programmeAllowance<0))return false;
 const [t,b,c,r,q]=[total,baselineUsed,currentUsed,reserved,requested].map(BigInt);
 if(r>t-c||q>t-c-r)return false;
 return programmeAllowance===null||c-b+r+q<=BigInt(programmeAllowance);
}
function capabilities(requested,host,task){
 if(![requested,host,task].every(a=>Array.isArray(a)&&a.length<=100&&a.every(token)))return [];
 return [...new Set(requested)].filter(x=>host.includes(x)&&task.includes(x)).sort();
}
module.exports={createReviewGate,selectMemory,admitBudget,capabilities,contractVersion:2};
