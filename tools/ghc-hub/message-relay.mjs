import {readPrivate,nexusHome} from './private-store.mjs';
import {readRegistry} from './chats.mjs';
import {queueMessage,claimMessage,messageStatus,listMessages,recordMessageReceipt} from './messages.mjs';

const UUID='^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$';
const ALIAS='^[a-z][a-z0-9_-]{0,63}$';
const id={type:'string',pattern:UUID};
const digest={type:'string',pattern:'^[a-f0-9]{64}$'};
const schema=(properties,required=Object.keys(properties))=>({type:'object',properties,required,additionalProperties:false});
export const MESSAGE_TOOLS=Object.freeze([
 {name:'nexus.messages.routes',readOnly:true,description:'List up to 16 selected message routes. Delivery uses an active agent and the native sender, not an automatic server sender.',schema:schema({offset:{type:'integer',minimum:0,maximum:127}},[])},
 {name:'nexus.messages.prepare',readOnly:false,idempotent:true,description:'Save one bounded message draft for a selected alias. Does not send or authorize delivery. Reuse the request ID after an uncertain response.',schema:schema({requestId:id,alias:{type:'string',pattern:ALIAS},body:{type:'string',minLength:1,maxLength:2048}})},
 {name:'nexus.messages.claim',readOnly:false,idempotent:false,description:'Claim an authorized draft once and return the exact native sender arguments. The active caller must verify human authorization and invoke that tool once; this operation itself sends nothing.',schema:schema({requestId:id,messageSha256:digest})},
 {name:'nexus.messages.record',readOnly:false,idempotent:true,description:'Record the caller-reported native sender result for a matching claimed request. This is not provider-signed evidence or recipient completion.',schema:schema({requestId:id,messageSha256:digest,outcome:{enum:['accepted','rejected','unknown']},deliveryReference:{type:'string',pattern:'^[A-Za-z0-9_.:-]{1,160}$'}})},
 {name:'nexus.messages.receipt',readOnly:true,description:'Read a selected request state without resending or exposing its message body. Unknown outcomes require reconciliation.',schema:schema({requestId:id})}
]);

const nativeTool='mcp__codex_app__send_message_to_thread';
function input(name,args){
 const spec=MESSAGE_TOOLS.find(s=>s.name===name);
 if(!spec||!args||typeof args!=='object'||Array.isArray(args)||Object.keys(args).some(k=>!Object.hasOwn(spec.schema.properties,k))||spec.schema.required.some(k=>!Object.hasOwn(args,k)))throw Error('Message arguments refused');
 if(name==='nexus.messages.routes'){
  if(args.offset!==undefined&&(!Number.isInteger(args.offset)||args.offset<0||args.offset>127))throw Error('Message offset refused');
  return;
 }
 if(!new RegExp(UUID).test(args.requestId??''))throw Error('Message ID refused');
 if(Object.hasOwn(args,'messageSha256')&&!/^[a-f0-9]{64}$/.test(args.messageSha256))throw Error('Message digest refused');
 if(name==='nexus.messages.prepare'&&(!new RegExp(ALIAS).test(args.alias??'')||typeof args.body!=='string'||Buffer.byteLength(args.body)>2048))throw Error('Message draft refused');
 if(name==='nexus.messages.record'&&(!['accepted','rejected','unknown'].includes(args.outcome)||!/^[A-Za-z0-9_.:-]{1,160}$/.test(args.deliveryReference??'')))throw Error('Message receipt refused');
}

export function createMessageRelay(c){
 const selectors=readPrivate(nexusHome(c),'mcp/selectors.json',{missing:{schema:'ghc.nexus.mcp-selectors.v1',chats:[]}});
 if(selectors.schema!=='ghc.nexus.mcp-selectors.v1'||!Array.isArray(selectors.chats)||selectors.chats.length>128)throw Error('Message selectors refused');
 const rows=readRegistry(c),bindings=new Map(),targets=new Set();
 for(const entry of selectors.chats){
  const matching=rows.filter(r=>r.id===entry.id&&r.kind===entry.kind);
  if(!new RegExp(ALIAS).test(entry.alias??'')||bindings.has(entry.alias)||matching.length!==1)throw Error('Message selector binding refused');
  const row=matching[0];
  const target=JSON.stringify([row.id.toLowerCase(),row.kind,row.hostId]);
  if(targets.has(target))throw Error('Duplicate message target binding refused');
  targets.add(target);
  bindings.set(entry.alias,{id:row.id.toLowerCase(),kind:row.kind,hostId:row.hostId});
 }
 const selected=(alias,rows=readRegistry(c))=>{
  const b=bindings.get(alias);if(!b)throw Error('Message alias refused');
  const matches=rows.filter(r=>r.id.toLowerCase()===b.id&&r.kind===b.kind&&r.hostId===b.hostId);
  if(matches.length!==1)throw Error('Message binding changed');
  return matches[0];
 };
 const resolveRecord=(requestId)=>{
  const r=messageStatus(c,requestId);
  const aliases=[...bindings].filter(([,b])=>b.id===r.target.threadId&&b.kind===r.target.kind&&b.hostId===r.target.hostId);
  if(aliases.length!==1)throw Error('Message record is outside selected routes');
  return {record:r,alias:aliases[0][0]};
 };
 const project=(record,alias)=>({requestId:record.requestId,alias,messageSha256:record.messageSha256,deliveryState:record.deliveryState,automaticDelivery:false,recipientCompletion:'not_observed',claimAt:record.claim?.claimedAt??null,receipt:record.receipt?{outcome:record.receipt.outcome,recordedAt:record.receipt.recordedAt,evidenceType:record.receipt.evidenceType}:null});
 return async function dispatch(name,args,{signal}={}){
  input(name,args);if(signal?.aborted)throw Error('Cancelled');
  if(name==='nexus.messages.routes'){
   const snapshot=readRegistry(c),idCounts=new Map();
   for(const row of snapshot){const key=row.id.toLowerCase();idCounts.set(key,(idCounts.get(key)??0)+1);}
   const offset=args.offset??0,keys=[...bindings.keys()],items=keys.slice(offset,offset+16).map(alias=>{
    let row;try{row=selected(alias,snapshot);}catch{return {alias,state:'binding_changed'};}
    const age=Date.now()-Date.parse(row.observedAt);
    return {alias,provider:row.kind,state:row.held?'held':!['codex-local','codex-managed','chatgpt'].includes(row.kind)?'unsupported':idCounts.get(row.id.toLowerCase())!==1?'ambiguous_target':row.kind!=='chatgpt'&&(!row.hostId||!row.hostId.trim())?'host_binding_missing':!['idle','notLoaded','active'].includes(row.status)?'refresh_required':!Number.isFinite(age)||age<0||age>300000?'refresh_required':'agent_relay',automaticDelivery:false};
   });
   return {items,nextOffset:offset+items.length<keys.length?offset+items.length:null,nativeTool,serverSenderAvailable:false};
  }
  if(name==='nexus.messages.prepare'){
   const row=selected(args.alias);
   let existing=false;try{messageStatus(c,args.requestId);existing=true;}catch{}
   if(!existing&&listMessages(c).messages.length>=128)throw Error('Message outbox capacity reached');
   const q=queueMessage(c,{requestId:args.requestId,toId:row.id,body:args.body},{draft:true});
   if(q.status!=='saved')return {status:q.status,reason:q.reason,automaticDelivery:false};
   const r=resolveRecord(args.requestId);return {...project(r.record,r.alias),requiresCurrentHumanAuthorization:true};
  }
  const {record,alias}=resolveRecord(args.requestId);
  if(name==='nexus.messages.receipt')return project(record,alias);
  if(record.messageSha256!==args.messageSha256)throw Error('Message digest mismatch');
  if(name==='nexus.messages.claim'){
   selected(alias);
   const full=messageStatus(c,args.requestId,{includeBody:true});
   if(Buffer.byteLength(full.request.body)>2048)throw Error('Existing message exceeds MCP relay body limit; use the local reviewed operator');
   const claim=claimMessage(c,args.requestId);
   if(claim.status!=='saved')return {status:claim.status,reason:claim.reason,deliveryState:claim.deliveryState??record.deliveryState,automaticDelivery:false};
   return {...project(messageStatus(c,args.requestId),alias),nativeAction:claim.nativeAction,requiresCurrentHumanAuthorization:true,note:'No message was sent by this tool. Invoke the exact supported native action once; record its result. Never retry an uncertain send.'};
  }
  const result=recordMessageReceipt(c,{requestId:args.requestId,messageSha256:args.messageSha256,threadId:record.target.threadId,hostId:record.target.hostId,outcome:args.outcome,tool:nativeTool,deliveryReference:args.deliveryReference});
  return project(result,alias);
 };
}
