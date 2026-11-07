'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { verifyRelease } = require('./verify-release.cjs');

function checkTrinityMandala(directory = __dirname) {
  const releaseCheck = verifyRelease(directory);
  const manifestPath = path.join(directory, 'trinity-mandala-manifest.json');
  const onboardingPath = path.join(directory, 'GEMINI-ARGON-4-ONBOARDING.md');

  const errors = [...releaseCheck.errors];
  let manifest = null;
  let manifestSha256 = null;
  let onboardingSha256 = null;

  try {
    const raw = fs.readFileSync(manifestPath);
    manifestSha256 = createHash('sha256').update(raw).digest('hex');
    manifest = JSON.parse(raw.toString('utf8'));
    if (manifest.schema !== 'ghc.trinity-mandala.public-manifest.v1') {
      errors.push('TRINITY_SCHEMA');
    }
    const pillarKeys = Object.keys(manifest.pillars || {});
    if (!['gmut', 'thos', 'freedIdAndCbr'].every((k) => pillarKeys.includes(k))) {
      errors.push('TRINITY_PILLARS');
    }
    const agentIds = (manifest.continuityAgents || []).map((a) => a.id);
    if (!['antigravity', 'antigravity-subagent', 'gemini-argon-4'].every((id) => agentIds.includes(id))) {
      errors.push('TRINITY_CONTINUITY_AGENTS');
    }
  } catch {
    errors.push('TRINITY_MANIFEST_READ');
  }

  try {
    const onboardingRaw = fs.readFileSync(onboardingPath);
    onboardingSha256 = createHash('sha256').update(onboardingRaw).digest('hex');
  } catch {
    errors.push('ONBOARDING_READ');
  }

  return {
    ok: releaseCheck.ok && errors.length === 0,
    releaseVerified: releaseCheck.ok,
    checkedEvidenceFiles: releaseCheck.checked,
    trinityPillars: manifest ? Object.keys(manifest.pillars) : [],
    continuityAgents: manifest ? manifest.continuityAgents.map((a) => a.id) : [],
    trinityManifestSha256: manifestSha256,
    onboardingSha256,
    errors
  };
}

module.exports = { checkTrinityMandala };
if (require.main === module) {
  const result = checkTrinityMandala(__dirname);
  process.stdout.write(JSON.stringify(result) + '\n');
  process.exitCode = result.ok ? 0 : 1;
}
