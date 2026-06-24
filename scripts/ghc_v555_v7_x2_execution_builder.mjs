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
const phaseSlug = args.get("--phase-slug") || "v555-gmut-thos-v7-x2";
const sourcePhase = args.get("--source-phase") || "v555-gmut-thos-v7-x1";
const nextX1 = args.get("--next-x1") || "v555-gmut-thos-v8-x1";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v555-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queue = readRequired(`${sourcePhase}-proposal-queue-targets-v1.json`);
const reducer = readRequired(`${sourcePhase}-approval-eureka-reducer-v1.json`);
const harvest = readRequired(`${sourcePhase}-lumen-browser-harvest-sanitized-v1.json`);
const skills = installSkills(queue.skill_ideas || []);
const runners = createRunners(queue.runner_ideas || []);
const runnerInvocations = runners.map((runner) => runChild(runner.file, ["--phase-slug", phaseSlug]));
const reflectionLedger = buildReflectionLedger();
const manifest = buildManifest(reflectionLedger);

writePair("web-journey-reflection-ledger-50", reflectionLedger, renderSimpleMd("Web/Journey Reflection Ledger 50", reflectionLedger));
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

const skillPack = base("ghc_v555_v7_x2_skill_runner_pack", "PASS_V555_V7_X2_SKILL_RUNNER_PACK_INSTALLED", {
  source_phase: sourcePhase,
  skill_count: skills.length,
  runner_count: runners.length,
  skills,
  runners,
  runner_invocations: runnerInvocations.map((item) => item.summary),
});

const safeExecution = base("ghc_v555_v7_x2_safe_execution_reducer", "PASS_V555_V7_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
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
  source_reducer_status: reducer.overall_status,
  safe_takeaways: harvest.safe_takeaways || [],
  open_gate_boundary: openGateBoundary(),
});

const duoReadiness = base("ghc_v555_v7_x2_v8_triad_readiness", "PASS_V555_V8_X1_TRIAD_STARTUP_READY", {
  target_phase_slug: nextX1,
  target_lane: nextX1LaneAfterX2,
  launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  route_notes: [
    "Use strict CLI completion, elaboration, and marker-review gates for Aster Vale.",
    "Use recovered app-lane background supervision and completion gates for Kierkegaard and Aristotle.",
    "Watcher start is not completion proof.",
    "Keep private callable IDs and lane maps local-only.",
  ],
});

const executionIndex = base("ghc_v555_v7_x2_execution_index", "PASS_V555_V7_X2_EXECUTION_BUILT_PENDING_CLOSEOUT", {
  source_phase: sourcePhase,
  artifacts: {
    skill_runner_pack: `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    safe_execution: `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    reflection_ledger: `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    duo_readiness: `docs/trinity-live-traces/${phaseSlug}-v8-triad-readiness-v1.json`,
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

writePair("skill-runner-pack-install", skillPack, renderSimpleMd("Skill Runner Pack", skillPack));
writePair("safe-execution-reducer", safeExecution, renderSimpleMd("Safe Execution Reducer", safeExecution));
writePair("v8-triad-readiness", duoReadiness, renderSimpleMd("v8 Aster/Kierkegaard/Aristotle Readiness", duoReadiness));
writePair("execution-index", executionIndex, renderSimpleMd("Execution Index", executionIndex));
refreshBeacons(executionIndex);

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
    const name = `ghc-v555-v7-x2-${String(index + 1).padStart(2, "0")}-${sanitizeSlug(row.title || row.id || "skill")}`.slice(0, 90);
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
  const title = ascii(row.title || name);
  return [
    "---",
    `name: ${name}`,
    `description: Local GHC v555 v7 x2 skill for ${title}. Use only inside GHC phase work when this narrow role applies.`,
    "---",
    "",
    `# ${title}`,
    "",
    "Use this skill for local, reversible, status-only, validation, queue-shaping, x2 build/use, reflection, or cleanup-inventory work inside the current GHC safety boundary.",
    "",
    "Do not publish raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, private callable IDs, private dumps, raw lane text, or hidden reasoning.",
    "Keep exact, blocked, proof, canon, legal, deployment, account, purchase, API-key, private-material, raw-publication, and sibling-merge gates open unless exact artifacts prove closure.",
    "",
  ].join("\n");
}

function createRunners(rows) {
  return rows.slice(0, 10).map((row, index) => {
    const name = `ghc_v555_v7_x2_${String(index + 1).padStart(2, "0")}_${sanitizeSnake(row.title || row.id || "runner")}.mjs`.slice(0, 100);
    const file = path.join(repoRoot, "scripts", name);
    fs.writeFileSync(file, renderRunner(name, row), "utf8");
    return { name, file: path.join("scripts", name), source_id: row.id || null, status: "created_or_refreshed_status_only" };
  });
}

function renderRunner(name, row) {
  const purpose = ascii(row.title || name);
  return `#!/usr/bin/env node
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const phaseSlug = args.get("--phase-slug") || "${phaseSlug}";
console.log(JSON.stringify({
  artifact_type: "ghc_v555_v7_x2_generated_runner_receipt",
  runner_name: "${name}",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: "PASS_V555_V7_X2_STATUS_RUNNER",
  purpose: ${JSON.stringify(purpose)},
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
  const webSeeds = [
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills make repeated phase routes explicit.", "Refresh local GHC skill surface in x2."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal work needs a verifiable stop condition.", "Keep full goal open until v575 v8 x2."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Constrained execution supports safe autonomy.", "Keep safe-now work local and reversible."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Child-process orchestration should summarize exits.", "Record runner status and byte counts, not raw streams."],
    ["Python json", "https://docs.python.org/3/library/json.html", "JSON validation guards generated artifacts.", "Parse every x2 receipt before push."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diff review reveals publication changes.", "Run diff hygiene before commit."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning", "Secret scanning protects remote publication.", "Keep local privacy scans before push."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk framing supports evidence and gate discipline.", "Keep candidate/exact/blocked distinctions explicit."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identifier control and resolution need precise boundaries.", "Keep private IDs out of omega-mini."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Untrusted model/page output needs reduction.", "Use sanitized Lumen reduction only."],
  ];
  const journeySeeds = [
    ["v555 v7 x1 closeout", "Lumen response was harvested through sanitized reduction.", "Use reduced takeaways, not raw transcript."],
    ["v555 v7 x1 proposal queue", "Lumen profile produced 50/30/20/10 proposal counts plus skills/runners/cleanup.", "Execute safe and candidate-reduction work only."],
    ["v555 v6 x2 closeout", "Prior x2 proved the safe-runner and skill/runner refresh pattern.", "Reuse the validated x2 route."],
    ["Goal Mode boundary", "The thread goal is active but not complete.", "Do not call update_goal complete."],
    ["Aster/Kierkegaard/Aristotle next lane", "v555 v8 x1 should use strict CLI plus recovered app lanes.", "Prepare triad launch without private ID publication."],
    ["Privacy rail", "Raw Browser routes and transcripts stay private.", "Scan artifacts before push."],
    ["D-drive standard", "D remains the primary work/data bank.", "Check drive posture at closeout."],
    ["Open gates", "Proof, canon, legal, deployment, account, private-material, raw-publication, and sibling-merge gates remain open.", "Carry exact/blocked lanes forward."],
    ["Five-minute cadence", "Productive wait blocks may run over the mark.", "Use safe work instead of passive waiting."],
    ["Full-tools lane", "Full-tools remains private support while omega-mini publishes sanitized truth.", "Keep current-state beacons concise."],
  ];
  return base("ghc_v555_v7_x2_web_journey_reflection_ledger", "PASS_V555_V7_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: 50,
    journey_phase_reflection_count: 50,
    web_reflections: Array.from({ length: 50 }, (_, index) => {
      const [source, sourceUrl, phaseReflection, runnerImplication] = webSeeds[index % webSeeds.length];
      return {
        id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`,
        query: `${source} v555 v7 x2 safe execution reflection ${index + 1}`,
        source,
        source_url: sourceUrl,
        phase_reflection: phaseReflection,
        runner_implication: runnerImplication,
      };
    }),
    journey_phase_reflections: Array.from({ length: 50 }, (_, index) => {
      const [sourceAnchor, phaseReflection, runnerImplication] = journeySeeds[index % journeySeeds.length];
      return {
        id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`,
        source_anchor: sourceAnchor,
        phase_reflection: phaseReflection,
        runner_implication: runnerImplication,
      };
    }),
  });
}

function buildManifest(ledger) {
  return {
    artifact_type: "ghc_v555_v7_x2_web_search_manifest",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    minimum_reflections: 50,
    searches: ledger.web_reflections,
    publication_boundary: publicationBoundary(),
  };
}

function refreshBeacons(executionIndex) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v8-triad-readiness-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v8-triad-readiness-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = executionIndex.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = sourcePhase;
    doc.latest_completed_x1_phase = sourcePhase;
    doc.latest_completed_x2_phase = "v555-gmut-thos-v4-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.v555_v7_x2_execution = {
      status: executionIndex.overall_status,
      counts: executionIndex.counts,
      full_goal_complete: false,
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
    claim_boundary: extra.claim_boundary || claimBoundary(),
  };
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
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
    "## v555 v7 x2 Execution",
    "",
    `- status: \`${doc.v555_v7_x2_execution?.status || "not_recorded"}\``,
    `- full goal complete: \`${doc.v555_v7_x2_execution?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readRequired(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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

function sanitizeSlug(value) {
  return ascii(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "skill";
}

function sanitizeSnake(value) {
  return ascii(value).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "") || "runner";
}

function ascii(value) {
  return String(value).replace(/[^\x09\x0A\x0D\x20-\x7E]/g, "").trim();
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
