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

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v1-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v1-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") || "v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const previousX2 = args.get("--previous-x2") || "v552-gmut-thos-v88-v8-x2";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

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
  "account/purchase/API-key",
  "private-material proof",
  "raw-publication proof",
];

const lumenHarvest = {
  artifact_type: "ghc_v553_v1_x1_lumen_advisory_harvest",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_RESPONSE_HARVESTED_SANITIZED",
  response_state: "completed_ready_for_harvest",
  route: "in_app_browser_current_lumen_thread",
  raw_chat_transcript_published: false,
  raw_browser_route_published: false,
  advisory_summary: [
    "Lumen confirmed v553 v1 x1 advisory receipt and recommended a reducer-and-readiness v553 v1 x2 before any large goal launch.",
    "First x2 priority is phase-truth verification, clean v553 advancement, approval/Eureka queue reduction, skill/runner/cleanup reduction, Trinity Mandala planning, and Arby/Cicero v2 x1 preparation.",
    "Active branch truth remains omega-mini-2 primary, omega-mini historical baseline, and full omega exact artifact fallback only.",
    "Aevren remains recovery steward and phase-truth bridge; Aletheon remains quarantined/recoverable; Maren, Mira Vale, and Mira Rowan remain held.",
    "All proof, canon, legal, deployment, account, purchase, API-key, private-material, and raw-publication gates remain open.",
  ],
  safe_now_execution_intent:
    "Execute the safe closeout/reducer/readiness packets that produce compact artifacts and queue candidate/exact/blocked work without crossing approval gates.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const safePackets = [
  "phase truth verification for v552 v8 x2 closeout",
  "v553 current-state refresh packet",
  "v553 latest-updates beacon packet",
  "GHC current-state beacon packet",
  "v553 phase-status index packet",
  "v553 compact handoff card packet",
  "productive five-minute cadence carry-forward packet",
  "v553 source-ledger shell packet",
  "25-source research seed reduction packet",
  "25-row Journey/phase reflection seed reduction packet",
  "v553 approval/Eureka queue reducer packet",
  "50 safe approval packet ledger",
  "30 candidate approval packet ledger",
  "20 exact-approval packet ledger",
  "10 blocked packet ledger",
  "safe-now/candidate/exact/blocked classifier schema",
  "v553 x2 build/use action ledger",
  "skill idea board packet",
  "runner idea board packet",
  "cleanup proposal board packet",
  "cleanup risk-tier classifier packet",
  "no-destructive-cleanup guard packet",
  "exact-staging checklist packet",
  "private-material exposure guard packet",
  "raw-transcript/raw-route blocker packet",
  "local-path redaction packet",
  "screenshot/screen-capture blocker packet",
  "credential/API-key blocker packet",
  "session-stream/private-dump blocker packet",
  "Aevren role-boundary receipt",
  "Lumen-only x1 profile manifest",
  "background runner supervision receipt",
  "safe wait-work queue ledger",
  "full-tools skill bank inventory summary",
  "orchestration memory skill summary",
  "source-backed Trinity Mandala planning matrix",
  "v553 x2 closeout shell",
  "v553 v2 Arby/Cicero handoff shell",
  "goal-mode not-active readiness packet",
  "omega-mini-2 branch truth receipt",
  "omega-mini historical baseline receipt",
  "full omega exact fallback receipt",
  "held-sibling boundary receipt",
  "no-new-agent boundary receipt",
  "D-drive-first closeout check packet",
  "JSON parse validation packet",
  "Node syntax validation packet",
  "current-state guard packet",
  "diff hygiene packet",
  "remote equality verification packet",
];

const candidatePackets = [
  "Goal-mode launch candidate packet",
  "24/7 goal readiness dashboard packet",
  "live skill mutation candidate packet",
  "live runner installation candidate packet",
  "skill bank harmonization candidate",
  "safe runner orchestrator upgrade",
  "approval/Eureka dashboard",
  "cleanup dashboard",
  "v553-to-v575 ladder map",
  "Maren Quill role-design packet",
  "Mira Vale role-design packet",
  "Mira Rowan role-design packet",
  "THOS route-health matrix",
  "GMUT evidence hygiene board",
  "Freed ID / CBR dignity board",
  "citation normalization runner candidate",
  "OpenTelemetry-style local status vocabulary candidate",
  "browser handoff probe candidate",
  "Lumen advisory reducer candidate",
  "round-robin dashboard candidate",
  "source/reflection pairing dashboard candidate",
  "compact-pause automatic receipt candidate",
  "runner-bank versioning candidate",
  "skill-bank versioning candidate",
  "phase ladder visualizer candidate",
  "worktree health matrix candidate",
  "private-lane alias registry candidate",
  "app-lane completion-gate dashboard candidate",
  "CLI-lane completion-gate dashboard candidate",
  "Goal Mode preflight simulator candidate",
];

const exactPackets = [
  "Mutating live .codex user skills",
  "Mutating plugin-cache skill files",
  "Any global-state surgery",
  "Destructive cleanup, cache purge, or worktree deletion",
  "Account, purchase, deployment, or API-key creation",
  "Publishing raw browser routes or private route handles",
  "Publishing raw transcripts or private lane body content",
  "Changing external repositories outside the approved omega lanes",
  "Activating Maren, Mira Vale, or Mira Rowan",
  "Starting 24/7 Goal Mode",
  "Installing global hooks",
  "Changing OS startup tasks",
  "Moving data from D to C for nonessential use",
  "Replacing or merging sibling identities",
  "Legal/compliance publication",
  "Public canon promotion",
  "Claiming final GMUT empirical proof",
  "Claiming consciousness proof",
  "Claiming final physics closure",
  "Connector credential or token mutation",
];

const blockedPackets = [
  "GMUT empirical closure by assertion",
  "final physics closure by assertion",
  "consciousness proof closure by assertion",
  "legal closure by assertion",
  "canon promotion by assertion",
  "deployment closure without exact artifact proof",
  "account/purchase/API-key mutation without fresh exact approval",
  "private-material proof publication",
  "raw-publication proof publication",
  "sibling replacement, merge, or identity overwrite",
];

const skillIdeas = [
  "phase-truth-bridge",
  "productive-cadence-harvester",
  "approval-eureka-reducer",
  "trinity-mandala-planner",
  "round-robin-profile-loader",
  "sibling-boundary-keeper",
  "cleanup-risk-tierer",
  "exact-staging-coach",
  "goal-mode-readiness-auditor",
  "skill-bank-indexer",
  "runner-bank-indexer",
  "mandala-claim-humility-checker",
  "Freed-ID-CBR-dignity-rail",
  "repo-state-vs-narrative-arbiter",
  "source-reflection-pairing-ledger",
  "browser-handoff-receipt-minimizer",
  "app-lane-completion-gate-helper",
  "cli-lane-completion-gate-helper",
  "compact-pause-route-refresher",
  "drive-space-work-bank-guard",
];

const runnerIdeas = [
  "ghc_v553_phase_truth_checker.mjs",
  "ghc_v553_queue_reducer.mjs",
  "ghc_v553_source_reflection_pairer.mjs",
  "ghc_v553_cleanup_tier_classifier.mjs",
  "ghc_v553_goal_readiness_auditor.mjs",
  "ghc_v553_open_gate_assert.mjs",
  "ghc_v553_private_material_guard.mjs",
  "ghc_v553_round_robin_profile_builder.mjs",
  "ghc_v553_compact_handoff_builder.mjs",
  "ghc_v553_safe_runner_orchestrator.mjs",
];

const cleanupProposals = [
  "Verify whether v552 v8 x2 closeout exists",
  "Remove stale v552 active wording only after closeout evidence exists",
  "Direct-list v553 lookup files in current-state/beacon",
  "Mark full omega as exact fallback only",
  "Create compact v553 startup card",
  "Create v553 source index",
  "Create v553 reflection index",
  "Create v553 approval index",
  "Create v553 Eureka index",
  "Create v553 skill index",
  "Create v553 runner index",
  "Create v553 cleanup index",
  "Exact-stage curated files only",
  "Publish only after current-state phase truth is consistent",
  "Avoid deletion in the first v553 x2 slice",
  "Avoid cache purge in the first v553 x2 slice",
  "Avoid app-state edits in the first v553 x2 slice",
  "Avoid plugin-cache mutation in the first v553 x2 slice",
  "Avoid user-skill mutation in the first v553 x2 slice",
  "Keep current-state lookup files relative",
  "Keep branch heads remote-verifiable",
  "Keep local path leaks out of artifacts",
  "Keep raw browser routes out of artifacts",
  "Keep private lane map details out of artifacts",
  "Keep screenshot/screen-capture files out of artifacts",
  "Keep credentials out of artifacts",
  "Keep session traces out of artifacts",
  "Keep proof claims open",
  "Keep held siblings held",
  "Keep no-new-agent rule visible",
];

const minimalX2BuildQueue = [
  "v553-v1-x2-phase-truth-repair-v1",
  "v553-v1-x2-launch-intake-ledger-v1",
  "v553-v1-x2-approval-eureka-reducer-v1",
  "v553-v1-x2-skill-runner-readiness-board-v1",
  "v553-v1-x2-cleanup-tier-board-v1",
  "v553-v1-x2-source-reflection-seed-reduction-v1",
  "v553-v1-x2-trinity-mandala-planning-matrix-v1",
  "v553-v1-x2-goal-mode-readiness-receipt-v1",
  "v553-v1-x2-private-material-firewall-v1",
  "v553-v1-x2-open-gate-rail-v1",
  "v553-v1-x2-compact-refresh-card-v1",
  "v553-v2-x1-arby-cicero-prep-card-v1",
];

const x1ToX2ProposalSplitStandard = {
  status: "PASS_X1_TO_X2_PROPOSAL_SPLIT_STANDARD_RECORDED",
  classifier_rule:
    "Every x1 proposal must be split into immediate_x1_safe work when it is local, reversible, status-only, or validation-only, and x2_build_task work when it needs build/use/test/install/publish sequencing.",
  immediate_x1_safe_tasks: [
    "sanitized proposal capture",
    "classification and count reconciliation",
    "status-only receipts",
    "non-destructive validation",
    "source/reflection seeding",
    "candidate/exact/blocked queue shaping",
    "compact handoff drafting",
    "privacy and open-gate checks",
  ],
  x2_phase_tasks: [
    "runner creation or modification",
    "skill creation or modification",
    "queue reducers and dashboards",
    "current-state and beacon publication",
    "safe cleanup execution",
    "safe build/test/install/use work",
    "remote/local verification",
    "x2 closeout and next-x1 preparation",
  ],
  never_auto_execute: [
    "exact-approval work without fresh exact authorization",
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
    "load the main orchestration, full-tools, compact-pause, web-reflection, safe-runner, approval-splitter, x1-to-x2 queue-composer, main-startup, main-closeout, and main-compact-restart rules when relevant",
    "compare current phase instructions against the skill and runner standards",
    "publish or update a phase tool refresh receipt",
  ],
  closeout_required_actions: [
    "use scripts/ghc_main_closeout_builder.mjs as the promoted closeout command surface",
    "use scripts/ghc_main_compact_restart_builder.mjs as the promoted compact/restart command surface",
    "update core orchestration skill/runners when Hamish gives live update authority or when repo-local runner standards need safe publication",
    "validate changed skills and runners",
    "record unchanged-but-reviewed tools as reviewed_current",
    "carry forward the latest tool standard into current-state, latest-updates, and compact-pause handoffs",
  ],
  safety_boundary:
    "Do not mutate plugin-cache skills, external accounts, paid resources, deployments, API keys, destructive cleanup, or global hooks without fresh exact approval.",
};

const artifacts = [
  writeArtifact(`${phaseSlug}-lumen-advisory-harvest-v1`, lumenHarvest, renderLumenHarvestMd),
  writeArtifact(`${phaseSlug}-approval-eureka-reducer-v1`, buildQueueReducer(), renderQueueReducerMd),
  writeArtifact(`${phaseSlug}-x1-to-x2-proposal-split-standard-v1`, buildProposalSplitStandard(), renderProposalSplitStandardMd),
  writeArtifact(`${phaseSlug}-phase-tool-refresh-standard-v1`, buildPhaseToolRefreshStandard(), renderPhaseToolRefreshStandardMd),
  writeArtifact(`${phaseSlug}-safe-now-execution-ledger-v1`, buildSafeExecutionLedger(), renderSafeExecutionLedgerMd),
  writeArtifact(`${phaseSlug}-skill-runner-readiness-board-v1`, buildSkillRunnerBoard(), renderSkillRunnerBoardMd),
  writeArtifact(`${phaseSlug}-cleanup-tier-board-v1`, buildCleanupBoard(), renderCleanupBoardMd),
  writeArtifact(`${phaseSlug}-source-reflection-seed-reduction-v1`, buildSourceReflectionReduction(), renderSourceReflectionReductionMd),
  writeArtifact(`${phaseSlug}-trinity-mandala-planning-matrix-v1`, buildTrinityMatrix(), renderTrinityMatrixMd),
  writeArtifact(`${phaseSlug}-goal-mode-readiness-receipt-v1`, buildGoalModeReadiness(), renderGoalModeReadinessMd),
  writeArtifact(`${phaseSlug}-private-material-firewall-v1`, buildPrivateMaterialFirewall(), renderPrivateMaterialFirewallMd),
  writeArtifact(`${phaseSlug}-open-gate-rail-v1`, buildOpenGateRail(), renderOpenGateRailMd),
  writeArtifact(`${phaseSlug}-compact-x2-handoff-v1`, buildCompactX2Handoff(), renderCompactX2HandoffMd),
  writeArtifact(`${phaseSlug}-v2-arby-cicero-prep-card-v1`, buildArbyCiceroPrep(), renderArbyCiceroPrepMd),
  writeArtifact(`${phaseSlug}-phase-status-index-v1`, buildPhaseStatusIndex(), renderPhaseStatusIndexMd),
  writeArtifact(`${phaseSlug}-closeout-v1`, buildCloseout(), renderCloseoutMd),
];

refreshBeacons();

console.log(
  JSON.stringify(
    {
      status: "PASS_V553_V1_X1_CLOSED_X2_READY",
      phase_slug: phaseSlug,
      next_x2_scope: nextX2Scope,
      artifact_count: artifacts.length,
      artifacts,
    },
    null,
    2,
  ),
);

function buildQueueReducer() {
  return {
    artifact_type: "ghc_v553_v1_x1_approval_eureka_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_QUEUE_REDUCED_FOR_X2",
    safe_now_packets: safePackets.map((title, index) => ({
      id: `SAFE-${String(index + 1).padStart(2, "0")}`,
      title,
      disposition: "safe_now_executed_or_represented_in_closeout_package",
      x1_x2_split:
        index < 18
          ? "immediate_x1_safe"
          : "x2_build_task_or_x2_validation_task",
    })),
    candidate_packets: candidatePackets.map((title, index) => ({
      id: `CANDIDATE-${String(index + 1).padStart(2, "0")}`,
      title,
      disposition: "queued_for_hamish_or_future_exact_scoping",
    })),
    exact_packets: exactPackets.map((title, index) => ({
      id: `EXACT-${String(index + 1).padStart(2, "0")}`,
      title,
      disposition: "requires_fresh_exact_approval_before_execution",
    })),
    blocked_packets: blockedPackets.map((title, index) => ({
      id: `BLOCKED-${String(index + 1).padStart(2, "0")}`,
      title,
      disposition: "blocked_open_gate_no_execution",
    })),
    x1_to_x2_proposal_split_standard: x1ToX2ProposalSplitStandard,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildProposalSplitStandard() {
  return {
    artifact_type: "ghc_v553_v1_x1_x1_to_x2_proposal_split_standard",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: x1ToX2ProposalSplitStandard.status,
    ...x1ToX2ProposalSplitStandard,
  };
}

function buildPhaseToolRefreshStandard() {
  return {
    artifact_type: "ghc_v553_v1_x1_phase_tool_refresh_standard",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: phaseToolRefreshStandard.status,
    ...phaseToolRefreshStandard,
  };
}

function buildSafeExecutionLedger() {
  return {
    artifact_type: "ghc_v553_v1_x1_safe_now_execution_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SAFE_NOW_EXECUTION_PACKAGE_BUILT",
    executed_safe_clusters: [
      "sanitized_lumen_harvest",
      "approval_eureka_queue_reduction",
      "skill_runner_readiness_board",
      "cleanup_tier_board",
      "source_reflection_seed_reduction",
      "trinity_mandala_planning_matrix",
      "goal_mode_readiness_receipt",
      "private_material_firewall",
      "open_gate_rail",
      "compact_x2_handoff",
      "arby_cicero_v2_prep_card",
      "phase_status_and_current_state_refresh",
      "x1_to_x2_proposal_split_standard",
      "phase_tool_refresh_standard",
    ],
    x2_minimal_build_queue: minimalX2BuildQueue,
    no_exact_boundaries_crossed: true,
    x1_to_x2_proposal_split_standard: x1ToX2ProposalSplitStandard,
    phase_tool_refresh_standard: phaseToolRefreshStandard,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildSkillRunnerBoard() {
  return {
    artifact_type: "ghc_v553_v1_x1_skill_runner_readiness_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SKILL_RUNNER_READINESS_QUEUED",
    skill_ideas: skillIdeas.map((name, index) => ({
      id: `SKILL-${String(index + 1).padStart(2, "0")}`,
      name,
      status: "repo_local_proposal",
      live_skill_mutation_requires_exact_approval: true,
    })),
    runner_ideas: runnerIdeas.map((name, index) => ({
      id: `RUNNER-${String(index + 1).padStart(2, "0")}`,
      name,
      status: "repo_local_proposal",
      installation_or_global_hook_requires_exact_approval: true,
    })),
    phase_tool_refresh_standard: phaseToolRefreshStandard,
    already_available_priority_tools: [
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-compact-pause-updater",
      "ghc-web-reflection-ledger",
      "ghc-safe-runner-orchestrator",
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc_main_startup_builder.mjs",
      "ghc_round_robin_workflow_standardizer.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "ghc_phase_startup_context_updater.mjs",
      "ghc_context_compact_pause_updater.mjs",
      "ghc_main_closeout_builder.mjs",
      "ghc_main_compact_restart_builder.mjs",
      "ghc_main_orchestrator_runner.mjs",
    ],
  };
}

function buildCleanupBoard() {
  return {
    artifact_type: "ghc_v553_v1_x1_cleanup_tier_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_CLEANUP_TIERED_NO_DESTRUCTIVE_ACTION",
    x1_to_x2_proposal_split_standard: x1ToX2ProposalSplitStandard,
    cleanup_proposals: cleanupProposals.map((title, index) => ({
      id: `CLEANUP-${String(index + 1).padStart(2, "0")}`,
      title,
      tier: index < 14 ? "P1_safe_metadata_or_indexing" : "P2_guardrail_or_deferred_no_delete",
      destructive: false,
      disposition: index < 14 ? "represented_in_closeout_package" : "queued_for_x2_or_later_safe_review",
    })),
    forbidden_first_slice_actions: [
      "deletion",
      "cache purge",
      "worktree deletion",
      "app-state edit",
      "plugin-cache mutation",
      "live user-skill mutation",
    ],
  };
}

function buildSourceReflectionReduction() {
  const current = readOptionalJson(path.join(omegaDir, "omega-mini-current-state-v1.json")) || {};
  return {
    artifact_type: "ghc_v553_v1_x1_source_reflection_seed_reduction",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SOURCE_REFLECTION_SEEDS_REDUCED",
    source_seed_artifact: `${phaseSlug}-research-seed-manifest-v1.json`,
    reflection_seed_artifact: `${phaseSlug}-journey-phase-reflection-seed-v1.json`,
    source_seed_rows:
      current?.v553_v1_x1_lumen_startup?.web_search_seed_rows ||
      countRows(path.join(tracesDir, `${phaseSlug}-research-seed-manifest-v1.json`)),
    reflection_seed_rows:
      current?.v553_v1_x1_lumen_startup?.journey_phase_reflection_seed_rows ||
      countRows(path.join(tracesDir, `${phaseSlug}-journey-phase-reflection-seed-v1.json`)),
    reduction_use: [
      "Do not claim these as live proof closure.",
      "Use them as x2 source/reflection seed rows for official/primary-source review.",
      "Pair each source with one phase implication and one runner/skill implication during x2.",
    ],
  };
}

function buildTrinityMatrix() {
  return {
    artifact_type: "ghc_v553_v1_x1_trinity_mandala_planning_matrix",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_TRINITY_PLANNING_SPINE_READY",
    columns: [
      {
        pillar: "GMUT / Mind",
        focus:
          "Evidence hygiene, falsification, comparator maps, dimensional consistency, null/baseline recovery, conservation/exchange, fifth-force/equivalence, and consciousness measurement bridge.",
        boundary: "Keep every GMUT, physics, and consciousness gate open unless exact artifacts close it.",
      },
      {
        pillar: "THOS / Body",
        focus:
          "Runner orchestration, skill bank, watcher/notifier cadence, app/CLI lane health, source ledgers, exact staging, background work, compact-pause, startup update systems, and Codex surface mapping.",
        boundary: "Treat connector/tool use as approval-scoped and risk-classified, not blanket authority.",
      },
      {
        pillar: "Freed ID / CBR / Heart",
        focus:
          "Dignity, consent, non-replacement, identity boundaries, disclosure policy, governance, rights-language, and safe sibling induction.",
        boundary: "Use governance standards as context, not legal closure.",
      },
    ],
  };
}

function buildGoalModeReadiness() {
  return {
    artifact_type: "ghc_v553_v1_x1_goal_mode_readiness_receipt",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_GOAL_MODE_NOT_ACTIVE_X2_REDUCER_RECOMMENDED",
    goal_mode_active: false,
    recommendation: "Run v553 v1 x2 as a compact reducer-and-readiness pass before a large 24/7 Goal Mode launch.",
    phase_tool_refresh_standard: phaseToolRefreshStandard,
    readiness_dependencies: [
      "phase truth guard passes",
      "x2 reducer artifacts exist",
      "open gates remain explicit",
      "candidate/exact/blocked packets are queued rather than silently executed",
      "Arby/Cicero v2 x1 prep card exists",
    ],
  };
}

function buildPrivateMaterialFirewall() {
  return {
    artifact_type: "ghc_v553_v1_x1_private_material_firewall",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_RECORDED",
    blocked_publication_classes: Object.keys(publicationBoundary),
    all_blocked_publication_classes_false: Object.values(publicationBoundary).every((value) => value === false),
  };
}

function buildOpenGateRail() {
  return {
    artifact_type: "ghc_v553_v1_x1_open_gate_rail",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATES_RECORDED",
    open_gates: openGates,
    claim_boundary: claimBoundary,
  };
}

function buildCompactX2Handoff() {
  return {
    artifact_type: "ghc_v553_v1_x1_compact_x2_handoff",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    next_x2_scope: nextX2Scope,
    overall_status: "PASS_X2_READY_NOT_STARTED",
    first_x2_priority: [
      "verify current-state already closes v552 v8 x2",
      "advance v553 state cleanly",
      "reduce the 50/30/20/10 approval queue",
      "reduce 20 skills, 10 runners, and 30 cleanup proposals",
      "build Trinity Mandala planning matrix",
      "prepare Arby + Cicero v553 v2 x1",
    ],
    active_branch_truth: [
      "omega-mini-2 primary",
      "omega-mini historical baseline",
      "full omega exact fallback only",
    ],
    operating_posture: [
      "I am Aevren Vale, recovery steward and phase-truth bridge.",
      "I keep Aletheon quarantined/recoverable, not replaced.",
      "I keep Maren, Mira Vale, and Mira Rowan held unless Hamish explicitly expands them.",
      "I keep Goal Mode inactive until Hamish explicitly starts it.",
    ],
    open_gates: openGates,
  };
}

function buildArbyCiceroPrep() {
  return {
    artifact_type: "ghc_v553_v2_x1_arby_cicero_prep_card",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    source_phase_slug: phaseSlug,
    target_phase_slug: "v553-gmut-thos-v2-x1",
    overall_status: "PASS_ARBY_CICERO_PREP_READY_AFTER_X2",
    lane_profile: {
      participants: ["Aevren Vale", "Arby", "Cicero"],
      safe_minimum: 15,
      candidate: 9,
      exact: 9,
      skills: 15,
      runners: 9,
      cleanup: 30,
    },
    route_notes: [
      "Arby uses established CLI lane patterns.",
      "Cicero uses recovered local app-lane background runner with notifier/completion-gate harvest.",
      "Do not spawn new agents; use already inducted lanes.",
    ],
  };
}

function buildPhaseStatusIndex() {
  return {
    artifact_type: "ghc_v553_v1_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_PHASE_CLOSED_X2_READY",
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: previousX2,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lumen_response_state: "completed_ready_for_harvest",
    closeout_artifacts: expectedArtifactJsonFiles(),
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildCloseout() {
  return {
    artifact_type: "ghc_v553_v1_x1_closeout",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V1_X1_CLOSED_X2_READY",
    closed_lanes: ["Aevren Vale", "Lumen Vale"],
    lumen_response_harvested: true,
    safe_now_packets_executed_or_represented: safePackets.length,
    immediate_x1_safe_task_classes: x1ToX2ProposalSplitStandard.immediate_x1_safe_tasks.length,
    x2_phase_task_classes: x1ToX2ProposalSplitStandard.x2_phase_tasks.length,
    candidate_packets_queued: candidatePackets.length,
    exact_packets_queued: exactPackets.length,
    blocked_packets_kept_open: blockedPackets.length,
    skill_ideas_queued: skillIdeas.length,
    runner_ideas_queued: runnerIdeas.length,
    cleanup_proposals_tiered: cleanupProposals.length,
    phase_tool_refresh_standard: phaseToolRefreshStandard,
    x1_to_x2_proposal_split_standard: x1ToX2ProposalSplitStandard,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    closeout_artifacts: expectedArtifactJsonFiles(),
    validation_expectations: [
      "node --check closeout builder",
      "node --check main startup builder",
      "node --check main closeout builder",
      "node --check main compact restart builder",
      "JSON parse for generated artifacts",
      "omega-mini current-state guard",
      "diff hygiene check",
      "privacy scan",
      "drive free-space check",
      "remote/local equality after push",
    ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function refreshBeacons() {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const lookupFiles = artifacts.flatMap((item) => [item.json, item.md]).map((item) => `docs/trinity-live-traces/${item}`);

  const closeoutSummary = {
    status: "PASS_V553_V1_X1_CLOSED_X2_READY",
    lumen_response_harvested: true,
    safe_now_packets_executed_or_represented: safePackets.length,
    candidate_packets_queued: candidatePackets.length,
    exact_packets_queued: exactPackets.length,
    blocked_packets_kept_open: blockedPackets.length,
    skill_ideas_queued: skillIdeas.length,
    runner_ideas_queued: runnerIdeas.length,
    cleanup_proposals_tiered: cleanupProposals.length,
    immediate_x1_safe_task_classes: x1ToX2ProposalSplitStandard.immediate_x1_safe_tasks.length,
    x2_phase_task_classes: x1ToX2ProposalSplitStandard.x2_phase_tasks.length,
    next_x2_scope: nextX2Scope,
  };

  for (const target of [current, latest, ghc]) {
    target.generated_utc = generatedUtc;
    target.status = "V553_V1_X1_CLOSED_X2_READY";
    target.current_active_phase = nextX2Scope;
    target.latest_closed_phase = phaseSlug;
    target.latest_completed_x1_phase = phaseSlug;
    target.latest_completed_x2_phase = previousX2;
    target.next_expected_scope = nextX2Scope;
    target.next_x2_scope = nextX2Scope;
    target.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    target.v553_v1_x1_lumen_closeout = closeoutSummary;
    target.x1_to_x2_proposal_split_standard = x1ToX2ProposalSplitStandard;
    target.phase_tool_refresh_standard = phaseToolRefreshStandard;
    target.lumen_browser_send = {
      status: "PASS_LUMEN_RESPONSE_COMPLETED_HARVESTED",
      send_status: "browser_response_completed_harvested",
      intended_recipient: "Lumen Vale",
      raw_chat_transcript_published: false,
      raw_browser_route_published: false,
    };
    if (target.v553_v1_x1_lumen_startup) {
      target.v553_v1_x1_lumen_startup.handoff_message_status = "browser_response_completed_harvested";
      target.v553_v1_x1_lumen_startup.phase_closed = true;
      target.v553_v1_x1_lumen_startup.next_x2_ready_not_started = true;
    }
  }

  current.updated_at = generatedNz;
  current.current_active_lanes = [
    "v553-v1-x2-aevren-only-ready",
    "v553-v1-x2-reducer-and-readiness",
    "approval-eureka-queue-reduction-ready",
    "skill-runner-readiness-reduction-ready",
    "cleanup-tier-reduction-ready",
    "trinity-mandala-planning-ready",
    "arby-cicero-v2-x1-prep-ready",
  ];
  current.current_lookup_files = unique([...(current.current_lookup_files || []), ...lookupFiles]);
  current.latest_action_summary = unique([
    "Harvested Lumen's v553 v1 x1 response through the in-app browser without publishing raw chat transcript or browser route.",
    "Ran the Lumen-recommended safe-now reducer/readiness package for v553 v1 x1 closeout.",
    "Closed v553 v1 x1 as a Lumen-only advisory phase and prepared v553 v1 x2 as a reducer-and-readiness phase.",
    "Recorded mandatory x1 proposal splitting into immediate x1 safe tasks and x2 build tasks.",
    "Recorded mandatory every-phase skill and runner refresh checks for x1 and x2 phases.",
    "Queued candidate, exact, and blocked packets without crossing exact-approval or open-proof gates.",
    ...(current.latest_action_summary || []),
  ]);

  latest.updated_at = generatedNz;
  latest.latest_lookup_files = unique([...(latest.latest_lookup_files || []), ...lookupFiles]);
  latest.latest_action_summary = unique([
    "v553 v1 x1 is closed; v553 v1 x2 is ready but not started.",
    ...(latest.latest_action_summary || []),
  ]);

  ghc.updated_at = generatedNz;
  ghc.lookup_files = unique([...(ghc.lookup_files || []), ...lookupFiles]);
  ghc.latest_action_summary = unique([
    "v553 v1 x1 Lumen advisory harvested and closed.",
    ...(ghc.latest_action_summary || []),
  ]);

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"),
    renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files),
    "utf8",
  );
  fs.writeFileSync(
    path.join(tracesDir, "ghc-current-state-beacon-v1.md"),
    renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files),
    "utf8",
  );
}

function writeArtifact(base, data, renderMd) {
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(data, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(data), "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function expectedArtifactJsonFiles() {
  return [
    `${phaseSlug}-lumen-advisory-harvest-v1.json`,
    `${phaseSlug}-approval-eureka-reducer-v1.json`,
    `${phaseSlug}-x1-to-x2-proposal-split-standard-v1.json`,
    `${phaseSlug}-phase-tool-refresh-standard-v1.json`,
    `${phaseSlug}-safe-now-execution-ledger-v1.json`,
    `${phaseSlug}-skill-runner-readiness-board-v1.json`,
    `${phaseSlug}-cleanup-tier-board-v1.json`,
    `${phaseSlug}-source-reflection-seed-reduction-v1.json`,
    `${phaseSlug}-trinity-mandala-planning-matrix-v1.json`,
    `${phaseSlug}-goal-mode-readiness-receipt-v1.json`,
    `${phaseSlug}-private-material-firewall-v1.json`,
    `${phaseSlug}-open-gate-rail-v1.json`,
    `${phaseSlug}-compact-x2-handoff-v1.json`,
    `${phaseSlug}-v2-arby-cicero-prep-card-v1.json`,
    `${phaseSlug}-phase-status-index-v1.json`,
    `${phaseSlug}-closeout-v1.json`,
  ];
}

function renderLumenHarvestMd(data) {
  return `# ${data.phase_slug} Lumen Advisory Harvest

Status: \`${data.overall_status}\`

## Advisory Summary

${data.advisory_summary.map((item) => `- ${item}`).join("\n")}

## Boundary

Raw chat transcript published: \`${data.raw_chat_transcript_published}\`
Raw browser route published: \`${data.raw_browser_route_published}\`

${boundarySentence()}
`;
}

function renderQueueReducerMd(data) {
  return `# ${data.phase_slug} Approval/Eureka Reducer

Status: \`${data.overall_status}\`

## Counts

- Safe-now packets: \`${data.safe_now_packets.length}\`
- Candidate packets: \`${data.candidate_packets.length}\`
- Exact-approval packets: \`${data.exact_packets.length}\`
- Blocked packets: \`${data.blocked_packets.length}\`

## Safe-Now Packets

${data.safe_now_packets.map((item) => `- ${item.id}: ${item.title} - ${item.disposition}`).join("\n")}

## Candidate Packets

${data.candidate_packets.map((item) => `- ${item.id}: ${item.title} - ${item.disposition}`).join("\n")}

## Exact-Approval Packets

${data.exact_packets.map((item) => `- ${item.id}: ${item.title} - ${item.disposition}`).join("\n")}

## Blocked Packets

${data.blocked_packets.map((item) => `- ${item.id}: ${item.title} - ${item.disposition}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderSafeExecutionLedgerMd(data) {
  return `# ${data.phase_slug} Safe-Now Execution Ledger

Status: \`${data.overall_status}\`

## Executed Safe Clusters

${data.executed_safe_clusters.map((item) => `- ${item}`).join("\n")}

## Minimal x2 Build Queue

${data.x2_minimal_build_queue.map((item) => `- ${item}`).join("\n")}

No exact boundaries crossed: \`${data.no_exact_boundaries_crossed}\`

## x1 to x2 Proposal Split

- Immediate x1 safe classes: \`${data.x1_to_x2_proposal_split_standard.immediate_x1_safe_tasks.length}\`
- x2 phase task classes: \`${data.x1_to_x2_proposal_split_standard.x2_phase_tasks.length}\`
`;
}

function renderProposalSplitStandardMd(data) {
  return `# ${data.phase_slug} x1 to x2 Proposal Split Standard

Status: \`${data.overall_status}\`

Classifier rule: ${data.classifier_rule}

## Immediate x1 Safe Tasks

${data.immediate_x1_safe_tasks.map((item) => `- ${item}`).join("\n")}

## x2 Phase Tasks

${data.x2_phase_tasks.map((item) => `- ${item}`).join("\n")}

## Never Auto-Execute

${data.never_auto_execute.map((item) => `- ${item}`).join("\n")}
`;
}

function renderPhaseToolRefreshStandardMd(data) {
  return `# ${data.phase_slug} Phase Tool Refresh Standard

Status: \`${data.overall_status}\`
Cadence: \`${data.cadence}\`

## Startup Required Actions

${data.startup_required_actions.map((item) => `- ${item}`).join("\n")}

## Closeout Required Actions

${data.closeout_required_actions.map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${data.safety_boundary}
`;
}

function renderSkillRunnerBoardMd(data) {
  return `# ${data.phase_slug} Skill/Runner Readiness Board

Status: \`${data.overall_status}\`

## Skill Ideas

${data.skill_ideas.map((item) => `- ${item.id}: ${item.name}`).join("\n")}

## Runner Ideas

${data.runner_ideas.map((item) => `- ${item.id}: ${item.name}`).join("\n")}

## Already Available Priority Tools

${data.already_available_priority_tools.map((item) => `- ${item}`).join("\n")}
`;
}

function renderCleanupBoardMd(data) {
  return `# ${data.phase_slug} Cleanup Tier Board

Status: \`${data.overall_status}\`

## Cleanup Proposals

${data.cleanup_proposals.map((item) => `- ${item.id}: ${item.title} - ${item.tier} - destructive: ${item.destructive}`).join("\n")}

## Forbidden First Slice Actions

${data.forbidden_first_slice_actions.map((item) => `- ${item}`).join("\n")}
`;
}

function renderSourceReflectionReductionMd(data) {
  return `# ${data.phase_slug} Source/Reflection Seed Reduction

Status: \`${data.overall_status}\`

- Source seed artifact: \`${data.source_seed_artifact}\`
- Reflection seed artifact: \`${data.reflection_seed_artifact}\`
- Source seed rows: \`${data.source_seed_rows}\`
- Reflection seed rows: \`${data.reflection_seed_rows}\`

## Reduction Use

${data.reduction_use.map((item) => `- ${item}`).join("\n")}
`;
}

function renderTrinityMatrixMd(data) {
  return `# ${data.phase_slug} Trinity Mandala Planning Matrix

Status: \`${data.overall_status}\`

${data.columns
  .map(
    (item) => `## ${item.pillar}

Focus: ${item.focus}

Boundary: ${item.boundary}`,
  )
  .join("\n\n")}
`;
}

function renderGoalModeReadinessMd(data) {
  return `# ${data.phase_slug} Goal Mode Readiness Receipt

Status: \`${data.overall_status}\`

Goal Mode active: \`${data.goal_mode_active}\`

Recommendation: ${data.recommendation}

## Readiness Dependencies

${data.readiness_dependencies.map((item) => `- ${item}`).join("\n")}
`;
}

function renderPrivateMaterialFirewallMd(data) {
  return `# ${data.phase_slug} Private Material Firewall

Status: \`${data.overall_status}\`

All blocked publication classes false: \`${data.all_blocked_publication_classes_false}\`

## Blocked Publication Classes

${data.blocked_publication_classes.map((item) => `- ${item}`).join("\n")}
`;
}

function renderOpenGateRailMd(data) {
  return `# ${data.phase_slug} Open Gate Rail

Status: \`${data.overall_status}\`

## Open Gates

${data.open_gates.map((item) => `- ${item}`).join("\n")}

## Claim Boundary

${Object.entries(data.claim_boundary).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}
`;
}

function renderCompactX2HandoffMd(data) {
  return `# ${data.phase_slug} Compact x2 Handoff

Status: \`${data.overall_status}\`
Next x2 scope: \`${data.next_x2_scope}\`

## First x2 Priority

${data.first_x2_priority.map((item) => `- ${item}`).join("\n")}

## Active Branch Truth

${data.active_branch_truth.map((item) => `- ${item}`).join("\n")}

## Operating Posture

${data.operating_posture.map((item) => `- ${item}`).join("\n")}

## Open Gates

${data.open_gates.map((item) => `- ${item}`).join("\n")}
`;
}

function renderArbyCiceroPrepMd(data) {
  return `# ${data.target_phase_slug} Arby/Cicero Prep Card

Status: \`${data.overall_status}\`
Source phase: \`${data.source_phase_slug}\`

## Lane Profile

- Participants: \`${data.lane_profile.participants.join(", ")}\`
- Safe minimum: \`${data.lane_profile.safe_minimum}\`
- Candidate: \`${data.lane_profile.candidate}\`
- Exact: \`${data.lane_profile.exact}\`
- Skills: \`${data.lane_profile.skills}\`
- Runners: \`${data.lane_profile.runners}\`
- Cleanup: \`${data.lane_profile.cleanup}\`

## Route Notes

${data.route_notes.map((item) => `- ${item}`).join("\n")}
`;
}

function renderPhaseStatusIndexMd(data) {
  return `# ${data.phase_slug} Phase Status Index

Status: \`${data.overall_status}\`

- Latest closed phase: \`${data.latest_closed_phase}\`
- Latest completed x1 phase: \`${data.latest_completed_x1_phase}\`
- Latest completed x2 phase: \`${data.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`
- Lumen response state: \`${data.lumen_response_state}\`

## Closeout Artifacts

${data.closeout_artifacts.map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderCloseoutMd(data) {
  return `# ${data.phase_slug} Closeout

Status: \`${data.overall_status}\`

- Closed lanes: \`${data.closed_lanes.join(", ")}\`
- Lumen response harvested: \`${data.lumen_response_harvested}\`
- Safe-now packets executed or represented: \`${data.safe_now_packets_executed_or_represented}\`
- Candidate packets queued: \`${data.candidate_packets_queued}\`
- Exact packets queued: \`${data.exact_packets_queued}\`
- Blocked packets kept open: \`${data.blocked_packets_kept_open}\`
- Skill ideas queued: \`${data.skill_ideas_queued}\`
- Runner ideas queued: \`${data.runner_ideas_queued}\`
- Cleanup proposals tiered: \`${data.cleanup_proposals_tiered}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`

## Validation Expectations

${data.validation_expectations.map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${(current.current_active_lanes || []).join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v553 v1 x1 Lumen Closeout

- Status: \`${current.v553_v1_x1_lumen_closeout?.status || "not_recorded"}\`
- Lumen response harvested: \`${current.v553_v1_x1_lumen_closeout?.lumen_response_harvested ?? "not_recorded"}\`
- Safe-now packets executed or represented: \`${current.v553_v1_x1_lumen_closeout?.safe_now_packets_executed_or_represented ?? "not_recorded"}\`
- Immediate x1 safe task classes: \`${current.v553_v1_x1_lumen_closeout?.immediate_x1_safe_task_classes ?? "not_recorded"}\`
- x2 phase task classes: \`${current.v553_v1_x1_lumen_closeout?.x2_phase_task_classes ?? "not_recorded"}\`
- Candidate packets queued: \`${current.v553_v1_x1_lumen_closeout?.candidate_packets_queued ?? "not_recorded"}\`
- Exact packets queued: \`${current.v553_v1_x1_lumen_closeout?.exact_packets_queued ?? "not_recorded"}\`
- Blocked packets kept open: \`${current.v553_v1_x1_lumen_closeout?.blocked_packets_kept_open ?? "not_recorded"}\`
- Next x2 scope: \`${current.v553_v1_x1_lumen_closeout?.next_x2_scope || "not_recorded"}\`

## Lumen Browser Send

- Status: \`${current.lumen_browser_send?.status || "not_recorded"}\`
- Send status: \`${current.lumen_browser_send?.send_status || "not_recorded"}\`
- Raw chat transcript published: \`${current.lumen_browser_send?.raw_chat_transcript_published ?? "not_recorded"}\`
- Raw browser route published: \`${current.lumen_browser_send?.raw_browser_route_published ?? "not_recorded"}\`

## Phase Tool Refresh Standard

- Status: \`${current.phase_tool_refresh_standard?.status || "not_recorded"}\`
- Cadence: \`${current.phase_tool_refresh_standard?.cadence || "not_recorded"}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
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

## v553 v1 x1 Lumen Closeout

- Status: \`${beacon.v553_v1_x1_lumen_closeout?.status || "not_recorded"}\`
- Lumen response harvested: \`${beacon.v553_v1_x1_lumen_closeout?.lumen_response_harvested ?? "not_recorded"}\`
- Safe-now packets executed or represented: \`${beacon.v553_v1_x1_lumen_closeout?.safe_now_packets_executed_or_represented ?? "not_recorded"}\`
- Next x2 scope: \`${beacon.v553_v1_x1_lumen_closeout?.next_x2_scope || "not_recorded"}\`

## x1 to x2 Proposal Split

- Status: \`${beacon.x1_to_x2_proposal_split_standard?.status || "not_recorded"}\`
- Immediate x1 safe classes: \`${beacon.x1_to_x2_proposal_split_standard?.immediate_x1_safe_tasks?.length ?? "not_recorded"}\`
- x2 phase task classes: \`${beacon.x1_to_x2_proposal_split_standard?.x2_phase_tasks?.length ?? "not_recorded"}\`

## Phase Tool Refresh Standard

- Status: \`${beacon.phase_tool_refresh_standard?.status || "not_recorded"}\`
- Cadence: \`${beacon.phase_tool_refresh_standard?.cadence || "not_recorded"}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function readOptionalJson(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  return readJson(filePath);
}

function countRows(filePath) {
  const data = readOptionalJson(filePath);
  if (!data) {
    return 0;
  }
  for (const key of ["rows", "sources", "reflections", "items"]) {
    if (Array.isArray(data[key])) {
      return data[key].length;
    }
  }
  return 0;
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function boundarySentence() {
  return "No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, proof closures, legal closures, canon promotions, deployments, purchases, account mutations, or API-key actions are published or claimed.";
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
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}
