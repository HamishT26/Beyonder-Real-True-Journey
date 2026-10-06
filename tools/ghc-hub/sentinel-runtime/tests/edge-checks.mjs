import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createOpenAIHttp, abortRace} from '../src/http.mjs';
import {FileLedger, readLocalJson} from '../src/ledger.mjs';
import {createSentinelRuntime} from '../src/client.mjs';
import {prepareRequest, ENDPOINT} from '../src/contract.mjs';
import {cliMain} from '../src/cli.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const artifacts = process.env.GHC_SENTINEL_TEST_ARTIFACTS || root;
fs.mkdirSync(path.join(artifacts, 'private'), {recursive:true});
fs.mkdirSync(path.join(artifacts, 'receipts'), {recursive:true});
const folder = path.join(artifacts, 'private', 'edge-01');
const receiptPath = path.join(artifacts, 'receipts', 'edges-01.json');
if (fs.existsSync(folder) || fs.existsSync(receiptPath)) throw new Error('Prior edge checks preserved');
fs.mkdirSync(folder);
const files = ['src/contract.mjs', 'src/ledger.mjs', 'src/http.mjs', 'src/client.mjs', 'src/cli.mjs', 'tests/edge-checks.mjs'];
const sources = files.map(file => {
  const bytes = fs.readFileSync(path.join(root, file)); const target = path.join(folder, 'source', file);
  fs.mkdirSync(path.dirname(target), {recursive: true}); fs.writeFileSync(target, bytes, {flag: 'wx'});
  return {path: file, sha256: crypto.createHash('sha256').update(bytes).digest('hex')};
});
const checks = [];
async function check(id, fn) {try {await fn(); checks.push({id, passed: true});} catch (error) {checks.push({id, passed: false, errorType: error.name});fs.appendFileSync(path.join(folder, 'failures.txt'), `${id}\n${error.stack}\n`);}}
const grant = {schema: 'ghc.sentinel.budget.v1', currency: 'USD', ceilingMicros: '1000', priorSpendMicros: '0', priorCommittedMicros: '0',
  availableBudgetVerified: true, scope: 'local-allocation', approvalReference: 'synthetic-test-only'};
const request = {schema: 'ghc.sentinel.runtime.request.v1', sentinelId: 'sentinel-test', provider: 'openai', model: 'fixture-text-model', input: 'Fixture', maxOutputTokens: 32};
const now = Date.parse('2026-10-07T00:00:00Z');
const quote = {schema: 'ghc.sentinel.quote.v1', kind: 'fixture', provider: 'openai', model: request.model, requestSha256: prepareRequest(request).requestSha256,
  currency: 'USD', serviceTier: 'default', inputTokensUpperBound: 100, inputCountVerified: true, inputCountSource: 'responses/input_tokens',
  inputUsdPerMillion: '1', outputUsdPerMillion: '2', fixedFeeUsd: '0.000001', allChargesCovered: true,
  source: 'fixture://synthetic-prices-not-real', verifiedAt: '2026-10-07T00:00:00Z', expiresAt: '2026-10-07T01:00:00Z'};
await check('pre-aborted-http-never-calls-fetch', async () => {
  let calls = 0; const http = createOpenAIHttp({kind: 'fixture', fetchImpl: () => {calls++; throw new Error('should not run');}});
  const aborter = new AbortController(); aborter.abort();
  await assert.rejects(http.request('{}', {key: 'SYNTHETIC_SECRET', runId: crypto.randomUUID(), signal: aborter.signal}), /aborted/);
  await new Promise(resolve => setTimeout(resolve, 10)); assert.equal(calls, 0);
});
await check('pre-aborted-race-consumes-late-rejection', async () => {
  const errors = []; const listener = error => errors.push(error); process.on('unhandledRejection', listener);
  try { const signal = new AbortController(); signal.abort(); await assert.rejects(abortRace(Promise.reject(new Error('synthetic')), signal.signal));
    await new Promise(resolve => setTimeout(resolve, 10)); assert.equal(errors.length, 0);
  } finally {process.removeListener('unhandledRejection', listener);}
});
await check('denied-runs-have-create-only-bounded-directory-count', async () => {
  const ledger = new FileLedger(path.join(folder, 'run-limit'), {maxRuns: 2}); let calls = 0;
  const runtime = createSentinelRuntime({ledger, now: () => now, httpProvider: createOpenAIHttp({kind: 'fixture', fetchImpl: () => {calls++;}})});
  const args = {request, execute: true, execution: 'simulate', reviewedRequestSha256: prepareRequest(request).requestSha256};
  assert.equal((await runtime.runOnce(args)).receiptSaved, true); assert.equal((await runtime.runOnce(args)).receiptSaved, true);
  const third = await runtime.runOnce(args); assert.equal(third.receiptSaved, false); assert.equal(calls, 0);
  assert.equal(fs.readdirSync(path.join(ledger.root, 'runs')).length, 2);
});
await check('local-json-file-bound-and-reserved-paths', () => {
  const file = path.join(folder, 'BIG.json'); fs.writeFileSync(file, ' '.repeat(100)); assert.throws(() => readLocalJson(file, 20));
  assert.throws(() => readLocalJson(path.join(folder, 'con.json')));
});
await check('prior-spend-and-prior-commitments-are-both-deducted', () => {
  const ledger = new FileLedger(path.join(folder, 'known-prior')); ledger.initialize({...grant, priorSpendMicros: '100', priorCommittedMicros: '200'});
  assert.equal(ledger.snapshot().availableMicros, '700'); const id = crypto.randomUUID(); ledger.reserve(id, 'a'.repeat(64), '600', 'b'.repeat(64));
  assert.equal(ledger.snapshot().availableMicros, '100'); ledger.settle(id, '21', 'reported_usage_upper_bound'); assert.equal(ledger.snapshot().availableMicros, '679');
});
await check('bounded-json-cli-accepts-escaped-text-without-echo', async () => {
  const input = {...request, input: '\u0000'.repeat(30000)}; const file = path.join(folder, 'escaped.json'); fs.writeFileSync(file, JSON.stringify(input));
  let output = ''; const code = await cliMain(['validate', '--request', file], {stdout: value => {output += value;}});
  assert.equal(code, 0); assert.equal(JSON.parse(output).valid, true); assert.ok(output.length < 500);
});
await check('current-http-and-ledger-still-complete-one-simulated-response', async () => {
  const ledger = new FileLedger(path.join(folder, 'final-smoke')); ledger.initialize(grant); let calls = 0;
  const runtime = createSentinelRuntime({ledger, now: () => now, credentialProvider: () => ({kind: 'openai-api-key', value: 'SYNTHETIC_SECRET'}),
    httpProvider: createOpenAIHttp({kind: 'fixture', fetchImpl: async (url, options) => {
      calls++; assert.equal(url, ENDPOINT); assert.equal(options.redirect, 'error'); assert.equal(ledger.snapshot().heldMicros, '165');
      const bytes = Buffer.from(JSON.stringify({object: 'response', status: 'completed', model: request.model, output: [{type: 'message', role: 'assistant', content: [{type: 'output_text', text: 'Done'}]}], usage: {input_tokens: 10, output_tokens: 5}}));
      return {url: ENDPOINT, status: 200, redirected: false, headers: new Headers({'content-type': 'application/json'}), body: new ReadableStream({start(controller) {controller.enqueue(bytes);controller.close();}})};
    }})});
  const result = await runtime.runOnce({request, quote, execute: true, execution: 'simulate', reviewedRequestSha256: prepareRequest(request).requestSha256});
  assert.equal(result.status, 'completed'); assert.equal(result.text, 'Done'); assert.equal(calls, 1); assert.equal(ledger.snapshot().accountedUpperMicros, '21');
});
const result = {sources, checks, counts: {checks: checks.length, passed: checks.filter(row => row.passed).length, failed: checks.filter(row => !row.passed).length}, realApiRequests: 0, realCredentialsRead: 0, aiHelpersCreated: 0};
fs.writeFileSync(receiptPath, JSON.stringify(result, null, 2)); console.log(JSON.stringify(result.counts)); process.exitCode = result.counts.failed ? 1 : 0;
