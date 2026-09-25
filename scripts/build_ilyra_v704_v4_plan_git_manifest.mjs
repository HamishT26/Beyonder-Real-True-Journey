import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const root = path.resolve(process.argv[2] || process.cwd());
const commit = process.argv[3];
if (!/^[0-9a-f]{40}$/.test(commit || '')) throw new Error('exact forty-character planning commit required');
const git = (...args) => execFileSync('git', ['-C', root, ...args]);
const paths = git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).toString('utf8').trim().split(/\r?\n/).filter(Boolean).sort();
const entries = paths.map(rel => {
  const bytes = git('show', `${commit}:${rel}`);
  return { path: rel.replaceAll('\\', '/'), bytes: bytes.length, sha256: crypto.createHash('sha256').update(bytes).digest('hex'), domain: 'raw_git_blob' };
});
const payload = {
  schema: 'ghc.family.exact-git-blob-manifest.v1',
  owner: 'Ilyra Fen', phase: 'v704-v4-planning', commit,
  entry_count: entries.length, entries,
  supersedes_working_byte_manifest_for_exact_commit_replay: true,
  retained_mismatch: 'The precommit working-byte manifest differed for complete-roster.md after Git line-ending normalization.',
  boundary: 'Finite synthetic same-owner software evidence only. No independent reproduction, empirical confirmation, authority or Stage 20 promotion. NOT_READY_FOR_STAGE_20.'
};
const out = path.join(root, 'docs', 'ilyra-fen', 'v704-v4', 'planning', 'manifest-git-blob.json');
fs.writeFileSync(out, JSON.stringify(payload, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ ok: true, commit, entries: entries.length, output: path.relative(root, out).replaceAll('\\', '/') }));
