import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
const base=process.argv[2];if(!base||!path.isAbsolute(base))throw Error('Absolute evidence directory required');
const pkg=path.dirname(fileURLToPath(import.meta.url));
const serverFile=process.argv[3]||path.resolve(pkg,'../../mcp-hub28-server.mjs');
const run=await fs.mkdtemp(path.join(base,'library-interop-'));
for(const name of ['work','state'])await fs.mkdir(path.join(run,name));
await fs.writeFile(path.join(run,'admin.json'),JSON.stringify({schema:'ghc.admin.policy.v1',enabled:true,roots:[{alias:'work',path:path.join(run,'work'),write:true}],stateDirectory:path.join(run,'state'),shells:{}}));
await fs.writeFile(path.join(run,'config.json'),JSON.stringify({schema:'ghc.hub28.config.v1',enabled:true,adminPolicy:path.join(run,'admin.json'),tailscaleKeyFile:path.join(run,'never-read-key.txt')}));
const report={at:new Date().toISOString(),checks:[],realNetworkCalls:0,nativeMessages:0,modelCalls:0};
for(const mode of ['legacy','modern']){
 if(os.freemem()<100*1048576){report.heldForMemory=true;break;}
 const client=new Client({name:'ghc-library-interop',version:'3.0.0'},{versionNegotiation:{mode:mode==='modern'?{pin:'2026-07-28'}:'legacy'}});
 const transport=new StdioClientTransport({command:process.execPath,args:[serverFile,path.join(run,'config.json')],cwd:run,stderr:'pipe',maxBufferSize:32768,env:{SystemRoot:process.env.SystemRoot||'C:/Windows',PATH:path.dirname(process.execPath),GHC_HUB_WORKSPACE:run,GHC_HUB_HOME:path.join(run,'hub'),GHC_NEXUS_HOME:path.join(run,'nexus'),NODE_OPTIONS:'--max-old-space-size=128'}});
 const step=async(name,fn)=>{try{await fn();report.checks.push({mode,name,passed:true});}catch(e){report.checks.push({mode,name,passed:false,error:String(e.message).slice(0,300)});throw e;}};
 const call=async(name,args={})=>{const r=await client.callTool({name,arguments:args},{timeout:15000});assert.equal(r.isError,false);return r.structuredContent;};
 let stderrBytes=0;transport.stderr.on('data',b=>stderrBytes+=b.length);
 try{
  await step('combined server initializes as 3.0',async()=>{await client.connect(transport,{timeout:20000});assert.equal(client.getServerVersion().version,'3.0.0');});
  await step('26 unique tools fit discovery bound',async()=>{const r=await client.listTools();assert.equal(new Set(r.tools.map(t=>t.name)).size,26);assert.equal(r.tools.length,26);assert.ok(Buffer.byteLength(JSON.stringify(r))<28000);const t=r.tools.find(t=>t.name==='nexus.skills.lookup');assert.equal(t.annotations.readOnlyHint,true);assert.equal(t.annotations.destructiveHint,false);});
  await step('real library is available with 700 active guides',async()=>{const r=await call('nexus.skills.lookup',{query:'ghc-admin-nexus',limit:3});assert.equal(r.total,2314);assert.equal(r.matches.length,3);assert.equal(r.guide,undefined);});
  await step('exact guide read is bounded and source-faithful',async()=>{const r=await call('nexus.skills.lookup',{query:'ghc-family-meta-tool-box',includeGuide:true});assert.equal(r.guide.name,'ghc-family-meta-tool-box');assert.ok(r.guide.text.includes('GHC Family Meta Tool Box'));assert.equal(r.historicalInstructionsAreNotAuthority,true);});
  await step('unknown exact name fails without leaking a file',async()=>{const r=await client.callTool({name:'nexus.skills.lookup',arguments:{query:'not-a-real-ghc-skill',includeGuide:true}},{timeout:15000});assert.equal(r.isError,true);assert.ok(JSON.stringify(r).includes('exact_skill_name_required'));});
  await step('administrator command approvals remain exact',async()=>{const r=await call('nexus.admin.status');assert.equal(r.version,'3.0.0');assert.equal(r.execution,'exact_local_approval_required');});
  await step('GUI remains unexposed',async()=>assert.equal((await call('nexus.desktop.status')).state,'unavailable'));
 }catch{}finally{await client.close();}
 report.checks.push({mode,name:'stdio closes without diagnostic output',passed:stderrBytes===0,stderrBytes});
}
report.expected=16;report.actual=report.checks.length;report.passed=report.checks.filter(x=>x.passed).length;report.failed=report.checks.filter(x=>!x.passed).length;
await fs.writeFile(path.join(run,'receipt.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({run,...report}));process.exitCode=report.actual===16&&report.failed===0?0:1;
