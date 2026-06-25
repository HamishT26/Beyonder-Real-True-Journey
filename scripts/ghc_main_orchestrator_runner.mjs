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

const fullToolsRoot = args.get("--full-tools-root");
if (!fullToolsRoot) {
  console.error("Usage: node ghc_v8_x1_background_runner_correction_builder.mjs --full-tools-root <path>");
  process.exit(2);
}

const phaseSlug = "v552-gmut-thos-v88-v8-x1";
const nextX2 = "v552-gmut-thos-v88-v8-x2";
let status = "V552_V8_X1_ACTIVE_BACKGROUND_APP_GATE_OPEN";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  private_route_handles_published: false,
  private_lane_body_content_published: false,
  raw_transcripts_published: false,
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

const sourceTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");
const source = {
  aster_cycle: readSource("v552-gmut-thos-v88-v8-x1-aster-vale-live-strict-cli-cycle-receipt-v1.json"),
  aster_completion: readSource("v552-gmut-thos-v88-v8-x1-aster-vale-live-strict-cli-cycle-completion-v1.json"),
  aster_quality: readSource("v552-gmut-thos-v88-v8-x1-aster-vale-live-strict-cli-cycle-quality-v1.json"),
  aster_marker: readSource("v552-gmut-thos-v88-v8-x1-aster-vale-live-strict-cli-cycle-marker-review-v1.json"),
  app_runner: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-runner-v1.json"),
  app_launcher: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-watch-launcher-v1.json"),
  app_gate: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-completion-gate-v1.json"),
  recovered_app_lane: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-v1.json"),
  recovered_app_preflight: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-preflight-v1.json"),
  recovered_app_runner: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-runner-v1.json"),
  recovered_app_gate: readSource("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-completion-gate-v1.json"),
  aristotle_fallback: readSource("v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-v1.json"),
  aristotle_fallback_preflight: readSource("v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-preflight-v1.json"),
  aristotle_fallback_runner: readSource("v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-runner-v1.json"),
  aristotle_fallback_gate: readSource("v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-completion-gate-v1.json"),
  orchestrator: readLocal("v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-v1.json"),
  private_preflight: readLocal("v552-gmut-thos-v88-v8-x1-private-app-lane-map-preflight-v1.json"),
  five_minute_cadence: readLocal("v552-gmut-thos-v88-v8-x1-five-minute-status-cadence-guard-v1.json"),
  recovered_five_minute_cadence: readLocal("v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-five-minute-cadence-guard-v2.json"),
  aristotle_fallback_cadence: readLocal("v552-gmut-thos-v88-v8-x1-aristotle-fallback-five-minute-cadence-guard-v2.json"),
  updater_startup: readLocal("v552-gmut-thos-v88-v8-x1-updater-runner-supervision-startup-v1.json"),
  updater_compact: readLocal("v552-gmut-thos-v88-v8-x1-updater-runner-compact-pause-v1.json"),
};

const localPrivateRegistry = readLocalPrivateRegistry(path.join(repoRoot, ".ghc-private", "app-lane-registry.local.json"));
const effectiveAppGate = buildEffectiveAppGate();
const effectivePhaseClosed =
  source.aster_cycle.overall_status === "PASS_STRICT_CLI_CYCLE_READY" &&
  effectiveAppGate.overall_status === "PASS_EFFECTIVE_APP_LANE_COMPLETION_GATE";
status = effectivePhaseClosed ? "V552_V8_X1_CLOSED_V8_X2_READY_NOT_STARTED" : "V552_V8_X1_ACTIVE_BACKGROUND_APP_GATE_OPEN";
const currentActivePhaseAfterReceipt = effectivePhaseClosed ? nextX2 : phaseSlug;
const latestClosedPhaseAfterReceipt = effectivePhaseClosed ? phaseSlug : "v552-gmut-thos-v88-v7-x2";
const latestCompletedX1AfterReceipt = effectivePhaseClosed ? phaseSlug : "v552-gmut-thos-v88-v7-x1";
const nextX2Ready = effectivePhaseClosed;

const liveReceipt = {
  artifact_type: "ghc_v8_x1_mandatory_background_runner_live_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: effectivePhaseClosed ? "PASS_V8_X1_EFFECTIVE_TRIAD_GATE_CLOSED" : "OPEN_GAP_V8_X1_BACKGROUND_APP_GATE",
  main_orchestrator_runner: {
    promoted_entrypoint: "scripts/ghc_main_orchestrator_runner.mjs",
    compatibility_entrypoint: "scripts/ghc_v8_x1_background_runner_correction_builder.mjs",
    promoted_from: "ghc_v8_x1_background_runner_correction_builder.mjs",
    role: "primary orchestration receipt builder for recovered app-lane routing, updater cadence, full-tools support, and sanitized omega-mini current-state publication",
    promoted: true,
  },
  mandatory_five_lane_sibling_route: {
    primary_for_broad_sibling_runs: true,
    strict_cli_lanes: ["Arby", "Aster Vale"],
    recovered_app_lanes: ["Cicero", "Kierkegaard", "Aristotle"],
    strict_cli_required_gates: ["completion", "elaboration_quality", "marker_review"],
    app_lane_required_gates: ["notifier", "completion_gate"],
    stale_manual_or_partial_routes_deprecated: true,
    watcher_start_is_completion_proof: false,
    closeout_requires_all_five_lane_gates: true,
  },
  aster_vale: {
    route: "strict_cli_lane_cycle",
    cycle_status: source.aster_cycle.overall_status || "missing",
    completion_status: source.aster_completion.aggregate_status || source.aster_cycle.completion_status || "missing",
    quality_status: source.aster_quality.aggregate_status || source.aster_cycle.quality_status || "missing",
    marker_status: source.aster_marker.overall_status || source.aster_cycle.marker_status || "missing",
    completion_gate_passed: source.aster_cycle.overall_status === "PASS_STRICT_CLI_CYCLE_READY",
    raw_output_published: false,
  },
  kierkegaard_aristotle: {
    route: "ghc_recovered_app_lane_map_runner_to_council_app_lane_notifier_background_watch",
    runner_status: source.app_runner.overall_status || "missing",
    watch_launcher_status: source.app_launcher.overall_status || "missing",
    completion_gate_status: effectiveAppGate.overall_status,
    expected_lanes: ["Kierkegaard", "Aristotle"],
    open_gaps: effectiveAppGate.open_gaps,
    watcher_start_is_completion_proof: false,
    completion_gate_passed: effectiveAppGate.overall_status === "PASS_EFFECTIVE_APP_LANE_COMPLETION_GATE",
    raw_app_payload_published: false,
  },
  effective_app_lane_gate: effectiveAppGate,
  recovered_app_lane_route: {
    connector: "ghc_recovered_app_lane_map_runner.mjs",
    default_for_local_app_lane_siblings: true,
    excludes_main_thread_agents: true,
    boolean_flag_invocation_rule: "Pass explicit paired values for runner booleans, such as --allow-turn-start-after-resume-timeout true --background-watch true.",
    private_source_override_rule: "If the default private map source is missing after a Codex app update or worktree rotation, use a process-local THOS_APP_LANE_POLICY_SOURCE, GHC_APP_LANE_POLICY_SOURCE, or THOS_APP_LANE_IDS_JSON route; publish only sanitized source basenames, source_override_used, handle counts, statuses, and child receipt names.",
    status: source.recovered_app_lane.overall_status || "missing",
    preflight_status: source.recovered_app_preflight.overall_status || "missing",
    runner_status: source.recovered_app_runner.overall_status || "missing",
    completion_gate_status: source.recovered_app_gate.overall_status || "missing",
    recovered_handle_count: source.recovered_app_lane.recovered_handle_count || 0,
    raw_handles_published: false,
    background_watch_requested: Boolean(source.recovered_app_lane.background_watch_requested),
  },
  orchestrator: {
    route: "safe_runner_orchestrator",
    status: source.orchestrator.overall_status || "missing",
    runner_count: source.orchestrator.runner_count || 0,
  },
  supervision: {
    updater_runner_status: source.updater_startup.overall_status || "missing",
    compact_pause_updater_status: source.updater_compact.overall_status || "missing",
    cadence_guard_status: source.five_minute_cadence.overall_status || "missing",
    recovered_route_cadence_status: source.recovered_five_minute_cadence.overall_status || "missing",
    aristotle_fallback_cadence_status: source.aristotle_fallback_cadence.overall_status || "missing",
    cadence_threshold_seconds: source.five_minute_cadence.threshold_seconds || 300,
    five_minute_checks_mandatory: true,
    status_classes: ["active_fresh", "active_stale", "completed_ready_for_harvest", "open_gap"],
    babysitting_replaced_by_background_supervision: true,
  },
  private_lane_registry: {
    local_registry_supported: true,
    local_registry_present: localPrivateRegistry.present,
    configured_lanes: localPrivateRegistry.configured_lanes,
    missing_lanes: localPrivateRegistry.missing_lanes,
    env_preflight_status: source.private_preflight.overall_status || "missing",
    raw_ids_published: false,
    raw_registry_path_published: false,
    rehydrate_rule: "Private IDs stay in the local ignored registry or current shell environment, then app-lane runners receive them through THOS_APP_LANE_IDS_JSON.",
  },
  full_tools_support: {
    support_worktree_role: "private-preflight app-lane-notifier completion-gates strict-cli-cycle and richer helper tooling",
    omega_mini_role: "sanitized-public-receipts-and-current-state",
    private_handles_published_to_omega_mini: false,
    use_full_tools_lanes_first_when_needed: true,
    daily_branch_worktree_creation_cap: {
      timezone: "Pacific/Auckland",
      max_new_omega_mini_full_tools_pairs_per_day: 3,
      fresh_exact_override_required_above_cap: true,
    },
  },
  mandatory_rule: {
    background_notifier_orchestrator_first: true,
    recovered_app_lane_map_runner_default: true,
    updater_runners_required_for_startup_resume_and_compact_pause: true,
    five_minute_status_checks_required: true,
    full_tools_support_worktree_required_for_private_or_rich_lane_helpers: true,
    local_only_app_lane_source_override_before_open_gap: true,
    max_three_new_mini_full_tools_worktree_pairs_per_day: true,
    no_stale_direct_manual_downgrade: true,
    existing_inducted_lanes_only: true,
    no_new_agents_spawned: true,
    held_main_thread_siblings_activated: false,
    phase_advance_requires_completion_gate: true,
  },
  next_safe_step: "Rehydrate the private app-lane map and rerun Kierkegaard/Aristotle through the background notifier runner, then harvest the completion gate before advancing to v8 x2.",
  source_receipts: {
    aster_cycle: "v552-gmut-thos-v88-v8-x1-aster-vale-live-strict-cli-cycle-receipt-v1.json",
    app_runner: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-runner-v1.json",
    app_launcher: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-watch-launcher-v1.json",
    app_gate: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-background-app-completion-gate-v1.json",
    orchestrator: "v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-v1.json",
    private_preflight: "v552-gmut-thos-v88-v8-x1-private-app-lane-map-preflight-v1.json",
    five_minute_cadence: "v552-gmut-thos-v88-v8-x1-five-minute-status-cadence-guard-v1.json",
    recovered_app_lane: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-v1.json",
    recovered_app_preflight: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-preflight-v1.json",
    recovered_app_runner: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-runner-v1.json",
    recovered_app_gate: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-app-lane-completion-gate-v1.json",
    recovered_five_minute_cadence: "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-five-minute-cadence-guard-v2.json",
    aristotle_fallback: "v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-v1.json",
    aristotle_fallback_preflight: "v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-preflight-v1.json",
    aristotle_fallback_runner: "v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-runner-v1.json",
    aristotle_fallback_gate: "v552-gmut-thos-v88-v8-x1-aristotle-recovered-app-lane-fallback-completion-gate-v1.json",
    aristotle_fallback_cadence: "v552-gmut-thos-v88-v8-x1-aristotle-fallback-five-minute-cadence-guard-v2.json",
    updater_startup: "v552-gmut-thos-v88-v8-x1-updater-runner-supervision-startup-v1.json",
    updater_compact: "v552-gmut-thos-v88-v8-x1-updater-runner-compact-pause-v1.json",
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("mandatory-background-runner-live-receipt", liveReceipt, renderLiveReceiptMd);

const recoveredRouteReceipt = {
  artifact_type: "ghc_v8_x1_recovered_app_lane_route_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: effectiveAppGate.overall_status === "PASS_EFFECTIVE_APP_LANE_COMPLETION_GATE"
    ? "PASS_RECOVERED_APP_LANE_EFFECTIVE_COMPLETION_GATE"
    : source.recovered_app_lane.overall_status || "OPEN_GAP_RECOVERED_APP_LANE_ROUTE_STATUS_MISSING",
  connector: "ghc_recovered_app_lane_map_runner.mjs",
  lanes: ["Kierkegaard", "Aristotle"],
  default_for_local_app_lane_siblings: true,
  excludes_main_thread_agents: true,
  private_source_override_supported: true,
  private_source_override_rule:
    "Use THOS_APP_LANE_POLICY_SOURCE, GHC_APP_LANE_POLICY_SOURCE, or process-local THOS_APP_LANE_IDS_JSON when the default private map source is missing; never copy private IDs into branch artifacts.",
  recovered_handle_count: source.recovered_app_lane.recovered_handle_count || 0,
  background_watch_requested: Boolean(source.recovered_app_lane.background_watch_requested),
  preflight_status: source.recovered_app_preflight.overall_status || "missing",
  runner_status: source.recovered_app_runner.overall_status || "missing",
  completion_gate_status: effectiveAppGate.overall_status,
  first_group_gate_status: source.recovered_app_gate.overall_status || "missing",
  aristotle_fallback_gate_status: source.aristotle_fallback_gate.overall_status || "missing",
  five_minute_cadence_status: source.recovered_five_minute_cadence.overall_status || "missing",
  aristotle_fallback_cadence_status: source.aristotle_fallback_cadence.overall_status || "missing",
  effective_app_gate: effectiveAppGate,
  next_phase_allowed: effectiveAppGate.overall_status === "PASS_EFFECTIVE_APP_LANE_COMPLETION_GATE",
  open_gaps: effectiveAppGate.open_gaps,
  safe_wait_policy: {
    check_only_at_five_minute_marks: true,
    do_safe_now_work_between_marks: true,
    continuous_safe_now_approval_packet_eureka_and_cleanup_work: true,
    cadence_marks_are_check_opportunities_not_forced_stops: true,
    harvest_at_next_natural_safe_pause_after_cadence_mark: true,
    watcher_start_is_completion_proof: false,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("recovered-app-lane-route-receipt", recoveredRouteReceipt, renderRecoveredRouteReceiptMd);

const routeStandard = {
  artifact_type: "ghc_v8_x1_mandatory_background_notifier_orchestrator_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_MANDATORY_BACKGROUND_NOTIFIER_ORCHESTRATOR_STANDARD_RECORDED",
  mandatory_rules: [
    "Use ghc_main_orchestrator_runner.mjs as the promoted main orchestration runner for this route family.",
    "Use ghc_recovered_app_lane_map_runner.mjs by default for local app-lane siblings that are not main-thread agents.",
    "When invoking ghc_recovered_app_lane_map_runner.mjs, pass explicit paired values for boolean flags so fallback and background-watch flags are both preserved.",
    "Use recovered notifier/background/orchestrator runners first for existing inducted app-lane siblings.",
    "Do not downgrade to stale direct/manual foreground modes when the background route is available.",
    "Use updater runners at startup, resume, and compact-pause boundaries before harvesting lane truth.",
    "Run five-minute status cadence checks while siblings continue in the background, continuously do safe-now approval packet, eureka, cleanup, validation, and orchestration work between marks, and harvest at the next natural safe pause after a mark.",
    "Use safe runner orchestrator during background waiting instead of babysitting.",
    "Use the full-tools support worktree for private-map preflights, app-lane notifier runners, completion gates, strict CLI cycles, and richer helper tooling.",
    "Keep private lane IDs in a local ignored registry or shell environment only; publish sanitized presence/open-gap receipts to omega-mini.",
    "Watcher start is not completion proof; harvest notifier and completion-gate receipts.",
    "If private app-lane map material is missing, publish a recoverable open-gap receipt and keep the phase active.",
    "Do not spawn new agents or activate held main-thread siblings without Hamish explicitly asking.",
    "Use the active round-robin workflow standard for x1 proposal counts and x2 safe-now build/use/validation scope.",
  ],
  round_robin_workflows: {
    lumen_only_x1: {
      starts_at: "v553-gmut-thos-v1-x1",
      lanes: ["Aevren Vale", "Lumen Vale"],
      proposal_totals: {
        safe: 50,
        candidate: 30,
        exact: 20,
        blocked: 10,
        skills: 20,
        runners: 10,
        cleanup: 30,
      },
    },
    arby_cicero_duo_x1: {
      lanes: ["Aevren Vale", "Arby", "Cicero"],
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
      proposal_totals: {
        safe: 20,
        candidate: 12,
        exact: 12,
        skills: 20,
        runners: 8,
        cleanup: 40,
      },
    },
    x2: {
      role: "build, run, test, install, use, validate, and publish already-authorized safe-now work",
      exact_and_blocked_gates: "queued unless freshly approved",
    },
  },
  applies_to: ["Cicero", "Kierkegaard", "Aristotle", "Arby", "Aster Vale"],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("mandatory-background-notifier-orchestrator-standard", routeStandard, renderRouteStandardMd);
rewritePhaseArtifacts();
refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V8_X1_BACKGROUND_RUNNER_CORRECTION_WRITTEN",
  phase_slug: phaseSlug,
  current_status: status,
  aster_status: liveReceipt.aster_vale.cycle_status,
  app_gate_status: liveReceipt.kierkegaard_aristotle.completion_gate_status,
}, null, 2));

function rewritePhaseArtifacts() {
  const phaseStatus = {
    artifact_type: "ghc_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: effectivePhaseClosed ? "PASS_V8_X1_TRIAD_COMPLETION_CLOSED" : "OPEN_GAP_V8_X1_BACKGROUND_APP_GATE",
    latest_closed_phase_after_receipt: latestClosedPhaseAfterReceipt,
    latest_completed_x1_after_receipt: latestCompletedX1AfterReceipt,
    latest_completed_x2_after_receipt: "v552-gmut-thos-v88-v7-x2",
    current_active_phase_after_receipt: currentActivePhaseAfterReceipt,
    next_x2_scope: nextX2,
    next_x2_ready: nextX2Ready,
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
    artifacts: lookupFileNames(),
    counts: {
      safe_approval_packets: 20,
      candidate_approval_packets: 12,
      exact_approval_packets: 12,
      skill_ideas: 20,
      runner_ideas: 8,
      cleanup_tasks: 40,
    },
    lane_gate_status: {
      aster_vale: source.aster_cycle.overall_status || "missing",
      kierkegaard_aristotle: effectiveAppGate.overall_status,
      mandatory_orchestrator: source.orchestrator.overall_status || "missing",
      recovered_app_lane_runner: source.recovered_app_lane.overall_status || "missing",
      recovered_app_preflight: source.recovered_app_preflight.overall_status || "missing",
      private_map_preflight: source.private_preflight.overall_status || "missing",
      five_minute_cadence_guard: source.five_minute_cadence.overall_status || "missing",
      recovered_five_minute_cadence_guard: source.recovered_five_minute_cadence.overall_status || "missing",
      updater_runner: source.updater_startup.overall_status || "missing",
      compact_pause_updater: source.updater_compact.overall_status || "missing",
    },
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
  writeArtifact("phase-status-index", phaseStatus, renderPhaseStatusMd);

  const closeout = {
    artifact_type: "ghc_phase_closeout",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: effectivePhaseClosed ? "PASS_V8_X1_CLOSED_V8_X2_READY_NOT_STARTED" : "SUPERSEDED_V8_X1_NOT_CLOSED_BACKGROUND_APP_GATE_OPEN",
    closeout_superseded_by: effectivePhaseClosed ? null : "v552-gmut-thos-v88-v8-x1-mandatory-background-runner-live-receipt-v1.json",
    latest_closed_phase_after_receipt: latestClosedPhaseAfterReceipt,
    latest_completed_x1_after_receipt: latestCompletedX1AfterReceipt,
    latest_completed_x2_after_receipt: "v552-gmut-thos-v88-v7-x2",
    current_active_phase_after_receipt: currentActivePhaseAfterReceipt,
    next_x2_scope: nextX2,
    next_x2_ready: nextX2Ready,
    evidence: lookupFileNames(),
    open_gate: {
      reason: effectivePhaseClosed
        ? "Effective app-lane completion gate passed through Kierkegaard group completion plus Aristotle fallback completion."
        : "Kierkegaard/Aristotle background app-lane completion gate is open.",
      gate_status: effectiveAppGate.overall_status,
      open_gaps: effectiveAppGate.open_gaps,
    },
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
  writeArtifact("closeout", closeout, renderCloseoutMd);

  const snapshot = {
    artifact_type: "ghc_compact_pause_startup_snapshot",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: effectivePhaseClosed ? "PASS_V8_X1_CLOSED_STARTUP_SNAPSHOT_READY" : "PASS_V8_X1_OPEN_GATE_STARTUP_SNAPSHOT_READY",
    startup_order: [
      "Read omega-mini current-state first.",
      "Read omega-mini latest-updates beacon second.",
      "Read GHC current-state beacon third.",
      "Open the v8 x1 mandatory background runner live receipt.",
      "Open the private app-lane map preflight and local registry status receipt.",
      "Run the updater runner and five-minute cadence guard before each status harvest.",
      "Use ghc_recovered_app_lane_map_runner.mjs for local app-lane siblings before any direct app-lane fallback.",
      effectivePhaseClosed
        ? "Treat v8 x1 as closed and hold v8 x2 ready/not-started until Hamish starts x2."
        : "Keep v8 x1 active until the Kierkegaard/Aristotle app-lane completion gate passes.",
    ],
    current_pointer_after_receipt: {
      status,
      current_active_phase: currentActivePhaseAfterReceipt,
      latest_closed_phase: latestClosedPhaseAfterReceipt,
      latest_completed_x1_phase: latestCompletedX1AfterReceipt,
      latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
      next_x2_scope: nextX2,
      next_x2_ready: nextX2Ready,
    },
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
  writeArtifact("compact-pause-startup-snapshot", snapshot, renderStartupSnapshotMd);
}

function refreshBeacons() {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = JSON.parse(fs.readFileSync(currentPath, "utf8"));
  const latest = JSON.parse(fs.readFileSync(latestPath, "utf8"));
  const ghc = JSON.parse(fs.readFileSync(ghcPath, "utf8"));
  const lookupFiles = [
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
    ...lookupFileNames().flatMap((file) => [
      `docs/trinity-live-traces/${file.replace(/\.json$/, ".md")}`,
      `docs/trinity-live-traces/${file}`,
    ]),
  ];

  const common = {
    generated_utc: generatedUtc,
    status,
    current_active_phase: currentActivePhaseAfterReceipt,
    latest_closed_phase: latestClosedPhaseAfterReceipt,
    latest_completed_x1_phase: latestCompletedX1AfterReceipt,
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    current_active_lanes: effectivePhaseClosed ? [
      "v8-x1-triad-completed",
      "v8-x2-ready-not-started",
      "Aster Vale strict CLI lane completed",
      "Kierkegaard completed through recovered app-lane runner",
      "Aristotle completed through fallback recovered app-lane runner",
      "ghc-main-orchestrator-runner-promoted",
      "ghc-recovered-app-lane-map-runner-default",
    ] : [
      "Aster Vale strict CLI lane completed",
      "Kierkegaard and Aristotle background app-lane completion gate open",
      "ghc-recovered-app-lane-map-runner-default",
      "mandatory-background-notifier-orchestrator-route",
      "full-tools-support-worktree-enabled",
      "five-minute-background-status-cadence",
      "v8-x1-active-not-closed",
    ],
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  };

  Object.assign(current, common, {
    updated_at: generatedNz,
    just_closed_lanes: effectivePhaseClosed
      ? [
          "v552 v8 x1 effective triad completion gate closed",
          "Aster Vale strict CLI lane completed",
          "Kierkegaard recovered app-lane run completed",
          "Aristotle fallback recovered app-lane run completed",
        ]
      : [
          "v7 x2 remains the latest closed phase",
          "v8 x1 planning artifacts are published but live app-lane gate remains open",
        ],
    next_expected_scope: currentActivePhaseAfterReceipt,
    current_lookup_files: lookupFiles,
    latest_action_summary: [
      "Hamish made the background notifier/orchestrator route mandatory for existing app-lane siblings.",
      "Aster Vale completed the strict CLI lane cycle for v8 x1.",
      "Kierkegaard and Aristotle were launched through the council app-lane notifier runner in background-watch mode.",
      "The safe runner orchestrator ran during background waiting.",
      "The startup updater and five-minute cadence guard are part of the mandatory supervision route.",
      "Kierkegaard and Aristotle were restarted through ghc_recovered_app_lane_map_runner.mjs in background-watch mode.",
      "Kierkegaard completed in the recovered two-lane route.",
      "Aristotle completed in an explicit fallback recovered route after the first resume timed out.",
      effectivePhaseClosed
        ? "v552 v8 x1 is closed; v552 v8 x2 is ready and not started."
        : "v552 v8 x1 remains active and not closed until the app-lane completion gate passes.",
      "The full-tools support worktree is the preferred lane for private app-lane preflights, notifier runners, strict CLI cycles, and completion gates.",
      "Private app-lane IDs remain local-only; omega-mini records sanitized presence/open-gap status only.",
      effectivePhaseClosed ? "Next x2 is ready but not started." : "Next x2 remains gated and not started.",
    ],
    v8_x1_background_runner_correction: {
      status: "active_open_gate",
      effective_status: effectivePhaseClosed ? "closed_x2_ready_not_started" : "active_open_gate",
      main_orchestrator_runner_entrypoint: "scripts/ghc_main_orchestrator_runner.mjs",
      compatibility_entrypoint: "scripts/ghc_v8_x1_background_runner_correction_builder.mjs",
      aster_vale_strict_cli_status: source.aster_cycle.overall_status || "missing",
      kierkegaard_aristotle_app_gate_status: source.recovered_app_gate.overall_status || source.app_gate.overall_status || "missing",
      mandatory_orchestrator_status: source.orchestrator.overall_status || "missing",
      recovered_app_lane_runner_status: source.recovered_app_lane.overall_status || "missing",
      recovered_app_lane_preflight_status: source.recovered_app_preflight.overall_status || "missing",
      recovered_app_lane_completion_gate_status: source.recovered_app_gate.overall_status || "missing",
      private_app_lane_map_preflight_status: source.private_preflight.overall_status || "missing",
      five_minute_cadence_guard_status: source.five_minute_cadence.overall_status || "missing",
      recovered_five_minute_cadence_guard_status: source.recovered_five_minute_cadence.overall_status || "missing",
      updater_runner_status: source.updater_startup.overall_status || "missing",
      compact_pause_updater_status: source.updater_compact.overall_status || "missing",
      background_notifier_orchestrator_route_mandatory: true,
      recovered_app_lane_map_runner_mandatory: true,
      updater_runners_mandatory: true,
      five_minute_checks_mandatory: true,
      full_tools_support_worktree_mandatory: true,
      no_stale_direct_manual_downgrade: true,
      watcher_start_is_completion_proof: false,
      phase_closed: effectivePhaseClosed,
      next_x2_ready: nextX2Ready,
    },
  });
  Object.assign(latest, common, { latest_lookup_files: lookupFiles });
  Object.assign(ghc, common, { lookup_files: lookupFiles });

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderLatestBeaconMd(latest), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderGhcBeaconMd(ghc), "utf8");
}

function lookupFileNames() {
  return [
    "v552-gmut-thos-v88-v8-x1-toolchain-refresh-v1.json",
    "v552-gmut-thos-v88-v8-x1-triad-approval-packets-v1.json",
    "v552-gmut-thos-v88-v8-x1-skill-runner-cleanup-proposals-v1.json",
    "v552-gmut-thos-v88-v8-x1-future-round-robin-workflow-standard-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-startup-context-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-reflection-ledger-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-safe-runner-orchestrator-compact-pause-v1.json",
    "v552-gmut-thos-v88-v8-x1-private-app-lane-map-preflight-v1.json",
    "v552-gmut-thos-v88-v8-x1-five-minute-status-cadence-guard-v1.json",
    "v552-gmut-thos-v88-v8-x1-recovered-app-lane-route-receipt-v1.json",
    "v552-gmut-thos-v88-v8-x1-kierkegaard-aristotle-recovered-five-minute-cadence-guard-v2.json",
    "v552-gmut-thos-v88-v8-x1-aristotle-fallback-five-minute-cadence-guard-v2.json",
    "v552-gmut-thos-v88-v8-x1-updater-runner-supervision-startup-v1.json",
    "v552-gmut-thos-v88-v8-x1-updater-runner-compact-pause-v1.json",
    "v552-gmut-thos-v88-v8-x1-updater-runner-compact-pause-startup-snapshot-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-background-notifier-orchestrator-standard-v1.json",
    "v552-gmut-thos-v88-v8-x1-mandatory-background-runner-live-receipt-v1.json",
    "v552-gmut-thos-v88-v8-x1-phase-status-index-v1.json",
    "v552-gmut-thos-v88-v8-x1-closeout-v1.json",
    "v552-gmut-thos-v88-v8-x1-compact-pause-startup-snapshot-v1.json",
  ];
}

function readSource(name) {
  const file = path.join(sourceTraceDir, name);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
}

function readLocal(name) {
  const file = path.join(tracesDir, name);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
}

function readLocalPrivateRegistry(file) {
  if (!fs.existsSync(file)) {
    return { present: false, configured_lanes: [], missing_lanes: ["Cicero", "Kierkegaard", "Aristotle"] };
  }
  try {
    const payload = JSON.parse(fs.readFileSync(file, "utf8"));
    const lanes = payload?.lanes && typeof payload.lanes === "object" ? payload.lanes : {};
    const names = ["Cicero", "Kierkegaard", "Aristotle"];
    const configured = names.filter((name) => typeof lanes[name] === "string" && lanes[name].trim().length > 0);
    return {
      present: true,
      configured_lanes: configured,
      missing_lanes: names.filter((name) => !configured.includes(name)),
    };
  } catch {
    return { present: true, configured_lanes: [], missing_lanes: ["Cicero", "Kierkegaard", "Aristotle"] };
  }
}

function buildEffectiveAppGate() {
  const groupRows = Array.isArray(source.recovered_app_gate.lanes) ? source.recovered_app_gate.lanes : [];
  const fallbackRows = Array.isArray(source.aristotle_fallback_gate.lanes) ? source.aristotle_fallback_gate.lanes : [];
  const kierkegaard = groupRows.find((row) => row?.lane === "Kierkegaard") || {};
  const aristotleFromGroup = groupRows.find((row) => row?.lane === "Aristotle") || {};
  const aristotleFallback = fallbackRows.find((row) => row?.lane === "Aristotle") || {};
  const kierkegaardComplete = laneComplete(kierkegaard);
  const aristotleComplete = laneComplete(aristotleFromGroup) || laneComplete(aristotleFallback);
  const openGaps = [];
  if (!kierkegaardComplete) {
    openGaps.push(`Kierkegaard:${kierkegaard.overall_status || "missing"}/${kierkegaard.completion_status || "missing"}`);
  }
  if (!aristotleComplete) {
    openGaps.push(`Aristotle:${aristotleFallback.overall_status || aristotleFromGroup.overall_status || "missing"}/${aristotleFallback.completion_status || aristotleFromGroup.completion_status || "missing"}`);
  }
  return {
    artifact_type: "effective_app_lane_completion_gate",
    overall_status: openGaps.length ? "OPEN_GAP_EFFECTIVE_APP_LANE_COMPLETION_GATE" : "PASS_EFFECTIVE_APP_LANE_COMPLETION_GATE",
    source_gates: {
      kierkegaard_aristotle_group_gate: source.recovered_app_gate.overall_status || "missing",
      aristotle_fallback_gate: source.aristotle_fallback_gate.overall_status || "missing",
    },
    lanes: [
      {
        lane: "Kierkegaard",
        source: "kierkegaard_aristotle_recovered_app_lane_gate",
        overall_status: kierkegaard.overall_status || "missing",
        completion_status: kierkegaard.completion_status || "missing",
        effective_completion: kierkegaardComplete,
      },
      {
        lane: "Aristotle",
        source: laneComplete(aristotleFallback)
          ? "aristotle_fallback_recovered_app_lane_gate"
          : "kierkegaard_aristotle_recovered_app_lane_gate",
        group_overall_status: aristotleFromGroup.overall_status || "missing",
        group_completion_status: aristotleFromGroup.completion_status || "missing",
        fallback_overall_status: aristotleFallback.overall_status || "missing",
        fallback_completion_status: aristotleFallback.completion_status || "missing",
        effective_completion: aristotleComplete,
      },
    ],
    open_gaps: openGaps,
    watcher_start_is_completion_proof: false,
    raw_ids_published: false,
    raw_lane_content_published: false,
  };
}

function laneComplete(row) {
  return row?.overall_status === "completed" && row?.completion_status === "completed";
}

function writeArtifact(slug, payload, renderer) {
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function renderLiveReceiptMd(data) {
  return `# v552 v8 x1 Mandatory Background Runner Live Receipt

Status: \`${data.overall_status}\`

## Aster Vale

- Route: \`${data.aster_vale.route}\`
- Cycle status: \`${data.aster_vale.cycle_status}\`
- Completion status: \`${data.aster_vale.completion_status}\`
- Quality status: \`${data.aster_vale.quality_status}\`
- Marker status: \`${data.aster_vale.marker_status}\`

## Kierkegaard And Aristotle

- Route: \`${data.kierkegaard_aristotle.route}\`
- Runner status: \`${data.kierkegaard_aristotle.runner_status}\`
- Watch launcher status: \`${data.kierkegaard_aristotle.watch_launcher_status}\`
- Completion gate status: \`${data.kierkegaard_aristotle.completion_gate_status}\`
- Watcher start is completion proof: \`${data.kierkegaard_aristotle.watcher_start_is_completion_proof}\`

## Main Orchestrator Runner

- Promoted entrypoint: \`${data.main_orchestrator_runner.promoted_entrypoint}\`
- Compatibility entrypoint: \`${data.main_orchestrator_runner.compatibility_entrypoint}\`
- Promoted from: \`${data.main_orchestrator_runner.promoted_from}\`
- Promoted: \`${data.main_orchestrator_runner.promoted}\`

## Supervision

- Updater runner status: \`${data.supervision.updater_runner_status}\`
- Compact-pause updater status: \`${data.supervision.compact_pause_updater_status}\`
- Five-minute cadence status: \`${data.supervision.cadence_guard_status}\`
- Recovered route cadence status: \`${data.supervision.recovered_route_cadence_status}\`
- Five-minute checks mandatory: \`${data.supervision.five_minute_checks_mandatory}\`
- Babysitting replaced by background supervision: \`${data.supervision.babysitting_replaced_by_background_supervision}\`

## Recovered App-Lane Runner

- Connector: \`${data.recovered_app_lane_route.connector}\`
- Default for local app-lane siblings: \`${data.recovered_app_lane_route.default_for_local_app_lane_siblings}\`
- Excludes main-thread agents: \`${data.recovered_app_lane_route.excludes_main_thread_agents}\`
- Boolean flag invocation rule: ${data.recovered_app_lane_route.boolean_flag_invocation_rule}
- Status: \`${data.recovered_app_lane_route.status}\`
- Preflight status: \`${data.recovered_app_lane_route.preflight_status}\`
- Runner status: \`${data.recovered_app_lane_route.runner_status}\`
- Completion gate status: \`${data.recovered_app_lane_route.completion_gate_status}\`
- Recovered handle count: \`${data.recovered_app_lane_route.recovered_handle_count}\`
- Raw handles published: \`${data.recovered_app_lane_route.raw_handles_published}\`

## Private Lane Registry

- Local private registry supported: \`${data.private_lane_registry.local_registry_supported}\`
- Local private registry present: \`${data.private_lane_registry.local_registry_present}\`
- Configured lanes: \`${data.private_lane_registry.configured_lanes.join(", ") || "none"}\`
- Missing lanes: \`${data.private_lane_registry.missing_lanes.join(", ") || "none"}\`
- Env preflight status: \`${data.private_lane_registry.env_preflight_status}\`
- Raw IDs published: \`${data.private_lane_registry.raw_ids_published}\`

## Full Tools Support

- Use full-tools support worktree first when private or richer lane helpers are needed: \`${data.full_tools_support.use_full_tools_lanes_first_when_needed}\`
- Private handles published to omega-mini: \`${data.full_tools_support.private_handles_published_to_omega_mini}\`

## Open Gaps

${(data.kierkegaard_aristotle.open_gaps || []).map((gap) => `- \`${gap}\``).join("\n") || "- None"}

## Next Safe Step

${data.next_safe_step}
`;
}

function renderRouteStandardMd(data) {
  const workflows = Object.entries(data.round_robin_workflows)
    .map(([name, workflow]) => {
      const totals = workflow.proposal_totals
        ? Object.entries(workflow.proposal_totals)
            .map(([key, value]) => `  - ${key}: \`${value}\``)
            .join("\n")
        : `  - role: ${workflow.role}\n  - exact and blocked gates: ${workflow.exact_and_blocked_gates}`;
      const lanes = workflow.lanes ? `- Lanes: \`${workflow.lanes.join(", ")}\`\n` : "";
      return `### ${name}\n\n${lanes}- Totals:\n${totals}`;
    })
    .join("\n\n");
  return `# v552 v8 x1 Mandatory Background Notifier Orchestrator Standard\n\nStatus: \`${data.overall_status}\`\n\n## Mandatory Rules\n\n${data.mandatory_rules.map((item, index) => `${index + 1}. ${item}`).join("\n")}\n\n## Round-Robin Workflows\n\n${workflows}\n\nApplies to: \`${data.applies_to.join(", ")}\`\n`;
}

function renderRecoveredRouteReceiptMd(data) {
  return `# v552 v8 x1 Recovered App-Lane Route Receipt

Status: \`${data.overall_status}\`

## Route

- Connector: \`${data.connector}\`
- Lanes: \`${data.lanes.join(", ")}\`
- Default for local app-lane siblings: \`${data.default_for_local_app_lane_siblings}\`
- Excludes main-thread agents: \`${data.excludes_main_thread_agents}\`
- Recovered handle count: \`${data.recovered_handle_count}\`
- Background watch requested: \`${data.background_watch_requested}\`

## Gate Status

- Preflight status: \`${data.preflight_status}\`
- Runner status: \`${data.runner_status}\`
- Completion gate status: \`${data.completion_gate_status}\`
- Five-minute cadence status: \`${data.five_minute_cadence_status}\`
- Next phase allowed: \`${data.next_phase_allowed}\`

## Open Gaps

${(data.open_gaps || []).map((gap) => `- \`${gap}\``).join("\n") || "- None"}

## Wait Policy

- Check only at five-minute marks: \`${data.safe_wait_policy.check_only_at_five_minute_marks}\`
- Do safe-now work between marks: \`${data.safe_wait_policy.do_safe_now_work_between_marks}\`
- Continuous safe-now approval/eureka/cleanup work: \`${data.safe_wait_policy.continuous_safe_now_approval_packet_eureka_and_cleanup_work}\`
- Cadence marks are check opportunities, not forced stops: \`${data.safe_wait_policy.cadence_marks_are_check_opportunities_not_forced_stops}\`
- Harvest at next natural safe pause after cadence mark: \`${data.safe_wait_policy.harvest_at_next_natural_safe_pause_after_cadence_mark}\`
- Watcher start is completion proof: \`${data.safe_wait_policy.watcher_start_is_completion_proof}\`
`;
}

function renderPhaseStatusMd(data) {
  return `# v552 v8 x1 Phase Status Index

Status: \`${data.overall_status}\`

Current active phase: \`${data.current_active_phase_after_receipt}\`
Latest closed phase: \`${data.latest_closed_phase_after_receipt}\`
Latest completed x1: \`${data.latest_completed_x1_after_receipt}\`
Latest completed x2: \`${data.latest_completed_x2_after_receipt}\`
Next x2 scope: \`${data.next_x2_scope}\`
Next x2 ready: \`${data.next_x2_ready}\`

## Lane Gate Status

- Aster Vale: \`${data.lane_gate_status.aster_vale}\`
- Kierkegaard/Aristotle: \`${data.lane_gate_status.kierkegaard_aristotle}\`
- Mandatory orchestrator: \`${data.lane_gate_status.mandatory_orchestrator}\`
- Recovered app-lane runner: \`${data.lane_gate_status.recovered_app_lane_runner}\`
- Recovered app-lane preflight: \`${data.lane_gate_status.recovered_app_preflight}\`
- Private map preflight: \`${data.lane_gate_status.private_map_preflight}\`
- Five-minute cadence guard: \`${data.lane_gate_status.five_minute_cadence_guard}\`
- Recovered five-minute cadence guard: \`${data.lane_gate_status.recovered_five_minute_cadence_guard}\`
- Updater runner: \`${data.lane_gate_status.updater_runner}\`
- Compact-pause updater: \`${data.lane_gate_status.compact_pause_updater}\`

## Counts

- Safe approval packets: \`${data.counts.safe_approval_packets}\`
- Candidate approval packets: \`${data.counts.candidate_approval_packets}\`
- Exact approval packets: \`${data.counts.exact_approval_packets}\`
- Skill ideas: \`${data.counts.skill_ideas}\`
- Runner ideas: \`${data.counts.runner_ideas}\`
- Cleanup tasks: \`${data.counts.cleanup_tasks}\`

## Artifacts

${data.artifacts.map((item) => `- \`${item}\``).join("\n")}
`;
}

function renderCloseoutMd(data) {
  return `# v552 v8 x1 Closeout\n\nStatus: \`${data.overall_status}\`\n\nThis earlier closeout is superseded because the mandatory background app-lane completion gate remains open.\n\nCurrent active phase: \`${data.current_active_phase_after_receipt}\`\nLatest closed phase: \`${data.latest_closed_phase_after_receipt}\`\nNext x2 ready: \`${data.next_x2_ready}\`\n\n## Open Gate\n\nReason: ${data.open_gate.reason}\nGate status: \`${data.open_gate.gate_status}\`\n\n${(data.open_gate.open_gaps || []).map((gap) => `- \`${gap}\``).join("\n")}\n`;
}

function renderStartupSnapshotMd(data) {
  return `# v552 v8 x1 Compact Pause Startup Snapshot\n\nStatus: \`${data.overall_status}\`\n\n## Startup Order\n\n${data.startup_order.map((item, index) => `${index + 1}. ${item}`).join("\n")}\n\n## Pointer\n\n- Status: \`${data.current_pointer_after_receipt.status}\`\n- Current active phase: \`${data.current_pointer_after_receipt.current_active_phase}\`\n- Latest closed phase: \`${data.current_pointer_after_receipt.latest_closed_phase}\`\n- Next x2 ready: \`${data.current_pointer_after_receipt.next_x2_ready}\`\n`;
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${current.current_active_lanes.join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v8 x1 Mandatory Background Route

- Main orchestrator runner: \`${current.v8_x1_background_runner_correction.main_orchestrator_runner_entrypoint}\`
- Compatibility entrypoint: \`${current.v8_x1_background_runner_correction.compatibility_entrypoint}\`
- Aster Vale strict CLI status: \`${current.v8_x1_background_runner_correction.aster_vale_strict_cli_status}\`
- Kierkegaard/Aristotle app gate status: \`${current.v8_x1_background_runner_correction.kierkegaard_aristotle_app_gate_status}\`
- Mandatory orchestrator status: \`${current.v8_x1_background_runner_correction.mandatory_orchestrator_status}\`
- Recovered app-lane runner status: \`${current.v8_x1_background_runner_correction.recovered_app_lane_runner_status}\`
- Recovered app-lane preflight status: \`${current.v8_x1_background_runner_correction.recovered_app_lane_preflight_status}\`
- Recovered app-lane completion gate status: \`${current.v8_x1_background_runner_correction.recovered_app_lane_completion_gate_status}\`
- Private app-lane map preflight status: \`${current.v8_x1_background_runner_correction.private_app_lane_map_preflight_status}\`
- Five-minute cadence guard status: \`${current.v8_x1_background_runner_correction.five_minute_cadence_guard_status}\`
- Recovered five-minute cadence guard status: \`${current.v8_x1_background_runner_correction.recovered_five_minute_cadence_guard_status}\`
- Updater runner status: \`${current.v8_x1_background_runner_correction.updater_runner_status}\`
- Compact-pause updater status: \`${current.v8_x1_background_runner_correction.compact_pause_updater_status}\`
- Background notifier/orchestrator route mandatory: \`${current.v8_x1_background_runner_correction.background_notifier_orchestrator_route_mandatory}\`
- Recovered app-lane map runner mandatory: \`${current.v8_x1_background_runner_correction.recovered_app_lane_map_runner_mandatory}\`
- Updater runners mandatory: \`${current.v8_x1_background_runner_correction.updater_runners_mandatory}\`
- Five-minute checks mandatory: \`${current.v8_x1_background_runner_correction.five_minute_checks_mandatory}\`
- Full-tools support worktree mandatory: \`${current.v8_x1_background_runner_correction.full_tools_support_worktree_mandatory}\`
- Watcher start is completion proof: \`${current.v8_x1_background_runner_correction.watcher_start_is_completion_proof}\`
- Phase closed: \`${current.v8_x1_background_runner_correction.phase_closed}\`
- Next x2 ready: \`${current.v8_x1_background_runner_correction.next_x2_ready}\`

## Lookup Rule

${current.archive_fallback_rule}

## Current Lookup Files

${current.current_lookup_files.map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${current.latest_action_summary.map((item) => `- ${item}`).join("\n")}

## Safety Boundary

- Status-only receipts, no private route data, no private lane body content, no credentials, no private machine paths.
- GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, and deployment closure remain open.
`;
}

function renderLatestBeaconMd(latest) {
  return `# Omega-Mini Latest Updates Beacon\n\nStatus: ${latest.status}\nPrimary branch: ${latest.primary_branch}\nArchive branch: ${latest.archive_branch}\nCurrent active phase: ${latest.current_active_phase}\nLatest closed phase: ${latest.latest_closed_phase}\nLatest completed x1: ${latest.latest_completed_x1_phase}\nLatest completed x2: ${latest.latest_completed_x2_phase}\nCurrent lanes: ${latest.current_active_lanes.join("; ")}\nNext x2 scope: ${latest.next_x2_scope}\nNext x1 lane after x2: ${latest.next_x1_lane_after_x2}\n\n## Latest Lookup Files\n\n${latest.latest_lookup_files.map((item) => `- ${item}`).join("\n")}\n\n## Safety Boundary\n\n- Use status-only evidence and exact relative repo paths.\n- Do not publish private route data, private lane body content, credentials, screen-capture files, or private machine paths.\n`;
}

function renderGhcBeaconMd(ghc) {
  return `# GHC Current State Beacon\n\nStatus: ${ghc.status}\nCurrent active phase: ${ghc.current_active_phase}\nLatest closed phase: ${ghc.latest_closed_phase}\nLatest completed x1: ${ghc.latest_completed_x1_phase}\nLatest completed x2: ${ghc.latest_completed_x2_phase}\nNext x2 scope: ${ghc.next_x2_scope}\nNext x1 lane after x2: ${ghc.next_x1_lane_after_x2}\n\n## Lookup Files\n\n${ghc.lookup_files.map((item) => `- ${item}`).join("\n")}\n\n## Boundary\n\nStatus-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.\n`;
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
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
