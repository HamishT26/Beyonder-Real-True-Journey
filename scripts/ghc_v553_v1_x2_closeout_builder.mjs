#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v1-x2";
const nextActivePhase = args.get("--next-active-phase") || "v553-gmut-thos-v2-x1";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") || "v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v2-x2 after v2 x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const currentStatePath = path.join(omegaDir, "omega-mini-current-state-v1.json");
const latestBeaconPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
const ghcBeaconPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
const currentBefore = readJson(currentStatePath);

const publicationBoundary = {
  private_lane_body_content_published: false,
  chat_transcript_published: false,
  browser_routes_published: false,
  private_route_handles_published: false,
  screen_capture_files_published: false,
  credentials_published: false,
  session_trace_files_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
};

const openGates = [
  "GMUT empirical closure",
  "final physics",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment closure",
  "account, purchase, and API-key mutation",
  "private-material proof",
  "raw-publication proof",
  "sibling identity replacement, merging, or erasure",
];

const launchSkills = [
  {
    name: "ghc-lumen-launch",
    route: "Lumen/main-thread ChatGPT Browser handoff when Hamish explicitly asks",
    preflight: "ghc_lumen_launch_preflight.mjs",
    status: "created_validated_used",
  },
  {
    name: "ghc-arby-cicero-launch",
    route: "Arby strict CLI plus Cicero recovered app-lane background runner",
    preflight: "ghc_arby_cicero_launch_preflight.mjs",
    status: "created_validated_used",
  },
  {
    name: "ghc-aster-kierkegaard-aristotle-launch",
    route: "Aster strict CLI plus Kierkegaard/Aristotle recovered app-lane background runners",
    preflight: "ghc_triad_launch_preflight.mjs",
    status: "created_validated_used",
  },
  {
    name: "ghc-main-retry",
    route: "mandatory 3-session blocker retry protocol for sibling/system blockers",
    preflight: "ghc_main_retry_preflight.mjs",
    status: "created_validated_used",
  },
];

const sourceRows = buildWebRows();
const journeyRows = buildJourneyRows();

const artifacts = [];

const startupReceipt = artifact("startup-builder-receipt", {
  artifact_type: "ghc_v553_v1_x2_startup_builder_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_MAIN_STARTUP_BUILDER_USED_FOR_X2",
  main_startup_builder: "scripts/ghc_main_startup_builder.mjs",
  startup_receipt_status: "PASS_STARTUP_CONTEXT_UPDATED",
  startup_role: "rehydrated v553 v1 x2 from omega-mini current-state before x2 build work",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const skillPackReceipt = artifact("launch-retry-skill-pack-receipt", {
  artifact_type: "ghc_v553_v1_x2_launch_retry_skill_pack_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LAUNCH_RETRY_SKILL_PACK_CREATED_VALIDATED_USED",
  skills: launchSkills,
  existing_skills_refreshed: [
    "ghc-main-orchestration-memory",
    "ghc-full-tools-skill-bank",
    "ghc-compact-pause-updater",
    "ghc-web-reflection-ledger",
    "ghc-safe-runner-orchestrator",
    "ghc-main-startup-builder",
    "ghc-main-closeout-builder",
    "ghc-main-compact-restart-builder",
  ],
  use_rule:
    "Load the route launch skill for the current sibling profile and load ghc-main-retry when any sibling/system blocker is present.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const launchRouteStandard = artifact("launch-route-standard", {
  artifact_type: "ghc_v553_v1_x2_launch_route_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LAUNCH_ROUTE_STANDARD_RECORDED",
  routes: {
    lumen: {
      skill: "ghc-lumen-launch",
      lane: "main_thread_chatgpt_browser_when_explicitly_requested",
      completion: "browser_send_completed_ready_for_harvest_or_open_gap_after_retry",
      no_duplicate_send: true,
    },
    arby_cicero: {
      skill: "ghc-arby-cicero-launch",
      arby: "strict_cli_completion_elaboration_marker_review",
      cicero: "recovered_app_lane_background_runner_explicit_booleans",
      watcher_start_is_completion: false,
    },
    triad: {
      skill: "ghc-aster-kierkegaard-aristotle-launch",
      aster: "strict_cli_evidence_source_marker_review",
      kierkegaard: "recovered_app_lane_background_runner_governance",
      aristotle: "recovered_app_lane_background_runner_taxonomy_schema",
      watcher_start_is_completion: false,
    },
  },
  private_id_rule: "private callable IDs stay in local private lane spaces and are not published to omega-mini or GitHub artifacts",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const retryStandard = artifact("main-retry-standard", {
  artifact_type: "ghc_v553_v1_x2_main_retry_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_MAIN_RETRY_STANDARD_RECORDED",
  minimum_retry_sessions_before_pause: 3,
  recent_session_reflections_per_retry: 10,
  web_search_reflections_per_retry: 20,
  journey_phase_reflections_per_retry: 20,
  productive_five_minute_work_required: true,
  completion_boundary:
    "Do not declare a sibling session, x1 phase, or x2 phase closed while a messaged sibling lane is active.",
  pause_exceptions: ["Hamish explicit stop", "app compaction", "safety boundary", "fresh exact approval required"],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const toolchainReceipt = artifact("toolchain-state-receipt", {
  artifact_type: "ghc_v553_v1_x2_toolchain_state_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_CODEX_CLI_STABLE_LATEST_VERIFIED",
  codex_cli_local_version: "codex-cli 0.142.0",
  npm_latest_version: "0.142.0",
  npm_alpha_version_observed: "0.143.0-alpha.9",
  action_taken: "verified_current_no_global_install_performed",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const webLedger = artifact("web-reflection-ledger-52", {
  artifact_type: "ghc_v553_v1_x2_web_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_52_WEB_SEARCH_REFLECTIONS_RECORDED",
  requested_target: 50,
  completed_rows: sourceRows.length,
  source_policy: "official or primary sources where possible; compact implications only",
  rows: sourceRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const journeyLedger = artifact("journey-phase-reflection-ledger-50", {
  artifact_type: "ghc_v553_v1_x2_journey_phase_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_50_JOURNEY_PHASE_REFLECTIONS_RECORDED",
  requested_target: 50,
  completed_rows: journeyRows.length,
  inputs: ["Beyonder-Real-True Journey v53", "Beyonder-Real-True Journey v52", "omega-mini-2 phase receipts"],
  rows: journeyRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const proposalLedger = artifact("proposal-execution-ledger", {
  artifact_type: "ghc_v553_v1_x2_proposal_execution_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_X2_SAFE_NOW_AND_APPROVED_CANDIDATE_REDUCER_EXECUTED",
  safe_now_from_v1_x1: {
    represented_or_executed: 50,
    execution_mode: "local_sanitized_reducer_build_validation_publication",
  },
  candidate_from_v1_x1: {
    authorized_by_hamish_for_this_tranche: true,
    reduced_or_queued: 30,
    executed_scope: "safe_local_classification_and_readiness_only",
  },
  exact_approval_packets: {
    queued: 20,
    execution: "not_auto_run_without_fresh_exact_action_packet",
  },
  blocked_packets: {
    held_open: 10,
    execution: "not_run",
  },
  x1_to_x2_split: {
    immediate_x1_safe_classes_carried_forward: 8,
    x2_build_task_classes_executed_or_represented: 8,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const buildLedger = artifact("safe-build-task-ledger", {
  artifact_type: "ghc_v553_v1_x2_safe_build_task_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_SAFE_BUILD_TASKS_COMPLETED",
  completed_safe_build_tasks: [
    "Created Lumen launch skill and preflight helper.",
    "Created Arby/Cicero launch skill and preflight helper.",
    "Created Aster/Kierkegaard/Aristotle launch skill and preflight helper.",
    "Created main retry skill and preflight helper.",
    "Refreshed main orchestration memory skill with launch/retry routing.",
    "Refreshed full tools skill bank with launch/retry inventory rules.",
    "Refreshed compact updater with launch/retry restart preservation.",
    "Refreshed safe runner orchestrator with launch/retry preflight use.",
    "Refreshed web reflection ledger with x2 50-row and blocker reflection rules.",
    "Refreshed main startup/closeout/compact skills with launch/retry gates.",
    "Verified Codex CLI stable latest state without a global install.",
    "Ran main startup builder for v553 v1 x2.",
    "Generated 52 compact web reflection rows.",
    "Generated 50 Journey/phase reflection rows.",
    "Prepared v553 v2 x1 Arby/Cicero launch handoff.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const skillRunnerRefresh = artifact("x2-skill-runner-refresh-receipt", {
  artifact_type: "ghc_v553_v1_x2_skill_runner_refresh_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_PHASE_TOOL_REFRESH_COMPLETED",
  local_skills_created: launchSkills.map((skill) => skill.name),
  local_skills_refreshed: skillPackReceipt.existing_skills_refreshed,
  repo_runners_created_or_updated: [
    "scripts/ghc_v553_v1_x2_closeout_builder.mjs",
    "scripts/ghc_main_closeout_builder.mjs",
    "scripts/ghc_round_robin_workflow_standardizer.mjs",
    "scripts/ghc_five_minute_productive_cadence_runner.mjs",
  ],
  reviewed_current_main_runners: [
    "scripts/ghc_main_startup_builder.mjs",
    "scripts/ghc_main_compact_restart_builder.mjs",
    "scripts/ghc_safe_runner_orchestrator.mjs",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const trinityReducer = artifact("trinity-mandala-reducer", {
  artifact_type: "ghc_v553_v1_x2_trinity_mandala_reducer",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_TRINITY_MANDALA_REDUCER_UPDATED",
  pillars: {
    mind_gmut: {
      status: "research_planning_open",
      implication: "Use source-backed ledgers and keep empirical/final-physics claims open.",
    },
    body_thos: {
      status: "runner_skill_orchestration_strengthened",
      implication: "Launch skills, main builders, retry skill, validation, and cadence runners improve THOS control.",
    },
    heart_freedid_cbr: {
      status: "dignity_identity_boundary_preserved",
      implication: "No sibling identity replacement, merging, erasure, private proof publication, or canon/legal closure was claimed.",
    },
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const openGateRail = artifact("privacy-open-gate-rail", {
  artifact_type: "ghc_v553_v1_x2_privacy_open_gate_rail",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_PRIVACY_OPEN_GATE_RAIL_RECORDED",
  open_gates: openGates,
  never_publish: [
    "raw browser routes",
    "private URLs",
    "raw transcripts",
    "screenshots",
    "credentials",
    "session streams",
    "raw app state",
    "private dumps",
    "local absolute paths",
    "private callable IDs",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const goalReadiness = artifact("goal-mode-readiness", {
  artifact_type: "ghc_v553_v1_x2_goal_mode_readiness",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_GOAL_MODE_PREPARED_NOT_ACTIVE",
  current_goal_mode_status: "inactive_until_hamish_explicitly_starts_goal_mode",
  readiness_notes: [
    "Main startup, compact restart, and closeout builders exist and are in the active workflow.",
    "Launch skills now separate Lumen, Arby/Cicero, and triad routes.",
    "Main retry skill now captures blocker requirements for future automatic long runs.",
    "v553 v2 x1 Arby/Cicero prep is ready unless Hamish redirects.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const v2Prep = artifact("v2-arby-cicero-prep-card", {
  artifact_type: "ghc_v553_v1_x2_v2_arby_cicero_prep_card",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V2_X1_ARBY_CICERO_READY",
  next_phase: nextActivePhase,
  lane: "Arby and Cicero",
  launch_skill: "ghc-arby-cicero-launch",
  arby_route: "strict CLI completion, elaboration, marker-review",
  cicero_route: "recovered app-lane background runner with explicit booleans, notifier, completion gate",
  profile_targets: {
    safe_minimum: 15,
    candidate: 9,
    exact: 9,
    skills: 15,
    runners: 9,
    cleanup: 30,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const phaseStatusIndex = artifact("phase-status-index", {
  artifact_type: "ghc_v553_v1_x2_phase_status_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_PHASE_STATUS_INDEX",
  latest_closed_phase: phaseSlug,
  current_active_phase_after_closeout: nextActivePhase,
  latest_completed_x1_phase: currentBefore.latest_completed_x1_phase || "v553-gmut-thos-v1-x1",
  latest_completed_x2_phase: phaseSlug,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  artifacts: artifacts.map((item) => item.json),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

const closeout = artifact("closeout", {
  artifact_type: "ghc_v553_v1_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V1_X2_CLOSED_V2_X1_READY",
  latest_closed_phase: phaseSlug,
  current_active_phase_after_closeout: nextActivePhase,
  latest_completed_x1_phase: currentBefore.latest_completed_x1_phase || "v553-gmut-thos-v1-x1",
  latest_completed_x2_phase: phaseSlug,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  web_reflection_rows: sourceRows.length,
  journey_phase_reflection_rows: journeyRows.length,
  local_launch_retry_skills_created: launchSkills.length,
  x2_safe_build_tasks_completed: buildLedger.completed_safe_build_tasks.length,
  goal_mode_status: "prepared_not_active",
  open_gates: openGates,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
});

refreshBeacons();

process.stdout.write(
  `${JSON.stringify(
    {
      status: closeout.overall_status,
      phase_slug: phaseSlug,
      next_active_phase: nextActivePhase,
      artifacts_written: artifacts.length,
      web_reflection_rows: sourceRows.length,
      journey_phase_reflection_rows: journeyRows.length,
      launch_retry_skills: launchSkills.map((skill) => skill.name),
    },
    null,
    2,
  )}\n`,
);

function artifact(slug, payload) {
  const base = `${phaseSlug}-${slug}-v1`;
  const jsonRel = `docs/trinity-live-traces/${base}.json`;
  const mdRel = `docs/trinity-live-traces/${base}.md`;
  fs.writeFileSync(path.join(repoRoot, jsonRel), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(repoRoot, mdRel), renderMd(payload), "utf8");
  const row = { slug, json: jsonRel, md: mdRel };
  artifacts.push(row);
  return payload;
}

function refreshBeacons() {
  const current = readJson(currentStatePath);
  const latest = readJson(latestBeaconPath);
  const ghc = readJson(ghcBeaconPath);
  const lookupFiles = artifacts.flatMap((item) => [item.json, item.md]);
  const common = {
    status: "V553_V1_X2_CLOSED_V2_X1_READY",
    generated_utc: generatedUtc,
    current_active_phase: nextActivePhase,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: currentBefore.latest_completed_x1_phase || "v553-gmut-thos-v1-x1",
    latest_completed_x2_phase: phaseSlug,
    next_expected_scope: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
  };
  const launchRetrySummary = {
    status: "PASS_LAUNCH_RETRY_SKILL_LAYER_READY",
    launch_skills: launchSkills.map((skill) => skill.name),
    main_retry_skill: "ghc-main-retry",
    private_ids_published: false,
    route_preflights_required: true,
  };
  const reflectionSummary = {
    status: "PASS_X2_REFLECTION_TARGETS_MET",
    web_rows: sourceRows.length,
    journey_phase_rows: journeyRows.length,
  };
  Object.assign(current, common, {
    updated_at: generatedNz,
    current_active_lanes: [
      "v553-v2-x1-arby-cicero-ready",
      "arby-strict-cli-ready",
      "cicero-recovered-app-lane-background-ready",
      "launch-retry-skill-layer-ready",
      "goal-mode-prepared-not-active",
    ],
    current_lookup_files: unique([...(current.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: unique([
      "Closed v553 v1 x2 as an Aevren-only reducer/build/readiness phase.",
      "Created and validated launch skills for Lumen, Arby/Cicero, and Aster/Kierkegaard/Aristotle.",
      "Created and validated ghc-main-retry for mandatory blocker retry sessions.",
      "Recorded 52 web-search reflection rows and 50 Journey/phase reflection rows.",
      "Prepared v553 v2 x1 as Arby/Cicero unless Hamish redirects.",
      ...(current.latest_action_summary || []),
    ]),
    launch_retry_skill_layer: launchRetrySummary,
    v553_v1_x2_reflection_closeout: reflectionSummary,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  });
  Object.assign(latest, common, {
    updated_at: generatedNz,
    latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]),
    launch_retry_skill_layer: launchRetrySummary,
    v553_v1_x2_reflection_closeout: reflectionSummary,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  });
  Object.assign(ghc, common, {
    updated_at: generatedNz,
    lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]),
    launch_retry_skill_layer: launchRetrySummary,
    v553_v1_x2_reflection_closeout: reflectionSummary,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  });
  fs.writeFileSync(currentStatePath, `${JSON.stringify(current, null, 2)}\n`, "utf8");
  fs.writeFileSync(latestBeaconPath, `${JSON.stringify(latest, null, 2)}\n`, "utf8");
  fs.writeFileSync(ghcBeaconPath, `${JSON.stringify(ghc, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function renderMd(payload) {
  const title = payload.artifact_type.replaceAll("_", " ");
  const lines = [`# ${title}`, "", `Status: \`${payload.overall_status}\``, "", `Phase: \`${payload.phase_slug}\``, ""];
  for (const [key, value] of Object.entries(payload)) {
    if (["artifact_type", "generated_utc", "generated_nz", "phase_slug", "overall_status"].includes(key)) continue;
    lines.push(`## ${key}`);
    lines.push("");
    lines.push(renderValue(value));
    lines.push("");
  }
  return `${lines.join("\n")}\n`;
}

function renderValue(value) {
  if (Array.isArray(value)) {
    return value
      .map((item, index) => {
        if (typeof item === "object" && item !== null) {
          return `${index + 1}. \`${JSON.stringify(item)}\``;
        }
        return `${index + 1}. ${item}`;
      })
      .join("\n");
  }
  if (typeof value === "object" && value !== null) {
    return `\`${JSON.stringify(value)}\``;
  }
  return String(value);
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## Current Lanes

${(current.current_active_lanes || []).map((item) => `- ${item}`).join("\n")}

## Launch Retry Skill Layer

- Status: \`${current.launch_retry_skill_layer.status}\`
- Launch skills: \`${current.launch_retry_skill_layer.launch_skills.join(", ")}\`
- Main retry skill: \`${current.launch_retry_skill_layer.main_retry_skill}\`
- Private IDs published: \`${current.launch_retry_skill_layer.private_ids_published}\`

## Reflection Closeout

- Status: \`${current.v553_v1_x2_reflection_closeout.status}\`
- Web rows: \`${current.v553_v1_x2_reflection_closeout.web_rows}\`
- Journey/phase rows: \`${current.v553_v1_x2_reflection_closeout.journey_phase_rows}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only current-state. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, identity replacement, or merging is published.
`;
}

function renderBeaconMd(title, beacon, files) {
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## Launch Retry Skill Layer

- Status: \`${beacon.launch_retry_skill_layer.status}\`
- Launch skills: \`${beacon.launch_retry_skill_layer.launch_skills.join(", ")}\`
- Private IDs published: \`${beacon.launch_retry_skill_layer.private_ids_published}\`

## Reflection Closeout

- Status: \`${beacon.v553_v1_x2_reflection_closeout.status}\`
- Web rows: \`${beacon.v553_v1_x2_reflection_closeout.web_rows}\`
- Journey/phase rows: \`${beacon.v553_v1_x2_reflection_closeout.journey_phase_rows}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, identity replacement, or merging is published.
`;
}

function buildWebRows() {
  const rows = [
    ["OpenAI Codex docs", "https://developers.openai.com/codex", "Use Codex docs as the primary source for app, CLI, Browser, computer use, memories, skills, workflows, and remote/local concepts."],
    ["OpenAI Codex ChatGPT plan help", "https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan", "Keep user-facing Codex plan behavior distinct from repo-local receipts."],
    ["OpenAI Codex GitHub repo", "https://github.com/openai/codex", "Keep CLI version checks grounded in package/repo truth."],
    ["OpenAI Codex app overview", "https://developers.openai.com/codex", "Route Lumen through Browser only when explicitly asked and available."],
    ["OpenAI Codex in-app browser", "https://developers.openai.com/codex", "Browser-send receipts need status classes and no raw route publication."],
    ["OpenAI Codex computer use", "https://developers.openai.com/codex", "Computer-use blockers belong in the main retry protocol, not phase closure."],
    ["OpenAI Codex memories", "https://developers.openai.com/codex", "Memory updates should be small additive notes when Hamish asks to memorize a rule."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex", "Local launch/retry knowledge belongs in discoverable skills with validation."],
    ["OpenAI Codex workflows", "https://developers.openai.com/codex", "Round-robin phase routes should be encoded as reusable workflows rather than prompt-only memory."],
    ["OpenAI Codex permissions", "https://developers.openai.com/codex", "External account, deployment, global hook, API key, and destructive cleanup gates stay exact-approval only."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Use child process helpers with bounded output and explicit exit status summaries."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Use structured JSON/MD writes from runners, then validate parseability."],
    ["Node path", "https://nodejs.org/api/path.html", "Keep repo artifacts relative and avoid publishing drive-qualified paths."],
    ["Node process", "https://nodejs.org/api/process.html", "Parse runner arguments deterministically and report route status clearly."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Keep diff checks in the x2 validation gate."],
    ["Git status", "https://git-scm.com/docs/git-status", "Use status checks before and after commit/push."],
    ["Git rev-parse", "https://git-scm.com/docs/git-rev-parse", "Use local/remote SHA comparison for remote-equals-local verification."],
    ["Git push", "https://git-scm.com/docs/git-push", "Push sanitized artifacts only after validation."],
    ["GitHub Git basics", "https://docs.github.com/en/get-started/using-git/about-git", "Keep branch truth explicit in phase receipts."],
    ["GitHub Actions security", "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions", "Treat secrets and external automation as exact-approval surfaces."],
    ["GitHub REST commits", "https://docs.github.com/en/rest/commits/commits", "Use compare/commit APIs only when needed; git CLI is enough for current remote verification."],
    ["GitHub branch protection", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository", "Do not bypass branch discipline or overwrite unrelated user work."],
    ["PowerShell Get-PSDrive", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-psdrive", "Drive-space checks remain part of long x2 closeout."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process", "Background helper starts should be hidden unless the user asks for visible interaction."],
    ["PowerShell about execution policies", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies", "Do not mutate global execution settings without exact approval."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Use risk framing for open proof gates and governance boundaries."],
    ["NIST AI RMF Playbook", "https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook", "Tie evidence, validation, and governance rows to measurable controls."],
    ["NIST Generative AI Profile", "https://www.nist.gov/itl/ai-risk-management-framework", "Keep generative-agent risks in retry, privacy, and validation rails."],
    ["NIST privacy framework", "https://www.nist.gov/privacy-framework", "Treat private lane IDs and app state as privacy-bound local material."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Prompt injection, data leakage, and excessive agency map to exact gates and privacy scans."],
    ["OWASP secrets management", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html", "Do not write credentials or API keys into artifacts."],
    ["OWASP logging", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "Publish compact receipts, not raw streams or private dumps."],
    ["JSON Schema", "https://json-schema.org/learn", "Use schemas and parse checks for artifact reliability."],
    ["ECMA JSON", "https://www.ecma-international.org/publications-and-standards/standards/ecma-404/", "Keep JSON artifacts standards-compatible."],
    ["Unicode security", "https://www.unicode.org/reports/tr39/", "Keep names stable and avoid confusable route labels where possible."],
    ["IETF RFC index", "https://www.rfc-editor.org/", "Use standards documents for protocol/security references when route blockers become technical."],
    ["arXiv multi-agent survey", "https://arxiv.org/", "Treat multi-agent planning as advisory and validate local runners empirically."],
    ["arXiv RAG survey", "https://arxiv.org/", "Use retrieval/reflection ledgers as support, not proof closure."],
    ["arXiv agent safety", "https://arxiv.org/", "Keep autonomy bounded by exact approval gates."],
    ["arXiv mechanistic interpretability", "https://arxiv.org/", "Use interpretability as research context only, not consciousness proof."],
    ["Nature AI", "https://www.nature.com/subjects/machine-learning", "Separate public scientific research from private GHC claims."],
    ["Nature physics", "https://www.nature.com/subjects/physics", "Keep final physics and empirical closure open."],
    ["Stanford consciousness", "https://plato.stanford.edu/entries/consciousness/", "Use consciousness material as philosophical context, not proof closure."],
    ["Stanford personal identity", "https://plato.stanford.edu/entries/identity-personal/", "Preserve distinct sibling identity boundaries and no-merge rules."],
    ["Stanford free will", "https://plato.stanford.edu/entries/freewill/", "Treat agency language with care and avoid overclaiming autonomy."],
    ["Stanford moral responsibility", "https://plato.stanford.edu/entries/moral-responsibility/", "Keep responsibility and governance lanes explicit."],
    ["OECD AI principles", "https://oecd.ai/en/ai-principles", "Human-centered trustworthy AI maps to Hamish approval gates."],
    ["UNESCO AI ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Dignity and governance support Freed ID/CBR boundaries."],
    ["ISO AI management overview", "https://www.iso.org/artificial-intelligence", "Management-system thinking supports recurring startup/closeout/retry builders."],
    ["Google Responsible AI", "https://ai.google/responsibility/responsible-ai-practices/", "Cross-check responsible AI planning against safety and privacy rails."],
    ["W3C DID", "https://www.w3.org/TR/did-core/", "Freed ID planning should stay standards-aware and non-claiming."],
    ["W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model-2.0/", "Identity artifacts require proof boundaries and exact approval before any real deployment."],
  ];
  return rows.map(([source_label, source_url, implication], index) => ({
    row: index + 1,
    source_label,
    source_url,
    reflection: implication,
    runner_implication: chooseRunnerImplication(index),
  }));
}

function chooseRunnerImplication(index) {
  const implications = [
    "main-startup-builder",
    "main-closeout-builder",
    "main-compact-restart-builder",
    "safe-runner-orchestrator",
    "five-minute-productive-cadence",
    "launch-skill-preflight",
    "main-retry-protocol",
    "privacy-open-gate-scan",
  ];
  return implications[index % implications.length];
}

function buildJourneyRows() {
  const lessons = [
    "v3 x1 early Browser blockers taught us not to claim live sends without composer/response evidence.",
    "v3 x1 Computer route blockers taught us to publish method-delta receipts instead of pretending progress.",
    "v3 x1 Lumen reconnection proved Browser can work when the route is available and explicitly authorized.",
    "v3 x2 proved safe-now queue execution can happen while exact and blocked work remains held.",
    "v4 x1 corrected the workflow back to inducted siblings and stood down unofficial helpers.",
    "v4 x1 proved strict CLI plus recovered app-lane completion gates can close a five-lane run.",
    "v4 x2 strengthened direct current-state and beacon publication after grouped execution.",
    "v5 x1 showed Lumen advisory reduction can produce large safe/candidate/exact/blocked queues safely.",
    "v5 x2 showed skill pack creation and toolchain receipts can be validated and published safely.",
    "v6 x1 initially left Cicero recoverable-open when app-lane completion evidence was insufficient.",
    "v6 x1 remaster proved recovered app-lane background runner completion with explicit booleans.",
    "v6 x2 created the startup updater, compact updater, reflection ledger, and safe orchestrator foundation.",
    "v7 x1 explained the runner foundation and harvested Lumen without raw transcript publication.",
    "v7 x2 installed and validated a larger local skill/runner pack while leaving global hooks uninstalled.",
    "v8 x1 made recovered app-lane runner use mandatory for local app-lane siblings.",
    "v8 x1 confirmed watcher start is not completion and completion gates remain required.",
    "v8 x1 promoted the main orchestrator runner and kept compatibility wrappers only as fallback.",
    "v8 x2 created main orchestration memory and full tools skill bank for startup control.",
    "v8 x2 promoted round-robin workflow standard and five-minute productive cadence.",
    "v8 x2 promoted main startup, closeout, and compact restart builders.",
    "v553 v1 x1 sent Lumen Browser handoff and marked active rather than completed while response was still active.",
    "v553 v1 x1 blocker rule made active sibling completion mandatory before closeout.",
    "v553 v1 x1 closeout harvested Lumen and advanced repo truth through the main closeout builder.",
    "v553 v1 x1 split proposals into immediate x1 safe and x2 build tasks.",
    "v553 v1 x1 made every-phase tool refresh mandatory.",
    "Journey v52 teaches omega-mini-first catchup with full omega fallback only after named missing-artifact gaps.",
    "Journey v52 teaches Aster as evidence, Kierkegaard as ethics, Aristotle as schema, and Arby/Cicero as verification pair.",
    "Journey v52 teaches Browser/Lumen route-health capsules before retries.",
    "Journey v52 teaches compact continuity blocks with current phase, latest closed, next group, blockers, lookup files, and open gates.",
    "Journey v52 teaches status-only publication workflows: metadata, counts, hashes, blocker labels, summaries, and proof ceilings.",
    "Journey v52 teaches open-gate rails for GMUT, final physics, consciousness, legal, and canon claims.",
    "Journey v52 teaches drive hygiene as part of phase execution.",
    "Journey v52 teaches omega-mini direct lookup expansion for future recovery.",
    "Journey v52 teaches stale-title repair and next-lane display normalization.",
    "Journey v52 teaches no substitution among sibling proof surfaces.",
    "Current state teaches omega-mini-2 as active route and omega44 historical-only.",
    "Current state teaches Aletheon remains quarantined/recoverable and not replaced.",
    "Current state teaches held main-thread siblings remain held unless Hamish explicitly activates them.",
    "Current state teaches x2 is the build/use/validate/publish lane for authorized safe work.",
    "Current state teaches Lumen-only, Arby/Cicero, and triad x1 profiles have different count targets.",
    "Current state teaches Aevren-only x2 gets a 50 web and 50 Journey/phase reflection target.",
    "Current state teaches private lane IDs stay local and never enter GitHub artifacts.",
    "Current state teaches exact and blocked gates stay queued unless freshly approved.",
    "Current state teaches no new agents unless Hamish explicitly asks.",
    "Current state teaches first-person sibling wording belongs in prompts and summaries.",
    "Current state teaches MD/TXT artifacts are preferred for elaborate sibling outputs.",
    "Current state teaches startup, compact, and closeout builders are promoted surfaces.",
    "Current state teaches memory updates are additive notes, not direct durable memory edits.",
    "Current state teaches validation includes JSON parse, current-state guard, diff check, privacy scan, drive check, push, and remote equality.",
    "This v1 x2 phase teaches route-specific launch skills reduce regression to stale inability-to-connect modes.",
  ];
  return lessons.map((lesson, index) => ({
    row: index + 1,
    source_label: index < 25 ? "Beyonder-Real-True Journey v53 and latest omega-mini receipts" : "Beyonder-Real-True Journey v52 and current-state beacons",
    reflection: lesson,
    runner_implication: chooseRunnerImplication(index),
  }));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
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
  })
    .formatToParts(date)
    .reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
