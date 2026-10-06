import {appServerRead} from './app-server-client.mjs';
import {bounded,clean,uuid,findExecutable} from './core.mjs';
import {nexusHome,readPrivate,writePrivate} from './private-store.mjs';

const KINDS=new Set(['codex-local','codex-managed','codex-cloud-task','chatgpt','cli-remote']);
function normalId(value,kind){return kind==='codex-cloud-task'?typeof value==='string'&&/^task_[A-Za-z0-9_-]{1,160}$/.test(value):uuid(value);}
export function normalizeEntry(raw,source,observedAt) {
  if(!raw||typeof raw!=='object'||(!KINDS.has(raw.kind)&&raw.kind!=='codex'))throw new Error('Invalid chat kind');
  const kind=KINDS.has(raw.kind)?raw.kind:raw.hostId==='durable'?'codex-managed':'codex-local';
  if(!normalId(raw.id,kind))throw new Error('Invalid chat ID');
  const title=clean(raw.title||raw.name||'Untitled chat').slice(0,180);
  const rawStatus=typeof raw.status==='object'?raw.status?.type:raw.status;
  const status=['active','idle','notLoaded','systemError','running','completed','failed','pending','queued','ready','cancelled'].includes(rawStatus)?rawStatus:'unknown';
  return {id:raw.id,kind,title,status,hostId:typeof raw.hostId==='string'?clean(raw.hostId).slice(0,80):kind==='codex-local'?'local':null,source:clean(source).slice(0,120),observedAt,held:raw.held===true,reportedActive:raw.reportedActive===true,resumeSettings:'preserve',sessionId:uuid(raw.sessionId)?raw.sessionId:null};
}
export function mergeEntries(groups) {
  const map=new Map();
  for(const group of groups)for(const row of group){
    const key=row.kind+':'+(row.hostId||'unknown-host')+':'+row.id, prev=map.get(key);
    if(!prev){map.set(key,row);continue;}
    const rowAt=Date.parse(row.observedAt),prevAt=Date.parse(prev.observedAt);
    const newer=Number.isFinite(rowAt)&&(!Number.isFinite(prevAt)||rowAt>=prevAt)?row:prev;
    const active=r=>r.status==='active'||r.status==='running'||r.reportedActive===true;
    // Explicit holds survive refresh. Superseded activity observations do not.
    const sameObservation=!(Number.isFinite(rowAt)&&Number.isFinite(prevAt))||rowAt===prevAt;
    map.set(key,{...newer,held:prev.held||row.held,reportedActive:sameObservation?(active(prev)||active(row)):active(newer)});
  }
  return [...map.values()].sort((a,b)=>a.title.localeCompare(b.title));
}
export function readRegistry(c) {
  const record=readPrivate(nexusHome(c),'chats/catalog.json',{missing:{schema:'ghc.nexus.catalog.v1',entries:[]}});
  if(record.schema!=='ghc.nexus.catalog.v1'||!Array.isArray(record.entries)||record.entries.length>1000)throw new Error('Invalid chat catalogue');
  return record.entries.map(r=>normalizeEntry(r,r.source||'saved catalogue',r.observedAt||null));
}
export function saveRegistry(c,entries) {
  if(!Array.isArray(entries)||entries.length>1000)throw new Error('Invalid chat catalogue');
  const normalized=entries.map(r=>normalizeEntry(r,r.source||'explicit import',r.observedAt||null));
  return writePrivate(nexusHome(c),'chats/catalog.json',{schema:'ghc.nexus.catalog.v1',savedAt:new Date().toISOString(),entries:mergeEntries([normalized])},{replace:true});
}
export async function listChats(c,{refresh=false,limit=100,search='',read=appServerRead,run=bounded}={}) {
  if(!Number.isInteger(limit)||limit<1||limit>100)throw new Error('Chat limit must be 1 to 100');
  const saved=readRegistry(c),groups=[saved],observations=[];
  if(refresh){
    const at=new Date().toISOString();
    const local=await read(c,'thread/list',{limit:100,archived:false,sortKey:'updated_at',sourceKinds:['cli','vscode','appServer','exec','unknown'],useStateDbOnly:true});
    if(local.status==='ok'&&Array.isArray(local.data?.data)){
      const entries=[];for(const r of local.data.data){try{entries.push(normalizeEntry({...r,kind:'codex-local',hostId:c.hostId||'local'},'live local app-server',at));}catch{}}
      groups.push(entries);observations.push({provider:'local',status:'ok',count:entries.length,nextCursor:local.data.nextCursor??null,childCloseObserved:local.childCloseObserved});
    }else observations.push({provider:'local',status:'unavailable',reason:local.reason||'invalid_response'});
    if(c.codex){
      const cloud=await run(c.codex,['cloud','list','--json','--limit','20'],{cwd:c.cwd,timeoutMs:30000,maxBytes:262144});
      if(cloud.status==='ok')try{
        const data=JSON.parse(cloud.stdout);if(!Array.isArray(data.tasks))throw new Error();
        groups.push(data.tasks.slice(0,20).map(r=>normalizeEntry({...r,kind:'codex-cloud-task'},'live Codex Cloud CLI',at)));
        observations.push({provider:'cloud-tasks',status:'ok',count:Math.min(data.tasks.length,20),cursor:data.next_cursor??null});
      }catch{observations.push({provider:'cloud-tasks',status:'unavailable',reason:'invalid_response'});}
      else observations.push({provider:'cloud-tasks',status:'unavailable',reason:cloud.status});
    }
  }
  const merged=mergeEntries(groups);let cache={status:'unchanged'};
  if(refresh&&observations.some(o=>o.status==='ok')){
    try{saveRegistry(c,mergeEntries([readRegistry(c),merged]));cache={status:'saved'};}catch{cache={status:'unavailable',reason:'local_snapshot_not_saved'};}
  }
  const filtered=merged.filter(r=>r.title.toLowerCase().includes(String(search).toLowerCase())||r.id===search);
  return {schema:'ghc.nexus.chat-list.v1',entries:filtered.slice(0,limit),total:filtered.length,truncated:filtered.length>limit,observations,cache,savedSnapshot:cache.status!=='unavailable',automaticChatStarts:0};
}
export function resolveChat(entries,selector){
  const exact=entries.filter(r=>r.id===selector||r.title===selector);
  if(exact.length!==1)throw new Error(exact.length?'Ambiguous chat selection':'Chat not found');
  return exact[0];
}
export function recoveryCatalogue(c,selector){
  const saved=readRegistry(c),entries=selector?[resolveChat(saved,selector)]:saved;
  return {schema:'ghc.nexus.recovery-catalogue.v1',observedAt:new Date().toISOString(),providerQueried:false,startsPerformed:0,
    note:'These are preserved identifiers and route hints, not copied histories or evidence of current access. Managed cloud and ChatGPT chats keep their original provider.',
    entries:entries.map(r=>({id:r.id,title:r.title,kind:r.kind,hostId:r.hostId,held:r.held,
      lastObservationAt:r.observedAt,lastRecordedStatus:r.status,source:r.source,
      recovery:r.held?'preserve_hold':r.kind==='codex-local'?'verify_local_history_and_official_session_lock':r.kind==='chatgpt'?'open_original_chatgpt_conversation':'restore_original_provider_connection',
      cliCandidate:r.kind==='codex-local'&&!r.held&&c.codex?{command:c.codex,args:['--no-daemon','--no-alt-screen','resume',r.id],requiresCurrentProviderCheck:true,historyAvailability:'unverified',preservesSettings:true}:null,
      browserUrl:r.kind==='chatgpt'?'https://chatgpt.com/c/'+r.id:null}))};
}
export function localResumePickerPlan(c){
 if(!c.codex)return {status:'unavailable',reason:'codex_not_found'};
 return {status:'ready',action:'local-resume-picker',command:c.codex,args:['--no-daemon','--no-alt-screen','resume','--all'],cwd:c.cwd,interactive:true,shell:false,
   note:'Choose an existing local session in the official CLI. It controls the session lock and retains that session settings. This does not open managed cloud or ChatGPT histories.'};
}
export function chatPlan(entry,c,{override=false,now=Date.now()}={}) {
  const r=normalizeEntry(entry,entry.source,entry.observedAt);
  if(override)throw new Error('Existing chat settings must be inherited');
  if(r.held)return {status:'held',id:r.id,title:r.title,reason:'Preserved record; activation is on hold'};
  if(r.status==='active'||r.status==='running'||entry.reportedActive)return {status:'busy',id:r.id,title:r.title,reason:'A source reports active work; finish or pause the existing session first'};
  if(r.kind==='codex-local'){
    if(!c.codex)return {status:'unavailable',reason:'codex_not_found'};
    if(r.hostId!==(c.hostId||'local'))return {status:'unavailable',reason:'different_host',id:r.id,title:r.title};
    const age=now-Date.parse(r.observedAt);
    if(!['idle','notLoaded'].includes(r.status)||!Number.isFinite(age)||age<0||age>300000)return {status:'unverified',id:r.id,title:r.title,reason:'Current local availability is not established; refresh the supported provider or use the official local picker',providerStatus:r.status};
    const args=['--no-daemon','--no-alt-screen','resume',r.id];
    return {status:'ready',schema:'ghc.nexus.chat-plan.v1',action:'chat-resume',id:r.id,title:r.title,command:c.codex,args,cwd:c.cwd,interactive:true,shell:false,preservesModelAndSettings:true,providerStatus:r.status,executionGate:'official_cli_session_lock',note:'No model, reasoning, context or permission override is supplied. notLoaded means this observer has not loaded the session; it is not proof of inactivity elsewhere. The official CLI must acquire the session lock; the hub never removes locks.'};
  }
  if(r.kind==='chatgpt'){
    const url='https://chatgpt.com/c/'+r.id;
    if(c.platform==='win32'&&c.pwsh)return {status:'ready',action:'chat-browser',id:r.id,title:r.title,command:c.pwsh,args:['-NoProfile','-NonInteractive','-Command',`Start-Process -FilePath '${url}'`],cwd:c.cwd,interactive:false,shell:false,note:'Opens the original ChatGPT conversation. It is not converted into a Codex model session.'};
    const open=findExecutable('xdg-open');return open?{status:'ready',action:'chat-browser',command:open,args:[url],cwd:c.cwd,interactive:false,shell:false,id:r.id,title:r.title}:{status:'manual',url,id:r.id,title:r.title};
  }
  if(r.kind==='codex-cloud-task')return {status:'ready',action:'cloud',id:r.id,title:r.title,command:c.codex,args:['cloud'],cwd:c.cwd,interactive:true,shell:false,note:'Use the official cloud task picker to select this task. This legacy cloud route does not grant access to every managed App worker.'};
  return {status:'native-route',id:r.id,title:r.title,kind:r.kind,hostId:r.hostId,nativeAction:{tool:'mcp__codex_app__navigate_to_codex_page',arguments:{threadId:r.id}},note:'Open this existing chat in the App, or connect its own supported remote host. No local copy of its private history is fabricated.'};
}
export async function admitChat(c,entry,{read=appServerRead}={}){
 const key=r=>r.kind+':'+r.hostId+':'+r.id;
 const current=readRegistry(c).filter(r=>key(r)===key(entry));
 if(current.length!==1)return {status:'unverified',reason:'catalogue_binding_changed'};
 const selected=current[0];
 if(selected.held)return chatPlan(selected,c);
 if(selected.kind!=='codex-local')return chatPlan(selected,c);
 if(selected.hostId!==(c.hostId||'local'))return {status:'unavailable',reason:'different_host'};
 const observed=await read(c,'thread/read',{threadId:selected.id,includeTurns:false});
 if(observed.status!=='ok'||observed.data?.thread?.id!==selected.id)return {status:'unverified',reason:'live_activity_unavailable'};
 const after=readRegistry(c).filter(r=>key(r)===key(selected));
 if(after.length!==1||after[0].held||after[0].title!==selected.title)return {status:'held',reason:'catalogue_changed_during_admission'};
  if(after[0].status==='active'||after[0].status==='running'||after[0].reportedActive)return {status:'busy',reason:'newer_catalogue_activity_blocks_admission'};
  if(JSON.stringify(after[0])!==JSON.stringify(selected))return {status:'unverified',reason:'catalogue_revision_changed_during_admission'};
 const live=normalizeEntry({...selected,status:observed.data.thread.status,reportedActive:false},'effect-time provider observation',new Date().toISOString());
 return chatPlan(live,c);
}
