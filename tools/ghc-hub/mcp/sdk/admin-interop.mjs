import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {createReadStream} from 'node:fs';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
import {createAdminCommander,loadAdminPolicy} from '../../admin-commander.mjs';

const base=process.argv[2];
if(!base||!path.isAbsolute(base))throw new Error('Existing absolute evidence directory required');
const root=path.dirname(fileURLToPath(import.meta.url));
const run=await fs.mkdtemp(path.join(base,'admin-interop-'));
const work=path.join(run,'work'),state=path.join(run,'state');
await fs.mkdir(work);await fs.mkdir(state);
const h=crypto.createHash('sha256');for await(const b of createReadStream(process.execPath,{highWaterMark:1048576}))h.update(b);
const policyFile=path.join(run,'policy.json');
await fs.writeFile(policyFile,JSON.stringify({schema:'ghc.admin.policy.v1',enabled:true,roots:[{alias:'work',path:work,write:true}],stateDirectory:state,shells:{node:{path:process.execPath,sha256:h.digest('hex')}}}));
const local=createAdminCommander(await loadAdminPolicy(policyFile));
const checks=[];
const expect=(name,fn)=>fn().then(()=>checks.push({name,passed:true})).catch(e=>{checks.push({name,passed:false,message:String(e.message).slice(0,300)});throw e;});
for(const mode of ['legacy','modern']){
 const client=new Client({name:'ghc-admin-interop',version:'2.7.0'},{versionNegotiation:{mode:mode==='modern'?{pin:'2026-07-28'}:'legacy'}});
 const transport=new StdioClientTransport({command:process.execPath,args:['--max-old-space-size=96',path.resolve(root,'../../mcp-admin-server.mjs'),policyFile],cwd:run,stderr:'pipe',maxBufferSize:32768,env:{SystemRoot:process.env.SystemRoot||'C:/Windows',PATH:path.dirname(process.execPath),GHC_HUB_WORKSPACE:run,GHC_HUB_HOME:path.join(run,'hub'),GHC_NEXUS_HOME:path.join(run,'nexus')}});
 let stderrBytes=0;transport.stderr.on('data',b=>{stderrBytes+=b.length;});
 const call=async(name,args={})=>{const r=await client.callTool({name,arguments:args},{timeout:60000});assert.equal(r.isError,false,JSON.stringify(r));assert.deepEqual(JSON.parse(r.content[0].text),r.structuredContent);return r.structuredContent;};
 try{
  await client.connect(transport,{timeout:60000});
  await expect(mode+' sixteen bounded tool declarations',async()=>{const r=await client.listTools({}, {timeout:15000});assert.equal(r.tools.length,16);assert.equal(new Set(r.tools.map(t=>t.name)).size,16);assert.ok(Buffer.byteLength(JSON.stringify(r))<32768);});
  await expect(mode+' original identity and admin status',async()=>{assert.equal((await call('nexus.identity.summary')).component,'nexus-hub');assert.equal((await call('nexus.admin.status')).version,'2.7.0');});
  await expect(mode+' text write read and backup',async()=>{const p=mode+'.md';const a=await call('nexus.files.write',{root:'work',path:p,text:'first',expectedSha256:null});assert.equal((await call('nexus.files.read',{root:'work',path:p})).text,'first');const b=await call('nexus.files.write',{root:'work',path:p,text:'second',expectedSha256:a.sha256});assert.ok(b.backupId);assert.equal(await fs.readFile(path.join(state,'file-backups',b.backupId+'.bin'),'utf8'),'first');});
  await expect(mode+' approval required and one execution',async()=>{const p=await call('nexus.exec.prepare',{shell:'node',root:'work',command:'console.log("sdk-smoke")'});const before=await client.callTool({name:'nexus.exec.execute',arguments:{id:p.id,sha256:p.sha256}},{timeout:60000});assert.equal(before.isError,true);await local.approve(p.id,p.sha256);const result=await call('nexus.exec.execute',{id:p.id,sha256:p.sha256});assert.equal(result.stdout.trim(),'sdk-smoke');assert.equal(result.exitCode,0);assert.equal(result.childClosed,true);const after=await client.callTool({name:'nexus.exec.execute',arguments:{id:p.id,sha256:p.sha256}},{timeout:60000});assert.equal(after.isError,true);assert.equal(Object.hasOwn(await call('nexus.exec.receipt',{id:p.id}),'stdout'),false);});
  await expect(mode+' rejects path escape',async()=>{const r=await client.callTool({name:'nexus.files.read',arguments:{root:'work',path:'../policy.json'}},{timeout:10000});assert.equal(r.isError,true);});
  await expect(mode+' excessive escaped result fails without closing connection',async()=>{await fs.writeFile(path.join(work,'escape.txt'),'\\'.repeat(8192));const r=await client.callTool({name:'nexus.files.read',arguments:{root:'work',path:'escape.txt'}},{timeout:10000});assert.equal(r.isError,true);assert.match(r.content[0].text,/output_too_large/);assert.equal((await call('nexus.admin.status')).held,false);});
 }catch{ /* retain the first failure and close this transport */ }
 finally{await client.close();}
 checks.push({name:mode+' no stderr',passed:stderrBytes===0,bytes:stderrBytes});
}
const receipt={schema:'ghc.admin.interop.v1',at:new Date().toISOString(),run,checks,passed:checks.filter(c=>c.passed).length,failed:checks.filter(c=>!c.passed).length,realPrivateStateRead:false,modelTurns:0};
await fs.writeFile(path.join(run,'receipt.json'),JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt));process.exitCode=receipt.failed?1:0;
