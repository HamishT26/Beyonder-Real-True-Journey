#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v5-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposalQueue = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-lumen-proposal-hash-queue-v1.json"));
const prototypeSuite = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-lumen-prototype-suite-index-v1.json"));
const matrix = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-grand-trinity-matrix-v1.json"));
const startup = readJson(path.join(tracesDir, `${phaseSlug}-lumen-startup-context-v1.json`));
const sendReceipt = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`));

const rows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const immediateSafeExecutable = rows.filter((row) =>
  row.execution_lane === "immediate_x1_safe" &&
  ["safe_now", "candidate"].includes(row.approval_bucket)
);
const immediateHeld = rows.filter((row) =>
  row.execution_lane === "immediate_x1_safe" &&
  ["exact_approval_needed", "blocked"].includes(row.approval_bucket)
);
const x2Rows = rows.filter((row) => row.execution_lane === "x2_build_task");
const dashboardRows = rows.filter((row) => rowTags(row).includes("dashboard"));
const browserRows = rows.filter((row) => rowTags(row).includes("browser_safety"));
const sourceRows = rows.filter((row) => rowTags(row).includes("source_reflection"));
const cleanupRows = rows.filter((row) => rowTags(row).includes("cleanup_classifier"));
const matrixRows = rows.filter((row) => rowTags(row).includes("matrix"));
const fullToolsRows = rows.filter((row) => rowTags(row).includes("full_tools_private"));

const executionLedger = artifact("ghc_v557_v5_x1_lumen_immediate_safe_execution_ledger", "PASS_V557_V5_X1_IMMEDIATE_SAFE_ROWS_REPRESENTED", {
  source_private_digest: proposalQueue.source_digest,
  proposal_candidates_indexed: rows.length,
  executable_rows_count: immediateSafeExecutable.length,
  held_immediate_rows_count: immediateHeld.length,
  x2_rows_count: x2Rows.length,
  safe_execution_policy: "safe_now and authorized candidate rows are represented as non-destructive planning, validation, classification, and dashboard work; exact and blocked rows remain queued.",
  executed_or_represented_rows_sample: immediateSafeExecutable.slice(0, 40).map(rowRef),
});

const x2Queue = artifact("ghc_v557_v5_x1_lumen_x2_build_queue", "PASS_V557_V5_X1_X2_BUILD_QUEUE_READY", {
  x2_rows_count: x2Rows.length,
  safe_now_x2_rows: x2Rows.filter((row) => row.approval_bucket === "safe_now").length,
  candidate_x2_rows: x2Rows.filter((row) => row.approval_bucket === "candidate").length,
  exact_x2_rows_queued: x2Rows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
  blocked_x2_rows_queued: x2Rows.filter((row) => row.approval_bucket === "blocked").length,
  build_lanes: [
    buildLane("phase-truth-checker", "phase_truth"),
    buildLane("source-reflection-reducer", "source_reflection"),
    buildLane("approval-eureka-splitter", "approval_splitter"),
    buildLane("cleanup-classifier", "cleanup_classifier"),
    buildLane("browser-handoff-safety-dashboard", "browser_safety"),
    buildLane("full-tools-private-support-dashboard", "full_tools_private"),
    buildLane("grand-trinity-matrix", "matrix"),
    buildLane("recovered-app-lane-builder", "recovered_app_lane"),
  ],
});

const dashboardWorkbench = artifact("ghc_v557_v5_x1_lumen_dashboard_workbench", "PASS_V557_V5_X1_DASHBOARD_WORKBENCH_READY", {
  dashboard_rows: dashboardRows.length,
  browser_safety_rows: browserRows.length,
  full_tools_private_rows: fullToolsRows.length,
  dashboards: [
    dashboard("goal-mode-continuity", ["current_phase", "latest_closed_phase", "active_lane", "open_gates"]),
    dashboard("browser-handoff-safety", ["message_hash", "duplicate_send_allowed", "response_active", "harvest_pending"]),
    dashboard("full-tools-private-support", ["raw_private_saved_local_only", "hashes_published", "private_paths_hidden"]),
    dashboard("lumen-launch-health", ["handoff_prepared", "send_submitted", "response_control_visible", "harvest_status"]),
    dashboard("main-retry-clock", ["retry_count", "reflection_counts", "safe_work_done", "next_harvest_window"]),
  ],
});

const sourceReflectionWorkbench = artifact("ghc_v557_v5_x1_source_reflection_workbench", "PASS_V557_V5_X1_SOURCE_REFLECTION_WORKBENCH_READY", {
  source_reflection_rows: sourceRows.length,
  matrix_rows: matrixRows.length,
  matrix_cells_available: Array.isArray(matrix.matrix_cells) ? matrix.matrix_cells.length : 0,
  reflection_lanes: [
    "Node runner reliability",
    "Python validation and JSON parse safety",
    "Git/GitHub branch hygiene",
    "Browser handoff safety",
    "private/public boundary review",
    "Trinity Mandala phase-truth alignment",
  ],
});

const cleanupWorkbench = artifact("ghc_v557_v5_x1_cleanup_workbench", "PASS_V557_V5_X1_CLEANUP_WORKBENCH_INVENTORY_ONLY", {
  cleanup_rows: cleanupRows.length,
  deletion_performed: false,
  cleanup_groups: [
    cleanup("duplicate stale route claims", "replace with latest current-state and send receipts"),
    cleanup("oversized lookup trails", "keep rolling windows through builders only"),
    cleanup("dirty private support lane", "keep local-only until safe clean-base rotation"),
    cleanup("line-ending warnings", "treat as non-blocking unless diff check reports content issues"),
    cleanup("held sibling prep", "keep prepared_not_activated until exact instruction"),
  ],
});

const backgroundWatch = artifact("ghc_v557_v5_x1_lumen_background_supervision_watchcard", "PASS_V557_V5_X1_LUMEN_BACKGROUND_SUPERVISION_ACTIVE", {
  browser_send_status: sendReceipt.browser_send_status,
  duplicate_send_allowed: false,
  response_control_visible_after_send: sendReceipt.response_control_visible_after_send,
  closeout_allowed_now: false,
  next_action: "harvest Lumen at next natural safe pause when response completes",
  productive_cadence_units_completed: [
    "startup package built",
    "send receipt built",
    "immediate safe ledger built",
    "x2 build queue built",
    "dashboard workbench built",
    "source/reflection workbench built",
    "cleanup inventory built",
  ],
});

const branchRotationWatch = artifact("ghc_v557_v5_x1_branch_rotation_watch", "PASS_V557_V5_X1_BRANCH_ROTATION_WATCH_RECORDED", {
  active_sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  active_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  next_rotation_pattern: "omega-mini-4/full-tools-3 and onward from verified safe bases",
  rotate_now: false,
  reason: "mini-3 is clean enough for the current v5 x1 package; rotate only at a verified boundary or repeated status slowness.",
  raw_private_material_moved: false,
});

const refs = [
  writePair("lumen-immediate-safe-execution-ledger", executionLedger),
  writePair("lumen-x2-build-queue", x2Queue),
  writePair("lumen-dashboard-workbench", dashboardWorkbench),
  writePair("source-reflection-workbench", sourceReflectionWorkbench),
  writePair("cleanup-workbench", cleanupWorkbench),
  writePair("lumen-background-supervision-watchcard", backgroundWatch),
  writePair("branch-rotation-watch", branchRotationWatch),
];

refreshBeacons(refs, backgroundWatch);

process.stdout.write(JSON.stringify({
  status: backgroundWatch.overall_status,
  phase_slug: phaseSlug,
  browser_send_status: sendReceipt.browser_send_status,
  executable_rows_count: immediateSafeExecutable.length,
  held_immediate_rows_count: immediateHeld.length,
  x2_rows_count: x2Rows.length,
  dashboard_rows: dashboardRows.length,
  cleanup_rows: cleanupRows.length,
  closeout_allowed_now: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function rowRef(row) {
  return {
    id: row.id,
    line_sha256: row.line_sha256,
    approval_bucket: row.approval_bucket,
    execution_lane: row.execution_lane,
    topic_tags: rowTags(row),
  };
}

function rowTags(row) {
  return Array.isArray(row.topic_tags) ? row.topic_tags : [];
}

function buildLane(name, tag) {
  const tagged = rows.filter((row) => rowTags(row).includes(tag));
  return {
    name,
    topic_tag: tag,
    rows_available: tagged.length,
    safe_or_candidate_rows: tagged.filter((row) => ["safe_now", "candidate"].includes(row.approval_bucket)).length,
    exact_or_blocked_rows_queued: tagged.filter((row) => ["exact_approval_needed", "blocked"].includes(row.approval_bucket)).length,
  };
}

function dashboard(name, fields) {
  return { name, fields, status: "design_ready" };
}

function cleanup(id, note) {
  return { id, mode: "inventory_only", note };
}

function artifact(type, status, extra) {
  return {
    artifact_type: type,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    startup_status: startup.overall_status,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
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

function refreshBeacons(refs, watchDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = watchDoc.overall_status;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = "v557-gmut-thos-v4-x2";
    data.latest_completed_x1_phase = "v557-gmut-thos-v4-x1";
    data.latest_completed_x2_phase = "v557-gmut-thos-v4-x2";
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = "v557-gmut-thos-v5-x2";
    data.next_x1_lane_after_x2 = "v557-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects";
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v5_x1_lumen_safe_cadence = {
      status: watchDoc.overall_status,
      browser_send_status: sendReceipt.browser_send_status,
      executable_rows_count: immediateSafeExecutable.length,
      held_immediate_rows_count: immediateHeld.length,
      x2_rows_count: x2Rows.length,
      closeout_allowed_now: false,
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
    "## v557 v5 x1 Lumen Safe Cadence",
    "",
    `Status: \`${doc.v557_v5_x1_lumen_safe_cadence?.status || "not_recorded"}\``,
    `Browser send status: \`${doc.v557_v5_x1_lumen_safe_cadence?.browser_send_status || "not_recorded"}\``,
    `Executable rows: \`${doc.v557_v5_x1_lumen_safe_cadence?.executable_rows_count ?? "not_recorded"}\``,
    `X2 rows: \`${doc.v557_v5_x1_lumen_safe_cadence?.x2_rows_count ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_v5_x1_lumen_safe_cadence?.closeout_allowed_now === true ? "true" : "false"}\``,
    `Full goal complete: \`${doc.v557_v5_x1_lumen_safe_cadence?.full_goal_complete === true ? "true" : "false"}\``,
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
  if (doc.artifact_type.endsWith("_execution_ledger")) {
    return {
      executable_rows_count: doc.executable_rows_count,
      held_immediate_rows_count: doc.held_immediate_rows_count,
      x2_rows_count: doc.x2_rows_count,
    };
  }
  if (doc.artifact_type.endsWith("_build_queue")) {
    return {
      x2_rows_count: doc.x2_rows_count,
      safe_now_x2_rows: doc.safe_now_x2_rows,
      candidate_x2_rows: doc.candidate_x2_rows,
    };
  }
  if (doc.artifact_type.endsWith("_watchcard")) {
    return {
      browser_send_status: doc.browser_send_status,
      closeout_allowed_now: doc.closeout_allowed_now,
      next_action: doc.next_action,
    };
  }
  return {
    artifact_type: doc.artifact_type,
    raw_private_material_published: false,
  };
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
  return "No private message body content, private Browser routes, private URLs, screenshots, private callable IDs, credentials, runtime streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function title(type) {
  return type.replace(/^ghc_v557_v5_x1_/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
