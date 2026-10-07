import {createHash} from 'node:crypto';
import {uuid} from './core.mjs';
import {containsCredential} from './content-checks.mjs';
import {readRegistry} from './chats.mjs';
import {nexusHome,readPrivate,writePrivate,listPrivate} from './private-store.mjs';

const digest=value=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const idPath=(id,folder)=>{if(!uuid(id))throw new Error('Invalid message ID');return `messages/${folder}/${id.toLowerCase()}.json`;};
const requestKeys=['requestId','toId','body'];
const receiptKeys=['requestId','messageSha256','threadId','hostId','outcome','tool','deliveryReference'];
const nativeTool='mcp__codex_app__send_message_to_thread';
const exactKeys=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).length===keys.length&&keys.every(k=>Object.hasOwn(value,k));
const timestamp=value=>typeof value==='string'&&value.length<=32&&Number.isFinite(Date.parse(value));
function validTarget(target,toId){
 return exactKeys(target,['threadId','kind','hostId','title'])&&target.threadId===toId&&['codex-local','codex-managed','chatgpt'].includes(target.kind)&&typeof target.title==='string'&&target.title.length<=180&&(target.kind==='chatgpt'?target.hostId===null:typeof target.hostId==='string'&&target.hostId.trim().length>0&&target.hostId.length<=80)&&!containsCredential(target);
}
function validateEvidence(row,kind){
 if(row===null)return;
 const keys=kind==='claim'?['schema','requestId','messageSha256','threadId','hostId','claimedAt']:['schema',...receiptKeys,'recordedAt','evidenceType','recipientCompletion'];
 if(!exactKeys(row,keys)||row.schema!==`ghc.nexus.message-${kind}.v1`||containsCredential(row))throw new Error('Invalid stored message evidence');
 if(kind==='claim'){
  if(!timestamp(row.claimedAt))throw new Error('Invalid stored message claim');
 }else if(!['accepted','rejected','unknown'].includes(row.outcome)||row.tool!==nativeTool||typeof row.deliveryReference!=='string'||!/^[A-Za-z0-9_.:-]{1,160}$/.test(row.deliveryReference)||!timestamp(row.recordedAt)||row.evidenceType!=='caller-reported-native-tool-result'||row.recipientCompletion!=='not_observed')throw new Error('Invalid stored message receipt');
}
function request(raw){
 if(!raw||typeof raw!=='object'||Array.isArray(raw)||Object.keys(raw).some(k=>!requestKeys.includes(k))||!uuid(raw.requestId)||!uuid(raw.toId)||typeof raw.body!=='string'||!raw.body.trim()||Buffer.byteLength(raw.body)>16384||/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u061c\u200e\u200f\u202a-\u202e\u2066-\u206f]/u.test(raw.body)||containsCredential(raw))throw new Error('Invalid message request');
 return {requestId:raw.requestId.toLowerCase(),toId:raw.toId.toLowerCase(),body:raw.body};
}
export function messagePlan(c,raw,{now=Date.now()}={}){
 const input=request(raw), matches=readRegistry(c).filter(r=>r.id.toLowerCase()===input.toId);
 if(matches.length!==1)throw new Error(matches.length?'Ambiguous exact message target':'Exact message target not found');
 const selected=matches[0];
 if(selected.held)return {status:'held',reason:'selected_chat_is_held',requestId:input.requestId};
 if(!['codex-local','codex-managed','chatgpt'].includes(selected.kind))return {status:'unavailable',reason:'native_message_route_not_established',requestId:input.requestId};
 if(selected.kind!=='chatgpt'&&!selected.hostId)return {status:'unverified',reason:'host_binding_missing',requestId:input.requestId};
 const target={threadId:selected.id.toLowerCase(),kind:selected.kind,hostId:selected.kind==='chatgpt'?null:selected.hostId,title:selected.title};
 if(!validTarget(target,input.toId))throw new Error('Invalid message target');
 const payload={...input,target};
 const age=now-Date.parse(selected.observedAt);
 if(!Number.isFinite(age)||age<0||age>300000||!['idle','notLoaded','active'].includes(selected.status))return {status:'unverified',reason:'refresh_native_chat_observation',requestId:input.requestId,target,messageSha256:digest(payload),automaticDelivery:false,requiresCurrentUserAuthorization:true};
 return {status:'ready',schema:'ghc.nexus.message-plan.v1',requestId:input.requestId,messageSha256:digest(payload),target,
  nativeAction:{tool:'mcp__codex_app__send_message_to_thread',arguments:{threadId:target.threadId,...(target.hostId?{hostId:target.hostId}:{}),prompt:input.body}},
  providerStatus:selected.status,observationAt:selected.observedAt,automaticDelivery:false,requiresCurrentUserAuthorization:true,
  note:'An active Codex agent must verify the human authorization, claim this request, use the supported native tool once, and record its acknowledgement. Queuing alone sends nothing. A receipt records the caller observation; it is not a signed provider attestation.'};
}
function readRecord(c,id){
 const row=readPrivate(nexusHome(c),idPath(id,'outbox'));
 if(!exactKeys(row,['schema','request','target','messageSha256','createdAt'])||row.schema!=='ghc.nexus.message.v1'||!timestamp(row.createdAt))throw new Error('Message record not found or malformed');
 const input=request(row.request);
 const target=row.target;
 if(input.requestId!==id.toLowerCase()||!validTarget(target,input.toId)||digest({...input,target})!==row.messageSha256)throw new Error('Message integrity mismatch');
 return row;
}
export function queueMessage(c,raw,options){
 const input=request(raw),root=nexusHome(c),relative=idPath(input.requestId,'outbox'),old=readPrivate(root,relative);
 // Existing request outcome remains authoritative even if its catalogue observation expired.
 // Revalidate live target metadata at claim time, never by discarding the delivery state.
 if(old){const verified=readRecord(c,input.requestId);if(digest(request(verified.request))!==digest(input))throw new Error('Message ID already has different content');return {...messageStatus(c,input.requestId),status:'saved',alreadyQueued:true};}
 const p=messagePlan(c,input,options);
 // An explicit draft may preserve a stale destination observation, but cannot be
 // claimed until a supported native observation has been refreshed and matched.
 if(p.status!=='ready'&&!(options?.draft===true&&p.status==='unverified'&&p.reason==='refresh_native_chat_observation'))return p;
 const row={schema:'ghc.nexus.message.v1',request:request(raw),target:p.target,messageSha256:p.messageSha256,createdAt:new Date().toISOString()};
 const saved=writePrivate(root,relative,row);
 return {...saved,requestId:p.requestId,messageSha256:p.messageSha256,deliveryState:'queued',requiresFreshObservation:p.status!=='ready',automaticDelivery:false};
}
export function messageStatus(c,id,{includeBody=false}={}){
 const row=readRecord(c,id),root=nexusHome(c),claim=readPrivate(root,idPath(id,'claims')),receipt=readPrivate(root,idPath(id,'receipts'));
 validateEvidence(claim,'claim');validateEvidence(receipt,'receipt');
 if(receipt&&!claim)throw new Error('Stored message receipt is missing its claim');
 for(const evidence of [claim,receipt])if(evidence&&(evidence.requestId!==row.request.requestId||evidence.messageSha256!==row.messageSha256||evidence.threadId!==row.target.threadId||evidence.hostId!==row.target.hostId))throw new Error('Message evidence binding mismatch');
 return {schema:'ghc.nexus.message-status.v1',requestId:row.request.requestId,target:row.target,messageSha256:row.messageSha256,createdAt:row.createdAt,
  deliveryState:receipt?receipt.outcome:claim?'claimed_outcome_unknown':'queued',claim,receipt,automaticDelivery:false,
  ...(includeBody?{request:row.request}:{}),recipientCompletion:'not_observed'};
}
export function listMessages(c){return {messages:listPrivate(nexusHome(c),'messages/outbox').map(n=>messageStatus(c,n.slice(0,-5))),automaticDelivery:false};}
export function claimMessage(c,id,options){
 const row=readRecord(c,id),root=nexusHome(c);
 const current=messageStatus(c,id);
 if(current.deliveryState!=='queued')return {status:'held',reason:'already_claimed_or_receipted_reconcile_without_resending',...current};
 const plan=messagePlan(c,row.request,options);if(plan.status!=='ready')return plan;
 if(plan.messageSha256!==row.messageSha256)throw new Error('Message target changed after queuing');
 const claim={schema:'ghc.nexus.message-claim.v1',requestId:id.toLowerCase(),messageSha256:row.messageSha256,threadId:row.target.threadId,hostId:row.target.hostId,claimedAt:new Date().toISOString()};
 writePrivate(root,idPath(id,'claims'),claim);
 return {...plan,status:'saved',deliveryState:'claimed_outcome_unknown',automaticDelivery:false};
}
export function recordMessageReceipt(c,raw){
 if(!raw||typeof raw!=='object'||Array.isArray(raw)||Object.keys(raw).some(k=>!receiptKeys.includes(k))||!uuid(raw.requestId)||!uuid(raw.threadId)||!['accepted','rejected','unknown'].includes(raw.outcome)||raw.tool!=='mcp__codex_app__send_message_to_thread'||typeof raw.deliveryReference!=='string'||!/^[A-Za-z0-9_.:-]{1,160}$/.test(raw.deliveryReference)||!/^[a-f0-9]{64}$/.test(raw.messageSha256)||containsCredential(raw))throw new Error('Invalid message receipt');
 const current=messageStatus(c,raw.requestId);
 if(!current.claim)throw new Error('Message was not claimed');
 if(current.messageSha256!==raw.messageSha256||current.target.threadId!==raw.threadId||current.target.hostId!==raw.hostId)throw new Error('Receipt target or content mismatch');
 const root=nexusHome(c),relative=idPath(raw.requestId,'receipts'),old=readPrivate(root,relative);
 if(old){if(receiptKeys.every(k=>old[k]===raw[k]))return {status:'saved',alreadyRecorded:true,...current};throw new Error('Receipt already recorded; reconcile without replacement');}
 writePrivate(root,relative,{schema:'ghc.nexus.message-receipt.v1',...raw,recordedAt:new Date().toISOString(),evidenceType:'caller-reported-native-tool-result',recipientCompletion:'not_observed'});
 return {status:'saved',...messageStatus(c,raw.requestId)};
}
