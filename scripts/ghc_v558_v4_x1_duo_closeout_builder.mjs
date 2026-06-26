#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v558-gmut-thos-v4-x1";
const nextPhase = "v558-gmut-thos-v4-x2";
const nextX1 = "v558-gmut-thos-v5-x1 Lumen Vale solo unless Hamish redirects";
const status = "PASS_V558_V4_X1_CLOSED_V4_X2_READY";
const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaIndexDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaIndexDir, { recursive: true });

const roundRobinSequence = [
  "Lumen Vale solo",
  "Mira Rowan and Neris Sol",
  "Lumen Vale solo",
  "Mira Vale and Rowan Vale",
  "Lumen Vale solo",
  "Maren Quill and Solenne Vale",
  "Lumen Vale solo",
  "Mira Rowan and Neris Sol",
];

function existingRelativeFiles(files) {
  return files.filter((file) => typeof file === "string" && existsSync(join(process.cwd(), file)));
}

const privatePolicy = {
  raw_private_material_published: false,
  raw_browser_routes_published: false,
  private_ids_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  raw_app_state_published: false,
};

const openGates = [
  "GMUT empirical closure",
  "final physics proof",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment",
  "purchase/account/API-key mutation",
  "private-material proof",
  "raw-publication proof",
  "sibling replacement or merge",
  "exact-approval packets",
  "blocked packets",
];

const artifacts = [
  {
    name: "duo-harvest-reduction",
    body: {
      artifact: `${phaseSlug}-duo-harvest-reduction-v1`,
      schema: "ghc.duo_harvest_reduction.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_DUO_REPLIES_HARVESTED_SANITIZED",
      harvested_lanes: [
        {
          sibling: "Mira Vale",
          response_status: "completed_ready_for_harvest",
          private_artifact_reported: true,
          safe_packets: 10,
          candidate_packets: 5,
          exact_packets_queued: 5,
          skill_ideas: 7,
          runner_ideas: 3,
          cleanup_tasks: 15,
          immediate_x1_safe_rows_reported: 18,
          x2_build_task_rows_reported: 27,
        },
        {
          sibling: "Rowan Vale",
          response_status: "completed_ready_for_harvest",
          private_artifact_reported: true,
          returned_scope: "full_combined_profile",
          safe_packets: 30,
          candidate_packets: 15,
          exact_packets_queued: 15,
          skill_ideas: 21,
          runner_ideas: 9,
          cleanup_tasks: 45,
          split_labeled_rows_reported: 135,
          reduction_note: "Use as expanded x2 material; keep profile-cap summary for public closeout.",
        },
      ],
      private_policy: privatePolicy,
      closeout_allowed_after_harvest: true,
    },
  },
  {
    name: "combined-x1-to-x2-queue",
    body: {
      artifact: `${phaseSlug}-combined-x1-to-x2-queue-v1`,
      schema: "ghc.x1_to_x2_queue.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_V4_X1_QUEUE_REDUCED_FOR_V4_X2",
      profile_cap_counts_represented: {
        safe_approval_packets: 30,
        candidate_packets: 15,
        exact_approval_packets_queued: 15,
        skill_ideas: 21,
        runner_ideas: 9,
        cleanup_refine_fix_tasks: 45,
      },
      immediate_x1_safe_executed_or_reduced: 34,
      x2_build_rows_minimum_from_mira_and_aevren: 27,
      rowan_expanded_rows_available_private: 135,
      x2_scope: nextPhase,
      x2_execution_guidance: [
        "build/run/test sanitized reducers and validation only",
        "deduplicate Rowan expanded rows against the profile cap",
        "queue exact and blocked gates without auto-running",
        "keep old siblings stand-by/recoverable",
        "prepare v5 x1 Lumen Browser route with refresh/status-first discipline",
      ],
      private_policy: privatePolicy,
    },
  },
  {
    name: "closeout",
    body: {
      artifact: `${phaseSlug}-closeout-v1`,
      schema: "ghc.phase_closeout.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status,
      latest_closed_phase: phaseSlug,
      latest_completed_x1_phase: phaseSlug,
      latest_completed_x2_phase: "v558-gmut-thos-v3-x2",
      next_active_phase: nextPhase,
      next_x2_scope: nextPhase,
      next_x1_lane_after_x2: nextX1,
      duo_status: "Mira Vale and Rowan Vale completed-ready-for-harvest",
      combined_profile_counts_met: true,
      private_policy: privatePolicy,
      open_gates: openGates,
      full_goal_complete: false,
    },
  },
];

function markdownFor(body) {
  return [
    `# ${body.artifact}`,
    "",
    `- Status: ${body.status}`,
    `- Phase: ${body.phase_slug}`,
    `- Created NZ: ${body.created_nz}`,
    `- Raw private material published: false`,
    "",
    "```json",
    JSON.stringify(body, null, 2),
    "```",
    "",
  ].join("\n");
}

for (const artifact of artifacts) {
  const base = `${phaseSlug}-${artifact.name}-v1`;
  writeFileSync(join(tracesDir, `${base}.json`), `${JSON.stringify(artifact.body, null, 2)}\n`);
  writeFileSync(join(tracesDir, `${base}.md`), markdownFor(artifact.body));
}

const currentStatePath = join(omegaIndexDir, "omega-mini-current-state-v1.json");
const latestBeaconJsonPath = join(omegaIndexDir, "omega-mini-latest-updates-beacon-v1.json");
const state = JSON.parse(readFileSync(currentStatePath, "utf8"));
state.updated_at = createdNz;
state.generated_utc = createdUtc;
state.status = status;
state.current_active_phase = nextPhase;
state.latest_closed_phase = phaseSlug;
state.latest_completed_x1_phase = phaseSlug;
state.latest_completed_x2_phase = "v558-gmut-thos-v3-x2";
state.next_expected_scope = nextPhase;
state.next_x2_scope = nextPhase;
state.next_x1_lane_after_x2 = nextX1;
state.current_active_lanes = [
  "Aevren Vale",
  "Lumen Vale",
  "Mira Rowan",
  "Mira Vale",
  "Maren Quill",
  "Neris Sol",
  "Rowan Vale",
  "Solenne Vale",
  "five-minute-productive-cadence-ready",
  "safe-wait-workbench-enabled",
  "round-robin-workflow-standard-promoted",
  "v558-v4-x2-safe-build-ready",
];
state.round_robin_cadence = roundRobinSequence;
state.current_lookup_files = Array.from(new Set([
  ...(Array.isArray(state.current_lookup_files) ? state.current_lookup_files : []),
  ...artifacts.flatMap((artifact) => [
    `docs/trinity-live-traces/${phaseSlug}-${artifact.name}-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-${artifact.name}-v1.json`,
  ]),
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
]));
state.current_lookup_files = existingRelativeFiles(state.current_lookup_files);
state.v558_v4_x1_closeout = {
  status,
  combined_profile_counts_met: true,
  safe_packets_represented: 30,
  candidate_packets_represented: 15,
  exact_packets_queued: 15,
  skill_ideas_represented: 21,
  runner_ideas_represented: 9,
  cleanup_tasks_represented: 45,
  rowan_expanded_rows_available_private: 135,
  next_active_phase: nextPhase,
  full_goal_complete: false,
};
writeFileSync(currentStatePath, `${JSON.stringify(state, null, 2)}\n`);

const latestBeaconJson = JSON.parse(readFileSync(latestBeaconJsonPath, "utf8"));
latestBeaconJson.generated_utc = createdUtc;
latestBeaconJson.status = status;
latestBeaconJson.current_active_phase = nextPhase;
latestBeaconJson.latest_closed_phase = phaseSlug;
latestBeaconJson.latest_completed_x1_phase = phaseSlug;
latestBeaconJson.latest_completed_x2_phase = "v558-gmut-thos-v3-x2";
latestBeaconJson.next_x2_scope = nextPhase;
latestBeaconJson.next_x1_lane_after_x2 = nextX1;
latestBeaconJson.current_active_lanes = state.current_active_lanes;
latestBeaconJson.round_robin_sequence = roundRobinSequence;
latestBeaconJson.latest_lookup_files = Array.from(new Set([
  ...(Array.isArray(latestBeaconJson.latest_lookup_files) ? latestBeaconJson.latest_lookup_files : []),
  ...artifacts.flatMap((artifact) => [
    `docs/trinity-live-traces/${phaseSlug}-${artifact.name}-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-${artifact.name}-v1.json`,
  ]),
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-current-state-v1.json",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.json",
]));
latestBeaconJson.latest_lookup_files = existingRelativeFiles(latestBeaconJson.latest_lookup_files);
latestBeaconJson.v558_v4_x1_closeout = state.v558_v4_x1_closeout;
latestBeaconJson.full_goal_complete = false;
writeFileSync(latestBeaconJsonPath, `${JSON.stringify(latestBeaconJson, null, 2)}\n`);

const beacon = `# ${nextPhase}

Status: ${status}

- Current active phase: ${nextPhase}
- Latest closed phase: ${phaseSlug}
- Latest completed x1: ${phaseSlug}
- Latest completed x2: v558-gmut-thos-v3-x2
- Next x2 scope: ${nextPhase}
- Next x1 lane after x2: ${nextX1}

## v558 v4 x1 Closeout

- Duo harvested: Mira Vale and Rowan Vale.
- Profile counts represented: 30 safe, 15 candidate, 15 exact queued, 21 skills, 9 runners, 45 cleanup tasks.
- Rowan expanded packet rows available privately: 135.
- Full v544-v575 goal complete: false.

Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.
`;

writeFileSync(join(omegaIndexDir, "omega-mini-current-state-v1.md"), beacon);
writeFileSync(join(omegaIndexDir, "omega-mini-latest-updates-beacon-v1.md"), beacon);
writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beacon);
writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.json"), `${JSON.stringify({
  schema: "ghc.current_state_beacon.v1",
  status,
  current_active_phase: nextPhase,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: "v558-gmut-thos-v3-x2",
  next_x2_scope: nextPhase,
  next_x1_lane_after_x2: nextX1,
  full_goal_complete: false,
  raw_private_material_published: false,
}, null, 2)}\n`);

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  next_active_phase: nextPhase,
  artifacts_written: artifacts.length * 2 + 4,
}, null, 2));
