import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.resolve(process.argv[2] || process.cwd());
const phase = path.join(root, 'docs', 'ilyra-fen', 'v704-v4', 'x2');
const out = path.join(phase, 'installations');
const userProfile = process.env.USERPROFILE;
if (!userProfile) throw new Error('USERPROFILE is required');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const shaFile = file => sha(fs.readFileSync(file));
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', 'utf8');
};
const boundary = 'Finite synthetic same-owner software and installation evidence only. No live hook observation, independent reproduction, empirical confirmation, authority or Stage 20 promotion. NOT_READY_FOR_STAGE_20.';

const skillNames = [
  'ghc-family-rectangular-relaxation-comparison',
  'ghc-family-rectangularity-gap-certificate',
  'ghc-family-model-deletion-sensitivity',
  'ghc-family-state-relabel-covariance',
  'ghc-family-discount-zero-certificate',
  'ghc-family-mixture-representation-boundary',
  'ghc-family-calibration-evidence-gap',
  'ghc-family-uncertainty-authority-gate',
  'ghc-family-accessible-coupled-model-summary',
  'ghc-family-uncertainty-scene-coordinates',
];
const skillRecords = skillNames.map(name => {
  const source = path.join(phase, 'skills', name, 'SKILL.md');
  const discovery = path.join(userProfile, '.codex', 'skills', name, 'SKILL.md');
  if (!fs.existsSync(source) || !fs.existsSync(discovery)) throw new Error(`missing skill entrypoint ${name}`);
  const sourceHash = shaFile(source);
  const discoveryHash = shaFile(discovery);
  if (sourceHash !== discoveryHash) throw new Error(`skill parity mismatch ${name}`);
  return {
    skill: name,
    global_discovery: 'C essential directory junction to D-first owner payload',
    source_path: `docs/ilyra-fen/v704-v4/x2/skills/${name}`,
    source_skill_sha256: sourceHash,
    entrypoint_parity: true,
    official_skill_creator_validation: 'passed',
  };
});
writeJson(path.join(out, 'global-skills.json'), {
  schema: 'ghc.family.global-skill-installation.v1',
  owner: 'Ilyra Fen', phase: 'v704-v4',
  installed_skills: skillRecords.length,
  payload_storage: 'D-first',
  c_discovery_entries: 'ten directory junctions',
  collision_count: 0,
  source_entrypoints_removed: 0,
  records: skillRecords,
  scope: 'Observed additive discovery installs and entrypoint parity only; no whole-inventory equivalence claim.',
  boundary,
});

const pluginName = 'ghc-family-ilyra-coupled-workflow-hooks';
const sourceRoot = path.join(phase, 'plugins', pluginName);
const personalRoot = path.join(userProfile, 'plugins', pluginName);
const cacheRoot = path.join(userProfile, '.codex', 'plugins', 'cache', 'personal', pluginName, '1.0.0');
const relatives = ['.codex-plugin/plugin.json', 'hooks/hooks.json', 'README.md', 'scripts/advisories.txt'];
const files = relatives.map(relative => {
  const source = path.join(sourceRoot, relative);
  const personal = path.join(personalRoot, relative);
  const cache = path.join(cacheRoot, relative);
  for (const file of [source, personal, cache]) if (!fs.existsSync(file)) throw new Error(`missing plugin file ${relative}`);
  const sourceHash = shaFile(source), personalHash = shaFile(personal), cacheHash = shaFile(cache);
  if (sourceHash !== personalHash || sourceHash !== cacheHash) throw new Error(`plugin parity mismatch ${relative}`);
  return { relative: relative.replaceAll('\\', '/'), bytes: fs.statSync(source).size, sha256: sourceHash };
});
const marketplace = path.join(userProfile, '.agents', 'plugins', 'marketplace.json');
const marketplacePayload = JSON.parse(fs.readFileSync(marketplace, 'utf8'));
const entry = marketplacePayload.plugins.find(row => row.name === pluginName);
if (!entry || entry.source?.path !== `./plugins/${pluginName}`) throw new Error('plugin marketplace entry mismatch');
const smokes = JSON.parse(fs.readFileSync(path.join(phase, 'hook-smokes.json'), 'utf8'));
writeJson(path.join(out, 'plugin.json'), {
  schema: 'ghc.family.plugin-installation.v1',
  owner: 'Ilyra Fen', phase: 'v704-v4',
  plugin_name: pluginName,
  marketplace_name: marketplacePayload.name,
  cli_exit: 0,
  installed_source_parity: true,
  installed_cache_parity: true,
  files,
  hook_count: 10,
  manual_smokes: smokes.check_count,
  manual_smokes_passed: smokes.passed,
  previous_marketplace_entries_preserved: marketplacePayload.plugins.filter(row => row.name !== pluginName).length === 2,
  marketplace_before_sha256: '29161df90f12c2b31aa0fa6b0cbb7b3223142be93a1a03962b53d6d9f0bc804a',
  marketplace_after_sha256: shaFile(marketplace),
  live_hook_execution: 'open_gap until an eligible new event is observed',
  trust_state: 'native installer result retained; no separate trust observation inferred',
  c_storage_exception: 'Essential personal source, marketplace, discovery junctions and managed cache; primary authored source and evidence remain on D.',
  raw_native_payload_published: false,
  boundary,
});
console.log(JSON.stringify({ ok: true, skills: skillRecords.length, plugin_files: files.length, hook_smokes: smokes.passed, marketplace_entries: marketplacePayload.plugins.length }));
