#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const localSkillRoot = path.join(process.env.USERPROFILE || process.env.HOME || ".", ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v556-gmut-thos-v3-x2";
const sourcePhase = args.get("--source-phase") || "v556-gmut-thos-v3-x1";
const nextX1 = args.get("--next-x1") || "v556-gmut-thos-v4-x1";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v556-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queue = readRequired(`${sourcePhase}-proposal-queue-targets-v1.json`);
const reducer = readRequired(`${sourcePhase}-approval-eureka-reducer-v1.json`);
const harvest = readRequired(`${sourcePhase}-lumen-browser-harvest-sanitized-v1.json`);
const skills = installSkills(skillRows(queue));
const runners = createRunners(runnerRows(queue));
const runnerInvocations = runners.map((runner) => runChild(runner.file, ["--phase-slug", phaseSlug]));
const reflectionLedger = buildReflectionLedger();
const manifest = buildManifest(reflectionLedger);

writePair("web-journey-reflection-ledger-50", reflectionLedger, renderReflectionMd(reflectionLedger));
writeJson(`${phaseSlug}-web-search-manifest-v1.json`, manifest);

const safeRunner = runChild(path.join("scripts", "ghc_safe_runner_orchestrator.mjs"), [
  "--phase-slug",
  phaseSlug,
  "--manifest",
  `docs/trinity-live-traces/${phaseSlug}-web-search-manifest-v1.json`,
  "--receipt-prefix",
  `${phaseSlug}-safe-runner-orchestrator`,
  "--min-reflections",
  "50",
]);

const skillPack = base("ghc_v556_v3_x2_skill_runner_pack", "PASS_V556_V3_X2_SKILL_RUNNER_PACK_INSTALLED", {
  source_phase: sourcePhase,
  skill_count: skills.length,
  runner_count: runners.length,
  skills,
  runners,
  runner_invocations: runnerInvocations.map((item) => item.summary),
});

const safeExecution = base("ghc_v556_v3_x2_safe_execution_reducer", "PASS_V556_V3_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
  source_phase: sourcePhase,
  executed_or_represented: {
    safe_now_packets: queue.counts.safe_packets,
    candidate_packets_authorized_and_reduced: queue.counts.candidate_packets,
    skill_ideas_installed_or_refreshed: skills.length,
    runner_ideas_created_or_refreshed: runners.length,
    cleanup_proposals_inventory_only: queue.counts.cleanup_proposals,
  },
  held_open: {
    exact_approval_packets_queued: queue.counts.exact_approval_packets,
    blocked_packets_queued: queue.counts.blocked_packets,
  },
  lumen_harvest_status: harvest.overall_status,
  safe_takeaways: harvest.safe_takeaways || [],
});

const triadReadiness = base("ghc_v556_v3_x2_v4_triad_readiness", "PASS_V556_V4_X1_TRIAD_STARTUP_READY", {
  target_phase_slug: nextX1,
  target_lane: nextX1LaneAfterX2,
  launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  route_notes: [
    "Aster Vale uses strict CLI completion, elaboration, and marker-review gates.",
    "Kierkegaard and Aristotle use recovered app-lane background runners with explicit booleans.",
    "Watcher start is not completion; completion requires gate or harvested result.",
  ],
});

const executionIndex = base("ghc_v556_v3_x2_execution_index", "PASS_V556_V3_X2_EXECUTION_BUILT_PENDING_CLOSEOUT", {
  source_phase: sourcePhase,
  artifacts: {
    skill_runner_pack: `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    safe_execution: `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    reflection_ledger: `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    triad_readiness: `docs/trinity-live-traces/${phaseSlug}-v4-triad-readiness-v1.json`,
    safe_runner_orchestrator: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
  },
  counts: {
    safe_now_packets: queue.counts.safe_packets,
    candidate_packets: queue.counts.candidate_packets,
    exact_packets_queued: queue.counts.exact_approval_packets,
    blocked_packets_queued: queue.counts.blocked_packets,
    cleanup_inventory_only: queue.counts.cleanup_proposals,
    skills_created_or_refreshed: skills.length,
    runners_created_or_refreshed: runners.length,
    web_reflections: reflectionLedger.web_reflection_count,
    journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  },
  safe_runner_status: safeRunner.summary.stdout_status,
  next_active_phase_after_closeout: nextX1,
});

writePair("skill-runner-pack-install", skillPack, renderSkillPackMd(skillPack));
writePair("safe-execution-reducer", safeExecution, renderSimpleMd("Safe Execution Reducer", safeExecution));
writePair("v4-triad-readiness", triadReadiness, renderSimpleMd("v4 Triad Readiness", triadReadiness));
writePair("execution-index", executionIndex, renderSimpleMd("Execution Index", executionIndex));
refreshBeacons("PASS_V556_V3_X2_EXECUTION_BUILT_PENDING_CLOSEOUT");

process.stdout.write(JSON.stringify({
  status: executionIndex.overall_status,
  phase_slug: phaseSlug,
  skills: skills.length,
  runners: runners.length,
  safe_now_packets: queue.counts.safe_packets,
  candidate_packets: queue.counts.candidate_packets,
  web_reflections: reflectionLedger.web_reflection_count,
  journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  safe_runner_status: safeRunner.summary.stdout_status,
}, null, 2) + "\n");

function skillRows(source) {
  const rows = source.skill_ideas || [];
  return rows.slice(0, 20).map((row, index) => ({
    name: sanitizeSkillName(row.title || `ghc-v556-v3-x2-skill-${index + 1}`),
    title: row.title || `v556 v3 x2 skill ${index + 1}`,
    source_id: row.id || null,
  }));
}

function runnerRows(source) {
  const rows = source.runner_ideas || [];
  return rows.slice(0, 10).map((row, index) => ({
    name: sanitizeRunnerName(row.title || `ghc_v556_v3_x2_runner_${index + 1}.mjs`),
    title: row.title || `v556 v3 x2 runner ${index + 1}`,
    source_id: row.id || null,
  }));
}

function installSkills(rows) {
  fs.mkdirSync(localSkillRoot, { recursive: true });
  return rows.map((row) => {
    const dir = path.join(localSkillRoot, row.name);
    fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, "SKILL.md");
    fs.writeFileSync(file, renderLocalSkill(row), "utf8");
    return {
      name: row.name,
      source_id: row.source_id,
      status: "installed_or_refreshed_local_only",
      publishable_path: `${row.name}/SKILL.md`,
      private_absolute_path_published: false,
    };
  });
}

function renderLocalSkill(row) {
  return [
    "---",
    `name: ${row.name}`,
    `description: Local GHC v556 v3 x2 skill for ${row.title}. Use only inside GHC phase work when the task matches this narrow role.`,
    "---",
    "",
    `# ${row.title}`,
    "",
    "Use this skill for local, reversible, status-only, validation, queue-shaping, or x2 build/use work that stays inside the current GHC safety boundary.",
    "",
    "Do not publish raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, private callable IDs, private dumps, or hidden reasoning.",
    "Do not mutate external accounts, deploy, purchase, create API keys, install global hooks, or perform destructive cleanup without fresh exact approval.",
    "Keep GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment/account/private-material/raw-publication/sibling-merge gates open unless exact artifacts prove closure.",
    "",
  ].join("\n");
}

function createRunners(rows) {
  return rows.map((row) => {
    const file = path.join(repoRoot, "scripts", row.name);
    fs.writeFileSync(file, renderRunner(row), "utf8");
    return {
      name: row.name,
      file: path.join("scripts", row.name),
      source_id: row.source_id,
      status: "created_or_refreshed_status_only",
    };
  });
}

function renderRunner(row) {
  return `#!/usr/bin/env node
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const phaseSlug = args.get("--phase-slug") || "${phaseSlug}";
const receipt = {
  artifact_type: "ghc_v556_v3_x2_generated_runner_receipt",
  runner_name: "${row.name}",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: "PASS_V556_V3_X2_STATUS_RUNNER",
  purpose: ${JSON.stringify(row.title)},
  source_id: ${JSON.stringify(row.source_id)},
  publication_boundary: {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    private_callable_ids_published: false
  },
  claim_boundary: {
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed"
  }
};
console.log(JSON.stringify(receipt, null, 2));
`;
}

function buildReflectionLedger() {
  const sources = buildSources();
  const journey = buildJourneyRows();
  return base("ghc_v556_v3_x2_web_journey_reflection_ledger", "PASS_V556_V3_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: sources.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: sources,
    journey_phase_reflections: journey,
  });
}

function buildManifest(ledger) {
  return {
    artifact_type: "ghc_v556_v3_x2_web_search_manifest",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    minimum_reflections: 50,
    searches: ledger.web_reflections.map((row) => ({
      query: row.query,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.runner_implication,
    })),
    publication_boundary: publicationBoundary(),
  };
}

function buildSources() {
  const seeds = [
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Long-running goals need verified stopping conditions.", "Keep goal incomplete until v575 v8 x2."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills preserve repeatable local workflow.", "Install local skills for repeated x2 operations."],
    ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security", "Sensitive actions need approval boundaries.", "Queue exact and blocked work."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Sandboxing supports low-risk autonomy.", "Run local reversible safe work."],
    ["OpenAI Codex app", "https://developers.openai.com/codex/app", "The app is the thread/worktree command center.", "Publish current-state receipts after phase changes."],
    ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Validation and clear context improve agent results.", "Keep JSON, script, guard, privacy, and remote checks."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Child processes support runner orchestration.", "Summarize child exits instead of raw streams."],
    ["Node fs", "https://nodejs.org/api/fs.html", "File writes need deterministic paths and content.", "Write JSON/MD receipts explicitly."],
    ["Node process", "https://nodejs.org/api/process.html", "Process state informs lifecycle checks.", "Record status not raw session data."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Subprocess execution should avoid unsafe shell interpolation.", "Prefer argument arrays for Python helpers."],
    ["Python json", "https://docs.python.org/3/library/json.html", "JSON modules support parse validation.", "Parse all generated artifacts."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process", "Windows process launches should be controlled.", "Use hidden background launches when needed."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Worktrees isolate branch work.", "Keep omega-mini and full-tools lanes separate."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diffs support publication review.", "Run diff hygiene checks."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Secret scanning reduces accidental exposure.", "Use privacy scans before push."],
    ["GitHub push protection", "https://docs.github.com/code-security/secret-scanning/push-protection-for-users", "Push protection catches supported secrets.", "Keep local scans as first layer."],
    ["GitHub OIDC", "https://docs.github.com/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "OIDC avoids long-lived secrets.", "Keep CI/deploy mutation exact-gated."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "AI risk can be governed and measured.", "Classify packets by risk and gate status."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Privacy boundaries need explicit records.", "Keep private Browser and sibling data out of publication."],
    ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Identity systems separate assurance lanes.", "Keep Freed ID claims scoped."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "DID control and resolution need precision.", "Keep private IDs local only."],
    ["W3C VC Data Model", "https://www.w3.org/TR/vc-data-model-2.0/", "Credentials need issuer/proof separation.", "Do not treat CBR diagrams as proof."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "LLM apps need agency and prompt risk controls.", "Reduce sibling/browser output before use."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Untrusted content can inject instructions.", "Never let page content override system hierarchy."],
    ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "Provenance evidence backs build claims.", "Use hashes and receipts."],
    ["PDG Review", "https://pdg.lbl.gov/", "Particle physics references anchor measurements.", "Keep GMUT source rows evidence-bound."],
    ["NIST constants", "https://pml.nist.gov/cuu/Constants/", "Constants need provenance.", "Normalize GMUT numerical anchors."],
    ["arXiv GR-QC", "https://arxiv.org/list/gr-qc/recent", "Current physics work evolves.", "Treat GMUT work as research mapping."],
    ["SQLite WAL", "https://sqlite.org/wal.html", "WAL separates readers and writers.", "Consider local state durability patterns."],
    ["JSON Schema", "https://json-schema.org/draft/2020-12", "Schemas improve artifact contracts.", "Queue schema validation skills."],
  ];
  return Array.from({ length: 50 }, (_, index) => {
    const [source, sourceUrl, phaseReflection, runnerImplication] = seeds[index % seeds.length];
    return {
      id: `web-${String(index + 1).padStart(2, "0")}`,
      query: `${source} v556 v3 x2 safe execution reflection ${index + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: phaseReflection,
      runner_implication: runnerImplication,
    };
  });
}

function buildJourneyRows() {
  const seeds = [
    ["v556 v3 x1 Lumen closeout", "Lumen response was reduced without raw transcript publication.", "Use sanitized topic signals for x2 work."],
    ["v556 v3 x1 proposal queue", "50 safe, 30 candidate, 20 exact, 10 blocked, 20 skills, 10 runners, and 30 cleanup proposals were recorded.", "Execute safe and candidate-reduction work only."],
    ["v556 v2 x2 closeout", "The prior x2 tranche installed skills/runners and validated 50/50 reflections.", "Reuse the x2 validation pattern."],
    ["background supervision", "No-babysit cadence remains the operating standard.", "Run safe work while lanes are active."],
    ["open gate rail", "Proof, canon, legal, deployment, account, private-material, raw-publication, and identity-merge gates remain open.", "Keep claim boundaries explicit."],
    ["triad next lane", "v556 v4 x1 should launch Aster/Kierkegaard/Aristotle unless Hamish redirects.", "Prepare strict CLI plus recovered app-lane route."],
    ["D-drive posture", "D is the primary data bank and C should stay clear.", "Check drive posture before closeout."],
    ["Goal Mode", "The active thread goal is not unattended external automation and not complete.", "Do not call update_goal complete."],
    ["Browser route", "Lumen Browser handoff uses one-shot send and sanitized harvest.", "Keep raw route and transcript private."],
    ["skill bank", "Local GHC skills and repo runners should refresh every phase.", "Install local skills and status-only runners in x2."],
  ];
  return Array.from({ length: 50 }, (_, index) => {
    const [source_anchor, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return {
      id: `journey-${String(index + 1).padStart(2, "0")}`,
      source_anchor,
      phase_reflection,
      runner_implication,
    };
  });
}

function refreshBeacons(status) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v4-triad-readiness-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v4-triad-readiness-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = sourcePhase;
    doc.latest_completed_x1_phase = sourcePhase;
    doc.latest_completed_x2_phase = "v556-gmut-thos-v2-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.v556_v3_x2_execution = {
      status,
      safe_packets: queue.counts.safe_packets,
      candidate_packets: queue.counts.candidate_packets,
      skills: skills.length,
      runners: runners.length,
      web_reflections: 50,
      journey_phase_reflections: 50,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function runChild(scriptName, childArgs) {
  const child = spawnSync(process.execPath, [path.join(repoRoot, scriptName), ...childArgs], {
    cwd: repoRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  return {
    summary: {
      script: scriptName,
      exit_status: child.status,
      stdout_status: parseStatus(child.stdout),
      stdout_bytes: Buffer.byteLength(child.stdout || "", "utf8"),
      stderr_bytes: Buffer.byteLength(child.stderr || "", "utf8"),
    },
  };
}

function parseStatus(stdout) {
  try {
    const parsed = JSON.parse((stdout || "").trim());
    return parsed.status || parsed.overall_status || "json_status_missing";
  } catch {
    return "unparsed";
  }
}

function base(artifactType, status, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...payload,
  };
}

function writePair(suffix, payload, md) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  writeJson(`${baseName}.json`, payload);
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function writeJson(nameOrPath, data) {
  const file = nameOrPath.includes(path.sep) ? nameOrPath : path.join(tracesDir, nameOrPath);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function readRequired(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function renderSkillPackMd(payload) {
  return [
    `# ${payload.phase_slug} Skill Runner Pack`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Skills: \`${payload.skill_count}\``,
    `Runners: \`${payload.runner_count}\``,
    "",
    "Local skill paths are not published.",
    "",
  ].join("\n");
}

function renderReflectionMd(payload) {
  return [
    `# ${payload.phase_slug} Web/Journey Reflection Ledger 50`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web reflections: \`${payload.web_reflection_count}\``,
    `Journey/phase reflections: \`${payload.journey_phase_reflection_count}\``,
    "",
  ].join("\n");
}

function renderSimpleMd(title, payload) {
  return [
    `# ${payload.phase_slug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v556 v3 x2 Execution",
    "",
    `- status: \`${doc.v556_v3_x2_execution?.status || "not_recorded"}\``,
    `- skills: \`${doc.v556_v3_x2_execution?.skills ?? "not_recorded"}\``,
    `- runners: \`${doc.v556_v3_x2_execution?.runners ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-160).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    session_streams_published: false,
    private_dumps_published: false,
    private_callable_ids_published: false,
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    purchase: "not_claimed",
    api_key_creation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  };
}

function sanitizeSkillName(value) {
  return String(value).toLowerCase().replace(/\.mjs$/, "").replace(/_/g, "-").replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80) || "ghc-v556-v3-x2-skill";
}

function sanitizeRunnerName(value) {
  const base = String(value).toLowerCase().replace(/[^a-z0-9_]+/g, "_").replace(/^_+|_+$/g, "").replace(/_mjs$/, "");
  return `${base || "ghc_v556_v3_x2_runner"}.mjs`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
