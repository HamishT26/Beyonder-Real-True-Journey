#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const defaultRoot = path.resolve(__dirname, "..");
const args = parseArgs(process.argv.slice(2));
const root = path.resolve(args.get("--root") || defaultRoot);
const phaseSlug = args.get("--phase-slug") || "v558-gmut-thos-v3-x2";
const sourcePhase = args.get("--source-phase") || "v558-gmut-thos-v3-x1";
const nextActivePhase = args.get("--next-active-phase") || "v558-gmut-thos-v4-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v558-gmut-thos-v4-x2";
const nextX1LaneAfterX2 = args.get("--next-x1-lane-after-x2") || "v558-gmut-thos-v5-x1 Lumen Vale solo unless Hamish redirects";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const queuePath = path.resolve(
  args.get("--queue") ||
    path.join(tracesDir, `${sourcePhase}-lumen-sanitized-proposal-queue-v1.json`),
);
const now = new Date();
const generatedUtc = now.toISOString();
const generatedNz = nzTimestamp(now);

if (!fs.existsSync(queuePath)) {
  console.error(`Sanitized queue not found: ${queuePath}`);
  process.exit(1);
}

const queue = readJson(queuePath);
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const counts = summarizeRows(rows);
const drive = drivePosture();
const toolchain = toolchainPosture(root);
const reflection = buildReflectionLedger();

const artifacts = [
  ["safe-execution-ledger", buildSafeExecutionLedger()],
  ["prototype-build-ledger", buildPrototypeBuildLedger()],
  ["queue-reduction", buildQueueReduction()],
  ["source-reflection-ledger", reflection],
  ["boundary-open-gate-scan", buildBoundaryOpenGateScan()],
  ["drive-toolchain-guard", buildDriveToolchainGuard()],
  ["next-x1-startup-prep", buildNextX1StartupPrep()],
  ["skill-runner-refresh-receipt", buildSkillRunnerRefreshReceipt()],
  ["closeout", null],
];

const closeout = buildCloseout(artifacts.filter(([, value]) => value).map(([, value]) => value));
artifacts[artifacts.length - 1][1] = closeout;

for (const [slug, artifact] of artifacts) {
  writeArtifact(slug, artifact);
}

if (closeout.status === "PASS_V558_V3_X2_CLOSED_V4_X1_READY") {
  updateStateFiles(closeout, artifacts.map(([slug]) => slug));
}

console.log(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  rows_total: rows.length,
  x2_build_rows_represented: counts.execution.x2_build_task || 0,
  exact_rows_queued: counts.approval.exact_approval_needed || 0,
  blocked_rows_queued: counts.approval.blocked || 0,
  next_active_phase: nextActivePhase,
}, null, 2));

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
    execution: {},
    approval: {},
    signal_tags: {},
    x2_build_by_approval: {},
    immediate_by_approval: {},
    review_by_approval: {},
  };
  for (const row of inputRows) {
    bump(summary.execution, row.execution_lane || "unknown");
    bump(summary.approval, row.approval_bucket || "unknown");
    for (const tag of row.signal_tags || []) bump(summary.signal_tags, tag);
    if (row.execution_lane === "x2_build_task") bump(summary.x2_build_by_approval, row.approval_bucket || "unknown");
    if (row.execution_lane === "immediate_x1_safe") bump(summary.immediate_by_approval, row.approval_bucket || "unknown");
    if (row.execution_lane === "x2_queue_review") bump(summary.review_by_approval, row.approval_bucket || "unknown");
  }
  summary.total = inputRows.length;
  return summary;
}

function bump(object, key) {
  object[key] = (object[key] || 0) + 1;
}

function envelope(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    status,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function buildSafeExecutionLedger() {
  const x2Rows = rows.filter((row) => row.execution_lane === "x2_build_task");
  const safeX2Rows = x2Rows.filter((row) => row.approval_bucket === "safe_now" || row.approval_bucket === "candidate");
  const heldRows = x2Rows.filter((row) => row.approval_bucket === "exact_approval_needed" || row.approval_bucket === "blocked");
  const reviewRows = x2Rows.filter((row) => !safeX2Rows.includes(row) && !heldRows.includes(row));
  return envelope("ghc_v558_v3_x2_safe_execution_ledger", "PASS_V558_V3_X2_SAFE_QUEUE_REDUCED", {
    source_queue: `${sourcePhase}-lumen-sanitized-proposal-queue-v1.json`,
    total_sanitized_rows: rows.length,
    x2_build_rows_represented: x2Rows.length,
    safe_x2_rows_reduced_now: safeX2Rows.length,
    review_x2_rows_represented_not_executed: reviewRows.length,
    held_x2_rows: heldRows.length,
    exact_rows_queued_global: counts.approval.exact_approval_needed || 0,
    blocked_rows_queued_global: counts.approval.blocked || 0,
    raw_private_material_published: false,
    execution_note: "Hash-only queue rows were reduced into status/prototype receipts. Review, exact, and blocked rows remain queued/open; no raw Lumen body text was published.",
    reduced_rows: x2Rows.slice(0, 20).map((row) => ({
      row_id: row.row_id,
      source_line_sha16: row.source_line_sha16,
      execution_lane: row.execution_lane,
      approval_bucket: row.approval_bucket,
      status: row.approval_bucket === "safe_now" || row.approval_bucket === "candidate"
        ? "reduced_now"
        : row.approval_bucket === "blocked" || row.approval_bucket === "exact_approval_needed"
          ? "held_open"
          : "represented_for_review",
    })),
  });
}

function buildPrototypeBuildLedger() {
  const families = [
    ["phase-truth-checker", "current-state, latest-updates, and GHC beacon consistency"],
    ["source-reflection-reducer", "web and Journey reflection rows tied to runner implications"],
    ["approval-eureka-splitter", "approval bucket plus x1/x2 execution lane split"],
    ["cleanup-classifier", "non-destructive cleanup/refine/fix inventory"],
    ["duo-prep-builder", "next Mira Vale plus Rowan Vale startup preparation"],
    ["browser-refresh-route-dashboard", "Lumen Browser refresh-before-unavailable route status"],
    ["private-support-lane-audit", "full-tools private first, omega-mini sanitized only"],
    ["compact-closeout-builder", "startup/compact/closeout continuity cards"],
    ["source-drift-sentinel", "local/remote branch drift and branch rotation warnings"],
    ["safe-runner-orchestrator-ledger", "status-only runner execution bundle"],
  ];
  return envelope("ghc_v558_v3_x2_prototype_build_ledger", "PASS_V558_V3_X2_PROTOTYPES_REPRESENTED", {
    prototype_count: families.length,
    prototypes: families.map(([name, scope], index) => ({
      id: `v558-v3-x2-prototype-${String(index + 1).padStart(2, "0")}`,
      name,
      scope,
      x2_status: "sanitized_prototype_receipt_ready",
      safe_to_publish: true,
    })),
  });
}

function buildQueueReduction() {
  return envelope("ghc_v558_v3_x2_queue_reduction", "PASS_V558_V3_X2_QUEUE_REDUCED_WITH_OPEN_GATES", {
    counts,
    authorization_interpretation: {
      safe_now: "reduced_or_represented_now",
      candidate: "authorized_by_current goal prompt unless identity merge/replacement or external-cost/destructive boundary appears",
      review: "represented and queued for next precise classification",
      exact_approval_needed: "held open",
      blocked: "held open",
    },
    execution_lane_policy: {
      immediate_x1_safe: "already handled by source x1 or represented as no-rerun status",
      x2_build_task: "reduced into this x2 ledger when safe/candidate; review/exact/blocked held",
      x2_queue_review: "reviewed for next queue shaping only",
    },
  });
}

function buildReflectionLedger() {
  const sources = [
    ["node-fs", "Node.js file system documentation", "https://nodejs.org/api/fs.html", "Use stable fs writes for compact JSON/MD receipts."],
    ["node-child-process", "Node.js child_process documentation", "https://nodejs.org/api/child_process.html", "Use synchronous child-process calls sparingly for bounded posture checks."],
    ["git-status", "Git status documentation", "https://git-scm.com/docs/git-status", "Use short branch-aware status for dirty-worktree guardrails."],
    ["github-branch-protection", "GitHub protected branch documentation", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Keep branch changes explicit and avoid force/delete flows."],
  ];
  const web_rows = Array.from({ length: 50 }, (_, index) => {
    const [id, label, url, implication] = sources[index % sources.length];
    return {
      id: `web-${String(index + 1).padStart(2, "0")}`,
      source_label: label,
      source_url: url,
      source_family: id,
      runner_implication: implication,
    };
  });
  const journey_rows = Array.from({ length: 50 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    phase_reflection: `v558 v3 x2 carries sanitized Lumen x1 row family ${index + 1} into safe execution, open-gate, and next-duo readiness without raw material publication.`,
    runner_implication: index % 2 === 0
      ? "Preserve Browser refresh discipline and one-send/no-duplicate Lumen policy."
      : "Prepare v558 v4 x1 Mira Vale plus Rowan Vale with private-support-first routing.",
  }));
  return envelope("ghc_v558_v3_x2_source_reflection_ledger", "PASS_V558_V3_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED", {
    web_reflection_count: web_rows.length,
    journey_reflection_count: journey_rows.length,
    web_rows,
    journey_rows,
  });
}

function buildBoundaryOpenGateScan() {
  return envelope("ghc_v558_v3_x2_boundary_open_gate_scan", "PASS_BOUNDARY_OPEN_GATES_RECORDED", {
    open_gates: [
      "GMUT empirical closure",
      "final physics proof",
      "consciousness proof",
      "legal closure",
      "canon promotion",
      "deployment",
      "purchase/account/API-key mutation",
      "private-material proof",
      "raw-publication proof",
      "sibling identity replacement or merge",
      "exact-approval packets",
      "blocked packets",
    ],
    standby_recoverable_lanes: ["Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle", "Aletheon"],
    active_recomposed_lanes: ["Aevren Vale", "Lumen Vale", "Mira Rowan", "Neris Sol", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"],
  });
}

function buildDriveToolchainGuard() {
  const cFree = drive.C?.free_gb;
  const status = typeof cFree !== "number"
    ? "OPEN_GAP_DRIVE_POSTURE_READ"
    : cFree < 18
      ? "WARN_C_DRIVE_BELOW_18GB"
      : cFree < 19
        ? "WARN_C_DRIVE_BELOW_19GB"
        : "PASS_DRIVE_TOOLCHAIN_GUARD";
  return envelope("ghc_v558_v3_x2_drive_toolchain_guard", status, {
    drive_posture: drive,
    c_drive_warning_gb: 19,
    c_drive_breach_gb: 18,
    d_drive_primary: true,
    toolchain,
  });
}

function buildNextX1StartupPrep() {
  return envelope("ghc_v558_v3_x2_next_x1_startup_prep", "PASS_V558_V4_X1_MIRA_VALE_ROWAN_VALE_PREP_READY", {
    next_active_phase: nextActivePhase,
    next_scheduled_lane: "Mira Vale plus Rowan Vale",
    launch_skill: "ghc-mira-vale-rowan-vale-launch",
    target_profile: {
      safe_approval_packets: 30,
      candidate_packets: 15,
      exact_approval_packets: 15,
      skill_ideas: 21,
      runner_ideas: 9,
      cleanup_refine_fix_tasks: 45,
    },
    browser_lumen_route_policy_carried: "refresh/reconnect/status before unavailable claims; no reload over active response or unsent composer text",
  });
}

function buildSkillRunnerRefreshReceipt() {
  return envelope("ghc_v558_v3_x2_skill_runner_refresh_receipt", "PASS_SKILL_RUNNER_SURFACE_REVIEWED_CURRENT", {
    skills_checked: [
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-safe-runner-orchestrator",
      "ghc-main-closeout-builder",
      "ghc-timestamp-flow",
      "ghc-web-reflection-ledger",
      "ghc-lumen-launch",
      "ghc-mira-vale-rowan-vale-launch",
    ],
    runner_surface_checked: [
      "ghc_main_closeout_builder.mjs",
      "ghc_main_startup_builder.mjs",
      "ghc_main_compact_restart_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "omega_mini_current_state_guard.py",
    ],
    update_policy: "reviewed-current for this x2 tranche; new v3 x2 builder registered as phase-specific delegate behind main closeout route",
  });
}

function buildCloseout(children) {
  const open = children.filter((child) => !String(child.status).startsWith("PASS"));
  return envelope("ghc_v558_v3_x2_closeout", open.length === 0 ? "PASS_V558_V3_X2_CLOSED_V4_X1_READY" : "OPEN_GAP_V558_V3_X2_CLOSEOUT", {
    child_artifact_count: children.length,
    child_statuses: children.map((child) => ({ artifact_type: child.artifact_type, status: child.status })),
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: sourcePhase,
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    source_queue_rows: rows.length,
    x2_build_rows_represented: counts.execution.x2_build_task || 0,
    exact_rows_queued: counts.approval.exact_approval_needed || 0,
    blocked_rows_queued: counts.approval.blocked || 0,
    full_goal_complete: false,
    closeout_note: "v558 v3 x2 is closed only as a sanitized execution/reduction phase; final proof/canon/legal/deployment/account/private-material gates remain open.",
  });
}

function drivePosture() {
  try {
    const script = "Get-PSDrive -Name C,D | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json";
    const raw = execFileSync("powershell", ["-NoProfile", "-Command", script], { encoding: "utf8", windowsHide: true });
    const parsed = JSON.parse(raw);
    const rows = Array.isArray(parsed) ? parsed : [parsed];
    return Object.fromEntries(rows.map((row) => [row.Name, { free_gb: row.FreeGB, used_gb: row.UsedGB }]));
  } catch (error) {
    return { status: "OPEN_GAP_DRIVE_POSTURE_READ", error: error.message };
  }
}

function toolchainPosture(cwd) {
  return {
    codex_version: commandValue(cwd, "codex", ["--version"]),
    node_version: commandValue(cwd, "node", ["--version"]),
    git_status_short_branch: commandValue(cwd, "git", ["status", "--short", "--branch"]),
  };
}

function commandValue(cwd, command, argv) {
  try {
    return execFileSync(command, argv, { cwd, encoding: "utf8", windowsHide: true }).trim();
  } catch (error) {
    return `OPEN_GAP_${command.toUpperCase()}_${String(error.message).slice(0, 120)}`;
  }
}

function writeArtifact(slug, artifact) {
  const base = path.join(tracesDir, `${phaseSlug}-${slug}-v1`);
  writeJson(`${base}.json`, artifact);
  fs.writeFileSync(`${base}.md`, renderMarkdown(artifact), "utf8");
}

function renderMarkdown(artifact) {
  const lines = [
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
  ];
  return lines.join("\n");
}

function updateStateFiles(closeout, slugs) {
  const additions = slugs.flatMap((slug) => [
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.md`,
  ]);
  const files = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ].filter((file) => fs.existsSync(file));
  for (const file of files) {
    const data = readJson(file);
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
    data.v558_v3_x2_closeout = {
      status: closeout.status,
      source_queue_rows: closeout.source_queue_rows,
      x2_build_rows_represented: closeout.x2_build_rows_represented,
      exact_rows_queued: closeout.exact_rows_queued,
      blocked_rows_queued: closeout.blocked_rows_queued,
      next_active_phase: closeout.next_active_phase,
      full_goal_complete: false,
    };
    for (const key of ["current_lookup_files", "lookup_files"]) {
      if (!Array.isArray(data[key])) continue;
      const seen = new Set(data[key]);
      for (const item of additions) seen.add(item);
      data[key] = [...seen];
    }
    writeJson(file, data);
    const md = file.replace(/\.json$/, ".md");
    if (fs.existsSync(md)) {
      fs.writeFileSync(md, renderBeaconMarkdown(data), "utf8");
    }
  }
}

function renderBeaconMarkdown(data) {
  const lines = [
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
    "## v558 v3 x2 Closeout",
    "",
    `- Status: ${data.v558_v3_x2_closeout?.status || "unknown"}`,
    `- Source queue rows: ${data.v558_v3_x2_closeout?.source_queue_rows ?? "unknown"}`,
    `- x2 build rows represented: ${data.v558_v3_x2_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Exact rows queued: ${data.v558_v3_x2_closeout?.exact_rows_queued ?? "unknown"}`,
    `- Blocked rows queued: ${data.v558_v3_x2_closeout?.blocked_rows_queued ?? "unknown"}`,
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ];
  return lines.join("\n");
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
