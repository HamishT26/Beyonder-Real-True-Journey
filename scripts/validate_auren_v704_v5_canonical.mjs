import crypto from 'node:crypto';
import cp from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const expectedFinal = process.argv[2];
if (!/^[0-9a-f]{40}$/.test(expectedFinal || '')) throw new Error('usage: validate_auren_v704_v5_canonical.mjs <40-char-final>');
const branch = 'codex/GHC-Family/auren-lark-main-3';
const source = 'ec723e278979d47a2d8ec77b409563e612d17191';
const planning = '19012bc59cc9588a31e0bf19854c46106871b0fb';
const correction = '073c94ee1a564c1baa03d5eca88259472fe8ab84';
const x1 = '0b701a3af0d36fb520c6945803235890fef7d3ca';
const x2 = 'e1e06d8298ef5137e9c7fd6dde83e12542262d5f';
const boundary = 'Metadata-only exact-final owner-scoped canonical under shared infrastructure. No full-repository suite, domain or test replay, external audit, independent reproduction, empirical validation, production certification, complete privacy or accessibility assurance, exhaustive security, authority or Stage 20 promotion. NOT_READY_FOR_STAGE_20.';

const run = args => cp.execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }).trim();
const blob = (commit, relative) => cp.execFileSync('git', ['-C', root, 'cat-file', 'blob', `${commit}:${relative}`], { maxBuffer: 64 * 1024 * 1024 });
const sha = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const words = text => (text.match(/\S+/g) || []).length;
const checks = [];
const check = (id, passed, observed) => checks.push({ id, passed: Boolean(passed), observed });

const head = run(['rev-parse', 'HEAD']);
const parent = run(['rev-parse', 'HEAD^']);
const currentBranch = run(['branch', '--show-current']);
const upstream = run(['rev-parse', '@{upstream}']);
const tracking = run(['rev-parse', `refs/remotes/origin/${branch}`]);
const liveLine = run(['ls-remote', '--heads', 'origin', `refs/heads/${branch}`]);
const live = liveLine.split(/\s+/)[0] || '';
const divergence = run(['rev-list', '--left-right', '--count', `${head}...${live}`]);
const status = run(['status', '--porcelain=v1']);
check('exact_head', head === expectedFinal, { head, expectedFinal });
check('owner_branch', currentBranch === branch, currentBranch);
check('direct_parent_x2', parent === x2, parent);
check('planning_parent_source', run(['rev-parse', `${planning}^`]) === source, run(['rev-parse', `${planning}^`]));
check('correction_parent_planning', run(['rev-parse', `${correction}^`]) === planning, run(['rev-parse', `${correction}^`]));
check('x1_parent_correction', run(['rev-parse', `${x1}^`]) === correction, run(['rev-parse', `${x1}^`]));
check('x2_parent_x1', run(['rev-parse', `${x2}^`]) === x1, run(['rev-parse', `${x2}^`]));
check('source_to_final_commit_count', run(['rev-list', '--count', `${source}..${expectedFinal}`]) === '5', run(['rev-list', '--count', `${source}..${expectedFinal}`]));
check('source_to_final_zero_merges', run(['rev-list', '--merges', '--count', `${source}..${expectedFinal}`]) === '0', run(['rev-list', '--merges', '--count', `${source}..${expectedFinal}`]));
check('clean_state', status === '', status);
check('typed_zero_divergence', divergence.replace(/\s+/g, '/') === '0/0', divergence);
check('four_way_equality', [head, upstream, tracking, live].every(value => value === expectedFinal), { head, upstream, tracking, live });

function replayManifest(name, commit, relative) {
  const manifest = JSON.parse(blob(commit, relative).toString('utf8'));
  const mismatches = [];
  for (const entry of manifest.entries) {
    let content;
    try { content = blob(commit, entry.path); }
    catch { mismatches.push({ path: entry.path, error: 'missing' }); continue; }
    const digest = sha(content);
    if (content.length !== entry.bytes || digest !== entry.sha256) mismatches.push({ path: entry.path, bytes: content.length, sha256: digest });
  }
  check(`${name}_manifest_replay`, mismatches.length === 0 && manifest.entry_count === manifest.entries.length, { entries: manifest.entries.length, mismatches });
  return manifest.entries.length;
}
const planningEntries = replayManifest('planning', planning, 'docs/auren-lark/v704-v5/planning/manifest.json');
const correctionEntries = replayManifest('planning_correction', correction, 'docs/auren-lark/v704-v5/planning/correction-manifest.json');
const x1Entries = replayManifest('x1', x1, 'docs/auren-lark/v704-v5/x1/manifest.json');
const x2Entries = replayManifest('x2', x2, 'docs/auren-lark/v704-v5/x2/manifest.json');
const sealEntries = replayManifest('content_seal', expectedFinal, 'docs/auren-lark/v704-v5/final/content-seal.json');

const repositoryPaths = run(['ls-tree', '-r', '--name-only', expectedFinal]).split(/\r?\n/).filter(Boolean);
const ownerPaths = repositoryPaths.filter(relative => relative.startsWith('docs/auren-lark/v704-v5/') || (relative.startsWith('scripts/') && relative.includes('auren_v704_v5')));
check('repository_file_guard', repositoryPaths.length < 2000, repositoryPaths.length);
check('owner_file_guard', ownerPaths.length < 2000, ownerPaths.length);
const ownerJson = ownerPaths.filter(relative => relative.endsWith('.json'));
const jsonFailures = [];
for (const relative of ownerJson) {
  try { JSON.parse(blob(expectedFinal, relative).toString('utf8')); }
  catch (error) { jsonFailures.push({ path: relative, error: String(error) }); }
}
check('owner_json_parse', jsonFailures.length === 0, { parses: ownerJson.length, failures: jsonFailures });

const batonRelative = 'docs/auren-lark/v704-v5/final/handoff-baton.md';
const baton = blob(expectedFinal, batonRelative);
const batonText = baton.toString('utf8');
const batonMetadata = JSON.parse(blob(expectedFinal, 'docs/auren-lark/v704-v5/final/baton-metadata.json').toString('utf8'));
check('baton_word_minimum', words(batonText) >= 2000 && batonMetadata.words === words(batonText), words(batonText));
check('baton_bytes', batonMetadata.bytes === baton.length, { declared: batonMetadata.bytes, observed: baton.length });
check('baton_sha256', batonMetadata.sha256 === sha(baton), { declared: batonMetadata.sha256, observed: sha(baton) });
check('baton_end_marker', batonText.trimEnd().endsWith('END OF AUREN LARK V704-V5 HANDOFF BATON'), batonText.trimEnd().split(/\r?\n/).at(-1));

const truth = JSON.parse(blob(expectedFinal, 'docs/auren-lark/v704-v5/final/phase-truth.json').toString('utf8'));
check('truth_outcomes', JSON.stringify(truth.core_outcomes) === JSON.stringify({ completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }), truth.core_outcomes);
check('truth_totals', JSON.stringify(truth.effective_totals) === JSON.stringify({ negatives: 64992, methods: 5775, failed_witnesses: 56157, passing_witnesses: 177808, witnesses: 233965, open_gaps: 2012, exact_gates: 2093 }), truth.effective_totals);
check('source_overlay_separate', truth.source_external_route_overlay_preserved_separately.folded === false, truth.source_external_route_overlay_preserved_separately);
check('stage20_gate', truth.terminal_verdict === 'NOT_READY_FOR_STAGE_20', truth.terminal_verdict);
check('no_successful_replay', truth.successful_session_replays === 0 && truth.source_canonical_replays === 0, { successful_session_replays: truth.successful_session_replays, source_canonical_replays: truth.source_canonical_replays });
const route = JSON.parse(blob(expectedFinal, 'docs/auren-lark/v704-v5/final/route-state.json').toString('utf8'));
check('route_prepared_not_sent', route.state === 'PREPARED_NOT_SENT' && route.prospective_recipient_exact_title === 'Thalen Reed' && route.precontacted === false, route);

const privacyPatterns = {
  credential_assignment: /(?:password|secret|token)\s*[:=]\s*["'][^"']+["']/ig,
  delegation_markup: /<\/?codex_delegation\b/ig,
  private_local_path: /\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]/ig,
  private_uri: /\b(?:plugin|app):\/\/[A-Za-z0-9._~!$&()*+,;=:@/?%-]+/ig,
  raw_uuid: /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/ig
};
const privacyHits = [];
let scannerDefinitionExclusions = 0;
const canonicalRelative = 'scripts/validate_auren_v704_v5_canonical.mjs';
for (const relative of ownerPaths.filter(relative => /\.(?:json|md|mjs|txt|py|html)$/.test(relative))) {
  const text = blob(expectedFinal, relative).toString('utf8');
  for (const [privacyClass, expression] of Object.entries(privacyPatterns)) {
    if (relative === canonicalRelative && privacyClass === 'delegation_markup') { scannerDefinitionExclusions += 1; continue; }
    expression.lastIndex = 0;
    if (expression.test(text)) privacyHits.push({ privacy_class: privacyClass, path: relative });
  }
}
check('five_class_privacy', privacyHits.length === 0, { confirmed_hits: privacyHits, scanner_definition_exclusions: scannerDefinitionExclusions });

const securityFindings = [];
const finalDelta = run(['diff-tree', '--no-commit-id', '--name-only', '-r', expectedFinal]).split(/\r?\n/).filter(Boolean);
for (const relative of finalDelta.filter(relative => /\.(?:py|mjs|txt)$/.test(relative))) {
  const text = blob(expectedFinal, relative).toString('utf8');
  if (/\beval\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'dynamic_eval' });
  if (/subprocess\.(?:run|Popen|check_output)\([^\n]*shell\s*=\s*True/.test(text)) securityFindings.push({ path: relative, rule: 'shell_true' });
  if (/\bos\.system\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'os_system' });
  if (/child_process\.(?:exec|execSync)\s*\(/.test(text)) securityFindings.push({ path: relative, rule: 'shell_exec' });
}
check('bounded_final_delta_security', securityFindings.length === 0, { files: finalDelta.length, findings: securityFindings });
check('final_delta_owner_only', finalDelta.every(relative => relative.startsWith('docs/auren-lark/v704-v5/final/') || (relative.startsWith('scripts/') && relative.includes('auren_v704_v5'))), finalDelta);

const failed = checks.filter(item => !item.passed);
const receiptWithoutDigest = {
  schema: 'ghc.family.exact-final-owner-scoped-canonical-receipt.v1', owner: 'Auren Lark', phase: 'v704-v5', state: failed.length ? 'INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' : 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',
  branch, exact_final: expectedFinal, immutable_source: source, planning, planning_correction: correction, immutable_x1: x1, immutable_x2: x2,
  invocation_count: 1, success_count: failed.length ? 0 : 1, replay_count: 0, metadata_only: true, domain_harnesses_replayed: 0, test_tranches_replayed: 0, source_canonical_replayed: 0,
  check_count: checks.length, passed_checks: checks.length - failed.length, failed_checks: failed.length, planning_manifest_entries: planningEntries, planning_correction_manifest_entries: correctionEntries, x1_manifest_entries: x1Entries, x2_manifest_entries: x2Entries, content_seal_entries: sealEntries,
  owner_json_parses: ownerJson.length, owner_files: ownerPaths.length, repository_files: repositoryPaths.length, baton_words: words(batonText), baton_bytes: baton.length, baton_sha256: sha(baton), privacy_hits: privacyHits, scanner_definition_exclusions: scannerDefinitionExclusions, security_findings: securityFindings, checks,
  same_owner_only: true, independent_reproduction: false, external_audit: false, terminal_verdict: 'NOT_READY_FOR_STAGE_20', boundary
};
const payloadSha256 = sha(Buffer.from(JSON.stringify(receiptWithoutDigest), 'utf8'));
const receipt = { ...receiptWithoutDigest, payload_sha256: payloadSha256 };
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
if (failed.length) process.exitCode = 1;
