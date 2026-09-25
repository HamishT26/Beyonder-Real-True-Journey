import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const relativeManifest = 'docs/auren-lark/v704-v5/planning/correction-manifest.json';
const manifest = JSON.parse(fs.readFileSync(path.join(root, ...relativeManifest.split('/')), 'utf8'));
const mismatches = [];
for (const entry of manifest.entries) {
  const file = path.join(root, ...entry.path.split('/'));
  const buffer = Buffer.from(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'));
  const digest = crypto.createHash('sha256').update(buffer).digest('hex');
  if (buffer.length !== entry.bytes || digest !== entry.sha256) mismatches.push({ path: entry.path, bytes: buffer.length, sha256: digest });
}
const flow = JSON.parse(fs.readFileSync(path.join(root, 'docs', 'auren-lark', 'v704-v5', 'planning', 'method-flow-correction.json'), 'utf8'));
const checks = [
  { id: 'manifest_replay', passed: mismatches.length === 0, observed: { entries: manifest.entries.length, mismatches } },
  { id: 'method_flow_shape', passed: flow.methods.length === 2 && flow.witnesses.length === 4 && flow.counts.witness_results.fail === 2 && flow.counts.witness_results.pass === 2, observed: flow.counts },
  { id: 'source_fold_count', passed: flow.source_fold_count === 0, observed: flow.source_fold_count },
  { id: 'x1_not_started', passed: JSON.parse(fs.readFileSync(path.join(root, 'docs', 'auren-lark', 'v704-v5', 'planning', 'correction.json'), 'utf8')).x1_started === false, observed: false }
];
const failed = checks.filter(check => !check.passed);
process.stdout.write(`${JSON.stringify({ schema: 'ghc.family.planning-correction-validation.v1', state: failed.length ? 'INVALID_PLANNING_CORRECTION' : 'VALID_PLANNING_CORRECTION', checks, passed_checks: checks.length - failed.length, failed_checks: failed.length, boundary: 'Bounded same-owner correction validation only.' }, null, 2)}\n`);
if (failed.length) process.exitCode = 1;
