#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v559-gmut-thos-v4-x1";
const nextPhase = "v559-gmut-thos-v4-x2";
const latestCompletedX2 = "v559-gmut-thos-v3-x2";
const nextX1LaneAfterX2 = "v559-gmut-thos-v5-x1 Lumen-only unless Hamish redirects";
const status = "PASS_V559_V4_X1_CLOSED_V4_X2_READY";
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const required = [
  `${phaseSlug}-mira-vale-rowan-vale-launch-receipt-v1.json`,
  `${phaseSlug}-duo-harvest-reduction-v1.json`,
  `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`,
  `${phaseSlug}-closeout-prep-v1.json`,
];

const missing = required.filter((file) => !existsSync(join(tracesDir, file)));
if (missing.length) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V559_V4_X1_CLOSEOUT_REQUIRED_ARTIFACTS_MISSING",
    phase_slug: phaseSlug,
    missing,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const launch = readJson(join(tracesDir, `${phaseSlug}-mira-vale-rowan-vale-launch-receipt-v1.json`));
const harvest = readJson(join(tracesDir, `${phaseSlug}-duo-harvest-reduction-v1.json`));
const queue = readJson(join(tracesDir, `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`));
const counts = queue.profile_cap_counts_represented || harvest.profile_cap_counts_represented || {};
const closeoutAllowed =
  launch.status === "PASS_V559_V4_X1_MIRA_VALE_ROWAN_VALE_LAUNCHED_BACKGROUND_SUPERVISED" &&
  harvest.status === "PASS_V559_V4_X1_DUO_HARVEST_REDUCED_FOR_V4_X2" &&
  Array.isArray(queue.rows) &&
  queue.rows.length >= 135;

const closeoutStatus = closeoutAllowed ? status : "OPEN_GAP_V559_V4_X1_CLOSEOUT_GATES_INCOMPLETE";

const artifacts = [
  artifact("duo-closeout", "ghc.duo_x1_closeout.v1", closeoutStatus, {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    launch_status: launch.status,
    harvest_status: harvest.status,
    queue_rows: queue.rows.length,
    profile_cap_counts_represented: counts,
    full_goal_complete: false,
  }),
  artifact("v4-x2-safe-build-handoff", "ghc.x2_handoff.v1", closeoutAllowed
    ? "PASS_V559_V4_X2_SAFE_BUILD_HANDOFF_READY"
    : "OPEN_GAP_V559_V4_X2_HANDOFF_NOT_READY", {
    source_x1_phase: phaseSlug,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    source_queue_basename: `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`,
    profile_cap_counts_represented: counts,
    exact_boundary: "exact approval packets remain queued/open, not auto-run",
    recomposed_duo_rule: "Mira Vale and Rowan Vale are active recomposed lanes; stand-by siblings remain recoverable and not replaced.",
  }),
];

for (const doc of artifacts) writePair(doc);
if (closeoutAllowed) refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
  safe_packets_represented: counts.safe_approval_packets || 0,
  candidate_packets_represented: counts.candidate_packets || 0,
  exact_packets_queued: counts.exact_approval_packets_queued || 0,
  skill_ideas_represented: counts.skill_ideas || 0,
  runner_ideas_represented: counts.runner_ideas || 0,
  cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
  queue_rows: queue.rows.length,
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
  const base = join(process.cwd(), doc.artifact);
  writeJson(`${base}.json`, doc);
  const lines = [
    `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private path values, session streams, private app state, private dumps, and hidden reasoning are not published.",
    "",
  ];
  if (doc.next_active_phase) lines.push(`Next active phase: ${doc.next_active_phase}`, "");
  if (doc.next_x1_lane_after_x2) lines.push(`Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "");
  if (doc.profile_cap_counts_represented) {
    lines.push("## Counts", "");
    for (const [key, value] of Object.entries(doc.profile_cap_counts_represented)) lines.push(`- ${key}: ${value}`);
    lines.push("");
  }
  writeFileSync(`${base}.md`, `${lines.join("\n")}\n`, "utf8");
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
    doc.current_active_phase = nextPhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = nextPhase;
    doc.next_x2_scope = nextPhase;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.current_active_lanes = [
      "Aevren Vale",
      "v559-v4-x2-safe-build-ready",
      "ghc-safe-runner-orchestrator",
      "ghc-mira-vale-rowan-vale-launch",
    ];
    doc.v559_v4_x1_duo_closeout = {
      status,
      safe_packets_represented: counts.safe_approval_packets || 0,
      candidate_packets_represented: counts.candidate_packets || 0,
      exact_packets_queued: counts.exact_approval_packets_queued || 0,
      skill_ideas_represented: counts.skill_ideas || 0,
      runner_ideas_represented: counts.runner_ideas || 0,
      cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
      queue_rows: queue.rows.length,
      next_active_phase: nextPhase,
      full_goal_complete: false,
    };
    doc.full_goal_complete = false;
    doc[lookupKey] = existingRelativeFiles([...(Array.isArray(doc[lookupKey]) ? doc[lookupKey] : []), ...lookup]);
  }

  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);

  const md = [
    `# ${nextPhase}`,
    "",
    `Status: ${status}`,
    "",
    `- Current active phase: ${nextPhase}`,
    `- Latest closed phase: ${phaseSlug}`,
    `- Latest completed x1: ${phaseSlug}`,
    `- Latest completed x2: ${latestCompletedX2}`,
    `- Next x2 scope: ${nextPhase}`,
    `- Next x1 lane after x2: ${nextX1LaneAfterX2}`,
    `- Duo queue rows: ${queue.rows.length}.`,
    `- Counts represented: ${counts.safe_approval_packets || 0} safe, ${counts.candidate_packets || 0} candidate, ${counts.exact_approval_packets_queued || 0} exact queued, ${counts.skill_ideas || 0} skills, ${counts.runner_ideas || 0} runners, ${counts.cleanup_refine_fix_tasks || 0} cleanup tasks.`,
    "- Full v544-v575 goal complete: false.",
    "",
    "Sanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private path values, session streams, and private app state are not published here.",
    "",
  ].join("\n");
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
