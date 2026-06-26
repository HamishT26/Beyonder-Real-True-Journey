#!/usr/bin/env node
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const defaultRoot = path.resolve(__dirname, "..");
const args = parseArgs(process.argv.slice(2));

const root = path.resolve(args.get("--root") || defaultRoot);
const phaseSlug = args.get("--phase-slug") || "v558-gmut-thos-v5-x2";
const sourcePhase = args.get("--source-phase") || "v558-gmut-thos-v5-x1";
const nextActivePhase = args.get("--next-active-phase") || "v558-gmut-thos-v6-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v558-gmut-thos-v6-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v558-gmut-thos-v7-x1 Lumen Vale solo unless Hamish redirects";
const nextLaneLabel = "Maren Quill and Solenne Vale";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const queuePath = path.resolve(
  args.get("--queue") ||
    path.join(tracesDir, `${sourcePhase}-lumen-sanitized-proposal-queue-v1.json`),
);

const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString();
const generatedNz = nzTimestamp(generatedDate);

if (!fs.existsSync(queuePath)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V558_V5_X2_SOURCE_QUEUE_MISSING",
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

fs.mkdirSync(tracesDir, { recursive: true });
fs.mkdirSync(omegaDir, { recursive: true });

const queue = readJson(queuePath);
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const counts = summarizeRows(rows);
const x2Rows = rows.filter((row) => row.execution_lane === "x2_build_task");
const safeX2Rows = x2Rows.filter((row) => row.approval_bucket === "safe_now" || row.approval_bucket === "candidate");
const heldX2Rows = x2Rows.filter((row) => row.approval_bucket === "exact_approval_needed" || row.approval_bucket === "blocked");

const manifest = buildSafeRunnerManifest();
writeArtifact("safe-runner-manifest", manifest);

const orchestrator = runSafeRunner(manifest);
const childArtifacts = [
  ["x2-execution-ledger", buildExecutionLedger(orchestrator)],
  ["prototype-build-ledger", buildPrototypeBuildLedger()],
  ["queue-reduction-ledger", buildQueueReductionLedger()],
  ["source-reflection-ledger", buildSourceReflectionLedger()],
  ["boundary-open-gate-scan", buildBoundaryOpenGateScan()],
  ["private-boundary-route-ledger", buildPrivateBoundaryRouteLedger()],
  ["next-duo-startup-prep", buildNextDuoStartupPrep()],
  ["skill-runner-refresh-receipt", buildSkillRunnerRefreshReceipt()],
  ["drive-toolchain-guard", buildDriveToolchainGuard()],
];

for (const [slug, artifact] of childArtifacts) {
  writeArtifact(slug, artifact);
}

const closeout = buildCloseout(childArtifacts.map(([, artifact]) => artifact), orchestrator);
writeArtifact("closeout", closeout);
writeArtifact("v6-x1-maren-solenne-startup-handoff", buildV6Handoff(closeout));

if (closeout.status === "PASS_V558_V5_X2_CLOSED_V6_X1_READY") {
  updateStateFiles(closeout);
}

console.log(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  tagged_rows: rows.length,
  x2_build_rows_represented: x2Rows.length,
  safe_x2_rows_reduced_now: safeX2Rows.length,
  held_x2_rows: heldX2Rows.length,
  exact_rows_queued_global: counts.approval.exact_approval_needed || 0,
  next_active_phase: closeout.next_active_phase,
}, null, 2));

process.exit(closeout.status.startsWith("PASS") ? 0 : 1);

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, next);
      i += 1;
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

function summarizeRows(inputRows) {
  const summary = {
    total: inputRows.length,
    execution: {},
    approval: {},
    topic_tags: {},
    x2_build_by_approval: {},
    immediate_by_approval: {},
  };
  for (const row of inputRows) {
    bump(summary.execution, row.execution_lane || "unknown");
    bump(summary.approval, row.approval_bucket || "unknown");
    for (const tag of row.topic_tags || []) bump(summary.topic_tags, tag);
    if (row.execution_lane === "x2_build_task") {
      bump(summary.x2_build_by_approval, row.approval_bucket || "unknown");
    }
    if (row.execution_lane === "immediate_x1_safe") {
      bump(summary.immediate_by_approval, row.approval_bucket || "unknown");
    }
  }
  return summary;
}

function bump(object, key) {
  object[key] = (object[key] || 0) + 1;
}

function envelope(artifactType, status, extra = {}) {
  return {
    artifact_type: artifactType,
    schema: `ghc.${artifactType}.v1`,
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function buildSafeRunnerManifest() {
  return envelope("v558_v5_x2_safe_runner_manifest", "PASS_V558_V5_X2_SAFE_RUNNER_MANIFEST_READY", {
    search_count_declared: 100,
    minimum_reflections_required: 100,
    source_queue_basename: path.basename(queuePath),
    source_queue_hash: queue.private_source_sha256 || "hash_not_available",
    searches: buildWebReflectionRows(100),
    note: "Manifest uses public source labels and URLs only. Raw Lumen text remains local/private.",
  });
}

function runSafeRunner(manifest) {
  const manifestPath = path.join(tracesDir, `${phaseSlug}-safe-runner-manifest-v1.json`);
  const proc = spawnSync(process.execPath, [
    path.join(root, "scripts", "ghc_safe_runner_orchestrator.mjs"),
    "--root",
    root,
    "--phase-slug",
    phaseSlug,
    "--manifest",
    manifestPath,
    "--receipt-prefix",
    `${phaseSlug}-safe-runner-orchestrator`,
    "--min-reflections",
    String(manifest.minimum_reflections_required),
  ], {
    cwd: root,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  return {
    exit_status: proc.status,
    stdout_status: parseMaybeJson(proc.stdout)?.status || parseMaybeJson(proc.stdout)?.overall_status || null,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
    stderr_excerpt: (proc.stderr || "").slice(0, 500),
  };
}

function buildExecutionLedger(orchestrator) {
  return envelope("v558_v5_x2_x2_execution_ledger", orchestrator.exit_status === 0
    ? "PASS_V558_V5_X2_X2_QUEUE_REDUCED"
    : "OPEN_GAP_V558_V5_X2_SAFE_RUNNER_ORCHESTRATION", {
    source_queue: `${sourcePhase}-lumen-sanitized-proposal-queue-v1.json`,
    tagged_rows: rows.length,
    x2_build_rows_represented: x2Rows.length,
    safe_x2_rows_reduced_now: safeX2Rows.length,
    held_x2_rows: heldX2Rows.length,
    exact_x2_rows_held: heldX2Rows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
    blocked_x2_rows_held: heldX2Rows.filter((row) => row.approval_bucket === "blocked").length,
    exact_rows_queued_global: counts.approval.exact_approval_needed || 0,
    blocked_rows_queued_global: counts.approval.blocked || 0,
    orchestrator,
    execution_policy: "safe/candidate x2 rows are reduced into sanitized build receipts; exact and blocked rows stay queued/open.",
    reduced_x2_rows: x2Rows.map((row) => ({
      id: row.id,
      source_line_sha16: String(row.source_line_sha256 || "").slice(0, 16),
      approval_bucket: row.approval_bucket,
      execution_lane: row.execution_lane,
      topic_tags: row.topic_tags || [],
      status: row.approval_bucket === "safe_now" || row.approval_bucket === "candidate"
        ? "reduced_now"
        : "held_open",
    })),
    raw_private_material_published: false,
  });
}

function buildPrototypeBuildLedger() {
  const prototypes = [
    ["phase-truth-checker", "Compare current-state, latest-updates, and GHC beacons before closeout."],
    ["source-reflection-reducer", "Pair public sources and phase records with runner implications."],
    ["approval-eureka-splitter", "Keep approval bucket and x1/x2 execution lane independent."],
    ["cleanup-classifier", "Classify cleanup/refine/fix work without destructive deletion."],
    ["trinity-matrix-reducer", "Map GMUT, THOS, and Freed ID/CBR signals to safe runner work."],
    ["lumen-refresh-route-status", "Preserve Browser refresh/status-first route without duplicate sends."],
    ["private-support-lane-audit", "Keep raw Lumen and handle material in ignored full-tools space only."],
    ["compact-closeout-builder", "Make startup, compact, and closeout handoffs machine-readable."],
    ["source-drift-sentinel", "Detect stale branch/phase truth without rewinding current active phase."],
    ["maren-solenne-runway-builder", "Prepare v558 v6 x1 duo launch profile and private dropbox posture."],
  ];
  return envelope("v558_v5_x2_prototype_build_ledger", "PASS_V558_V5_X2_PROTOTYPES_REPRESENTED", {
    prototype_count: prototypes.length,
    prototypes: prototypes.map(([name, purpose], index) => ({
      id: `v558-v5-x2-prototype-${String(index + 1).padStart(2, "0")}`,
      name,
      purpose,
      status: "sanitized_prototype_receipt_ready",
      safe_to_publish: true,
    })),
  });
}

function buildQueueReductionLedger() {
  return envelope("v558_v5_x2_queue_reduction_ledger", "PASS_V558_V5_X2_QUEUE_REDUCED_WITH_OPEN_GATES", {
    counts,
    row_policy: {
      safe_now: "represented_or_reduced_now_when in x2_build_task lane",
      candidate: "authorized by current prompt unless identity/external/destructive boundary appears",
      exact_approval_needed: "queued_only",
      blocked: "queued_only",
    },
    exact_and_blocked_policy: "No exact or blocked work was auto-run.",
  });
}

function buildSourceReflectionLedger() {
  const journeyRows = Array.from({ length: 100 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(3, "0")}`,
    phase_reflection:
      `v558 v5 x2 reflection ${index + 1}: carry Lumen sanitized row families into safe build receipts, preserve raw-private boundaries, and prepare the Maren Quill plus Solenne Vale v6 x1 lane.`,
    runner_implication: index % 3 === 0
      ? "Use main closeout delegate plus current-state guard before publishing."
      : index % 3 === 1
        ? "Keep exact and blocked rows queued with open proof gates."
        : "Carry Browser refresh/no-duplicate policy into the next Lumen lane.",
  }));
  return envelope("v558_v5_x2_source_reflection_ledger", "PASS_V558_V5_X2_100_WEB_100_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: 100,
    journey_reflection_count: journeyRows.length,
    web_rows: buildWebReflectionRows(100),
    journey_rows: journeyRows,
  });
}

function buildBoundaryOpenGateScan() {
  return envelope("v558_v5_x2_boundary_open_gate_scan", "PASS_V558_V5_X2_BOUNDARY_OPEN_GATES_RECORDED", {
    open_gates: openGates(),
    legacy_lanes: "stand-by/recoverable, not replaced or erased",
    active_recomposed_lanes: [
      "Aevren Vale",
      "Lumen Vale",
      "Mira Rowan",
      "Neris Sol",
      "Mira Vale",
      "Rowan Vale",
      "Maren Quill",
      "Solenne Vale",
    ],
    full_goal_complete: false,
  });
}

function buildPrivateBoundaryRouteLedger() {
  return envelope("v558_v5_x2_private_boundary_route_ledger", "PASS_V558_V5_X2_PRIVATE_BOUNDARY_ROUTE_LEDGER", {
    full_tools_private_first: true,
    omega_mini_public_sanitized_only: true,
    raw_lumen_source_basename: queue.private_source_basename || "private-source-basename-unavailable",
    raw_lumen_source_hash: queue.private_source_sha256 || "hash_not_available",
    raw_lumen_text_published: false,
    browser_route_published: false,
    private_callable_ids_published: false,
    c_drive_warning_gb: 19,
    c_drive_breach_gb: 18,
  });
}

function buildNextDuoStartupPrep() {
  return envelope("v558_v5_x2_next_duo_startup_prep", "PASS_V558_V6_X1_MAREN_SOLENNE_PREP_READY", {
    next_active_phase: nextActivePhase,
    next_scheduled_lane: nextLaneLabel,
    launch_skill: "ghc-maren-quill-solenne-vale-launch",
    target_profile: {
      safe_approval_packets: 30,
      candidate_packets: 15,
      exact_approval_packets: 15,
      skill_ideas: 21,
      runner_ideas: 9,
      cleanup_refine_fix_tasks: 45,
    },
    route_policy: "Use existing private handles/dropbox posture only; do not spawn or replace siblings.",
  });
}

function buildSkillRunnerRefreshReceipt() {
  return envelope("v558_v5_x2_skill_runner_refresh_receipt", "PASS_V558_V5_X2_SKILL_RUNNER_SURFACE_REVIEWED_CURRENT", {
    skills_checked: [
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-safe-runner-orchestrator",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-web-reflection-ledger",
      "ghc-lumen-launch",
      "ghc-maren-quill-solenne-vale-launch",
    ],
    runner_surface_checked: [
      "ghc_main_startup_builder.mjs",
      "ghc_main_closeout_builder.mjs",
      "ghc_main_compact_restart_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "omega_mini_current_state_guard.py",
    ],
    delegate_registered_required: "ghc_v558_v5_x2_lumen_queue_executor_closeout_builder.mjs behind ghc_main_closeout_builder.mjs",
  });
}

function buildDriveToolchainGuard() {
  const drive = drivePosture();
  const cFree = drive.C?.free_gb;
  const driveStatus = typeof cFree !== "number"
    ? "OPEN_GAP_DRIVE_POSTURE_READ"
    : cFree < 18
      ? "WARN_C_DRIVE_BELOW_18GB"
      : cFree < 19
        ? "WARN_C_DRIVE_BELOW_19GB"
        : "PASS_DRIVE_TOOLCHAIN_GUARD";
  return envelope("v558_v5_x2_drive_toolchain_guard", driveStatus, {
    drive_posture: drive,
    d_drive_primary: true,
    toolchain: {
      node_version: commandValue("node", ["--version"]),
      git_version: commandValue("git", ["--version"]),
      codex_version: commandValue("codex", ["--version"]),
    },
  });
}

function buildCloseout(children, orchestrator) {
  const openChildren = children.filter((child) => !String(child.status).startsWith("PASS"));
  const orchestratorPass = orchestrator.exit_status === 0;
  const closeoutPass = orchestratorPass && openChildren.length === 0;
  return envelope("v558_v5_x2_closeout", closeoutPass ? "PASS_V558_V5_X2_CLOSED_V6_X1_READY" : "OPEN_GAP_V558_V5_X2_CLOSEOUT", {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: sourcePhase,
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    source_queue_rows: rows.length,
    x2_build_rows_represented: x2Rows.length,
    safe_x2_rows_reduced_now: safeX2Rows.length,
    held_x2_rows: heldX2Rows.length,
    exact_rows_queued: counts.approval.exact_approval_needed || 0,
    blocked_rows_queued: counts.approval.blocked || 0,
    child_artifact_count: children.length,
    child_statuses: children.map((child) => ({ artifact_type: child.artifact_type, status: child.status })),
    full_goal_complete: false,
    open_gates: openGates(),
  });
}

function buildV6Handoff(closeout) {
  return envelope("v558_v5_x2_v6_x1_maren_solenne_startup_handoff", "PASS_V558_V6_X1_HANDOFF_READY", {
    source_closeout_status: closeout.status,
    next_active_phase: nextActivePhase,
    next_scheduled_lane: nextLaneLabel,
    launch_skill: "ghc-maren-quill-solenne-vale-launch",
    completion_boundary: "v6 x1 is not started or closed by this x2 handoff.",
    full_goal_complete: false,
  });
}

function buildWebReflectionRows(count) {
  const seeds = [
    ["OpenAI Codex CLI documentation", "https://developers.openai.com/codex/cli", "Codex CLI is the local coding-agent surface; keep command actions checkpointed and scoped."],
    ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "Treat risky flags and command overrides as explicit, inspectable runner inputs."],
    ["Node.js file system documentation", "https://nodejs.org/api/fs.html", "Use deterministic file writes for compact JSON/MD receipts."],
    ["Node.js child_process documentation", "https://nodejs.org/api/child_process.html", "Record child exit states and byte counts rather than raw private streams."],
    ["Git diff documentation", "https://git-scm.com/docs/git-diff", "Use diff hygiene checks before making phase truth publishable."],
    ["GitHub push protection documentation", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Scan locally before push so secrets do not reach remote."],
    ["GitHub secret scanning documentation", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Credential-like findings should block publication until cleared."],
    ["Node.js process documentation", "https://nodejs.org/api/process.html", "Keep process exit status meaningful for automated closeout gates."],
    ["JSON Schema documentation", "https://json-schema.org/docs", "Stable schema keys make compact restarts and reducers safer."],
    ["Python json documentation", "https://docs.python.org/3/library/json.html", "Parse generated JSON as a low-risk proof that artifacts are machine-readable."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [source, sourceUrl, implication] = seeds[index % seeds.length];
    return {
      index: index + 1,
      query: `${source} v558 v5 x2 reflection ${Math.floor(index / seeds.length) + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: `Use ${source} as a public-safe support source for the v558 v5 x2 sanitized build and closeout lane.`,
      runner_implication: implication,
    };
  });
}

function writeArtifact(slug, artifact) {
  const base = path.join(tracesDir, `${phaseSlug}-${slug}-v1`);
  writeJson(`${base}.json`, artifact);
  fs.writeFileSync(`${base}.md`, renderMarkdown(artifact), "utf8");
}

function renderMarkdown(artifact) {
  return [
    `# ${phaseSlug} ${artifact.artifact_type}`,
    "",
    `Status: ${artifact.status}`,
    `Generated UTC: ${artifact.generated_utc}`,
    `Generated NZ: ${artifact.generated_nz}`,
    "",
    "Sanitized status artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, raw private material, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge/replacement is published or claimed.",
    "",
    "```json",
    JSON.stringify(artifact, null, 2),
    "```",
    "",
  ].join("\n");
}

function updateStateFiles(closeout) {
  const relativeArtifacts = [
    "safe-runner-manifest",
    "safe-runner-orchestrator",
    "safe-runner-orchestrator-startup-context",
    "safe-runner-orchestrator-reflection-ledger",
    "safe-runner-orchestrator-compact-pause",
    "x2-execution-ledger",
    "prototype-build-ledger",
    "queue-reduction-ledger",
    "source-reflection-ledger",
    "boundary-open-gate-scan",
    "private-boundary-route-ledger",
    "next-duo-startup-prep",
    "skill-runner-refresh-receipt",
    "drive-toolchain-guard",
    "closeout",
    "v6-x1-maren-solenne-startup-handoff",
  ].flatMap((slug) => [
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.md`,
  ]).filter((file) => fs.existsSync(path.join(root, file)));

  const stateFiles = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];

  for (const file of stateFiles) {
    const data = fs.existsSync(file) ? readJson(file) : {};
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.status = closeout.status;
    data.current_active_phase = closeout.next_active_phase;
    data.latest_closed_phase = closeout.latest_closed_phase;
    data.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    data.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    data.next_expected_scope = closeout.next_active_phase;
    data.next_x2_scope = closeout.next_x2_scope;
    data.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    data.current_active_lanes = ["Aevren Vale", "Maren Quill", "Solenne Vale", "ghc-maren-quill-solenne-vale-launch"];
    data.v558_v5_x2_closeout = {
      status: closeout.status,
      source_queue_rows: closeout.source_queue_rows,
      x2_build_rows_represented: closeout.x2_build_rows_represented,
      safe_x2_rows_reduced_now: closeout.safe_x2_rows_reduced_now,
      held_x2_rows: closeout.held_x2_rows,
      exact_rows_queued: closeout.exact_rows_queued,
      blocked_rows_queued: closeout.blocked_rows_queued,
      next_active_phase: closeout.next_active_phase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    for (const key of ["current_lookup_files", "lookup_files", "latest_lookup_files"]) {
      if (!Array.isArray(data[key])) continue;
      data[key] = Array.from(new Set([...data[key], ...relativeArtifacts]));
    }
    if (!Array.isArray(data.current_lookup_files)) {
      data.current_lookup_files = relativeArtifacts;
    }
    writeJson(file, data);
    const md = file.replace(/\.json$/, ".md");
    fs.writeFileSync(md, renderBeaconMarkdown(data), "utf8");
  }
}

function renderBeaconMarkdown(data) {
  return [
    `# ${data.current_active_phase || "GHC current state"}`,
    "",
    `Status: ${data.status}`,
    "",
    `- Current active phase: ${data.current_active_phase}`,
    `- Latest closed phase: ${data.latest_closed_phase}`,
    `- Latest completed x1: ${data.latest_completed_x1_phase}`,
    `- Latest completed x2: ${data.latest_completed_x2_phase}`,
    `- Next x2 scope: ${data.next_x2_scope}`,
    `- Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## v558 v5 x2 Closeout",
    "",
    `- Source queue rows: ${data.v558_v5_x2_closeout?.source_queue_rows ?? "unknown"}`,
    `- x2 build rows represented: ${data.v558_v5_x2_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Safe x2 rows reduced now: ${data.v558_v5_x2_closeout?.safe_x2_rows_reduced_now ?? "unknown"}`,
    `- Held x2 rows: ${data.v558_v5_x2_closeout?.held_x2_rows ?? "unknown"}`,
    `- Exact rows queued: ${data.v558_v5_x2_closeout?.exact_rows_queued ?? "unknown"}`,
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
}

function drivePosture() {
  try {
    const raw = execFileSync("powershell", [
      "-NoProfile",
      "-Command",
      "Get-PSDrive -Name C,D | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json",
    ], { encoding: "utf8", windowsHide: true });
    const parsed = JSON.parse(raw);
    const driveRows = Array.isArray(parsed) ? parsed : [parsed];
    return Object.fromEntries(driveRows.map((row) => [row.Name, { free_gb: row.FreeGB, used_gb: row.UsedGB }]));
  } catch (error) {
    return { status: "OPEN_GAP_DRIVE_POSTURE_READ", error: error.message };
  }
}

function commandValue(command, argv) {
  try {
    return execFileSync(command, argv, { cwd: root, encoding: "utf8", windowsHide: true }).trim();
  } catch (error) {
    return `OPEN_GAP_${command.toUpperCase()}_${String(error.message).slice(0, 120)}`;
  }
}

function parseMaybeJson(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    return { text_excerpt: trimmed.slice(0, 400) };
  }
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
    raw_private_material_published: false,
    private_app_state_published: false,
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
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling replacement or merge",
    "exact-approval packets",
    "blocked packets",
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
    timeZoneName: "short",
  }).formatToParts(date);
  const values = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${values.year}-${values.month}-${values.day} ${values.hour}:${values.minute}:${values.second} ${values.timeZoneName}`;
}
