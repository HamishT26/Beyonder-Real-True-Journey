import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {deviceProjection,planWorkload,readTailscaleDevices,createFabricDispatcher} from './host-fabric.mjs';

const now=Date.parse('2026-10-11T00:00:00Z');
const local={platform:'win32',observedAt:new Date(now).toISOString(),freeMemoryMiB:460,reserveMemoryMiB:256};
test('small local Node work fits reserved memory while large work is held',()=>{assert.equal(planWorkload({kind:'node',memoryMiB:128},local,[],{},now).state,'local-candidate');assert.equal(planWorkload({kind:'node',memoryMiB:256},local,[],{},now).state,'held');});
test('online or administrator-labelled cloud device cannot stand in for an executor',()=>{assert.equal(planWorkload({kind:'linux-cli'},local,[{host:'cloud',online:true,administrator:true,availableMemoryMiB:16000}],{},now).state,'held');});
test('stale cloud execution evidence cannot admit a workload',()=>{const r={host:'cloud',executionVerified:true,evidenceSha256:'a'.repeat(64),observedAt:new Date(now-900001).toISOString(),kinds:['linux-cli'],availableMemoryMiB:1024};assert.equal(planWorkload({kind:'linux-cli'},local,[r],{},now).state,'held');});
test('fresh compatible cloud evidence produces a plan without execution',()=>{const r={host:'cloud',executionVerified:true,evidenceSha256:'b'.repeat(64),observedAt:new Date(now-1000).toISOString(),kinds:['linux-cli'],availableMemoryMiB:1024};const p=planWorkload({kind:'linux-cli'},local,[r],{},now);assert.equal(p.state,'remote-candidate');assert.equal(p.executes,false);assert.equal(p.provisions,false);});
test('staged GUI is held even if there is sufficient local memory',()=>{assert.equal(planWorkload({kind:'desktop-gui'},{...local,freeMemoryMiB:1024},[],{state:'staged'},now).state,'held');});
test('stale or future local snapshots fail closed',()=>{for(const delta of [-60001,1])assert.throws(()=>planWorkload({kind:'node'},{...local,observedAt:new Date(now+delta).toISOString()},[],{},now),/stale_resource/);});
test('arbitrary hosts and executable parameters are not accepted',()=>assert.throws(()=>planWorkload({kind:'node',command:'something'},local,[],{},now),/invalid_arguments/));
test('network projection excludes addresses, keys and full device identifiers',()=>{const p=deviceProjection({devices:[{hostname:'cloud',os:'linux',authorized:true,addresses:['private-address'],nodeKey:'secret',id:'private-id'}]},now);const s=JSON.stringify(p);assert.ok(!s.includes('private-address')&&!s.includes('secret')&&!s.includes('private-id'));assert.equal(p.devices[0].ephemeral,null);});
test('network projection bounds large tailnets',()=>{const p=deviceProjection({devices:Array.from({length:130},()=>({hostname:'node'}))},now);assert.equal(p.devices.length,128);assert.equal(p.truncated,true);});
test('credential is sent only to fixed official API with redirects disabled',async()=>{
 const dir=await fs.mkdtemp(path.join(os.tmpdir(),'ghc-ts-fixture-'));const file=path.join(dir,'key.txt');await fs.writeFile(file,'tskey-api-SYNTHETIC_FIXTURE');
 try{let seen;const p=await readTailscaleDevices(file,{now:()=>now,fetchImpl:async(url,init)=>{seen={url,init};return new Response(JSON.stringify({devices:[]}),{status:200});}});assert.equal(seen.url,'https://api.tailscale.com/api/v2/tailnet/-/devices');assert.equal(seen.init.redirect,'error');assert.equal(seen.init.method,'GET');assert.ok(!JSON.stringify(p).includes('SYNTHETIC'));}finally{await fs.unlink(file);await fs.rmdir(dir);}
});
test('API errors cannot echo a credential through exception messages',async()=>{
 const dir=await fs.mkdtemp(path.join(os.tmpdir(),'ghc-ts-fixture-'));const file=path.join(dir,'key.txt');await fs.writeFile(file,'tskey-api-SYNTHETIC_FIXTURE');
 try{await assert.rejects(readTailscaleDevices(file,{fetchImpl:async()=>{throw Error('tskey-api-SYNTHETIC_FIXTURE');}}),e=>e.code==='network_unavailable'&&!e.message.includes('SYNTHETIC'));}finally{await fs.unlink(file);await fs.rmdir(dir);}
});
test('MCP caller cannot select an arbitrary credential file',async()=>{const dispatch=createFabricDispatcher({tailscaleKeyFile:'fixed'});await assert.rejects(dispatch('nexus.network.devices',{keyFile:'other'}),/invalid_arguments/);});
