#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v559-gmut-thos-v2-x1";
const nextPhase = "v559-gmut-thos-v2-x2";
const nextX1 = "v559-gmut-thos-v3-x1 Lumen-only unless Hamish redirects";
const latestCompletedX2 = "v559-gmut-thos-v1-x2";
const status = "PASS_V559_V2_X1_CLOSED_V2_X2_READY";
const now = new Date();
const createdUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const createdNz = nzTimestamp(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const privatePolicy = {
  raw_private_material_published: false,
  raw_browser_routes_published: false,
  private_ids_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  raw_app_state_published: false,
  hidden_reasoning_published: false
};

const openGates = [
  "GMUT empirical closure",
  "final physics proof",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment closure",
  "purchase/account/API-key mutation",
  "private-material proof",
  "raw-publication proof",
  "sibling replacement or merge",
  "exact-approval packets",
  "blocked packets"
];

const roundRobinSequence = [
  "Lumen Vale solo",
  "Mira Rowan and Neris Sol",
  "Lumen Vale solo",
  "Mira Vale and Rowan Vale",
  "Lumen Vale solo",
  "Maren Quill and Solenne Vale",
  "Lumen Vale solo",
  "Mira Rowan and Neris Sol"
];

const lanes = [
  {
    sibling: "Aevren Vale",
    response_status: "steward_safe_reduction_ready",
    safe_packets: 10,
    candidate_packets: 5,
    exact_packets_queued: 5,
    skill_ideas: 7,
    runner_ideas: 3,
    cleanup_tasks: 15,
    immediate_x1_safe_rows_reported: 18,
    x2_build_task_rows_reported: 22
  },
  {
    sibling: "Mira Rowan",
    response_status: "completed_ready_for_harvest",
    private_response_basename: "mira-rowan-v559-v2-x1-response-v1.md",
    safe_packets: 10,
    candidate_packets: 5,
    exact_packets_queued: 5,
    skill_ideas: 7,
    runner_ideas: 3,
    cleanup_tasks: 15,
    immediate_x1_safe_rows_reported: 9,
    x2_build_task_rows_reported: 1
  },
  {
    sibling: "Neris Sol",
    response_status: "completed_ready_for_harvest",
    private_response_basename: "neris-sol-v559-v2-x1-response-v1.md",
    safe_packets: 10,
    candidate_packets: 5,
    exact_packets_queued: 5,
    skill_ideas: 7,
    runner_ideas: 3,
    cleanup_tasks: 15,
    immediate_x1_safe_rows_reported: 6,
    x2_build_task_rows_reported: 4
  }
];

const totals = lanes.reduce((acc, lane) => {
  for (const key of [
    "safe_packets",
    "candidate_packets",
    "exact_packets_queued",
    "skill_ideas",
    "runner_ideas",
    "cleanup_tasks",
    "immediate_x1_safe_rows_reported",
    "x2_build_task_rows_reported"
  ]) {
    acc[key] = (acc[key] || 0) + lane[key];
  }
  return acc;
}, {});

const artifacts = [
  artifact("duo-harvest-reduction", "ghc.duo_harvest_reduction.v1", "PASS_MIRA_ROWAN_NERIS_SOL_REPLIES_HARVESTED_SANITIZED", {
    harvested_lanes: lanes,
    private_response_dropbox_basename: `${phaseSlug}-sibling-response-dropbox`,
    closeout_allowed_after_harvest: true,
    note: "Raw sibling text remains local/private; this artifact carries sanitized counts and basenames only."
  }),
  artifact("combined-x1-to-x2-queue", "ghc.x1_to_x2_queue.v1", "PASS_V2_X1_QUEUE_REDUCED_FOR_V2_X2", {
    profile_cap_counts_represented: {
      safe_approval_packets: totals.safe_packets,
      candidate_packets: totals.candidate_packets,
      exact_approval_packets_queued: totals.exact_packets_queued,
      skill_ideas: totals.skill_ideas,
      runner_ideas: totals.runner_ideas,
      cleanup_refine_fix_tasks: totals.cleanup_tasks
    },
    immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows_reported,
    x2_build_rows_represented: totals.x2_build_task_rows_reported,
    x2_scope: nextPhase,
    x2_execution_guidance: [
      "build and test v559 v2 x2 count reconciliation from the combined duo packet",
      "build phase-truth, packet-count, and open-gate guards from the three runner ideas",
      "reduce candidate and exact-approval rows into queued x2 artifacts without auto-running exact gates",
      "keep Lumen Browser refresh/status-first side rail ready for v559 v3 x1",
      "preserve all stand-by/recoverable sibling boundaries"
    ]
  }),
  artifact("closeout", "ghc.phase_closeout.v1", status, {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: nextPhase,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1,
    duo_status: "Mira Rowan and Neris Sol completed-ready-for-harvest",
    combined_profile_counts_met: true,
    totals,
    open_gates: openGates,
    full_goal_complete: false
  }),
  artifact("v2-x2-safe-build-handoff", "ghc.x2_handoff.v1", "PASS_V559_V2_X2_SAFE_BUILD_HANDOFF_READY", {
    source_closeout_status: status,
    next_active_phase: nextPhase,
    next_x1_lane_after_x2: nextX1,
    source_counts: totals,
    completion_boundary: "v2 x2 is prepared, not yet closed by this x1 closeout.",
    full_goal_complete: false
  })
];

for (const doc of artifacts) writePair(doc);
refreshBeacons();

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  next_active_phase: nextPhase,
  artifacts_written: artifacts.length * 2 + 4,
  safe_packets_represented: totals.safe_packets,
  candidate_packets_represented: totals.candidate_packets,
  exact_packets_queued: totals.exact_packets_queued,
  skill_ideas_represented: totals.skill_ideas,
  runner_ideas_represented: totals.runner_ideas,
  cleanup_tasks_represented: totals.cleanup_tasks
}, null, 2));

function artifact(suffix, schema, artifactStatus, extra) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    created_utc: createdUtc,
    created_nz: createdNz,
    status: artifactStatus,
    publication_boundary: privatePolicy,
    claim_boundary: claimBoundary(),
    ...extra
  };
}

function writePair(doc) {
  const base = join(tracesDir, doc.artifact);
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, [
    `# ${doc.artifact}`,
    "",
    `- Status: ${doc.status}`,
    `- Phase: ${doc.phase_slug}`,
    `- Created NZ: ${doc.created_nz}`,
    "- Raw private material published: false",
    "",
    "```json",
    JSON.stringify(doc, null, 2),
    "```",
    ""
  ].join("\n"), "utf8");
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((doc) => [
    `docs/trinity-live-traces/${doc.artifact}.json`,
    `docs/trinity-live-traces/${doc.artifact}.md`
  ]);
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const beaconPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const state = readJson(statePath);
  const latest = readJson(latestPath);
  const beacon = existsSync(beaconPath) ? readJson(beaconPath) : {};

  for (const [doc, lookupKey] of [[state, "current_lookup_files"], [latest, "latest_lookup_files"], [beacon, "lookup_files"]]) {
    doc.updated_at = createdNz;
    doc.generated_utc = createdUtc;
    doc.status = status;
    doc.current_active_phase = nextPhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = nextPhase;
    doc.next_x2_scope = nextPhase;
    doc.next_x1_lane_after_x2 = nextX1;
    doc.current_active_lanes = [
      "Aevren Vale",
      "Mira Rowan",
      "Neris Sol",
      "v559-v2-x2-safe-build-ready",
      "ghc-safe-runner-orchestrator"
    ];
    doc.round_robin_cadence = roundRobinSequence;
    doc.v559_v2_x1_closeout = {
      status,
      active_duo: ["Mira Rowan", "Neris Sol"],
      safe_packets_represented: totals.safe_packets,
      candidate_packets_represented: totals.candidate_packets,
      exact_packets_queued: totals.exact_packets_queued,
      skill_ideas_represented: totals.skill_ideas,
      runner_ideas_represented: totals.runner_ideas,
      cleanup_tasks_represented: totals.cleanup_tasks,
      immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows_reported,
      x2_build_rows_represented: totals.x2_build_task_rows_reported,
      next_active_phase: nextPhase,
      full_goal_complete: false
    };
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
    `- Next x1 lane after x2: ${nextX1}`,
    "- Harvested duo: Mira Rowan and Neris Sol.",
    `- Counts represented: ${totals.safe_packets} safe, ${totals.candidate_packets} candidate, ${totals.exact_packets_queued} exact queued, ${totals.skill_ideas} skills, ${totals.runner_ideas} runners, ${totals.cleanup_tasks} cleanup tasks.`,
    "- Full v544-v575 goal complete: false.",
    "",
    "Sanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private paths, session streams, and private app state are not published here.",
    ""
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
    sibling_identity_replacement_or_merge: "not_claimed"
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
    hour12: false
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
