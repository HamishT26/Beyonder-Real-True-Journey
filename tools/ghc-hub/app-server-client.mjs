import {spawn} from 'node:child_process';
import {StringDecoder} from 'node:string_decoder';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {checkPath,readPrivate,writePrivate} from './private-store.mjs';

// Only metadata reads are admitted here. Model turns use the official CLI/UI.
const READ_METHODS = new Set(['thread/list','thread/read','thread/loaded/list']);
let unresolvedCleanup=false;
function reserveReader(c){
 if(!c.state)return null;
 const relative='metadata/read-lease.json',record={schema:'ghc.nexus.metadata-lease.v1',id:crypto.randomUUID(),parentPid:process.pid,childPid:null,state:'starting',createdAt:new Date().toISOString()};
 writePrivate(c.state,relative,record);
 return {record,child(pid){record.childPid=pid;record.state='running';if(readPrivate(c.state,relative)?.id!==record.id)throw new Error('Reader lease changed');writePrivate(c.state,relative,record,{replace:true});},release(){if(readPrivate(c.state,relative)?.id===record.id)fs.unlinkSync(checkPath(c.state,relative));}};
}
const threadSummary=t=>({id:t?.id,name:typeof t?.name==='string'?t.name:null,status:t?.status,sessionId:t?.sessionId,createdAt:t?.createdAt,updatedAt:t?.updatedAt,modelProvider:t?.modelProvider});
function metadataParams(method,params){
  if(!params||typeof params!=='object'||Array.isArray(params))throw new Error('Invalid metadata parameters');
  const keys=Object.keys(params);
  if(method==='thread/read'){
    if(keys.some(k=>!['threadId','includeTurns'].includes(k))||!/^[a-f0-9-]{36}$/i.test(params.threadId||'')||(params.includeTurns!==undefined&&params.includeTurns!==false))throw new Error('Summary-only metadata read required');
    return {threadId:params.threadId,includeTurns:false};
  }
  if(method==='thread/loaded/list'){if(keys.length)throw new Error('Invalid metadata parameters');return {};}
  const allowed=['limit','archived','sortKey','sourceKinds','useStateDbOnly','cursor','searchTerm'];
  if(keys.some(k=>!allowed.includes(k))||!Number.isInteger(params.limit)||params.limit<1||params.limit>100||params.archived!==false||params.useStateDbOnly!==true||!['updated_at','created_at','recency_at'].includes(params.sortKey))throw new Error('Invalid metadata parameters');
  if(params.cursor!==undefined&&(typeof params.cursor!=='string'||params.cursor.length>4096))throw new Error('Invalid metadata cursor');
  if(params.searchTerm!==undefined&&(typeof params.searchTerm!=='string'||params.searchTerm.length>200))throw new Error('Invalid metadata search');
  if(!Array.isArray(params.sourceKinds)||params.sourceKinds.some(k=>!['cli','vscode','appServer','exec','unknown'].includes(k)))throw new Error('Invalid metadata sources');
  return params;
}
export function appServerRead(c, method, params = {}, {spawnFn=spawn, timeoutMs=60000}={}) {
  if (!READ_METHODS.has(method)) throw new Error('Unsupported metadata method');
  params=metadataParams(method,params);
  if (!Number.isInteger(timeoutMs) || timeoutMs < 100 || timeoutMs > 60000) throw new Error('Invalid metadata timeout');
  if (!c.codex) return Promise.resolve({status:'unavailable',reason:'codex_not_found'});
  if(unresolvedCleanup&&spawnFn===spawn)return Promise.resolve({status:'unavailable',reason:'prior_child_cleanup_unconfirmed'});
  let lease;try{lease=spawnFn===spawn?reserveReader(c):null;}catch{return Promise.resolve({status:'unavailable',reason:'metadata_reader_busy_or_cleanup_unconfirmed'});}
  return new Promise(resolve=>{
    let child, buffer='', size=0, done=false, response, stopTimer, hardCloseTimer, deadline, spawnObserved=false, initialized=false, requestSent=false, stopping=false, cleanupErrors=0, stdoutBytes=0,stderrBytes=0,protocolLines=0;
    const decoder=new StringDecoder('utf8');
    const finish = value => {if(done)return;done=true;clearTimeout(deadline);clearTimeout(stopTimer);clearTimeout(hardCloseTimer);if(value.childCloseObserved===true||(!spawnObserved&&!child?.pid)){try{lease?.release();}catch{cleanupErrors++;}}resolve({...value,diagnostics:{spawnObserved,childPid:child?.pid??null,stdoutBytes,stderrBytes,protocolLines,initialized,requestSent,cleanupErrors}});};
    const stop = () => {
      if(stopping||done)return;stopping=true;
      try {child.stdin.end();} catch {}
      stopTimer=setTimeout(()=>{
        try{child.kill('SIGKILL');}catch{cleanupErrors++;}
        if(done)return;
        // Windows reports close asynchronously after termination. Keep ownership
        // until that event arrives, instead of declaring a leak immediately.
        hardCloseTimer=setTimeout(()=>{
          for(const action of [()=>child.stdout.destroy(),()=>child.stderr.destroy(),()=>child.stdin.destroy(),()=>child.unref()]){try{action();}catch{cleanupErrors++;}}
          if(spawnFn===spawn)unresolvedCleanup=true;
          finish({...response,childCloseObserved:false});
        },1500);
      },1500);
    };
    const fail = reason => {if(response||done)return;response={status:'unavailable',reason,spawnObserved};stop();};
    const send = value => {try{child.stdin.write(JSON.stringify(value)+'\n');return true;}catch{fail('write_failed');return false;}};
    try{child=spawnFn(c.codex,['--no-daemon','-c','features.apps=false','app-server','--listen','stdio://'],{cwd:c.cwd,shell:false,windowsHide:true,stdio:['pipe','pipe','pipe']});}
    catch {finish({status:'unavailable',reason:'spawn_failed',spawnObserved:false});return;}
    child.on('spawn',()=>{spawnObserved=true;try{lease?.child(child.pid);}catch{fail('reader_lease_unavailable');return;}send({id:1,method:'initialize',params:{clientInfo:{name:'ghc_nexus_metadata',title:'GHC Nexus metadata',version:'2.0.0'},capabilities:{experimentalApi:false}}});});
    child.stdin.on('error',()=>fail('input_closed'));
    child.stdout.on('error',()=>fail('output_pipe_error'));
    child.stderr.on('error',()=>fail('error_pipe_error'));
    child.stderr.on('data',d=>{stderrBytes+=d.length;size+=d.length;if(size>2097152)fail('output_limit');});
    child.stdout.on('data',d=>{
      if(done||response)return;
      stdoutBytes+=d.length;size+=d.length;if(size>2097152){fail('output_limit');return;}
      buffer+=decoder.write(d);
      while(buffer.includes('\n')){
        const i=buffer.indexOf('\n'), line=buffer.slice(0,i);buffer=buffer.slice(i+1);
        if(!line.trim())continue;
        protocolLines++;
        let msg;try{msg=JSON.parse(line);}catch{fail('invalid_protocol');return;}
        if(msg.id===1){
          if(initialized){fail('duplicate_initialization');return;}initialized=true;
          if(msg.error){fail('initialization_rejected');return;}
          if(!msg.result||typeof msg.result!=='object'||Array.isArray(msg.result)){fail('invalid_initialization');return;}
          if(send({method:'initialized',params:{}}))requestSent=send({id:2,method,params});
        }else if(msg.id===2){
          if(!initialized||!requestSent){fail('unexpected_response');return;}
          if(msg.error){fail('metadata_read_rejected');return;}
          const valid=method==='thread/read'?msg.result?.thread?.id===params.threadId:Array.isArray(msg.result?.data);
          if(!valid){fail('invalid_response_shape');return;}
          const data=method==='thread/read'?{thread:threadSummary(msg.result.thread)}:method==='thread/list'?{data:msg.result.data.map(threadSummary),nextCursor:msg.result.nextCursor??null}:{data:msg.result.data.filter(v=>typeof v==='string')};
          response={status:'ok',data,spawnObserved};stop();return;
        }
      }
    });
    child.on('error',()=>{if(!spawnObserved)finish({status:'unavailable',reason:'spawn_failed',spawnObserved:false});else fail('process_error');});
    child.on('close',(code,signal)=>finish(response ? {...response,childCloseObserved:true,exitCode:code,signal:signal||null} : {status:'unavailable',reason:'closed_before_response',exitCode:code,signal:signal||null,childCloseObserved:true}));
    deadline=setTimeout(()=>fail('timeout'),timeoutMs);
  });
}
