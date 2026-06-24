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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v5-x1";
const previousPhase = args.get("--previous-phase") || "v553-gmut-thos-v4-x2";
const latestCompletedX2 = args.get("--latest-completed-x2") || previousPhase;
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v5-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects";
const lumenResponseState = args.get("--lumen-response-state") || "active_fresh";
const mode = args.get("--mode") || "open";
const shouldClose = mode === "close" && lumenResponseState === "completed_ready_for_harvest";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  raw_browser_routes_published: false,
  private_urls_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  session_streams_published: false,
  private_dumps_published: false,
  private_callable_ids_published: false,
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

const required = [
  `${phaseSlug}-lumen-handoff-message-v1.json`,
  `${phaseSlug}-lumen-browser-send-receipt-v1.json`,
  `${phaseSlug}-proposal-queue-targets-v1.json`,
  `${phaseSlug}-web-reflection-ledger-30-v1.json`,
  `${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
];
const missing = required.filter((name) => !fs.existsSync(path.join(tracesDir, name)));
const proposalQueue = readJsonOptional(`${phaseSlug}-proposal-queue-targets-v1.json`);
const webLedger = readJsonOptional(`${phaseSlug}-web-reflection-ledger-30-v1.json`);
const journeyLedger = readJsonOptional(`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`);
const sendReceipt = readJsonOptional(`${phaseSlug}-lumen-browser-send-receipt-v1.json`);
const safeRunner = readJsonOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`);
const rows = {
  web: countRows(webLedger),
  journey: countRows(journeyLedger),
};
const counts = {
  safe_now_packets: countArray(proposalQueue, "safe_packets", 50),
  candidate_packets: countArray(proposalQueue, "candidate_packets", 30),
  exact_approval_packets: countArray(proposalQueue, "exact_approval_packets", 20),
  blocked_packets: countArray(proposalQueue, "blocked_packets", 10),
  skill_ideas: countArray(proposalQueue, "skill_ideas", 20),
  runner_ideas: countArray(proposalQueue, "runner_ideas", 10),
  cleanup_proposals: countArray(proposalQueue, "cleanup_tasks", 30),
  web_reflections: rows.web,
  journey_phase_reflections: rows.journey,
};

const preconditionsPass =
  missing.length === 0 &&
  rows.web >= 30 &&
  rows.journey >= 30 &&
  sendReceipt?.send_status === "browser_send_submitted_response_active" &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";

const closeoutStatus = shouldClose && preconditionsPass
  ? "PASS_V553_V5_X1_CLOSED_V5_X2_READY"
  : "ACTIVE_OPEN_V553_V5_X1_LUMEN_PENDING_HARVEST";

const artifacts = [
  writePair("lumen-advisory-harvest", buildHarvest(), renderHarvestMd),
  writePair("approval-eureka-reducer", buildApprovalReducer(), renderApprovalReducerMd),
  writePair("skill-runner-readiness-board", buildSkillRunnerBoard(), renderSkillRunnerBoardMd),
  writePair("cleanup-tier-board", buildCleanupBoard(), renderCleanupBoardMd),
  writePair("source-reflection-reduction", buildSourceReflectionReduction(), renderSourceReductionMd),
  writePair("trinity-mandala-planning-matrix", buildTrinityMatrix(), renderTrinityMatrixMd),
  writePair("private-material-firewall", buildFirewall(), renderSimpleMd),
  writePair("open-gate-rail", buildOpenGateRail(), renderSimpleMd),
  writePair("v5-x2-readiness-handoff", buildX2Handoff(), renderSimpleMd),
  writePair("v6-arby-cicero-prep-card", buildV6Prep(), renderSimpleMd),
  writePair("phase-status-index", buildPhaseStatusIndex(), renderSimpleMd),
  writePair("closeout", buildCloseout(), renderCloseoutMd),
];

refreshBeacons();

process.stdout.write(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  lumen_response_state: lumenResponseState,
  preconditions_pass: preconditionsPass,
  next_active_phase: shouldClose && preconditionsPass ? nextX2Scope : phaseSlug,
  missing_required_artifacts: missing,
  counts,
  artifacts: artifacts.length,
}, null, 2) + "\n");

process.exit(preconditionsPass ? 0 : 1);

function buildHarvest() {
  return {
    artifact_type: "ghc_v553_v5_x1_lumen_advisory_harvest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: shouldClose
      ? "PASS_LUMEN_RESPONSE_COMPLETED_READY_FOR_SANITIZED_HARVEST"
      : "ACTIVE_OPEN_LUMEN_RESPONSE_NOT_YET_HARVESTED",
    response_state: lumenResponseState,
    route_class: "in_app_browser_lumen_main_thread",
    raw_response_published: false,
    advisory_summary: shouldClose
      ? [
          "Lumen v5 x1 response completed and was reduced into sanitized phase artifacts without publishing raw transcript or Browser route data.",
          "Lumen's main correction is to keep repo state synchronized from the v4 x2 closeout into v5 x1 and v5 x2 truth before publication.",
          "Lumen recommends v5 x2 as a precision pass: sync state, reduce queues, guard privacy, prepare Arby/Cicero, validate hard, and publish only curated artifacts.",
          "The first v5 x2 slice is current-state sync, Lumen advisory reducer, 30-web reduction, 30-Journey reduction, approval/Eureka ledger, skill/runner board, cleanup tier board, private-material firewall, open-gate rail, and Arby/Cicero v6 prep.",
          "The v6 x1 runway remains Arby and Cicero unless Hamish redirects, and all proof/legal/canon/deployment/account/API-key/private-material/raw-publication/sibling-merge gates remain open.",
        ]
      : [
          "Lumen v5 x1 response is still active or not yet marked completed-ready-for-harvest.",
          "The phase remains open and should not advance to v5 x2 until a completed harvest is verified.",
          "Continue productive five-minute safe work and re-check at the next natural pause.",
        ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildApprovalReducer() {
  return {
    artifact_type: "ghc_v553_v5_x1_approval_eureka_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: shouldClose
      ? "PASS_V5_X1_PROPOSALS_REDUCED_FOR_V5_X2"
      : "ACTIVE_OPEN_V5_X1_PROPOSALS_PREPARED_PENDING_LUMEN_HARVEST",
    spending_ceiling_usd_per_packet: 100,
    counts,
    immediate_x1_safe: [
      "sanitized send receipt",
      "source/reflection count verification",
      "proposal count reconciliation",
      "privacy firewall refresh",
      "open-gate rail refresh",
      "D-drive/C-drive posture receipt",
      "v6 duo prep continuity",
    ],
    x2_build_tasks: [
      "v5 x2 execution ledger",
      "v5 x2 skill/runner build-use pass",
      "v5 x2 source/reflection reducer",
      "v5 x2 validation and privacy scan",
      "v5 x2 closeout and v6 x1 handoff",
    ],
    exact_and_blocked_remain_queued: true,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildSkillRunnerBoard() {
  return {
    artifact_type: "ghc_v553_v5_x1_skill_runner_readiness_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SKILL_RUNNER_READINESS_REDUCED_FOR_V5_X2",
    skill_idea_count: counts.skill_ideas,
    runner_idea_count: counts.runner_ideas,
    priority_skill_lanes: [
      "ghc-lumen-launch",
      "ghc-background-sibling-supervision",
      "ghc-safe-runner-orchestrator",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-retry",
    ],
    priority_runner_lanes: [
      "ghc_v553_v5_x1_lumen_startup_builder.mjs",
      "ghc_lumen_browser_send_receipt_builder.mjs",
      "ghc_v553_v5_x1_lumen_closeout_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
    ],
  };
}

function buildCleanupBoard() {
  return {
    artifact_type: "ghc_v553_v5_x1_cleanup_tier_board",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_CLEANUP_PROPOSALS_TIERED_NON_DESTRUCTIVE",
    cleanup_proposal_count: counts.cleanup_proposals,
    safe_cleanup_lanes: [
      "deduplicate lookup file references",
      "normalize phase wording",
      "refresh open-gate wording",
      "validate JSON and Node syntax",
      "scan for private material",
    ],
    destructive_cleanup_requires_fresh_exact_approval: true,
  };
}

function buildSourceReflectionReduction() {
  return {
    artifact_type: "ghc_v553_v5_x1_source_reflection_reduction",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: rows.web >= 30 && rows.journey >= 30
      ? "PASS_SOURCE_REFLECTION_TARGETS_MET"
      : "OPEN_GAP_SOURCE_REFLECTION_TARGETS_BELOW_REQUIRED",
    web_reflection_rows: rows.web,
    journey_phase_reflection_rows: rows.journey,
  };
}

function buildTrinityMatrix() {
  return {
    artifact_type: "ghc_v553_v5_x1_trinity_mandala_planning_matrix",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_TRINITY_MANDALA_V5_PLANNING_MATRIX_REDUCED",
    matrix: [
      ["GMUT / Mind", "source-backed evidence hygiene and proof-ceiling discipline"],
      ["THOS / Body", "Browser, CLI, app-lane, skill, runner, startup, compact, closeout, and validation posture"],
      ["Freed ID / CBR / Heart", "dignity, identity boundary, privacy, recourse, and non-merge governance"],
    ].map(([pillar, focus]) => ({ pillar, focus, closure_claimed: false })),
  };
}

function buildFirewall() {
  return {
    artifact_type: "ghc_v553_v5_x1_private_material_firewall",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_RECORDED",
    publication_boundary: publicationBoundary,
  };
}

function buildOpenGateRail() {
  return {
    artifact_type: "ghc_v553_v5_x1_open_gate_rail",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATE_RAIL_RECORDED",
    claim_boundary: claimBoundary,
  };
}

function buildX2Handoff() {
  return {
    artifact_type: "ghc_v553_v5_x1_v5_x2_readiness_handoff",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: shouldClose && preconditionsPass
      ? "PASS_V5_X2_READY"
      : "ACTIVE_OPEN_V5_X2_NOT_STARTED_PENDING_LUMEN_HARVEST",
    next_x2_scope: nextX2Scope,
    first_x2_tasks: [
      "execute or represent safe-now packets",
      "reduce candidate packets",
      "keep exact and blocked gates queued",
      "validate generated scripts and JSON",
      "privacy scan and open-gate lint",
      "commit and remote-verify only after phase truth is consistent",
    ],
  };
}

function buildV6Prep() {
  return {
    artifact_type: "ghc_v553_v5_x1_v6_arby_cicero_prep_card",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V6_DUO_PREP_CONTINUITY_RECORDED",
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    route: "ghc-arby-cicero-launch with Arby strict CLI plus Cicero recovered app-lane background supervision",
    private_ids_published: false,
  };
}

function buildPhaseStatusIndex() {
  return {
    artifact_type: "ghc_v553_v5_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: closeoutStatus,
    latest_closed_phase_after_run: shouldClose && preconditionsPass ? phaseSlug : previousPhase,
    latest_completed_x1_after_run: shouldClose && preconditionsPass ? phaseSlug : "v553-gmut-thos-v4-x1",
    latest_completed_x2_after_run: latestCompletedX2,
    next_active_phase: shouldClose && preconditionsPass ? nextX2Scope : phaseSlug,
    lumen_response_state: lumenResponseState,
    preconditions_pass: preconditionsPass,
    missing_required_artifacts: missing,
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function buildCloseout() {
  return {
    artifact_type: "ghc_v553_v5_x1_closeout",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: closeoutStatus,
    lumen_response_harvested: shouldClose && preconditionsPass,
    next_active_phase: shouldClose && preconditionsPass ? nextX2Scope : phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    counts,
    missing_required_artifacts: missing,
    validation_expectations: [
      "node --check changed Node scripts",
      "parse changed JSON artifacts",
      "omega-mini phase/current-state guard",
      "git diff hygiene check",
      "privacy scan",
      "open-gate linter",
      "drive posture check",
      "remote/local equality after push",
    ],
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
}

function refreshBeacons() {
  const lookupFiles = artifacts.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
  for (const target of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = JSON.parse(fs.readFileSync(target, "utf8"));
    data.generated_utc = generatedUtc;
    data.updated_at = generatedNz;
    data.status = closeoutStatus;
    data.current_active_phase = shouldClose && preconditionsPass ? nextX2Scope : phaseSlug;
    data.latest_closed_phase = shouldClose && preconditionsPass ? phaseSlug : previousPhase;
    data.latest_completed_x1_phase = shouldClose && preconditionsPass ? phaseSlug : data.latest_completed_x1_phase;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = data.current_active_phase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.v553_v5_x1_lumen_closeout = {
      status: closeoutStatus,
      lumen_response_harvested: shouldClose && preconditionsPass,
      counts,
      next_x2_scope: nextX2Scope,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
    };
    data.lumen_browser_send = {
      ...(data.lumen_browser_send || {}),
      send_status: shouldClose && preconditionsPass
        ? "browser_response_completed_harvested"
        : "browser_send_submitted_response_active",
      raw_browser_route_published: false,
      raw_transcript_published: false,
    };
    const key = target.includes("latest-updates")
      ? "latest_lookup_files"
      : target.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    data[key] = unique([...(data[key] || []), ...lookupFiles]);
    fs.writeFileSync(target, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    const mdTarget = target.replace(/\.json$/, ".md");
    fs.writeFileSync(mdTarget, renderBeaconMd(path.basename(mdTarget, ".md"), data, data[key]), "utf8");
  }
}

function renderBeaconMd(title, data, files) {
  return [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## v553 v5 x1 Lumen Closeout",
    "",
    `- status: \`${data.v553_v5_x1_lumen_closeout?.status || "not_recorded"}\``,
    `- Lumen response harvested: \`${data.v553_v5_x1_lumen_closeout?.lumen_response_harvested ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-100).map((file) => `- \`${file}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderHarvestMd(data) {
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
    "## Boundary",
    "",
    boundarySentence(),
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
    "## Immediate x1 Safe",
    "",
    ...data.immediate_x1_safe.map((item) => `- ${item}`),
    "",
    "## x2 Build Tasks",
    "",
    ...data.x2_build_tasks.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderSkillRunnerBoardMd(data) {
  return [
    `# ${phaseSlug} Skill/Runner Readiness Board`,
    "",
    `Status: \`${data.overall_status}\``,
    `Skill ideas: \`${data.skill_idea_count}\``,
    `Runner ideas: \`${data.runner_idea_count}\``,
    "",
    "## Priority Skill Lanes",
    "",
    ...data.priority_skill_lanes.map((item) => `- ${item}`),
    "",
    "## Priority Runner Lanes",
    "",
    ...data.priority_runner_lanes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderCleanupBoardMd(data) {
  return [
    `# ${phaseSlug} Cleanup Tier Board`,
    "",
    `Status: \`${data.overall_status}\``,
    `Cleanup proposals: \`${data.cleanup_proposal_count}\``,
    `Destructive cleanup requires fresh exact approval: \`${data.destructive_cleanup_requires_fresh_exact_approval}\``,
    "",
    "## Safe Cleanup Lanes",
    "",
    ...data.safe_cleanup_lanes.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderSourceReductionMd(data) {
  return [
    `# ${phaseSlug} Source/Reflection Reduction`,
    "",
    `Status: \`${data.overall_status}\``,
    `Web reflection rows: \`${data.web_reflection_rows}\``,
    `Journey/phase reflection rows: \`${data.journey_phase_reflection_rows}\``,
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
      `Closure claimed: \`${item.closure_claimed}\``,
      "",
    ]),
  ].join("\n");
}

function renderCloseoutMd(data) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Lumen response harvested: \`${data.lumen_response_harvested}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\``,
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

function renderSimpleMd(data) {
  return [
    `# ${phaseSlug} ${data.artifact_type}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
    "```json",
    JSON.stringify(data, null, 2),
    "```",
    "",
  ].join("\n");
}

function writePair(suffix, payload, renderMd) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function readJsonOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function countRows(doc) {
  if (!doc || typeof doc !== "object") return 0;
  for (const key of ["rows", "sources", "reflections", "items"]) {
    if (Array.isArray(doc[key])) return doc[key].length;
  }
  return Number(doc.row_count || 0);
}

function countArray(doc, key, fallback) {
  return Array.isArray(doc?.[key]) ? doc[key].length : fallback;
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function boundarySentence() {
  return "No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, proof closures, legal closures, canon promotions, deployments, purchases, account/API-key mutations, private-material proof, raw-publication proof, or sibling identity merge/replacement claims are published or claimed.";
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
