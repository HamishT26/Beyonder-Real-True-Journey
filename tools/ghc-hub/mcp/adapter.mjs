import {TextDecoder} from 'node:util';

export const PROTOCOL_VERSION = '2025-11-25';
export const SUPPORTED_PROTOCOL_VERSIONS = Object.freeze([PROTOCOL_VERSION]);
export const SERVER_INFO = Object.freeze({name:'nexus-hub-readonly',version:'0.1.0'});
export const DEFAULT_LIMITS = Object.freeze({lineBytes:32768,outputLineBytes:16384,queuedOutputBytes:65536,sessionInputBytes:1048576,sessionOutputBytes:1048576,messages:512,requestIds:256,jsonDepth:24,jsonNodes:2048,callbacksPerSecond:16,callbackTimeoutMs:2000,writeTimeoutMs:2000});
const specs = Object.freeze([
  ['nexus.chats.list','chatsList','chats',false,'List explicitly selected public chat aliases.'],
  ['nexus.chats.resolve','chatsResolve','chats',true,'Resolve one selected alias without private chat metadata.'],
  ['nexus.chats.plan','chatsPlan','chats',true,'Describe a read-only chat route plan; send no messages.'],
  ['nexus.lab.catalogue','labCatalogue','labs',false,'List explicitly selected lab aliases.'],
  ['nexus.lab.plan','labPlan','labs',true,'Describe a selected lab plan without running it.'],
  ['nexus.identity.summary','identitySummary',null,false,'Return technical component capabilities; omit human personal fields.'],
  ['nexus.sentinel.validate','sentinelValidate','sentinels',true,'Validate one selected Sentinel reference without executing a research phase.'],
  ['nexus.sentinel.plan','sentinelPlan','sentinels',true,'Describe a selected Sentinel plan without executing it.'],
  ['nexus.remote.plan','remotePlan','remotes',true,'Describe a reviewed remote route; open no connection.']
]);
const aliasPattern = '^[a-z][a-z0-9_-]{0,63}$';
const reserved = new Set(['constructor','prototype','__proto__']);
const aliasValid = value => typeof value==='string' && new RegExp(aliasPattern).test(value) && !reserved.has(value);
const object = value => value!==null && typeof value==='object' && !Array.isArray(value);
const has = (value,key) => Object.hasOwn(value,key);
const routes = ['local','cloud','manual','unavailable'];
const steps = ['select','validate','review','handoff'];
const issueCodes = ['missing_input','unsupported_format','unverified_source','invalid_fields','unavailable'];
const fixedToolErrors = Object.freeze({invalid_arguments:'Use the declared input schema and a reviewed selector alias.',operation_failed:'The read-only operation failed. No provider details were returned.',invalid_output:'The operation returned unsupported data.',timeout:'The read-only operation exceeded its time limit.',rate_limited:'The read-only call rate limit was reached.'});
export function wireJson(value) {return JSON.stringify(value).replace(/[\x7f-\x9f\u061c\u200e\u200f\u202a-\u202e\u2066-\u206f]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));}
function rpcError(id,code,message){return {jsonrpc:'2.0',...(id===undefined?{}:{id}),error:{code,message}};}
function success(id,result){return {jsonrpc:'2.0',id,result};}
function toolError(id,code){return success(id,{isError:true,content:[{type:'text',text:fixedToolErrors[code]}]});}
function boundedLimits(custom){
  if(!object(custom)||Object.keys(custom).some(k=>!has(DEFAULT_LIMITS,k)))throw new TypeError('Invalid adapter limits');
  const limits={...DEFAULT_LIMITS,...custom};
  for(const [k,v] of Object.entries(limits))if(!Number.isSafeInteger(v)||v<1||v>DEFAULT_LIMITS[k])throw new TypeError('Invalid adapter limits');
  if(limits.outputLineBytes<1024||limits.queuedOutputBytes<limits.outputLineBytes)throw new TypeError('Invalid adapter limits');
  return Object.freeze(limits);
}
function idValid(id){return (typeof id==='string'&&Buffer.byteLength(id,'utf8')<=128)||(Number.isSafeInteger(id));}
function finiteTree(value,limits,depth=0,count={n:0}){
  if(depth>limits.jsonDepth||++count.n>limits.jsonNodes)return false;
  if(typeof value==='number')return Number.isFinite(value);
  if(value&&typeof value==='object')for(const v of Object.values(value))if(!finiteTree(v,limits,depth+1,count))return false;
  return true;
}
function bool(v){if(typeof v!=='boolean')throw new TypeError();return v;}
function enumeration(v,allowed){if(!allowed.includes(v))throw new TypeError();return v;}
function project(spec,data,args,selectors){
  if(!object(data))throw new TypeError();
  const [name,,domain]=spec;
  if(name==='nexus.chats.list'||name==='nexus.lab.catalogue'){
    if(!Array.isArray(data.items)||data.items.length>128)throw new TypeError();
    const seen=new Set();
    return {items:data.items.map(item=>{if(!object(item)||!selectors[domain].has(item.alias)||seen.has(item.alias))throw new TypeError();seen.add(item.alias);return {alias:item.alias,available:bool(item.available)};})};
  }
  if(name==='nexus.identity.summary'){
    if(!object(data.capabilities))throw new TypeError();
    return {component:'nexus-hub',platform:enumeration(data.platform,['linux','win32','darwin','unknown']),capabilities:Object.fromEntries(['chats','lab','sentinel','remote'].map(k=>[k,bool(data.capabilities[k])]))};
  }
  if(name==='nexus.sentinel.validate'){
    if(![true,false,null].includes(data.valid)||!Array.isArray(data.issues)||data.issues.length>8)throw new TypeError();
    return {alias:args.alias,valid:data.valid,issues:data.issues.map(v=>enumeration(v,issueCodes)),executed:false};
  }
  if(name==='nexus.chats.resolve')return {alias:args.alias,available:bool(data.available),route:enumeration(data.route,routes)};
  if(!Array.isArray(data.steps)||data.steps.length>8)throw new TypeError();
  return {alias:args.alias,available:bool(data.available),route:enumeration(data.route,routes),steps:data.steps.map(v=>enumeration(v,steps)),requiresReview:true,executed:false};
}

/** Dispatch is trusted read-only integration code, not a sandboxed plugin. */
export function createSession({dispatch:invoke,selectors,limits:custom={}}){
  const limits=boundedLimits(custom);
  if(typeof invoke!=='function'||!object(selectors))throw new TypeError('An explicit read-only dispatcher and selector registry are required');
  const callbacks=new Map();
  for(const spec of specs)callbacks.set(spec[0],(args,context)=>invoke(spec[0],args,context));
  const selected={};
  for(const domain of ['chats','labs','sentinels','remotes']){
    const values=selectors[domain];if(!Array.isArray(values)||values.length>128||!values.every(aliasValid)||new Set(values).size!==values.length)throw new TypeError('Invalid selector registry');selected[domain]=new Set(values);
  }
  const tools=specs.map(([name,,,needsAlias,description])=>({name,description,inputSchema:{$schema:'https://json-schema.org/draft/2020-12/schema',type:'object',properties:needsAlias?{alias:{type:'string',pattern:aliasPattern,minLength:1,maxLength:64}}:{},...(needsAlias?{required:['alias']} : {}),additionalProperties:false},annotations:{readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false}}));
  let phase='new',active=null,windowStart=performance.now(),callCount=0;
  const usedIds=new Set();
  function close(){phase='closed';if(active)active.controller.abort();}
  function dispatch(message){
    if(phase==='closed')return null;
    if(!object(message)||message.jsonrpc!=='2.0')return rpcError(undefined,-32600,'Invalid request');
    const notificationEnvelope=!has(message,'id')&&typeof message.method==='string'&&!has(message,'result')&&!has(message,'error');
    if(!finiteTree(message,limits))return notificationEnvelope?null:rpcError(undefined,-32600,'Invalid request');
    if(!has(message,'method')&&(has(message,'result')||has(message,'error')))return null; // No server requests: unsolicited responses are ignored.
    if(typeof message.method!=='string'||has(message,'result')||has(message,'error'))return rpcError(undefined,-32600,'Invalid request');
    const notification=!has(message,'id');
    if(notification){
      if(message.params!==undefined&&!object(message.params))return null;
      if(message.method==='notifications/initialized'&&phase==='initializing')phase='ready';
      if(message.method==='notifications/cancelled'&&active&&idValid(message.params?.requestId)&&message.params.requestId===active.id)active.controller.abort();
      return null; // Never invoke tools/call delivered as a notification.
    }
    if(!idValid(message.id))return rpcError(undefined,-32600,'Invalid request');
    const id=message.id;
    if(usedIds.has(id))return rpcError(id,-32600,'Request ID already used');
    if(usedIds.size>=limits.requestIds){close();return rpcError(id,-32000,'Session request limit reached');}
    usedIds.add(id);
    if(message.params!==undefined&&!object(message.params))return rpcError(id,-32602,'Invalid parameters');
    const params=message.params??{};
    if(params._meta!==undefined&&!object(params._meta))return rpcError(id,-32602,'Invalid parameters');
    if(message.method==='ping')return success(id,{});
    if(message.method==='initialize'){
      if(phase!=='new')return rpcError(id,-32600,'Initialization already started');
      if(typeof params.protocolVersion!=='string'||params.protocolVersion.length>64||!object(params.capabilities)||!object(params.clientInfo)||typeof params.clientInfo.name!=='string'||typeof params.clientInfo.version!=='string')return rpcError(id,-32602,'Invalid initialization parameters');
      const protocolVersion=SUPPORTED_PROTOCOL_VERSIONS.includes(params.protocolVersion)?params.protocolVersion:SUPPORTED_PROTOCOL_VERSIONS[0];
      phase='initializing';return success(id,{protocolVersion,capabilities:{tools:{listChanged:false}},serverInfo:SERVER_INFO});
    }
    if(!['tools/list','tools/call'].includes(message.method))return rpcError(id,-32601,'Method not found');
    if(phase!=='ready')return rpcError(id,-32002,'Initialization required');
    if(message.method==='tools/list'){
      if(Object.keys(params).some(k=>k!=='_meta'))return rpcError(id,-32602,'Invalid parameters');
      return success(id,{tools:structuredClone(tools)});
    }
    if(typeof params.name!=='string'||(params.arguments!==undefined&&!object(params.arguments))||Object.keys(params).some(k=>!['name','arguments','_meta'].includes(k)))return rpcError(id,-32602,'Invalid parameters');
    const spec=specs.find(s=>s[0]===params.name);if(!spec)return rpcError(id,-32602,'Unknown tool');
    const args=params.arguments??{};
    if(spec[3]?Object.keys(args).length!==1||!has(args,'alias')||!aliasValid(args.alias)||!selected[spec[2]].has(args.alias):Object.keys(args).length!==0)return toolError(id,'invalid_arguments');
    if(active)return rpcError(id,-32001,'Read-only operation already in progress');
    if(performance.now()-windowStart>=1000){windowStart=performance.now();callCount=0;}
    if(++callCount>limits.callbacksPerSecond)return toolError(id,'rate_limited');
    const safeArgs=Object.freeze(spec[3]?{alias:args.alias}:{}),controller=new AbortController();
    const operation={id,controller};active=operation;
    const context=Object.freeze({signal:controller.signal,readOnly:true});
    let timer,onAbort;
    const abort=new Promise(resolve=>{onAbort=()=>resolve({kind:'cancelled'});controller.signal.addEventListener('abort',onAbort,{once:true});});
    const timeout=new Promise(resolve=>{timer=setTimeout(()=>resolve({kind:'timeout'}),limits.callbackTimeoutMs);});
    const called=Promise.resolve().then(()=>controller.signal.aborted?{kind:'cancelled'}:Promise.resolve(callbacks.get(spec[0])(safeArgs,context)).then(data=>({kind:'result',data}))).catch(()=>({kind:'failed'}));
    return Promise.race([called,abort,timeout]).then(outcome=>{
      if(outcome.kind==='cancelled'){close();return null;}
      if(outcome.kind==='timeout'){close();return toolError(id,'timeout');}
      if(phase==='closed')return null;
      if(outcome.kind==='failed')return toolError(id,'operation_failed');
      try{const data=project(spec,outcome.data,safeArgs,selected);return success(id,{content:[{type:'text',text:wireJson(data)}],structuredContent:data,isError:false});}catch{return toolError(id,'invalid_output');}
    }).finally(()=>{clearTimeout(timer);controller.signal.removeEventListener('abort',onAbort);if(active===operation)active=null;});
  }
  return Object.freeze({dispatch,close,limits,get phase(){return phase;}});
}

/** Bounded stdio only. The caller owns process lifecycle and trusted callback code. */
export function serveStdio({input,output,...options}){
  const session=createSession(options),limits=session.limits,decoder=new TextDecoder('utf-8',{fatal:true});
  const frame=Buffer.alloc(limits.lineBytes),queue=[];let used=0,inBytes=0,outBytes=0,messageCount=0,queuedBytes=0,writing=false,writeTimer=null,stopped=false,ending=false,stopReason='eof';
  const jobs=new Set();let resolveDone;const done=new Promise(resolve=>{resolveDone=resolve;});
  function finish(reason=stopReason){if(stopped)return;stopped=true;stopReason=reason;clearTimeout(writeTimer);session.close();input.removeListener('data',onData);input.removeListener('end',onEnd);input.pause?.();resolveDone({reason,inputBytes:inBytes,outputBytes:outBytes,messages:messageCount});}
  function maybeFinish(){if(ending&&!writing&&queue.length===0&&jobs.size===0)finish();}
  function pump(){
    if(stopped||writing||queue.length===0){maybeFinish();return;}
    const bytes=queue.shift();writing=true;
    writeTimer=setTimeout(()=>finish('output_timeout'),limits.writeTimeoutMs);
    try{output.write(bytes,error=>{clearTimeout(writeTimer);writing=false;queuedBytes-=bytes.length;if(error){finish('output_error');return;}pump();});}catch{finish('output_error');}
  }
  function send(response){
    if(stopped||response===null)return;
    let text=wireJson(response)+'\n';
    if(Buffer.byteLength(text)>limits.outputLineBytes)text=wireJson(rpcError(idValid(response.id)?response.id:undefined,-32603,'Response limit exceeded'))+'\n';
    const bytes=Buffer.from(text,'utf8');
    if(queuedBytes+bytes.length>limits.queuedOutputBytes||outBytes+bytes.length>limits.sessionOutputBytes){finish('output_limit');return;}
    outBytes+=bytes.length;queuedBytes+=bytes.length;queue.push(bytes);pump();
  }
  function endAfter(reason){if(!ending||stopReason==='eof')stopReason=reason;ending=true;input.pause?.();maybeFinish();}
  function accept(bytes){
    if(++messageCount>limits.messages){send(rpcError(undefined,-32000,'Session message limit reached'));session.close();endAfter('message_limit');return;}
    let value;
    try{value=JSON.parse(decoder.decode(bytes));}catch{send(rpcError(undefined,-32700,'Parse error'));return;}
    let result;try{result=session.dispatch(value);}catch{send(rpcError(undefined,-32603,'Internal error'));return;}
    if(result&&typeof result.then==='function'){
      const job=result.then(send,()=>send(rpcError(undefined,-32603,'Internal error'))).finally(()=>{jobs.delete(job);if(session.phase==='closed')endAfter('operation_stopped');maybeFinish();});jobs.add(job);
    }else{send(result);if(session.phase==='closed')endAfter('session_limit');}
  }
  function onData(chunk){
    if(stopped||ending)return;
    if(!Buffer.isBuffer(chunk)){finish('input_type');return;}
    inBytes+=chunk.length;
    if(inBytes>limits.sessionInputBytes){send(rpcError(undefined,-32000,'Session input limit reached'));session.close();endAfter('input_limit');return;}
    for(let from=0;from<chunk.length&&!stopped&&!ending;){
      const newline=chunk.indexOf(10,from),end=newline===-1?chunk.length:newline,length=end-from;
      if(used+length>limits.lineBytes){send(rpcError(undefined,-32000,'Input line limit exceeded'));session.close();endAfter('line_limit');return;}
      chunk.copy(frame,used,from,end);used+=length;
      if(newline===-1)break;
      const size=used>0&&frame[used-1]===13?used-1:used;accept(frame.subarray(0,size));used=0;from=newline+1;
    }
  }
  function onEnd(){if(used>0)send(rpcError(undefined,-32700,'Incomplete input line'));endAfter('eof');}
  function onInputError(){finish('input_error');}
  function onOutputError(){finish('output_error');}
  // Keep error guards through stream close: writable callbacks can precede error events.
  input.once('close',()=>{input.removeListener('error',onInputError);if(!ending)finish('input_closed');});
  output.once('close',()=>{output.removeListener('error',onOutputError);finish('output_closed');});
  input.on('data',onData);input.once('end',onEnd);input.on('error',onInputError);output.on('error',onOutputError);
  return Object.freeze({done,close:()=>finish('closed')});
}
