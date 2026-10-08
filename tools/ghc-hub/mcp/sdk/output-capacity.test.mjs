import test from 'node:test';
import assert from 'node:assert/strict';
import {PassThrough, Writable} from 'node:stream';
import {BoundedStdioTransport, boundedLimits, DEFAULT_LIMITS} from './src/bounded-transport.mjs';
import {copyRegistry, publicProjection, TOOL_SPECS, toolSuccess} from './src/contract.mjs';

function catalogue(count) {
  return Array.from({length: count}, (_, i) => 'a' + String(i).padStart(3, '0') + 'x'.repeat(60));
}
function response(count, id = 1, toolName = 'nexus.chats.list', availability = 'false') {
  const aliases = catalogue(count);
  const registry = copyRegistry({chats: aliases, labs: aliases, sentinels: [], remotes: []});
  const spec = TOOL_SPECS.find(s => s.name === toolName);
  const data = publicProjection(spec, {items: aliases.map((alias, i) => ({alias, available: availability === 'true' || (availability === 'mixed' && i % 2 === 0), private: 'DO_NOT_EXPORT'}))}, {}, registry);
  return {jsonrpc: '2.0', id, result: toolSuccess(data)};
}
function transport(t, limits = {}) {
  const input = new PassThrough();
  const output = new PassThrough();
  const parts = [];
  output.on('data', part => parts.push(part));
  const value = new BoundedStdioTransport({input, output, limits});
  t.after(() => value.close());
  return {value, bytes: () => Buffer.concat(parts)};
}

test('all 128 longest admitted aliases survive the complete duplicated wire result', async t => {
  const {value, bytes} = transport(t);
  const message = response(128);
  assert.equal(Buffer.byteLength(JSON.stringify(message) + '\n'), 25223);
  await value.send(message);
  const observed = JSON.parse(bytes().toString());
  assert.equal(observed.result.structuredContent.items.length, 128);
  assert.deepEqual(JSON.parse(observed.result.content[0].text), observed.result.structuredContent);
  assert.doesNotMatch(bytes().toString(), /DO_NOT_EXPORT/);
  assert.equal(value.closed, false);
});

test('the prior 45-alias control still fits and preserves correlation', async t => {
  const {value, bytes} = transport(t);
  await value.send(response(45, 'control'));
  assert.equal(JSON.parse(bytes()).id, 'control');
  assert.equal(JSON.parse(bytes()).result.structuredContent.items.length, 45);
});

test('maximum catalogue also fits with escaped 128-character correlation data', async t => {
  const {value, bytes} = transport(t);
  const id = '\u0000'.repeat(128);
  await value.send(response(128, id));
  assert.equal(JSON.parse(bytes()).id, id);
});

test('an explicit smaller output budget still rejects without leaking a partial frame', async t => {
  const {value, bytes} = transport(t, {outputLineBytes: 16384});
  await assert.rejects(value.send(response(128)), /Output capacity exceeded/);
  assert.equal((await value.done).reason, 'output_limit');
  assert.equal(bytes().length, 0);
});

test('oversized arbitrary output still closes and queue/session budgets stay bounded', async t => {
  const {value, bytes} = transport(t);
  await assert.rejects(value.send({jsonrpc: '2.0', id: 1, result: 'x'.repeat(65536)}));
  assert.equal((await value.done).reason, 'output_limit');
  assert.equal(bytes().length, 0);
  assert.equal(DEFAULT_LIMITS.queuedOutputBytes, 65536);
  assert.equal(DEFAULT_LIMITS.sessionOutputBytes, 1048576);
});

function exactFrame(size) {
  const frame = {jsonrpc: '2.0', id: 1, result: {text: ''}};
  frame.result.text = 'x'.repeat(size - Buffer.byteLength(JSON.stringify(frame) + '\n'));
  assert.equal(Buffer.byteLength(JSON.stringify(frame) + '\n'), size);
  return frame;
}

test('chat and lab catalogues preserve true, false and mixed values with multibyte IDs', async t => {
  const {value, bytes} = transport(t);
  for (const tool of ['nexus.chats.list', 'nexus.lab.catalogue']) {
    for (const availability of ['true', 'false', 'mixed']) {
      const frame = response(128, '🌿'.repeat(128), tool, availability);
      await value.send(frame);
    }
  }
  const frames = bytes().toString().trim().split('\n').map(JSON.parse);
  assert.equal(frames.length, 6);
  for (const frame of frames) {
    assert.equal(frame.id, '🌿'.repeat(128));
    assert.equal(frame.result.structuredContent.items.length, 128);
    assert.deepEqual(JSON.parse(frame.result.content[0].text), frame.result.structuredContent);
  }
  assert.equal(frames[0].result.structuredContent.items.filter(r => r.available).length, 128);
  assert.equal(frames[1].result.structuredContent.items.filter(r => r.available).length, 0);
  assert.equal(frames[2].result.structuredContent.items.filter(r => r.available).length, 64);
});

test('exact 32768-byte frames are admitted', async t => {
  const {value, bytes} = transport(t);
  await value.send(exactFrame(32768));
  assert.equal(bytes().length, 32768);
  assert.equal(value.closed, false);
});

test('32769-byte frames are refused before emitting any part', async t => {
  const {value, bytes} = transport(t);
  await assert.rejects(value.send(exactFrame(32769)));
  assert.equal(bytes().length, 0);
  assert.equal((await value.done).reason, 'output_limit');
});

test('active plus waiting writes fill 64KiB and the next frame is refused', async t => {
  const input = new PassThrough();
  const observed = [];
  const output = new Writable({write(chunk, encoding, callback) { observed.push(Buffer.from(chunk)); }});
  const value = new BoundedStdioTransport({input, output});
  t.after(() => value.close());
  const pending = [value.send(exactFrame(32768)), value.send(exactFrame(32768))].map(p => p.then(() => 'sent', () => 'closed'));
  assert.equal(value.queuedBytes, 65536);
  await assert.rejects(value.send(exactFrame(128)));
  assert.deepEqual(await Promise.all(pending), ['closed', 'closed']);
  assert.equal((await value.done).reason, 'queue_limit');
  assert.equal(Buffer.concat(observed).length, 32768);
  assert.equal(input.destroyed && output.destroyed, true);
});

test('bounded profile still limits lifetime output to one MiB', async t => {
  const {value, bytes} = transport(t);
  for (let i = 0; i < 32; i++) await value.send(exactFrame(32768));
  await assert.rejects(value.send(exactFrame(128)));
  assert.equal(bytes().length, 1048576);
  assert.equal((await value.done).reason, 'output_limit');
});

test('parent-owned output renews only after conservative rolling expiry', async t => {
  let now = 1;
  const input = new PassThrough(), output = new PassThrough();
  let emitted = 0;
  output.on('data', b => { emitted += b.length; });
  const value = new BoundedStdioTransport({input, output, servingProfile: 'parent-owned', now: () => now});
  t.after(() => value.close());
  for (let i = 0; i < 32; i++) await value.send(exactFrame(32768));
  now = 60000 + Math.ceil(60000 / 64);
  await value.send(exactFrame(32768));
  assert.equal(emitted, 1048576 + 32768);
  assert.equal(value.closed, false);
  assert.ok(value.quota.peakBuckets <= 65);
});

test('queue-only overrides below the new frame cap require an explicit frame override', () => {
  assert.throws(() => boundedLimits({queuedOutputBytes: 24576}), /Invalid output capacity/);
  assert.doesNotThrow(() => boundedLimits({queuedOutputBytes: 24576, outputLineBytes: 16384}));
  assert.throws(() => boundedLimits({outputLineBytes: 32769}), /Invalid transport limits/);
});

test('a stalled larger write times out and settles its promise', async t => {
  const input = new PassThrough();
  const output = new Writable({write(chunk, encoding, callback) {}});
  const value = new BoundedStdioTransport({input, output, limits: {writeTimeoutMs: 20}});
  t.after(() => value.close());
  await assert.rejects(value.send(exactFrame(32768)));
  assert.equal((await value.done).reason, 'output_timeout');
  assert.equal(input.destroyed && output.destroyed, true);
});
