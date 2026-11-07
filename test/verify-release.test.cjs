'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const modulePath = path.join(__dirname, '..', 'verify-release.cjs');
const api = fs.existsSync(modulePath) ? require(modulePath) : {};
const names = ['EVIDENCE.json', 'cases-x2.json', 'cases.json', 'check-x2.cjs', 'check.cjs', 'kernels-x2.cjs', 'kernels.cjs'];
const digest = b => crypto.createHash('sha256').update(b).digest('hex');
function fixture(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ghc-verifier-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const files = names.map(name => {
    const content = Buffer.from('synthetic ' + name + '\n');
    fs.writeFileSync(path.join(dir, name), content);
    return { path: name, bytes: content.length, sha256: digest(content) };
  });
  const manifest = { schema: 'ghc.release-integrity.v1', files };
  const save = () => fs.writeFileSync(path.join(dir, 'RELEASE-MANIFEST.json'), JSON.stringify(manifest));
  save();
  return { dir, manifest, save };
}
test('exports the release verifier', () => assert.equal(typeof api.verifyRelease, 'function'));
test('matches all seven files without changing bytes', t => {
  const f = fixture(t), before = names.map(n => fs.readFileSync(path.join(f.dir, n)));
  assert.deepEqual(api.verifyRelease(f.dir), { ok: true, checked: 7, errors: [] });
  names.forEach((n, i) => assert.deepEqual(fs.readFileSync(path.join(f.dir, n)), before[i]));
});
const badManifests = [
  ['wrong schema', m => { m.schema = 'other'; }],
  ['extra top-level field', m => { m.authority = true; }],
  ['missing entry', m => { m.files.pop(); }],
  ['duplicate entry', m => { m.files[1] = m.files[0]; }],
  ['traversal path', m => { m.files[0].path = '../outside'; }],
  ['absolute path', m => { m.files[0].path = '/outside'; }],
  ['unknown basename', m => { m.files[0].path = 'private.txt'; }],
  ['extra entry field', m => { m.files[0].token = 'synthetic'; }],
  ['negative bytes', m => { m.files[0].bytes = -1; }],
  ['fractional bytes', m => { m.files[0].bytes = 1.5; }],
  ['string bytes', m => { m.files[0].bytes = '1'; }],
  ['oversized declared bytes', m => { m.files[0].bytes = 1048577; }],
  ['uppercase digest', m => { m.files[0].sha256 = 'A'.repeat(64); }],
  ['digest with newline', m => { m.files[0].sha256 += '\n'; }],
  ['null entry', m => { m.files[0] = null; }],
  ['non-array files', m => { m.files = {}; }]
];
for (const [label, mutate] of badManifests) test('rejects ' + label + ' before reading payloads', t => {
  const f = fixture(t); mutate(f.manifest); f.save();
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 0, errors: ['MANIFEST_SCHEMA'] });
});
for (const [label, value, expected] of [
  ['malformed JSON', '{', 'MANIFEST_JSON'],
  ['null root', 'null', 'MANIFEST_SCHEMA'],
  ['array root', '[]', 'MANIFEST_SCHEMA'],
  ['oversized manifest', ' '.repeat(16385), 'MANIFEST_READ']
]) test('rejects ' + label, t => {
  const f = fixture(t); fs.writeFileSync(path.join(f.dir, 'RELEASE-MANIFEST.json'), value);
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 0, errors: [expected] });
});
test('reports missing manifest without leaking an absolute path', t => {
  const f = fixture(t); fs.unlinkSync(path.join(f.dir, 'RELEASE-MANIFEST.json'));
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 0, errors: ['MANIFEST_READ'] });
});
for (const kind of ['missing', 'directory', 'oversized']) test('rejects ' + kind + ' payload', t => {
  const f = fixture(t), p = path.join(f.dir, names[0]); fs.unlinkSync(p);
  if (kind === 'directory') fs.mkdirSync(p);
  if (kind === 'oversized') fs.writeFileSync(p, Buffer.alloc(1048577));
  const result = api.verifyRelease(f.dir);
  assert.equal(result.ok, false); assert.equal(result.checked, 6);
  assert.deepEqual(result.errors, [names[0] + ':READ']);
});
test('rejects symlink payload', t => {
  const f = fixture(t), p = path.join(f.dir, names[0]); fs.unlinkSync(p);
  try { fs.symlinkSync(path.join(f.dir, names[1]), p); }
  catch (e) { if (e.code === 'EPERM') return t.skip('Symlink creation unavailable on this host'); throw e; }
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 6, errors: [names[0] + ':READ'] });
});
test('rejects symlink manifest', t => {
  const f = fixture(t), p = path.join(f.dir, 'RELEASE-MANIFEST.json'); fs.renameSync(p, path.join(f.dir, 'saved.json'));
  try { fs.symlinkSync(path.join(f.dir, 'saved.json'), p); }
  catch (e) { if (e.code === 'EPERM') return t.skip('Symlink creation unavailable on this host'); throw e; }
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 0, errors: ['MANIFEST_READ'] });
});
test('detects same-length content change', t => {
  const f = fixture(t), p = path.join(f.dir, names[0]), b = fs.readFileSync(p); b[0] ^= 1; fs.writeFileSync(p, b);
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 7, errors: [names[0] + ':SHA256'] });
});
test('detects changed byte length and digest', t => {
  const f = fixture(t); fs.appendFileSync(path.join(f.dir, names[0]), '\n');
  assert.deepEqual(api.verifyRelease(f.dir), { ok: false, checked: 7, errors: [names[0] + ':BYTES', names[0] + ':SHA256'] });
});
test('CLI uses its release directory rather than caller cwd', t => {
  const f = fixture(t); fs.copyFileSync(modulePath, path.join(f.dir, 'verify-release.cjs'));
  const r = spawnSync(process.execPath, [path.join(f.dir, 'verify-release.cjs')], { cwd: os.tmpdir(), encoding: 'utf8', timeout: 5000 });
  assert.equal(r.status, 0); assert.equal(r.stderr, '');
  assert.deepEqual(JSON.parse(r.stdout), { ok: true, checked: 7, errors: [] });
});
test('CLI failure exits nonzero with bounded diagnostic', t => {
  const f = fixture(t); fs.copyFileSync(modulePath, path.join(f.dir, 'verify-release.cjs')); fs.unlinkSync(path.join(f.dir, names[0]));
  const r = spawnSync(process.execPath, [path.join(f.dir, 'verify-release.cjs')], { encoding: 'utf8', timeout: 5000 });
  assert.equal(r.status, 1); assert.equal(JSON.parse(r.stdout).ok, false); assert.equal(r.stderr, '');
});
