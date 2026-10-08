import test from 'node:test';
import assert from 'node:assert/strict';
import {codexOptions,plan} from './core.mjs';

const c={platform:'win32',cwd:'D:/test-workspace',codex:'D:/tools/codex.exe'};
test('new CLI launch does not blanket-disable App or MCP capabilities',()=>{
 const args=codexOptions(c);
 assert.equal(args.some(x=>/^mcp_servers\..*\.enabled=false$/.test(x)),false);
 assert.equal(args.includes('features.apps=false'),false);
 assert.equal(args.includes('--ephemeral'),false);
 assert.equal(args.includes('features.multi_agent=false'),true);
});
test('new CLI launch keeps the selected model and explicit executor settings',()=>{
 const p=plan('codex',{},c);
 assert.equal(p.command,c.codex);
 assert.equal(p.args[p.args.indexOf('--model')+1],'gpt-6-astra');
 assert.equal(p.args[p.args.indexOf('--sandbox')+1],'danger-full-access');
 assert.ok(p.args.includes('model_reasoning_effort="max"'));
 assert.ok(p.args.includes('service_tier="priority"'));
 assert.match(p.note,/App\/MCP capabilities are inherited/);
});
test('existing session resume never overrides model, apps or registered MCPs',()=>{
 const id='00112233-4455-6677-8899-aabbccddeeff';
 const p=plan('codex-resume',{session:id},c);
 assert.deepEqual(p.args,['--no-daemon','--no-alt-screen','resume',id]);
});
