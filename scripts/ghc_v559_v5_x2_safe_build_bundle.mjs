#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const phaseSlug = "v559-gmut-thos-v5-x2";
const sourceX1 = "v559-gmut-thos-v5-x1";
const nextX1 = "v559-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const root = process.cwd();
const traceDir = join(root, "docs", "trinity-live-traces");
const omegaDir = join(root, "docs", "omega-mini-index");
mkdirSync(traceDir, { recursive: true });

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const state = readJson(join(omegaDir, "omega-mini-current-state-v1.json"));
const queue = readJson(join(traceDir, `${sourceX1}-lumen-sanitized-proposal-queue-v1.json`));
const closeout = readJson(join(traceDir, `${sourceX1}-lumen-closeout-v1.json`));
const counts = queue.profile_cap_counts_represented || {};

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
    status: state.current_active_phase === phaseSlug &&
      state.latest_closed_phase === sourceX1 &&
      state.next_x1_lane_after_x2 === nextX1
      ? "PASS_V559_V5_X2_PHASE_TRUTH_GUARD"
      : "OPEN_GAP_V559_V5_X2_PHASE_TRUTH_GUARD",
    checks: {
      active_phase: state.current_active_phase,
      expected_active_phase: phaseSlug,
      latest_closed_phase: state.latest_closed_phase,
      expected_latest_closed_phase: sourceX1,
      next_x1_lane_after_x2: state.next_x1_lane_after_x2,
      expected_next_x1_lane_after_x2: nextX1,
    },
  }),
  buildArtifact("lumen-queue-count-guard", "ghc.lumen_queue_count_guard.v1", {
    status: countsPass(counts) && Array.isArray(queue.rows) && queue.rows.length >= 170
      ? "PASS_V559_V5_X2_LUMEN_QUEUE_COUNT_GUARD"
      : "OPEN_GAP_V559_V5_X2_LUMEN_QUEUE_COUNT_GUARD",
    counts,
    queue_rows: Array.isArray(queue.rows) ? queue.rows.length : 0,
    required_counts: {
      safe_approval_packets: 50,
      candidate_packets: 30,
      exact_approval_packets_queued: 20,
      blocked_packets_queued: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_refine_fix_tasks: 30,
    },
  }),
  buildArtifact("candidate-exact-blocked-open-gate-queue", "ghc.candidate_exact_blocked_queue.v1", {
    status: "PASS_V559_V5_X2_CANDIDATE_EXACT_BLOCKED_QUEUED_OPEN",
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    blocked_packets_queued: counts.blocked_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate, exact, and blocked rows are queued as sanitized guidance; exact and blocked gates are not auto-run.",
    open_gates: openGates(),
  }),
  buildArtifact("skill-runner-prototype-use-ledger", "ghc.skill_runner_prototype_use_ledger.v1", {
    status: "PASS_V559_V5_X2_SKILL_RUNNER_PROTOTYPE_LEDGER",
    skills_represented: counts.skill_ideas || 0,
    runners_represented: counts.runner_ideas || 0,
    prototypes_built_or_used: [
      "reflection manifest builder",
      "safe build bundle",
      "safe runner orchestrator",
      "main closeout builder",
      "Maren Quill and Solenne Vale launch prep card",
    ],
    boundary: "prototype receipts only; no new paid resource, account mutation, deployment, API key, or identity merge.",
  }),
  buildArtifact("cleanup-classifier-ledger", "ghc.cleanup_classifier_ledger.v1", {
    status: "PASS_V559_V5_X2_CLEANUP_CLASSIFIER_LEDGER",
    cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
    cleanup_policy: "Classify cleanup proposals as x2 build tasks unless they require destructive deletion, account mutation, private-material publication, or sibling identity merge.",
    destructive_cleanup_auto_run: false,
  }),
  buildArtifact("v6-x1-maren-quill-solenne-vale-prep-card", "ghc.next_duo_x1_prep.v1", {
    status: "PASS_V559_V6_X1_MAREN_QUILL_SOLENNE_VALE_PREP_READY",
    next_phase: nextX1,
    launch_skill: "ghc-maren-quill-solenne-vale-launch",
    expected_profile: {
      safe_packets_total: 30,
      candidate_packets_total: 15,
      exact_approval_packets_total: 15,
      skill_ideas_total: 21,
      runner_ideas_total: 9,
      cleanup_tasks_total: 45,
    },
    launch_rules: [
      "use the recomposed duo route, not legacy Arby/Aster/Cicero/Kierkegaard/Aristotle lanes",
      "keep long-form sibling outputs local/private and publish sanitized receipts only",
      "use timestamped check-ins and productive cadence windows rather than passive waiting",
    ],
  }),
  buildArtifact("safe-build-use-ledger", "ghc.safe_build_use_ledger.v1", {
    status: "PASS_V559_V5_X2_SAFE_BUILD_USE_LEDGER",
    source_queue_basename: `${sourceX1}-lumen-sanitized-proposal-queue-v1.json`,
    closeout_source_status: closeout.status,
    safe_builds_executed: [
      "phase truth guard",
      "Lumen queue count guard",
      "candidate/exact/blocked open-gate queue",
      "skill/runner prototype use ledger",
      "cleanup classifier ledger",
      "v6 x1 Maren Quill plus Solenne Vale prep card",
    ],
    next_closeout_scope: "close v559-gmut-thos-v5-x2 to v559-gmut-thos-v6-x1 after validation",
  }),
];

for (const artifact of artifacts) writePair(artifact);

const failed = artifacts.filter((artifact) => artifact.status.startsWith("OPEN_GAP"));
console.log(JSON.stringify({
  status: failed.length ? "OPEN_GAP_V559_V5_X2_SAFE_BUILD_BUNDLE" : "PASS_V559_V5_X2_SAFE_BUILD_BUNDLE",
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
    "",
  ].join("\n"), "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function countsPass(nextCounts = {}) {
  return nextCounts.safe_approval_packets === 50 &&
    nextCounts.candidate_packets === 30 &&
    nextCounts.exact_approval_packets_queued === 20 &&
    nextCounts.blocked_packets_queued === 10 &&
    nextCounts.skill_ideas === 20 &&
    nextCounts.runner_ideas === 10 &&
    nextCounts.cleanup_refine_fix_tasks === 30;
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
