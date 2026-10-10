import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
const output=process.argv[2];if(!output||!path.isAbsolute(output))throw Error('Absolute evidence file required');
const client=new Client({name:'ghc-installed28-check',version:'2.8.0'},{versionNegotiation:{mode:'legacy'}});
const transport=new StdioClientTransport({command:process.execPath,args:['D:/GHC-Archives/global-tools/ghc-nexus-hub/mcp-hub28-server.mjs','D:/GHC-Archives/private/ghc-nexus/admin/hub28.json'],stderr:'pipe',maxBufferSize:32768});
const r={at:new Date().toISOString(),mutations:0,nativeSends:0,networkInventoryCalls:0,checks:[],closed:false};let stderrBytes=0;
transport.stderr.on('data',b=>stderrBytes+=b.length);
const step=async(name,fn)=>{await fn();r.checks.push({name,passed:true});};
const call=async(name,args={})=>{const x=await client.callTool({name,arguments:args},{timeout:30000});assert.equal(x.isError,false,JSON.stringify(x));return x.structuredContent;};
try{
 await step('installed entrypoint initializes',()=>client.connect(transport,{timeout:30000}));
 await step('25 unique tools within transport bounds',async()=>{const x=await client.listTools();r.toolNames=x.tools.map(t=>t.name);assert.equal(new Set(r.toolNames).size,25);assert.ok(Buffer.byteLength(JSON.stringify(x))<28000);});
 await step('live admin status is version 2.8.0',async()=>{r.admin=await call('nexus.admin.status');assert.equal(r.admin.version,'2.8.0');assert.equal(r.admin.execution,'exact_local_approval_required');});
 await step('ChatGPT route is manual',async()=>{r.chatPlan=await call('nexus.chats.plan',{alias:'teren-serein-7df93e'});assert.equal(r.chatPlan.route,'manual');assert.equal(r.chatPlan.executed,false);});
 await step('existing real delivery receipt survives promotion',async()=>{r.message=await call('nexus.messages.receipt',{requestId:'5343be13-0bed-4b05-801b-77d162fafa27'});assert.equal(r.message.deliveryState,'accepted');assert.equal(r.message.recipientCompletion,'not_observed');});
 await step('resource observation comes from the installed host',async()=>{r.resources=await call('nexus.host.resources');assert.equal(r.resources.platform,process.platform);assert.ok(r.resources.totalMemoryMiB>0);});
 await step('unverified GUI remains unavailable',async()=>{r.gui=await call('nexus.desktop.status');assert.equal(r.gui.state,'unavailable');});
}catch(e){r.error=String(e.message).slice(0,500);}finally{try{await client.close();r.closed=true;}catch{r.closed=false;}r.stderrBytes=stderrBytes;}
r.passed=r.checks.length===7&&r.closed&&stderrBytes===0&&!r.error;
await fs.writeFile(output,JSON.stringify(r,null,2)+'\n');console.log(JSON.stringify(r));process.exitCode=r.passed?0:1;
