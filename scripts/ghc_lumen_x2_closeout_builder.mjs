#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const sourceX1Phase = required("--source-x1");
const nextActivePhase = required("--next-active-phase");
const nextX2Scope = required("--next-x2-scope");
const nextX1LaneAfterX2 = required("--next-x1-after-x2");
const status = args.get("--status") || "PASS_LUMEN_X2_CLOSED_NEXT_X1_READY";
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const requiredFiles = {
  source_queue: `${sourceX1Phase}-lumen-sanitized-proposal-queue-v1.json`,
  reflection_manifest: `${phaseSlug}-reflection-manifest-v1.json`,
  safe_runner_orchestrator: `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  safe_build_ledger: `${phaseSlug}-safe-build-use-ledger-v1.json`,
  next_x1_prep_card: `${phaseSlug}-next-x1-prep-card-v1.json`,
};
const missing = Object.values(requiredFiles).filter((name) => !existsSync(join(tracesDir, name)));
if (missing.length) {
  console.error(JSON.stringify({ status: "OPEN_GAP_LUMEN_X2_REQUIRED_ARTIFACTS_MISSING", phase_slug: phaseSlug, missing, closeout_claimed: false }, null, 2));
  process.exit(2);
}

const sourceQueue = readJson(join(tracesDir, requiredFiles.source_queue));
const reflectionManifest = readJson(join(tracesDir, requiredFiles.reflection_manifest));
const orchestrator = readJson(join(tracesDir, requiredFiles.safe_runner_orchestrator));
const safeBuildLedger = readJson(join(tracesDir, requiredFiles.safe_build_ledger));
const counts = sourceQueue.expected_profile || sourceQueue.profile_cap_counts_represented || {};
const reflectionCount = Number(reflectionManifest.reflection_count || 0);
const searchCount = Number(reflectionManifest.search_count_declared || 0);
const orchestratorPass = orchestrator.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";
const safeBuildCount = Array.isArray(safeBuildLedger.safe_builds_executed) ? safeBuildLedger.safe_builds_executed.length : 0;
const closeoutAllowed = orchestratorPass && reflectionCount >= 100 && searchCount >= 100 && safeBuildCount >= 1;
const closeoutStatus = closeoutAllowed ? status : "OPEN_GAP_LUMEN_X2_CLOSEOUT_GATES_INCOMPLETE";

const artifacts = [
  artifact("x2-execution-ledger", "ghc.lumen_x2_execution_ledger.v2", closeoutAllowed ? "PASS_LUMEN_X2_SAFE_QUEUE_REDUCED" : "OPEN_GAP_LUMEN_X2_SAFE_QUEUE_REDUCTION", {
    source_x1_phase: sourceX1Phase,
    source_queue_basename: requiredFiles.source_queue,
    profile_cap_counts_represented: counts,
    queue_rows_represented: Array.isArray(sourceQueue.rows) ? sourceQueue.rows.length : 0,
    safe_runner_overall_status: orchestrator.overall_status,
    safe_runner_count: orchestrator.runner_count,
    reflection_count: reflectionCount,
    search_count_declared: searchCount,
    safe_builds_executed: safeBuildCount,
  }),
  artifact("candidate-exact-blocked-open-gate-queue", "ghc.lumen_x2_open_gate_queue.v2", "PASS_CANDIDATE_EXACT_BLOCKED_ROWS_QUEUED_OPEN", {
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    blocked_packets_queued: counts.blocked_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate rows are represented in safe build guidance; exact and blocked gates are not auto-run.",
    open_gates: openGates(),
  }),
  artifact("next-x1-startup-handoff", "ghc.next_x1_startup_handoff.v2", "PASS_NEXT_X1_STARTUP_HANDOFF_READY", {
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    full_goal_complete: false,
  }),
  artifact("closeout", "ghc.phase_closeout.v2", closeoutStatus, {
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
  queue_rows_represented: Array.isArray(sourceQueue.rows) ? sourceQueue.rows.length : 0,
  reflections: reflectionCount,
  searches: searchCount,
  artifacts_written: artifacts.length * 2 + (closeoutAllowed ? 6 : 0),
}, null, 2));
process.exit(closeoutAllowed ? 0 : 1);

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_lumen_x2_closeout_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

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
  writeFileSync(mdPath, `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}\n\nStatus: ${doc.status}\n\nGenerated NZ: ${doc.generated_nz}\n\nBoundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.\n`, "utf8");
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
    doc.next_expected_scope = nextX2Scope;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.current_active_lanes = ["Aevren Vale", nextActivePhase, "recomposed-round-robin-ready"];
    doc.lumen_x2_closeout = {
      status,
      source_x1_phase: sourceX1Phase,
      profile_counts_represented: counts,
      reflection_count: reflectionCount,
      search_count_declared: searchCount,
      safe_runner_overall_status: orchestrator.overall_status,
      next_active_phase: nextActivePhase,
      full_goal_complete: false,
    };
    doc.full_goal_complete = false;
    doc[lookupKey] = existingRelativeFiles([...(Array.isArray(doc[lookupKey]) ? doc[lookupKey] : []), ...lookup]);
  }
  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);
  const md = `# ${nextActivePhase}\n\nStatus: ${status}\n\n- Current active phase: ${nextActivePhase}\n- Latest closed phase: ${phaseSlug}\n- Latest completed x1: ${sourceX1Phase}\n- Latest completed x2: ${phaseSlug}\n- Next x2 scope: ${nextX2Scope}\n- Next x1 lane after x2: ${nextX1LaneAfterX2}\n- Full v544-v575 goal complete: false.\n\nSanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private paths, session streams, and private app state are not published here.\n`;
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), md, "utf8");
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), md, "utf8");
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), md, "utf8");
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
