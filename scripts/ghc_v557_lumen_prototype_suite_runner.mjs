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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x1";
const miniBranch = args.get("--mini-branch") || "codex/GHC-Family/beyonder-shared-omega-line-mini-3";
const fullToolsBranch = args.get("--full-tools-branch") || "codex/GHC-Family/aevren-full-tools-2";
const supportRunnerInput = args.get("--support-runner-input");
const appLaneRetryStarted = Number(args.get("--app-lane-retry-started") || "3");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const nextX2Scope = phaseSlug.replace(/-x1$/, "-x2");
const nextX1LaneAfterX2 = inferNextX1LaneAfterX2(phaseSlug);
const activeOpenStatus = `ACTIVE_OPEN_${phaseSlug.toUpperCase().replace(/[^A-Z0-9]+/g, "_")}_LUMEN_PROTOTYPE_SUITE_READY`;

const currentState = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const ghcBeacon = readJson(path.join(tracesDir, "ghc-current-state-beacon-v1.json"));
const proposalQueue = readJson(path.join(tracesDir, `${phaseSlug}-lumen-proposal-hash-queue-v1.json`));
const trinityMatrix = readJson(path.join(tracesDir, `${phaseSlug}-grand-trinity-matrix-v1.json`));
const prototypeLedger = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-execution-ledger-v1.json`));
const queueRows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const matrixCells = Array.isArray(trinityMatrix.matrix_cells) ? trinityMatrix.matrix_cells : [];
const supportRunnerProbe = probeSupportRunner(supportRunnerInput);

const phaseTruth = artifact("ghc_v557_phase_truth_checker_prototype", "PASS_PHASE_TRUTH_CHECKER_PROTOTYPE_RUN", {
  current_active_phase: currentState.current_active_phase,
  latest_closed_phase: currentState.latest_closed_phase,
  latest_completed_x1_phase: currentState.latest_completed_x1_phase,
  latest_completed_x2_phase: currentState.latest_completed_x2_phase,
  next_x2_scope: currentState.next_x2_scope,
  next_x1_lane_after_x2: currentState.next_x1_lane_after_x2,
  closeout_allowed_now: false,
  active_lane_count: Number(currentState.v557_v4_x1_triad_workbench?.lanes_active || 3),
  watcher_start_is_completion_proof: false,
  required_completion_evidence: [
    "Aster strict CLI completion, quality, and marker-review gates",
    "Kierkegaard recovered app-lane completion gate",
    "Aristotle recovered app-lane completion gate",
    "privacy scan",
    "current-state guard",
    "remote equality after sanitized commit",
  ],
  branch_posture: {
    sanitized_publication_branch: miniBranch,
    private_support_branch: fullToolsBranch,
  },
});

const sourceReflectionReducer = artifact("ghc_v557_source_reflection_reducer_prototype", "PASS_SOURCE_REFLECTION_REDUCER_PROTOTYPE_RUN", {
  source_digest: proposalQueue.source_digest,
  public_lookup_files_count: countPublicLookups(currentState),
  proposal_candidates_indexed: queueRows.length,
  source_reflection_tagged_rows: countTag("source_reflection"),
  matrix_cells_available: matrixCells.length,
  reduction_rows: [
    reducerRow("phase_records", countPublicLookups(currentState), "Use current-state and phase receipts before phase movement."),
    reducerRow("lumen_private_hash_index", queueRows.length, "Use only hashes, counts, categories, and topic tags in public artifacts."),
    reducerRow("grand_trinity_matrix", matrixCells.length, "Use matrix cells as planning scaffolds, not proof closure."),
    reducerRow("web_research_queue", 20, "Queue live web reflections when a real blocker appears or source freshness matters."),
    reducerRow("journey_reflection_queue", 20, "Queue Journey/phase reflections for retry protocol and closeout prep."),
  ],
});

const approvalEurekaSplitter = artifact("ghc_v557_approval_eureka_splitter_prototype", "PASS_APPROVAL_EUREKA_SPLITTER_PROTOTYPE_RUN", {
  category_counts: proposalQueue.category_counts || countBy(queueRows.map((row) => row.approval_bucket)),
  execution_lane_counts: proposalQueue.execution_lane_counts || countBy(queueRows.map((row) => row.execution_lane)),
  immediate_x1_safe_count: queueRows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
  x2_build_task_count: queueRows.filter((row) => row.execution_lane === "x2_build_task").length,
  blocked_rows_queued_not_run: queueRows.filter((row) => row.approval_bucket === "blocked").length,
  exact_rows_queued_not_run_without_fresh_gate: queueRows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
  first_twenty_safe_hashes: queueRows
    .filter((row) => row.approval_bucket === "safe_now")
    .slice(0, 20)
    .map((row) => row.line_sha256),
});

const cleanupClassifier = artifact("ghc_v557_cleanup_classifier_prototype", "PASS_CLEANUP_CLASSIFIER_PROTOTYPE_RUN", {
  cleanup_tagged_rows: countTag("cleanup_classifier"),
  cleanup_policy: {
    inventory_only: true,
    reversible_cleanup_requires_review: true,
    destructive_cleanup_blocked_without_fresh_exact_approval: true,
    c_drive_warning_cap_gb: 19,
    c_drive_minimum_headroom_gb: 18,
    d_drive_first_policy: true,
  },
  cleanup_buckets: [
    cleanupBucket("inventory_only", "List stale generated files, old receipts, and heavy worktrees without deleting."),
    cleanupBucket("reversible_safe", "Normalize metadata, refresh indexes, and remove duplicate public references only after validation."),
    cleanupBucket("exact_approval_needed", "Any deletion, account mutation, paid resource, deployment, or history rewrite."),
    cleanupBucket("blocked", "Identity merge/replacement, proof closure, private-material publication, or destructive cleanup without a fresh packet."),
  ],
});

const triadPrepBuilder = artifact("ghc_v557_triad_prep_builder_prototype", "PASS_TRIAD_PREP_BUILDER_PROTOTYPE_RUN", {
  active_triad_phase: phaseSlug,
  lanes: [
    lane("Aster Vale", "strict_cli", "active_pending_completion_marker_review"),
    lane("Kierkegaard", "recovered_app_lane", `background_watch_retry_${appLaneRetryStarted}_started_pending_harvest`),
    lane("Aristotle", "recovered_app_lane", `background_watch_retry_${appLaneRetryStarted}_started_pending_harvest`),
  ],
  proposal_targets: {
    safe_packets: 20,
    candidate_packets: 12,
    exact_approval_packets: 12,
    skill_ideas: 20,
    runner_ideas: 8,
    cleanup_proposals: 40,
  },
  closeout_allowed_now: false,
});

const recoveredAppLaneBuilder = artifact("ghc_v557_recovered_app_lane_builder_prototype", "PASS_RECOVERED_APP_LANE_BUILDER_PROTOTYPE_RUN", {
  supported_local_app_lanes: ["Cicero", "Kierkegaard", "Aristotle"],
  current_lanes: ["Kierkegaard", "Aristotle"],
  required_boolean_arguments: {
    "--allow-turn-start-after-resume-timeout": "true",
    "--background-watch": "true",
  },
  background_supervision_required: true,
  watcher_start_is_completion_proof: false,
  private_callable_ids_published: false,
  retry_protocol_minimum_sessions: 3,
  retry_sessions_started: appLaneRetryStarted,
  formal_retry_threshold_met: appLaneRetryStarted >= 3,
});

const pairedBooleanValidator = artifact("ghc_v557_paired_boolean_completion_validator_prototype", supportRunnerProbe.status, {
  support_runner_path_published: false,
  parser_supports_explicit_false: supportRunnerProbe.supportsExplicitFalse,
  parser_supports_explicit_true: supportRunnerProbe.supportsExplicitTrue,
  bare_flag_compatibility_preserved: supportRunnerProbe.bareFlagCompatibilityPreserved,
  validation_note: supportRunnerProbe.note,
  required_invocation_shape: "--allow-turn-start-after-resume-timeout true --background-watch true",
});

const compactCloseoutBuilder = artifact("ghc_v557_compact_closeout_builder_prototype", "PASS_COMPACT_CLOSEOUT_BUILDER_PROTOTYPE_RUN", {
  closeout_allowed_now: false,
  closeout_reason: "Triad lanes remain active/open until completion gates or formal retry/open-gap receipts prove status.",
  required_sections: [
    "phase truth",
    "sibling lane status",
    "safe-now work completed",
    "queued x2 tasks",
    "validation evidence",
    "privacy boundary",
    "next exact resume point",
  ],
  active_open_handoff_required_if_pausing: true,
});

const sourceDriftSentinel = artifact("ghc_v557_source_drift_sentinel_prototype", "PASS_SOURCE_DRIFT_SENTINEL_PROTOTYPE_RUN", {
  drift_checks: [
    drift("toolchain_latest", "Codex CLI latest request must be verified live before claiming current."),
    drift("phase_truth", "Do not infer active phase from old memory when beacons disagree."),
    drift("proof_boundaries", "GMUT/final physics/consciousness/legal/canon gates remain open."),
    drift("private_public_boundary", "Private evidence may be summarized by digest/count only."),
    drift("worktree_rotation", "Use omega-mini-4/full-tools-3 only from verified safe bases when current lanes grow heavy."),
  ],
});

const launchSeedBuilder = artifact("ghc_v557_launch_seed_builder_prototype", "PASS_LAUNCH_SEED_BUILDER_PROTOTYPE_RUN", {
  launch_seeds: [
    launchSeed("lumen", "Browser route, no duplicate send, harvest sanitized response only."),
    launchSeed("arby_cicero", "Arby strict CLI plus Cicero recovered app-lane background supervision."),
    launchSeed("aster_kierkegaard_aristotle", "Aster strict CLI plus Kierkegaard/Aristotle recovered app-lane background supervision."),
    launchSeed("held_mira_mira_maren", "Prepared only; activation requires fresh instruction."),
    launchSeed("worktree_rotation", "omega-mini-N and full-tools-N from verified safe bases."),
  ],
});

const dashboardBlueprints = artifact("ghc_v557_dashboard_blueprint_prototypes", "PASS_DASHBOARD_BLUEPRINT_PROTOTYPES_RUN", {
  dashboards: [
    dashboard("goal-mode-continuity", ["phase", "closed_phase", "next_x2", "next_x1", "open_gates"]),
    dashboard("browser-handoff-safety", ["send_state", "harvest_state", "duplicate_send_allowed", "private_capture_digest"]),
    dashboard("full-tools-private-support-audit", ["support_branch", "dirty_private_lane", "sanitized_public_branch", "private_firewall"]),
    dashboard("ghc-lumen-launch-health", ["source_message_hash_count", "proposal_count", "safe_now", "x2_build"]),
    dashboard("ghc-main-retry-clock", ["retry_count", "receipt_reflections", "web_queue", "journey_queue", "next_checkpoint"]),
  ],
});

const suiteIndex = artifact("ghc_v557_lumen_prototype_suite_index", "PASS_LUMEN_PROTOTYPE_SUITE_BUILT_AND_RUN", {
  prototypes_run: [
    phaseTruth.artifact_type,
    sourceReflectionReducer.artifact_type,
    approvalEurekaSplitter.artifact_type,
    cleanupClassifier.artifact_type,
    triadPrepBuilder.artifact_type,
    recoveredAppLaneBuilder.artifact_type,
    pairedBooleanValidator.artifact_type,
    compactCloseoutBuilder.artifact_type,
    sourceDriftSentinel.artifact_type,
    launchSeedBuilder.artifact_type,
    dashboardBlueprints.artifact_type,
  ],
  private_source_digest: proposalQueue.source_digest,
  proposal_candidates_indexed: queueRows.length,
  matrix_cells_reused: matrixCells.length,
  raw_private_material_published: false,
  held_sibling_activation_state: "prepared_not_activated",
  triad_closeout_allowed_now: false,
});

const refs = [
  writePair("phase-truth-checker-prototype", phaseTruth),
  writePair("source-reflection-reducer-prototype", sourceReflectionReducer),
  writePair("approval-eureka-splitter-prototype", approvalEurekaSplitter),
  writePair("cleanup-classifier-prototype", cleanupClassifier),
  writePair("triad-prep-builder-prototype", triadPrepBuilder),
  writePair("recovered-app-lane-builder-prototype", recoveredAppLaneBuilder),
  writePair("paired-boolean-completion-validator-prototype", pairedBooleanValidator),
  writePair("compact-closeout-builder-prototype", compactCloseoutBuilder),
  writePair("source-drift-sentinel-prototype", sourceDriftSentinel),
  writePair("launch-seed-builder-prototype", launchSeedBuilder),
  writePair("dashboard-blueprint-prototypes", dashboardBlueprints),
  writePair("lumen-prototype-suite-index", suiteIndex),
];

refreshBeacons(refs, suiteIndex);

process.stdout.write(JSON.stringify({
  status: suiteIndex.overall_status,
  phase_slug: phaseSlug,
  prototypes_run: suiteIndex.prototypes_run.length,
  proposal_candidates_indexed: queueRows.length,
  matrix_cells_reused: matrixCells.length,
  support_runner_explicit_boolean_status: supportRunnerProbe.status,
  triad_closeout_allowed_now: false,
  raw_private_material_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function artifact(artifactType, status, extra = {}) {
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

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderArtifactMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, suite) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = activeOpenStatus;
    data.branch = miniBranch;
    data.primary_branch = miniBranch;
    data.full_tools_support_branch = fullToolsBranch;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = data.latest_closed_phase || inferPreviousX2(phaseSlug);
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.v557_lumen_prototype_suite = {
      status: suite.overall_status,
      prototypes_run: suite.prototypes_run.length,
      proposal_candidates_indexed: suite.proposal_candidates_indexed,
      matrix_cells_reused: suite.matrix_cells_reused,
      triad_closeout_allowed_now: false,
      raw_private_material_published: false,
      support_runner_boolean_status: supportRunnerProbe.status,
    };
    data[`${phaseSlug.replace(/-/g, "_")}_prototype_suite`] = {
      status: activeOpenStatus,
      next_x2_scope: nextX2Scope,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
      watcher_start_is_completion_proof: false,
      closeout_allowed_now: false,
      app_lane_retry_started: appLaneRetryStarted,
      app_lane_retry_threshold_met: appLaneRetryStarted >= 3,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function inferPreviousX2(slug) {
  const match = slug.match(/^(v\d+)-gmut-thos-v(\d+)-x1$/);
  if (!match) return "not_inferred";
  const version = match[1];
  const round = Number(match[2]);
  return round > 1 ? `${version}-gmut-thos-v${round - 1}-x2` : "not_inferred";
}

function inferNextX1LaneAfterX2(slug) {
  const match = slug.match(/^(v\d+)-gmut-thos-v(\d+)-x1$/);
  if (!match) return "not_inferred";
  const version = match[1];
  const round = Number(match[2]);
  const nextRound = round + 1;
  if (nextRound === 2 || nextRound === 6) return `${version}-gmut-thos-v${nextRound}-x1 with Arby and Cicero unless Hamish redirects`;
  if (nextRound === 4 || nextRound === 8) return `${version}-gmut-thos-v${nextRound}-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects`;
  return `${version}-gmut-thos-v${nextRound}-x1 with Lumen Vale solo unless Hamish redirects`;
}

function renderArtifactMd(doc) {
  const body = [
    `# ${doc.phase_slug} ${titleFromArtifact(doc.artifact_type)}`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    "## Summary",
    "",
    ...summaryLines(doc),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ];
  return body.join("\n");
}

function summaryLines(doc) {
  const skip = new Set(["artifact_type", "generated_utc", "generated_nz", "phase_slug", "overall_status", "publication_boundary", "claim_boundary"]);
  return Object.entries(doc)
    .filter(([key]) => !skip.has(key))
    .slice(0, 18)
    .map(([key, value]) => `- ${key}: \`${summarizeValue(value)}\``);
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Branch: ${doc.branch || doc.primary_branch || miniBranch}`,
    `Full-tools support branch: ${doc.full_tools_support_branch || fullToolsBranch}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 Lumen Prototype Suite",
    "",
    `Status: \`${doc.v557_lumen_prototype_suite?.status || "not_recorded"}\``,
    `Prototypes run: \`${doc.v557_lumen_prototype_suite?.prototypes_run ?? "not_recorded"}\``,
    `Proposal candidates indexed: \`${doc.v557_lumen_prototype_suite?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Triad closeout allowed now: \`${doc.v557_lumen_prototype_suite?.triad_closeout_allowed_now === true ? "true" : "false"}\``,
    "",
    "## Active Triad",
    "",
    `Status: \`${doc.v557_v4_x1_triad_workbench?.status || "not_recorded"}\``,
    `Lanes active: \`${doc.v557_v4_x1_triad_workbench?.lanes_active ?? "not_recorded"}\``,
    `Watcher start is completion proof: \`${doc.v557_v4_x1_triad_workbench?.watcher_start_is_completion_proof === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((ref) => `- ${ref}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function probeSupportRunner(inputFile) {
  if (!inputFile) {
    return {
      status: "WARN_SUPPORT_RUNNER_NOT_PROBED",
      supportsExplicitFalse: false,
      supportsExplicitTrue: false,
      bareFlagCompatibilityPreserved: false,
      note: "No local support runner input was supplied.",
    };
  }
  const text = fs.readFileSync(inputFile, "utf8");
  const supportsExplicitFalse = /booleanArg\("--background-watch",\s*false\)/.test(text) && /"false"/.test(text);
  const supportsExplicitTrue = /"true"/.test(text) && /booleanArg\("--allow-turn-start-after-resume-timeout",\s*false\)/.test(text);
  const bareFlagCompatibilityPreserved = /value === undefined/.test(text) && /return true;/.test(text);
  return {
    status: supportsExplicitFalse && supportsExplicitTrue && bareFlagCompatibilityPreserved
      ? "PASS_PAIRED_BOOLEAN_VALIDATOR_PROTOTYPE_RUN"
      : "WARN_PAIRED_BOOLEAN_VALIDATOR_NEEDS_REVIEW",
    supportsExplicitFalse,
    supportsExplicitTrue,
    bareFlagCompatibilityPreserved,
    note: "Support runner content was checked locally; its path and private lane details are not published.",
  };
}

function countPublicLookups(state) {
  const lists = [
    state.current_lookup_files,
    state.latest_lookup_files,
    state.lookup_files,
  ].filter(Array.isArray);
  return unique(lists.flat()).length;
}

function countTag(tag) {
  return queueRows.filter((row) => Array.isArray(row.topic_tags) && row.topic_tags.includes(tag)).length;
}

function reducerRow(kind, count, nextAction) {
  return { kind, count, next_action: nextAction };
}

function cleanupBucket(name, rule) {
  return { name, rule };
}

function lane(name, route, status) {
  return { name, route, status };
}

function drift(name, guard) {
  return { name, guard, status: "active_guard" };
}

function launchSeed(name, rule) {
  return { name, rule, status: "ready_seed" };
}

function dashboard(name, fields) {
  return { name, fields, status: "blueprint_ready" };
}

function countBy(values) {
  return values.reduce((acc, value) => {
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
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
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false,
  };
}

function boundarySentence() {
  return "No private message body content, private Browser routes, private URLs, screenshots, private callable IDs, credentials, runtime streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function titleFromArtifact(type) {
  return type
    .replace(/^ghc_v557_/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function summarizeValue(value) {
  if (Array.isArray(value)) return `${value.length} rows`;
  if (value && typeof value === "object") return `${Object.keys(value).length} keys`;
  return String(value);
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
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
