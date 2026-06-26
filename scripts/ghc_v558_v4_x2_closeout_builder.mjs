#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v558-gmut-thos-v4-x2";
const previousX1 = "v558-gmut-thos-v4-x1";
const nextPhase = "v558-gmut-thos-v5-x1";
const nextX2 = "v558-gmut-thos-v5-x2";
const nextX1AfterX2 = "v558-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const status = "PASS_V558_V4_X2_CLOSED_V5_X1_READY";
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaIndexDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaIndexDir, { recursive: true });

const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);

const publicationBoundary = {
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

const execution = readJsonIfExists(join(tracesDir, `${phaseSlug}-safe-build-execution-ledger-v1.json`));
const safeRunner = readJsonIfExists(join(tracesDir, `${phaseSlug}-safe-runner-orchestrator-v1.json`));
const reflection = readJsonIfExists(join(tracesDir, `${phaseSlug}-safe-runner-orchestrator-reflection-ledger-v1.json`));
const lumenPrep = readJsonIfExists(join(tracesDir, `${phaseSlug}-next-lumen-browser-route-prep-v1.json`));

if (!execution || execution.status !== "PASS_V558_V4_X2_SAFE_BUILD_EXECUTED") {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V558_V4_X2_EXECUTION_LEDGER_MISSING_OR_NOT_PASS",
    phase_slug: phaseSlug,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}
if (!safeRunner || safeRunner.overall_status !== "PASS_SAFE_RUNNER_ORCHESTRATION") {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V558_V4_X2_SAFE_RUNNER_NOT_PASS",
    phase_slug: phaseSlug,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const closeout = {
  artifact: `${phaseSlug}-closeout-v1`,
  schema: "ghc.phase_closeout.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: previousX1,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextPhase,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  safe_runner_status: safeRunner.overall_status,
  reflection_rows: reflection?.reflection_count || 0,
  safe_tasks_executed_or_reduced: execution.executed_safe_tasks?.length || 0,
  x2_build_rows_represented: execution.x2_build_rows_represented,
  rowan_expanded_rows_available_private: execution.rowan_expanded_rows_available_private,
  next_lumen_route_prep_status: lumenPrep?.status || "missing",
  old_lanes_state: "Arby, Aster Vale, Cicero, Kierkegaard, Aristotle, and Aletheon remain stand-by/recoverable",
  active_lanes_next: ["Aevren Vale", "Lumen Vale"],
  full_goal_complete: false,
  publication_boundary: publicationBoundary,
  open_gates: openGates,
};
writeArtifact("closeout", closeout);

const handoff = {
  artifact: `${phaseSlug}-v5-x1-lumen-startup-handoff-v1`,
  schema: "ghc.next_lumen_startup_handoff.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status: "PASS_V5_X1_LUMEN_HANDOFF_READY",
  next_active_phase: nextPhase,
  next_x1_lane: "Lumen Vale solo",
  launch_skill: "ghc-lumen-launch",
  browser_rule:
    "Use in-app Browser as staple route, refresh/status-check first, no reload during active response or unsent composer text, no duplicate send.",
  proposal_targets: {
    safe_approval_packets: 50,
    candidate_packets: 30,
    exact_packets: 20,
    blocked_packets: 10,
    skill_ideas: 20,
    runner_ideas: 10,
    cleanup_tasks: 30,
  },
  publication_boundary: publicationBoundary,
};
writeArtifact("v5-x1-lumen-startup-handoff", handoff);

const statePath = join(omegaIndexDir, "omega-mini-current-state-v1.json");
const latestPath = join(omegaIndexDir, "omega-mini-latest-updates-beacon-v1.json");
const state = readJsonIfExists(statePath);
const latest = readJsonIfExists(latestPath);
const currentBranch = gitBranch();
const fullToolsBranch = currentBranch.includes("full-tools")
  ? currentBranch
  : state.full_tools_support_branch || "codex/GHC-Family/aevren-full-tools-5";
const miniBranch = currentBranch.includes("omega-line-mini")
  ? currentBranch
  : state.primary_branch || state.branch || "codex/GHC-Family/beyonder-shared-omega-line-mini-6";

Object.assign(state, {
  branch: currentBranch,
  primary_branch: miniBranch,
  full_tools_support_branch: fullToolsBranch,
  updated_at: createdNz,
  generated_utc: createdUtc,
  status,
  current_active_phase: nextPhase,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: previousX1,
  latest_completed_x2_phase: phaseSlug,
  next_expected_scope: nextPhase,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  current_active_lanes: [
    "Aevren Vale",
    "Lumen Vale",
    "ghc-lumen-launch-browser-refresh-status-first-ready",
    "v558-v5-x1-lumen-solo-ready",
  ],
  round_robin_cadence: roundRobinSequence,
  v558_v4_x2_closeout: {
    status,
    safe_tasks_executed_or_reduced: closeout.safe_tasks_executed_or_reduced,
    reflection_rows: closeout.reflection_rows,
    next_active_phase: nextPhase,
    full_goal_complete: false,
  },
  full_goal_complete: false,
});
state.current_lookup_files = existingRelativeFiles(Array.from(new Set([
  ...(Array.isArray(state.current_lookup_files) ? state.current_lookup_files : []),
  ...traceFilesForPhase(phaseSlug),
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-current-state-v1.json",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.json",
])));
writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);

Object.assign(latest, {
  generated_utc: createdUtc,
  status,
  current_active_phase: nextPhase,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: previousX1,
  latest_completed_x2_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  current_active_lanes: state.current_active_lanes,
  round_robin_sequence: roundRobinSequence,
  primary_branch: miniBranch,
  full_tools_support_branch: fullToolsBranch,
  v558_v4_x2_closeout: state.v558_v4_x2_closeout,
  full_goal_complete: false,
});
latest.latest_lookup_files = existingRelativeFiles(Array.from(new Set([
  ...(Array.isArray(latest.latest_lookup_files) ? latest.latest_lookup_files : []),
  ...traceFilesForPhase(phaseSlug),
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-current-state-v1.json",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.json",
])));
writeFileSync(latestPath, `${JSON.stringify(latest, null, 2)}\n`);

const beaconMd = `# ${nextPhase}

Status: ${status}

- Current active phase: ${nextPhase}
- Latest closed phase: ${phaseSlug}
- Latest completed x1: ${previousX1}
- Latest completed x2: ${phaseSlug}
- Next x2 scope: ${nextX2}
- Next x1 lane after x2: ${nextX1AfterX2}

## v558 v4 x2 Closeout

- Safe tasks executed or reduced: ${closeout.safe_tasks_executed_or_reduced}
- Reflection rows recorded: ${closeout.reflection_rows}
- Next Lumen route: ghc-lumen-launch plus in-app Browser, refresh/status first.
- Full v544-v575 goal complete: false.

Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.
`;

writeFileSync(join(omegaIndexDir, "omega-mini-current-state-v1.md"), beaconMd);
writeFileSync(join(omegaIndexDir, "omega-mini-latest-updates-beacon-v1.md"), beaconMd);
writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beaconMd);
writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.json"), `${JSON.stringify({
  schema: "ghc.current_state_beacon.v1",
  status,
  current_active_phase: nextPhase,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: previousX1,
  latest_completed_x2_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  full_goal_complete: false,
  raw_private_material_published: false,
}, null, 2)}\n`);

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  next_active_phase: nextPhase,
  artifacts_written: 6,
}, null, 2));

function readJsonIfExists(path) {
  if (!existsSync(path)) {
    return null;
  }
  return JSON.parse(readFileSync(path, "utf8"));
}

function writeArtifact(name, body) {
  const base = `${phaseSlug}-${name}-v1`;
  writeFileSync(join(tracesDir, `${base}.json`), `${JSON.stringify(body, null, 2)}\n`);
  writeFileSync(join(tracesDir, `${base}.md`), [
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
  ].join("\n"));
}

function traceFilesForPhase(slug) {
  return [
    "safe-runner-manifest",
    "safe-runner-orchestrator",
    "safe-runner-orchestrator-startup-context",
    "safe-runner-orchestrator-reflection-ledger",
    "safe-runner-orchestrator-compact-pause",
    "safe-build-execution-ledger",
    "next-lumen-browser-route-prep",
    "closeout-prep",
    "closeout",
    "v5-x1-lumen-startup-handoff",
  ].flatMap((name) => [
    `docs/trinity-live-traces/${slug}-${name}-v1.md`,
    `docs/trinity-live-traces/${slug}-${name}-v1.json`,
  ]);
}

function existingRelativeFiles(files) {
  return files.filter((file) => typeof file === "string" && existsSync(join(process.cwd(), file)));
}

function gitBranch() {
  try {
    return execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"], {
      cwd: process.cwd(),
      encoding: "utf8",
      windowsHide: true,
    }).trim();
  } catch {
    return "unknown";
  }
}
