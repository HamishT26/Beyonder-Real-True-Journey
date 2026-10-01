import { createHash } from 'node:crypto';
import { TextDecoder } from 'node:util';

export const SCHEMA = 'nexus.evidence/v1';
export const POLICY_VERSION = 'nexus.sanitized-json/v1';
export const STATES = Object.freeze({
  RECEIVED: 'received', HASH_VERIFIED: 'hash-verified',
  SCHEMA_VALIDATED: 'schema-validated', HUMAN_ACCEPTED: 'human-accepted',
});
export const LIMITS = Object.freeze({
  capsuleBytes: 524288, payloadBytes: 65536, depth: 16, nodes: 10000,
  observations: 128, lifetimeMs: 86400000,
});
const BINDINGS = Object.freeze([
  'sourceRepository', 'sourceCommit', 'artifactPath', 'sha256', 'byteLength',
  'purpose', 'schema', 'policyVersion',
]);
const MANIFEST_FIELDS = [...BINDINGS, 'issuedAt', 'expiresAt'];
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });
const SESSION_TOKEN = Symbol('capsule-session');

export class CapsuleError extends Error {
  constructor(code, stage, field) {
    super(code);
    this.name = 'CapsuleError';
    this.code = code;
    this.stage = stage;
    if (field !== undefined) this.field = field;
  }
}
function fail(code, stage = STATES.RECEIVED, field) {
  throw new CapsuleError(code, stage, field);
}
function unicode(text, stage) {
  for (let i = 0; i < text.length; i++) {
    const unit = text.charCodeAt(i);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      const next = text.charCodeAt(++i);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail('INVALID_UNICODE', stage);
    } else if (unit >= 0xdc00 && unit <= 0xdfff) fail('INVALID_UNICODE', stage);
  }
}
function keyAllowed(key, stage) {
  const normalized = key.replace(/[^a-z0-9]/gi, '').toLowerCase();
  if (['__proto__', 'prototype', 'constructor'].includes(key)) {
    fail('FORBIDDEN_KEY', stage);
  }
  if (/secret|password|passwd|credential|authorization|authentication|apikey|token|privatekey|signingkey|cookie|sessionid/.test(normalized) || normalized === 'pwd') {
    fail('SECRET_KEY', stage);
  }
}

// Scan before JSON.parse: native parsing alone silently accepts duplicate keys.
// Decoded keys are checked, so escape aliases cannot bypass this check.
function parseStrict(text, stage) {
  let cursor = 0;
  let nodes = 0;
  function white() {
    while (/[\x20\t\r\n]/.test(text[cursor] ?? '') && cursor < text.length) cursor++;
  }
  function string() {
    const start = cursor++;
    while (cursor < text.length) {
      const char = text[cursor++];
      if (char === '\\') cursor++;
      else if (char === '"') {
        let value;
        try { value = JSON.parse(text.slice(start, cursor)); }
        catch { fail('INVALID_JSON', stage); }
        unicode(value, stage);
        return value;
      }
    }
    fail('INVALID_JSON', stage);
  }
  function value(depth) {
    if (depth > LIMITS.depth || ++nodes > LIMITS.nodes) fail('JSON_LIMIT', stage);
    white();
    const char = text[cursor];
    if (char === '"') { string(); return; }
    if (char === '{' || char === '[') {
      const object = char === '{';
      const end = object ? '}' : ']';
      const seen = new Set();
      cursor++;
      white();
      if (text[cursor] === end) { cursor++; return; }
      while (cursor < text.length) {
        if (object) {
          if (text[cursor] !== '"') fail('INVALID_JSON', stage);
          const key = string();
          keyAllowed(key, stage);
          if (seen.has(key)) fail('DUPLICATE_KEY', stage);
          seen.add(key);
          white();
          if (text[cursor++] !== ':') fail('INVALID_JSON', stage);
        }
        value(depth + 1);
        white();
        const separator = text[cursor++];
        if (separator === end) return;
        if (separator !== ',') fail('INVALID_JSON', stage);
        white();
      }
      fail('INVALID_JSON', stage);
    }
    const match = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(text.slice(cursor));
    if (!match) fail('INVALID_JSON', stage);
    if (/^-?\d/.test(match[0]) && !Number.isFinite(Number(match[0]))) {
      fail('NON_FINITE_NUMBER', stage);
    }
    cursor += match[0].length;
  }
  value(0);
  white();
  if (cursor !== text.length) fail('INVALID_JSON', stage);
  try { return JSON.parse(text); }
  catch { fail('INVALID_JSON', stage); }
}
function exactFields(record, fields, stage) {
  if (record === null || typeof record !== 'object' || Array.isArray(record)) {
    fail('FIELD_SET', stage);
  }
  const proto = Object.getPrototypeOf(record);
  if (proto !== Object.prototype && proto !== null) fail('FIELD_SET', stage);
  const keys = Reflect.ownKeys(record);
  for (const key of keys) {
    if (typeof key !== 'string') fail('FIELD_SET', stage);
    keyAllowed(key, stage);
    if (!Object.hasOwn(Object.getOwnPropertyDescriptor(record, key), 'value')) {
      fail('FIELD_SET', stage);
    }
  }
  if (keys.length !== fields.length || fields.some(key => !Object.hasOwn(record, key))) {
    fail('FIELD_SET', stage);
  }
}
function safeText(text, max, stage) {
  if (typeof text !== 'string' || text.length === 0 || text.length > max ||
      /[\x00-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]/.test(text)) {
    fail('INVALID_TEXT', stage);
  }
  unicode(text, stage);
}
function safePath(path, stage) {
  if (typeof path !== 'string' || path.length === 0 || path.length > 1024) {
    fail('UNSAFE_PATH', stage);
  }
  for (const part of path.split('/')) {
    if (!/^[A-Za-z0-9._-]{1,255}$/.test(part) || part === '.' || part === '..' ||
        part.endsWith('.') || /^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(part)) {
      fail('UNSAFE_PATH', stage);
    }
  }
}
function bindingShape(record, fields, stage) {
  exactFields(record, fields, stage);
  safeText(record.sourceRepository, 1024, stage);
  let repository;
  try { repository = new URL(record.sourceRepository); }
  catch { fail('INVALID_REPOSITORY', stage); }
  if (repository.protocol !== 'https:' || !repository.hostname || repository.username ||
      repository.password || repository.search || repository.hash || repository.port ||
      repository.href !== record.sourceRepository) fail('INVALID_REPOSITORY', stage);
  if (typeof record.sourceCommit !== 'string' || !/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(record.sourceCommit)) {
    fail('INVALID_COMMIT', stage);
  }
  safePath(record.artifactPath, stage);
  if (typeof record.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(record.sha256)) fail('INVALID_HASH', stage);
  if (!Number.isSafeInteger(record.byteLength) || record.byteLength < 1 ||
      record.byteLength > LIMITS.payloadBytes) fail('INVALID_LENGTH', stage);
  if (typeof record.purpose !== 'string' || record.purpose.length > 128 ||
      !/^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$/.test(record.purpose)) fail('INVALID_PURPOSE', stage);
  if (record.purpose.replace(/[._-]/g, '').includes('secretlocal')) fail('SECRET_LOCAL_EXPORT', stage);
  safeText(record.schema, 128, stage);
  safeText(record.policyVersion, 128, stage);
}
function timestamp(value, stage) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)) {
    fail('INVALID_TIMESTAMP', stage);
  }
  const ms = Date.parse(value);
  if (!Number.isFinite(ms) || new Date(ms).toISOString() !== value) fail('INVALID_TIMESTAMP', stage);
  return ms;
}
function fresh(manifest, clock, stage) {
  const now = clock(); // This callback belongs to the consumer, never to a capsule.
  if (!Number.isSafeInteger(now) || now < 0 || now > 8640000000000000) fail('INVALID_CLOCK', stage);
  const issued = timestamp(manifest.issuedAt, stage);
  const expires = timestamp(manifest.expiresAt, stage);
  if (expires <= issued || expires - issued > LIMITS.lifetimeMs) fail('INVALID_LIFETIME', stage);
  if (issued > now) fail('FUTURE_TIMESTAMP', stage);
  if (expires <= now) fail('EXPIRED', stage);
  return now;
}
function freezeTree(value) {
  if (value !== null && typeof value === 'object') {
    for (const child of Object.values(value)) freezeTree(child);
    Object.freeze(value);
  }
  return value;
}
function decodeInput(input) {
  if (typeof input === 'string') {
    if (input.length > LIMITS.capsuleBytes) fail('TRANSPORT_LIMIT');
    unicode(input, STATES.RECEIVED);
    if (Buffer.byteLength(input, 'utf8') > LIMITS.capsuleBytes) fail('TRANSPORT_LIMIT');
    return input;
  }
  if (!Buffer.isBuffer(input) && !(input instanceof Uint8Array)) fail('INVALID_TRANSPORT');
  if (input.byteLength > LIMITS.capsuleBytes) fail('TRANSPORT_LIMIT');
  try { return decoder.decode(input); }
  catch { fail('INVALID_UTF8'); }
}
function validateEvidence(text, manifest, stage) {
  const evidence = parseStrict(text, stage);
  exactFields(evidence, ['schema', 'purpose', 'issuedAt', 'expiresAt', 'observations'], stage);
  if (evidence.schema !== manifest.schema || evidence.purpose !== manifest.purpose ||
      evidence.issuedAt !== manifest.issuedAt || evidence.expiresAt !== manifest.expiresAt) {
    fail('PAYLOAD_BINDING_MISMATCH', stage);
  }
  const records = evidence.observations;
  if (!Array.isArray(records) || records.length === 0 || records.length > LIMITS.observations) {
    fail('INVALID_OBSERVATIONS', stage);
  }
  const ids = new Set();
  for (const record of records) {
    exactFields(record, ['id', 'status', 'summary'], stage);
    if (typeof record.id !== 'string' || !/^[a-z][a-z0-9-]{0,63}$/.test(record.id) || ids.has(record.id)) {
      fail('INVALID_OBSERVATION_ID', stage);
    }
    ids.add(record.id);
    if (!['pass', 'fail', 'info'].includes(record.status)) fail('INVALID_STATUS', stage);
    safeText(record.summary, 512, stage);
  }
  return freezeTree(evidence);
}

class CapsuleSession {
  #state = STATES.RECEIVED;
  #history = [STATES.RECEIVED];
  #manifest; #text; #clock; #evidence; #acceptance = null;
  constructor(token, manifest, text, clock) {
    if (token !== SESSION_TOKEN) fail('INVALID_SESSION');
    this.#manifest = freezeTree(manifest);
    this.#text = text;
    this.#clock = clock;
    Object.freeze(this);
  }
  get state() { return this.#state; }
  get history() { return Object.freeze([...this.#history]); }
  get manifest() { return this.#manifest; }
  get acceptance() { return this.#acceptance; }
  get evidence() {
    if (![STATES.SCHEMA_VALIDATED, STATES.HUMAN_ACCEPTED].includes(this.#state)) {
      fail('WRONG_STATE', this.#state);
    }
    fresh(this.#manifest, this.#clock, this.#state);
    return this.#evidence;
  }
  #require(state) {
    if (this.#state !== state) fail('WRONG_STATE', this.#state);
    return fresh(this.#manifest, this.#clock, this.#state);
  }
  #advance(state) {
    const now = fresh(this.#manifest, this.#clock, this.#state);
    this.#state = state;
    this.#history.push(state);
    return now;
  }
  verifyHash() {
    this.#require(STATES.RECEIVED);
    if (Buffer.byteLength(this.#text, 'utf8') !== this.#manifest.byteLength) {
      fail('BYTE_LENGTH_MISMATCH', this.#state);
    }
    if (createHash('sha256').update(this.#text, 'utf8').digest('hex') !== this.#manifest.sha256) {
      fail('HASH_MISMATCH', this.#state);
    }
    this.#advance(STATES.HASH_VERIFIED);
    return this;
  }
  validateSchema() {
    this.#require(STATES.HASH_VERIFIED);
    this.#evidence = validateEvidence(this.#text, this.#manifest, this.#state);
    this.#advance(STATES.SCHEMA_VALIDATED);
    return this;
  }
  acceptHuman(confirmation) {
    this.#require(STATES.SCHEMA_VALIDATED);
    exactFields(confirmation, ['decision', 'note'], this.#state);
    if (confirmation.decision !== 'accept') fail('HUMAN_DECISION_REQUIRED', this.#state);
    safeText(confirmation.note, 512, this.#state);
    const now = this.#advance(STATES.HUMAN_ACCEPTED);
    this.#acceptance = Object.freeze({
      decision: 'accept', note: confirmation.note, acceptedAt: new Date(now).toISOString(),
    });
    return this;
  }
}

// Expectation and clock must be locally held; never derive them from received data.
export function receiveCapsule(input, expectation, options = {}) {
  const stage = STATES.RECEIVED;
  if (expectation === undefined || expectation === null) fail('UNKNOWN_EXPECTATION', stage);
  bindingShape(expectation, BINDINGS, stage);
  const expected = Object.freeze(Object.fromEntries(BINDINGS.map(key => [key, expectation[key]])));
  if (options === null || typeof options !== 'object' || Array.isArray(options)) fail('INVALID_OPTIONS', stage);
  if (Object.getPrototypeOf(options) !== Object.prototype && Object.getPrototypeOf(options) !== null) {
    fail('INVALID_OPTIONS', stage);
  }
  const optionKeys = Reflect.ownKeys(options);
  if (optionKeys.some(key => !Object.hasOwn(Object.getOwnPropertyDescriptor(options, key), 'value'))) {
    fail('INVALID_OPTIONS', stage);
  }
  if (optionKeys.some(key => key !== 'clock') || (options.clock !== undefined && typeof options.clock !== 'function')) {
    fail('INVALID_OPTIONS', stage);
  }
  const clock = options.clock ?? Date.now;
  const capsule = parseStrict(decodeInput(input), stage);
  exactFields(capsule, ['manifest', 'payloadUtf8'], stage);
  bindingShape(capsule.manifest, MANIFEST_FIELDS, stage);
  for (const key of BINDINGS) {
    if (capsule.manifest[key] !== expected[key]) fail('EXPECTATION_MISMATCH', stage, key);
  }
  if (capsule.manifest.schema !== SCHEMA) fail('UNSUPPORTED_SCHEMA', stage);
  if (capsule.manifest.policyVersion !== POLICY_VERSION) fail('UNSUPPORTED_POLICY', stage);
  if (typeof capsule.payloadUtf8 !== 'string') fail('INVALID_PAYLOAD', stage);
  if (Buffer.byteLength(capsule.payloadUtf8, 'utf8') > LIMITS.payloadBytes) fail('PAYLOAD_LIMIT', stage);
  fresh(capsule.manifest, clock, stage);
  return new CapsuleSession(SESSION_TOKEN, capsule.manifest, capsule.payloadUtf8, clock);
}
