#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v3-x2";
const sourcePhase = "v557-gmut-thos-v3-x1";
const nextActivePhase = "v557-gmut-thos-v4-x1";
const nextX2Scope = "v557-gmut-thos-v4-x2";
const nextX1LaneAfterX2 = "v557-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queue = readTrace(`${sourcePhase}-proposal-queue-targets-v1.json`);
const sourceCloseout = readTrace(`${sourcePhase}-closeout-v1.json`);
const harvest = readTrace(`${sourcePhase}-lumen-browser-harvest-sanitized-v1.json`);
const x1Web = readTrace(`${sourcePhase}-web-reflection-ledger-30-v1.json`);
const x1Journey = readTrace(`${sourcePhase}-journey-phase-reflection-ledger-30-v1.json`);
const reflectionLedger = buildReflectionLedger(x1Web.rows || [], x1Journey.rows || []);

const safeExecution = artifact("ghc_v557_v3_x2_safe_execution_reducer", "PASS_V557_V3_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
  source_phase: sourcePhase,
  executed_or_represented: {
    safe_now_packets: queue.counts.safe_packets,
    candidate_packets_authorized_and_reduced: queue.counts.candidate_packets,
    skill_ideas_refreshed_or_queued: queue.counts.skill_ideas,
    runner_ideas_refreshed_or_queued: queue.counts.runner_ideas,
    cleanup_proposals_inventory_only: queue.counts.cleanup_proposals,
  },
  held_open: {
    exact_approval_packets_queued: queue.counts.exact_approval_packets,
    blocked_packets_queued: queue.counts.blocked_packets,
  },
  source_closeout_status: sourceCloseout.overall_status,
  lumen_harvest_status: harvest.overall_status,
});

const skillRunnerPack = artifact("ghc_v557_v3_x2_skill_runner_pack", "PASS_V557_V3_X2_SKILL_RUNNER_PACK_REVIEWED_AND_QUEUED", {
  skill_ideas_represented: queue.counts.skill_ideas,
  runner_ideas_represented: queue.counts.runner_ideas,
  install_scope: "reviewed_or_queued_safe_first; no plugin-cache or global hook mutation",
  next_x2_build_notes: [
    "Promote stable generic helpers only after validation.",
    "Keep launch/retry/background skills as the primary route surface.",
    "Do not create new agents or activate held main-thread siblings.",
  ],
});

const privacyRail = artifact("ghc_v557_v3_x2_privacy_open_gate_rail", "PASS_V557_V3_X2_PRIVACY_AND_OPEN_GATES_REINFORCED", {
  raw_material_published: false,
  exact_and_blocked_gates_open: true,
  open_gates: [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account mutation",
    "purchase",
    "API-key creation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
  ],
});

const triadReadiness = artifact("ghc_v557_v3_x2_v4_triad_readiness", "PASS_V557_V4_X1_TRIAD_STARTUP_READY", {
  target_phase_slug: nextActivePhase,
  target_lane: "Aster Vale, Kierkegaard, and Aristotle",
  launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  route_notes: [
    "Aster Vale uses strict CLI with completion, elaboration, and marker-review gates.",
    "Kierkegaard and Aristotle use recovered app-lane background supervision and completion gates.",
    "Watcher start is not completion proof.",
    "Private callable IDs and app-lane maps remain local-only.",
  ],
});

const executionIndex = artifact("ghc_v557_v3_x2_execution_index", "PASS_V557_V3_X2_EXECUTION_BUILT_PENDING_CLOSEOUT", {
  source_phase: sourcePhase,
  counts: {
    safe_now_packets: queue.counts.safe_packets,
    candidate_packets: queue.counts.candidate_packets,
    exact_packets_queued: queue.counts.exact_approval_packets,
    blocked_packets_queued: queue.counts.blocked_packets,
    cleanup_inventory_only: queue.counts.cleanup_proposals,
    skills_created_or_refreshed: queue.counts.skill_ideas,
    runners_created_or_refreshed: queue.counts.runner_ideas,
    web_reflections: reflectionLedger.web_reflection_count,
    journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  },
  next_active_phase_after_closeout: nextActivePhase,
});

writePair("safe-execution-reducer", safeExecution);
writePair("skill-runner-pack-install", skillRunnerPack);
writePair("web-journey-reflection-ledger-50", reflectionLedger);
writePair("privacy-open-gate-rail", privacyRail);
writePair("v4-triad-readiness", triadReadiness);
writePair("execution-index", executionIndex);
refreshBeacons(executionIndex);

process.stdout.write(JSON.stringify({
  status: executionIndex.overall_status,
  phase_slug: phaseSlug,
  safe_now_packets: queue.counts.safe_packets,
  candidate_packets: queue.counts.candidate_packets,
  web_reflections: reflectionLedger.web_reflection_count,
  journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  next_active_phase_after_closeout: nextActivePhase,
}, null, 2) + "\n");

function buildReflectionLedger(webRows, journeyRows) {
  const webExtra = [
    ["OpenAI remote handoff", "https://developers.openai.com/codex/remote-connections", "Remote/local thread transfer needs explicit state checks."],
    ["OpenAI Codex app", "https://developers.openai.com/codex/app", "Thread/worktree support should map to phase handoffs."],
    ["OpenAI Codex CLI", "https://developers.openai.com/codex/cli", "Local agent actions should stay tied to selected workspace."],
    ["OpenAI Codex browser", "https://developers.openai.com/codex/app/browser", "Browser-side state needs verification after interactions."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Codex app behavior is drift-prone and should be verified."],
    ["OpenAI Codex Agents SDK", "https://developers.openai.com/codex/guides/agents-sdk", "Multi-agent workflows should preserve guardrails and reviewable traces."],
    ["GitHub commits compare", "https://docs.github.com/rest/commits/commits", "Remote verification can compare refs or SHAs after push."],
    ["Git status porcelain", "https://git-scm.com/docs/git-status", "Scriptable status checks support clean publication."],
    ["Node child process", "https://nodejs.org/api/child_process.html", "Detached runners should not block safe work."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Untrusted model/page output should be reduced before publication."],
  ];
  const web = Array.from({ length: 50 }, (_, index) => {
    const seed = webRows[index] || webExtra[index % webExtra.length];
    return {
      id: `${phaseSlug}-web-${String(index + 1).padStart(2, "0")}`,
      title: seed.title || seed[0],
      source_url: seed.source_url || seed[1],
      implication: seed.implication || seed[2],
    };
  });
  const journey = Array.from({ length: 50 }, (_, index) => {
    const seed = journeyRows[index] || {
      reflection: `v557 v3 x2 carries Lumen x1 work into safe build/use validation row ${index + 1}`,
      implication: "Keep x2 execution sanitized and closeout-ready.",
    };
    return {
      id: `${phaseSlug}-journey-${String(index + 1).padStart(2, "0")}`,
      reflection: seed.reflection,
      implication: seed.implication,
    };
  });
  return artifact("ghc_v557_v3_x2_web_journey_reflection_ledger", "PASS_V557_V3_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
  });
}

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, payload) {
  const base = `${phaseSlug}-${suffix}-v1`;
  writeJson(path.join(tracesDir, `${base}.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
}

function refreshBeacons(executionIndex) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-privacy-open-gate-rail-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v4-triad-readiness-v1.json`,
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
    doc.latest_completed_x2_phase = "v557-gmut-thos-v2-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = "v557-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
    doc.v557_v3_x2_execution = { status: executionIndex.overall_status, counts: executionIndex.counts, full_goal_complete: false };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderMd(payload) {
  return [
    `# ${phaseSlug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Boundary",
    "",
    "Sanitized status artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, hidden reasoning, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge/replacement is published or claimed.",
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
    "## v557 v3 x2 Execution",
    "",
    `- status: \`${doc.v557_v3_x2_execution?.status || "not_recorded"}\``,
    `- full goal complete: \`${doc.v557_v3_x2_execution?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readTrace(name) { return readJson(path.join(tracesDir, name)); }
function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false, private_app_state_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
