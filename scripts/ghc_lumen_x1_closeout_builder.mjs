#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const nextPhase = args.get("--next-phase") || phaseSlug.replace(/-x1$/, "-x2");
const latestCompletedX2 = args.get("--latest-completed-x2") || readCurrent("latest_completed_x2_phase") || "not_recorded";
const nextX1LaneAfterX2 = args.get("--next-x1-after-x2") || readCurrent("next_x1_lane_after_x2") || "not_recorded";
const status = args.get("--status") || "PASS_LUMEN_X1_CLOSED_NEXT_X2_READY";
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const requiredFiles = [
  `${phaseSlug}-lumen-browser-send-receipt-v1.json`,
  `${phaseSlug}-lumen-harvest-reduction-v1.json`,
  `${phaseSlug}-lumen-sanitized-proposal-queue-v1.json`,
  `${phaseSlug}-closeout-prep-v1.json`,
];

const missing = requiredFiles.filter((file) => !existsSync(join(tracesDir, file)));
if (missing.length) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_LUMEN_X1_CLOSEOUT_REQUIRED_ARTIFACTS_MISSING",
    phase_slug: phaseSlug,
    missing,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const send = readJson(join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`));
const harvest = readJson(join(tracesDir, `${phaseSlug}-lumen-harvest-reduction-v1.json`));
const queue = readJson(join(tracesDir, `${phaseSlug}-lumen-sanitized-proposal-queue-v1.json`));
const counts = queue.expected_profile || queue.profile_cap_counts_represented || harvest.expected_profile || harvest.expected_counts || {};
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const acceptableSendStatuses = new Set([
  "browser_send_submitted_response_active",
  "browser_send_submitted_response_completed_ready_for_harvest",
]);
const closeoutAllowed =
  acceptableSendStatuses.has(send.send_status) &&
  String(harvest.harvest_status || "").includes("harvest") &&
  rows.length > 0;
const closeoutStatus = closeoutAllowed ? status : "OPEN_GAP_LUMEN_X1_CLOSEOUT_GATES_INCOMPLETE";
const queueCounts = queue.queue_counts || {};

const artifacts = [
  artifact("lumen-closeout", "ghc.lumen_x1_closeout.v2", closeoutStatus, {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lumen_send_status: send.send_status,
    lumen_harvest_status: harvest.harvest_status,
    queue_rows: rows.length,
    queue_counts: queueCounts,
    profile_cap_counts_represented: counts,
    full_goal_complete: false,
  }),
  artifact("x2-safe-build-handoff", "ghc.x2_handoff.v2", closeoutAllowed
    ? "PASS_LUMEN_X2_SAFE_BUILD_HANDOFF_READY"
    : "OPEN_GAP_LUMEN_X2_HANDOFF_NOT_READY", {
    source_x1_phase: phaseSlug,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    source_queue_basename: `${phaseSlug}-lumen-sanitized-proposal-queue-v1.json`,
    profile_cap_counts_represented: counts,
    queue_rows: rows.length,
    immediate_x1_safe_rows: queueCounts.by_execution_lane?.immediate_x1_safe || 0,
    x2_build_task_rows: queueCounts.by_execution_lane?.x2_build_task || 0,
    exact_and_blocked_boundary: "exact approval and blocked packets remain queued/open unless freshly authorized",
    lumen_browser_rule: "fresh DOM/status refresh first; safe reload only when no active response and no unsent composer text; visible contenteditable fallback is valid after refresh",
  }),
];

for (const doc of artifacts) writePair(doc);
if (closeoutAllowed) refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
  latest_completed_x1_phase: closeoutAllowed ? phaseSlug : null,
  safe_packets_represented: counts.safe_approval_packets || 0,
  candidate_packets_represented: counts.candidate_packets || 0,
  exact_packets_queued: counts.exact_approval_packets_queued || 0,
  blocked_packets_queued: counts.blocked_packets_queued || 0,
  skill_ideas_represented: counts.skill_ideas || 0,
  runner_ideas_represented: counts.runner_ideas || 0,
  cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
  queue_rows: rows.length,
  immediate_x1_safe_rows: queueCounts.by_execution_lane?.immediate_x1_safe || 0,
  x2_build_task_rows: queueCounts.by_execution_lane?.x2_build_task || 0,
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
    console.error(`Usage: node scripts/ghc_lumen_x1_closeout_builder.mjs ${flag} <value>`);
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
  const base = join(process.cwd(), doc.artifact);
  writeJson(`${base}.json`, doc);
  const lines = [
    `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.",
    "",
  ];
  if (doc.next_active_phase) lines.push(`Next active phase: ${doc.next_active_phase}`, "");
  if (doc.next_x1_lane_after_x2) lines.push(`Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "");
  if (doc.profile_cap_counts_represented) {
    lines.push("## Counts", "");
    for (const [key, value] of Object.entries(doc.profile_cap_counts_represented)) lines.push(`- ${key}: ${value}`);
    lines.push("");
  }
  if (doc.queue_rows !== undefined) lines.push(`Queue rows: ${doc.queue_rows}`, "");
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
      `${nextPhase}-safe-build-ready`,
      "ghc-safe-runner-orchestrator",
      "ghc-lumen-launch",
    ];
    doc.lumen_x1_closeout = {
      status,
      phase_slug: phaseSlug,
      queue_rows: rows.length,
      profile_counts_represented: counts,
      next_active_phase: nextPhase,
      full_goal_complete: false,
    };
    doc.lumen_browser_refresh_rule = "fresh DOM/status refresh before unavailable claims; no reload during active response or unsent composer text; visible contenteditable fallback after safe refresh";
    doc.full_goal_complete = false;
    doc[lookupKey] = existingRelativeFiles([...(Array.isArray(doc[lookupKey]) ? doc[lookupKey] : []), ...lookup]);
  }

  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);
  const beaconMd = [
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
    "- Lumen Browser route: fresh DOM/status refresh first; safe reload only when no active response and no unsent composer text; contenteditable fallback is valid after refresh.",
    `- Lumen queue rows: ${rows.length}.`,
    `- Counts represented: ${counts.safe_approval_packets || 0} safe, ${counts.candidate_packets || 0} candidate, ${counts.exact_approval_packets_queued || 0} exact queued, ${counts.blocked_packets_queued || 0} blocked queued, ${counts.skill_ideas || 0} skills, ${counts.runner_ideas || 0} runners, ${counts.cleanup_refine_fix_tasks || 0} cleanup tasks.`,
    "- Full v544-v575 goal complete: false.",
    "",
    "Sanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private paths, session streams, and private app state are not published here.",
    "",
  ].join("\n");
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), beaconMd, "utf8");
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), beaconMd, "utf8");
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beaconMd, "utf8");
}

function readCurrent(key) {
  try {
    return readJson(join(omegaDir, "omega-mini-current-state-v1.json"))[key];
  } catch {
    return null;
  }
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
