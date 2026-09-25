import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const stage = process.argv[2];
if (!['x1', 'x2'].includes(stage)) throw new Error('usage: validate_auren_v704_v5_stage.mjs x1|x2');
const base = path.join(root, 'docs', 'auren-lark', 'v704-v5', stage);
const manifestPath = path.join(base, 'manifest.json');

function walk(dir, rows = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, rows);
    else if (entry.isFile()) rows.push(full);
  }
  return rows;
}
const sha = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const normalized = file => Buffer.from(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'));

const files = walk(base);
const stageRunner = path.join(root, 'scripts', `run_auren_v704_v5_${stage}.py`);
files.push(stageRunner);
files.push(fileURLToPath(import.meta.url));
if (stage === 'x2') files.push(path.join(root, 'scripts', 'validate_auren_v704_v5_hooks.mjs'));
const jsonFiles = files.filter(file => file.endsWith('.json'));
for (const file of jsonFiles) JSON.parse(fs.readFileSync(file, 'utf8'));

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const mismatches = [];
for (const entry of manifest.entries) {
  const file = path.join(root, ...entry.path.split('/'));
  const buffer = normalized(file);
  const observed = sha(buffer);
  if (buffer.length !== entry.bytes || observed !== entry.sha256) mismatches.push({ path: entry.path, bytes: buffer.length, sha256: observed });
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
const thisRelative = path.relative(root, fileURLToPath(import.meta.url)).replaceAll('\\', '/');
for (const file of files) {
  if (!/\.(?:json|md|mjs|txt|py|html)$/.test(file)) continue;
  const text = fs.readFileSync(file, 'utf8');
  const relative = path.relative(root, file).replaceAll('\\', '/');
  for (const [privacyClass, expression] of Object.entries(patterns)) {
    if (relative === thisRelative && privacyClass === 'delegation_markup') {
      scannerDefinitionExclusions += 1;
      continue;
    }
    expression.lastIndex = 0;
    if (expression.test(text)) privacyHits.push({ privacy_class: privacyClass, path: relative });
  }
}

const securityFindings = [];
for (const file of files.filter(file => /\.(?:py|mjs|txt)$/.test(file))) {
  const text = fs.readFileSync(file, 'utf8');
  const relative = path.relative(root, file).replaceAll('\\', '/');
  if (/\beval\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'dynamic_eval' });
  if (/subprocess\.(?:run|Popen|check_output)\([^\n]*shell\s*=\s*True/.test(text)) securityFindings.push({ path: relative, rule: 'shell_true' });
  if (/\bos\.system\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'os_system' });
  if (/child_process\.(?:exec|execSync)\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'shell_exec' });
}

const summary = JSON.parse(fs.readFileSync(path.join(base, 'session-summary.json'), 'utf8'));
const flow = JSON.parse(fs.readFileSync(path.join(base, 'method-flow.json'), 'utf8'));
const expected = stage === 'x1'
  ? { contracts: 150, safe: 400, candidates: 300, refusals: 300, cfr: 300, tests: 15, skills: 10, runners: 5, smokes: 10, passing: 1000, failed: 300 }
  : { contracts: 150, safe: 400, candidates: 300, refusals: 300, cfr: 300, tests: 30, skills: 10, runners: 5, smokes: 10, passing: 1000, failed: 300 };
const skillValidation = JSON.parse(fs.readFileSync(path.join(base, 'skill-validation.json'), 'utf8'));
const runnerSmokes = JSON.parse(fs.readFileSync(path.join(base, 'runner-smokes.json'), 'utf8'));
const checks = [
  { id: 'strict_json', passed: jsonFiles.length >= 12, observed: jsonFiles.length },
  { id: 'manifest_replay', passed: mismatches.length === 0, observed: { entries: manifest.entries.length, mismatches } },
  { id: 'five_class_privacy', passed: privacyHits.length === 0, observed: { confirmed_hits: privacyHits, scanner_definition_exclusions: scannerDefinitionExclusions } },
  { id: 'bounded_changed_source_security', passed: securityFindings.length === 0, observed: securityFindings },
  { id: 'domain_counts', passed: summary.domain_harness.contracts === expected.contracts && summary.safe === expected.safe && summary.candidate_failed === expected.candidates && summary.separate_refusals_passed === expected.refusals && summary.clean_fix_refine_passed === expected.cfr, observed: summary },
  { id: 'test_counts', passed: summary.tests.passed === expected.tests && summary.tests.failed === 0 && summary.tests.replays === 0, observed: summary.tests },
  { id: 'skill_validation', passed: skillValidation.count === expected.skills && skillValidation.passed === expected.skills, observed: { count: skillValidation.count, passed: skillValidation.passed } },
  { id: 'runner_smokes', passed: runnerSmokes.count === expected.smokes && runnerSmokes.passed === expected.smokes, observed: { count: runnerSmokes.count, passed: runnerSmokes.passed } },
  { id: 'method_flow_counts', passed: flow.counts.methods === 10 && flow.counts.witness_results.pass === expected.passing && flow.counts.witness_results.fail === expected.failed, observed: flow.counts },
  { id: 'subject_nonpromotion', passed: summary.malformed_subjects_promoted === 0 && summary.evidence_deleted === 0, observed: { promoted: summary.malformed_subjects_promoted, deleted: summary.evidence_deleted } },
  { id: 'owner_file_guard', passed: files.length < 2000, observed: files.length }
];
if (stage === 'x2') {
  const models = JSON.parse(fs.readFileSync(path.join(base, 'models.json'), 'utf8'));
  checks.push({ id: 'x2_coordinate_models', passed: models.count === 15 && models.records.every(record => Array.isArray(record.coordinates) && record.coordinates.length === 3), observed: models.count });
  const hooks = JSON.parse(fs.readFileSync(path.join(base, 'hook-smokes.json'), 'utf8'));
  checks.push({ id: 'advisory_hook_smokes', passed: hooks.hook_count === 10 && hooks.passed === 20, observed: { hooks: hooks.hook_count, passed: hooks.passed } });
}
const failed = checks.filter(check => !check.passed);
const receipt = { schema: 'ghc.family.stage-validation-receipt.v1', owner: 'Auren Lark', phase: 'v704-v5', stage, state: failed.length ? `INVALID_${stage.toUpperCase()}_OWNER_SCOPED` : `VALID_${stage.toUpperCase()}_OWNER_SCOPED`, checks, passed_checks: checks.length - failed.length, failed_checks: failed.length, successful_component_replays: 0, same_owner_only: true, independent_reproduction: false, boundary: 'Bounded same-owner stage validation only; no full-repository suite, independent reproduction, empirical validation, authority or Stage 20 promotion.' };
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
if (failed.length) process.exitCode = 1;
