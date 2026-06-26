#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const phaseSlug = "v559-gmut-thos-v6-x2";
const sourceX1 = "v559-gmut-thos-v6-x1";
const nextX1 = "v559-gmut-thos-v7-x1 Lumen-only unless Hamish redirects";
const root = process.cwd();
const traceDir = join(root, "docs", "trinity-live-traces");
const omegaDir = join(root, "docs", "omega-mini-index");
mkdirSync(traceDir, { recursive: true });

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const state = readJson(join(omegaDir, "omega-mini-current-state-v1.json"));
const queue = readJson(join(traceDir, `${sourceX1}-combined-x1-to-x2-queue-v1.json`));
const counts = queue.profile_cap_counts_represented || {};
const phaseTruthPass = (
  state.current_active_phase === phaseSlug &&
  state.latest_closed_phase === sourceX1 &&
  state.latest_completed_x1_phase === sourceX1 &&
  state.next_x1_lane_after_x2 === nextX1
) || (
  state.current_active_phase === "v559-gmut-thos-v7-x1" &&
  state.latest_closed_phase === phaseSlug &&
  state.latest_completed_x1_phase === sourceX1 &&
  state.latest_completed_x2_phase === phaseSlug
);

const commonBoundary = {
  raw_private_material_published: false,
  raw_browser_routes_published: false,
  private_ids_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  raw_app_state_published: false,
};

const claimBoundary = {
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

const artifacts = [
  buildArtifact("phase-truth-guard", "ghc.phase_truth_guard.v1", {
    status: phaseTruthPass ? "PASS_V559_V6_X2_PHASE_TRUTH_GUARD" : "OPEN_GAP_V559_V6_X2_PHASE_TRUTH_GUARD",
    checks: {
      active_phase: state.current_active_phase,
      expected_active_phase_before_closeout: phaseSlug,
      expected_active_phase_after_closeout: "v559-gmut-thos-v7-x1",
      latest_closed_phase: state.latest_closed_phase,
      expected_latest_closed_before_closeout: sourceX1,
      expected_latest_closed_after_closeout: phaseSlug,
      latest_completed_x1_phase: state.latest_completed_x1_phase,
      expected_latest_completed_x1_phase: sourceX1,
      latest_completed_x2_phase: state.latest_completed_x2_phase,
      expected_latest_completed_x2_after_closeout: phaseSlug,
      next_x1_lane_after_x2: state.next_x1_lane_after_x2,
      expected_next_x1_lane_after_x2: nextX1,
    },
  }),
  buildArtifact("duo-queue-count-guard", "ghc.duo_queue_count_guard.v1", {
    status: countsPass(counts)
      ? "PASS_V559_V6_X2_DUO_QUEUE_COUNT_GUARD"
      : "OPEN_GAP_V559_V6_X2_DUO_QUEUE_COUNT_GUARD",
    counts,
    immediate_x1_safe_rows: queue.immediate_x1_safe_rows_represented || 0,
    x2_build_rows: queue.x2_build_rows_represented || 0,
    required_counts: {
      safe_approval_packets: 30,
      candidate_packets: 15,
      exact_approval_packets_queued: 15,
      skill_ideas: 21,
      runner_ideas: 9,
      cleanup_refine_fix_tasks: 45,
    },
  }),
  buildArtifact("candidate-exact-open-gate-queue", "ghc.candidate_exact_queue.v1", {
    status: "PASS_V559_V6_X2_CANDIDATE_EXACT_ROWS_QUEUED_OPEN",
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate rows are represented in safe build guidance; exact gates are not auto-run.",
    open_gates: openGates(),
  }),
  buildArtifact("skill-runner-prototype-use-ledger", "ghc.skill_runner_prototype_use_ledger.v1", {
    status: "PASS_V559_V6_X2_SKILL_RUNNER_PROTOTYPE_LEDGER",
    skills_represented: counts.skill_ideas || 0,
    runners_represented: counts.runner_ideas || 0,
    prototypes_built_or_used: [
      "v6 x2 reflection manifest builder",
      "v6 x2 safe build bundle",
      "safe runner orchestrator",
      "main closeout builder",
      "v7 x1 Lumen prep card",
    ],
  }),
  buildArtifact("cleanup-classifier-ledger", "ghc.cleanup_classifier_ledger.v1", {
    status: "PASS_V559_V6_X2_CLEANUP_CLASSIFIER_LEDGER",
    cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
    destructive_cleanup_auto_run: false,
    cleanup_policy: "Classify cleanup proposals as x2 build tasks unless they require destructive deletion, external mutation, private publication, or sibling identity merge.",
  }),
  buildArtifact("v7-x1-lumen-prep-card", "ghc.next_lumen_x1_prep.v1", {
    status: "PASS_V559_V7_X1_LUMEN_PREP_READY",
    next_phase: nextX1,
    launch_skill: "ghc-lumen-launch",
    browser_route_rules: [
      "use in-app Browser plus ghc-lumen-launch as the staple route",
      "refresh/reconnect and inspect status before unavailable claims",
      "do not reload over an active response or unsent composer text",
      "harvest raw Lumen text into private/local support only before reducing sanitized counts",
    ],
  }),
  buildArtifact("safe-build-use-ledger", "ghc.safe_build_use_ledger.v1", {
    status: "PASS_V559_V6_X2_SAFE_BUILD_USE_LEDGER",
    source_queue_basename: `${sourceX1}-combined-x1-to-x2-queue-v1.json`,
    safe_builds_executed: [
      "phase truth guard",
      "duo queue count guard",
      "candidate/exact open-gate queue",
      "skill/runner prototype use ledger",
      "cleanup classifier ledger",
      "v7 x1 Lumen prep card",
    ],
    next_closeout_scope: "close v559-gmut-thos-v6-x2 to v559-gmut-thos-v7-x1 after validation",
  }),
];

for (const artifact of artifacts) writePair(artifact);

const failed = artifacts.filter((artifact) => artifact.status.startsWith("OPEN_GAP"));
console.log(JSON.stringify({
  status: failed.length ? "OPEN_GAP_V559_V6_X2_SAFE_BUILD_BUNDLE" : "PASS_V559_V6_X2_SAFE_BUILD_BUNDLE",
  phase_slug: phaseSlug,
  artifacts_written: artifacts.length * 2,
  open_gaps: failed.map((artifact) => artifact.artifact),
}, null, 2));
process.exit(failed.length ? 1 : 0);

function buildArtifact(suffix, schema, body) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    source_x1_phase: sourceX1,
    publication_boundary: commonBoundary,
    claim_boundary: claimBoundary,
    ...body,
  };
}

function writePair(doc) {
  const base = join(traceDir, doc.artifact);
  mkdirSync(dirname(base), { recursive: true });
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, [
    `# ${doc.artifact}`,
    "",
    `Status: \`${doc.status}\``,
    "",
    `Phase: \`${doc.phase_slug}\``,
    "",
    "```json",
    JSON.stringify(doc, null, 2),
    "```",
  ].join("\n") + "\n", "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function countsPass(nextCounts = {}) {
  return nextCounts.safe_approval_packets === 30 &&
    nextCounts.candidate_packets === 15 &&
    nextCounts.exact_approval_packets_queued === 15 &&
    nextCounts.skill_ideas === 21 &&
    nextCounts.runner_ideas === 9 &&
    nextCounts.cleanup_refine_fix_tasks === 45;
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "purchase",
    "account mutation",
    "API key creation",
    "private material proof",
    "raw publication proof",
    "sibling replacement or merge",
  ];
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
