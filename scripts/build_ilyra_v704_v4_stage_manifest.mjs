import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.resolve(process.argv[2] || process.cwd());
const stage = process.argv[3];
if (!['x1', 'x2', 'final'].includes(stage)) throw new Error('stage must be x1, x2 or final');
const stageRoot = path.join(root, 'docs', 'ilyra-fen', 'v704-v4', stage);
const entries = [];
function walk(dir) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p);
    else if (ent.name !== 'manifest.json') {
      const bytes = fs.readFileSync(p);
      entries.push({ path: path.relative(root, p).replaceAll('\\', '/'), bytes: bytes.length, sha256: crypto.createHash('sha256').update(bytes).digest('hex'), domain: 'working_bytes_precommit' });
    }
  }
}
walk(stageRoot);
entries.sort((a, b) => a.path.localeCompare(b.path));
const payload = {
  schema: 'ghc.family.precommit-stage-manifest.v1', owner: 'Ilyra Fen', phase: 'v704-v4', stage,
  entry_count: entries.length, entries,
  note: 'Precommit working-byte manifest. Exact Git-blob replay is recorded after the immutable stage commit.',
  boundary: 'Finite synthetic same-owner software evidence only. No independent reproduction, empirical confirmation, authority or Stage 20 promotion. NOT_READY_FOR_STAGE_20.'
};
fs.writeFileSync(path.join(stageRoot, 'manifest.json'), JSON.stringify(payload, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ ok: true, stage, entries: entries.length }));
