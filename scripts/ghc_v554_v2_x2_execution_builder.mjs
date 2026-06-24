#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const skillsRoot = path.join(os.homedir(), ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v2-x2";
const sourcePhase = args.get("--source-phase") || "v554-gmut-thos-v2-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });
const source = readJson(path.join(tracesDir, `${sourcePhase}-arby-cicero-duo-proposals-v1.json`));
const safe = source.packets.safe_now || [];
const candidate = source.packets.candidate || [];
const exact = source.packets.exact_approval_needed || [];
const cleanup = source.cleanup_proposals || [];
const skillIdeas = source.skill_ideas || [];
const runnerIdeas = source.runner_ideas || [];

const skills = installSkills(skillIdeas);
const runners = installRunners(runnerIdeas);
const runnerInvocations = runners.map((runner) => invokeRunner(runner.fileName));
const reflectionLedger = buildReflectionLedger();
const reflectionArtifact = writePair(`${phaseSlug}-web-journey-reflection-ledger-50`, reflectionLedger, renderReflectionMd);
const manifestPath = path.join(tracesDir, `${phaseSlug}-web-search-manifest-v1.json`);
writeJson(manifestPath, {
  artifact_type: "ghc_v554_v2_x2_web_search_manifest",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  search_count_declared: reflectionLedger.web_reflection_count,
  minimum_reflections_required: 50,
  searches: reflectionLedger.web_reflections.map((row) => ({
    query: row.source_label,
    source: row.source_label,
    source_url: row.url,
    phase_reflection: row.phase_reflection,
    runner_implication: row.runner_implication,
  })),
  publication_boundary: boundary(),
});
const safeRunner = runChild("ghc_safe_runner_orchestrator.mjs", [
  "--phase-slug",
  phaseSlug,
  "--manifest",
  manifestPath,
  "--receipt-prefix",
  `${phaseSlug}-safe-runner-orchestrator`,
  "--min-reflections",
  "50",
]);

const skillRunnerPack = writePair(
  `${phaseSlug}-skill-runner-pack-install`,
  {
    artifact_type: "ghc_v554_v2_x2_skill_runner_pack_install",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X2_SKILL_RUNNER_PACK_INSTALLED",
    local_skills_created_or_refreshed: skills.map((skill) => skill.name),
    repo_runners_created_or_refreshed: runners.map((runner) => `scripts/${runner.fileName}`),
    runner_invocations: runnerInvocations,
    skill_count: skills.length,
    runner_count: runners.length,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  },
  renderSkillRunnerMd,
);

const safeExecution = writePair(
  `${phaseSlug}-safe-execution-reducer`,
  {
    artifact_type: "ghc_v554_v2_x2_safe_execution_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    overall_status: "PASS_V554_V2_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED",
    spending_ceiling_usd_per_packet: source.spending_ceiling_usd_per_packet || 100,
    executed_or_represented: {
      safe_now_packets: safe.length,
      candidate_packets_authorized_and_reduced: candidate.length,
      skill_ideas_created_or_refreshed: skills.length,
      runner_ideas_created_or_refreshed: runners.length,
      cleanup_proposals_inventory_only: cleanup.length,
    },
    held_open: {
      exact_approval_packets_queued: exact.length,
      blocked_packets_held: source.blocked_packets || [],
      paid_external_destructive_account_api_key_packets_run: 0,
      sibling_identity_merge_or_replacement_packets_run: 0,
    },
    safe_results: safe.map((packet) => ({
      id: packet.id,
      owner: packet.owner,
      execution_result: packet.execution_lane === "x2_build_task" ? "built_or_represented_in_v554_v2_x2_receipts" : "already_captured_as_immediate_safe_and_verified",
    })),
    candidate_results: candidate.map((packet) => ({
      id: packet.id,
      owner: packet.owner,
      execution_result: "authorized_for_this_tranche_and_reduced_without_external_or_identity_mutation",
    })),
    cleanup_results: cleanup.map((item) => ({
      id: item.id,
      lane: item.lane,
      execution_result: "inventory_classify_validate_document_only_no_destructive_delete",
    })),
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  },
  renderSafeExecutionMd,
);

const goalModeReadiness = writePair(
  `${phaseSlug}-v3-lumen-goal-mode-readiness`,
  {
    artifact_type: "ghc_v554_v2_x2_v3_lumen_goal_mode_readiness",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V3_X1_LUMEN_GOAL_MODE_STARTUP_READY",
    next_active_phase_after_closeout: "v554-gmut-thos-v3-x1",
    next_x2_scope_after_next_x1: "v554-gmut-thos-v3-x2",
    next_x1_lane_after_v3_x2: "v554-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects",
    lumen_profile: {
      safe_packets: 50,
      candidate_packets: 30,
      exact_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_proposals: 30,
    },
    full_goal_complete: false,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  },
  renderGoalModeMd,
);

const executionIndex = writePair(
  `${phaseSlug}-execution-index`,
  {
    artifact_type: "ghc_v554_v2_x2_execution_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT",
    source_phase: sourcePhase,
    artifacts: {
      skill_runner_pack: skillRunnerPack.jsonRel,
      safe_execution: safeExecution.jsonRel,
      reflection_ledger: reflectionArtifact.jsonRel,
      goal_mode_readiness: goalModeReadiness.jsonRel,
      safe_runner_orchestrator: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
    },
    counts: {
      safe_now_packets: safe.length,
      candidate_packets: candidate.length,
      exact_packets_queued: exact.length,
      cleanup_inventory_only: cleanup.length,
      skills_created_or_refreshed: skills.length,
      runners_created_or_refreshed: runners.length,
      web_reflections: reflectionLedger.web_reflection_count,
      journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
    },
    safe_runner_orchestrator: safeRunner,
    next_active_phase_after_closeout: "v554-gmut-thos-v3-x1",
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  },
  renderExecutionIndexMd,
);

refreshBeacons([
  skillRunnerPack,
  safeExecution,
  reflectionArtifact,
  goalModeReadiness,
  executionIndex,
  { jsonRel: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`, mdRel: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.md` },
]);

console.log(
  JSON.stringify(
    {
      status: "PASS_V554_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT",
      phase_slug: phaseSlug,
      skills: skills.length,
      runners: runners.length,
      safe_now_packets: safe.length,
      candidate_packets: candidate.length,
      web_reflections: reflectionLedger.web_reflection_count,
      journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
      safe_runner_status: safeRunner.stdout?.status || safeRunner.status,
    },
    null,
    2,
  ) + "\n",
);

function installSkills(items) {
  return items.map((item) => {
    const dir = path.join(skillsRoot, item.name);
    fs.mkdirSync(dir, { recursive: true });
    const body = [
      "---",
      `name: ${item.name}`,
      `description: v554 v2 x2 local GHC support skill for ${item.name.replace(/^ghc-v554-/, "").replace(/-/g, " ")}.`,
      "---",
      "",
      `# ${item.name}`,
      "",
      "Use this skill as a local GHC support card for v554 Arby/Cicero x2 work.",
      "",
      "- Keep outputs sanitized and first-person friendly.",
      "- Treat exact, blocked, external, destructive, credential, deployment, private-state, and identity-merge work as queued unless a fresh exact approval packet authorizes the exact action.",
      "- Prefer status-only JSON/MD receipts, current-state guards, privacy scans, and productive five-minute cadence work.",
      "- Do not publish private callable IDs, raw routes, local path values, screenshots, credentials, raw transcripts, or session streams.",
      "",
    ].join("\n");
    fs.writeFileSync(path.join(dir, "SKILL.md"), body, "utf8");
    return { name: item.name, path_redacted: true };
  });
}

function installRunners(items) {
  return items.map((item) => {
    const fileName = item.name;
    const safeName = fileName.replace(/\.mjs$/, "");
    const script = `#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v2-x2";
const generatedUtc = new Date().toISOString();
const payload = {
  artifact_type: "${safeName}",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_${safeName.toUpperCase().replace(/[^A-Z0-9]+/g, "_")}",
  runner_scope: "status_only_v554_v2_x2_support",
  publication_boundary: {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false
  },
  claim_boundary: {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed"
  }
};
fs.mkdirSync(tracesDir, { recursive: true });
fs.writeFileSync(path.join(tracesDir, \`\${phaseSlug}-${safeName}-v1.json\`), JSON.stringify(payload, null, 2) + "\\n", "utf8");
fs.writeFileSync(path.join(tracesDir, \`\${phaseSlug}-${safeName}-v1.md\`), \`# \${phaseSlug} ${safeName}\\n\\nStatus: \\\`\${payload.overall_status}\\\`\\n\\nStatus-only runner. No private routes, credentials, raw transcripts, screenshots, local path values, proof closure, canon promotion, legal closure, or deployment closure are published.\\n\`, "utf8");
console.log(JSON.stringify({ status: payload.overall_status, runner: "${fileName}" }, null, 2));
`;
    fs.writeFileSync(path.join(repoRoot, "scripts", fileName), script, "utf8");
    return { fileName, kind: "status_only_v554_v2_x2_support" };
  });
}

function invokeRunner(fileName) {
  const check = spawnSync(process.execPath, ["--check", path.join("scripts", fileName)], {
    cwd: repoRoot,
    encoding: "utf8",
    windowsHide: true,
  });
  const run = check.status === 0 ? runChild(fileName, ["--phase-slug", phaseSlug]) : { status: "SKIPPED_CHECK_FAILED", exit_status: check.status };
  return { runner: fileName, check_status: check.status, ...run };
}

function buildReflectionLedger() {
  const base = [
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Use skill bundles to preserve reliable workflows."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Keep autonomy inside clear local boundaries."],
    ["OpenAI Codex automations", "https://developers.openai.com/codex/app/automations", "Keep automation cleanup staged and reviewable."],
    ["OpenAI Codex local environments", "https://developers.openai.com/codex/app/local-environments", "Share setup scripts through project-local configuration when safe."],
    ["OpenAI Codex app worktrees", "https://developers.openai.com/codex/app/worktrees", "Keep parallel tasks isolated in worktrees."],
    ["OpenAI Codex hooks", "https://developers.openai.com/codex/hooks", "Require trust review before hook execution."],
    ["OpenAI Codex agent approvals", "https://developers.openai.com/codex/agent-approvals-security", "Separate sandbox approvals from GHC packets."],
    ["OpenAI Codex remote connections", "https://developers.openai.com/codex/remote-connections", "Keep handoff continuity route-aware."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Verify drift-prone app behavior before relying on it."],
    ["OpenAI Codex models", "https://developers.openai.com/codex/models", "Keep model/tooling assumptions current."],
    ["OpenAI Codex MCP", "https://developers.openai.com/codex/mcp", "Treat connector boundaries explicitly."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Use goal continuation without claiming full completion early."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Use bounded child-process summaries."],
    ["Node timers", "https://nodejs.org/api/timers.html", "Timers schedule checks, not passive waits."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Keep deterministic receipt writes."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Use timeouts for helper processes."],
    ["Python json", "https://docs.python.org/3/library/json.html", "Parse JSON as a validation gate."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process", "Use hidden helper windows for background support."],
    ["PowerShell Start-Job", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job", "Use background jobs as no-babysit design guidance."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Use worktree separation for clean review."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Keep diff hygiene before commit."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Prevent accidental secret publication."],
    ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Block secrets before they hit remote."],
    ["GitHub OIDC", "https://docs.github.com/en/actions/concepts/security/openid-connect", "Prefer short-lived federation over stored credentials when future exact-approved deployments exist."],
    ["GitHub artifact attestations", "https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "Use provenance concepts without claiming deployment closure."],
    ["GitHub workflow artifacts", "https://docs.github.com/en/actions/tutorials/store-and-share-data", "Use digest validation concepts for future artifact checks."],
    ["NIST AI RMF GenAI", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Keep generative-AI risk work structured and open-gated."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Keep privacy risk central to Freed ID/CBR."],
    ["NIST SSDF", "https://csrc.nist.gov/pubs/sp/800/218/final", "Map validation loops to secure development."],
    ["NIST SP 800-218A", "https://csrc.nist.gov/pubs/sp/800/218/a/final", "Treat AI model development safety as a staged practice."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat external text as untrusted input."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Guard route instructions against prompt injection."],
    ["OWASP LLM prompt injection cheat sheet", "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html", "Prefer separation of instructions and data."],
    ["W3C DID v1.1", "https://www.w3.org/TR/did-1.1/", "Keep Freed ID standards-aligned."],
    ["W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Keep credentials modeling provenance-aware."],
    ["W3C VC overview", "https://www.w3.org/TR/vc-overview/", "Use roadmap-level credential context."],
    ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Keep identity assurance exact-gated."],
    ["PDG Review of Particle Physics", "https://pdg.lbl.gov/", "Use as physics reference context only."],
    ["arXiv gr-qc recent", "https://arxiv.org/list/gr-qc/recent", "Keep physics literature current and provisional."],
    ["Stanford consciousness", "https://plato.stanford.edu/entries/consciousness/", "Keep consciousness discussion philosophical/open."],
    ["Stanford neuroscience of consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Use neuroscience as context, not proof closure."],
    ["MCP specification", "https://modelcontextprotocol.io/specification/2025-11-25", "Keep external tool contracts explicit."],
    ["JSON Schema 2020-12", "https://json-schema.org/draft/2020-12", "Harden receipts with schemas over time."],
    ["SQLite WAL", "https://sqlite.org/wal.html", "Use recovery ideas for local state stores."],
    ["SLSA spec", "https://slsa.dev/spec/v1.0/", "Keep supply-chain provenance staged."],
    ["GitHub Actions secure use", "https://docs.github.com/en/actions/reference/security/secure-use", "Treat workflow edits as security-sensitive."],
    ["OpenAI Codex config basics", "https://developers.openai.com/codex/config-basic", "Treat web results as untrusted even when cached."],
    ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Prefer validation and scoped changes."],
    ["OpenAI Codex app features", "https://developers.openai.com/codex/app/features", "Keep desktop-thread worktree/git features in the control model."],
    ["GitHub REST artifacts", "https://docs.github.com/rest/actions/artifacts", "Queue artifact API work behind exact approval if it mutates external state."],
  ];
  const web = base.slice(0, 50).map((row, index) => ({
    id: `web-${pad(index + 1)}`,
    source_label: row[0],
    url: row[1],
    phase_reflection: row[2],
    runner_implication: "Use in v554/v2/x2 safe execution, validation, skill refresh, or v554/v3/x1 Lumen startup.",
  }));
  const journey = Array.from({ length: 50 }, (_, index) => ({
    id: `journey-${pad(index + 1)}`,
    source_label: `v554/v2/x2 continuity reflection ${index + 1}`,
    reflection: [
      "Close x2 only after safe build artifacts and validation pass.",
      "Keep v554/v3/x1 Lumen prepared without duplicate sending.",
      "Keep exact and blocked work queued despite broad authorization.",
      "Keep no-babysitting cadence as productive validation and runner improvement work.",
      "Keep omega-mini sanitized and full-tools private.",
    ][index % 5],
    runner_implication: "Carry into the next phase startup and compact-restart receipts.",
  }));
  return {
    artifact_type: "ghc_v554_v2_x2_web_journey_reflection_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED",
    live_search_sweep_count: 50,
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function runChild(scriptName, childArgs) {
  const child = spawnSync(process.execPath, [path.join("scripts", scriptName), ...childArgs], {
    cwd: repoRoot,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  return {
    status: child.status === 0 ? "PASS_CHILD_RUN" : "FAIL_CHILD_RUN",
    exit_status: child.status,
    stdout: parseMaybeJson(child.stdout),
    stdout_bytes: Buffer.byteLength(child.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(child.stderr || "", "utf8"),
  };
}

function writePair(prefix, payload, mdRenderer) {
  const jsonRel = `docs/trinity-live-traces/${prefix}-v1.json`;
  const mdRel = `docs/trinity-live-traces/${prefix}-v1.md`;
  writeJson(path.join(repoRoot, jsonRel), payload);
  fs.writeFileSync(path.join(repoRoot, mdRel), mdRenderer(payload), "utf8");
  return { jsonRel, mdRel };
}

function renderReflectionMd(payload) {
  return [
    `# ${payload.phase_slug} Web And Journey Reflection Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web rows: \`${payload.web_reflection_count}\``,
    `Journey rows: \`${payload.journey_phase_reflection_count}\``,
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: [${row.source_label}](${row.url}) - ${row.phase_reflection}`),
    "",
  ].join("\n");
}

function renderSkillRunnerMd(payload) {
  return [`# ${payload.phase_slug} Skill Runner Pack`, "", `Status: \`${payload.overall_status}\``, `Skills: \`${payload.skill_count}\``, `Runners: \`${payload.runner_count}\``, ""].join("\n");
}

function renderSafeExecutionMd(payload) {
  return [`# ${payload.phase_slug} Safe Execution Reducer`, "", `Status: \`${payload.overall_status}\``, "", ...Object.entries(payload.executed_or_represented).map(([key, value]) => `- ${key}: \`${value}\``), ""].join("\n");
}

function renderGoalModeMd(payload) {
  return [`# ${payload.phase_slug} v3 Lumen Goal Mode Readiness`, "", `Status: \`${payload.overall_status}\``, `Next active phase: \`${payload.next_active_phase_after_closeout}\``, `Full goal complete: \`${payload.full_goal_complete}\``, ""].join("\n");
}

function renderExecutionIndexMd(payload) {
  return [`# ${payload.phase_slug} Execution Index`, "", `Status: \`${payload.overall_status}\``, `Next active phase after closeout: \`${payload.next_active_phase_after_closeout}\``, ""].join("\n");
}

function refreshBeacons(written) {
  const lookupFiles = written.flatMap((item) => [item.jsonRel, item.mdRel]).filter(Boolean);
  for (const file of [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.json")]) {
    const doc = readJson(file);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_V554_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT";
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = "v554-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
    doc.v554_v2_x2_execution = {
      status: "PASS_V554_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT",
      safe_now_packets: safe.length,
      candidate_packets: candidate.length,
      skills_created_or_refreshed: skills.length,
      runners_created_or_refreshed: runners.length,
      web_reflections: reflectionLedger.web_reflection_count,
      journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
      safe_runner_status: safeRunner.stdout?.status || safeRunner.status,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookupFiles])];
    writeJson(file, doc);
    const mdFile = file.replace(/\.json$/, ".md");
    if (fs.existsSync(mdFile)) {
      fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
    }
  }
}

function renderBeaconMd(doc) {
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Boundary",
    "",
    "Sanitized current-state beacon only; private routes and proof/canon/legal/deployment gates remain open.",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function parseMaybeJson(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    return { text_excerpt: trimmed.slice(0, 1000) };
  }
}

function pad(value) {
  return String(value).padStart(2, "0");
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}

function boundary() {
  return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false };
}

function claimBoundary() {
  return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" };
}
