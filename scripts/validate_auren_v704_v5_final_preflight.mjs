import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const base = path.join(root, 'docs', 'auren-lark', 'v704-v5');
const sealPath = path.join(base, 'final', 'content-seal.json');
const sha = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const normalized = file => Buffer.from(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'));
const words = text => (text.match(/\S+/g) || []).length;
function walk(dir, rows = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, rows);
    else if (entry.isFile()) rows.push(full);
  }
  return rows;
}

const files = walk(base);
for (const name of fs.readdirSync(path.join(root, 'scripts'))) if (name.includes('auren_v704_v5') && /\.(?:mjs|py)$/.test(name)) files.push(path.join(root, 'scripts', name));
const uniqueFiles = [...new Set(files)];
const jsonFiles = uniqueFiles.filter(file => file.endsWith('.json'));
const jsonFailures = [];
for (const file of jsonFiles) {
  try { JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { jsonFailures.push({ path: path.relative(root, file).replaceAll('\\', '/'), error: String(error) }); }
}

const seal = JSON.parse(fs.readFileSync(sealPath, 'utf8'));
const sealMismatches = [];
for (const entry of seal.entries) {
  const file = path.join(root, ...entry.path.split('/'));
  const buffer = normalized(file);
  const digest = sha(buffer);
  if (buffer.length !== entry.bytes || digest !== entry.sha256) sealMismatches.push({ path: entry.path, bytes: buffer.length, sha256: digest });
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
const scannerPaths = new Set(['scripts/validate_auren_v704_v5_canonical.mjs', 'scripts/validate_auren_v704_v5_final_preflight.mjs']);
for (const file of uniqueFiles.filter(file => /\.(?:json|md|mjs|txt|py|html)$/.test(file))) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  const text = fs.readFileSync(file, 'utf8');
  for (const [privacyClass, expression] of Object.entries(patterns)) {
    if (scannerPaths.has(relative) && privacyClass === 'delegation_markup') { scannerDefinitionExclusions += 1; continue; }
    expression.lastIndex = 0;
    if (expression.test(text)) privacyHits.push({ privacy_class: privacyClass, path: relative });
  }
}

const securityFindings = [];
for (const file of uniqueFiles.filter(file => /\.(?:py|mjs|txt)$/.test(file))) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  const text = fs.readFileSync(file, 'utf8');
  if (/\beval\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'dynamic_eval' });
  if (/subprocess\.(?:run|Popen|check_output)\([^\n]*shell\s*=\s*True/.test(text)) securityFindings.push({ path: relative, rule: 'shell_true' });
  if (/\bos\.system\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'os_system' });
  if (/child_process\.(?:exec|execSync)\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'shell_exec' });
}

const baton = fs.readFileSync(path.join(base, 'final', 'handoff-baton.md'));
const batonText = baton.toString('utf8');
const batonMetadata = JSON.parse(fs.readFileSync(path.join(base, 'final', 'baton-metadata.json'), 'utf8'));
const truth = JSON.parse(fs.readFileSync(path.join(base, 'final', 'phase-truth.json'), 'utf8'));
const flow = JSON.parse(fs.readFileSync(path.join(base, 'final', 'method-flow-index.json'), 'utf8'));
const route = JSON.parse(fs.readFileSync(path.join(base, 'final', 'route-state.json'), 'utf8'));
const expectedTotals = { negatives: 64992, methods: 5775, failed_witnesses: 56157, passing_witnesses: 177808, witnesses: 233965, open_gaps: 2012, exact_gates: 2093 };
const checks = [
  { id: 'strict_json', passed: jsonFailures.length === 0, observed: { parses: jsonFiles.length, failures: jsonFailures } },
  { id: 'content_seal', passed: seal.entries.length === seal.entry_count && sealMismatches.length === 0, observed: { entries: seal.entries.length, mismatches: sealMismatches } },
  { id: 'five_class_privacy', passed: privacyHits.length === 0, observed: { confirmed_hits: privacyHits, scanner_definition_exclusions: scannerDefinitionExclusions } },
  { id: 'bounded_source_security', passed: securityFindings.length === 0, observed: securityFindings },
  { id: 'baton_words', passed: words(batonText) >= 2000 && batonMetadata.words === words(batonText), observed: words(batonText) },
  { id: 'baton_bytes', passed: batonMetadata.bytes === baton.length, observed: { declared: batonMetadata.bytes, actual: baton.length } },
  { id: 'baton_hash', passed: batonMetadata.sha256 === sha(baton), observed: sha(baton) },
  { id: 'baton_eof', passed: batonText.trimEnd().endsWith('END OF AUREN LARK V704-V5 HANDOFF BATON'), observed: batonText.trimEnd().split(/\r?\n/).at(-1) },
  { id: 'truth_outcomes', passed: JSON.stringify(truth.core_outcomes) === JSON.stringify({ completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }), observed: truth.core_outcomes },
  { id: 'truth_totals', passed: JSON.stringify(truth.effective_totals) === JSON.stringify(expectedTotals), observed: truth.effective_totals },
  { id: 'method_flow_totals', passed: JSON.stringify(flow.effective_totals) === JSON.stringify(expectedTotals), observed: flow.effective_totals },
  { id: 'route_prepared', passed: route.state === 'PREPARED_NOT_SENT' && route.prospective_recipient_exact_title === 'Thalen Reed' && route.precontacted === false, observed: route },
  { id: 'owner_file_guard', passed: uniqueFiles.length < 2000, observed: uniqueFiles.length },
  { id: 'stage20_gate', passed: truth.terminal_verdict === 'NOT_READY_FOR_STAGE_20', observed: truth.terminal_verdict }
];
const failed = checks.filter(check => !check.passed);
process.stdout.write(`${JSON.stringify({ schema: 'ghc.family.final-preflight-receipt.v1', owner: 'Auren Lark', phase: 'v704-v5', state: failed.length ? 'INVALID_FINAL_PREFLIGHT' : 'VALID_FINAL_PREFLIGHT', checks, passed_checks: checks.length - failed.length, failed_checks: failed.length, domain_harnesses_replayed: 0, test_tranches_replayed: 0, successful_component_replays: 0, same_owner_only: true, independent_reproduction: false, boundary: 'Bounded same-owner final precommit metadata validation only.' }, null, 2)}\n`);
if (failed.length) process.exitCode = 1;
