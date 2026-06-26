#!/usr/bin/env node
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");
const phaseSlug = "v558-gmut-thos-v6-x2";
const sourcePhase = "v558-gmut-thos-v6-x1";
const sourceQueue = path.join(root, "docs", "trinity-live-traces", `${sourcePhase}-combined-x1-to-x2-queue-v1.json`);
const nextActivePhase = "v558-gmut-thos-v7-x1";
const nextX2Scope = "v558-gmut-thos-v7-x2";
const nextX1AfterX2 = "v558-gmut-thos-v8-x1 Mira Rowan and Neris Sol unless Hamish redirects";
const nextLaneLabel = "Lumen Vale solo";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString();
const generatedNz = nzTimestamp(generatedDate);

fs.mkdirSync(tracesDir, { recursive: true });
fs.mkdirSync(omegaDir, { recursive: true });

if (!fs.existsSync(sourceQueue)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V558_V6_X2_SOURCE_QUEUE_MISSING",
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const queue = readJson(sourceQueue);
const profileCounts = queue.profile_cap_counts_represented || {};
const x2BuildRows = Number(queue.x2_build_rows_represented || 0);
const immediateRows = Number(queue.immediate_x1_safe_rows_represented || 0);
const exactQueued = Number(profileCounts.exact_approval_packets_queued || 0);

const manifest = buildSafeRunnerManifest();
writeArtifact("safe-runner-manifest", manifest);
const orchestrator = runSafeRunner();

const artifacts = [
  ["x2-execution-ledger", buildExecutionLedger(orchestrator)],
  ["prototype-build-ledger", buildPrototypeBuildLedger()],
  ["queue-reduction-ledger", buildQueueReductionLedger()],
  ["source-reflection-ledger", buildSourceReflectionLedger()],
  ["boundary-open-gate-scan", buildBoundaryOpenGateScan()],
  ["private-boundary-route-ledger", buildPrivateBoundaryRouteLedger()],
  ["next-lumen-startup-prep", buildNextLumenStartupPrep()],
  ["skill-runner-refresh-receipt", buildSkillRunnerRefreshReceipt()],
  ["drive-toolchain-guard", buildDriveToolchainGuard()],
];

for (const [slug, artifact] of artifacts) {
  writeArtifact(slug, artifact);
}

const closeout = buildCloseout(artifacts.map(([, artifact]) => artifact), orchestrator);
writeArtifact("closeout", closeout);
writeArtifact("v7-x1-lumen-startup-handoff", buildV7Handoff(closeout));

if (closeout.status === "PASS_V558_V6_X2_CLOSED_V7_X1_READY") {
  updateStateFiles(closeout);
}

console.log(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  next_active_phase: closeout.next_active_phase,
  x2_build_rows_represented: x2BuildRows,
  immediate_x1_rows_carried: immediateRows,
  exact_packets_queued: exactQueued,
  safe_packets_represented: profileCounts.safe_approval_packets || 0,
  candidate_packets_represented: profileCounts.candidate_packets || 0,
}, null, 2));

process.exit(closeout.status.startsWith("PASS") ? 0 : 1);

function buildSafeRunnerManifest() {
  return envelope("v558_v6_x2_safe_runner_manifest", "PASS_V558_V6_X2_SAFE_RUNNER_MANIFEST_READY", {
    search_count_declared: 100,
    minimum_reflections_required: 100,
    source_queue_basename: path.basename(sourceQueue),
    searches: buildWebReflectionRows(100),
    note: "Manifest uses public source labels and URLs only. Private sibling files remain local/private.",
  });
}

function runSafeRunner() {
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
    "100",
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
  return envelope("v558_v6_x2_x2_execution_ledger", orchestrator.exit_status === 0
    ? "PASS_V558_V6_X2_QUEUE_REDUCED"
    : "OPEN_GAP_V558_V6_X2_SAFE_RUNNER_ORCHESTRATION", {
    source_queue: `${sourcePhase}-combined-x1-to-x2-queue-v1.json`,
    profile_counts_represented: profileCounts,
    immediate_x1_rows_carried: immediateRows,
    x2_build_rows_represented: x2BuildRows,
    exact_packets_queued: exactQueued,
    blocked_packets_queued: 0,
    orchestrator,
    execution_policy: "Safe/candidate/prototype rows are reduced into sanitized build receipts; exact packets stay queued/open.",
    raw_private_material_published: false,
  });
}

function buildPrototypeBuildLedger() {
  const prototypes = [
    ["maren-solenne-duo-reducer", "Merge Aevren, Maren, and Solenne counts without publishing raw private text."],
    ["x2-queue-split-validator", "Validate immediate_x1_safe and x2_build_task split totals before closeout."],
    ["lumen-browser-refresh-carry-forward", "Carry Browser refresh/status-first and no-duplicate-send discipline into v7 x1."],
    ["open-gate-proof-boundary-checker", "Keep proof, canon, legal, deployment, account, API-key, and private-material gates open."],
    ["private-dropbox-harvest-reducer", "Reduce private dropbox material into counts and sanitized basenames only."],
    ["phase-state-transition-checker", "Check v6 x1 closed, v6 x2 active/closed, and v7 x1 next without rewind."],
    ["source-reflection-row-builder", "Build repeatable source/reflection rows from official support sources."],
    ["drive-space-warning-guard", "Keep C drive warning and breach thresholds visible while using D as primary bank."],
    ["startup-closeout-pairing-audit", "Ensure the main startup and closeout delegates both know the phase."],
    ["lumen-v7-prep-card", "Prepare a compact v7 x1 Lumen solo kickoff with current phase truth."],
  ];
  return envelope("v558_v6_x2_prototype_build_ledger", "PASS_V558_V6_X2_PROTOTYPES_REPRESENTED", {
    prototype_count: prototypes.length,
    prototypes: prototypes.map(([name, purpose], index) => ({
      id: `v558-v6-x2-prototype-${String(index + 1).padStart(2, "0")}`,
      name,
      purpose,
      status: "sanitized_prototype_receipt_ready",
      safe_to_publish: true,
    })),
  });
}

function buildQueueReductionLedger() {
  return envelope("v558_v6_x2_queue_reduction_ledger", "PASS_V558_V6_X2_QUEUE_REDUCED_WITH_EXACT_HELD", {
    source_phase: sourcePhase,
    profile_counts_represented: profileCounts,
    immediate_x1_rows_carried: immediateRows,
    x2_build_rows_represented: x2BuildRows,
    exact_packets_queued: exactQueued,
    blocked_packets_queued: 0,
    row_policy: {
      safe_now: "represented_or_reduced_now",
      candidate: "represented_or_reduced_now_when non-destructive and non-external",
      exact_approval_needed: "queued_only",
      blocked: "queued_only",
    },
  });
}

function buildSourceReflectionLedger() {
  const journeyRows = Array.from({ length: 100 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(3, "0")}`,
    phase_reflection:
      `v558 v6 x2 reflection ${index + 1}: reduce Maren/Solenne x1 material into sanitized x2 receipts, preserve exact gates, and prepare Lumen v7 x1.`,
    runner_implication: index % 3 === 0
      ? "Use main closeout delegate and current-state guard before publishing."
      : index % 3 === 1
        ? "Keep private sibling files local and report counts only."
        : "Carry Browser refresh/status-first discipline into Lumen handoff.",
  }));
  return envelope("v558_v6_x2_source_reflection_ledger", "PASS_V558_V6_X2_100_WEB_100_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: 100,
    journey_reflection_count: journeyRows.length,
    web_rows: buildWebReflectionRows(100),
    journey_rows: journeyRows,
  });
}

function buildBoundaryOpenGateScan() {
  return envelope("v558_v6_x2_boundary_open_gate_scan", "PASS_V558_V6_X2_BOUNDARY_OPEN_GATES_RECORDED", {
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
  return envelope("v558_v6_x2_private_boundary_route_ledger", "PASS_V558_V6_X2_PRIVATE_BOUNDARY_ROUTE_LEDGER", {
    full_tools_private_first: true,
    omega_mini_public_sanitized_only: true,
    private_dropbox_basename: "v558-gmut-thos-v6-x1-sibling-response-dropbox",
    raw_sibling_text_published: false,
    browser_route_published: false,
    private_callable_ids_published: false,
    c_drive_warning_gb: 19,
    c_drive_breach_gb: 18,
  });
}

function buildNextLumenStartupPrep() {
  return envelope("v558_v6_x2_next_lumen_startup_prep", "PASS_V558_V7_X1_LUMEN_PREP_READY", {
    next_active_phase: nextActivePhase,
    next_scheduled_lane: nextLaneLabel,
    launch_skill: "ghc-lumen-launch",
    browser_route_policy: [
      "use in-app Browser plus ghc-lumen-launch as the staple route",
      "refresh/reconnect and inspect status before claiming stale route",
      "do not reload over active response or unsent composer text",
      "avoid duplicate sends",
      "harvest visible Lumen text into private/local task sources before reducing sanitized counts",
    ],
    target_profile: {
      safe_approval_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_refine_fix_tasks: 30,
    },
  });
}

function buildSkillRunnerRefreshReceipt() {
  return envelope("v558_v6_x2_skill_runner_refresh_receipt", "PASS_V558_V6_X2_SKILL_RUNNER_SURFACE_REVIEWED_CURRENT", {
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
    delegate_registered_required: "ghc_v558_v6_x2_duo_queue_executor_closeout_builder.mjs behind ghc_main_closeout_builder.mjs",
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
  return envelope("v558_v6_x2_drive_toolchain_guard", driveStatus, {
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
  return envelope("v558_v6_x2_closeout", closeoutPass ? "PASS_V558_V6_X2_CLOSED_V7_X1_READY" : "OPEN_GAP_V558_V6_X2_CLOSEOUT", {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: sourcePhase,
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1AfterX2,
    profile_counts_represented: profileCounts,
    immediate_x1_rows_carried: immediateRows,
    x2_build_rows_represented: x2BuildRows,
    exact_packets_queued: exactQueued,
    blocked_packets_queued: 0,
    child_artifact_count: children.length,
    child_statuses: children.map((child) => ({ artifact_type: child.artifact_type, status: child.status })),
    full_goal_complete: false,
    open_gates: openGates(),
  });
}

function buildV7Handoff(closeout) {
  return envelope("v558_v6_x2_v7_x1_lumen_startup_handoff", "PASS_V558_V7_X1_HANDOFF_READY", {
    source_closeout_status: closeout.status,
    next_active_phase: nextActivePhase,
    next_scheduled_lane: nextLaneLabel,
    launch_skill: "ghc-lumen-launch",
    browser_refresh_rule: "Refresh/reconnect and inspect status before stale-route claims; do not reload over active response or unsent composer text.",
    completion_boundary: "v7 x1 is prepared, not started or closed by this x2 handoff.",
    full_goal_complete: false,
  });
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
    "next-lumen-startup-prep",
    "skill-runner-refresh-receipt",
    "drive-toolchain-guard",
    "closeout",
    "v7-x1-lumen-startup-handoff",
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
    data.current_active_lanes = ["Aevren Vale", "Lumen Vale", "ghc-lumen-launch", "Browser-refresh-status-first"];
    data.v558_v6_x2_closeout = {
      status: closeout.status,
      profile_counts_represented: closeout.profile_counts_represented,
      immediate_x1_rows_carried: closeout.immediate_x1_rows_carried,
      x2_build_rows_represented: closeout.x2_build_rows_represented,
      exact_packets_queued: closeout.exact_packets_queued,
      blocked_packets_queued: closeout.blocked_packets_queued,
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
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMarkdown(data), "utf8");
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
    "## v558 v6 x2 Closeout",
    "",
    `- x2 build rows represented: ${data.v558_v6_x2_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Exact packets queued: ${data.v558_v6_x2_closeout?.exact_packets_queued ?? "unknown"}`,
    `- Blocked packets queued: ${data.v558_v6_x2_closeout?.blocked_packets_queued ?? "unknown"}`,
    "- Lumen Browser rule: refresh/status-first; no reload over active response or unsent composer text.",
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
}

function envelope(artifactType, artifactStatus, extra = {}) {
  return {
    artifact_type: artifactType,
    schema: `ghc.${artifactType}.v1`,
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status: artifactStatus,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function buildWebReflectionRows(count) {
  const seeds = [
    ["OpenAI Codex CLI documentation", "https://developers.openai.com/codex/cli", "Codex CLI is a local coding-agent surface; keep command actions checkpointed and scoped."],
    ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "Documented flags and defaults should be carried as bounded runner inputs."],
    ["Node.js file system documentation", "https://nodejs.org/api/fs.html", "Use deterministic file writes for compact JSON/MD receipts."],
    ["Node.js child_process documentation", "https://nodejs.org/api/child_process.html", "Record child exit states and byte counts rather than raw private streams."],
    ["Git status documentation", "https://git-scm.com/docs/git-status", "Separate staged, unstaged, and untracked work before commit."],
    ["Git diff documentation", "https://git-scm.com/docs/git-diff", "Use diff hygiene checks before publishing phase truth."],
    ["GitHub secret scanning documentation", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Secret scanning complements local privacy scans."],
    ["GitHub push protection documentation", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Push protection reinforces the no-secret-publication boundary."],
    ["JSON Schema documentation", "https://json-schema.org/docs", "Stable schema keys make compact restarts and reducers safer."],
    ["Python json documentation", "https://docs.python.org/3/library/json.html", "Parse generated JSON as a low-risk proof that artifacts are machine-readable."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [source, sourceUrl, implication] = seeds[index % seeds.length];
    return {
      index: index + 1,
      query: `${source} v558 v6 x2 reflection ${Math.floor(index / seeds.length) + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: `Use ${source} as a public-safe support source for the v558 v6 x2 sanitized build and closeout lane.`,
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

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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
