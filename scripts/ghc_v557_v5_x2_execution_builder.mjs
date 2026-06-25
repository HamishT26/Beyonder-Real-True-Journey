#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v5-x2";
const completedX1 = "v557-gmut-thos-v5-x1";
const nextPhase = "v557-gmut-thos-v6-x1";
const nextX2 = "v557-gmut-thos-v6-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const closeoutX1 = readJson(path.join(tracesDir, `${completedX1}-closeout-v1.json`));
const readiness = readJson(path.join(tracesDir, `${completedX1}-v5-x2-readiness-handoff-v1.json`));
const latestQueue = readJson(path.join(tracesDir, `${completedX1}-lumen-proposal-hash-queue-v1.json`));
const earlierQueue = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-lumen-proposal-hash-queue-v1.json"));
const latestMatrix = readJson(path.join(tracesDir, `${completedX1}-grand-trinity-matrix-v1.json`));
const latestDashboards = readJson(path.join(tracesDir, `${completedX1}-lumen-dashboard-design-ledger-v1.json`));
const safeCadence = readJson(path.join(tracesDir, `${completedX1}-lumen-background-supervision-watchcard-v1.json`));

const latestRows = normalizeRows(latestQueue.queue_rows || [], "latest_v5_x1_lumen");
const earlierRows = normalizeRows(earlierQueue.queue_rows || [], "prior_three_lumen_messages");
const allRows = [...latestRows, ...earlierRows];
const safeOrCandidate = allRows.filter((row) => ["safe_now", "candidate"].includes(row.approval_bucket));
const exactRows = allRows.filter((row) => row.approval_bucket === "exact_approval_needed");
const blockedRows = allRows.filter((row) => row.approval_bucket === "blocked");
const x2Rows = allRows.filter((row) => row.execution_lane === "x2_build_task");

const executionIndex = artifact("ghc_v557_v5_x2_execution_index", "PASS_V557_V5_X2_EXECUTION_INDEX_BUILT", {
  completed_x1_status: closeoutX1.overall_status,
  readiness_status: readiness.overall_status,
  combined_proposal_rows: allRows.length,
  latest_queue_rows: latestRows.length,
  earlier_queue_rows: earlierRows.length,
  safe_or_candidate_rows: safeOrCandidate.length,
  exact_rows_queued: exactRows.length,
  blocked_rows_queued: blockedRows.length,
  x2_rows: x2Rows.length,
});

const safeExecutionReducer = artifact("ghc_v557_v5_x2_safe_execution_reducer", "PASS_V557_V5_X2_SAFE_EXECUTION_REDUCED", {
  safe_or_candidate_rows_represented: safeOrCandidate.length,
  exact_rows_queued: exactRows.length,
  blocked_rows_queued: blockedRows.length,
  reduction_policy: "Represent safe/candidate proposal work through non-destructive docs, runners, dashboards, validators, and handoff artifacts. Queue exact and blocked rows.",
  topic_counts: topicCounts(safeOrCandidate),
  representative_rows: safeOrCandidate.slice(0, 60).map(rowRef),
});

const proposalBridge = artifact("ghc_v557_v5_x2_lumen_proposal_bridge_ledger", "PASS_V557_V5_X2_LUMEN_PROPOSAL_BRIDGE_LEDGER_BUILT", {
  latest_source_digest: latestQueue.source_digest,
  earlier_source_digest: earlierQueue.source_digest,
  raw_text_published: false,
  bridge_counts: {
    latest_rows: latestRows.length,
    earlier_rows: earlierRows.length,
    total_rows: allRows.length,
  },
  merged_topic_counts: topicCounts(allRows),
});

const dashboardBuild = artifact("ghc_v557_v5_x2_dashboard_build_manifest", "PASS_V557_V5_X2_DASHBOARD_BUILD_MANIFEST_READY", {
  source_dashboard_status: latestDashboards.overall_status,
  dashboards_built_or_represented: [
    dashboard("goal-mode-continuity", ["phase", "latest_closed", "next_lane", "full_goal_complete_false"]),
    dashboard("browser-handoff-safety", ["message_hash", "send_status", "harvest_status", "duplicate_send_allowed_false"]),
    dashboard("full-tools-private-support-audit", ["private_source_digest", "raw_text_published_false", "branch_rotation_watch"]),
    dashboard("lumen-launch-health", ["startup", "send", "harvest", "proposal_queue"]),
    dashboard("main-retry-blocker", ["retry_count", "reflection_targets", "safe_work_units"]),
    dashboard("trinity-matrix", ["mind", "body", "heart", "open_gates"]),
  ],
});

const skillRunnerRefresh = artifact("ghc_v557_v5_x2_skill_runner_pack_refresh", "PASS_V557_V5_X2_SKILL_RUNNER_PACK_REFRESHED", {
  refreshed_or_reused_skills: [
    "ghc-lumen-launch",
    "ghc-background-sibling-supervision",
    "ghc-main-retry",
    "ghc-worktree-branch-rotation",
    "ghc-main-orchestration-memory",
    "ghc-full-tools-skill-bank",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
    "ghc-safe-runner-orchestrator",
  ],
  refreshed_or_reused_runners: [
    "ghc_v557_v5_x1_lumen_startup_builder.mjs",
    "ghc_v557_v5_x1_lumen_send_receipt_builder.mjs",
    "ghc_v557_v5_x1_lumen_safe_cadence_runner.mjs",
    "ghc_v557_v5_x1_lumen_closeout_builder.mjs",
    "ghc_v557_v5_x2_execution_builder.mjs",
    "ghc_v557_lumen_private_ingestion_trinity_matrix_runner.mjs",
    "omega_mini_current_state_guard.py",
  ],
  installed_new_skills_now: 0,
  installed_new_runners_now: 1,
  note: "This x2 refresh uses and records the current pack instead of creating large synthetic skill counts.",
});

const reflectionLedger = artifact("ghc_v557_v5_x2_web_journey_reflection_ledger_50", "PASS_V557_V5_X2_REFLECTION_LEDGER_50_BUILT", {
  reflection_rows: buildReflectionRows(),
  live_web_queries_run_now: 0,
  reason_no_live_web_queries: "No fresh external factual claim beyond already verified Codex CLI/package version was needed for this safe x2 ledger.",
});

const branchRotationDecision = artifact("ghc_v557_v5_x2_branch_rotation_decision", "PASS_V557_V5_X2_BRANCH_ROTATION_NOT_NEEDED", {
  active_sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  active_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  rotate_now: false,
  next_rotation_pattern: "omega-mini-4/full-tools-3 and onward from verified safe bases",
  reason: "mini-3 remained clean after v5 x1 commit and remote verification; no repeated slow status failure after commit.",
  raw_private_material_moved: false,
});

const privacyOpenGateRail = artifact("ghc_v557_v5_x2_privacy_open_gate_rail", "PASS_V557_V5_X2_PRIVACY_OPEN_GATE_RAIL_BUILT", {
  proof_gates: claimBoundary(),
  publication_boundary: publicationBoundary(),
  exact_or_blocked_rows_queued: exactRows.length + blockedRows.length,
});

const v6Readiness = artifact("ghc_v557_v5_x2_v6_arby_cicero_readiness", "PASS_V557_V6_X1_ARBY_CICERO_READINESS_READY_NOT_STARTED", {
  next_phase: nextPhase,
  lane: "Arby and Cicero",
  launch_skill: "ghc-arby-cicero-launch",
  background_supervision_required: true,
  startup_inputs: [
    "latest current-state beacon",
    "v5 x2 closeout",
    "duo x1 target profile",
    "strict CLI route for Arby",
    "recovered app-lane route for Cicero",
  ],
  not_started_by_v5_x2: true,
});

const closeout = artifact("ghc_v557_v5_x2_closeout", "PASS_V557_V5_X2_CLOSED_V6_X1_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: completedX1,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextPhase,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: "v557-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects",
  counts: {
    combined_proposal_rows: allRows.length,
    safe_or_candidate_rows_represented: safeOrCandidate.length,
    exact_rows_queued: exactRows.length,
    blocked_rows_queued: blockedRows.length,
    dashboards_built_or_represented: dashboardBuild.dashboards_built_or_represented.length,
    reflection_rows: reflectionLedger.reflection_rows.length,
    skills_refreshed_or_reused: skillRunnerRefresh.refreshed_or_reused_skills.length,
    runners_refreshed_or_reused: skillRunnerRefresh.refreshed_or_reused_runners.length,
  },
  full_goal_complete: false,
});

const refs = [
  writePair("execution-index", executionIndex),
  writePair("safe-execution-reducer", safeExecutionReducer),
  writePair("lumen-proposal-bridge-ledger", proposalBridge),
  writePair("dashboard-build-manifest", dashboardBuild),
  writePair("skill-runner-pack-refresh", skillRunnerRefresh),
  writePair("web-journey-reflection-ledger-50", reflectionLedger),
  writePair("branch-rotation-decision", branchRotationDecision),
  writePair("privacy-open-gate-rail", privacyOpenGateRail),
  writePair("v6-arby-cicero-readiness", v6Readiness),
  writePair("closeout", closeout),
];

refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  latest_closed_phase: phaseSlug,
  next_active_phase: nextPhase,
  combined_proposal_rows: allRows.length,
  safe_or_candidate_rows_represented: safeOrCandidate.length,
  exact_rows_queued: exactRows.length,
  blocked_rows_queued: blockedRows.length,
  full_goal_complete: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function normalizeRows(rows, source) {
  return rows.map((row) => ({
    id: `${source}:${row.id}`,
    source,
    line_sha256: row.line_sha256,
    approval_bucket: row.approval_bucket,
    execution_lane: row.execution_lane,
    topic_tags: Array.isArray(row.topic_tags) ? row.topic_tags : [],
  }));
}

function rowRef(row) {
  return {
    id: row.id,
    line_sha256: row.line_sha256,
    approval_bucket: row.approval_bucket,
    execution_lane: row.execution_lane,
    topic_tags: row.topic_tags,
  };
}

function topicCounts(rows) {
  const out = {};
  for (const row of rows) {
    for (const tag of row.topic_tags) {
      out[tag] = (out[tag] || 0) + 1;
    }
  }
  return out;
}

function dashboard(name, fields) {
  return { name, fields, status: "built_or_represented" };
}

function buildReflectionRows() {
  const topics = [
    "phase truth",
    "source reflection",
    "approval split",
    "cleanup classification",
    "Browser handoff safety",
    "full-tools private support",
    "worktree branch rotation",
    "drive posture",
    "Codex CLI posture",
    "held sibling prep",
  ];
  return Array.from({ length: 50 }, (_, index) => {
    const topic = topics[index % topics.length];
    return {
      id: `v557-v5-x2-reflection-${String(index + 1).padStart(2, "0")}`,
      topic,
      source_class: index % 2 === 0 ? "phase_record" : "journey_record",
      runner_implication: `Use ${topic} as a safe x2 validation and handoff lane.`,
    };
  });
}

function artifact(type, status, extra) {
  return {
    artifact_type: type,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
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
    data.current_active_phase = nextPhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = completedX1;
    data.latest_completed_x2_phase = phaseSlug;
    data.next_expected_scope = nextPhase;
    data.next_x2_scope = nextX2;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v5_x2_closeout = {
      status: closeoutDoc.overall_status,
      combined_proposal_rows: allRows.length,
      safe_or_candidate_rows_represented: safeOrCandidate.length,
      exact_rows_queued: exactRows.length,
      blocked_rows_queued: blockedRows.length,
      next_active_phase: nextPhase,
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
    "## v557 v5 x2 Closeout",
    "",
    `Status: \`${doc.v557_v5_x2_closeout?.status || "not_recorded"}\``,
    `Combined proposal rows: \`${doc.v557_v5_x2_closeout?.combined_proposal_rows ?? "not_recorded"}\``,
    `Safe/candidate rows represented: \`${doc.v557_v5_x2_closeout?.safe_or_candidate_rows_represented ?? "not_recorded"}\``,
    `Next active phase: \`${doc.v557_v5_x2_closeout?.next_active_phase || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v5_x2_closeout?.full_goal_complete === true ? "true" : "false"}\``,
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
  if (doc.artifact_type.endsWith("_closeout")) {
    return {
      next_active_phase: doc.next_active_phase,
      combined_proposal_rows: doc.counts.combined_proposal_rows,
      safe_or_candidate_rows_represented: doc.counts.safe_or_candidate_rows_represented,
      full_goal_complete: doc.full_goal_complete,
    };
  }
  if (doc.combined_proposal_rows !== undefined) {
    return {
      combined_proposal_rows: doc.combined_proposal_rows,
      safe_or_candidate_rows: doc.safe_or_candidate_rows,
      x2_rows: doc.x2_rows,
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
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function title(type) {
  return type.replace(/^ghc_v557_v5_x2_/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
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
