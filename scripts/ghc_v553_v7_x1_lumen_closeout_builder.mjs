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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v7-x1";
const previousPhase = args.get("--previous-phase") || "v553-gmut-thos-v6-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v553-gmut-thos-v6-x1";
const latestCompletedX2 = args.get("--latest-completed-x2") || previousPhase;
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v7-x2";
const nextX1LaneAfterX2 = args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const responseState = args.get("--lumen-response-state") || "active_fresh";
const mode = args.get("--mode") || "open";
const shouldClose = mode === "close" && responseState === "completed_ready_for_harvest";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

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

const counts = {
  safe_now_packets: countArray(proposalQueue, "safe_packets", 50),
  candidate_packets: countArray(proposalQueue, "candidate_packets", 30),
  exact_approval_packets: countArray(proposalQueue, "exact_approval_packets", 20),
  blocked_packets: countArray(proposalQueue, "blocked_packets", 10),
  skill_ideas: countArray(proposalQueue, "skill_ideas", 20),
  runner_ideas: countArray(proposalQueue, "runner_ideas", 10),
  cleanup_proposals: countArray(proposalQueue, "cleanup_tasks", 30),
  web_reflections: countRows(webLedger),
  journey_phase_reflections: countRows(journeyLedger),
};

const preconditionsPass =
  missing.length === 0 &&
  counts.web_reflections >= 30 &&
  counts.journey_phase_reflections >= 30 &&
  sendReceipt?.send_status === "browser_send_submitted_response_active" &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";

const status = shouldClose && preconditionsPass
  ? "PASS_V553_V7_X1_CLOSED_V7_X2_READY"
  : "ACTIVE_OPEN_V553_V7_X1_LUMEN_PENDING_HARVEST";

const harvest = {
  artifact_type: "ghc_v553_v7_x1_lumen_advisory_harvest",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: shouldClose
    ? "PASS_LUMEN_RESPONSE_COMPLETED_READY_FOR_SANITIZED_HARVEST"
    : "ACTIVE_OPEN_LUMEN_RESPONSE_NOT_YET_HARVESTED",
  response_state: responseState,
  route_class: "in_app_browser_lumen_main_thread",
  raw_response_published: false,
  advisory_summary: shouldClose
    ? [
        "Lumen v7 x1 response completed and was reduced into sanitized phase artifacts without publishing raw transcript or Browser route data.",
        "Lumen's current guidance is treated as a planning and queue-shaping input, not as proof/canon/legal/deployment closure.",
        "The v7 x2 runway remains a safe build/use/validate/publish phase for already-authorized local work.",
        "The next grouped x1 lane after v7 x2 is the triad profile with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects.",
      ]
    : [
        "Lumen v7 x1 response is still active or not yet marked completed-ready-for-harvest.",
        "The phase remains open and must not advance to v7 x2 until the harvest is verified.",
        "Continue productive five-minute safe work and re-check at the next natural pause.",
      ],
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const artifacts = [
  writePair("lumen-advisory-harvest", harvest, renderHarvestMd(harvest)),
  writePair("approval-eureka-reducer", reducerArtifact(), renderReducerMd(reducerArtifact())),
  writePair("skill-runner-readiness-board", skillRunnerArtifact(), renderSimpleMd("Skill Runner Readiness Board", skillRunnerArtifact())),
  writePair("cleanup-tier-board", cleanupArtifact(), renderSimpleMd("Cleanup Tier Board", cleanupArtifact())),
  writePair("trinity-mandala-planning-matrix", trinityArtifact(), renderSimpleMd("Trinity Mandala Planning Matrix", trinityArtifact())),
  writePair("private-material-firewall", firewallArtifact(), renderSimpleMd("Private Material Firewall", firewallArtifact())),
  writePair("open-gate-rail", openGateArtifact(), renderSimpleMd("Open Gate Rail", openGateArtifact())),
  writePair("v7-x2-readiness-handoff", x2Handoff(), renderSimpleMd("v7 x2 Readiness Handoff", x2Handoff())),
  writePair("v8-triad-prep-card", v8PrepCard(), renderSimpleMd("v8 Triad Prep Card", v8PrepCard())),
  writePair("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
  writePair("closeout", closeoutArtifact(), renderCloseoutMd(closeoutArtifact())),
];

refreshBeacons();

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  lumen_response_state: responseState,
  preconditions_pass: preconditionsPass,
  next_active_phase: shouldClose && preconditionsPass ? nextX2Scope : phaseSlug,
  missing_required_artifacts: missing,
  counts,
  artifacts: artifacts.length,
}, null, 2));

function reducerArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_approval_eureka_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: shouldClose
      ? "PASS_V7_X1_PROPOSALS_REDUCED_FOR_V7_X2"
      : "ACTIVE_OPEN_V7_X1_PROPOSALS_PREPARED_PENDING_LUMEN_HARVEST",
    spending_ceiling_usd_per_packet: 100,
    counts,
    exact_and_blocked_remain_queued: true,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function skillRunnerArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_skill_runner_readiness_board",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_SKILL_RUNNER_READINESS_REDUCED_FOR_V7_X2",
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
  };
}

function cleanupArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_cleanup_tier_board",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_CLEANUP_PROPOSALS_TIERED_NON_DESTRUCTIVE",
    cleanup_proposal_count: counts.cleanup_proposals,
    destructive_cleanup_requires_fresh_exact_approval: true,
  };
}

function trinityArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_trinity_mandala_planning_matrix",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_TRINITY_MANDALA_V7_PLANNING_MATRIX_REDUCED",
    matrix: [
      { pillar: "GMUT / Mind", focus: "source-backed evidence hygiene and proof-ceiling discipline", closure_claimed: false },
      { pillar: "THOS / Body", focus: "Browser, CLI, app-lane, runner, startup, compact, closeout, and validation posture", closure_claimed: false },
      { pillar: "Freed ID / CBR / Heart", focus: "dignity, identity boundary, privacy, recourse, and non-merge governance", closure_claimed: false },
    ],
  };
}

function firewallArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_private_material_firewall",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_RECORDED",
    publication_boundary: publicationBoundary(),
  };
}

function openGateArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_open_gate_rail",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATE_RAIL_RECORDED",
    claim_boundary: claimBoundary(),
  };
}

function x2Handoff() {
  return {
    artifact_type: "ghc_v553_v7_x1_v7_x2_readiness_handoff",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: shouldClose && preconditionsPass
      ? "PASS_V7_X2_READY"
      : "ACTIVE_OPEN_V7_X2_NOT_STARTED_PENDING_LUMEN_HARVEST",
    next_x2_scope: nextX2Scope,
  };
}

function v8PrepCard() {
  return {
    artifact_type: "ghc_v553_v7_x1_v8_triad_prep_card",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V8_TRIAD_PREP_CONTINUITY_RECORDED",
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    private_ids_published: false,
  };
}

function closeoutArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_closeout",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    lumen_response_harvested: shouldClose && preconditionsPass,
    next_active_phase: shouldClose && preconditionsPass ? nextX2Scope : phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    counts,
    missing_required_artifacts: missing,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function phaseStatusIndex() {
  const closed = shouldClose && preconditionsPass;
  return {
    artifact_type: "ghc_v553_v7_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    latest_closed_phase: closed ? phaseSlug : previousPhase,
    latest_completed_x1_phase: closed ? phaseSlug : latestCompletedX1,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: closed ? nextX2Scope : phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    closeout_allowed_now: closed,
    closeout_blocker: closed ? null : "Lumen response has not yet reached completed-ready-for-harvest with all closeout preconditions passing.",
    lumen_response_harvested: closed,
    missing_required_artifacts: missing,
    counts,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
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
    const data = readJson(target);
    data.generated_utc = generatedUtc;
    if (target.endsWith("omega-mini-current-state-v1.json")) data.updated_at = generatedNz;
    data.status = status;
    data.current_active_phase = shouldClose && preconditionsPass ? nextX2Scope : phaseSlug;
    data.latest_closed_phase = shouldClose && preconditionsPass ? phaseSlug : previousPhase;
    data.latest_completed_x1_phase = shouldClose && preconditionsPass ? phaseSlug : latestCompletedX1;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = data.current_active_phase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.v553_v7_x1_lumen_closeout = {
      status,
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
    writeJson(target, data);
    writeMdBeacon(target, data, data[key]);
  }
}

function writeMdBeacon(jsonPath, data, files) {
  const mdPath = jsonPath.replace(/\.json$/, ".md");
  const title = jsonPath.includes("latest-updates") ? "Omega-Mini Latest Updates Beacon" :
    jsonPath.includes("ghc-current-state") ? "GHC Current State Beacon" :
      "Omega-Mini Current State";
  fs.writeFileSync(mdPath, [
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
    "## v553 v7 x1 Lumen Closeout",
    "",
    `- status: \`${data.v553_v7_x1_lumen_closeout?.status || "not_recorded"}\``,
    `- Lumen response harvested: \`${data.v553_v7_x1_lumen_closeout?.lumen_response_harvested ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-100).map((file) => `- \`${file}\``),
    "",
  ].join("\n"), "utf8");
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
  ].join("\n");
}

function renderReducerMd(data) {
  return [
    `# ${phaseSlug} Approval/Eureka Reducer`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function renderCloseoutMd(data) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Lumen response harvested: \`${data.lumen_response_harvested}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
  ].join("\n");
}

function renderSimpleMd(title, data) {
  return [
    `# ${title}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "```json",
    JSON.stringify(data, null, 2),
    "```",
    "",
  ].join("\n");
}

function writePair(suffix, payload, md) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function readJsonOptional(name) {
  try {
    return readJson(path.join(tracesDir, name));
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function countRows(doc) {
  if (!doc || typeof doc !== "object") return 0;
  if (Array.isArray(doc.rows)) return doc.rows.length;
  if (Array.isArray(doc.reflections)) return doc.reflections.length;
  return Number(doc.row_count || doc.reflection_count || 0);
}

function countArray(doc, key, fallback) {
  return Array.isArray(doc?.[key]) ? doc[key].length : fallback;
}

function publicationBoundary() {
  return {
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
}

function claimBoundary() {
  return {
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

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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

function parseArgs(raw) {
  const parsed = new Map();
  for (let index = 0; index < raw.length; index += 2) {
    parsed.set(raw[index], raw[index + 1]);
  }
  return parsed;
}
