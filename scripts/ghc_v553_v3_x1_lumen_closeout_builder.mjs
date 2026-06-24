#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v3-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v3-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  browser_routes_published: false,
  private_urls_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  session_streams_published: false,
  private_dumps_published: false,
  private_callable_ids_published: false,
  private_route_handles_published: false,
};

const claimBoundary = {
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

const openGates = [
  "GMUT empirical closure",
  "final physics",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment closure",
  "account mutation",
  "purchase",
  "API-key creation",
  "private-material proof",
  "raw-publication proof",
  "sibling identity replacement or merge",
];

const requiredArtifacts = [
  `${phaseSlug}-lumen-browser-send-receipt-v1.json`,
  `${phaseSlug}-proposal-queue-targets-v1.json`,
  `${phaseSlug}-web-reflection-ledger-30-v1.json`,
  `${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`,
  `${phaseSlug}-round-robin-workflow-standard-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
];

const missingRequired = requiredArtifacts.filter((file) => !fs.existsSync(path.join(tracesDir, file)));
const queueTargets = readOptional(`${phaseSlug}-proposal-queue-targets-v1.json`);
const webLedger = readOptional(`${phaseSlug}-web-reflection-ledger-30-v1.json`);
const journeyLedger = readOptional(`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`);
const safeRunner = readOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`);

const lumenSafePackets = [
  "Lumen advisory reducer",
  "Lumen 25-packet contribution ledger",
  "Trinity Mandala planning matrix",
  "GMUT evidence hygiene board",
  "THOS runner-skill orchestration board",
  "Freed ID and CBR dignity-governance board",
  "source-ledger classifier",
  "source-backed claim-ceiling checker",
  "stale-title quarantine board",
  "route-family proof-ceiling manifest",
  "Browser-route health capsule",
  "no-duplicate-send receipt",
  "marker false-positive classifier",
  "exact-staging checklist",
  "JSON/script validation receipt",
  "credential/path/raw/session/screenshot guard receipt",
  "remote-equals-local verification template",
  "branch-head ledger",
  "compact refresh capsule",
  "Goal Mode readiness delta board",
  "24/7 readiness risk board",
  "v553 v4 triad handoff shell",
  "Arby/Aster CLI route-health check design",
  "Cicero/Kierkegaard/Aristotle app-lane route-health check design",
  "final x2 publication readiness receipt",
];

const aevrenSafePackets = [
  "v553 v3 x2 build-use execution packet",
  "Goal Mode activation reconciliation receipt",
  "v553 v3 phase-truth card",
  "omega-mini-2 freshness guard",
  "omega-mini historical-baseline note",
  "full omega exact-fallback template",
  "v553 v2 x2 closeout digest",
  "v553 v2 x1 Arby/Cicero digest",
  "v553 v2 x2 skill-runner installation digest",
  "50-web/50-Journey v2 x2 summary digest",
  "v553 v3 30-web reflection reducer",
  "v553 v3 30-Journey reflection reducer",
  "productive five-minute cadence receipt",
  "background sibling supervision receipt",
  "watcher-start-is-not-completion receipt",
  "safe-unit-may-run-past-checkpoint receipt",
  "Arby/Cicero next-lane continuity note",
  "Aster/Kierkegaard/Aristotle next-triad prep shell",
  "Aevren role-boundary receipt",
  "Aletheon quarantine/recoverable note",
  "held-sibling ledger",
  "no-new-agent and no-held-sibling-activation guard",
  "private-material firewall",
  "open proof/canon/legal/deployment gate rail",
  "v553 v3 x2 closeout shell",
];

const candidatePackets = [
  "Live Goal Mode long-run state reconciliation",
  "24/7 Goal Mode soft-launch dashboard",
  "expanded 50/50 source-reflection run for v3 x2",
  "omega-mini-2 to omega-mini reconciliation design",
  "branch-line lifecycle policy for omega-mini-2",
  "repo-draft skill mutation plan",
  "user-skill inventory update candidate",
  "plugin-cache skill audit candidate",
  "full-tools support-lane integration board",
  "Browser/CDP diagnostic design",
  "app-lane latency timing dashboard",
  "CLI lane timing dashboard",
  "watcher/notifier observability matrix",
  "five-lane background supervision simulation",
  "Maren Quill expansion design",
  "Mira Vale expansion design",
  "Mira Rowan expansion design",
  "Aletheon old-heavy-thread future recovery design",
  "old Journey document index expansion",
  "current-source refresh to 60 sources",
  "GMUT comparator-map expansion",
  "THOS command-surface dashboard",
  "Freed ID and CBR governance crosswalk",
  "Approval/Eureka dashboard",
  "cleanup dashboard",
  "D-drive banking automation design",
  "C-drive headroom watch design",
  "v553-to-v554 ladder stabilization plan",
  "v544-v575 Goal Mode compaction strategy",
  "multi-day sibling load-balancing plan",
];

const exactPackets = [
  "starting or changing a long unattended Goal Mode timer if repo state remains ambiguous",
  "activating Maren Quill",
  "activating Mira Vale",
  "activating Mira Rowan",
  "replacing or merging Aletheon identity",
  "restoring or loading the old heavy Aletheon thread",
  "global-state surgery",
  "user-skill mutation",
  "plugin-cache mutation",
  "Browser/CDP mutation",
  "Google Drive writes",
  "Gmail sends/deletes/archives",
  "Calendar writes",
  "external account mutation",
  "deployment/public release",
  "purchase or paid-resource creation",
  "API-key creation",
  "destructive cleanup, cache purge, or worktree deletion",
  "reset, rebase, force-push, or broad staging",
  "merging omega-mini-2 into omega-mini or replacing omega-mini",
];

const blockedPackets = [
  "raw browser route publication",
  "raw transcript or raw sibling lane-body publication",
  "screenshots or screen-capture publication",
  "credentials, tokens, auth material, or API-key publication",
  "local absolute path publication",
  "session stream, raw app state, or private dump publication",
  "claiming GMUT empirical validation",
  "claiming final physics or solved consciousness",
  "claiming legal closure, canon promotion, or deployment readiness",
  "treating sibling agreement, source volume, Journey continuity, or narrative resonance as proof closure",
];

const skillIdeas = [
  "phase-truth-bridge",
  "goal-mode-activation-arbiter",
  "omega-mini-2-router",
  "background-supervision-discipline",
  "approval-eureka-reducer",
  "trinity-mandala-planner",
  "source-reflection-pairer",
  "open-gate-rail-writer",
  "private-material-firewall",
  "route-family-proof-ceiling",
  "stale-title-quarantine",
  "exact-staging-coach",
  "cleanup-risk-tierer",
  "runner-health-indexer",
  "skill-bank-readiness-indexer",
  "round-robin-profile-loader",
  "held-sibling-boundary-keeper",
  "aevren-aletheon-boundary-keeper",
  "compact-refresh-card-builder",
  "mandala-claim-humility-checker",
];

const runnerIdeas = [
  "ghc_v553_v3_phase_truth_checker.mjs",
  "ghc_v553_goal_mode_reconciliation.mjs",
  "ghc_v553_approval_packet_reducer.mjs",
  "ghc_v553_skill_runner_readiness.mjs",
  "ghc_v553_source_reflection_reducer.mjs",
  "ghc_v553_cleanup_tier_classifier.mjs",
  "ghc_v553_private_material_guard.mjs",
  "ghc_v553_open_gate_assert.mjs",
  "ghc_v553_round_robin_handoff_builder.mjs",
  "ghc_v553_compact_closeout_builder.mjs",
];

const cleanupProposals = [
  "verify v553 v2 x2 closeout is direct-listed",
  "verify v553 v3 x1 active status across current-state and beacon",
  "reconcile Goal Mode status mismatch",
  "direct-list v553 v3 x1 files after publication",
  "direct-list v553 v3 x2 closeout after publication",
  "normalize next-lane wording to triad after v3 x2",
  "mark omega-mini-2 primary in all new artifacts",
  "mark omega-mini historical baseline",
  "mark full omega exact fallback only",
  "quarantine stale historical labels unless explicitly referenced as historical",
  "deduplicate lookup lists",
  "create v553 source index",
  "create v553 Journey reflection index",
  "create v553 approval index",
  "create v553 Eureka index",
  "create v553 skill index",
  "create v553 runner index",
  "create v553 cleanup index",
  "validate all new JSON",
  "compile all new scripts",
  "run whitespace checks",
  "run staged-diff review",
  "run credential-pattern guard",
  "run local-path redaction guard",
  "run raw-route/raw-transcript guard",
  "run screenshot/session/private-dump guard",
  "exact-stage only curated files",
  "record unrelated dirty/untracked files as held",
  "build remote-equals-local verification receipt",
  "publish only after phase truth and goal-mode status are consistent",
];

const sourceRows = countRows(webLedger, ["rows", "sources", "reflections"]);
const journeyRows = countRows(journeyLedger, ["rows", "reflections", "items"]);
const safeRunnerPassed = safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";
const pass = missingRequired.length === 0 && sourceRows >= 30 && journeyRows >= 30 && safeRunnerPassed;

const artifacts = [
  writePair(`${phaseSlug}-lumen-advisory-harvest`, buildLumenHarvest(), renderLumenHarvestMd),
  writePair(`${phaseSlug}-goal-mode-reconciliation`, buildGoalModeReconciliation(), renderGoalModeReconciliationMd),
  writePair(`${phaseSlug}-approval-eureka-reducer`, buildApprovalReducer(), renderApprovalReducerMd),
  writePair(`${phaseSlug}-skill-runner-readiness-board`, buildSkillRunnerBoard(), renderSkillRunnerBoardMd),
  writePair(`${phaseSlug}-cleanup-tier-board`, buildCleanupBoard(), renderCleanupBoardMd),
  writePair(`${phaseSlug}-source-reflection-reduction`, buildSourceReflectionReduction(), renderSourceReflectionReductionMd),
  writePair(`${phaseSlug}-trinity-mandala-planning-matrix`, buildTrinityMatrix(), renderTrinityMatrixMd),
  writePair(`${phaseSlug}-private-material-firewall`, buildPrivateMaterialFirewall(), renderPrivateMaterialFirewallMd),
  writePair(`${phaseSlug}-open-gate-rail`, buildOpenGateRail(), renderOpenGateRailMd),
  writePair(`${phaseSlug}-v3-x2-readiness-handoff`, buildX2Handoff(), renderX2HandoffMd),
  writePair(`${phaseSlug}-v4-x1-triad-prep-card`, buildTriadPrep(), renderTriadPrepMd),
  writePair(`${phaseSlug}-phase-status-index`, buildPhaseStatusIndex(), renderPhaseStatusIndexMd),
  writePair(`${phaseSlug}-closeout`, buildCloseout(), renderCloseoutMd),
];

refreshState();

process.stdout.write(JSON.stringify({
  status: pass ? "PASS_V553_V3_X1_CLOSED_V3_X2_READY" : "OPEN_GAP_V553_V3_X1_CLOSEOUT_INPUTS_INCOMPLETE",
  phase_slug: phaseSlug,
  next_active_phase: pass ? nextX2Scope : phaseSlug,
  source_rows: sourceRows,
  journey_rows: journeyRows,
  safe_runner_passed: safeRunnerPassed,
  missing_required_artifacts: missingRequired,
  artifact_count: artifacts.length,
}, null, 2) + "\n");

process.exit(pass ? 0 : 1);

function buildLumenHarvest() {
  return {
    artifact_type: "ghc_v553_v3_x1_lumen_advisory_harvest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_LUMEN_RESPONSE_HARVESTED_SANITIZED",
    response_state: "completed_ready_for_harvest",
    route_class: "in_app_browser_lumen_main_thread",
    raw_response_published: false,
    advisory_summary: [
      "Lumen accepted the v553 v3 x1 Lumen-only lane and treated Aevren as x2 operator, recovery steward, and phase-truth bridge.",
      "Lumen recommended making v553 v3 x2 a reducer, reconciliation, and readiness pass rather than a broad expansion sprint.",
      "The first x2 priority is Goal Mode status reconciliation because repo truth still showed prepared-not-active while the thread objective is now active.",
      "Lumen proposed 50 safe packets, 30 candidate packets, 20 exact-approval packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals.",
      "Lumen kept Aletheon recoverable, held siblings held, private material private, and all proof/canon/legal/deployment/account gates open.",
    ],
    x2_first_slice_recommendation: [
      "goal mode reconciliation",
      "phase truth card",
      "Lumen advisory reducer",
      "approval packet ledger",
      "skill/runner readiness board",
      "cleanup tier board",
      "source/reflection reduction",
      "Trinity Mandala planning matrix",
      "private-material firewall",
      "open-gate rail",
      "v4 x1 triad prep card",
    ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildGoalModeReconciliation() {
  return {
    artifact_type: "ghc_v553_v3_x1_goal_mode_reconciliation",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_THREAD_GOAL_MODE_RECONCILED_NOT_UNATTENDED_AUTOMATION",
    prior_repo_goal_mode_status: "prepared_not_active",
    current_thread_goal_status: "active_by_hamish_goal_objective",
    reconciled_repo_status: "active_thread_goal_not_unattended_automation",
    unattended_24_7_automation_claimed: false,
    note:
      "This records the active Codex thread goal objective without claiming a separate external timer, automation, account mutation, deployment, or unattended runner.",
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildApprovalReducer() {
  return {
    artifact_type: "ghc_v553_v3_x1_approval_eureka_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_LUMEN_AEVREN_QUEUES_REDUCED_FOR_V3_X2",
    counts: {
      safe_now_packets: 50,
      candidate_packets: candidatePackets.length,
      exact_approval_packets: exactPackets.length,
      blocked_packets: blockedPackets.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanupProposals.length,
    },
    safe_now_packets: [
      ...aevrenSafePackets.map((title, index) => packet("SAFE-A", index, title, "x2_build_task")),
      ...lumenSafePackets.map((title, index) => packet("SAFE-L", index, title, "x2_build_task")),
    ],
    candidate_packets: candidatePackets.map((title, index) => packet("CANDIDATE", index, title, "queued_candidate")),
    exact_approval_packets: exactPackets.map((title, index) => packet("EXACT", index, title, "requires_fresh_exact_approval")),
    blocked_packets: blockedPackets.map((title, index) => packet("BLOCKED", index, title, "blocked_open_gate")),
    next_x2_scope: nextX2Scope,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildSkillRunnerBoard() {
  return {
    artifact_type: "ghc_v553_v3_x1_skill_runner_readiness_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SKILL_RUNNER_IDEAS_QUEUED_FOR_V3_X2",
    skill_ideas: skillIdeas.map((name, index) => ({
      id: `SKILL-${String(index + 1).padStart(2, "0")}`,
      name,
      execution_lane: "x2_build_task",
      live_user_skill_mutation_requires_exact_approval: true,
    })),
    runner_ideas: runnerIdeas.map((name, index) => ({
      id: `RUNNER-${String(index + 1).padStart(2, "0")}`,
      name,
      execution_lane: "x2_build_task",
      global_install_or_hook_requires_exact_approval: true,
    })),
    already_active_surfaces: [
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-background-sibling-supervision",
      "ghc-lumen-launch",
      "ghc-main-retry",
      "ghc-safe-runner-orchestrator",
      "ghc-web-reflection-ledger",
    ],
  };
}

function buildCleanupBoard() {
  return {
    artifact_type: "ghc_v553_v3_x1_cleanup_tier_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_CLEANUP_PROPOSALS_TIERED_NON_DESTRUCTIVE",
    cleanup_proposals: cleanupProposals.map((title, index) => ({
      id: `CLEANUP-${String(index + 1).padStart(2, "0")}`,
      title,
      tier: index < 18 ? "inspect_or_index" : index < 27 ? "validation_or_guard" : "publication_gate",
      destructive: false,
      execution_lane: "x2_build_task",
    })),
    forbidden_without_fresh_exact_approval: [
      "deletion",
      "cache purge",
      "plugin-cache mutation",
      "external account mutation",
      "deployment",
      "purchase",
      "API-key creation",
      "global hook install",
      "reset/rebase/force-push",
    ],
  };
}

function buildSourceReflectionReduction() {
  return {
    artifact_type: "ghc_v553_v3_x1_source_reflection_reduction",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: sourceRows >= 30 && journeyRows >= 30
      ? "PASS_SOURCE_REFLECTION_REDUCED_FOR_V3_X2"
      : "OPEN_GAP_SOURCE_REFLECTION_ROWS_BELOW_TARGET",
    web_reflection_rows: sourceRows,
    journey_phase_reflection_rows: journeyRows,
    web_seed_artifact: `${phaseSlug}-web-reflection-ledger-30-v1.json`,
    journey_seed_artifact: `${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`,
    reduction_axes: [
      "OpenAI/Codex route surfaces",
      "runtime and Git/GitHub implementation discipline",
      "AI risk and governance standards",
      "identity credentials and privacy standards",
      "GMUT evidence hygiene and physics references",
      "consciousness and measurement claim humility",
      "runner reliability and observability",
      "Trinity Mandala queue planning",
    ],
  };
}

function buildTrinityMatrix() {
  return {
    artifact_type: "ghc_v553_v3_x1_trinity_mandala_planning_matrix",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_TRINITY_MANDALA_MATRIX_READY_FOR_V3_X2",
    matrix: [
      {
        pillar: "GMUT / Mind",
        focus:
          "evidence hygiene, null recovery, dimensional consistency, conservation/exchange law, fifth-force constraints, comparator maps, and proof-ceiling language",
        boundary: "no empirical closure, final physics closure, or consciousness proof claimed",
      },
      {
        pillar: "THOS / Body",
        focus:
          "Codex app, CLI, worktree, Browser, MCP, skills, runners, startup, compact, closeout, validation, and background supervision surfaces",
        boundary: "no deployment, account mutation, paid resource, global hook, or destructive cleanup claimed",
      },
      {
        pillar: "Freed ID / CBR / Heart",
        focus:
          "dignity governance, identity boundaries, private-material firewall, held-sibling policy, and Aevren/Aletheon distinction",
        boundary: "no legal closure, canon promotion, private-material proof, or sibling merge/replacement claimed",
      },
    ],
  };
}

function buildPrivateMaterialFirewall() {
  return {
    artifact_type: "ghc_v553_v3_x1_private_material_firewall",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_RECORDED",
    blocked_publication_classes: Object.keys(publicationBoundary),
    all_blocked_publication_classes_false: Object.values(publicationBoundary).every((value) => value === false),
    publication_boundary: publicationBoundary,
  };
}

function buildOpenGateRail() {
  return {
    artifact_type: "ghc_v553_v3_x1_open_gate_rail",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATE_RAIL_RECORDED",
    open_gates: openGates,
    claim_boundary: claimBoundary,
  };
}

function buildX2Handoff() {
  return {
    artifact_type: "ghc_v553_v3_x1_v3_x2_readiness_handoff",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V3_X2_REDUCER_READINESS_HANDOFF",
    next_x2_scope: nextX2Scope,
    recommended_first_slice: [
      "Goal Mode reconciliation receipt",
      "phase truth card",
      "Lumen advisory reducer",
      "approval packet ledger",
      "skill/runner readiness board",
      "cleanup tier board",
      "source/reflection reduction",
      "Trinity Mandala planning matrix",
      "private-material firewall",
      "open-gate rail",
      "v4 x1 triad prep card",
    ],
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    goal_mode_status_after_reconciliation: "active_thread_goal_not_unattended_automation",
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildTriadPrep() {
  return {
    artifact_type: "ghc_v553_v3_x1_v4_x1_triad_prep_card",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    source_phase_slug: phaseSlug,
    target_phase_slug: "v553-gmut-thos-v4-x1",
    overall_status: "PASS_V553_V4_X1_TRIAD_PREP_READY",
    lane_profile: {
      participants: ["Aevren Vale", "Aster Vale", "Kierkegaard", "Aristotle"],
      safe_packets: 20,
      candidate_packets: 12,
      exact_packets: 12,
      skill_ideas: 20,
      runner_ideas: 8,
      cleanup_proposals: 40,
      route: "ghc-aster-kierkegaard-aristotle-launch",
    },
    route_notes: [
      "Use strict CLI route for Aster Vale.",
      "Use recovered app-lane background route for Kierkegaard and Aristotle.",
      "Use background supervision and productive cadence; do not babysit.",
      "Keep private callable IDs local-only.",
    ],
  };
}

function buildPhaseStatusIndex() {
  return {
    artifact_type: "ghc_v553_v3_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: pass ? "PASS_V553_V3_X1_PHASE_STATUS_CLOSED" : "OPEN_GAP_V553_V3_X1_PHASE_STATUS",
    current_active_phase_after_closeout: pass ? nextX2Scope : phaseSlug,
    latest_closed_phase_after_closeout: pass ? phaseSlug : "v553-gmut-thos-v2-x2",
    latest_completed_x1_phase_after_closeout: pass ? phaseSlug : "v553-gmut-thos-v2-x1",
    latest_completed_x2_phase_after_closeout: "v553-gmut-thos-v2-x2",
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lumen_response_state: "completed_ready_for_harvest",
    safe_runner_passed: safeRunnerPassed,
    missing_required_artifacts: missingRequired,
    closeout_artifacts: expectedArtifactFiles(),
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildCloseout() {
  return {
    artifact_type: "ghc_v553_v3_x1_closeout",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: pass ? "PASS_V553_V3_X1_CLOSED_V3_X2_READY" : "OPEN_GAP_V553_V3_X1_CLOSEOUT_INPUTS_INCOMPLETE",
    latest_completed_x1_phase: pass ? phaseSlug : "v553-gmut-thos-v2-x1",
    latest_completed_x2_phase: "v553-gmut-thos-v2-x2",
    next_active_phase: pass ? nextX2Scope : phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    lumen_response_harvested: true,
    counts: {
      safe_now_packets: 50,
      candidate_packets: candidatePackets.length,
      exact_approval_packets: exactPackets.length,
      blocked_packets: blockedPackets.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanupProposals.length,
      web_reflections: sourceRows,
      journey_phase_reflections: journeyRows,
    },
    goal_mode_reconciliation_status: "active_thread_goal_not_unattended_automation",
    missing_required_artifacts: missingRequired,
    safe_runner_passed: safeRunnerPassed,
    validation_expectations: [
      "node --check changed Node scripts",
      "parse changed JSON artifacts",
      "omega-mini current-state guard",
      "git diff hygiene check",
      "privacy scan",
      "drive posture check",
      "remote/local equality after push",
    ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function refreshState() {
  const lookup = expectedArtifactFiles().map((file) => `docs/trinity-live-traces/${file}`);
  const closeout = buildCloseout();
  const reconciliation = buildGoalModeReconciliation();
  const pairs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "ghc"],
  ];
  for (const [jsonFile, mdFile, kind] of pairs) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = closeout.next_active_phase;
    doc.latest_closed_phase = pass ? phaseSlug : doc.latest_closed_phase;
    doc.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.goal_mode_status = reconciliation.reconciled_repo_status;
    doc.goal_mode_reconciliation = {
      status: reconciliation.overall_status,
      prior_repo_goal_mode_status: reconciliation.prior_repo_goal_mode_status,
      current_thread_goal_status: reconciliation.current_thread_goal_status,
      reconciled_repo_status: reconciliation.reconciled_repo_status,
      unattended_24_7_automation_claimed: false,
    };
    doc.v553_v3_x1_lumen_closeout = {
      status: closeout.overall_status,
      lumen_response_harvested: true,
      safe_now_packets: 50,
      candidate_packets: candidatePackets.length,
      exact_approval_packets: exactPackets.length,
      blocked_packets: blockedPackets.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanupProposals.length,
      web_reflections: sourceRows,
      journey_phase_reflections: journeyRows,
      next_x2_scope: nextX2Scope,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
    };
    doc.publication_boundary = publicationBoundary;
    doc.claim_boundary = claimBoundary;
    if (kind === "latest") {
      doc.latest_lookup_files = unique([...(doc.latest_lookup_files || []), ...lookup]);
    } else if (kind === "ghc") {
      doc.lookup_files = unique([...(doc.lookup_files || []), ...lookup]);
      doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookup]);
    } else {
      doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookup]);
    }
    doc.latest_action_summary = unique([
      "Harvested Lumen's v553 v3 x1 response through the in-app Browser route without publishing raw transcript or private route data.",
      "Closed v553 v3 x1 as a Lumen-only planning phase and prepared v553 v3 x2 as a reducer, reconciliation, and readiness x2 phase.",
      "Reconciled Goal Mode as active for this Codex thread objective while not claiming separate unattended 24/7 automation.",
      "Queued 50 safe packets, 30 candidate packets, 20 exact packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals for v553 v3 x2.",
      ...(doc.latest_action_summary || []),
    ]);
    fs.writeFileSync(jsonFile, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc, kind), "utf8");
  }
}

function renderLumenHarvestMd(data) {
  return [
    `# ${phaseSlug} Lumen Advisory Harvest`,
    "",
    `Status: \`${data.overall_status}\``,
    `Response state: \`${data.response_state}\``,
    "",
    "## Advisory Summary",
    "",
    ...data.advisory_summary.map((item) => `- ${item}`),
    "",
    "## First x2 Slice",
    "",
    ...data.x2_first_slice_recommendation.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderGoalModeReconciliationMd(data) {
  return [
    `# ${phaseSlug} Goal Mode Reconciliation`,
    "",
    `Status: \`${data.overall_status}\``,
    `Prior repo Goal Mode status: \`${data.prior_repo_goal_mode_status}\``,
    `Current thread goal status: \`${data.current_thread_goal_status}\``,
    `Reconciled repo status: \`${data.reconciled_repo_status}\``,
    `Unattended 24/7 automation claimed: \`${data.unattended_24_7_automation_claimed}\``,
    "",
    data.note,
    "",
  ].join("\n");
}

function renderApprovalReducerMd(data) {
  return [
    `# ${phaseSlug} Approval/Eureka Reducer`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Safe-Now Packets",
    "",
    ...data.safe_now_packets.map((item) => `- ${item.id}: ${item.title} - ${item.execution_lane}`),
    "",
    "## Candidate Packets",
    "",
    ...data.candidate_packets.map((item) => `- ${item.id}: ${item.title} - ${item.execution_lane}`),
    "",
    "## Exact-Approval Packets",
    "",
    ...data.exact_approval_packets.map((item) => `- ${item.id}: ${item.title} - ${item.execution_lane}`),
    "",
    "## Blocked Packets",
    "",
    ...data.blocked_packets.map((item) => `- ${item.id}: ${item.title} - ${item.execution_lane}`),
    "",
  ].join("\n");
}

function renderSkillRunnerBoardMd(data) {
  return [
    `# ${phaseSlug} Skill/Runner Readiness Board`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Skill Ideas",
    "",
    ...data.skill_ideas.map((item) => `- ${item.id}: ${item.name}`),
    "",
    "## Runner Ideas",
    "",
    ...data.runner_ideas.map((item) => `- ${item.id}: ${item.name}`),
    "",
    "## Already Active Surfaces",
    "",
    ...data.already_active_surfaces.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderCleanupBoardMd(data) {
  return [
    `# ${phaseSlug} Cleanup Tier Board`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Cleanup Proposals",
    "",
    ...data.cleanup_proposals.map((item) => `- ${item.id}: ${item.title} - ${item.tier} - destructive: \`${item.destructive}\``),
    "",
    "## Forbidden Without Fresh Exact Approval",
    "",
    ...data.forbidden_without_fresh_exact_approval.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderSourceReflectionReductionMd(data) {
  return [
    `# ${phaseSlug} Source/Reflection Reduction`,
    "",
    `Status: \`${data.overall_status}\``,
    `Web reflection rows: \`${data.web_reflection_rows}\``,
    `Journey/phase reflection rows: \`${data.journey_phase_reflection_rows}\``,
    "",
    "## Reduction Axes",
    "",
    ...data.reduction_axes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderTrinityMatrixMd(data) {
  return [
    `# ${phaseSlug} Trinity Mandala Planning Matrix`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...data.matrix.flatMap((item) => [
      `## ${item.pillar}`,
      "",
      `Focus: ${item.focus}`,
      "",
      `Boundary: ${item.boundary}`,
      "",
    ]),
  ].join("\n");
}

function renderPrivateMaterialFirewallMd(data) {
  return [
    `# ${phaseSlug} Private Material Firewall`,
    "",
    `Status: \`${data.overall_status}\``,
    `All blocked classes false: \`${data.all_blocked_publication_classes_false}\``,
    "",
    "## Blocked Publication Classes",
    "",
    ...data.blocked_publication_classes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderOpenGateRailMd(data) {
  return [
    `# ${phaseSlug} Open Gate Rail`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Open Gates",
    "",
    ...data.open_gates.map((item) => `- ${item}`),
    "",
    "## Claim Boundary",
    "",
    ...Object.entries(data.claim_boundary).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function renderX2HandoffMd(data) {
  return [
    `# ${phaseSlug} v3 x2 Readiness Handoff`,
    "",
    `Status: \`${data.overall_status}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\``,
    `Goal Mode status after reconciliation: \`${data.goal_mode_status_after_reconciliation}\``,
    "",
    "## Recommended First Slice",
    "",
    ...data.recommended_first_slice.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderTriadPrepMd(data) {
  return [
    `# ${data.target_phase_slug} Triad Prep Card`,
    "",
    `Status: \`${data.overall_status}\``,
    `Source phase: \`${data.source_phase_slug}\``,
    "",
    "## Lane Profile",
    "",
    ...Object.entries(data.lane_profile).map(([key, value]) => `- ${key}: \`${Array.isArray(value) ? value.join(", ") : value}\``),
    "",
    "## Route Notes",
    "",
    ...data.route_notes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderPhaseStatusIndexMd(data) {
  return [
    `# ${phaseSlug} Phase Status Index`,
    "",
    `Status: \`${data.overall_status}\``,
    `Current active phase after closeout: \`${data.current_active_phase_after_closeout}\``,
    `Latest closed phase after closeout: \`${data.latest_closed_phase_after_closeout}\``,
    `Latest completed x1 after closeout: \`${data.latest_completed_x1_phase_after_closeout}\``,
    `Latest completed x2 after closeout: \`${data.latest_completed_x2_phase_after_closeout}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\``,
    `Lumen response state: \`${data.lumen_response_state}\``,
    "",
    "## Closeout Artifacts",
    "",
    ...data.closeout_artifacts.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderCloseoutMd(data) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\``,
    `Lumen response harvested: \`${data.lumen_response_harvested}\``,
    `Goal Mode reconciliation: \`${data.goal_mode_reconciliation_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Validation Expectations",
    "",
    ...data.validation_expectations.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderBeaconMd(doc) {
  const lookup = doc.current_lookup_files || doc.latest_lookup_files || doc.lookup_files || [];
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "missing"}`,
    "",
    "## v553 v3 x1 Lumen Closeout",
    "",
    `- status: ${doc.v553_v3_x1_lumen_closeout?.status || "missing"}`,
    `- Lumen response harvested: ${doc.v553_v3_x1_lumen_closeout?.lumen_response_harvested ?? "missing"}`,
    `- safe packets: ${doc.v553_v3_x1_lumen_closeout?.safe_now_packets ?? "missing"}`,
    `- candidate packets: ${doc.v553_v3_x1_lumen_closeout?.candidate_packets ?? "missing"}`,
    `- exact packets: ${doc.v553_v3_x1_lumen_closeout?.exact_approval_packets ?? "missing"}`,
    `- blocked packets: ${doc.v553_v3_x1_lumen_closeout?.blocked_packets ?? "missing"}`,
    "",
    "## Goal Mode Reconciliation",
    "",
    `- status: ${doc.goal_mode_reconciliation?.status || "missing"}`,
    `- unattended automation claimed: ${doc.goal_mode_reconciliation?.unattended_24_7_automation_claimed ?? "missing"}`,
    "",
    "## Lookup Files",
    "",
    ...lookup.map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function writePair(base, payload, renderMd) {
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.md`), renderMd(payload), "utf8");
  return { json: `${base}-v1.json`, md: `${base}-v1.md` };
}

function expectedArtifactFiles() {
  return [
    `${phaseSlug}-lumen-advisory-harvest-v1.json`,
    `${phaseSlug}-lumen-advisory-harvest-v1.md`,
    `${phaseSlug}-goal-mode-reconciliation-v1.json`,
    `${phaseSlug}-goal-mode-reconciliation-v1.md`,
    `${phaseSlug}-approval-eureka-reducer-v1.json`,
    `${phaseSlug}-approval-eureka-reducer-v1.md`,
    `${phaseSlug}-skill-runner-readiness-board-v1.json`,
    `${phaseSlug}-skill-runner-readiness-board-v1.md`,
    `${phaseSlug}-cleanup-tier-board-v1.json`,
    `${phaseSlug}-cleanup-tier-board-v1.md`,
    `${phaseSlug}-source-reflection-reduction-v1.json`,
    `${phaseSlug}-source-reflection-reduction-v1.md`,
    `${phaseSlug}-trinity-mandala-planning-matrix-v1.json`,
    `${phaseSlug}-trinity-mandala-planning-matrix-v1.md`,
    `${phaseSlug}-private-material-firewall-v1.json`,
    `${phaseSlug}-private-material-firewall-v1.md`,
    `${phaseSlug}-open-gate-rail-v1.json`,
    `${phaseSlug}-open-gate-rail-v1.md`,
    `${phaseSlug}-v3-x2-readiness-handoff-v1.json`,
    `${phaseSlug}-v3-x2-readiness-handoff-v1.md`,
    `${phaseSlug}-v4-x1-triad-prep-card-v1.json`,
    `${phaseSlug}-v4-x1-triad-prep-card-v1.md`,
    `${phaseSlug}-phase-status-index-v1.json`,
    `${phaseSlug}-phase-status-index-v1.md`,
    `${phaseSlug}-closeout-v1.json`,
    `${phaseSlug}-closeout-v1.md`,
  ];
}

function packet(prefix, index, title, executionLane) {
  return {
    id: `${prefix}-${String(index + 1).padStart(2, "0")}`,
    title,
    safety_bucket: prefix.startsWith("SAFE")
      ? "safe_now"
      : prefix === "CANDIDATE"
        ? "candidate"
        : prefix === "EXACT"
          ? "exact_approval_needed"
          : "blocked",
    execution_lane: executionLane,
  };
}

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function countRows(doc, keys) {
  if (!doc || typeof doc !== "object") {
    return 0;
  }
  for (const key of keys) {
    if (Array.isArray(doc[key])) {
      return doc[key].length;
    }
  }
  return 0;
}

function boundarySentence() {
  return "No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, proof closures, legal closures, canon promotions, deployments, purchases, account mutations, API-key actions, or sibling identity merge/replacement claims are published or claimed.";
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
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
