#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const sourceX1 = required("--source-x1");
const nextActivePhase = required("--next-active-phase");
const nextX2Scope = required("--next-x2-scope");
const nextX1LaneAfterX2 = required("--next-x1-after-x2");
const nextLaunchSkill = args.get("--next-launch-skill") || "not_recorded";
const nextLane = args.get("--next-lane") || nextActivePhase;
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
const counts = queue.expected_profile || queue.profile_cap_counts_represented || {};
const queueCounts = queue.queue_counts || {};
const rows = Array.isArray(queue.rows) ? queue.rows : [];

const artifacts = [
  buildArtifact("phase-truth-guard", "ghc.phase_truth_guard.v2", {
    status: state.current_active_phase === phaseSlug && state.latest_closed_phase === sourceX1
      ? "PASS_LUMEN_X2_PHASE_TRUTH_GUARD"
      : "OPEN_GAP_LUMEN_X2_PHASE_TRUTH_GUARD",
    checks: {
      active_phase: state.current_active_phase,
      expected_active_phase: phaseSlug,
      latest_closed_phase: state.latest_closed_phase,
      expected_latest_closed_phase: sourceX1,
    },
  }),
  buildArtifact("candidate-exact-blocked-open-gate-queue", "ghc.candidate_exact_blocked_queue.v2", {
    status: "PASS_CANDIDATE_EXACT_BLOCKED_QUEUED_OPEN",
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    blocked_packets_queued: counts.blocked_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate, exact, and blocked rows are queued as sanitized guidance; exact and blocked gates are not auto-run.",
    open_gates: openGates(),
  }),
  buildArtifact("skill-runner-prototype-use-ledger", "ghc.skill_runner_prototype_use_ledger.v2", {
    status: "PASS_SKILL_RUNNER_PROTOTYPE_LEDGER",
    skills_represented: counts.skill_ideas || 0,
    runners_represented: counts.runner_ideas || 0,
    prototypes_built_or_used: [
      "generic Lumen x1 private response reducer",
      "generic Lumen x1 closeout builder",
      "generic Lumen x2 reflection manifest builder",
      "generic Lumen x2 safe build bundle",
      "main closeout route registration",
    ],
    boundary: "prototype receipts only; no new paid resource, account mutation, deployment, API key, or identity merge.",
  }),
  buildArtifact("cleanup-classifier-ledger", "ghc.cleanup_classifier_ledger.v2", {
    status: "PASS_CLEANUP_CLASSIFIER_LEDGER",
    cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
    cleanup_policy: "Classify cleanup proposals as x2 build tasks unless they require destructive deletion, account mutation, private-material publication, or sibling identity merge.",
    destructive_cleanup_auto_run: false,
  }),
  buildArtifact("next-x1-prep-card", "ghc.next_x1_prep.v2", {
    status: "PASS_NEXT_X1_PREP_READY",
    next_phase: nextActivePhase,
    next_lane: nextLane,
    launch_skill: nextLaunchSkill,
    expected_profile: nextLaunchSkill === "ghc-lumen-launch"
      ? { safe_packets_total: 50, candidate_packets_total: 30, exact_packets_total: 20, blocked_packets_total: 10, skill_ideas_total: 20, runner_ideas_total: 10, cleanup_tasks_total: 30 }
      : { safe_packets_total: 30, candidate_packets_total: 15, exact_packets_total: 15, skill_ideas_total: 21, runner_ideas_total: 9, cleanup_tasks_total: 45 },
    launch_rules: [
      "use the active recomposed route only",
      "keep long-form sibling outputs local/private and publish sanitized receipts only",
      "use timestamped check-ins and productive cadence windows rather than passive waiting",
    ],
  }),
  buildArtifact("safe-build-use-ledger", "ghc.safe_build_use_ledger.v2", {
    status: "PASS_LUMEN_X2_SAFE_BUILD_USE_LEDGER",
    source_queue_basename: `${sourceX1}-lumen-sanitized-proposal-queue-v1.json`,
    source_closeout_status: closeout.status,
    queue_rows_represented: rows.length,
    immediate_x1_safe_rows_represented: queueCounts.by_execution_lane?.immediate_x1_safe || 0,
    x2_build_rows_represented: queueCounts.by_execution_lane?.x2_build_task || 0,
    safe_builds_executed: [
      "phase truth guard",
      "candidate/exact/blocked open-gate queue",
      "skill/runner prototype use ledger",
      "cleanup classifier ledger",
      "next x1 prep card",
    ],
    next_closeout_scope: `close ${phaseSlug} to ${nextActivePhase} after validation`,
  }),
];

for (const artifact of artifacts) writePair(artifact);
const failed = artifacts.filter((artifact) => artifact.status.startsWith("OPEN_GAP"));
console.log(JSON.stringify({
  status: failed.length ? "OPEN_GAP_LUMEN_X2_SAFE_BUILD_BUNDLE" : "PASS_LUMEN_X2_SAFE_BUILD_BUNDLE",
  phase_slug: phaseSlug,
  artifacts_written: artifacts.length * 2,
  open_gaps: failed.map((artifact) => artifact.artifact),
}, null, 2));
process.exit(failed.length ? 1 : 0);

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_lumen_x2_safe_build_bundle.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function buildArtifact(suffix, schema, body) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    source_x1_phase: sourceX1,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...body,
  };
}

function writePair(doc) {
  const base = join(traceDir, doc.artifact);
  mkdirSync(dirname(base), { recursive: true });
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, `# ${doc.artifact}\n\nStatus: \`${doc.status}\`\n\nPhase: \`${doc.phase_slug}\`\n\nBoundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.\n`, "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
  };
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
    sibling_identity_replacement_or_merge: "not_claimed",
  };
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
