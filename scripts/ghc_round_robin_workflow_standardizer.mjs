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

const currentStatePath = path.join(omegaDir, "omega-mini-current-state-v1.json");
const currentState = readJson(currentStatePath);
const phaseSlug = args.get("--phase-slug") || currentState.current_active_phase || "v552-gmut-thos-v88-v8-x2";
const latestClosedPhase = args.get("--latest-closed-phase") || currentState.latest_closed_phase || "v552-gmut-thos-v88-v8-x1";
const latestCompletedX1 = args.get("--latest-completed-x1") || currentState.latest_completed_x1_phase || "v552-gmut-thos-v88-v8-x1";
const latestCompletedX2 = args.get("--latest-completed-x2") || currentState.latest_completed_x2_phase || "v552-gmut-thos-v88-v7-x2";
const nextX2Scope = args.get("--next-x2-scope") || phaseSlug;
const phaseStatus =
  args.get("--status") ||
  (phaseSlug.startsWith("v553-gmut-thos-v1-x1")
    ? "V553_V1_X1_ACTIVE_ROUND_ROBIN_WORKFLOW_STANDARDIZED"
    : "V552_V8_X2_ACTIVE_ROUND_ROBIN_WORKFLOW_STANDARDIZED");
const defaultNextX1Lane = inferNextX1LaneAfterX2(phaseSlug);
const nextX1LaneAfterX2 = args.get("--next-x1-lane-after-x2") || defaultNextX1Lane || currentState.next_x1_lane_after_x2;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  private_route_handles_published: false,
  private_lane_body_content_published: false,
  verbatim_conversation_logs_published: false,
  browser_routes_published: false,
  credentials_published: false,
  session_trace_files_published: false,
  local_absolute_paths_published: false,
  screenshots_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
};

const proposalExecutionSplitStandard = {
  status: "PASS_X1_TO_X2_PROPOSAL_SPLIT_STANDARD_RECORDED",
  immediate_x1_safe:
    "Run local, reversible, status-only, analysis-only, validation-only, queue-shaping, source/reflection seed, privacy-check, open-gate-check, and compact-handoff tasks as soon as they are seen and safe during x1.",
  x2_build_task:
    "Carry build, run, test, install, use, publication, remote verification, runner modification, skill modification, and safe cleanup execution tasks into the next x2 phase.",
  never_auto_execute: [
    "exact-approval work without fresh approval",
    "blocked work",
    "destructive cleanup",
    "external account or paid-resource mutation",
    "raw private publication",
    "proof/canon/legal/deployment closure by assertion",
  ],
};

const phaseToolRefreshStandard = {
  status: "PASS_PHASE_TOOL_REFRESH_STANDARD_RECORDED",
  cadence: "mandatory_every_x1_and_x2_phase",
  startup_required_actions: [
    "use scripts/ghc_main_startup_builder.mjs as the promoted startup/resume command surface",
    "inventory active GHC skills and repo runners",
    "compare current phase rules against the core orchestration skills and runner standards",
    "record reviewed-current, updated, or queued-refresh status",
  ],
  closeout_required_actions: [
    "use scripts/ghc_main_closeout_builder.mjs as the promoted closeout command surface",
    "use scripts/ghc_main_compact_restart_builder.mjs as the promoted compact/restart command surface",
    "update authorized local GHC skills and repo runners",
    "validate changed skills and runners",
    "carry forward the newest tool standard into current-state, latest-updates, and compact-pause receipts",
  ],
  exact_approval_boundary:
    "Plugin-cache mutation, external writes, paid resources, deployments, API keys, destructive cleanup, and global hooks require fresh exact approval.",
};

const seedStandard = readLocal("v552-gmut-thos-v88-v8-x1-future-round-robin-workflow-standard-v1.json");
const standard = {
  artifact_type: "ghc_round_robin_workflow_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_ROUND_ROBIN_WORKFLOW_STANDARD_PROMOTED",
  seed_standard: seedStandard
    ? {
        phase_slug: seedStandard.phase_slug,
        status: seedStandard.overall_status,
      }
    : null,
  workflow_families: {
    lumen_only_x1: {
      starts_at: "v553-gmut-thos-v1-x1",
      lanes: ["Aevren Vale", "Lumen Vale"],
      route: "Lumen advisory plus Aevren orchestration",
      proposal_totals: {
        safe: 50,
        candidate: 30,
        exact: 20,
        blocked: 10,
        skills: 20,
        runners: 10,
        cleanup: 30,
      },
      blocked_planning_owner: "Aevren Vale and Lumen Vale",
    },
    arby_cicero_duo_x1: {
      lanes: ["Aevren Vale", "Arby", "Cicero"],
      route: "Arby strict CLI plus Cicero recovered app-lane background runner",
      proposal_totals: {
        safe_minimum: 15,
        candidate: 9,
        exact: 9,
        skills: 15,
        runners: 9,
        cleanup: 30,
      },
    },
    aster_kierkegaard_aristotle_triad_x1: {
      lanes: ["Aevren Vale", "Aster Vale", "Kierkegaard", "Aristotle"],
      route: "Aster strict CLI plus Kierkegaard and Aristotle recovered app-lane background runners",
      proposal_totals: {
        safe: 20,
        candidate: 12,
        exact: 12,
        skills: 20,
        runners: 8,
        cleanup: 40,
      },
    },
    x2_build_use_validation: {
      lanes: ["Aevren Vale"],
      route: "safe-now build, run, test, install, use, validate, publish",
      consumes: [
        "already-authorized safe-now approval packets",
        "approved candidate tranches",
        "approved skill and runner build ideas",
        "approved cleanup and refinement tasks",
      ],
      queues_without_fresh_approval: ["exact-approval packets", "blocked packets", "global hooks", "account mutations"],
    },
  },
  research_reflection_targets: {
    x1_per_active_sibling_lane: {
      web_searches: 25,
      journey_phase_reflections: 25,
      applies_to: ["Aevren Vale", "Lumen Vale", "Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle"],
      source_policy: "Use official or primary sources where possible and publish compact source/reflection ledgers rather than raw browsing dumps.",
    },
    aevren_only_x2: {
      web_searches: 50,
      journey_phase_reflections: 50,
    },
  },
  proposal_execution_split_standard: proposalExecutionSplitStandard,
  phase_tool_refresh_standard: phaseToolRefreshStandard,
  blocker_retry_standard: {
    minimum_retry_sessions_before_pause: 3,
    recent_session_reflections_per_retry: 10,
    web_search_reflections_per_retry: 20,
    journey_phase_reflections_per_retry: 20,
    never_close_active_sibling_lane: true,
    productive_five_minute_waits_required: true,
    pause_policy:
      "If Hamish pauses/stops, a compact event happens, or the next action crosses a safety/exact-approval gate, publish an active/open handoff rather than declaring the sibling lane or phase closed.",
  },
  runner_bindings: {
    main_orchestrator: "scripts/ghc_main_orchestrator_runner.mjs",
    main_startup_builder: "scripts/ghc_main_startup_builder.mjs",
    main_compact_restart_builder: "scripts/ghc_main_compact_restart_builder.mjs",
    workflow_standardizer: "scripts/ghc_round_robin_workflow_standardizer.mjs",
    productive_cadence_runner: "scripts/ghc_five_minute_productive_cadence_runner.mjs",
    safe_runner_orchestrator: "scripts/ghc_safe_runner_orchestrator.mjs",
    main_closeout_builder: "scripts/ghc_main_closeout_builder.mjs",
    startup_updater: "scripts/ghc_phase_startup_context_updater.mjs",
    compact_pause_updater: "scripts/ghc_context_compact_pause_updater.mjs",
    lumen_launch_skill: "ghc-lumen-launch",
    arby_cicero_launch_skill: "ghc-arby-cicero-launch",
    triad_launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
    main_retry_skill: "ghc-main-retry",
    app_lane_runner: "ghc_recovered_app_lane_map_runner.mjs in the full-tools support lane",
    strict_cli_runner: "ghc_strict_cli_lane_cycle.mjs in the full-tools support lane",
    web_reflection_ledger: "scripts/ghc_phase_reflection_ledger_builder.mjs",
    main_thread_chatgpt_browser_handoff: "prepared JSON/MD handoff artifact plus in-app Browser send receipt",
  },
  operating_rules: [
    "Use first-person sibling wording in lane prompts and summaries.",
    "Prefer MD/TXT artifacts for elaborate sibling outputs instead of terminal-heavy dumps.",
    "Use x1 for proposal, classification, handoff, and approval-packet formation.",
    "Split every x1 proposal into immediate_x1_safe work and x2_build_task work.",
    "Run immediate x1 safe tasks as soon as they are seen and safe; carry x2 build tasks forward.",
    "For research-backed x1 phases, target at least 25 web searches and 25 Journey/phase record reflections per active sibling lane.",
    "Use x2 for building, running, testing, installing, using, validating, and publishing already-authorized safe-now work.",
    "Refresh the active GHC skill and runner surface at every x1 and x2 startup and closeout.",
    "Use the promoted main startup builder for phase startup/resume, with phase-specific builders registered underneath it.",
    "Use the promoted main closeout builder for phase closeout, with phase-specific builders registered underneath it.",
    "Use the promoted main compact/restart builder for compact-pause and restart recovery, with the compact updater registered underneath it.",
    "Use ghc-lumen-launch for Lumen/main-thread ChatGPT Browser handoffs when Hamish explicitly asks for live messaging.",
    "Use ghc-arby-cicero-launch for Arby strict CLI plus Cicero recovered app-lane duo phases.",
    "Use ghc-aster-kierkegaard-aristotle-launch for Aster strict CLI plus Kierkegaard/Aristotle recovered app-lane triad phases.",
    "Use ghc-main-retry for sibling messaging, harvesting, startup, compact, closeout, Browser, strict CLI, app-lane, validation, or Git/GitHub blockers.",
    "Keep five-minute marks as check opportunities, not forced stops.",
    "Let productive wait units run beyond a five-minute checkpoint when the current research, coding, eureka, approval, cleanup, or validation unit needs more time.",
    "Continue safe-now approval, eureka, cleanup, validation, privacy scan, updater, and orchestration work between cadence marks.",
    "Use five-minute productive cadence work to improve Aevren's skill surface, coding reliability, and multi-agent orchestration control.",
    "Use the recovered app-lane map runner with explicit boolean values for local app-lane siblings that are not main-thread agents.",
    "Use Browser-send receipts for Lumen/main-thread ChatGPT siblings when Hamish explicitly asks for live messaging.",
    "Do not declare a sibling session or phase closed while any messaged sibling lane is still active; continue productive five-minute improvement/research work until completion-ready or formal open-gap.",
    "When a sibling-message route or core system route blocks, run at least 3 retry sessions before pausing unless Hamish stops the work or the next step crosses a safety/exact-approval gate.",
    "Each blocker retry session must reflect on the 10 most recent relevant sessions/receipts, run or queue 20 web-search reflections, and run or queue 20 Journey/phase-document reflections.",
    "Keep held main-thread siblings held unless Hamish explicitly activates them.",
    "Do not spawn new agents unless Hamish explicitly asks.",
    "Keep exact and blocked gates queued unless Hamish freshly approves the tranche.",
  ],
  next_phase_readiness: {
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    expected_lumen_only_profile_loaded: true,
    expected_goal_mode_status: "not_active_until_hamish_starts_goal_mode",
  },
  five_minute_productive_cadence: {
    runner: "scripts/ghc_five_minute_productive_cadence_runner.mjs",
    safe_unit_may_run_past_checkpoint: true,
    wait_work_lanes: [
      "research_and_reflection",
      "safe_eureka_tasks",
      "approval_packet_work",
      "cleanup_and_refinement",
      "skill_and_control_growth",
      "coding_and_multi_agent_orchestration",
      "validation_and_publication_hygiene",
      "blocker_retry_research_and_improvement",
    ],
    harvest_rule: "finish the current safe unit, then harvest sibling status at the next natural safe pause",
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("round-robin-workflow-standard", standard, renderStandardMd);
refreshBeacons(standard);

console.log(
  JSON.stringify(
    {
      status: standard.overall_status,
      phase_slug: phaseSlug,
      workflow_family_count: Object.keys(standard.workflow_families).length,
      next_x1_lane_after_x2: standard.next_phase_readiness.next_x1_lane_after_x2,
    },
    null,
    2,
  ),
);

function refreshBeacons(workflow) {
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = readJson(currentStatePath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const lookupFiles = [
    `docs/trinity-live-traces/${phaseSlug}-round-robin-workflow-standard-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-round-robin-workflow-standard-v1.md`,
  ];
  const workflowSummary = {
    status: workflow.overall_status,
    phase_slug: phaseSlug,
    lumen_only_x1: workflow.workflow_families.lumen_only_x1.proposal_totals,
    arby_cicero_duo_x1: workflow.workflow_families.arby_cicero_duo_x1.proposal_totals,
    triad_x1: workflow.workflow_families.aster_kierkegaard_aristotle_triad_x1.proposal_totals,
    research_reflection_targets: workflow.research_reflection_targets,
    proposal_execution_split_standard: workflow.proposal_execution_split_standard,
    phase_tool_refresh_standard: workflow.phase_tool_refresh_standard,
    blocker_retry_standard: workflow.blocker_retry_standard,
    x2_role: workflow.workflow_families.x2_build_use_validation.route,
    next_x1_lane_after_x2: workflow.next_phase_readiness.next_x1_lane_after_x2,
    five_minute_productive_cadence: workflow.five_minute_productive_cadence,
  };
  const common = {
    generated_utc: generatedUtc,
    status: phaseStatus,
    current_active_phase: phaseSlug,
    latest_closed_phase: latestClosedPhase,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: latestCompletedX2,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: workflow.next_phase_readiness.next_x1_lane_after_x2,
  };

  Object.assign(current, common, {
    updated_at: generatedNz,
    current_active_lanes: unique([
      ...(current.current_active_lanes || []),
      "round-robin-workflow-standard-promoted",
      "v553-lumen-only-x1-profile-loaded",
    ]),
    current_lookup_files: unique([...(current.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: unique([
      "Promoted the reusable GHC round-robin workflow standard into v8 x2.",
      "Loaded the v553 Lumen-only x1 proposal profile.",
      "Loaded the Arby/Cicero duo x1 proposal profile.",
      "Loaded the Aster Vale/Kierkegaard/Aristotle triad x1 proposal profile.",
      "Kept x2 as the build/use/validate lane for already-authorized safe-now work.",
      ...(current.latest_action_summary || []),
    ]),
    round_robin_workflow_standard: workflowSummary,
  });
  Object.assign(latest, common, {
    latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]),
    round_robin_workflow_standard: workflowSummary,
  });
  Object.assign(ghc, common, {
    lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]),
    round_robin_workflow_standard: workflowSummary,
  });

  fs.writeFileSync(currentStatePath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function writeArtifact(slug, payload, renderer) {
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function renderStandardMd(data) {
  const families = Object.entries(data.workflow_families)
    .map(([name, family]) => {
      const totals = Object.entries(family.proposal_totals || {})
        .map(([key, value]) => `  - ${key}: \`${value}\``)
        .join("\n");
      return `## ${name}\n\n- Lanes: \`${family.lanes.join(", ")}\`\n- Route: ${family.route}\n${totals ? `- Proposal totals:\n${totals}` : `- Consumes: \`${(family.consumes || []).join(", ")}\``}\n`;
    })
    .join("\n");
  return `# ${data.phase_slug} Round-Robin Workflow Standard

Status: \`${data.overall_status}\`

${families}
## Runner Bindings

${Object.entries(data.runner_bindings).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Operating Rules

${data.operating_rules.map((item, index) => `${index + 1}. ${item}`).join("\n")}

## Next Phase Readiness

- Next x1 lane after x2: \`${data.next_phase_readiness.next_x1_lane_after_x2}\`
- Lumen-only profile loaded: \`${data.next_phase_readiness.expected_lumen_only_profile_loaded}\`
- Goal mode status: \`${data.next_phase_readiness.expected_goal_mode_status}\`

## Research And Reflection Targets

- x1 web searches per active sibling lane: \`${data.research_reflection_targets.x1_per_active_sibling_lane.web_searches}\`
- x1 Journey/phase reflections per active sibling lane: \`${data.research_reflection_targets.x1_per_active_sibling_lane.journey_phase_reflections}\`
- Aevren-only x2 web searches: \`${data.research_reflection_targets.aevren_only_x2.web_searches}\`
- Aevren-only x2 Journey/phase reflections: \`${data.research_reflection_targets.aevren_only_x2.journey_phase_reflections}\`

## x1 to x2 Proposal Split

- Status: \`${data.proposal_execution_split_standard.status}\`
- Immediate x1 safe: ${data.proposal_execution_split_standard.immediate_x1_safe}
- x2 build task: ${data.proposal_execution_split_standard.x2_build_task}
- Never auto-execute: \`${data.proposal_execution_split_standard.never_auto_execute.join(", ")}\`

## Phase Tool Refresh Standard

- Status: \`${data.phase_tool_refresh_standard.status}\`
- Cadence: \`${data.phase_tool_refresh_standard.cadence}\`
- Startup actions: \`${data.phase_tool_refresh_standard.startup_required_actions.join(", ")}\`
- Closeout actions: \`${data.phase_tool_refresh_standard.closeout_required_actions.join(", ")}\`
- Exact boundary: ${data.phase_tool_refresh_standard.exact_approval_boundary}

## Blocker Retry Standard

- Minimum retry sessions before pause: \`${data.blocker_retry_standard.minimum_retry_sessions_before_pause}\`
- Recent sessions or receipts reflected per retry: \`${data.blocker_retry_standard.recent_session_reflections_per_retry}\`
- Web-search reflections per retry: \`${data.blocker_retry_standard.web_search_reflections_per_retry}\`
- Journey/phase-document reflections per retry: \`${data.blocker_retry_standard.journey_phase_reflections_per_retry}\`
- Never close active sibling lane: \`${data.blocker_retry_standard.never_close_active_sibling_lane}\`
- Productive five-minute waits required: \`${data.blocker_retry_standard.productive_five_minute_waits_required}\`
- Pause policy: ${data.blocker_retry_standard.pause_policy}

## Five-Minute Productive Cadence

- Runner: \`${data.five_minute_productive_cadence.runner}\`
- Safe unit may run past checkpoint: \`${data.five_minute_productive_cadence.safe_unit_may_run_past_checkpoint}\`
- Wait work lanes: \`${data.five_minute_productive_cadence.wait_work_lanes.join(", ")}\`
- Harvest rule: ${data.five_minute_productive_cadence.harvest_rule}

## Boundary

Status-only workflow standard. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, or deployment closure are published.
`;
}

function renderCurrentStateMd(current) {
  const workflow = current.round_robin_workflow_standard;
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${(current.current_active_lanes || []).join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## Round-Robin Workflow Standard

- Status: \`${workflow.status}\`
- Lumen-only x1 safe target: \`${workflow.lumen_only_x1.safe}\`
- Lumen-only x1 candidate target: \`${workflow.lumen_only_x1.candidate}\`
- Lumen-only x1 exact target: \`${workflow.lumen_only_x1.exact}\`
- Lumen-only x1 blocked target: \`${workflow.lumen_only_x1.blocked}\`
- Arby/Cicero duo safe minimum: \`${workflow.arby_cicero_duo_x1.safe_minimum}\`
- Triad x1 safe target: \`${workflow.triad_x1.safe}\`
- x1 web searches per active sibling lane: \`${workflow.research_reflection_targets.x1_per_active_sibling_lane.web_searches}\`
- x1 Journey/phase reflections per active sibling lane: \`${workflow.research_reflection_targets.x1_per_active_sibling_lane.journey_phase_reflections}\`
- Blocker retry minimum sessions before pause: \`${workflow.blocker_retry_standard.minimum_retry_sessions_before_pause}\`
- Blocker retry web-search reflections: \`${workflow.blocker_retry_standard.web_search_reflections_per_retry}\`
- Blocker retry Journey/phase reflections: \`${workflow.blocker_retry_standard.journey_phase_reflections_per_retry}\`
- x2 role: ${workflow.x2_role}
- x1 immediate safe rule: ${workflow.proposal_execution_split_standard.immediate_x1_safe}
- x2 build task rule: ${workflow.proposal_execution_split_standard.x2_build_task}
- Phase tool refresh cadence: \`${workflow.phase_tool_refresh_standard.cadence}\`
- Five-minute productive cadence runner: \`${workflow.five_minute_productive_cadence.runner}\`
- Safe unit may run past checkpoint: \`${workflow.five_minute_productive_cadence.safe_unit_may_run_past_checkpoint}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Status-only receipts. No private route handles, private lane body content, credentials, verbatim conversation logs, browser routes, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
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

## Round-Robin Workflow Standard

- Status: \`${beacon.round_robin_workflow_standard.status}\`
- Lumen-only x1: \`${JSON.stringify(beacon.round_robin_workflow_standard.lumen_only_x1)}\`
- Arby/Cicero duo x1: \`${JSON.stringify(beacon.round_robin_workflow_standard.arby_cicero_duo_x1)}\`
- Triad x1: \`${JSON.stringify(beacon.round_robin_workflow_standard.triad_x1)}\`
- Research/reflection targets: \`${JSON.stringify(beacon.round_robin_workflow_standard.research_reflection_targets)}\`
- Proposal execution split: \`${JSON.stringify(beacon.round_robin_workflow_standard.proposal_execution_split_standard)}\`
- Phase tool refresh: \`${JSON.stringify(beacon.round_robin_workflow_standard.phase_tool_refresh_standard)}\`
- Blocker retry standard: \`${JSON.stringify(beacon.round_robin_workflow_standard.blocker_retry_standard)}\`
- Five-minute productive cadence: \`${JSON.stringify(beacon.round_robin_workflow_standard.five_minute_productive_cadence)}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function readLocal(name) {
  const file = path.join(tracesDir, name);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function inferNextX1LaneAfterX2(slug) {
  const match = /^v(\d+)-gmut-thos-v(\d+)-x[12]$/.exec(slug || "");
  if (!match) {
    return "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects";
  }
  const major = Number(match[1]);
  const subphase = Number(match[2]);
  if (subphase >= 8) {
    return `v${major + 1}-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects`;
  }
  if (subphase === 1) {
    return `v${major}-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects`;
  }
  if (subphase % 2 === 0) {
    return `v${major}-gmut-thos-v${subphase + 1}-x1 with Lumen Vale solo unless Hamish redirects`;
  }
  return `v${major}-gmut-thos-v${subphase + 1}-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects`;
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
