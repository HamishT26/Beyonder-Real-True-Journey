import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const root = path.resolve(process.argv[2] || process.cwd());
const exactFinal = process.argv[3];
const receiptPath = path.resolve(process.argv[4] || 'D:/GHC-Archives/phase-banks/ilyra-fen-v704-v4/canonical-receipt.json');
if (!/^[0-9a-f]{40}$/.test(exactFinal || '')) throw new Error('exact forty-character final commit required');
const source = 'f6c86fb56f5492d4d830b0439300001e54ba284f';
const x1 = '0459221af11cf03a12feb2b70d65bfff4f97df7e';
const x2 = 'eb0b912def92a0696207d9c6137c991db0714791';
const branch = 'codex/GHC-Family/ilyra-fen-main-2';
const git = (...args) => execFileSync('git', ['-C', root, ...args], { maxBuffer: 128 * 1024 * 1024 });
const text = (...args) => git(...args).toString('utf8').trim();
const blob = relative => git('show', `${exactFinal}:${relative}`);
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const checks = [];
const check = (id, condition, observed) => {
  checks.push({ id, passed: Boolean(condition), observed });
  if (!condition) throw new Error(`${id} failed: ${JSON.stringify(observed)}`);
};

const head = text('rev-parse', 'HEAD');
const upstream = text('rev-parse', '@{upstream}');
const tracking = text('rev-parse', `refs/remotes/origin/${branch}`);
const liveLine = text('ls-remote', 'origin', `refs/heads/${branch}`);
const live = liveLine.split(/\s+/)[0];
const divergence = text('rev-list', '--left-right', '--count', 'HEAD...@{upstream}');
const status = text('status', '--porcelain');
check('exact_head', head === exactFinal, { head, exactFinal });
check('direct_parent_x2', text('rev-parse', `${exactFinal}^`) === x2, text('rev-parse', `${exactFinal}^`));
check('source_ancestor', (() => { try { git('merge-base', '--is-ancestor', source, exactFinal); return true; } catch { return false; } })(), source);
check('source_to_final_commit_count', Number(text('rev-list', '--count', `${source}..${exactFinal}`)) === 5, text('rev-list', '--count', `${source}..${exactFinal}`));
check('source_to_final_zero_merges', Number(text('rev-list', '--count', '--min-parents=2', `${source}..${exactFinal}`)) === 0, text('rev-list', '--count', '--min-parents=2', `${source}..${exactFinal}`));
check('clean_state', status === '', status);
check('typed_zero_divergence', divergence === '0\t0' || divergence === '0 0', divergence);
check('four_way_equality', [head, upstream, tracking, live].every(value => value === exactFinal), { head, upstream, tracking, live });

const allPaths = text('ls-tree', '-r', '--name-only', exactFinal).split(/\r?\n/).filter(Boolean);
const ownerPaths = allPaths.filter(relative => relative.startsWith('docs/ilyra-fen/v704-v4/') || [
  '.codex/coordination/project.yaml',
  'scripts/build_ilyra_v704_v4_plan.mjs', 'scripts/build_ilyra_v704_v4_plan_git_manifest.mjs',
  'scripts/build_ilyra_v704_v4_stage_manifest.mjs', 'scripts/ghc_family_coupled_uncertainty.py',
  'scripts/run_ilyra_v704_v4_x1.py', 'scripts/run_ilyra_v704_v4_x2.py',
  'scripts/validate_ilyra_v704_v4_hooks.mjs', 'scripts/build_ilyra_v704_v4_installation_receipts.mjs',
  'scripts/build_ilyra_v704_v4_final.mjs', 'scripts/validate_ilyra_v704_v4_canonical.mjs',
  'tests/test_ilyra_v704_v4.py', 'tests/test_ilyra_v704_v4_x2.py',
].includes(relative));
check('repository_file_guard', allPaths.length < 2000, allPaths.length);
check('owner_file_guard', ownerPaths.length < 2000, ownerPaths.length);

let jsonCount = 0;
for (const relative of ownerPaths.filter(relative => relative.endsWith('.json'))) {
  JSON.parse(blob(relative).toString('utf8'));
  jsonCount += 1;
}
check('owner_json_parse', jsonCount > 0, jsonCount);

const replayManifest = relative => {
  const manifest = JSON.parse(blob(relative).toString('utf8'));
  const mismatches = [];
  for (const entry of manifest.entries) {
    const bytes = blob(entry.path);
    if (bytes.length !== entry.bytes || sha(bytes) !== entry.sha256) mismatches.push(entry.path);
  }
  return { entries: manifest.entry_count, mismatches };
};
const x1Manifest = replayManifest('docs/ilyra-fen/v704-v4/x1/manifest.json');
const x2Manifest = replayManifest('docs/ilyra-fen/v704-v4/x2/manifest.json');
check('x1_manifest_replay', x1Manifest.entries === 25 && x1Manifest.mismatches.length === 0, x1Manifest);
check('x2_manifest_replay', x2Manifest.entries === 37 && x2Manifest.mismatches.length === 0, x2Manifest);

const seal = JSON.parse(blob('docs/ilyra-fen/v704-v4/final/content-seal.json').toString('utf8'));
const sealMismatches = [];
for (const entry of seal.entries) {
  const bytes = blob(entry.path);
  if (bytes.length !== entry.bytes || sha(bytes) !== entry.sha256) sealMismatches.push(entry.path);
}
check('content_seal_replay', seal.entry_count === seal.entries.length && sealMismatches.length === 0, { entries: seal.entry_count, mismatches: sealMismatches });

const batonBytes = blob('docs/ilyra-fen/v704-v4/final/handoff-baton.md');
const baton = batonBytes.toString('utf8');
const batonWords = baton.trim().split(/\s+/).length;
check('baton_word_minimum', batonWords >= 2000, batonWords);
check('baton_end_marker', baton.endsWith('END OF ILYRA FEN V704-V4 HANDOFF BATON\n'), baton.slice(-80));
const batonMetadata = JSON.parse(blob('docs/ilyra-fen/v704-v4/final/baton-metadata.json').toString('utf8'));
check('baton_metadata', batonMetadata.words === batonWords && batonMetadata.bytes === batonBytes.length && batonMetadata.sha256 === sha(batonBytes), batonMetadata);

const truth = JSON.parse(blob('docs/ilyra-fen/v704-v4/final/phase-truth.json').toString('utf8'));
check('truth_outcomes', JSON.stringify(truth.core_outcomes) === JSON.stringify({ completed: 255, represented: 15, open_gap: 15, exact_gate: 15 }), truth.core_outcomes);
check('truth_totals', JSON.stringify(truth.effective_totals) === JSON.stringify({ negatives: 64380, methods: 5746, failed_witnesses: 55545, passing_witnesses: 175796, witnesses: 231341, open_gaps: 1995, exact_gates: 2078 }), truth.effective_totals);
check('stage20_gate', truth.terminal_verdict === 'NOT_READY_FOR_STAGE_20', truth.terminal_verdict);
const route = JSON.parse(blob('docs/ilyra-fen/v704-v4/final/route-state.json').toString('utf8'));
check('route_prepared_not_sent', route.state === 'PREPARED_NOT_SENT' && route.acknowledgement === 'UNOBSERVED' && route.precontacted === false, route);

const changedPaths = text('diff-tree', '--no-commit-id', '--name-only', '-r', exactFinal).split(/\r?\n/).filter(Boolean);
check('final_delta_bounded', changedPaths.length > 0 && changedPaths.length < 100, changedPaths.length);
const privacyPatterns = [
  { id: 'credential_assignment', pattern: /\b(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}/i },
  { id: 'delegation_markup', pattern: /<codex_delegation>/i },
  { id: 'private_local_path', pattern: /(?:[A-Za-z]:\\Users\\[^\\\s]+|\/Users\/[^/\s]+)/ },
  { id: 'private_uri', pattern: /(?:file|vscode):\/\//i },
  { id: 'raw_uuid', pattern: /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/i },
];
const privacyHits = [];
for (const relative of ownerPaths.filter(relative => /\.(?:json|md|mjs|py|txt|html|ya?ml)$/.test(relative))) {
  const content = blob(relative).toString('utf8');
  for (const { id, pattern } of privacyPatterns) if (pattern.test(content)) privacyHits.push({ path: relative, class: id });
}
check('five_class_privacy_scan', privacyHits.length === 0, privacyHits);

const payload = {
  schema: 'ghc.family.exact-final-owner-scoped-canonical-receipt.v1',
  owner: 'Ilyra Fen', phase: 'v704-v4', state: 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',
  branch, exact_final: exactFinal, immutable_source: source, immutable_x1: x1, immutable_x2: x2,
  invocation_count: 1, success_count: 1, replay_count: 0,
  metadata_only: true,
  domain_harnesses_replayed: 0, test_tranches_replayed: 0, source_canonical_replayed: 0,
  check_count: checks.length, passed_checks: checks.filter(row => row.passed).length, failed_checks: checks.filter(row => !row.passed).length,
  owner_json_parses: jsonCount,
  x1_manifest_entries: x1Manifest.entries, x2_manifest_entries: x2Manifest.entries,
  content_seal_entries: seal.entry_count,
  baton_words: batonWords, baton_bytes: batonBytes.length, baton_sha256: sha(batonBytes),
  owner_files: ownerPaths.length, repository_files: allPaths.length, final_delta_entries: changedPaths.length,
  privacy_classes: privacyPatterns.map(row => row.id), privacy_hits: privacyHits,
  checks,
  same_owner_only: true, independent_reproduction: false, external_audit: false,
  terminal_verdict: 'NOT_READY_FOR_STAGE_20',
  boundary: 'Metadata-only exact-final owner-scoped canonical evidence under shared infrastructure. It is not a full-repository suite, domain replay, external audit, independent reproduction, empirical validation, production certification, complete privacy or accessibility assurance, exhaustive security, authority or Stage 20 evidence.',
};
payload.payload_sha256 = sha(Buffer.from(JSON.stringify(payload), 'utf8'));
fs.mkdirSync(path.dirname(receiptPath), { recursive: true });
fs.writeFileSync(receiptPath, JSON.stringify(payload, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ ok: true, state: payload.state, checks: payload.check_count, owner_json: jsonCount, x1_manifest: x1Manifest.entries, x2_manifest: x2Manifest.entries, content_seal: seal.entry_count, owner_files: ownerPaths.length, repository_files: allPaths.length, baton_words: batonWords, payload_sha256: payload.payload_sha256 }));
