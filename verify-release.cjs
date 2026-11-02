'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');

// This fixed list is deliberately independent of the supplied manifest.
const FILES = Object.freeze([
  'EVIDENCE.json', 'cases-x2.json', 'cases.json', 'check-x2.cjs',
  'check.cjs', 'kernels-x2.cjs', 'kernels.cjs'
]);
const MANIFEST_LIMIT = 16384;
const PAYLOAD_LIMIT = 1048576;
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const exactKeys = (value, keys) => record(value) && Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key));

function boundedRead(filename, limit) {
  // Reject ordinary symlinks before open and verify the opened object too.
  // This is not protection against a malicious concurrent filesystem writer.
  const before = fs.lstatSync(filename);
  if (!before.isFile() || before.size > limit) throw new Error('READ');
  const fd = fs.openSync(filename, 'r');
  try {
    const opened = fs.fstatSync(fd);
    if (!opened.isFile() || opened.size > limit || opened.dev !== before.dev || opened.ino !== before.ino) throw new Error('READ');
    const buffer = Buffer.alloc(limit + 1);
    let count = 0;
    while (count < buffer.length) {
      const read = fs.readSync(fd, buffer, count, buffer.length - count, null);
      if (read === 0) break;
      count += read;
    }
    if (count > limit) throw new Error('READ');
    return buffer.subarray(0, count);
  } finally {
    fs.closeSync(fd);
  }
}

function validManifest(manifest) {
  if (!exactKeys(manifest, ['schema', 'files']) || manifest.schema !== 'ghc.release-integrity.v1' || !Array.isArray(manifest.files) || manifest.files.length !== FILES.length) return false;
  const seen = new Set();
  for (const item of manifest.files) {
    if (!exactKeys(item, ['path', 'bytes', 'sha256']) || !FILES.includes(item.path) || seen.has(item.path) || !Number.isSafeInteger(item.bytes) || item.bytes < 0 || item.bytes > PAYLOAD_LIMIT || typeof item.sha256 !== 'string' || item.sha256.length !== 64 || !/^[a-f0-9]{64}$/.test(item.sha256)) return false;
    seen.add(item.path);
  }
  return true;
}

function verifyRelease(directory) {
  const fail = error => ({ ok: false, checked: 0, errors: [error] });
  let bytes, manifest;
  try { bytes = boundedRead(path.join(directory, 'RELEASE-MANIFEST.json'), MANIFEST_LIMIT); }
  catch { return fail('MANIFEST_READ'); }
  try { manifest = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { return fail('MANIFEST_JSON'); }
  if (!validManifest(manifest)) return fail('MANIFEST_SCHEMA');
  const byPath = new Map(manifest.files.map(item => [item.path, item]));
  const errors = [];
  let checked = 0;
  for (const filename of FILES) {
    let actual;
    try { actual = boundedRead(path.join(directory, filename), PAYLOAD_LIMIT); }
    catch { errors.push(filename + ':READ'); continue; }
    checked++;
    const expected = byPath.get(filename);
    if (actual.length !== expected.bytes) errors.push(filename + ':BYTES');
    if (createHash('sha256').update(actual).digest('hex') !== expected.sha256) errors.push(filename + ':SHA256');
  }
  return { ok: errors.length === 0, checked, errors };
}

module.exports = { verifyRelease };
if (require.main === module) {
  const result = verifyRelease(__dirname);
  process.stdout.write(JSON.stringify(result) + '\n');
  process.exitCode = result.ok ? 0 : 1;
}
