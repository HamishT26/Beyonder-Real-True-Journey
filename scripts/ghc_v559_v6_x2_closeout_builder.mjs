#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v559-gmut-thos-v6-x2";
const sourceX1Phase = "v559-gmut-thos-v6-x1";
const nextActivePhase = "v559-gmut-thos-v7-x1";
const nextX2Scope = "v559-gmut-thos-v7-x2";
const nextX1LaneAfterX2 = "v559-gmut-thos-v8-x1 Mira Rowan and Neris Sol unless Hamish redirects";
const status = "PASS_V559_V6_X2_CLOSED_V7_X1_READY";

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const requiredFiles = {
  source_queue: `${sourceX1Phase}-combined-x1-to-x2-queue-v1.json`,
  reflection_manifest: `${phaseSlug}-reflection-manifest-v1.json`,
  safe_runner_orchestrator: `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  safe_build_ledger: `${phaseSlug}-safe-build-use-ledger-v1.json`,
  v7_lumen_prep_card: `${phaseSlug}-v7-x1-lumen-prep-card-v1.json`,
};

const missing = Object.values(requiredFiles).filter((name) => !existsSync(join(tracesDir, name)));
if (missing.length) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V559_V6_X2_REQUIRED_ARTIFACTS_MISSING",
    phase_slug: phaseSlug,
    missing,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const sourceQueue = readJson(join(tracesDir, requiredFiles.source_queue));
const reflectionManifest = readJson(join(tracesDir, requiredFiles.reflection_manifest));
const orchestrator = readJson(join(tracesDir, requiredFiles.safe_runner_orchestrator));
const safeBuildLedger = readJson(join(tracesDir, requiredFiles.safe_build_ledger));
const counts = sourceQueue.profile_cap_counts_represented || {};
const reflectionCount = Number(reflectionManifest.reflection_count || 0);
const searchCount = Number(reflectionManifest.search_count_declared || 0);
const orchestratorPass = orchestrator.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";
const safeBuildCount = Array.isArray(safeBuildLedger.safe_builds_executed) ? safeBuildLedger.safe_builds_executed.length : 0;
const closeoutAllowed = orchestratorPass && reflectionCount >= 100 && searchCount >= 100 && safeBuildCount >= 1;
const closeoutStatus = closeoutAllowed ? status : "OPEN_GAP_V559_V6_X2_CLOSEOUT_GATES_INCOMPLETE";

const artifacts = [
  artifact("x2-execution-ledger", "ghc.v559_v6_x2_execution_ledger.v1", closeoutAllowed
    ? "PASS_V559_V6_X2_SAFE_QUEUE_REDUCED"
    : "OPEN_GAP_V559_V6_X2_SAFE_QUEUE_REDUCTION", {
    source_x1_phase: sourceX1Phase,
    source_queue_basename: requiredFiles.source_queue,
    profile_cap_counts_represented: counts,
    immediate_x1_safe_rows_represented: sourceQueue.immediate_x1_safe_rows_represented || 0,
    x2_build_rows_represented: sourceQueue.x2_build_rows_represented || 0,
    safe_runner_overall_status: orchestrator.overall_status,
    safe_runner_count: orchestrator.runner_count,
    reflection_count: reflectionCount,
    search_count_declared: searchCount,
    safe_builds_executed: safeBuildCount,
  }),
  artifact("candidate-exact-open-gate-queue", "ghc.v559_v6_x2_open_gate_queue.v1", "PASS_CANDIDATE_EXACT_ROWS_QUEUED_OPEN", {
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    blocked_packets_queued: counts.blocked_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate rows are represented in safe build guidance; exact gates are not auto-run.",
    open_gates: openGates(),
  }),
  artifact("v7-x1-lumen-startup-handoff", "ghc.v559_v7_x1_lumen_startup_handoff.v1", "PASS_V559_V7_X1_LUMEN_STARTUP_HANDOFF_READY", {
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    next_lane: "Lumen-only",
    launch_skill: "ghc-lumen-launch",
    browser_refresh_rule: "refresh/reconnect and inspect status before unavailable claims; do not reload over an active response or unsent composer text",
  }),
  artifact("closeout", "ghc.phase_closeout.v1", closeoutStatus, {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: sourceX1Phase,
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    closeout_allowed: closeoutAllowed,
    queue_counts: counts,
    reflection_count: reflectionCount,
    search_count_declared: searchCount,
    safe_runner_overall_status: orchestrator.overall_status,
    safe_builds_executed: safeBuildCount,
    full_goal_complete: false,
    open_gates: openGates(),
  }),
];

for (const doc of artifacts) writePair(doc);
if (closeoutAllowed) refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  next_active_phase: closeoutAllowed ? nextActivePhase : phaseSlug,
  latest_completed_x2_phase: closeoutAllowed ? phaseSlug : null,
  safe_packets_represented: counts.safe_approval_packets || 0,
  candidate_packets_represented: counts.candidate_packets || 0,
  exact_packets_queued: counts.exact_approval_packets_queued || 0,
  skill_ideas_represented: counts.skill_ideas || 0,
  runner_ideas_represented: counts.runner_ideas || 0,
  cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
  reflections: reflectionCount,
  searches: searchCount,
  artifacts_written: artifacts.length * 2 + (closeoutAllowed ? 6 : 0),
}, null, 2));

process.exit(closeoutAllowed ? 0 : 1);

function artifact(suffix, schema, artifactStatus, body = {}) {
  return {
    artifact: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status: artifactStatus,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...body,
  };
}

function writePair(doc) {
  const jsonPath = join(process.cwd(), `${doc.artifact}.json`);
  const mdPath = join(process.cwd(), `${doc.artifact}.md`);
  writeJson(jsonPath, doc);
  const lines = [
    `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    `Phase: ${doc.phase_slug}`,
    "",
    "Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.",
    "",
  ];
  if (doc.next_active_phase) lines.push(`Next active phase: ${doc.next_active_phase}`, "");
  if (doc.next_x1_lane_after_x2) lines.push(`Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "");
  if (doc.queue_counts || doc.profile_cap_counts_represented) {
    const nextCounts = doc.queue_counts || doc.profile_cap_counts_represented;
    lines.push("## Counts", "");
    for (const [key, value] of Object.entries(nextCounts)) lines.push(`- ${key}: ${value}`);
  }
  if (doc.launch_skill) lines.push("", "## Launch Skill", "", doc.launch_skill);
  while (lines.at(-1) === "") lines.pop();
  writeFileSync(mdPath, `${lines.join("\n")}\n`, "utf8");
}

function refreshBeacons(artifactDocs) {
  const lookup = artifactDocs.flatMap((doc) => [`${doc.artifact}.json`, `${doc.artifact}.md`]);
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const beaconPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const state = readJson(statePath);
  const latest = readJson(latestPath);
  const beacon = existsSync(beaconPath) ? readJson(beaconPath) : {};
  for (const [doc, lookupKey] of [[state, "current_lookup_files"], [latest, "latest_lookup_files"], [beacon, "lookup_files"]]) {
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = status;
    doc.current_active_phase = nextActivePhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = sourceX1Phase;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.next_expected_scope = nextActivePhase;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.current_active_lanes = ["Aevren Vale", "Lumen", "ghc-lumen-launch", "Browser refresh/status-first"];
    doc.v559_v6_x2_closeout = {
      status,
      source_x1_phase: sourceX1Phase,
      profile_counts_represented: counts,
      reflection_count: reflectionCount,
      search_count_declared: searchCount,
      safe_runner_overall_status: orchestrator.overall_status,
      next_active_phase: nextActivePhase,
      full_goal_complete: false,
    };
    doc.lumen_browser_refresh_rule = "fresh DOM/status refresh before unavailable claims; no reload during active response or unsent composer text";
    doc.full_goal_complete = false;
    doc[lookupKey] = existingRelativeFiles([...(Array.isArray(doc[lookupKey]) ? doc[lookupKey] : []), ...lookup]);
  }
  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);
  const beaconMd = [
    `# ${nextActivePhase}`,
    "",
    `Status: ${status}`,
    "",
    `- Current active phase: ${nextActivePhase}`,
    `- Latest closed phase: ${phaseSlug}`,
    `- Latest completed x1: ${sourceX1Phase}`,
    `- Latest completed x2: ${phaseSlug}`,
    `- Next x2 scope: ${nextX2Scope}`,
    `- Next x1 lane after x2: ${nextX1LaneAfterX2}`,
    "- Next lane: Lumen-only through ghc-lumen-launch.",
    "- Lumen Browser route rule remains preserved: fresh DOM/status refresh before unavailable claims; no reload during active response or unsent composer text.",
    `- Counts represented: ${counts.safe_approval_packets || 0} safe, ${counts.candidate_packets || 0} candidate, ${counts.exact_approval_packets_queued || 0} exact queued, ${counts.skill_ideas || 0} skills, ${counts.runner_ideas || 0} runners, ${counts.cleanup_refine_fix_tasks || 0} cleanup tasks.`,
    `- Reflection/search count: ${reflectionCount}/${searchCount}.`,
    "- Full v544-v575 goal complete: false.",
    "",
    "Sanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private paths, session streams, and private app state are not published here.",
    "",
  ].join("\n");
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), beaconMd, "utf8");
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), beaconMd, "utf8");
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beaconMd, "utf8");
}

function existingRelativeFiles(files) {
  return Array.from(new Set(files.filter((file) => typeof file === "string" && existsSync(join(process.cwd(), file)))));
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
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

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "purchase",
    "account mutation",
    "API key creation",
    "private material proof",
    "raw publication proof",
    "sibling replacement or merge",
  ];
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
