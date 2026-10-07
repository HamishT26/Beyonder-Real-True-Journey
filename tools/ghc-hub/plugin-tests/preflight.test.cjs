const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const h=require('../plugins/ghc-nexus-hub-exec/scripts/nexus_preflight.cjs');
const spec=require('../plugins/ghc-nexus-hub-exec/references/hub-source.json');
const hub='node "D:/GHC-Archives/global-tools/ghc-nexus-hub/hub.mjs" ';
const payload=command=>({hook_event_name:'PreToolUse',tool_name:'Bash',tool_input:{command}});
const run=(command,sourceCheck=()=>true)=>h.evaluate(payload(command),{sourceCheck,actions:spec.actions});
test('unrelated commands and wrong events do not inspect files',()=>{
 const fail=()=>{throw Error('unexpected file access')};
 assert.deepEqual(run('git status',fail),[]);
 assert.deepEqual(h.evaluate({...payload(hub+'run app --execute'),hook_event_name:'Stop'},{sourceCheck:fail}),[]);
});
test('valid quoted Hub plans and explicit effects retain their boundary',()=>{
 assert.deepEqual(run(hub+'plan app-admin --json'),[]);
 assert.deepEqual(run(hub+'run app-admin-check --execute --json'),[]);
 assert.deepEqual(run(hub+'lab run --id diffusion --size 1000 --execute --json'),[]);
});
test('source mismatch and unresolved alias are advisory and never execute',()=>{
 assert.deepEqual(run(hub+'run app --execute',()=>false),['source_manifest']);
 assert.deepEqual(run('ghc-nexus run app --execute'),['source_manifest']);
 assert.deepEqual(Object.keys(h.output(['source_manifest'])),['systemMessage']);
});
test('configuration check distinguishes valid display changes from privileged keys',()=>{
 assert.deepEqual(run('python config_menu.py propose --set tui.animations=false'),[]);
 assert.deepEqual(run('python config_menu.py propose --set sandbox_mode="danger-full-access"'),['config_schema']);
 assert.deepEqual(run('python config_menu.py propose --set tui.animations=1'),['config_schema']);
});
test('selected memory export is bounded and does not echo sensitive literals',()=>{
 assert.deepEqual(run(hub+'memory export --id alpha,beta --execute'),[]);
 assert.ok(run(hub+'memory export --id * --execute').includes('secret_export'));
 const token='sk-'+'syntheticNotARealCredential000000';
 const result=h.output(run(hub+'memory export --id '+token+' --execute'));
 assert.ok(result.systemMessage);assert.equal(JSON.stringify(result).includes(token),false);
 const ids=Array.from({length:30},(_,i)=>'record-'+i);
 assert.deepEqual(run(hub+'memory export --id '+ids.join(',')+' --execute'),[]);
 assert.ok(run(hub+'memory export --id '+[...ids,'extra'].join(',')+' --execute').includes('secret_export'));
 assert.ok(run(hub+'memory export --id alpha,alpha --execute').includes('secret_export'));
});
test('new snapshot writes retain source and execution advisories',()=>{
 assert.deepEqual(run(hub+'memory snapshot --id alpha --execute'),[]);
 assert.ok(run(hub+'memory snapshot --id alpha --execute',()=>false).includes('source_manifest'));
 assert.ok(run(hub+'memory restore --id 11111111-2222-3333-4444-555555555555').includes('selected_route'));
});
test('message writes require execute and the pinned source',()=>{
 assert.deepEqual(run(hub+'messages draft --file D:/request.json --execute'),[]);
 assert.ok(run(hub+'messages queue --file D:/request.json --execute',()=>false).includes('source_manifest'));
 assert.ok(run(hub+'messages receipt --file D:/receipt.json').includes('selected_route'));
});
test('message plans and claims require their exact selected inputs',()=>{
 assert.ok(run(hub+'messages plan').includes('selected_route'));
 assert.ok(run(hub+'messages claim --id someone --execute').includes('selected_route'));
 assert.deepEqual(run(hub+'messages claim --id 11111111-2222-3333-4444-555555555555 --execute'),[]);
 assert.ok(run(hub+'messages send --execute').includes('selected_route'));
});
test('unknown routes, missing selection and compound shell expressions stay unclassified',()=>{
 assert.deepEqual(run(hub+'run arbitrary --execute'),['selected_route']);
 assert.deepEqual(run(hub+'run app'),['selected_route']);
 assert.deepEqual(run(hub+'chats open --execute'),['selected_route']);
 assert.deepEqual(run(hub+'run app --execute; echo more'),['selected_route']);
});
test('finite budget bounds accept the endpoints and reject duplicate or invalid sizes',()=>{
 for(const n of ['1','200000'])assert.deepEqual(run(hub+'lab plan --id queue --size '+n),[]);
 for(const n of ['0','200001','NaN','1.5'])assert.ok(run(hub+'lab plan --id queue --size '+n).includes('budget_admission'));
 assert.ok(run(hub+'lab plan --id queue --size 2 --size 3').includes('budget_admission'));
});
test('pin verifier checks real bytes and rejects tampering and hardlinks',()=>{
 const parent=process.env.GHC_HUB_TEST_TMP||path.join(__dirname,'fixtures');fs.mkdirSync(parent,{recursive:true});const dir=fs.mkdtempSync(path.join(parent,'pin-'));
 const p=path.join(dir,'core.mjs');fs.writeFileSync(p,'fixture');const pins=[{path:'core.mjs',sha256:crypto.createHash('sha256').update('fixture').digest('hex')}];
 assert.equal(h.checkPins(dir,pins),true);fs.writeFileSync(p,'changed');assert.equal(h.checkPins(dir,pins),false);
 fs.writeFileSync(p,'fixture');fs.linkSync(p,path.join(dir,'copy.mjs'));assert.equal(h.checkPins(dir,pins),false);
});
test('registered output contains only supported PreToolUse advisory fields',()=>{
 assert.deepEqual(h.output([]),{});const result=h.output(Object.keys(h.notices));
 assert.deepEqual(Object.keys(result),['systemMessage']);assert.ok(result.systemMessage.length<1800);
 assert.equal('continue' in result,false);assert.equal('permissionDecision' in result,false);
});
