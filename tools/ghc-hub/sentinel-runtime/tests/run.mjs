import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import os from 'node:os';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createRequest, prepareRequest, offlinePlan, normalizeQuote, upperCost, usdMicros, fromHubSpec, ENDPOINT, LIMITS} from '../src/contract.mjs';
import {FileLedger} from '../src/ledger.mjs';
import {createOpenAIHttp} from '../src/http.mjs';
import {createSentinelRuntime} from '../src/client.mjs';
import {cliMain} from '../src/cli.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const artifacts = process.env.GHC_SENTINEL_TEST_ARTIFACTS || root;
fs.mkdirSync(path.join(artifacts, 'private'), {recursive:true});
fs.mkdirSync(path.join(artifacts, 'receipts'), {recursive:true});
const attempt = process.argv[2] ?? '01';
assert.match(attempt, /^\d{2}$/);
const privateRoot = path.join(artifacts, 'private', `attempt-${attempt}`);
const receiptFile = path.join(artifacts, 'receipts', `tests-${attempt}.json`);
if (fs.existsSync(privateRoot) || fs.existsSync(receiptFile)) throw new Error('Prior attempt preserved');
fs.mkdirSync(privateRoot, {recursive: true});
const sourceFiles = ['package.json', ...fs.readdirSync(path.join(root, 'src')).map(name => 'src/' + name), 'tests/run.mjs'];
const sources = sourceFiles.map(file => {
  const bytes = fs.readFileSync(path.join(root, file)); const target = path.join(privateRoot, 'source', file);
  fs.mkdirSync(path.dirname(target), {recursive: true}); fs.writeFileSync(target, bytes, {flag: 'wx'});
  return {path: file, bytes: bytes.length, sha256: crypto.createHash('sha256').update(bytes).digest('hex')};
});
const fixedNow = Date.parse('2026-10-07T00:00:00.000Z');
const SECRET = 'SYNTHETIC_PRIVATE_CREDENTIAL_CANARY';
const raw = {schema: 'ghc.sentinel.runtime.request.v1', sentinelId: 'sentinel-fixture', provider: 'openai',
  model: 'fixture-text-model', input: 'Synthetic test input.', instructions: 'Return concise plain text.', maxOutputTokens: 32};
const grant = {schema: 'ghc.sentinel.budget.v1', currency: 'USD', ceilingMicros: '1000', priorSpendMicros: '0',
  priorCommittedMicros: '0', availableBudgetVerified: true, scope: 'local-allocation', approvalReference: 'fixture-only-not-real-budget'};
function quote(request = raw, overrides = {}) {
  return {schema: 'ghc.sentinel.quote.v1', kind: 'fixture', provider: request.provider, model: request.model,
    requestSha256: prepareRequest(request).requestSha256, currency: 'USD', serviceTier: 'default', inputTokensUpperBound: 100,
    inputCountVerified: true, inputCountSource: 'responses/input_tokens', inputUsdPerMillion: '1', outputUsdPerMillion: '2',
    fixedFeeUsd: '0.000001', allChargesCovered: true, source: 'fixture://synthetic-prices-not-real',
    verifiedAt: '2026-10-07T00:00:00.000Z', expiresAt: '2026-10-07T01:00:00.000Z', ...overrides};
}
function payload(overrides = {}) {
  return {object: 'response', id: 'resp_fixture', status: 'completed', model: raw.model, service_tier: 'default',
    output: [{type: 'reasoning', summary: []}, {type: 'message', role: 'assistant', content: [{type: 'output_text', text: 'First'}, {type: 'output_text', text: 'Second'}]}],
    usage: {input_tokens: 10, output_tokens: 5, total_tokens: 15, input_tokens_details: {cached_tokens: 8}, output_tokens_details: {reasoning_tokens: 2}}, ...overrides};
}
function response(data = payload(), {status = 200, url = ENDPOINT, redirected = false, contentType = 'application/json', length = null, bytes = null, stream = null} = {}) {
  const buffer = bytes ?? Buffer.from(JSON.stringify(data));
  const headers = new Headers({'content-type': contentType}); if (length !== null) headers.set('content-length', length);
  return {status, url, redirected, headers, body: stream ?? new ReadableStream({start(controller) {controller.enqueue(buffer); controller.close();}})};
}
let sequence = 0; let fakeHttpInvocations = 0;
function setup(options = {}) {
  const stateRoot = path.join(privateRoot, 'states', String(++sequence));
  const ledger = options.ledger ?? new FileLedger(stateRoot);
  if (options.initialize !== false) ledger.initialize({...grant, ...options.grant});
  const events = []; let credentials = 0, httpCalls = 0;
  const httpProvider = createOpenAIHttp({kind: options.kind ?? 'fixture', fetchImpl: async (url, config) => {
    fakeHttpInvocations++; httpCalls++; events.push('http');
    assert.equal(url, ENDPOINT); assert.equal(config.redirect, 'error'); assert.equal(config.credentials, 'omit');
    assert.equal(config.method, 'POST'); assert.equal(config.headers.Authorization, 'Bearer ' + SECRET);
    assert.equal(ledger.snapshot().unsettled, 1, 'Reservation must exist before HTTP');
    const body = JSON.parse(config.body); assert.equal(body.store, false); assert.equal(body.stream, false); assert.equal(body.background, false);
    assert.deepEqual(body.tools, []); assert.equal(body.tool_choice, 'none'); assert.equal(body.service_tier, 'default');
    return options.fetch ? options.fetch(url, config) : response();
  }});
  const runtime = createSentinelRuntime({ledger, httpProvider, allowNetwork: options.allowNetwork ?? false, now: () => fixedNow,
    timeoutMs: options.timeoutMs ?? 1000, maxResponseBytes: options.maxResponseBytes ?? LIMITS.responseBytes,
    maxOutputBytes: options.maxOutputBytes ?? LIMITS.outputBytes,
    credentialProvider: options.noCredential ? null : async context => {
      credentials++; events.push('credential'); assert.equal(ledger.snapshot().unsettled, 1, 'Reserve before credentials');
      return options.credential ? options.credential(context) : {kind: 'openai-api-key', value: SECRET};
    }});
  return {ledger, runtime, events, stateRoot, get httpCalls() {return httpCalls;}, get credentials() {return credentials;},
    invoke: overrides => runtime.runOnce({request: raw, quote: quote(), execute: true, execution: 'simulate',
      reviewedRequestSha256: prepareRequest(raw).requestSha256, ...overrides})};
}
const checks = []; const started = performance.now(); let peakRss = process.memoryUsage().rss, minimumFreeRam = os.freemem();
function save() {
  peakRss = Math.max(peakRss, process.memoryUsage().rss); minimumFreeRam = Math.min(minimumFreeRam, os.freemem());
  fs.writeFileSync(receiptFile, JSON.stringify({attempt, sources, checks, counts: {checks: checks.length,
    passed: checks.filter(row => row.passed).length, failed: checks.filter(row => !row.passed).length},
    fakeHttpInvocations, realApiRequests: 0, realCredentialsRead: 0, automaticRetries: 0,
    node: process.version, platform: process.platform, elapsedMs: +(performance.now() - started).toFixed(3),
    resources: {peakSampledRssBytes: peakRss, minimumSampledFreeRamBytes: minimumFreeRam},
    syntheticPricesOnly: true}, null, 2));
}
async function check(id, fn) {
  if (checks.length >= 150) throw new Error('Check budget exceeded');
  try { await fn(); checks.push({id, passed: true}); }
  catch (error) { checks.push({id, passed: false, errorType: error.name}); fs.appendFileSync(path.join(privateRoot, 'failures.txt'), `${id}\n${error.stack}\n`); }
  save();
}
async function unknownCase(id, options, reason) {
  await check(id, async () => {
    const f = setup(options), result = await f.invoke();
    assert.equal(result.status, 'unknown'); if (reason) assert.equal(result.reason, reason);
    assert.equal(result.httpAttempts, 1); assert.equal(f.httpCalls, 1); assert.equal(result.accounting.reservationRetained, true);
    assert.equal(new FileLedger(f.stateRoot).snapshot().heldMicros, '165');
    assert.equal(f.runtime.requiresReview, true); assert.equal(result.text, null);
  });
}

await check('hub-21-template-adapts-with-explicit-model-and-no-mutation', async () => {
  const hub = await import(pathToFileURL('D:/GHC-Archives/worktrees/saelin-reed-main/tools/ghc-hub/sentinel.mjs'));
  const spec = hub.sentinelTemplate('sentinel-fixture'); assert.equal(hub.validateSentinel(spec).valid, true);
  const before = JSON.stringify(spec); const adapted = fromHubSpec(spec, {input: 'Fixture', model: raw.model, maxOutputTokens: 32});
  assert.equal(adapted.model, raw.model); assert.equal(JSON.stringify(spec), before); assert.deepEqual(JSON.parse(prepareRequest(adapted).serialized).tools, []);
  assert.throws(() => fromHubSpec({...spec, modalities: ['image']}, {input: 'Fixture', model: raw.model}));
});
await check('missing-model-provider-and-extra-fields-rejected', () => {
  for (const change of [{model: null}, {provider: 'unsupported'}, {baseUrl: 'https://example.invalid'}, {apiKey: SECRET}, {maxOutputTokens: 1}]) assert.throws(() => createRequest({...raw, ...change}));
});
await check('text-and-known-credential-input-bounds', () => {
  assert.throws(() => createRequest({...raw, input: 'x'.repeat(65537)}));
  assert.throws(() => createRequest({...raw, input: 'sk-proj-' + 'X'.repeat(32)}));
  assert.throws(() => createRequest({...raw, input: ''}));
});
await check('offline-plan-denies-unknown-price-and-budget-without-global-cap-claim', () => {
  const plan = offlinePlan(raw, {now: fixedNow}); assert.equal(plan.eligibleForExplicitExecution, false);
  assert.ok(plan.blockers.includes('pricing_and_token_evidence_required')); assert.ok(plan.blockers.includes('known_available_budget_required'));
  assert.equal(plan.aggregateUsd50Enforced, false); assert.equal(plan.networkCalls, 0); assert.ok(!JSON.stringify(plan).includes(raw.input));
});
await check('exact-micro-dollar-ceilings-and-conservative-cache-handling', () => {
  const q = normalizeQuote(quote(), prepareRequest(raw), 'simulate', fixedNow);
  assert.equal(upperCost(q, 100, 32), 165n); assert.equal(upperCost(q, 10, 5), 21n);
  assert.equal(usdMicros('0.000001'), 1n); assert.throws(() => usdMicros('0.0000001')); assert.throws(() => usdMicros('1e-6'));
});
await check('request-bound-token-and-price-evidence-required', () => {
  for (const change of [{requestSha256: '0'.repeat(64)}, {inputCountVerified: false}, {allChargesCovered: false}, {currency: 'NZD'},
    {serviceTier: 'priority'}, {expiresAt: '2026-10-06T00:00:00Z'}, {inputTokensUpperBound: -1}]) {
    assert.throws(() => normalizeQuote(quote(raw, change), prepareRequest(raw), 'simulate', fixedNow));
  }
  assert.throws(() => normalizeQuote(quote(), prepareRequest(raw), 'live', fixedNow));
});
await check('budget-needs-known-prior-spend-and-commitments', () => {
  const ledger = new FileLedger(path.join(privateRoot, 'invalid-budget'));
  assert.throws(() => ledger.initialize({...grant, priorSpendMicros: null}));
  assert.throws(() => ledger.initialize({...grant, availableBudgetVerified: false}));
  assert.throws(() => ledger.initialize({...grant, ceilingMicros: '50000001'}));
  assert.equal(ledger.snapshot().known, false);
});
await check('successful-text-response-reserved-first-and-settled-conservatively', async () => {
  const f = setup(), result = await f.invoke(); assert.equal(result.status, 'completed'); assert.equal(result.text, 'First\nSecond');
  assert.deepEqual(f.events, ['credential', 'http']); assert.equal(result.accounting.reservedMicros, '165'); assert.equal(result.accounting.accountedUpperMicros, '21');
  const reopened = new FileLedger(f.stateRoot).snapshot(); assert.equal(reopened.accountedUpperMicros, '21'); assert.equal(reopened.heldMicros, '0'); assert.equal(reopened.availableMicros, '979');
  const record = f.ledger.read(`runs/${result.runId}/receipt.json`); assert.equal(record.execution, 'simulate'); assert.equal(record.remoteOutcomeConfirmed, false);
  assert.equal(record.promptRecorded, false); assert.equal(record.responseTextRecorded, false); assert.equal(record.credentialRecorded, false);
  assert.ok(!JSON.stringify(record).includes(SECRET)); assert.ok(!JSON.stringify(record).includes(raw.input));
});
await check('explicit-execution-and-reviewed-hash-gates-precede-credentials', async () => {
  for (const change of [{execute: false}, {reviewedRequestSha256: '0'.repeat(64)}, {execution: 'live'}]) {
    const f = setup(), r = await f.invoke(change); assert.equal(r.httpAttempts, 0); assert.equal(f.credentials, 0);
  }
});
await check('live-network-disabled-and-fixture-pricing-cannot-enable-it', async () => {
  const a = setup({kind: 'live'}), x = await a.invoke({execution: 'live'});
  assert.equal(x.reason, 'network_execution_not_authorized'); assert.equal(a.httpCalls, 0);
  const b = setup({kind: 'live', allowNetwork: true}), y = await b.invoke({execution: 'live'});
  assert.equal(y.reason, 'fixture_pricing_not_live'); assert.equal(b.credentials, 0); assert.equal(b.httpCalls, 0);
});
await check('missing-budget-or-quote-denies-before-credential-access', async () => {
  const a = setup({initialize: false}), x = await a.invoke(); assert.equal(x.reason, 'known_available_budget_required'); assert.equal(a.credentials, 0);
  const b = setup(), y = await b.invoke({quote: null}); assert.equal(y.reason, 'pricing_and_token_evidence_required'); assert.equal(b.credentials, 0);
});
await check('insufficient-budget-does-not-reserve-or-settle', async () => {
  const f = setup({grant: {ceilingMicros: '164'}}), r = await f.invoke();
  assert.equal(r.reason, 'insufficient_local_budget'); assert.equal(f.credentials, 0); assert.equal(f.ledger.snapshot().reservations, 0);
  assert.equal(r.accounting.reservedMicros, null);
});
await check('reused-run-id-cannot-overwrite-or-repeat-http', async () => {
  const f = setup(), runId = crypto.randomUUID(); const first = await f.invoke({runId}); const receipt = path.join(f.stateRoot, 'runs', runId, 'receipt.json');
  const bytes = fs.readFileSync(receipt); const second = await f.invoke({runId});
  assert.equal(first.status, 'completed'); assert.equal(second.httpAttempts, 0); assert.equal(f.httpCalls, 1); assert.deepEqual(fs.readFileSync(receipt), bytes);
});
await check('known-not-sent-credential-failure-releases-reservation-without-secret-log', async () => {
  const f = setup({credential: () => {throw new Error(SECRET);}}), r = await f.invoke();
  assert.equal(r.status, 'not_sent'); assert.equal(r.reason, 'credential_unavailable'); assert.equal(f.httpCalls, 0);
  assert.equal(f.ledger.snapshot().heldMicros, '0'); assert.ok(!JSON.stringify(r).includes(SECRET));
});
await check('developers-oauth-is-not-an-api-key-provider', async () => {
  const f = setup({credential: () => ({kind: 'developers-connector-oauth', value: SECRET})}), r = await f.invoke();
  assert.equal(r.reason, 'wrong_credential_kind'); assert.equal(f.httpCalls, 0); assert.equal(f.ledger.snapshot().heldMicros, '0');
});
await check('credential-header-injection-and-credential-in-body-denied', async () => {
  const f = setup({credential: () => ({kind: 'openai-api-key', value: SECRET + '\r\nX-Leak: yes'})}), x = await f.invoke();
  assert.equal(x.reason, 'invalid_credential'); assert.equal(f.httpCalls, 0);
  const altered = {...raw, input: SECRET}; const b = setup(); const y = await b.invoke({request: altered, quote: quote(altered), reviewedRequestSha256: prepareRequest(altered).requestSha256});
  assert.equal(y.reason, 'credential_in_payload'); assert.equal(b.httpCalls, 0);
});
await check('opaque-secret-echo-redacted-and-terminal-controls-removed', async () => {
  const f = setup({fetch: () => response(payload({output: [{type: 'message', role: 'assistant', content: [{type: 'output_text', text: SECRET + '\u001b[31m\u202e'}]}]}))});
  const r = await f.invoke(); assert.equal(r.status, 'completed'); assert.ok(!r.text.includes(SECRET)); assert.ok(!/[\u001b\u202e]/.test(r.text));
});
await unknownCase('redirect-is-rejected-with-reservation-retained', {fetch: () => response({}, {status: 302, url: 'https://example.invalid/', redirected: true})}, 'redirect_rejected');
await unknownCase('changed-response-origin-is-rejected', {fetch: () => response(payload(), {url: 'https://example.invalid/v1/responses'})}, 'redirect_rejected');
await unknownCase('429-is-not-retried-and-not-assumed-free', {fetch: () => response({}, {status: 429})}, 'http_status_unknown_cost');
await unknownCase('transport-throw-holds-cost-and-hides-provider-error', {fetch: () => {throw new Error(SECRET);}}, 'transport_or_response_failure');
await unknownCase('advertised-response-size-limit', {fetch: () => response(payload(), {length: '262145'})}, 'response_size_limit');
await unknownCase('actual-response-size-limit', {maxResponseBytes: 100, fetch: () => response({}, {bytes: Buffer.alloc(101, 65)})}, 'response_size_limit');
await unknownCase('wrong-content-type', {fetch: () => response(payload(), {contentType: 'text/html'})}, 'unexpected_content_type');
await unknownCase('invalid-json-and-utf8', {fetch: () => response({}, {bytes: Buffer.from([255])})}, 'invalid_response_json');
await unknownCase('missing-usage-keeps-full-reservation', {fetch: () => response(payload({usage: null}))}, 'usage_unknown');
await unknownCase('unexpected-tools-never-execute', {fetch: () => response(payload({output: [{type: 'function_call', name: 'exec', arguments: SECRET}]}))}, 'unsupported_response_item');
await unknownCase('wrong-response-model', {fetch: () => response(payload({model: 'unquoted-model'}))}, 'invalid_response_schema');
await unknownCase('price-tier-drift', {fetch: () => response(payload({service_tier: 'priority'}))}, 'response_price_tier_mismatch');
await unknownCase('returned-text-bound', {maxOutputBytes: 3}, 'output_size_limit');
await check('approved-response-model-alias-is-explicit', async () => {
  const f = setup({fetch: () => response(payload({model: 'fixture-model-snapshot'}))});
  const r = await f.invoke({quote: quote(raw, {approvedResponseModels: [raw.model, 'fixture-model-snapshot']})}); assert.equal(r.status, 'completed');
});
await check('incomplete-and-refused-responses-are-distinct-with-usage', async () => {
  const a = setup({fetch: () => response(payload({status: 'incomplete'}))}); assert.equal((await a.invoke()).status, 'incomplete');
  const b = setup({fetch: () => response(payload({output: [{type: 'message', role: 'assistant', content: [{type: 'refusal', refusal: SECRET}]}]}))});
  const r = await b.invoke(); assert.equal(r.status, 'refused'); assert.ok(!JSON.stringify(r).includes(SECRET)); assert.equal(r.accounting.settlementSaved, true);
});
await check('usage-bound-breach-freezes-reopened-ledger', async () => {
  const f = setup({fetch: () => response(payload({usage: {input_tokens: 101, output_tokens: 0, total_tokens: 101}}))}), r = await f.invoke();
  assert.equal(r.status, 'usage_bound_breached'); assert.equal(r.text, null); assert.equal(new FileLedger(f.stateRoot).snapshot().overrun, true);
});
await check('cancel-before-http-is-known-not-sent', async () => {
  const signal = new AbortController(); signal.abort(); const f = setup(); const r = await f.invoke({signal: signal.signal});
  assert.equal(r.httpAttempts, 0); assert.equal(f.credentials, 0); assert.equal(f.ledger.snapshot().reservations, 0);
});
await check('credential-timeout-does-not-send-and-releases-known-reserve', async () => {
  const f = setup({timeoutMs: 25, credential: () => new Promise(() => {})}), r = await f.invoke();
  assert.equal(r.reason, 'timeout'); assert.equal(r.status, 'not_sent'); assert.equal(f.httpCalls, 0); assert.equal(f.ledger.snapshot().heldMicros, '0');
});
await unknownCase('http-timeout-retains-unknown-even-if-provider-ignores-abort', {timeoutMs: 25, fetch: () => new Promise(() => {})}, 'timeout');
await check('cancellation-after-dispatch-is-unknown-and-quarantines-client', async () => {
  const aborter = new AbortController(); const f = setup({fetch: (_url, options) => new Promise(() => {setTimeout(() => aborter.abort(), 10);})});
  const r = await f.invoke({signal: aborter.signal}); assert.equal(r.status, 'unknown'); assert.equal(r.reason, 'cancelled');
  const next = await f.invoke(); assert.equal(next.reason, 'client_requires_review'); assert.equal(f.httpCalls, 1); assert.equal(f.ledger.snapshot().heldMicros, '165');
});
await unknownCase('body-timeout-retains-unknown', {timeoutMs: 25, fetch: () => response({}, {stream: new ReadableStream({start() {}})})}, 'timeout');
await check('single-active-operation-and-budget-reservation-order', async () => {
  let unblock; const gate = new Promise(resolve => {unblock = resolve;});
  const f = setup({fetch: async () => {await gate; return response();}});
  const first = f.invoke(); while (f.httpCalls === 0) await new Promise(resolve => setTimeout(resolve, 1));
  const second = await f.invoke(); assert.equal(second.reason, 'operation_in_progress'); assert.equal(f.httpCalls, 1);
  unblock(); assert.equal((await first).status, 'completed');
});
await check('separate-ledger-instances-cannot-double-reserve', () => {
  const f = setup(); const other = new FileLedger(f.stateRoot); const hash = 'a'.repeat(64);
  f.ledger.reserve(crypto.randomUUID(), hash, '600', hash); assert.throws(() => other.reserve(crypto.randomUUID(), hash, '600', hash));
  other.reserve(crypto.randomUUID(), hash, '400', hash); assert.equal(f.ledger.snapshot().availableMicros, '0');
  f.ledger.withLock(() => assert.throws(() => other.reserve(crypto.randomUUID(), hash, '0', hash), /ledger_busy/));
});
await check('unknown-holds-and-crash-style-intent-survive-reopening', () => {
  const f = setup(); const id = crypto.randomUUID(), hash = 'b'.repeat(64);
  f.ledger.beginRun(id, {schema: 'fixture-intent', runId: id}); f.ledger.reserve(id, hash, '165', hash); f.ledger.markDispatch(id);
  const state = new FileLedger(f.stateRoot).snapshot(); assert.equal(state.heldMicros, '165'); assert.equal(state.unsettled, 1);
});
await check('stale-lock-fails-closed-without-removing-it', () => {
  const f = setup(); const lock = path.join(f.stateRoot, 'ledger', 'reservation.lock'); fs.writeFileSync(lock, 'synthetic-unowned-lock', {flag: 'wx'});
  assert.throws(() => f.ledger.reserve(crypto.randomUUID(), 'a'.repeat(64), '1', 'b'.repeat(64)), /ledger_busy/);
  assert.equal(fs.readFileSync(lock, 'utf8'), 'synthetic-unowned-lock');
});
await check('receipt-write-failure-keeps-reservation-and-output-private', async () => {
  const f = setup(); f.ledger.receipt = () => {throw new Error(SECRET);};
  const r = await f.invoke(); assert.equal(r.status, 'persistence_failure'); assert.equal(r.text, null); assert.equal(f.ledger.snapshot().heldMicros, '165');
  assert.ok(!JSON.stringify(r).includes(SECRET));
});
await check('intent-write-failure-prevents-http', async () => {
  const f = setup(); f.ledger.beginRun = () => {throw new Error(SECRET);};
  const r = await f.invoke(); assert.equal(f.httpCalls, 0); assert.equal(f.credentials, 0); assert.equal(r.receiptSaved, false);
});
await check('linked-accounting-record-rejected', () => {
  const f = setup(); const budget = path.join(f.stateRoot, 'ledger', 'budget.json');
  fs.linkSync(budget, path.join(f.stateRoot, 'ledger', 'budget-copy.json')); assert.throws(() => f.ledger.snapshot());
});
await check('corrupt-ledger-record-never-becomes-zero-spend', () => {
  const f = setup(); const id = crypto.randomUUID(); f.ledger.reserve(id, 'a'.repeat(64), '165', 'b'.repeat(64));
  fs.writeFileSync(path.join(f.stateRoot, 'ledger', 'entries', id + '.reserve.json'), '{'); assert.throws(() => f.ledger.snapshot());
});
await check('no-global-environment-access-in-production-client', () => {
  for (const file of fs.readdirSync(path.join(root, 'src'))) assert.ok(!fs.readFileSync(path.join(root, 'src', file), 'utf8').includes('process.env'));
});
await check('offline-cli-validation-and-plan-do-not-echo-prompt', async () => {
  const input = path.join(privateRoot, 'offline-request.json'); fs.writeFileSync(input, JSON.stringify(raw), {flag: 'wx'});
  for (const command of ['validate', 'plan']) {
    let output = ''; assert.equal(await cliMain([command, '--request', input], {stdout: value => {output += value;}}), 0);
    assert.equal(JSON.parse(output).networkCalls, 0); assert.ok(!output.includes(raw.input));
  }
  let denied = ''; assert.equal(await cliMain(['run', '--request', input], {stdout: value => {denied += value;}}), 2);
  assert.equal(JSON.parse(denied).reason, 'trusted_runtime_and_credential_provider_required');
});
await check('actual-offline-cli-process-is-bounded-and-json-only', () => {
  const result = spawnSync(process.execPath, ['--max-old-space-size=64', path.join(root, 'src', 'cli.mjs'), 'providers'],
    {cwd: root, shell: false, windowsHide: true, timeout: 5000, maxBuffer: 16384, encoding: 'utf8'});
  assert.equal(result.status, 0); assert.equal(result.stderr, ''); const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.providers[0].endpoint, ENDPOINT); assert.equal(parsed.networkCalls, 0);
});
await check('all-persisted-synthetic-run-records-omit-credential-and-prose', () => {
  const walk = directory => {for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
    const item = path.join(directory, entry.name); if (entry.isDirectory()) walk(item);
    else if (entry.name.endsWith('.json')) { const data = fs.readFileSync(item, 'utf8'); assert.ok(!data.includes(SECRET)); assert.ok(!data.includes(raw.input)); }
  }};
  walk(path.join(privateRoot, 'states'));
});
save();
console.log(JSON.stringify({attempt, checks: checks.length, passed: checks.filter(row => row.passed).length,
  failed: checks.filter(row => !row.passed).length, fakeHttpInvocations, realApiRequests: 0, peakRss, minimumFreeRam}));
process.exitCode = checks.some(row => !row.passed) ? 1 : 0;
