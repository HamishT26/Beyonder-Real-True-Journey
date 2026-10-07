import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {randomUUID} from 'node:crypto';

export function reviewCases(subject,{saveRegistry,nexusCommand,NEXUS_HELP},label){
 const root=process.env.GHC_NEXUS_TEST_ARTIFACTS || (process.platform==='win32'?'D:/GHC-Archives/phase-banks/saelin-cmd-remaster-20261007/review-cases':path.resolve(import.meta.dirname,'../fixtures',label));fs.mkdirSync(root,{recursive:true});
 function fixture({upper=false}={}){
  const home=fs.mkdtempSync(path.join(root,'case-'));
  const c={platform:process.platform,nexusHome:home,hostId:'local'};
  const id=upper?randomUUID().toUpperCase():randomUUID();
  const entry={id,kind:'codex-local',hostId:'local',title:'Synthetic fixture only',status:'idle',observedAt:new Date().toISOString(),source:'synthetic metadata'};
  saveRegistry(c,[entry]);return {c,entry,raw:{requestId:randomUUID(),toId:id.toLowerCase(),body:'Private synthetic message fixture. No sender is invoked.'}};
 }
 function makeClaim(f){subject.queueMessage(f.c,f.raw);subject.claimMessage(f.c,f.raw.requestId);return subject.messageStatus(f.c,f.raw.requestId)}
 function receipt(f,outcome='unknown'){const status=subject.messageStatus(f.c,f.raw.requestId);return {requestId:f.raw.requestId,messageSha256:status.messageSha256,threadId:status.target.threadId,hostId:status.target.hostId,outcome,tool:'mcp__codex_app__send_message_to_thread',deliveryReference:'synthetic-result'}}
 test('UUID request never resolves another chat through its title',()=>{
  const f=fixture(),missing=randomUUID();saveRegistry(f.c,[{...f.entry,title:missing}]);
  assert.throws(()=>subject.messagePlan(f.c,{...f.raw,toId:missing}));
  assert.throws(()=>subject.queueMessage(f.c,{...f.raw,toId:missing}));
  assert.equal(subject.listMessages(f.c).messages.length,0);
 });
 test('valid uppercase catalogue UUID is bound canonically to the requested target',()=>{
  const f=fixture({upper:true});const p=subject.messagePlan(f.c,f.raw);
  assert.equal(p.status,'ready');assert.equal(p.nativeAction.arguments.threadId,f.raw.toId);
  subject.queueMessage(f.c,f.raw);assert.equal(subject.claimMessage(f.c,f.raw.requestId).status,'saved');
 });
 test('idempotent queue preserves a known unknown outcome after catalogue expiry',()=>{
  const f=fixture();makeClaim(f);subject.recordMessageReceipt(f.c,receipt(f));
  saveRegistry(f.c,[{...f.entry,observedAt:new Date(Date.now()-600000).toISOString()}]);
  const r=subject.queueMessage(f.c,f.raw);assert.equal(r.deliveryState,'unknown');assert.equal(r.alreadyQueued,true);
  assert.equal(subject.listMessages(f.c).messages.length,1);
  assert.equal(subject.claimMessage(f.c,f.raw.requestId).status,'held');
 });
 test('persisted receipt cannot invent queued state after a claim',()=>{
  const f=fixture();makeClaim(f);subject.recordMessageReceipt(f.c,receipt(f));
  const p=path.join(f.c.nexusHome,'messages','receipts',f.raw.requestId+'.json');
  const r=JSON.parse(fs.readFileSync(p));r.outcome='queued';fs.writeFileSync(p,JSON.stringify(r));
  assert.throws(()=>subject.messageStatus(f.c,f.raw.requestId));
 });
 test('malformed claim metadata cannot expose a body through the default list',()=>{
  const f=fixture();makeClaim(f);
  const p=path.join(f.c.nexusHome,'messages','claims',f.raw.requestId+'.json');
  const r=JSON.parse(fs.readFileSync(p));r.privateBody=f.raw.body;fs.writeFileSync(p,JSON.stringify(r));
  assert.throws(()=>subject.listMessages(f.c));
 });
 test('message help exposes the manual relay boundary and claim command',()=>{
  assert.match(NEXUS_HELP,/messages claim --id UUID --execute/);
  assert.match(NEXUS_HELP,/no automatic sender/i);
 });
 test('actual message command rejects queue without execute before reading a file',async()=>{
  const f=fixture();await assert.rejects(()=>nexusCommand('messages','queue',{},f.c),/--execute/);
  assert.equal(subject.listMessages(f.c).messages.length,0);
 });
}
