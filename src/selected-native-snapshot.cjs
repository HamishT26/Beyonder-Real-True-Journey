'use strict';
const crypto=require('node:crypto');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const fail=code=>{throw Object.assign(new Error(code),{safeCode:code});};
const token=x=>typeof x==='string'&&/^[A-Za-z0-9_.:-]{1,128}$/.test(x);
function parseUnique(raw){let i=0;const ws=()=>{while(/[\t\r\n ]/.test(raw[i]??'!'))i++;};const str=()=>{const start=i++;let closed=false;while(i<raw.length){const c=raw[i++];if(c==='\\')i++;else if(c==='"'){closed=true;break;}}if(!closed)fail('json');try{return JSON.parse(raw.slice(start,i));}catch{fail('json');}};const value=depth=>{if(depth>32)fail('depth');ws();if(raw[i]==='"'){str();return;}if(raw[i]==='{'){i++;ws();const keys=new Set();if(raw[i]==='}'){i++;return;}for(;;){if(raw[i]!=='"')fail('json');const k=str();if(keys.has(k))fail('duplicate_key');keys.add(k);ws();if(raw[i++]!==':')fail('json');value(depth+1);ws();if(raw[i]===','){i++;ws();continue;}if(raw[i++]==='}')return;fail('json');}}if(raw[i]==='['){i++;ws();if(raw[i]===']'){i++;return;}for(;;){value(depth+1);ws();if(raw[i]===','){i++;continue;}if(raw[i++]===']')return;fail('json');}}const s=i;while(i<raw.length&&!/[\s,\]}]/.test(raw[i]))i++;try{JSON.parse(raw.slice(s,i));}catch{fail('json');}};value(0);ws();if(i!==raw.length)fail('json');return JSON.parse(raw);}
function project(raw,expectedThreadId,retrievedAt){try{
 if(typeof raw!=='string')fail('input_type');if(raw.length>524288||Buffer.byteLength(raw)>524288)fail('input_size');
 const p=parseUnique(raw);if(!p||p.schemaVersion!==1||!p.thread||!Array.isArray(p.turns)||p.turns.length>10)fail('shape');
 if(!token(expectedThreadId)||p.thread.id!==expectedThreadId)fail('thread_mismatch');if(!['codex','chatgpt'].includes(p.thread.kind))fail('source_kind');
 if(typeof retrievedAt!=='string'||retrievedAt.length>40||!Number.isFinite(Date.parse(retrievedAt)))fail('retrieval_time');
 const records=[],seen=new Set(),turnsSeen=new Set();let excludedItems=0,omittedContent=0,outputBudget=8192;
 for(const turn of p.turns){if(!turn||!Array.isArray(turn.items)||turn.items.length>1000)fail('turn_shape');if(!token(turn.id)||turnsSeen.has(turn.id))fail('turn_id');turnsSeen.add(turn.id);for(const item of turn.items){
 if(!item||!['userMessage','agentMessage'].includes(item.type)){excludedItems++;continue;}
 if(!token(item.id))fail('message_id');if(seen.has(item.id))fail('duplicate_id');seen.add(item.id);
 let body='',truncated=item.truncated===true,omitted=0;
 if(item.type==='agentMessage'&&typeof item.text==='string')body=item.text;
 else if(Array.isArray(item.content)){if(item.content.length>100)fail('content_limit');const pieces=[];for(const part of item.content){if(part?.type==='text'&&typeof part.text==='string'){pieces.push(part.text);truncated=truncated||part.truncated===true;}else omitted++;}body=pieces.join('\n');}
 else fail('message_shape');
 if(!body.isWellFormed())fail('unicode');if(Buffer.byteLength(body)>32768)fail('message_size');if(records.length>=30)fail('record_limit');omittedContent+=omitted;
 const record={messageId:item.id,turnId:turn.id,role:item.type==='userMessage'?'user':'assistant',phase:typeof item.phase==='string'?item.phase:null,capturedText:body,capturedTextSha256:hash(body),truncatedReported:truncated,textCompleteness:'provider_unverified',omittedContent:omitted};outputBudget+=Buffer.byteLength(JSON.stringify(record))+1024;if(outputBudget>2097152)fail('output_size');records.push(record);
 }}
 if(typeof p.page?.nextCursor==='string'&&(p.page.nextCursor.length>4096||Buffer.byteLength(p.page.nextCursor)>4096||!p.page.nextCursor.isWellFormed()))fail('cursor_size');
 const archive={schema:'ghc.selected-native-snapshot.v1',source:{kind:p.thread.kind??null,threadId:expectedThreadId,retrievedAt,rawEnvelopeSha256:hash(raw),roleSemantics:'provider_role_only',humanAuthorshipEstablished:false},coverage:{kind:'selected_provider_snapshot',messageCount:records.length,excludedItems,omittedContent,providerHistoryComplete:false,nextCursor:typeof p.page?.nextCursor==='string'?p.page.nextCursor:null,hasMore:typeof p.page?.hasMore==='boolean'?p.page.hasMore:null,recordOrder:'provider_return_order',redactionPerformed:false},records,nativeHistoryMutated:false,nativeCacheBytesReclaimed:0};
 const text=JSON.stringify(archive,null,2)+'\n';if(Buffer.byteLength(text)>2097152)fail('output_size');return {ok:true,text,sha256:hash(text),bytes:Buffer.byteLength(text),messageCount:records.length};
 }catch(e){return {ok:false,code:e.safeCode??'invalid_input'};}}
module.exports={project};
