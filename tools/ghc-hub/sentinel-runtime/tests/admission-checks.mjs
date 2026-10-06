import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {FileLedger} from '../src/ledger.mjs';
import {createRequest} from '../src/contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const artifacts = process.env.GHC_SENTINEL_TEST_ARTIFACTS || root;
fs.mkdirSync(path.join(artifacts, 'private'), {recursive:true});
fs.mkdirSync(path.join(artifacts, 'receipts'), {recursive:true});
const state = path.join(artifacts, 'private', 'admission-01');
const resultPath = path.join(artifacts, 'receipts', 'admission-01.json');
if (fs.existsSync(state) || fs.existsSync(resultPath)) throw new Error('Prior admission checks preserved');
fs.mkdirSync(state); const checks = [];
function check(id, fn) {try {fn();checks.push({id, passed: true});}catch(error){checks.push({id, passed: false, errorType:error.name});fs.appendFileSync(path.join(state,'failures.txt'),id+'\n'+error.stack+'\n');}}
check('run-directory-admission-is-serialized-across-ledger-instances', () => {
  const a = new FileLedger(path.join(state, 'ledger'), {maxRuns: 1}); const b = new FileLedger(a.root, {maxRuns: 1});
  const original = a.create.bind(a); let contentionObserved = false;
  a.create = (relative, value) => {
    if (relative.endsWith('intent.json')) {
      assert.throws(() => b.beginRun(crypto.randomUUID(), {schema:'fixture'}), /ledger_busy/); contentionObserved = true;
    }
    return original(relative, value);
  };
  const id = crypto.randomUUID(); a.beginRun(id, {schema:'fixture', runId:id});
  assert.equal(contentionObserved, true); assert.equal(fs.readdirSync(path.join(a.root, 'runs')).length, 1);
  assert.throws(() => b.beginRun(crypto.randomUUID(), {schema:'fixture'}), /run_receipt_capacity/);
});
check('known-key-patterns-cannot-be-logged-as-model-or-sentinel-label', () => {
  const key = 'sk-proj-'+'a'.repeat(32); const base={schema:'ghc.sentinel.runtime.request.v1',sentinelId:'sentinel-test',provider:'openai',model:'fixture-model',input:'Fixture',maxOutputTokens:32};
  assert.throws(() => createRequest({...base,model:key}), /credential_material/);
  assert.throws(() => createRequest({...base,sentinelId:key}), /credential_material/);
});
check('known-key-pattern-cannot-be-budget-approval-reference', () => {
  const ledger=new FileLedger(path.join(state,'bad-reference'));
  assert.throws(()=>ledger.initialize({schema:'ghc.sentinel.budget.v1',currency:'USD',ceilingMicros:'1000',priorSpendMicros:'0',priorCommittedMicros:'0',availableBudgetVerified:true,scope:'local-allocation',approvalReference:'sk-proj-'+'a'.repeat(32)}),/credential_material/);
});
check('create-only-intent-and-receipt-remain-intact', () => {
  const ledger=new FileLedger(path.join(state,'immutable')); const id=crypto.randomUUID(); ledger.beginRun(id,{schema:'fixture',runId:id});
  ledger.receipt(id,{outcome:'fixture'}); const file=path.join(ledger.root,'runs',id,'receipt.json'); const before=fs.readFileSync(file);
  assert.throws(()=>ledger.receipt(id,{outcome:'replacement'})); assert.deepEqual(fs.readFileSync(file),before);
});
const sources=['src/contract.mjs','src/ledger.mjs','tests/admission-checks.mjs'].map(file=>({path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')}));
const result={sources,checks,counts:{checks:checks.length,passed:checks.filter(row=>row.passed).length,failed:checks.filter(row=>!row.passed).length},realApiRequests:0,aiHelpersCreated:0,childrenStarted:0};
fs.writeFileSync(resultPath,JSON.stringify(result,null,2)); console.log(JSON.stringify(result.counts)); process.exitCode=result.counts.failed?1:0;
