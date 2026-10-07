const test=require('node:test'),assert=require('node:assert/strict');
const {evaluate}=require('../plugins/ghc-nexus-hub-exec/scripts/nexus_preflight.cjs');
const base='node D:/GHC-Archives/global-tools/ghc-nexus-hub/hub.mjs study search --file D:/public/catalogue.json --search Riemann';
const payload=command=>({hook_event_name:'PreToolUse',tool_name:'Bash',tool_input:{command}});
test('read-only study lookup admits explicit source fingerprint without execute',()=>assert.deepEqual(evaluate(payload(base+' --fingerprint '+'a'.repeat(64))),[]));
test('study missing fingerprint or an execute flag is flagged as an invalid route',()=>{assert.ok(evaluate(payload(base)).includes('selected_route'));assert.ok(evaluate(payload(base+' --fingerprint '+'a'.repeat(64)+' --execute')).includes('selected_route'))});
