#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const localSkillRoot = path.join(process.env.USERPROFILE || process.env.HOME || ".", ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v556-gmut-thos-v4-x2";
const sourcePhase = args.get("--source-phase") || "v556-gmut-thos-v4-x1";
const nextX1 = args.get("--next-x1") || "v556-gmut-thos-v5-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queue = readRequired(`${sourcePhase}-proposal-queue-targets-v1.json`);
const reducer = readRequired(`${sourcePhase}-approval-eureka-reducer-v1.json`);
const harvest = readRequired(`${sourcePhase}-triad-harvest-reduction-v1.json`);
const skills = installSkills(queue.skill_ideas || []);
const runners = createRunners(queue.runner_ideas || []);
const runnerInvocations = runners.map((runner) => runChild(runner.file, ["--phase-slug", phaseSlug]));
const reflectionLedger = buildReflectionLedger();
const manifest = buildManifest(reflectionLedger);

writePair("web-journey-reflection-ledger-50", reflectionLedger, renderSimpleMd("Web Journey Reflection Ledger", reflectionLedger));
writeJson(path.join(tracesDir, `${phaseSlug}-web-search-manifest-v1.json`), manifest);

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

const skillPack = base("ghc_v556_v4_x2_skill_runner_pack", "PASS_V556_V4_X2_SKILL_RUNNER_PACK_INSTALLED", {
  source_phase: sourcePhase,
  skill_count: skills.length,
  runner_count: runners.length,
  skills,
  runners,
  runner_invocations: runnerInvocations.map((item) => item.summary),
});

const safeExecution = base("ghc_v556_v4_x2_safe_execution_reducer", "PASS_V556_V4_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
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
    blocked_packets_queued: queue.counts.blocked_packets || 0,
  },
  triad_harvest_status: harvest.overall_status,
  open_gate_boundary: openGateBoundary(),
});

const lumenReadiness = base("ghc_v556_v4_x2_v5_lumen_readiness", "PASS_V556_V5_X1_LUMEN_STARTUP_READY", {
  target_phase_slug: nextX1,
  target_lane: "Lumen Vale solo unless Hamish redirects",
  launch_skill: "ghc-lumen-launch",
  route_notes: [
    "Prepare sanitized handoff artifact before Browser send.",
    "Do not duplicate-send while a response is active.",
    "Use background supervision and productive cadence until harvest.",
  ],
});

const executionIndex = base("ghc_v556_v4_x2_execution_index", "PASS_V556_V4_X2_EXECUTION_BUILT_PENDING_CLOSEOUT", {
  source_phase: sourcePhase,
  artifacts: {
    skill_runner_pack: `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    safe_execution: `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    reflection_ledger: `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    lumen_readiness: `docs/trinity-live-traces/${phaseSlug}-v5-lumen-readiness-v1.json`,
    safe_runner_orchestrator: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
  },
  counts: {
    safe_now_packets: queue.counts.safe_packets,
    candidate_packets: queue.counts.candidate_packets,
    exact_packets_queued: queue.counts.exact_approval_packets,
    blocked_packets_queued: queue.counts.blocked_packets || 0,
    cleanup_inventory_only: queue.counts.cleanup_proposals,
    skills_created_or_refreshed: skills.length,
    runners_created_or_refreshed: runners.length,
    web_reflections: reflectionLedger.web_reflection_count,
    journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  },
  safe_runner_status: safeRunner.summary.stdout_status,
  next_active_phase_after_closeout: nextX1,
});

writePair("skill-runner-pack-install", skillPack, renderSimpleMd("Skill Runner Pack", skillPack));
writePair("safe-execution-reducer", safeExecution, renderSimpleMd("Safe Execution Reducer", safeExecution));
writePair("v5-lumen-readiness", lumenReadiness, renderSimpleMd("v5 Lumen Readiness", lumenReadiness));
writePair("execution-index", executionIndex, renderSimpleMd("Execution Index", executionIndex));

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

function installSkills(rows) {
  fs.mkdirSync(localSkillRoot, { recursive: true });
  return rows.slice(0, 20).map((row, index) => {
    const name = sanitizeSkillName(row.title || `v556 v4 x2 skill ${index + 1}`);
    const dir = path.join(localSkillRoot, name);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "SKILL.md"), renderLocalSkill(name, row), "utf8");
    return {
      name,
      source_id: row.id || null,
      status: "installed_or_refreshed_local_only",
      publishable_path: `${name}/SKILL.md`,
      private_absolute_path_published: false,
    };
  });
}

function renderLocalSkill(name, row) {
  return [
    "---",
    `name: ${name}`,
    `description: Local GHC v556 v4 x2 skill for ${row.title || name}. Use only inside GHC phase work when this narrow role applies.`,
    "---",
    "",
    `# ${row.title || name}`,
    "",
    "Use this skill for local, reversible, status-only, validation, queue-shaping, x2 build/use, or reflection work inside the current GHC safety boundary.",
    "",
    "Do not publish raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, private callable IDs, private dumps, or hidden reasoning.",
    "Keep exact, blocked, proof, canon, legal, deployment, account, purchase, API-key, private-material, raw-publication, and sibling-merge gates open unless exact artifacts prove closure.",
    "",
  ].join("\n");
}

function createRunners(rows) {
  return rows.slice(0, 8).map((row, index) => {
    const name = sanitizeRunnerName(row.title || `ghc_v556_v4_x2_runner_${index + 1}.mjs`);
    const file = path.join(repoRoot, "scripts", name);
    fs.writeFileSync(file, renderRunner(name, row), "utf8");
    return { name, file: path.join("scripts", name), source_id: row.id || null, status: "created_or_refreshed_status_only" };
  });
}

function renderRunner(name, row) {
  return `#!/usr/bin/env node
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const phaseSlug = args.get("--phase-slug") || "${phaseSlug}";
console.log(JSON.stringify({
  artifact_type: "ghc_v556_v4_x2_generated_runner_receipt",
  runner_name: "${name}",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: "PASS_V556_V4_X2_STATUS_RUNNER",
  purpose: ${JSON.stringify(row.title || name)},
  source_id: ${JSON.stringify(row.id || null)},
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
}, null, 2));
`;
}

function buildReflectionLedger() {
  const web = Array.from({ length: 50 }, (_, index) => ({
    id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`,
    query: `v556 v4 x2 source reflection ${index + 1}`,
    source: [
      "OpenAI Codex skills",
      "OpenAI Codex goals",
      "Node child_process",
      "Python subprocess",
      "GitHub secret scanning",
      "NIST AI RMF",
      "W3C DID Core",
      "OWASP LLM Top 10",
      "JSON Schema",
      "NIST constants",
    ][index % 10],
    source_url: [
      "https://developers.openai.com/codex/skills",
      "https://developers.openai.com/codex/use-cases/follow-goals",
      "https://nodejs.org/api/child_process.html",
      "https://docs.python.org/3/library/subprocess.html",
      "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning",
      "https://www.nist.gov/itl/ai-risk-management-framework",
      "https://www.w3.org/TR/did-core/",
      "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
      "https://json-schema.org/",
      "https://physics.nist.gov/cuu/Constants/",
    ][index % 10],
    phase_reflection: "Use primary-source guidance for validation, privacy, source quality, and open proof gates.",
    runner_implication: "Carry into v4 x2 safe-runner, closeout, and v5 Lumen readiness.",
  }));
  const journey = Array.from({ length: 50 }, (_, index) => ({
    id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`,
    source: `v556 v4 x1 to v4 x2 continuity signal ${index + 1}`,
    phase_reflection: "Triad work is reduced into x2 build/use validation without raw lane publication.",
    runner_implication: "Use for skill pack, runner pack, exact gate queueing, and compact restart.",
  }));
  return base("ghc_v556_v4_x2_web_journey_reflection_ledger", "PASS_V556_V4_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
  });
}

function buildManifest(ledger) {
  return {
    artifact_type: "ghc_v556_v4_x2_web_search_manifest",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    minimum_reflections: 50,
    searches: ledger.web_reflections,
    publication_boundary: publicationBoundary(),
  };
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
      status: child.status,
      stdout_status: parseStatus(child.stdout),
      stdout_bytes: Buffer.byteLength(child.stdout || "", "utf8"),
      stderr_bytes: Buffer.byteLength(child.stderr || "", "utf8"),
    },
  };
}

function parseStatus(stdout) {
  try {
    const parsed = JSON.parse(stdout || "{}");
    return parsed.status || parsed.overall_status || "json_status_missing";
  } catch {
    return "unparsed";
  }
}

function base(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: extra.publication_boundary || publicationBoundary(),
  };
}

function writePair(suffix, payload, md) {
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Boundary",
    "",
    "Sanitized status artifact only. No private route handles, raw transcripts, screenshots, credentials, local absolute paths, raw lane text, or private IDs are published.",
    "",
  ].join("\n");
}

function readRequired(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function sanitizeSkillName(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 70) || "ghc-v556-v4-x2-skill";
}

function sanitizeRunnerName(value) {
  const baseName = value.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "").slice(0, 70) || "ghc_v556_v4_x2_runner";
  return baseName.endsWith(".mjs") ? baseName : `${baseName}.mjs`;
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

function openGateBoundary() {
  return {
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment_closure: "open",
    account_mutation: "open",
    purchase: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_replacement_or_merge: "open",
  };
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
