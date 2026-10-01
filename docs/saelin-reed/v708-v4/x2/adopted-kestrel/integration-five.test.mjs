import { after, test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { CapsuleError, receiveCapsule } from './capsule-verifier.mjs';

// Exact public fixture: UTF-8, 429 bytes, including final LF. No wall-clock expiry.
const payloadUtf8 = `{
  "schema": "nexus.evidence/v1",
  "purpose": "nexus.sanitized-evidence",
  "issuedAt": "2026-10-01T00:00:00.000Z",
  "expiresAt": "2026-10-02T00:00:00.000Z",
  "observations": [
    {
      "id": "utf8-fixture",
      "status": "pass",
      "summary": "UTF-8 evidence: café, λ and 🌿."
    },
    {
      "id": "trust-limit",
      "status": "info",
      "summary": "A valid hash proves byte identity only."
    }
  ]
}
`;
const sha = text => createHash('sha256').update(text, 'utf8').digest('hex');
const expectation = Object.freeze({
  sourceRepository: 'https://example.org/nexus/demo.git',
  sourceCommit: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  artifactPath: 'evidence/sanitized.json',
  sha256: '81ece98c880cc8dce16f116c64b7260b0f96a831be0433c800454f697f9402b2',
  byteLength: 429, purpose: 'nexus.sanitized-evidence', schema: 'nexus.evidence/v1',
  policyVersion: 'nexus.sanitized-json/v1',
});
const times = Object.freeze({ issuedAt: '2026-10-01T00:00:00.000Z', expiresAt: '2026-10-02T00:00:00.000Z' });
const clock = () => Date.parse('2026-10-01T00:30:00.000Z');
const raw = JSON.stringify({ manifest: { ...expectation, ...times }, payloadUtf8 });
const effects = [];
function observe(id, input, expected, steps, code, stage, claimedState = null) {
  let session;
  let error;
  try {
    session = receiveCapsule(input, expected, { clock });
    for (const step of steps) session[step]();
  } catch (caught) { error = caught; }
  // Capture actual effects before assertions; incoming labels never become results.
  const effect = {
    id, errorCode: error instanceof CapsuleError ? error.code : error ? 'UNEXPECTED_ERROR' : null,
    errorStage: error?.stage ?? null, observedState: session?.state ?? null,
    history: session?.history ?? [], humanAccepted: session?.acceptance !== null && session !== undefined,
    claimedState, executedIncoming: Object.hasOwn(globalThis, '__kestrelIntegrationExecuted'),
  };
  effects.push(effect);
  assert.ok(error instanceof CapsuleError);
  assert.equal(effect.errorCode, code);
  assert.equal(effect.errorStage, stage);
  assert.equal(effect.observedState, session ? stage : null);
  assert.equal(effect.humanAccepted, false);
  assert.equal(effect.executedIncoming, false);
  return effect;
}

test('1: same raw bytes under a wrong source are rejected', () => {
  assert.equal(sha(payloadUtf8), expectation.sha256);
  assert.equal(Buffer.byteLength(payloadUtf8, 'utf8'), expectation.byteLength);
  observe('same-bytes-wrong-source', raw,
    { ...expectation, sourceRepository: 'https://example.org/nexus/other.git' },
    [], 'EXPECTATION_MISMATCH', 'received');
});
test('2: absent or unknown consumer expectation is rejected', () => {
  observe('unknown-expectation-undefined', raw, undefined, [], 'UNKNOWN_EXPECTATION', 'received');
  observe('unknown-expectation-null', raw, null, [], 'UNKNOWN_EXPECTATION', 'received');
});
test('3: secret-local export fails even with matching bytes and expectation', () => {
  const evidence = { ...JSON.parse(payloadUtf8), purpose: 'secret-local' };
  const text = JSON.stringify(evidence);
  const expected = { ...expectation, purpose: evidence.purpose, sha256: sha(text), byteLength: Buffer.byteLength(text, 'utf8') };
  const input = JSON.stringify({ manifest: { ...expected, ...times }, payloadUtf8: text });
  assert.equal(sha(JSON.parse(input).payloadUtf8), expected.sha256);
  observe('secret-local-export', input, expected, [], 'SECRET_LOCAL_EXPORT', 'received');
});
test('4: stale and extra-field capsules are rejected', () => {
  const stale = JSON.stringify({ manifest: { ...expectation, ...times, expiresAt: '2026-10-01T00:20:00.000Z' }, payloadUtf8 });
  observe('stale-capsule', stale, expectation, [], 'EXPIRED', 'received');
  const extra = JSON.stringify({ ...JSON.parse(raw), extra: true });
  observe('extra-field-capsule', extra, expectation, [], 'FIELD_SET', 'received');
});
test('5: observed effects outrank returned labels; incoming code stays inert', () => {
  assert.equal(Object.hasOwn(globalThis, '__kestrelIntegrationExecuted'), false);
  const evidence = JSON.parse(payloadUtf8);
  evidence.humanAccepted = true;
  evidence.observations[0].summary = 'globalThis.__kestrelIntegrationExecuted = true;';
  const text = JSON.stringify(evidence);
  const expected = { ...expectation, sha256: sha(text), byteLength: Buffer.byteLength(text, 'utf8') };
  const input = JSON.stringify({ manifest: { ...expected, ...times }, payloadUtf8: text });
  const effect = observe('claimed-accepted-vs-observed', input, expected,
    ['verifyHash', 'validateSchema'], 'FIELD_SET', 'hash-verified', 'human-accepted');
  assert.notEqual(effect.observedState, effect.claimedState);
  assert.deepEqual(effect.history, ['received', 'hash-verified']);
});
after(() => writeFileSync(new URL('./integration-effects.json', import.meta.url), JSON.stringify({
  scope: 'Cloud-side source checks only; no reproduction of the coordinator root implementation.',
  clockUtc: '2026-10-01T00:30:00.000Z', fixtureSha256: expectation.sha256,
  fixtureByteLength: expectation.byteLength, effects,
}, null, 2) + '\n', 'utf8'));
