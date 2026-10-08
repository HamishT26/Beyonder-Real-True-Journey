import test from 'node:test';
import assert from 'node:assert/strict';
import { renderDeliveryPanel } from './delivery-state-panel.mjs';

const opts={columns:80,tty:true,ascii:true,env:{NO_COLOR:''}};
const id='00000000-0000-4000-8000-000000000901';
const target='00000000-0000-4000-8000-000000000504';
function fixture(outcome='accepted') {
  const binding={requestId:id,messageSha256:'a'.repeat(64),threadId:target,hostId:'synthetic-fixture-host'};
  return {schema:'ghc.nexus.message-status.v1',requestId:id,messageSha256:binding.messageSha256,
    target:{threadId:target,hostId:binding.hostId},deliveryState:outcome,recipientCompletion:'not_observed',
    claim:{schema:'ghc.nexus.message-claim.v1',...binding},
    receipt:{schema:'ghc.nexus.message-receipt.v1',...binding,outcome,
      evidenceType:'caller-reported-native-tool-result',tool:'mcp__codex_app__send_message_to_thread',
      recipientCompletion:'not_observed'}};
}
const render=(message,options=opts)=>renderDeliveryPanel({messages:[message]},options);
const compact=output=>output.replace(/[|+\-\s]/g,'');
function unknown(message) { const out=render(message); assert.match(out,/UNKNOWN/); assert.doesNotMatch(out,/ACKNOWLEDGED/); }

test('accepted binding names caller report and does not imply completion',()=>{
  const out=render(fixture()); assert.match(out,/ACKNOWLEDGED \(caller-reported\)/);
  assert.match(out,/NOT OBSERVED/); assert.match(out,/not provider attestations/);
});
test('a mismatched target host cannot acknowledge',()=>{const m=fixture();m.receipt.hostId='different';unknown(m);});
test('a mismatched message digest cannot acknowledge',()=>{const m=fixture();m.receipt.messageSha256='b'.repeat(64);unknown(m);});
test('accepted state without receipt remains unknown',()=>{const m=fixture();m.receipt=null;unknown(m);});
test('accepted receipt without bound claim remains unknown',()=>{const m=fixture();m.claim=null;unknown(m);});
test('a different evidence type cannot acknowledge',()=>{const m=fixture();m.receipt.evidenceType='signed-provider-result';unknown(m);});
test('claimed recipient completion is not promoted',()=>{const m=fixture();m.recipientCompletion='completed';unknown(m);});
test('queued is explicitly not sent',()=>{const m=fixture('queued');m.claim=null;m.receipt=null;assert.match(render(m),/QUEUED - not sent/);});
test('claimed outcome remains unknown',()=>{const m=fixture('claimed_outcome_unknown');m.receipt=null;unknown(m);assert.match(render(m),/claim recorded/);});
test('rejection is separate from acknowledgment',()=>{const out=render(fixture('rejected'));assert.match(out,/REJECTED/);assert.doesNotMatch(out,/ACKNOWLEDGED/);});
test('unknown receipt is explicitly unknown',()=>unknown(fixture('unknown')));
test('message body is never read or displayed',()=>{const m=fixture();Object.defineProperty(m,'message',{get(){throw new Error('body access');}});assert.match(render(m),/ACKNOWLEDGED/);});
test('empty and malformed records remain bounded summaries',()=>{assert.match(renderDeliveryPanel({},opts),/No message records/);unknown(null);});
test('20 columns requests resize instead of showing a partial identity',()=>{const out=render(fixture(),{...opts,columns:20});assert.match(out,/RESIZE/);assert.doesNotMatch(out,/00000000/);assert.ok(out.split('\n').every(line=>line.length<=20));});
test('24, 40 and 80 column ASCII output retains complete identity',()=>{
  for(const columns of [24,40,80]) {const out=render(fixture(),{...opts,columns});assert.ok(out.split('\n').every(line=>line.length===columns));assert.ok(compact(out).includes(target.replaceAll('-','')));}
});
test('NO_COLOR presence suppresses color sequences',()=>{assert.doesNotMatch(render(fixture()),/\x1b\[[\d;]*m/);});
test('untrusted identity control sequences cannot change terminal style',()=>{const m=fixture();m.target.hostId='host\x1b[31mred\x1b[0m';const out=render(m);assert.doesNotMatch(out,/\x1b/);assert.match(out,/UNKNOWN/);});
test('ChatGPT null-host binding can show a caller-reported acknowledgment',()=>{
 const m=fixture();m.target.kind='chatgpt';m.target.hostId=null;m.claim.hostId=null;m.receipt.hostId=null;
 const out=render(m);assert.match(out,/ACKNOWLEDGED/);assert.match(out,/ChatGPT provider/);assert.match(out,/NOT OBSERVED/);
});
test('ChatGPT receipt with a fabricated host cannot acknowledge',()=>{
 const m=fixture();m.target.kind='chatgpt';m.target.hostId=null;m.claim.hostId=null;
 unknown(m);
});
test('Codex null-host record cannot acknowledge',()=>{
 const m=fixture();m.target.kind='codex-local';m.target.hostId=null;m.claim.hostId=null;m.receipt.hostId=null;
 unknown(m);
});
