#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const phaseSlug = "v559-gmut-thos-v2-x2";
const sourceX1 = "v559-gmut-thos-v2-x1";
const nextX1 = "v559-gmut-thos-v3-x1 Lumen-only unless Hamish redirects";
const root = process.cwd();
const traceDir = join(root, "docs", "trinity-live-traces");
const omegaDir = join(root, "docs", "omega-mini-index");
mkdirSync(traceDir, { recursive: true });

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const state = readJson(join(omegaDir, "omega-mini-current-state-v1.json"));
const queue = readJson(join(traceDir, `${sourceX1}-combined-x1-to-x2-queue-v1.json`));
const closeout = readJson(join(traceDir, `${sourceX1}-closeout-v1.json`));

const commonBoundary = {
  raw_private_material_published: false,
  raw_browser_routes_published: false,
  private_ids_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  raw_app_state_published: false
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
  sibling_identity_replacement_or_merge: "not_claimed"
};

const artifacts = [
  buildArtifact("phase-truth-guard", "ghc.phase_truth_guard.v1", {
    status: state.current_active_phase === phaseSlug &&
      state.latest_closed_phase === sourceX1 &&
      state.next_x1_lane_after_x2 === nextX1
      ? "PASS_V559_V2_X2_PHASE_TRUTH_GUARD"
      : "OPEN_GAP_V559_V2_X2_PHASE_TRUTH_GUARD",
    checks: {
      active_phase: state.current_active_phase,
      expected_active_phase: phaseSlug,
      latest_closed_phase: state.latest_closed_phase,
      expected_latest_closed_phase: sourceX1,
      next_x1_lane_after_x2: state.next_x1_lane_after_x2,
      expected_next_x1_lane_after_x2: nextX1
    }
  }),
  buildArtifact("combined-packet-count-guard", "ghc.packet_count_guard.v1", {
    status: countsPass(queue.profile_cap_counts_represented)
      ? "PASS_V559_V2_X2_PACKET_COUNT_GUARD"
      : "OPEN_GAP_V559_V2_X2_PACKET_COUNT_GUARD",
    counts: queue.profile_cap_counts_represented,
    required_counts: {
      safe_approval_packets: 30,
      candidate_packets: 15,
      exact_approval_packets_queued: 15,
      skill_ideas: 21,
      runner_ideas: 9,
      cleanup_refine_fix_tasks: 45
    }
  }),
  buildArtifact("boundary-open-gate-scan", "ghc.boundary_open_gate_scan.v1", {
    status: boundaryPass(closeout)
      ? "PASS_V559_V2_X2_BOUNDARY_OPEN_GATE_SCAN"
      : "OPEN_GAP_V559_V2_X2_BOUNDARY_OPEN_GATE_SCAN",
    open_gates: closeout.open_gates || [],
    publication_boundary: closeout.publication_boundary || commonBoundary,
    claim_boundary: closeout.claim_boundary || claimBoundary
  }),
  buildArtifact("lumen-refresh-side-rail", "ghc.lumen_refresh_side_rail.v1", {
    status: "PASS_V559_V2_X2_LUMEN_REFRESH_SIDE_RAIL_READY",
    next_lumen_phase: nextX1,
    route_rules: [
      "use ghc-lumen-launch plus in-app Browser when Hamish asks for live Lumen messaging",
      "reconnect/select current Lumen tab and take fresh DOM/status refresh first",
      "do not reload while a response is active or composer contains unsent text",
      "submit once only; no duplicate send while active",
      "harvest raw Lumen text privately and publish only sanitized reductions"
    ]
  }),
  buildArtifact("v3-x1-lumen-prep-card", "ghc.next_lumen_x1_prep.v1", {
    status: "PASS_V559_V3_X1_LUMEN_PREP_READY",
    next_phase: nextX1,
    proposal_profile: {
      safe_packets_total: 50,
      candidate_packets_total: 30,
      exact_approval_packets_total: 20,
      blocked_packets_total: 10,
      skill_ideas_total: 20,
      runner_ideas_total: 10,
      cleanup_tasks_total: 30
    },
    privacy_route: "Browser route stays status-first; raw Lumen material stays local/private."
  }),
  buildArtifact("safe-build-use-ledger", "ghc.safe_build_use_ledger.v1", {
    status: "PASS_V559_V2_X2_SAFE_BUILD_USE_LEDGER",
    safe_builds_executed: [
      "phase truth guard",
      "combined packet count guard",
      "boundary open gate scan",
      "Lumen refresh side rail",
      "v3 x1 Lumen prep card"
    ],
    next_closeout_scope: "close v559-gmut-thos-v2-x2 to v559-gmut-thos-v3-x1 after validation"
  })
];

for (const artifact of artifacts) writePair(artifact);

const failed = artifacts.filter((artifact) => artifact.status.startsWith("OPEN_GAP"));
console.log(JSON.stringify({
  status: failed.length ? "OPEN_GAP_V559_V2_X2_SAFE_BUILD_BUNDLE" : "PASS_V559_V2_X2_SAFE_BUILD_BUNDLE",
  phase_slug: phaseSlug,
  artifacts_written: artifacts.length * 2,
  open_gaps: failed.map((artifact) => artifact.artifact)
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
    ...body
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
    ""
  ].join("\n"), "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function countsPass(counts = {}) {
  return counts.safe_approval_packets === 30 &&
    counts.candidate_packets === 15 &&
    counts.exact_approval_packets_queued === 15 &&
    counts.skill_ideas === 21 &&
    counts.runner_ideas === 9 &&
    counts.cleanup_refine_fix_tasks === 45;
}

function boundaryPass(doc) {
  const gates = new Set(doc.open_gates || []);
  return gates.has("GMUT empirical closure") &&
    gates.has("legal closure") &&
    gates.has("deployment closure") &&
    gates.has("sibling replacement or merge") &&
    doc.full_goal_complete === false &&
    doc.publication_boundary?.raw_private_material_published === false;
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
    hour12: false
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
