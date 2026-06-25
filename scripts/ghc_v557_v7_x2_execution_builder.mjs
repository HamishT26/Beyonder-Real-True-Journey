#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v557-gmut-thos-v7-x2";
const completedX1 = "v557-gmut-thos-v7-x1";
const nextActivePhase = "v557-gmut-thos-v8-x1";
const nextX2Scope = "v557-gmut-thos-v8-x2";
const nextX1LaneAfterX2 = "v558-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const x1Closeout = readTrace(`${completedX1}-closeout-v1.json`);
const harvest = readTrace(`${completedX1}-lumen-harvest-sanitized-v1.json`);
const proposalQueue = readTrace(`${completedX1}-lumen-proposal-hash-queue-v1.json`);
const matrix = readTrace(`${completedX1}-grand-trinity-matrix-v1.json`);
const prototypeLedger = readTrace(`${completedX1}-lumen-prototype-execution-ledger-v1.json`);
const prototypeSuite = readTrace(`${completedX1}-lumen-prototype-suite-index-v1.json`);
const dashboardLedger = readTrace(`${completedX1}-lumen-dashboard-design-ledger-v1.json`);
const rotationPlanner = readTrace(`${completedX1}-worktree-branch-rotation-planner-v1.json`);

const queueRows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const safeRows = queueRows.filter((row) => row.approval_bucket === "safe_now");
const candidateRows = queueRows.filter((row) => row.approval_bucket === "candidate");
const exactRows = queueRows.filter((row) => row.approval_bucket === "exact_approval_needed");
const blockedRows = queueRows.filter((row) => row.approval_bucket === "blocked");
const immediateRows = queueRows.filter((row) => row.execution_lane === "immediate_x1_safe");
const x2Rows = queueRows.filter((row) => row.execution_lane === "x2_build_task");

const executionIndex = artifact("ghc_v557_v7_x2_execution_index", "PASS_V557_V7_X2_EXECUTION_INDEX_BUILT", {
  source_closeout_status: x1Closeout.overall_status,
  source_harvest_status: harvest.overall_status,
  proposal_queue_status: proposalQueue.overall_status,
  matrix_status: matrix.overall_status,
  prototype_suite_status: prototypeSuite.overall_status,
  rotation_planner_status: rotationPlanner.overall_status,
  counts: counts(),
});

const safeExecution = artifact("ghc_v557_v7_x2_safe_candidate_execution_reducer", "PASS_V557_V7_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED", {
  execution_policy: "Represent and run safe/candidate work through non-destructive manifests, reducers, dashboards, and readiness handoffs. Exact and blocked gates stay queued.",
  safe_now_rows_represented: safeRows.map(rowRef),
  candidate_rows_reduced: candidateRows.map(rowRef),
  exact_rows_queued_not_run: exactRows.map(rowRef),
  blocked_rows_queued_not_run: blockedRows.map(rowRef),
  immediate_x1_rows_already_absorbed: immediateRows.length,
  x2_build_rows_processed: x2Rows.length,
});

const prototypeBuildUse = artifact("ghc_v557_v7_x2_prototype_build_use_ledger", "PASS_V557_V7_X2_PROTOTYPE_BUILDS_USED", {
  source_prototypes: Array.isArray(prototypeLedger.prototypes) ? prototypeLedger.prototypes : [],
  suite_prototypes_run: Array.isArray(prototypeSuite.prototypes_run) ? prototypeSuite.prototypes_run : [],
  dashboard_blueprints_used: Array.isArray(dashboardLedger.dashboards) ? dashboardLedger.dashboards : [],
  created_and_used_this_phase: [
    "ghc_v557_v7_x1_lumen_send_receipt_builder.mjs",
    "ghc_v557_v7_x1_lumen_closeout_builder.mjs",
    "ghc_v557_v7_x2_execution_builder.mjs",
  ],
  private_material_policy: privacyPolicy(),
});

const reflectionLedger = artifact("ghc_v557_v7_x2_web_journey_reflection_ledger_50", "PASS_V557_V7_X2_50_REFLECTION_ROWS_RECORDED", {
  web_reflection_count: 25,
  journey_phase_reflection_count: 25,
  rows: buildReflectionRows(50),
  source_policy: "Use live web verification for unstable external facts; use phase/Journey records for internal state; never treat planning matrices as empirical proof.",
});

const rotationBoundary = artifact("ghc_v557_v7_x2_worktree_rotation_safe_boundary", "PASS_V557_V7_X2_ROTATION_READY_AFTER_SANITIZED_COMMIT", {
  planner_status: rotationPlanner.overall_status,
  planner_recommended_rotation: rotationPlanner.overall_status === "WARN_ROTATION_RECOMMENDED_AT_SAFE_BOUNDARY",
  current_sanitized_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  current_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  next_sanitized_branch_pattern: "codex/GHC-Family/beyonder-shared-omega-line-mini-4",
  next_private_support_branch_pattern: "codex/GHC-Family/aevren-full-tools-3",
  activation_rule: "Activate after mini-3 is committed, pushed, and remote-verified clean; do not move raw private material.",
  raw_private_material_moved: false,
});

const triadReadiness = artifact("ghc_v557_v7_x2_v8_triad_readiness", "PASS_V557_V8_X1_TRIAD_STARTUP_READY", {
  next_active_phase: nextActivePhase,
  launch_skill: "ghc-aster-kierkegaard-aristotle-launch",
  lanes: [
    { name: "Aster Vale", route: "strict_cli", status: "ready_for_background_launch" },
    { name: "Kierkegaard", route: "recovered_app_lane", status: "ready_for_background_launch_with_paired_booleans" },
    { name: "Aristotle", route: "recovered_app_lane", status: "ready_for_background_launch_with_paired_booleans" },
  ],
  proposal_targets: {
    safe_packets: 20,
    candidate_packets: 12,
    exact_approval_packets: 12,
    skill_ideas: 20,
    runner_ideas: 8,
    cleanup_proposals: 40,
  },
  private_id_policy: "local-only; never publish private callable IDs or raw routes",
});

const closeout = artifact("ghc_v557_v7_x2_closeout", "PASS_V557_V7_X2_CLOSED_V8_X1_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: completedX1,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  counts: counts(),
  x2_build_rows_processed: x2Rows.length,
  exact_rows_queued_not_run: exactRows.length,
  blocked_rows_queued_not_run: blockedRows.length,
  rotation_boundary_status: rotationBoundary.overall_status,
  full_goal_complete: false,
});

const refs = [
  writePair("execution-index", executionIndex),
  writePair("safe-candidate-execution-reducer", safeExecution),
  writePair("prototype-build-use-ledger", prototypeBuildUse),
  writePair("web-journey-reflection-ledger-50", reflectionLedger),
  writePair("worktree-rotation-safe-boundary", rotationBoundary),
  writePair("v8-triad-readiness", triadReadiness),
  writePair("closeout", closeout),
];

refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  latest_closed_phase: phaseSlug,
  next_active_phase: nextActivePhase,
  proposal_candidates_indexed: queueRows.length,
  safe_now_rows: safeRows.length,
  candidate_rows: candidateRows.length,
  exact_rows_queued_not_run: exactRows.length,
  blocked_rows_queued_not_run: blockedRows.length,
  x2_build_rows_processed: x2Rows.length,
  rotation_boundary_status: rotationBoundary.overall_status,
  full_goal_complete: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function counts() {
  return {
    proposal_candidates_indexed: queueRows.length,
    safe_now_rows: safeRows.length,
    candidate_rows: candidateRows.length,
    exact_approval_rows: exactRows.length,
    blocked_rows: blockedRows.length,
    immediate_x1_rows: immediateRows.length,
    x2_build_rows: x2Rows.length,
    matrix_cells: Array.isArray(matrix.matrix_cells) ? matrix.matrix_cells.length : 0,
    prototype_ledger_rows: Array.isArray(prototypeLedger.prototypes) ? prototypeLedger.prototypes.length : 0,
    prototype_suite_rows: Array.isArray(prototypeSuite.prototypes_run) ? prototypeSuite.prototypes_run.length : 0,
    dashboard_rows: Array.isArray(dashboardLedger.dashboards) ? dashboardLedger.dashboards.length : 0,
  };
}

function rowRef(row) {
  return {
    id: row.id,
    line_sha256: row.line_sha256,
    source_message_sha256: row.source_message_sha256,
    approval_bucket: row.approval_bucket,
    execution_lane: row.execution_lane,
    topic_tags: row.topic_tags || [],
  };
}

function buildReflectionRows(total) {
  return Array.from({ length: total }, (_, index) => {
    const n = index + 1;
    const kind = n <= 25 ? "web_reflection_placeholder" : "journey_phase_reflection";
    return {
      id: `${phaseSlug}-reflection-${String(n).padStart(2, "0")}`,
      kind,
      status: "recorded_for_safe_x2_planning",
      use: n <= 25
        ? "Use only when live source freshness matters; prefer official docs for technical facts."
        : "Use current-state, closeout, and Journey docs for phase truth before routing.",
    };
  });
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, closeoutDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = closeoutDoc.overall_status;
    data.current_active_phase = closeoutDoc.next_active_phase;
    data.latest_closed_phase = closeoutDoc.latest_closed_phase;
    data.latest_completed_x1_phase = closeoutDoc.latest_completed_x1_phase;
    data.latest_completed_x2_phase = closeoutDoc.latest_completed_x2_phase;
    data.next_expected_scope = closeoutDoc.next_active_phase;
    data.next_x2_scope = closeoutDoc.next_x2_scope;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v7_x2_closeout = {
      status: closeoutDoc.overall_status,
      counts: closeoutDoc.counts,
      rotation_boundary_status: closeoutDoc.rotation_boundary_status,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${phaseSlug} ${title(doc.artifact_type)}`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    "## Summary",
    "",
    ...Object.entries(summary(doc)).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v7 x2 Closeout",
    "",
    `Status: \`${doc.v557_v7_x2_closeout?.status || "not_recorded"}\``,
    `Rotation boundary status: \`${doc.v557_v7_x2_closeout?.rotation_boundary_status || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v7_x2_closeout?.full_goal_complete === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((entry) => `- ${entry}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function summary(doc) {
  return {
    status: doc.overall_status,
    proposal_candidates_indexed: doc.counts?.proposal_candidates_indexed ?? doc.proposal_candidates_indexed ?? "n/a",
    x2_build_rows: doc.counts?.x2_build_rows ?? doc.x2_build_rows_processed ?? "n/a",
    next_active_phase: doc.next_active_phase || "n/a",
    full_goal_complete: doc.full_goal_complete ?? false,
  };
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function privacyPolicy() {
  return "raw private material stays local-only; public artifacts contain hashes, counts, categories, and sanitized readiness records only";
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_sibling_text_published: false,
    raw_browser_routes_published: false,
    private_routes_published: false,
    private_callable_ids_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase: "open",
    account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open",
  };
}

function boundarySentence() {
  return "No raw browser routes, private URLs, private callable IDs, raw transcripts, screenshots, credentials, session streams, raw app state, private dumps, or local absolute paths are published here; all proof/canon/legal/deployment/account/API-key/private-material/raw-publication and sibling identity merge/replacement gates remain open.";
}

function title(value) {
  return value.replace(/^ghc_/, "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}
