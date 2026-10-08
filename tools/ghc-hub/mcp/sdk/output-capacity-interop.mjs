import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {saveRegistry} from '../../chats.mjs';
import {writePrivate} from '../../private-store.mjs';
import {saveSentinel,sentinelTemplate} from '../../sentinel.mjs';
const {Client}=await import('@modelcontextprotocol/client');
const {StdioClientTransport}=await import('@modelcontextprotocol/client/stdio');
const root=path.dirname(fileURLToPath(import.meta.url));
const bank=process.argv[2];
if(!bank||!path.isAbsolute(bank)||!fs.statSync(bank).isDirectory())throw new Error('An existing absolute evidence directory is required');
const run=fs.mkdtempSync(path.join(bank,'mcp-capacity-interop-'));
const c={platform:process.platform,cwd:run,state:path.join(run,'state'),nexusHome:path.join(run,'private'),hostId:'local'};
fs.mkdirSync(c.nexusHome,{mode:0o700});
const entries=Array.from({length:128},(_,i)=>({id:'00000000-0000-4000-8000-'+String(i).padStart(12,'0'),kind:'codex-local',hostId:'local',title:'SYNTHETIC_PRIVATE_TITLE_'+i,status:'idle',source:'isolated interop fixture',observedAt:new Date().toISOString()}));
saveRegistry(c,entries);
writePrivate(c.nexusHome,'mcp/selectors.json',{schema:'ghc.nexus.mcp-selectors.v1',chats:entries.map((r,i)=>({alias:'chat-'+String(i).padStart(3,'0')+'x'.repeat(56),id:r.id,kind:r.kind}))});
writePrivate(c.nexusHome,'personal/contact.json',{canary:'SYNTHETIC_PRIVATE_CONTACT'});
saveSentinel(c,sentinelTemplate('sentinel-1'));
const calls=[['nexus.chats.list',{}],['nexus.chats.resolve',{alias:'chat-000'+'x'.repeat(56)}],['nexus.chats.plan',{alias:'chat-000'+'x'.repeat(56)}],['nexus.lab.catalogue',{}],['nexus.lab.plan',{alias:'queue'}],['nexus.identity.summary',{}],['nexus.remote.plan',{alias:'primary'}],['nexus.sentinel.validate',{alias:'sentinel-1'}],['nexus.sentinel.plan',{alias:'sentinel-1'}]];
const checks=[],connections=[];
const alive=pid=>{try{process.kill(pid,0);return true;}catch(e){if(e.code==='ESRCH')return false;throw e;}};
for(const mode of ['legacy','modern']){
 const pidFile=path.join(run,mode+'-pids.jsonl');
 const client=new Client({name:'ghc-root-integration',version:'2.0.0'},{versionNegotiation:{mode:mode==='modern'?{pin:'2026-07-28'}:'legacy'}});
 const transport=new StdioClientTransport({command:process.execPath,args:['--max-old-space-size=96',path.join(root,'root-interop-fixture.mjs')],cwd:run,stderr:'pipe',maxBufferSize:32768,env:{SystemRoot:process.env.SystemRoot||'C:\\Windows',PATH:path.dirname(process.execPath),GHC_HUB_WORKSPACE:run,GHC_HUB_HOME:c.state,GHC_NEXUS_HOME:c.nexusHome,GHC_NEXUS_TEST_PID_FILE:pidFile}});
 let stderrBytes=0;
 transport.stderr.on('data',b=>{stderrBytes+=b.length;});
 try{
  await client.connect(transport,{timeout:60000});
  const tools=await client.listTools({}, {timeout:10000});
  assert.equal(tools.tools.length,9);checks.push({name:mode+' exact nine tools',passed:true});
  for(const [name,args] of calls){
   const result=await client.callTool({name,arguments:args},{timeout:10000});
   assert.equal(result.isError,false);assert.ok(result.structuredContent);
   assert.doesNotMatch(JSON.stringify(result),/SYNTHETIC_PRIVATE|00000000-0000-4000-8000/);
   if(name==='nexus.chats.list')assert.equal(result.structuredContent.items.length,128);
   checks.push({name:mode+' '+name,passed:true});
  }
  let rejected=false;try{const result=await client.callTool({name:'nexus.chats.plan',arguments:{alias:'chat-000'+'x'.repeat(56),command:'invalid'}},{timeout:10000});rejected=result.isError===true;}catch{rejected=true;}
  assert.equal(rejected,true);checks.push({name:mode+' rejects extra command input',passed:true});
 }catch(e){checks.push({name:mode+' integration',passed:false,errorType:e.name,message:String(e.message).slice(0,250)});}
 finally{try{await client.close();}catch{checks.push({name:mode+' close',passed:false});}}
 const pids=fs.existsSync(pidFile)?fs.readFileSync(pidFile,'utf8').trim().split('\n').filter(Boolean).map(l=>JSON.parse(l).pid):[];
 const deadline=performance.now()+7000;
 while(pids.some(alive)&&performance.now()<deadline)await new Promise(r=>setTimeout(r,30));
 const remaining=pids.filter(alive);
 checks.push({name:mode+' all observed fixture children closed',passed:pids.length>0&&remaining.length===0});
 for(const pid of remaining){try{process.kill(pid,'SIGKILL');}catch{}}
 connections.push({mode,pids,childrenClosed:remaining.length===0,stderrBytes});
}
const receipt={schema:'ghc.root-sdk-interop.v1',at:new Date().toISOString(),sdkVersion:'2.3.1',run,checks,connections,passed:checks.filter(r=>r.passed).length,failed:checks.filter(r=>!r.passed).length,realPrivateStateRead:false,modelTurns:0,credentialReads:0,networkListeners:0};
fs.writeFileSync(path.join(run,'receipt.json'),JSON.stringify(receipt,null,2));
console.log(JSON.stringify({receipt:path.join(run,'receipt.json'),passed:receipt.passed,failed:receipt.failed,connections}));
process.exitCode=receipt.failed?1:0;
