import * as fs from 'node:fs';
import path from 'node:path';
import { createHash, randomBytes } from 'node:crypto';
import { TextDecoder } from 'node:util';
import { parseJsonWithUniqueNames } from './json-name-guard.mjs';

export const FORMATS = Object.freeze({
  record: 'saelin-local-evidence-record/v1',
  bundle: 'saelin-local-evidence-bundle/v1',
  promotion: 'saelin-local-evidence-promotion/v1',
});
export const CLASSIFICATIONS = Object.freeze(['public-evidence', 'private-memory', 'secret-local']);
const DESTINATIONS = ['github', 'private-cloud'];
const HASH = /^[a-f0-9]{64}$/;
const ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;
const DEVICE = /^(?:con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\.|$)/i;
const utf8 = new TextDecoder('utf-8', { fatal: true });
const secretKey = /(?:password|passwd|secret|apikey|token|authorization|credential|privatekey|awsaccesskey)|^pwd$/i;
const tokenPatterns = [
  /\bgh[pousr]_[A-Za-z0-9]{20,}\b/,
  /\bgithub_pat_[A-Za-z0-9_]{20,}\b/,
  /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b/,
  /\b(?:AKIA|ASIA)[A-Z0-9]{16}\b/,
  /\bxox[baprs]-[A-Za-z0-9-]{12,}\b/,
  /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b/,
  /-----BEGIN (?:[A-Z0-9 ]* )?PRIVATE KEY-----/,
  /\bBearer\s+[A-Za-z0-9._~+/-]{12,}/i,
  /\bAIza[A-Za-z0-9_-]{30,}\b/,
  /\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b/,
  /\bnpm_[A-Za-z0-9]{20,}\b/,
  /\bglpat-[A-Za-z0-9_-]{16,}\b/,
  /\bpypi-[A-Za-z0-9_-]{20,}\b/,
  /\bya29\.[A-Za-z0-9_-]{16,}\b/,
];
const assignmentPattern = /(?:^|[\s"'`{;,])[A-Za-z0-9_.-]*(?:api[_-]?key|password|passwd|pwd|secret|credential|token|authorization|private[_-]?key)[A-Za-z0-9_.-]*["'` ]*\s*[:=]/im;

export class AdapterError extends Error {
  constructor(code) {
    super(code);
    this.name = 'AdapterError';
    this.code = code;
  }
}
const fail = (code) => { throw new AdapterError(code); };
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

function shape(value, keys, code = 'INVALID_SHAPE') {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(code);
  const proto = Object.getPrototypeOf(value);
  if (proto !== Object.prototype && proto !== null) fail(code);
  const actual = Reflect.ownKeys(value);
  if (actual.length !== keys.length || actual.some(key => typeof key !== 'string' || !keys.includes(key))) fail(code);
  if (actual.some(key => !Object.getOwnPropertyDescriptor(value, key)?.hasOwnProperty('value'))) fail(code);
}

function canonical(value, depth = 0, budget = { nodes: 0 }) {
  if (++budget.nodes > 20000 || depth > 64) fail('STRUCTURE_LIMIT');
  if (value === null || typeof value === 'boolean' || typeof value === 'string') return JSON.stringify(value);
  if (typeof value === 'number' && Number.isFinite(value)) return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(item => canonical(item, depth + 1, budget)).join(',')}]`;
  if (value && typeof value === 'object') {
    const proto = Object.getPrototypeOf(value);
    if (proto !== Object.prototype && proto !== null) fail('INVALID_JSON');
    return `{${Object.keys(value).sort().map(key => {
      if (!Object.getOwnPropertyDescriptor(value, key)?.hasOwnProperty('value')) fail('INVALID_JSON');
      return `${JSON.stringify(key)}:${canonical(value[key], depth + 1, budget)}`;
    }).join(',')}}`;
  }
  fail('INVALID_JSON');
}
const jsonBytes = (value) => Buffer.from(canonical(value), 'utf8');

function identifier(value) {
  if (typeof value !== 'string' || !ID.test(value)) fail('INVALID_IDENTIFIER');
  checkText(value);
  return value;
}
function hash(value) { if (typeof value !== 'string' || !HASH.test(value)) fail('INVALID_HASH'); }
function classification(value, payload = false) {
  if (!CLASSIFICATIONS.includes(value)) fail('INVALID_CLASSIFICATION');
  if (payload && value === 'secret-local') fail('SECRET_PAYLOAD_UNAVAILABLE');
}
function destination(value) { if (!DESTINATIONS.includes(value)) fail('INVALID_DESTINATION'); }

export function validateLogicalPath(value) {
  if (typeof value !== 'string' || value.length < 1 || value.length > 512 || path.posix.isAbsolute(value) || path.win32.isAbsolute(value)) fail('UNSAFE_PATH');
  const segments = value.split('/');
  if (segments.length > 32 || segments.some(segment => !/^[A-Za-z0-9._-]{1,100}$/.test(segment) || segment === '.' || segment === '..' || /[. ]$/.test(segment) || DEVICE.test(segment))) fail('UNSAFE_PATH');
  return value;
}

function payloadPath(value) {
  validateLogicalPath(value);
  if (!/\.(?:json|md|txt)$/i.test(value)) fail('UNSUPPORTED_PAYLOAD');
  if (value.split('/').some(segment => /^(?:\.env(?:\.|$)|id_(?:rsa|dsa|ecdsa|ed25519)(?:\.|$))|(?:credential|password|secret|token)/i.test(segment))) fail('SENSITIVE_PATH');
}

function checkText(value) {
  if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(value) || tokenPatterns.some(pattern => pattern.test(value)) || assignmentPattern.test(value)) fail('SENSITIVE_PAYLOAD');
}

function checkTree(value, depth = 0, budget = { nodes: 0 }) {
  if (++budget.nodes > 20000 || depth > 64) fail('STRUCTURE_LIMIT');
  if (typeof value === 'string') return checkText(value);
  if (Array.isArray(value)) return value.forEach(item => checkTree(item, depth + 1, budget));
  if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) {
      const normalized = key.replace(/[\s_.-]/g, '');
      if (secretKey.test(normalized) || ['__proto__', 'prototype', 'constructor'].includes(key)) fail('SENSITIVE_KEY');
      checkText(key);
      checkTree(item, depth + 1, budget);
    }
  }
}

function sanitizedPayload(bytes, ...names) {
  names.forEach(payloadPath);
  let text;
  try { text = utf8.decode(bytes); } catch { fail('INVALID_UTF8'); }
  checkText(text);
  let parsed;
  try { parsed = parseJsonWithUniqueNames(text); }
  catch (error) {
    if (error.code === 'DUPLICATE_JSON_NAME' || error.code === 'STRUCTURE_LIMIT') fail(error.code);
    if (names.some(name => /\.json$/i.test(name))) fail('INVALID_JSON');
    return;
  }
  checkTree(parsed);
}

function sourceBinding(value) {
  shape(value, ['sourceId', 'version', 'path', 'sha256', 'bytes'], 'INCOMPLETE_SOURCE_BINDING');
  identifier(value.sourceId);
  identifier(value.version);
  payloadPath(value.path);
  hash(value.sha256);
  if (!Number.isSafeInteger(value.bytes) || value.bytes < 0) fail('INCOMPLETE_SOURCE_BINDING');
  checkTree(value);
}

function recordIdFor(record) {
  const { recordId, ...core } = record;
  return sha256(jsonBytes(core));
}

function validateRecord(record, { allowSecret = false, maxPayloadBytes }) {
  if (!record || typeof record !== 'object') fail('INVALID_RECORD');
  classification(record.classification, !allowSecret);
  if (record.classification === 'secret-local') {
    shape(record, ['format', 'classification', 'logicalPath', 'reference', 'sanitized', 'recordId']);
    shape(record.reference, ['referenceId', 'sourceId', 'version', 'kind', 'purpose']);
    ['referenceId', 'sourceId', 'version', 'kind'].forEach(key => identifier(record.reference[key]));
    if (typeof record.reference.purpose !== 'string' || record.reference.purpose.length > 512) fail('INVALID_REFERENCE');
    validateLogicalPath(record.logicalPath);
  } else {
    shape(record, ['format', 'classification', 'logicalPath', 'source', 'payload', 'sanitized', 'recordId']);
    sourceBinding(record.source);
    payloadPath(record.logicalPath);
    shape(record.payload, ['sha256', 'bytes']);
    hash(record.payload.sha256);
    if (record.payload.sha256 !== record.source.sha256 || record.payload.bytes !== record.source.bytes) fail('SOURCE_BINDING_MISMATCH');
    if (record.payload.bytes > maxPayloadBytes) fail('PAYLOAD_TOO_LARGE');
  }
  if (record.format !== FORMATS.record || record.sanitized !== true) fail('INVALID_RECORD');
  hash(record.recordId);
  checkTree(record);
  if (recordIdFor(record) !== record.recordId) fail('RECORD_DIGEST_MISMATCH');
  return record;
}

export function bindingFor(record) {
  classification(record?.classification, true);
  return JSON.parse(canonical({ recordId: record.recordId, classification: record.classification, logicalPath: record.logicalPath, source: record.source }));
}

function verifyExpected(records, expectedSources) {
  if (!Array.isArray(expectedSources) || expectedSources.length !== records.length || !expectedSources.length) fail('INCOMPLETE_SOURCE_BINDING');
  const expected = new Map();
  for (const entry of expectedSources) {
    shape(entry, ['recordId', 'classification', 'logicalPath', 'source'], 'INCOMPLETE_SOURCE_BINDING');
    hash(entry.recordId);
    classification(entry.classification, true);
    payloadPath(entry.logicalPath);
    sourceBinding(entry.source);
    if (expected.has(entry.recordId)) fail('DUPLICATE_RECORD');
    expected.set(entry.recordId, entry);
  }
  for (const record of records) {
    const entry = expected.get(record.recordId);
    if (!entry || canonical(bindingFor(record)) !== canonical(entry)) fail('SOURCE_BINDING_MISMATCH');
  }
}

function normalizedAbsolute(value) {
  let result = path.resolve(value);
  if (process.platform === 'win32') result = result.replace(/^\\\\\?\\/, '').toLowerCase();
  return result;
}
function contains(root, candidate) {
  const relative = path.relative(normalizedAbsolute(root), normalizedAbsolute(candidate));
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}
function disjoint(left, right) { if (contains(left, right) || contains(right, left)) fail('ROOT_OVERLAP'); }
function absoluteRoot(value) {
  if (typeof value !== 'string' || !path.isAbsolute(value) || value.includes('\0') || /^[/\\]{2}/.test(value)) fail('INVALID_ROOT');
  return path.resolve(value);
}

// Check every ancestor, including ancestors above the caller's chosen root.
// realpath equality complements lstat's symlink/junction detection.
function inspectAbsolute(target, allowMissing = false) {
  const parsed = path.parse(target);
  const segments = path.relative(parsed.root, target).split(path.sep).filter(Boolean);
  let current = parsed.root;
  for (let i = -1; i < segments.length; i++) {
    if (i >= 0) current = path.join(current, segments[i]);
    let stat;
    try { stat = fs.lstatSync(current); }
    catch (error) { if (error.code === 'ENOENT' && allowMissing) return null; fail(error.code === 'ENOENT' ? 'PATH_MISSING' : 'PATH_ACCESS'); }
    if (stat.isSymbolicLink()) fail('LINK_REJECTED');
    let actual;
    try { actual = fs.realpathSync.native(current); } catch { fail('PATH_ACCESS'); }
    if (normalizedAbsolute(actual) !== normalizedAbsolute(current)) fail('REPARSE_ESCAPE');
    if (i < segments.length - 1 && !stat.isDirectory()) fail('PATH_TYPE');
    if (i === segments.length - 1) return stat;
  }
  return fs.lstatSync(parsed.root);
}

function directory(target, create = false) {
  // A complete inspection already visits every ancestor. For an existing
  // directory, avoid repeating that same full walk for each prefix.
  const present = inspectAbsolute(target, true);
  if (present) {
    if (!present.isDirectory()) fail('PATH_TYPE');
    return;
  }
  if (!create) fail('PATH_MISSING');
  const parsed = path.parse(target);
  let current = parsed.root;
  if (!inspectAbsolute(current)?.isDirectory()) fail('PATH_TYPE');
  for (const segment of path.relative(parsed.root, target).split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    let stat = inspectAbsolute(current, true);
    if (!stat) {
      if (!create) fail('PATH_MISSING');
      inspectAbsolute(path.dirname(current));
      try { fs.mkdirSync(current, { mode: 0o700 }); }
      catch (error) { if (error.code !== 'EEXIST') fail('WRITE_FAILED'); }
      stat = inspectAbsolute(current);
    }
    if (!stat.isDirectory()) fail('PATH_TYPE');
  }
}

function containedPath(root, logicalPath) {
  validateLogicalPath(logicalPath);
  const target = path.join(root, ...logicalPath.split('/'));
  if (!contains(root, target) || normalizedAbsolute(root) === normalizedAbsolute(target)) fail('UNSAFE_PATH');
  return target;
}

function sameFile(a, b) {
  return a.dev === b.dev && a.ino === b.ino && a.size === b.size && a.mtimeMs === b.mtimeMs && a.ctimeMs === b.ctimeMs;
}

function safeRead(root, logicalPath, limit) {
  directory(root);
  const target = containedPath(root, logicalPath);
  const before = inspectAbsolute(target);
  if (!before.isFile()) fail('PATH_TYPE');
  if (before.nlink !== 1) fail('HARDLINK_REJECTED');
  if (!Number.isSafeInteger(before.size) || before.size > limit) fail('PAYLOAD_TOO_LARGE');
  let fd;
  try { fd = fs.openSync(target, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW ?? 0)); }
  catch { fail('PATH_ACCESS'); }
  try {
    const opened = fs.fstatSync(fd);
    if (!sameFile(before, opened) || opened.nlink !== 1 || !opened.isFile()) fail('SOURCE_CHANGED');
    const bytes = Buffer.alloc(opened.size);
    let offset = 0;
    while (offset < bytes.length) {
      const read = fs.readSync(fd, bytes, offset, bytes.length - offset, offset);
      if (read === 0) fail('SOURCE_CHANGED');
      offset += read;
    }
    if (fs.readSync(fd, Buffer.alloc(1), 0, 1, offset) !== 0) fail('SOURCE_CHANGED');
    const after = fs.fstatSync(fd);
    const pathAfter = inspectAbsolute(target);
    if (!sameFile(opened, after) || !sameFile(after, pathAfter) || after.nlink !== 1) fail('SOURCE_CHANGED');
    return bytes;
  } finally { fs.closeSync(fd); }
}

function syncDirectory(target) {
  let fd;
  try { fd = fs.openSync(target, 'r'); fs.fsyncSync(fd); }
  catch (error) { if (!['EPERM', 'EISDIR', 'EINVAL', 'ENOTSUP', 'EBADF', 'EACCES'].includes(error.code)) fail('SYNC_FAILED'); }
  finally { if (fd !== undefined) fs.closeSync(fd); }
}

// Publish through an exclusive hard link. rename() can overwrite an existing
// destination on supported platforms and is intentionally not used here.
function immutableWrite(root, logicalPath, bytes, { allowIdentical = true } = {}) {
  directory(root);
  const target = containedPath(root, logicalPath);
  directory(path.dirname(target), true);
  if (inspectAbsolute(target, true)) {
    if (!allowIdentical) fail('DESTINATION_EXISTS');
    let existing;
    try { existing = safeRead(root, logicalPath, bytes.length); }
    catch (error) { if (error.code === 'PAYLOAD_TOO_LARGE') fail('HASH_COLLISION'); throw error; }
    if (!existing.equals(bytes)) fail('HASH_COLLISION');
    return;
  }
  const relativeParent = path.posix.dirname(logicalPath);
  const temporaryName = `.stage-${randomBytes(16).toString('hex')}.tmp`;
  const temporaryLogical = relativeParent === '.' ? temporaryName : `${relativeParent}/${temporaryName}`;
  const temporary = containedPath(root, temporaryLogical);
  let fd;
  let created = false;
  try {
    directory(path.dirname(target));
    fd = fs.openSync(temporary, 'wx', 0o600);
    created = true;
    fs.writeFileSync(fd, bytes);
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = undefined;
    directory(path.dirname(target));
    inspectAbsolute(temporary);
    try { fs.linkSync(temporary, target); }
    catch (error) {
      if (error.code !== 'EEXIST') fail('ATOMIC_PUBLISH_FAILED');
      if (!allowIdentical) fail('DESTINATION_EXISTS');
      const existing = safeRead(root, logicalPath, bytes.length);
      if (!existing.equals(bytes)) fail('HASH_COLLISION');
    }
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
    if (created) {
      directory(path.dirname(temporary));
      const stat = inspectAbsolute(temporary);
      if (!stat.isFile()) fail('PATH_TYPE');
      fs.unlinkSync(temporary); // Only this call's exact, random staging file.
    }
  }
  syncDirectory(path.dirname(target));
  if (!safeRead(root, logicalPath, bytes.length).equals(bytes)) fail('WRITE_VERIFICATION_FAILED');
}

function parse(bytes) {
  let value;
  try { value = parseJsonWithUniqueNames(utf8.decode(bytes)); }
  catch (error) {
    if (error.code === 'DUPLICATE_JSON_NAME' || error.code === 'STRUCTURE_LIMIT') fail(error.code);
    fail('INVALID_JSON');
  }
  canonical(value); // Apply depth/node limits before deeper schema work.
  return value;
}

function uniqueLogicalPaths(records) {
  const names = records.map(record => record.logicalPath.toLowerCase());
  const selected = new Set(names);
  if (selected.size !== names.length) fail('LOGICAL_PATH_CONFLICT');
  for (const name of names) {
    const segments = name.split('/');
    for (let count = 1; count < segments.length; count++) {
      if (selected.has(segments.slice(0, count).join('/'))) fail('LOGICAL_PATH_CONFLICT');
    }
  }
}

class LocalEvidenceAdapter {
  constructor(options) {
    const permitted = ['storeRoot', 'allowedRoot', 'maxPayloadBytes', 'maxBundleBytes', 'maxRecords'];
    if (!options || Object.keys(options).some(key => !permitted.includes(key))) fail('INVALID_OPTIONS');
    this.storeRoot = absoluteRoot(options.storeRoot);
    this.allowedRoot = absoluteRoot(options.allowedRoot);
    this.maxPayloadBytes = options.maxPayloadBytes ?? 1024 * 1024;
    this.maxBundleBytes = options.maxBundleBytes ?? 16 * 1024 * 1024;
    this.maxRecords = options.maxRecords ?? 64;
    for (const [number, cap] of [[this.maxPayloadBytes, 16 * 1024 * 1024], [this.maxBundleBytes, 64 * 1024 * 1024], [this.maxRecords, 256]]) {
      if (!Number.isSafeInteger(number) || number < 1 || number > cap) fail('INVALID_LIMIT');
    }
    disjoint(this.storeRoot, this.allowedRoot);
    directory(this.allowedRoot);
    directory(this.storeRoot, true);
    for (const child of ['objects/public-evidence', 'objects/private-memory', ...CLASSIFICATIONS.map(name => `records/${name}`), 'prepared', 'quarantine', 'promotions']) {
      directory(containedPath(this.storeRoot, child), true);
    }
    Object.freeze(this);
  }

  ingest(request) {
    shape(request, ['sourcePath', 'logicalPath', 'classification', 'sanitized', 'expectedSource']);
    classification(request.classification, true);
    if (request.sanitized !== true) fail('SANITIZED_ATTESTATION_REQUIRED');
    payloadPath(request.sourcePath);
    payloadPath(request.logicalPath);
    sourceBinding(request.expectedSource);
    if (request.expectedSource.path !== request.sourcePath) fail('SOURCE_BINDING_MISMATCH');
    if (request.expectedSource.bytes > this.maxPayloadBytes) fail('PAYLOAD_TOO_LARGE');
    const bytes = safeRead(this.allowedRoot, request.sourcePath, this.maxPayloadBytes);
    if (sha256(bytes) !== request.expectedSource.sha256 || bytes.length !== request.expectedSource.bytes) fail('SOURCE_BINDING_MISMATCH');
    sanitizedPayload(bytes, request.sourcePath, request.logicalPath);
    const record = {
      format: FORMATS.record, classification: request.classification, logicalPath: request.logicalPath,
      source: JSON.parse(canonical(request.expectedSource)), payload: { sha256: sha256(bytes), bytes: bytes.length }, sanitized: true,
    };
    record.recordId = recordIdFor(record);
    validateRecord(record, this);
    this.#persist(record, bytes);
    return JSON.parse(canonical(record));
  }

  recordSecretReference(request) {
    shape(request, ['referenceId', 'sourceId', 'version', 'kind', 'purpose', 'logicalPath', 'sanitized']);
    if (request.sanitized !== true) fail('SANITIZED_ATTESTATION_REQUIRED');
    const record = {
      format: FORMATS.record, classification: 'secret-local', logicalPath: request.logicalPath,
      reference: { referenceId: request.referenceId, sourceId: request.sourceId, version: request.version, kind: request.kind, purpose: request.purpose }, sanitized: true,
    };
    record.recordId = recordIdFor(record);
    validateRecord(record, { ...this, allowSecret: true });
    immutableWrite(this.storeRoot, `records/secret-local/${record.recordId}.json`, jsonBytes(record));
    return JSON.parse(canonical(record));
  }

  #persist(record, bytes) {
    immutableWrite(this.storeRoot, `objects/${record.classification}/${record.payload.sha256}.blob`, bytes);
    immutableWrite(this.storeRoot, `records/${record.classification}/${record.recordId}.json`, jsonBytes(record));
  }

  getRecord(reference) {
    shape(reference, ['recordId', 'classification']);
    classification(reference.classification);
    hash(reference.recordId);
    const record = parse(safeRead(this.storeRoot, `records/${reference.classification}/${reference.recordId}.json`, 16 * 1024));
    validateRecord(record, { ...this, allowSecret: true });
    if (record.recordId !== reference.recordId || record.classification !== reference.classification) fail('RECORD_BINDING_MISMATCH');
    return record;
  }

  #records(references) {
    if (!Array.isArray(references) || references.length < 1 || references.length > this.maxRecords) fail('RECORD_LIMIT');
    const records = references.map(reference => this.getRecord(reference));
    if (new Set(records.map(record => record.recordId)).size !== records.length) fail('DUPLICATE_RECORD');
    records.forEach(record => classification(record.classification, true));
    uniqueLogicalPaths(records);
    return records.sort((a, b) => a.recordId.localeCompare(b.recordId));
  }

  #payload(record) {
    const bytes = safeRead(this.storeRoot, `objects/${record.classification}/${record.payload.sha256}.blob`, this.maxPayloadBytes);
    if (bytes.length !== record.payload.bytes || sha256(bytes) !== record.payload.sha256) fail('PAYLOAD_DIGEST_MISMATCH');
    sanitizedPayload(bytes, record.source.path, record.logicalPath);
    return bytes;
  }

  prepareExport(request) {
    shape(request, ['records', 'destination', 'expectedSources']);
    destination(request.destination);
    const records = this.#records(request.records);
    verifyExpected(records, request.expectedSources);
    if (request.destination === 'github' && records.some(record => record.classification !== 'public-evidence')) fail('EXPORT_CLASS_DENIED');
    const objects = new Map();
    for (const record of records) {
      const bytes = this.#payload(record);
      objects.set(`${record.classification}:${record.payload.sha256}`, { classification: record.classification, sha256: record.payload.sha256, bytes: bytes.length, data: bytes.toString('base64') });
    }
    const bundle = { format: FORMATS.bundle, destination: request.destination, records, objects: [...objects.values()].sort((a, b) => `${a.classification}:${a.sha256}`.localeCompare(`${b.classification}:${b.sha256}`)) };
    const bytes = jsonBytes(bundle);
    if (bytes.length > this.maxBundleBytes) fail('BUNDLE_TOO_LARGE');
    const bundleDigest = sha256(bytes);
    const logical = `prepared/${bundleDigest}.json`;
    immutableWrite(this.storeRoot, logical, bytes);
    return { status: 'PREPARED_LOCAL_ONLY', bundleDigest, bundlePath: containedPath(this.storeRoot, logical), bytes: bytes.length, destination: request.destination, recordIds: records.map(record => record.recordId) };
  }

  #validateBundle(bytes, expectedSources, expectedDestination) {
    if (bytes.length > this.maxBundleBytes) fail('BUNDLE_TOO_LARGE');
    destination(expectedDestination);
    const bundle = parse(bytes);
    shape(bundle, ['format', 'destination', 'records', 'objects']);
    if (bundle.format !== FORMATS.bundle) fail('INVALID_BUNDLE');
    destination(bundle.destination);
    if (bundle.destination !== expectedDestination) fail('DESTINATION_BINDING_MISMATCH');
    if (!Array.isArray(bundle.records) || bundle.records.length < 1 || bundle.records.length > this.maxRecords) fail('RECORD_LIMIT');
    if (!Array.isArray(bundle.objects) || bundle.objects.length < 1 || bundle.objects.length > this.maxRecords) fail('OBJECT_LIMIT');
    const records = bundle.records.map(record => validateRecord(record, this));
    if (new Set(records.map(record => record.recordId)).size !== records.length) fail('DUPLICATE_RECORD');
    uniqueLogicalPaths(records);
    verifyExpected(records, expectedSources);
    if (bundle.destination === 'github' && records.some(record => record.classification !== 'public-evidence')) fail('EXPORT_CLASS_DENIED');
    const objects = new Map();
    for (const object of bundle.objects) {
      shape(object, ['classification', 'sha256', 'bytes', 'data']);
      classification(object.classification, true);
      hash(object.sha256);
      if (!Number.isSafeInteger(object.bytes) || object.bytes < 0 || object.bytes > this.maxPayloadBytes) fail('PAYLOAD_TOO_LARGE');
      if (typeof object.data !== 'string' || object.data.length > 4 * Math.ceil(this.maxPayloadBytes / 3) || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(object.data)) fail('INVALID_BASE64');
      const payload = Buffer.from(object.data, 'base64');
      if (payload.toString('base64') !== object.data) fail('INVALID_BASE64');
      if (payload.length !== object.bytes || sha256(payload) !== object.sha256) fail('PAYLOAD_DIGEST_MISMATCH');
      const key = `${object.classification}:${object.sha256}`;
      if (objects.has(key)) fail('DUPLICATE_OBJECT');
      objects.set(key, payload);
    }
    const needed = new Set();
    for (const record of records) {
      const key = `${record.classification}:${record.payload.sha256}`;
      const payload = objects.get(key);
      if (!payload || payload.length !== record.payload.bytes) fail('MISSING_OBJECT');
      sanitizedPayload(payload, record.source.path, record.logicalPath);
      needed.add(key);
    }
    if (needed.size !== objects.size) fail('UNREFERENCED_OBJECT');
    return { bundle, objects, bytes: jsonBytes(bundle) };
  }

  quarantineImport(request) {
    shape(request, ['sourcePath', 'expectedSources', 'expectedDestination']);
    payloadPath(request.sourcePath);
    if (!/\.json$/i.test(request.sourcePath)) fail('UNSUPPORTED_PAYLOAD');
    const incoming = safeRead(this.allowedRoot, request.sourcePath, this.maxBundleBytes);
    const validated = this.#validateBundle(incoming, request.expectedSources, request.expectedDestination);
    const quarantineDigest = sha256(validated.bytes);
    immutableWrite(this.storeRoot, `quarantine/${quarantineDigest}.json`, validated.bytes);
    return { status: 'QUARANTINED', quarantineDigest, recordIds: validated.bundle.records.map(record => record.recordId), destination: request.expectedDestination };
  }

  promote(request) {
    shape(request, ['quarantineDigest', 'expectedSources', 'expectedDestination', 'approval']);
    hash(request.quarantineDigest);
    shape(request.approval, ['reviewed', 'reviewerId', 'quarantineDigest'], 'PROMOTION_APPROVAL_REQUIRED');
    if (request.approval.reviewed !== true || request.approval.quarantineDigest !== request.quarantineDigest) fail('PROMOTION_APPROVAL_REQUIRED');
    identifier(request.approval.reviewerId);
    const bytes = safeRead(this.storeRoot, `quarantine/${request.quarantineDigest}.json`, this.maxBundleBytes);
    if (sha256(bytes) !== request.quarantineDigest) fail('QUARANTINE_DIGEST_MISMATCH');
    const validated = this.#validateBundle(bytes, request.expectedSources, request.expectedDestination);
    for (const record of validated.bundle.records) this.#persist(record, validated.objects.get(`${record.classification}:${record.payload.sha256}`));
    const receipt = { format: FORMATS.promotion, quarantineDigest: request.quarantineDigest, destination: request.expectedDestination, recordIds: validated.bundle.records.map(record => record.recordId).sort(), approval: JSON.parse(canonical(request.approval)) };
    immutableWrite(this.storeRoot, `promotions/${request.quarantineDigest}.json`, jsonBytes(receipt));
    return { status: 'PROMOTED_LOCAL', ...receipt };
  }

  restore(request) {
    shape(request, ['records', 'destinationRoot', 'expectedSources']);
    const destinationRoot = absoluteRoot(request.destinationRoot);
    disjoint(destinationRoot, this.storeRoot);
    disjoint(destinationRoot, this.allowedRoot);
    directory(destinationRoot);
    const records = this.#records(request.records);
    verifyExpected(records, request.expectedSources);
    const pending = records.map(record => {
      const target = containedPath(destinationRoot, record.logicalPath);
      if (inspectAbsolute(target, true)) fail('DESTINATION_EXISTS');
      return { record, bytes: this.#payload(record), target };
    });
    // Full preflight precedes any restore write. A later OS failure may retain a
    // partial restore; retry never overwrites any destination file.
    for (const { record, bytes } of pending) {
      immutableWrite(destinationRoot, record.logicalPath, bytes, { allowIdentical: false });
      const restored = safeRead(destinationRoot, record.logicalPath, this.maxPayloadBytes);
      if (restored.length !== record.payload.bytes || sha256(restored) !== record.payload.sha256) fail('RESTORE_VERIFICATION_FAILED');
    }
    return { status: 'RESTORED_VERIFIED', files: pending.map(({ record, target }) => ({ logicalPath: record.logicalPath, absolutePath: target, sha256: record.payload.sha256, bytes: record.payload.bytes, recordId: record.recordId })) };
  }
}

export function openAdapter(options) { return new LocalEvidenceAdapter(options); }
