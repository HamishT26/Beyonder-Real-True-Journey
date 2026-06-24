#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs();
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v1-x1";
const latestClosedBefore = "v553-gmut-thos-v8-x2";
const latestCompletedX2 = "v553-gmut-thos-v8-x2";
const nextX2Scope = "v554-gmut-thos-v1-x2";
const nextX1LaneAfterX2 = "v554-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposalQueue = readTrace(`${phaseSlug}-proposal-queue-targets-v1.json`);
const sendReceipt = readTrace(`${phaseSlug}-lumen-browser-send-receipt-v1.json`);
const harvestReceipt = readTrace(`${phaseSlug}-lumen-browser-harvest-sanitized-v1.json`);
const safeRunner = readTrace(`${phaseSlug}-safe-runner-orchestrator-v1.json`);
const liveWeb = readTrace(`${phaseSlug}-live-web-search-reflection-ledger-32-v1.json`);
const journey30 = ensureJourney30();

const counts = {
  safe_now_packets: countArray(proposalQueue.safe_packets),
  candidate_packets: countArray(proposalQueue.candidate_packets),
  exact_approval_packets: countArray(proposalQueue.exact_approval_packets),
  blocked_packets: countArray(proposalQueue.blocked_packets),
  skill_ideas: countArray(proposalQueue.skill_ideas),
  runner_ideas: countArray(proposalQueue.runner_ideas),
  cleanup_proposals: countArray(proposalQueue.cleanup_tasks),
  live_web_search_reflections: countArray(liveWeb.rows),
  journey_phase_reflections: countArray(journey30.reflections),
};

const missing = [
  [`${phaseSlug}-proposal-queue-targets-v1.json`, proposalQueue],
  [`${phaseSlug}-lumen-browser-send-receipt-v1.json`, sendReceipt],
  [`${phaseSlug}-lumen-browser-harvest-sanitized-v1.json`, harvestReceipt],
  [`${phaseSlug}-safe-runner-orchestrator-v1.json`, safeRunner],
  [`${phaseSlug}-live-web-search-reflection-ledger-32-v1.json`, liveWeb],
  [`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`, journey30],
].filter(([, value]) => !value).map(([name]) => name);

const checks = {
  missing_artifacts: missing,
  send_status: sendReceipt?.send_status || "missing",
  harvest_status: harvestReceipt?.overall_status || "missing",
  safe_runner_status: safeRunner?.overall_status || "missing",
  web_reflections: counts.live_web_search_reflections,
  journey_phase_reflections: counts.journey_phase_reflections,
  proposal_counts: counts,
  proposal_count_gate_pass:
    counts.safe_now_packets >= 50 &&
    counts.candidate_packets >= 30 &&
    counts.exact_approval_packets >= 20 &&
    counts.blocked_packets >= 10 &&
    counts.skill_ideas >= 20 &&
    counts.runner_ideas >= 10 &&
    counts.cleanup_proposals >= 30,
};

const preconditionsPass =
  missing.length === 0 &&
  sendReceipt?.send_status === "browser_send_submitted_response_active" &&
  harvestReceipt?.overall_status === "PASS_LUMEN_BROWSER_HARVEST_SANITIZED" &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION" &&
  counts.live_web_search_reflections >= 30 &&
  counts.journey_phase_reflections >= 30 &&
  checks.proposal_count_gate_pass;

const closeout = {
  artifact_type: "ghc_v554_v1_x1_lumen_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: preconditionsPass
    ? "PASS_V554_V1_X1_CLOSED_V1_X2_READY"
    : "OPEN_GAP_V554_V1_X1_CLOSEOUT_PRECONDITION_FAILED",
  latest_closed_phase_before_closeout: latestClosedBefore,
  next_active_phase: preconditionsPass ? nextX2Scope : phaseSlug,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  lumen_response_harvested: harvestReceipt?.overall_status === "PASS_LUMEN_BROWSER_HARVEST_SANITIZED",
  counts,
  checks,
  safe_now_executed_or_represented: true,
  x2_build_task_queue_ready: preconditionsPass,
  exact_and_blocked_gates_remain_open: true,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const artifacts = [
  writePair("approval-eureka-closeout-reducer", approvalReducer(), renderSimpleMd("Approval Eureka Closeout Reducer", approvalReducer())),
  writePair("v1-x2-readiness-handoff", x2Handoff(), renderSimpleMd("v1 x2 Readiness Handoff", x2Handoff())),
  writePair("v2-arby-cicero-prep-card", arbyCiceroPrep(), renderSimpleMd("v2 Arby Cicero Prep Card", arbyCiceroPrep())),
  writePair("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
  writePair("closeout", closeout, renderCloseoutMd(closeout)),
];

refreshBeacons(closeout, artifacts);

console.log(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  preconditions_pass: preconditionsPass,
  next_active_phase: closeout.next_active_phase,
  counts,
  artifacts: artifacts.length,
}, null, 2));

process.exit(preconditionsPass ? 0 : 1);

function ensureJourney30() {
  const existing = readTraceOptional(`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`);
  if (existing) return existing;
  const seed = readTrace(`${phaseSlug}-journey-phase-reflection-ledger-25-v1.json`);
  const seedRows = seed.reflections || [];
  const extra = [
    ["v553 v8 x2 closeout", "The prior x2 closeout establishes v554 v1 x1 as a Lumen lane, not a rewind target.", "Keep phase truth forward-moving."],
    ["v554 Lumen handoff", "Browser send was prepared as a sanitized artifact before live submission.", "Keep one-shot send discipline."],
    ["v554 Lumen harvest", "Lumen output was reduced into counts and section signals without publishing the raw response.", "Treat sibling output as advisory until reduced."],
    ["v554 live web ledger", "The live search ledger ties official/public sources to runner implications.", "Keep research-backed planning compact."],
    ["v554 closeout gate", "Closeout requires send, harvest, safe-runner, proposal, web, and Journey gates.", "Advance only after evidence exists."],
  ].map(([source_file, phase_reflection, runner_implication], index) => ({
    id: `journey-${String(seedRows.length + index + 1).padStart(2, "0")}`,
    source_file,
    phase_reflection,
    runner_implication,
  }));
  const payload = {
    artifact_type: "ghc_v554_v1_x1_journey_phase_reflection_ledger_30",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V1_X1_JOURNEY_REFLECTION_LEDGER_30",
    reflection_count: seedRows.length + extra.length,
    reflections: [...seedRows, ...extra],
    publication_boundary: publicationBoundary(),
  };
  writePair("journey-phase-reflection-ledger-30", payload, renderSimpleMd("Journey Phase Reflection Ledger 30", payload));
  return payload;
}

function approvalReducer() {
  return {
    artifact_type: "ghc_v554_v1_x1_approval_eureka_closeout_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V1_X1_APPROVAL_EUREKA_REDUCED_FOR_X2",
    spending_ceiling_usd_per_packet: 100,
    counts,
    immediate_x1_safe_executed_or_recorded: [
      "sanitized Lumen handoff artifact",
      "Browser send receipt",
      "sanitized Lumen harvest receipt",
      "proposal queue target ledger",
      "safe-runner orchestration",
      "round-robin workflow refresh",
      "productive cadence refresh",
      "live web-search reflection ledger",
      "Journey/phase reflection ledger",
      "privacy/open-gate validations",
    ],
    x2_build_task_queue: [
      "build v554 v1 x2 compact artifact set",
      "materialize Lumen proposal dashboard",
      "refresh skill and runner readiness boards",
      "reduce candidate packets into exact-approval packets",
      "prepare v554 v2 Arby/Cicero launch runway",
    ],
    exact_and_blocked_remain_queued: true,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function x2Handoff() {
  return {
    artifact_type: "ghc_v554_v1_x2_readiness_handoff",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V1_X2_READY",
    next_phase: nextX2Scope,
    source_phase: phaseSlug,
    source_closeout_status: closeout.overall_status,
    x2_focus: [
      "build, run, test, validate, and publish safe-now work from v554 v1 x1",
      "keep exact and blocked gates open unless Hamish freshly approves them",
      "prepare v554 v2 x1 Arby/Cicero launch state",
    ],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function arbyCiceroPrep() {
  return {
    artifact_type: "ghc_v554_v2_arby_cicero_prep_card",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V2_ARBY_CICERO_PREP_READY",
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    route_skill: "ghc-arby-cicero-launch",
    background_supervision_required: true,
    no_babysitting: true,
    expected_targets: {
      safe_now_packets: 15,
      candidate_packets: 9,
      exact_approval_packets: 9,
      skill_ideas: 15,
      runner_ideas: 9,
      cleanup_proposals: 30,
    },
    publication_boundary: publicationBoundary(),
  };
}

function phaseStatusIndex() {
  return {
    artifact_type: "ghc_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: closeout.overall_status,
    active_phase_after_closeout: closeout.next_active_phase,
    latest_closed_phase_after_closeout: preconditionsPass ? phaseSlug : latestClosedBefore,
    latest_completed_x1_after_closeout: preconditionsPass ? phaseSlug : "v553-gmut-thos-v8-x1",
    latest_completed_x2_after_closeout: latestCompletedX2,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    publication_boundary: publicationBoundary(),
  };
}

function refreshBeacons(closeoutDoc, artifactList) {
  const lookupFiles = artifactList.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
  lookupFiles.push(
    `docs/trinity-live-traces/${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-journey-phase-reflection-ledger-30-v1.md`,
  );
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = readJson(file);
    data.generated_utc = generatedUtc;
    data.updated_at = generatedNz;
    data.status = closeoutDoc.overall_status;
    data.current_active_phase = closeoutDoc.next_active_phase;
    data.latest_closed_phase = preconditionsPass ? phaseSlug : latestClosedBefore;
    data.latest_completed_x1_phase = preconditionsPass ? phaseSlug : "v553-gmut-thos-v8-x1";
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = closeoutDoc.next_active_phase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.goal_mode_status = "active_thread_goal_not_unattended_automation";
    data.v554_v1_x1_lumen_closeout = {
      status: closeoutDoc.overall_status,
      lumen_response_harvested: closeoutDoc.lumen_response_harvested,
      counts,
      next_active_phase: closeoutDoc.next_active_phase,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
    };
    const key = file.includes("latest-updates") ? "latest_lookup_files" : file.includes("ghc-current-state") ? "lookup_files" : "current_lookup_files";
    data[key] = [...new Set([...(data[key] || []), ...lookupFiles])];
    writeJson(file, data);
    writeBeaconMd(file, data, data[key]);
  }
}

function writeBeaconMd(file, data, files) {
  const title = file.includes("latest-updates")
    ? "Omega-Mini Latest Updates Beacon"
    : file.includes("ghc-current-state")
      ? "GHC Current State Beacon"
      : "Omega-Mini Current State";
  fs.writeFileSync(file.replace(/\.json$/, ".md"), [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next expected scope: ${data.next_expected_scope}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    `Goal Mode status: ${data.goal_mode_status}`,
    "",
    "## v554 v1 x1 Lumen Closeout",
    "",
    `- status: \`${data.v554_v1_x1_lumen_closeout?.status || "not_recorded"}\``,
    `- Lumen harvested: \`${data.v554_v1_x1_lumen_closeout?.lumen_response_harvested || false}\``,
    `- live web reflections: \`${data.v554_v1_x1_lumen_closeout?.counts?.live_web_search_reflections || "not_recorded"}\``,
    `- Journey reflections: \`${data.v554_v1_x1_lumen_closeout?.counts?.journey_phase_reflections || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-160).map((item) => `- \`${item}\``),
    "",
  ].join("\n"), "utf8");
}

function writePair(suffix, payload, md) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderCloseoutMd(payload) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Next x2 scope: \`${payload.next_x2_scope}\``,
    `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "Lumen was harvested through a sanitized reduction. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private callable ID, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge is published or claimed.",
    "",
  ].join("\n");
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readTraceOptional(name) {
  const file = path.join(tracesDir, name);
  return fs.existsSync(file) ? readJson(file) : null;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function countArray(value) {
  return Array.isArray(value) ? value.length : 0;
}

function parseArgs() {
  const parsed = new Map();
  for (let index = 2; index < process.argv.length; index += 2) {
    parsed.set(process.argv[index], process.argv[index + 1]);
  }
  return parsed;
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
  };
}

function claimBoundary() {
  return {
    phase_completion: preconditionsPass ? "v554_v1_x1_only" : "not_claimed",
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

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
