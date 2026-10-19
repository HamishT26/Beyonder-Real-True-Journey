'use strict';
// Finite run9 contract models. No I/O, native sending, permission grant or scientific claim.
const id = x => typeof x === 'string' && /^[A-Za-z0-9_-]{1,64}$/.test(x);
function selection({records,selected}) {
 if(!Array.isArray(records)||!Array.isArray(selected)||records.length>1000||selected.length>1000) return {ok:false,code:'shape'};
 const seen=new Map();
 for(const r of records){if(!r||!id(r.id)||!['message','correction','tombstone'].includes(r.kind))return {ok:false,code:'shape'};if(seen.has(r.id))return {ok:false,code:'duplicate'};if(r.kind!=='message'&&(!id(r.target)||!seen.has(r.target)))return {ok:false,code:'target'};seen.set(r.id,r);}
 const pick=new Set(selected);if(pick.size!==selected.length)return {ok:false,code:'duplicate'};
 for(const x of pick)if(!seen.has(x))return {ok:false,code:'missing'};
 for(const r of records)if(r.kind!=='message'&&((pick.has(r.target)&&!pick.has(r.id))||(pick.has(r.id)&&!pick.has(r.target))))return {ok:false,code:'closure'};
 const visible=new Set();for(const r of records){if(!pick.has(r.id))continue;if(r.kind==='message')visible.add(r.id);else {visible.delete(r.target);if(r.kind==='correction')visible.add(r.id);}}
 return {ok:true,visible:[...visible]};
}
function custody({state,event}) {
 if(!state||!event||!Number.isSafeInteger(state.epoch)||state.epoch<0||typeof state.admissionHold!=='boolean'||!Array.isArray(state.used)||state.used.length>2||state.used.some(x=>!id(x))||new Set(state.used).size!==state.used.length||!(state.grant===null||id(state.grant)))return {ok:false,code:'shape'};
 const s={epoch:state.epoch,grant:state.grant,admissionHold:state.admissionHold,used:[...state.used]};
 if(event.type==='revoke'){if(s.epoch===Number.MAX_SAFE_INTEGER)return {ok:false,code:'epoch',...s};return {ok:true,...s,epoch:s.epoch+1,grant:null};}
 if(event.type!=='effect'||!id(event.id))return {ok:false,code:'event',...s};
 if(s.admissionHold)return {ok:false,code:'held',...s};
 if(!id(event.grant)||event.grant!==s.grant)return {ok:false,code:'grant',...s};
 if(s.used.includes(event.id))return {ok:false,code:'duplicate',...s};
 if(s.used.length===2)return {ok:false,code:'capacity',...s,admissionHold:true};
 s.used.push(event.id);return {ok:true,...s};
}
function budget({limit,events}) {
 if(!Number.isSafeInteger(limit)||limit<0||!Array.isArray(events)||events.length>1000)return {ok:false,code:'shape'};
 const pending=new Map(),done=new Set();let committed=0;
 const result=(ok,code)=>({ok,...(code?{code}:{}),committed,reserved:[...pending.values()].reduce((a,b)=>a+b,0)});
 for(const e of events){if(!Array.isArray(e)||e.length!==3||!id(e[1]))return result(false,'shape');const [type,key,amount]=e;
 if(!Number.isSafeInteger(amount)||amount<0)return result(false,'amount');
 if(type==='reserve'){if(pending.has(key)||done.has(key))return result(false,'duplicate');if(amount>limit-committed-result(true).reserved)return result(false,'ceiling');pending.set(key,amount);}
 else if(type==='commit'){if(done.has(key))return result(false,'duplicate');if(!pending.has(key))return result(false,'missing');if(amount!==pending.get(key))return result(false,'price_changed');committed+=amount;pending.delete(key);done.add(key);}
 else if(type==='cancel'){if(!pending.has(key))return result(false,'missing');pending.delete(key);done.add(key);}
 else return result(false,'event');}
 return result(true);
}
function resource({held,samples}) {
 if(typeof held!=='boolean'||!Array.isArray(samples)||samples.length===0||samples.length>1000)return {held:true,admit:false};
 let h=held,admit=false;for(const n of samples){if(typeof n!=='number'||!Number.isFinite(n)||n<0){h=true;admit=false;continue;}if(n<70)h=true;else if(h&&n>200)h=false;admit=!h&&n>=100;}return {held:h,admit};
}
function receipt({expectedBinding,record}) {
 if(!record)return {ok:false,code:'missing'};
 if(!expectedBinding||['request','target','claim'].some(k=>!id(expectedBinding[k])||record[k]!==expectedBinding[k]))return {ok:false,code:'binding'};
 if(!['accepted','queued','unknown','rejected'].includes(record.state))return {ok:false,code:'state'};
 return {ok:true,delivered:record.state==='accepted',completed:false,...(record.state==='unknown'?{retry:false}:{})};
}
module.exports={selection,custody,budget,resource,receipt};
