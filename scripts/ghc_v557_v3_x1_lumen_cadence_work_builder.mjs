#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v557-gmut-thos-v3-x1";
const nextX2Scope = "v557-gmut-thos-v3-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const latest = readJson(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"));
const ghc = readJson(path.join(tracesDir, "ghc-current-state-beacon-v1.json"));
const sendReceipt = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`));
const startup = readJson(path.join(tracesDir, `${phaseSlug}-main-startup-context-v1.json`));
const prepared = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-handoff-prepared-v1.json`));

const immediateSafeWork = [
  task("v3x1-safe-01", "Record live Browser send as active under background supervision", "receipt_status", "completed_now"),
  task("v3x1-safe-02", "Preserve no-duplicate-send guard while Lumen response is active", "browser_guard", "completed_now"),
  task("v3x1-safe-03", "Classify Lumen-only proposal targets into immediate_x1_safe and x2_build_task lanes", "queue_shaping", "completed_now"),
  task("v3x1-safe-04", "Seed v557 v3 x2 build queue without executing exact or blocked work", "x2_queue_seed", "completed_now"),
  task("v3x1-safe-05", "Refresh open-gate rail for proof, canon, legal, deployment, account, API-key, raw-publication, and sibling-merge boundaries", "open_gate_check", "completed_now"),
  task("v3x1-safe-06", "Add privacy publication firewall checks to the active Lumen phase workboard", "privacy_check", "completed_now"),
  task("v3x1-safe-07", "Prepare source/reflection ledger seed slots for Trinity Mandala planning", "reflection_seed", "queued_safe_next"),
  task("v3x1-safe-08", "Prepare Journey/phase reflection seed slots for Lumen harvest reduction", "journey_reflection_seed", "queued_safe_next"),
  task("v3x1-safe-09", "Keep startup, compact restart, closeout, orchestration, full-tools, Lumen launch, background supervision, retry, safe-runner, and web-ledger skills in the refresh set", "tool_refresh", "completed_now"),
  task("v3x1-safe-10", "Record that Lumen lane closeout is disallowed until completed-ready-for-harvest or formal retry/open-gap", "completion_boundary", "completed_now"),
  task("v3x1-safe-11", "Prepare compact-pause recovery card inputs if Codex compacts during the active Lumen lane", "compact_restart_seed", "queued_safe_next"),
  task("v3x1-safe-12", "Prepare validation bundle inputs for JSON parse, current-state guard, diff hygiene, privacy scan, and drive posture", "validation_seed", "queued_safe_next"),
];

const x2BuildQueueSeed = [
  x2("v3x2-build-01", "Reduce Lumen response into 50 safe, 30 candidate, 20 exact, 10 blocked, 20 skill, 10 runner, and 30 cleanup buckets after harvest"),
  x2("v3x2-build-02", "Execute authorized safe-now Lumen/Aevren packets through safe-runner orchestration"),
  x2("v3x2-build-03", "Build or refresh the Lumen response reducer for v557 v3 x1"),
  x2("v3x2-build-04", "Build the v557 v3 x2 execution index and closeout delegate behind the main closeout route"),
  x2("v3x2-build-05", "Record 50 web and 50 Journey/phase reflections for the Aevren-only x2 build phase when research-backed scope is active"),
  x2("v3x2-build-06", "Refresh skill and runner bank status, preserving full-tools private support and omega-mini-2 sanitized publication"),
  x2("v3x2-build-07", "Validate current-state beacons, latest-updates beacon, and GHC current-state beacon after harvest reduction"),
  x2("v3x2-build-08", "Publish privacy/open-gate rail after x2 execution without claiming closed proof gates"),
  x2("v3x2-build-09", "Prepare the v557 v4 x1 triad startup handoff for Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects"),
  x2("v3x2-build-10", "Commit and remote-verify sanitized omega-mini-2 artifacts only after validation passes"),
];

const artifact = {
  artifact_type: "ghc_v557_v3_x1_lumen_cadence_workboard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V3_X1_LUMEN_CADENCE_WORKBOARD_BUILT",
  latest_closed_phase: current.latest_closed_phase,
  latest_completed_x1_phase: current.latest_completed_x1_phase,
  latest_completed_x2_phase: current.latest_completed_x2_phase,
  current_active_phase: phaseSlug,
  next_x2_scope: nextX2Scope,
  lumen_lane_status: {
    send_status: sendReceipt.send_status,
    background_supervision: "active_fresh",
    duplicate_send_allowed: false,
    harvest_status: "pending",
    closeout_allowed_now: false,
  },
  checks: {
    current_state_status: current.status,
    latest_updates_status: latest.status,
    ghc_current_state_status: ghc.status,
    startup_status: startup.overall_status || startup.status,
    prepared_handoff_status: prepared.overall_status,
    send_receipt_status: sendReceipt.overall_status,
  },
  proposal_targets: {
    safe_packets_total: 50,
    candidate_packets_total: 30,
    exact_approval_packets_total: 20,
    blocked_packets_total: 10,
    skill_ideas_total: 20,
    runner_ideas_total: 10,
    cleanup_proposals_total: 30,
    web_reflections_per_active_lane: 25,
    journey_reflections_per_active_lane: 25,
  },
  immediate_x1_safe_work: immediateSafeWork,
  x2_build_queue_seed: x2BuildQueueSeed,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
  next_action: "continue_productive_safe_work_then_harvest_lumen_at_next_natural_pause",
};

writePair("lumen-cadence-workboard", artifact, renderMd(artifact));
refreshBeacons(artifact);

process.stdout.write(JSON.stringify({
  status: artifact.overall_status,
  phase_slug: phaseSlug,
  lumen_lane_status: artifact.lumen_lane_status.background_supervision,
  immediate_x1_safe_work: immediateSafeWork.length,
  x2_build_queue_seed: x2BuildQueueSeed.length,
  closeout_allowed_now: false,
}, null, 2) + "\n");

function task(id, title, lane, status) {
  return {
    id,
    title,
    safety_bucket: "safe_now",
    execution_lane: "immediate_x1_safe",
    work_type: lane,
    status,
  };
}

function x2(id, title) {
  return {
    id,
    title,
    safety_bucket: "safe_now_or_candidate_reduced_after_harvest",
    execution_lane: "x2_build_task",
    status: "queued_for_v557_gmut_thos_v3_x2",
  };
}

function refreshBeacons(artifact) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-cadence-workboard-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-cadence-workboard-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = artifact.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2Scope;
    doc.v557_v3_x1_lumen = {
      status: artifact.overall_status,
      browser_send_status: artifact.lumen_lane_status.send_status,
      background_supervision: artifact.lumen_lane_status.background_supervision,
      duplicate_send_allowed: false,
      closeout_allowed_now: false,
      immediate_x1_safe_work_count: artifact.immediate_x1_safe_work.length,
      x2_build_queue_seed_count: artifact.x2_build_queue_seed.length,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderMd(data) {
  return [
    `# ${phaseSlug} Lumen Cadence Workboard`,
    "",
    `Status: \`${data.overall_status}\``,
    `Lumen lane: \`${data.lumen_lane_status.background_supervision}\``,
    `Send status: \`${data.lumen_lane_status.send_status}\``,
    `Closeout allowed now: \`${data.lumen_lane_status.closeout_allowed_now}\``,
    "",
    "## Immediate x1 Safe Work",
    "",
    ...data.immediate_x1_safe_work.map((item) => `- ${item.id}: ${item.title} (${item.status})`),
    "",
    "## v3 x2 Build Queue Seed",
    "",
    ...data.x2_build_queue_seed.map((item) => `- ${item.id}: ${item.title}`),
    "",
    "## Boundary",
    "",
    "Lumen is active under background supervision. This workboard does not close the Lumen session or phase. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private app state, session stream, private dump, private callable ID, proof closure, or sibling merge claim is published.",
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
    "## v557 v3 x1 Lumen",
    "",
    `- status: \`${doc.v557_v3_x1_lumen?.status || "not_recorded"}\``,
    `- browser send status: \`${doc.v557_v3_x1_lumen?.browser_send_status || "not_recorded"}\``,
    `- background supervision: \`${doc.v557_v3_x1_lumen?.background_supervision || "not_recorded"}\``,
    `- closeout allowed now: \`${doc.v557_v3_x1_lumen?.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
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
    private_app_state_published: false,
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

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
