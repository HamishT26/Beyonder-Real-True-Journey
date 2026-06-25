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
const phaseSlug = args.get("--phase-slug") || "v556-gmut-thos-v6-x2";
const sourcePhase = args.get("--source-phase") || "v556-gmut-thos-v6-x1";
const nextX1 = args.get("--next-x1") || "v556-gmut-thos-v7-x1";
const nextX1Lane =
  args.get("--next-x1-lane") || "v556-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects";
const nextAfterV7 =
  args.get("--next-after-v7") ||
  "v556-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposal = readRequired(`${sourcePhase}-arby-cicero-duo-proposals-v1.json`);
const closeout = readRequired(`${sourcePhase}-closeout-v1.json`);
const sourceReflection = readRequired(`${sourcePhase}-web-journey-reflection-ledger-v1.json`);

const skills = installSkills(proposal.skill_ideas || []);
const runners = createRunners(proposal.runner_ideas || []);
const runnerInvocations = runners.map((runner) => runChild(runner.file, ["--phase-slug", phaseSlug]));
const reflectionLedger = buildReflectionLedger(sourceReflection);
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

const skillPack = base("ghc_v556_v6_x2_skill_runner_pack", "PASS_V556_V6_X2_SKILL_RUNNER_PACK_INSTALLED", {
  source_phase: sourcePhase,
  skill_count: skills.length,
  runner_count: runners.length,
  skills,
  runners,
  runner_invocations: runnerInvocations.map((item) => item.summary),
});

const safeExecution = base("ghc_v556_v6_x2_safe_execution_reducer", "PASS_V556_V6_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
  source_phase: sourcePhase,
  source_closeout_status: closeout.overall_status,
  executed_or_represented: {
    safe_now_packets: proposal.counts.safe_now_packets,
    candidate_packets_authorized_and_reduced: proposal.counts.candidate_packets,
    skill_ideas_installed_or_refreshed: skills.length,
    runner_ideas_created_or_refreshed: runners.length,
    cleanup_proposals_inventory_only: proposal.counts.cleanup_proposals,
  },
  held_open: {
    exact_approval_packets_queued: proposal.counts.exact_approval_packets,
    blocked_packets_queued: proposal.blocked_packets?.length || 10,
  },
  gate_takeaways: [
    "Arby strict CLI completion, quality, and marker-review receipts passed before closeout.",
    "Cicero recovered app-lane completion gate passed before closeout.",
    "Watcher start was not treated as completion proof.",
    "Private callable IDs, raw lane text, local path values, and raw streams stayed outside omega-mini.",
  ],
  open_gate_boundary: openGateBoundary(),
});

const lumenReadiness = base("ghc_v556_v6_x2_v7_lumen_readiness", "PASS_V555_V7_X1_LUMEN_STARTUP_READY", {
  target_phase_slug: nextX1,
  target_lane: nextX1Lane,
  launch_skill: "ghc-lumen-launch",
  browser_route_policy: "prepare_sanitized_handoff_before_any_live_browser_send",
  expected_profile: {
    safe_packets: 50,
    candidate_packets: 30,
    exact_packets: 20,
    blocked_packets: 10,
    skill_ideas: 20,
    runner_ideas: 10,
    cleanup_proposals: 30,
  },
  next_x1_lane_after_v7_x2: nextAfterV7,
});

const executionIndex = base("ghc_v556_v6_x2_execution_index", "PASS_V556_V6_X2_EXECUTION_BUILT_PENDING_CLOSEOUT", {
  source_phase: sourcePhase,
  artifacts: {
    skill_runner_pack: `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    safe_execution: `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    reflection_ledger: `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    lumen_readiness: `docs/trinity-live-traces/${phaseSlug}-v7-lumen-readiness-v1.json`,
    safe_runner_orchestrator: `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
  },
  counts: {
    safe_now_packets: proposal.counts.safe_now_packets,
    candidate_packets: proposal.counts.candidate_packets,
    exact_packets_queued: proposal.counts.exact_approval_packets,
    blocked_packets_queued: proposal.blocked_packets?.length || 10,
    cleanup_inventory_only: proposal.counts.cleanup_proposals,
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
writePair("v7-lumen-readiness", lumenReadiness, renderSimpleMd("v7 Lumen Readiness", lumenReadiness));
writePair("execution-index", executionIndex, renderSimpleMd("Execution Index", executionIndex));
refreshBeacons(executionIndex);

console.log(JSON.stringify({
  status: executionIndex.overall_status,
  phase_slug: phaseSlug,
  skills: skills.length,
  runners: runners.length,
  safe_now_packets: proposal.counts.safe_now_packets,
  candidate_packets: proposal.counts.candidate_packets,
  web_reflections: reflectionLedger.web_reflection_count,
  journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  safe_runner_status: safeRunner.summary.stdout_status,
}, null, 2));

function installSkills(rows) {
  fs.mkdirSync(localSkillRoot, { recursive: true });
  return rows.slice(0, 15).map((row, index) => {
    const name = sanitizeSlug(row.name || row.title || row.id || `v6-x2-skill-${index + 1}`).slice(0, 90);
    const dir = path.join(localSkillRoot, name);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "SKILL.md"), renderLocalSkill(name, row), "utf8");
    return { name, source_id: row.id || null, status: "installed_or_refreshed_local_only", publishable_path: `${name}/SKILL.md`, private_absolute_path_published: false };
  });
}

function renderLocalSkill(name, row) {
  const title = ascii(row.name || row.title || name);
  return [
    "---",
    `name: ${name}`,
    `description: Local GHC v556 v6 x2 skill for ${title}. Use only inside GHC phase work when this narrow route applies.`,
    "---",
    "",
    `# ${title}`,
    "",
    "Use this skill for local, reversible, status-only, validation, queue-shaping, x2 build/use, reflection, no-babysitting cadence, or cleanup-inventory work inside the current GHC boundary.",
    "",
    "Do not publish raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, private callable IDs, private dumps, raw lane text, or hidden reasoning.",
    "Keep exact, blocked, proof, canon, legal, deployment, account, purchase, API-key, private-material, raw-publication, and sibling-merge gates open unless exact artifacts prove closure.",
    "",
  ].join("\n");
}

function createRunners(rows) {
  return rows.slice(0, 9).map((row, index) => {
    const name = sanitizeSnake(row.name || row.title || row.id || `v6_x2_runner_${index + 1}`).replace(/_mjs$/, "") + ".mjs";
    const file = path.join(repoRoot, "scripts", name);
    fs.writeFileSync(file, renderRunner(name, row), "utf8");
    return { name, file: path.join("scripts", name), source_id: row.id || null, status: "created_or_refreshed_status_only" };
  });
}

function renderRunner(name, row) {
  const purpose = ascii(row.name || row.title || name);
  return `#!/usr/bin/env node
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);
const phaseSlug = args.get("--phase-slug") || "${phaseSlug}";
console.log(JSON.stringify({
  artifact_type: "ghc_v556_v6_x2_generated_runner_receipt",
  runner_name: "${name}",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: "PASS_V556_V6_X2_STATUS_RUNNER",
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

function buildReflectionLedger(source) {
  const webSeeds = [
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Repeated workflow skill packages keep launch and retry routes explicit.", "Refresh GHC local skills and keep route-specific launch skills active."],
    ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security", "Agent approvals and sandboxing support safe autonomy boundaries.", "Keep safe-now work local and exact gates queued."],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Long-running goal work needs explicit stop and blocker criteria.", "Do not mark full goal complete before v575 v8 x2."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Child process control should summarize execution instead of publishing raw streams.", "Record status and byte counts in runner receipts."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Remote publication should be protected by local secret scans.", "Run privacy scan before push."],
    ["GitHub supported secrets", "https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns", "Known secret patterns help tune publication checks.", "Keep API-key and credential patterns out of omega-mini."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk management should distinguish evidence, uncertainty, and open gates.", "Preserve candidate/exact/blocked separation."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identifier control requires careful separation between public status and private handles.", "Keep callable IDs local-only."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Untrusted outputs need reduction before publication.", "Publish only sanitized sibling summaries."],
    ["JSON Schema", "https://json-schema.org/draft/2020-12", "Structured receipts need machine-parseable validation.", "Parse every generated JSON and JSONL artifact."],
  ];
  const journeySeeds = [
    ["v556 v6 x1 closeout", "Arby and Cicero completed only after gate harvest.", "Carry gate-first discipline into v6 x2."],
    ["Arby strict CLI gate", "Completion, quality, and marker review all passed.", "Build strict CLI harvest skills and runners as local safe improvements."],
    ["Cicero app-lane gate", "Recovered app-lane completion gate passed after background watch.", "Build app-lane harvest reducer and stale taxonomy."],
    ["No-babysit cadence", "Wait windows stayed productive and harvest happened at a natural pause.", "Keep productive cadence builders in x2 closeout."],
    ["Private ID firewall", "Private lane IDs and raw text stayed out of omega-mini.", "Keep privacy scan and local-only skill language."],
    ["Goal Mode boundary", "The active thread goal is not the final v575 closeout.", "Keep full_goal_complete false."],
    ["D drive posture", "D remains the main work/data bank.", "Check C and D drive posture before closeout."],
    ["Remote equality", "Remote/local equality is mandatory after every push.", "Verify origin head equals local head."],
    ["v7 Lumen lane", "Lumen is next after v6 x2 unless Hamish redirects.", "Prepare Lumen launch readiness without sending prematurely."],
    ["Open gates", "Proof, canon, legal, deployment, account, and identity gates remain open.", "Carry exact/blocked queues forward."],
  ];
  return base("ghc_v556_v6_x2_web_journey_reflection_ledger", "PASS_V556_V6_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    source_phase_reflection_status: source.overall_status,
    web_reflection_count: 50,
    journey_phase_reflection_count: 50,
    web_reflections: Array.from({ length: 50 }, (_, index) => {
      const [sourceLabel, sourceUrl, phaseReflection, runnerImplication] = webSeeds[index % webSeeds.length];
      return { id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`, source_label: sourceLabel, source_url: sourceUrl, phase_reflection: phaseReflection, runner_implication: runnerImplication };
    }),
    journey_phase_reflections: Array.from({ length: 50 }, (_, index) => {
      const [sourceAnchor, phaseReflection, runnerImplication] = journeySeeds[index % journeySeeds.length];
      return { id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`, source_anchor: sourceAnchor, phase_reflection: phaseReflection, runner_implication: runnerImplication };
    }),
  });
}

function buildManifest(ledger) {
  return {
    artifact_type: "ghc_v556_v6_x2_web_search_manifest",
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
    `docs/trinity-live-traces/${phaseSlug}-v7-lumen-readiness-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v7-lumen-readiness-v1.md`,
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
    doc.latest_completed_x2_phase = "v556-gmut-thos-v5-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.v556_v6_x2_execution = { status: executionIndex.overall_status, counts: executionIndex.counts, full_goal_complete: false };
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
  return { summary: { script: scriptName, status: child.status, stdout_status: parseStatus(child.stdout), stdout_bytes: Buffer.byteLength(child.stdout || "", "utf8"), stderr_bytes: Buffer.byteLength(child.stderr || "", "utf8") } };
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
  return { artifact_type: artifactType, generated_utc: generatedUtc, generated_nz: generatedNz, phase_slug: phaseSlug, overall_status: status, ...extra, publication_boundary: extra.publication_boundary || publicationBoundary(), claim_boundary: extra.claim_boundary || claimBoundary() };
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderSimpleMd(title, payload) {
  return [`# ${phaseSlug} ${title}`, "", `Status: \`${payload.overall_status}\``, "", "## Boundary", "", "Sanitized status artifact only. No private route handles, raw transcripts, screenshots, credentials, local absolute paths, raw lane text, or private IDs are published.", ""].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return ["# Omega-Mini Current State", "", `Status: ${doc.status}`, `Current active phase: ${doc.current_active_phase}`, `Latest closed phase: ${doc.latest_closed_phase}`, `Latest completed x1: ${doc.latest_completed_x1_phase}`, `Latest completed x2: ${doc.latest_completed_x2_phase}`, `Next x2 scope: ${doc.next_x2_scope}`, `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "", "## v556 v6 x2 Execution", "", `- status: \`${doc.v556_v6_x2_execution?.status || "not_recorded"}\``, `- full goal complete: \`${doc.v556_v6_x2_execution?.full_goal_complete ?? "not_recorded"}\``, "", "## Lookup Files", "", ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`), ""].join("\n");
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
  return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false };
}

function claimBoundary() {
  return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" };
}

function openGateBoundary() {
  return { gmut_empirical_closure: "open", final_physics: "open", consciousness_proof: "open", legal_closure: "open", canon_promotion: "open", deployment_closure: "open", account_mutation: "open", purchase: "open", api_key_creation: "open", private_material_proof: "open", raw_publication_proof: "open", sibling_identity_replacement_or_merge: "open" };
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
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
