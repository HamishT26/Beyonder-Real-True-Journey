import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';

const base=process.argv[2];if(!base||!path.isAbsolute(base))throw Error('Evidence directory required');
const pkg=path.dirname(fileURLToPath(import.meta.url));
const run=await fs.mkdtemp(path.join(base,'fabric-interop-'));
await fs.mkdir(path.join(run,'work'));await fs.mkdir(path.join(run,'state'));
await fs.writeFile(path.join(run,'admin.json'),JSON.stringify({schema:'ghc.admin.policy.v1',enabled:true,roots:[{alias:'work',path:path.join(run,'work'),write:true}],stateDirectory:path.join(run,'state'),shells:{}}));
await fs.writeFile(path.join(run,'key.txt'),'tskey-api-SYNTHETIC_NOT_SENT');
await fs.writeFile(path.join(run,'config.json'),JSON.stringify({schema:'ghc.hub28.config.v1',enabled:true,adminPolicy:path.join(run,'admin.json'),tailscaleKeyFile:path.join(run,'key.txt')}));
await fs.mkdir(path.join(run,'nexus','chats'),{recursive:true});await fs.mkdir(path.join(run,'nexus','mcp'),{recursive:true});
const targetId='11111111-2222-4333-8444-555555555555';
await fs.writeFile(path.join(run,'nexus','chats','catalog.json'),JSON.stringify({schema:'ghc.nexus.catalog.v1',entries:[{id:targetId,title:'Synthetic relay target',kind:'chatgpt',hostId:null,status:'idle',observedAt:new Date().toISOString()}]}));
await fs.writeFile(path.join(run,'nexus','mcp','selectors.json'),JSON.stringify({schema:'ghc.nexus.mcp-selectors.v1',chats:[{id:targetId,kind:'chatgpt',alias:'synthetic-chat'}]}));
const checks=[];const timings=[];
for(const mode of ['legacy','modern']){
 const client=new Client({name:'ghc-fabric-interop',version:'2.8.0-candidate'},{versionNegotiation:{mode:mode==='modern'?{pin:'2026-07-28'}:'legacy'}});
 const transport=new StdioClientTransport({command:process.execPath,args:[path.resolve(pkg,'../../mcp-hub28-server.mjs'),path.join(run,'config.json')],cwd:run,stderr:'pipe',maxBufferSize:32768,env:{SystemRoot:process.env.SystemRoot||'C:/Windows',PATH:path.dirname(process.execPath),GHC_HUB_WORKSPACE:run,GHC_HUB_HOME:path.join(run,'hub'),GHC_NEXUS_HOME:path.join(run,'nexus')}});
 const step=async(name,fn)=>{try{await fn();checks.push({name:mode+' '+name,passed:true});}catch(e){checks.push({name:mode+' '+name,passed:false,error:String(e.message).slice(0,300)});throw e;}};
 const call=async(name,args={})=>{const r=await client.callTool({name,arguments:args},{timeout:30000});assert.equal(r.isError,false,JSON.stringify(r));return r.structuredContent;};
 let stderrBytes=0;transport.stderr.on('data',b=>stderrBytes+=b.length);
 try{
  await step('connect',async()=>{const start=performance.now();await client.connect(transport,{timeout:30000});timings.push({mode,discoveryMs:Math.round(performance.now()-start)});});
  await step('twenty-five tools within the existing transport bound',async()=>{const r=await client.listTools({}, {timeout:10000});assert.equal(r.tools.length,25);assert.equal(new Set(r.tools.map(x=>x.name)).size,25);assert.ok(Buffer.byteLength(JSON.stringify(r))<28000);});
  await step('measured local resources',async()=>{const r=await call('nexus.host.resources');assert.equal(r.platform,process.platform);assert.ok(r.totalMemoryMiB>0);assert.equal(r.administrator,'not_measured_by_this_operation');});
  await step('GUI readiness not invented',async()=>{assert.equal((await call('nexus.desktop.status')).state,'unavailable');});
  await step('unverified Linux execution remains held on Windows',async()=>{const r=await call('nexus.workload.plan',{kind:process.platform==='win32'?'linux-cli':'windows-cli'});assert.equal(r.state,'held');assert.equal(r.executes,false);});
  await step('credential path cannot be supplied by caller',async()=>{let refused=false;try{const r=await client.callTool({name:'nexus.network.devices',arguments:{keyFile:'another'}},{timeout:10000});refused=r.isError===true;}catch{refused=true;}assert.equal(refused,true);assert.ok((await call('nexus.host.resources')).totalMemoryMiB>0);});
  let message;const requestId=mode==='legacy'?'11111111-2222-4333-8444-555555555551':'11111111-2222-4333-8444-555555555552';
  await step('agent relay route without server sender',async()=>{const r=await call('nexus.messages.routes');assert.equal(r.serverSenderAvailable,false);assert.equal(r.items[0].alias,'synthetic-chat');});
  await step('bounded remote draft and correct mutating annotation',async()=>{message=await call('nexus.messages.prepare',{requestId,alias:'synthetic-chat',body:'Synthetic fixture only; no native send is invoked.'});assert.equal(message.deliveryState,'queued');const listed=await client.listTools();assert.equal(listed.tools.find(t=>t.name==='nexus.messages.prepare').annotations.readOnlyHint,false);});
  await step('single claim returns exact provider action',async()=>{const r=await call('nexus.messages.claim',{requestId,messageSha256:message.messageSha256});assert.equal(r.nativeAction.arguments.threadId,targetId);assert.equal(r.nativeAction.arguments.hostId,undefined);assert.equal(r.automaticDelivery,false);});
  await step('unknown native result retained without automatic retry',async()=>{const r=await call('nexus.messages.record',{requestId,messageSha256:message.messageSha256,outcome:'unknown',deliveryReference:'synthetic-timeout'});assert.equal(r.deliveryState,'unknown');assert.equal((await call('nexus.messages.claim',{requestId,messageSha256:message.messageSha256})).status,'held');});
  await step('receipt keeps completion and sender evidence separate',async()=>{const r=await call('nexus.messages.receipt',{requestId});assert.equal(r.recipientCompletion,'not_observed');assert.equal(r.receipt.evidenceType,'caller-reported-native-tool-result');assert.ok(!JSON.stringify(r).includes(targetId));});
  await step('original admin status preserved',async()=>{assert.equal((await call('nexus.admin.status')).version,'2.8.0');});
 }catch{}finally{await client.close();}
 checks.push({name:mode+' no stderr',passed:stderrBytes===0,bytes:stderrBytes});
}
const report={at:new Date().toISOString(),run,expected:26,actual:checks.length,passed:checks.filter(x=>x.passed).length,failed:checks.filter(x=>!x.passed).length,checks,timings,realNetworkCalls:0,modelCalls:0};
await fs.writeFile(path.join(run,'receipt.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));process.exitCode=report.failed||report.actual!==report.expected?1:0;
