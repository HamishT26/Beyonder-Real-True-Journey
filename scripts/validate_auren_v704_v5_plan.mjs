import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const base = path.join(root, 'docs', 'auren-lark', 'v704-v5');

function walk(dir, rows = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, rows);
    else if (entry.isFile()) rows.push(full);
  }
  return rows;
}
function digest(buffer) { return crypto.createHash('sha256').update(buffer).digest('hex'); }
function normalized(file) { return Buffer.from(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n')); }

const files = walk(base);
files.push(path.join(root, 'scripts', 'build_auren_v704_v5_plan.mjs'));
files.push(path.join(root, 'scripts', 'validate_auren_v704_v5_plan.mjs'));
const jsonFiles = files.filter(file => file.endsWith('.json'));
for (const file of jsonFiles) JSON.parse(fs.readFileSync(file, 'utf8'));

const index = JSON.parse(fs.readFileSync(path.join(base, 'planning', 'proposal-index.json'), 'utf8'));
const inherited = files
  .filter(file => /planning[\\/]inherited[\\/]part-\d+\.json$/.test(file))
  .reduce((count, file) => count + JSON.parse(fs.readFileSync(file, 'utf8')).records.length, 0);
const manifest = JSON.parse(fs.readFileSync(path.join(base, 'planning', 'manifest.json'), 'utf8'));
const manifestMismatches = [];
for (const entry of manifest.entries) {
  const file = path.join(root, ...entry.path.split('/'));
  const buffer = normalized(file);
  const observed = digest(buffer);
  if (buffer.length !== entry.bytes || observed !== entry.sha256) {
    manifestMismatches.push({ path: entry.path, observed_bytes: buffer.length, observed_sha256: observed });
  }
}

const patterns = {
  credential_assignment: /(?:password|secret|token)\s*[:=]\s*["'][^"']+["']/ig,
  delegation_markup: /<\/?codex_delegation\b/ig,
  private_local_path: /\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]/ig,
  private_uri: /\b(?:plugin|app):\/\/[A-Za-z0-9._~!$&()*+,;=:@/?%-]+/ig,
  raw_uuid: /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/ig
};
const privacyHits = [];
let scannerDefinitionExclusions = 0;
const validatorRelative = 'scripts/validate_auren_v704_v5_plan.mjs';
for (const file of files) {
  if (!/\.(?:json|md|mjs|txt|py|html)$/.test(file)) continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const [privacyClass, expression] of Object.entries(patterns)) {
    if (path.relative(root, file).replaceAll('\\', '/') === validatorRelative && privacyClass === 'delegation_markup') {
      scannerDefinitionExclusions += 1;
      continue;
    }
    expression.lastIndex = 0;
    if (expression.test(text)) privacyHits.push({ privacy_class: privacyClass, path: path.relative(root, file).replaceAll('\\', '/') });
  }
}

const flow = JSON.parse(fs.readFileSync(path.join(base, 'planning', 'method-flow.json'), 'utf8'));
const expectedOutcomes = { completed: 255, represented: 15, open_gap: 15, exact_gate: 15 };
const checks = [
  { id: 'strict_json', passed: jsonFiles.length > 0, observed: jsonFiles.length },
  { id: 'new_contracts', passed: index.new_contracts === 300, observed: index.new_contracts },
  { id: 'inherited_zero_credit', passed: inherited === 300, observed: inherited },
  { id: 'four_outcome_labels', passed: JSON.stringify(index.outcomes) === JSON.stringify(expectedOutcomes), observed: index.outcomes },
  { id: 'manifest_replay', passed: manifestMismatches.length === 0, observed: { entries: manifest.entries.length, mismatches: manifestMismatches } },
  { id: 'five_class_privacy', passed: privacyHits.length === 0, observed: { confirmed_hits: privacyHits, scanner_definition_exclusions: scannerDefinitionExclusions } },
  { id: 'method_flow_shape', passed: flow.schema === 'ghc.family.method-flow-state.v1' && flow.methods.length === flow.counts.methods && flow.witnesses.length === flow.counts.witnesses, observed: flow.counts },
  { id: 'allowed_extensions', passed: files.every(file => ['.json', '.md', '.mjs'].includes(path.extname(file))), observed: [...new Set(files.map(file => path.extname(file)))].sort() },
  { id: 'owner_file_guard', passed: files.length < 2000, observed: files.length }
];
const failed = checks.filter(check => !check.passed);
const receipt = { schema: 'ghc.family.planning-validation-receipt.v1', owner: 'Auren Lark', phase: 'v704-v5', state: failed.length ? 'INVALID_PLANNING' : 'VALID_PLANNING', checks, passed_checks: checks.length - failed.length, failed_checks: failed.length, boundary: 'Bounded same-owner planning validation only; no domain execution, independent reproduction, authority or Stage 20 promotion.' };
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
if (failed.length) process.exitCode = 1;
