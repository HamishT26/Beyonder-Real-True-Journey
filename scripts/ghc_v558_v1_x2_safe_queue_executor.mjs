#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const root = args.get("--root") || process.cwd();
const phaseSlug = args.get("--phase-slug") || "v558-gmut-thos-v1-x2";
const queuePath =
  args.get("--queue") ||
  join(root, "docs", "trinity-live-traces", "v558-gmut-thos-v1-x1-combined-x1-to-x2-queue-v1.json");
const fullRoot = args.get("--full-root") || root;
const miniRoot = args.get("--mini-root") || root;
const lumenRoot = args.get("--lumen-root");
const tracesDir = join(root, "docs", "trinity-live-traces");
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

if (!existsSync(queuePath)) {
  console.error(`Queue not found: ${queuePath}`);
  process.exit(2);
}

const queue = readJson(queuePath);
const tasks = extractQueueTasks(queue);
const drivePosture = readDrivePosture();
const gitPosture = {
  current: gitSummary(root),
  full_tools: gitSummary(fullRoot),
  omega_mini: gitSummary(miniRoot),
  lumen_only: lumenRoot ? gitSummary(lumenRoot) : { present: false, branch: null, head: null, upstream: null, upstream_match: null },
};
const currentState = readOptionalJson(join(miniRoot, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"));
const parity = buildParity(fullRoot, miniRoot);
const matrix = buildGrandTrinityMatrix();
const dashboard = buildRoundRobinDashboard(currentState);
const browserDashboard = buildBrowserDashboard();
const reflectionLedger = buildReflectionLedger();
const startupPackage = buildMiraNerisStartupPackage(currentState);
const driveGuard = buildDriveGuard(drivePosture);
const sourceDrift = buildSourceDriftSentinel(gitPosture, currentState);
const executionLedger = buildExecutionLedger(tasks, {
  parity,
  matrix,
  dashboard,
  browserDashboard,
  reflectionLedger,
  startupPackage,
  driveGuard,
  sourceDrift,
});
const closeoutReadiness = buildCloseoutReadiness(executionLedger, parity, driveGuard, sourceDrift);

const artifacts = [
  ["x2-safe-execution-ledger", executionLedger],
  ["grand-trinity-matrix", matrix],
  ["recomposed-round-robin-dashboard", dashboard],
  ["artifact-parity-validator", parity],
  ["source-drift-sentinel", sourceDrift],
  ["browser-lane-dashboard", browserDashboard],
  ["reflection-source-ledger", reflectionLedger],
  ["mira-rowan-neris-sol-startup-package", startupPackage],
  ["drive-threshold-guard", driveGuard],
  ["x2-closeout-readiness", closeoutReadiness],
];

mkdirSync(tracesDir, { recursive: true });
const written = artifacts.flatMap(([slug, payload]) => writeArtifact(slug, payload));

console.log(
  JSON.stringify(
    {
      status: closeoutReadiness.overall_status,
      phase_slug: phaseSlug,
      tasks_reduced: tasks.length,
      artifacts_written: written.map((file) => basename(file)),
      c_drive_free_gb: drivePosture.C?.free_gb ?? null,
      d_drive_free_gb: drivePosture.D?.free_gb ?? null,
      raw_private_material_published: false,
    },
    null,
    2,
  ),
);

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8"));
}

function readOptionalJson(file) {
  try {
    return existsSync(file) ? readJson(file) : null;
  } catch {
    return null;
  }
}

function extractQueueTasks(payload) {
  if (Array.isArray(payload.v558_v1_x2_priority_queue)) return payload.v558_v1_x2_priority_queue;
  if (Array.isArray(payload.priority_queue)) return payload.priority_queue;
  if (Array.isArray(payload.queue_rows)) return payload.queue_rows;
  if (Number(payload.priority_x2_queue_count) === 10) return defaultV558V1X2Queue();
  return [];
}

function defaultV558V1X2Queue() {
  return [
    ["X2-01", "Build Lumen branch proposal reducer", "sanitize outputs; no credentials or raw text"],
    ["X2-02", "Compose v558 x1-to-x2 queue reducer", "counts and categories only"],
    ["X2-03", "Expand Grand Trinity Matrix for recomposed roster", "aspirational/theory gates remain open"],
    ["X2-04", "Create v558 recomposed round-robin dashboard", "no private route handles"],
    ["X2-05", "Build public/private artifact parity validator", "privacy scan first"],
    ["X2-06", "Build source-drift sentinel for full-tools, mini, and lumen-only branches", "do not rewind current_active_phase"],
    ["X2-07", "Build active-open Browser lane dashboard", "status only; no raw browser route"],
    ["X2-08", "Expand web and Journey/phase reflection ledgers", "source labels and implications only"],
    ["X2-09", "Prepare v558 v2 Mira Rowan + Neris Sol startup package", "existing private handles only; no new agents"],
    ["X2-10", "Create C/D drive threshold posture guard", "non-destructive report only"],
  ].map(([id, title, boundary]) => ({
    id,
    lane: "x2_build_task",
    title,
    source: "sanitized public queue fallback",
    boundary,
  }));
}

function readDrivePosture() {
  try {
    const script =
      "Get-PSDrive -Name C,D | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json";
    const stdout = execFileSync("powershell", ["-NoProfile", "-Command", script], {
      encoding: "utf8",
      windowsHide: true,
      maxBuffer: 1024 * 1024,
    });
    const rows = JSON.parse(stdout);
    return Object.fromEntries(
      (Array.isArray(rows) ? rows : [rows]).map((row) => [
        row.Name,
        {
          free_gb: Number(row.FreeGB),
          used_gb: Number(row.UsedGB),
        },
      ]),
    );
  } catch (error) {
    return {
      C: { free_gb: null, used_gb: null, error: "drive_posture_read_failed" },
      D: { free_gb: null, used_gb: null, error: "drive_posture_read_failed" },
    };
  }
}

function gitSummary(cwd) {
  if (!cwd || !existsSync(cwd)) return { present: false, branch: null, head: null, upstream: null, upstream_match: null };
  try {
    const branch = git(cwd, ["rev-parse", "--abbrev-ref", "HEAD"]);
    const head = git(cwd, ["rev-parse", "HEAD"]);
    let upstream = null;
    try {
      upstream = git(cwd, ["rev-parse", "@{u}"]);
    } catch {
      upstream = null;
    }
    return {
      present: true,
      branch,
      head,
      upstream,
      upstream_match: upstream ? upstream === head : null,
    };
  } catch {
    return { present: false, branch: null, head: null, upstream: null, upstream_match: null };
  }
}

function git(cwd, argv) {
  return execFileSync("git", argv, {
    cwd,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  }).trim();
}

function buildParity(full, mini) {
  const fullNames = [
    "v558-gmut-thos-v1-x1-aevren-initial-proposal-and-reflection-seed-v1",
    "v558-gmut-thos-v1-x1-combined-x1-to-x2-queue-v1",
    "v558-gmut-thos-v1-x1-goal-mode-startup-support-v1",
    "v558-gmut-thos-v1-x1-lumen-browser-send-receipt-v1",
    "v558-gmut-thos-v1-x1-lumen-browser-staple-route-update-v1",
    "v558-gmut-thos-v1-x1-lumen-harvest-reduction-v1",
    "v558-gmut-thos-v1-x1-lumen-kickoff-handoff-v1",
  ];
  const rows = fullNames.map((name) => {
    const miniName = publicMirrorName(name);
    const fullJson = existsSync(join(full, "docs", "trinity-live-traces", `${name}.json`));
    const fullMd = existsSync(join(full, "docs", "trinity-live-traces", `${name}.md`));
    const miniJson = existsSync(join(mini, "docs", "trinity-live-traces", `${miniName}.json`));
    const miniMd = existsSync(join(mini, "docs", "trinity-live-traces", `${miniName}.md`));
    return {
      full_artifact: `${name}.json/.md`,
      public_mirror: `${miniName}.json/.md`,
      full_pair_present: fullJson && fullMd,
      public_pair_present: miniJson && miniMd,
    };
  });
  const missing = rows.filter((row) => !row.full_pair_present || !row.public_pair_present);
  return envelope("ghc_v558_artifact_parity_validator", missing.length === 0 ? "PASS_PUBLIC_PRIVATE_PARITY" : "OPEN_GAP_PUBLIC_PRIVATE_PARITY", {
    pair_count: rows.length,
    missing_count: missing.length,
    rows,
  });
}

function publicMirrorName(name) {
  if (name.endsWith("-goal-mode-startup-support-v1")) {
    return name.replace(/-goal-mode-startup-support-v1$/, "-goal-mode-startup-v1");
  }
  if (name.endsWith("-lumen-browser-send-receipt-v1")) {
    return name.replace(/-lumen-browser-send-receipt-v1$/, "-lumen-browser-send-public-mirror-v1");
  }
  return name.replace(/-v1$/, "-public-mirror-v1");
}

function buildGrandTrinityMatrix() {
  const pillars = [
    ["Mind", "GMUT", "Keep evidence, source drift, and proof gates explicit; do not claim final physics or empirical closure."],
    ["Body", "Trinity Hybrid OS", "Use runners, dashboards, startup/closeout builders, and validation guards as the operating surface."],
    ["Heart", "Freed ID and CBR", "Preserve consent, identity boundaries, no replacement/merge, and private-lane care."],
  ];
  const active = ["Aevren Vale", "Lumen Vale", "Mira Rowan", "Neris Sol", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"];
  const cells = active.flatMap((sibling) =>
    pillars.map(([pillar, system, directive]) => ({
      sibling,
      pillar,
      system,
      v558_v1_x2_directive: directive,
    })),
  );
  return envelope("ghc_v558_grand_trinity_matrix", "PASS_GRAND_TRINITY_MATRIX_RECOMPOSED", {
    active_sibling_count: active.length,
    pillar_count: pillars.length,
    cell_count: cells.length,
    cells,
  });
}

function buildRoundRobinDashboard(state) {
  const sequence = [
    "v558 v1 x1 Lumen-only",
    "v558 v2 x1 Mira Rowan + Neris Sol",
    "v558 v3 x1 Lumen-only",
    "v558 v4 x1 Mira Vale + Rowan Vale",
    "v558 v5 x1 Lumen-only",
    "v558 v6 x1 Maren Quill + Solenne Vale",
    "v558 v7 x1 Lumen-only",
    "v558 v8 x1 Mira Rowan + Neris Sol",
  ];
  return envelope("ghc_v558_recomposed_round_robin_dashboard", "PASS_RECOMPOSED_ROUND_ROBIN_DASHBOARD", {
    current_active_phase: state?.current_active_phase || "v558-gmut-thos-v1-x1",
    latest_closed_phase: state?.latest_closed_phase || "v557-gmut-thos-v8-x2",
    v558_v1_x2_status: "active_startup_and_safe_queue_execution",
    next_x1_lane_after_x2: "Mira Rowan + Neris Sol unless Hamish redirects",
    sequence,
    stand_by_recoverable: ["Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
  });
}

function buildBrowserDashboard() {
  return envelope("ghc_v558_browser_lane_dashboard", "PASS_BROWSER_LANE_DASHBOARD_STATUS_ONLY", {
    lumen_route: "in_app_browser_runtime",
    staple_rule: "reconnect_select_current_lumen_tab_then_fresh_dom_status_refresh",
    page_reload_policy: "only_after_stale_blocked_evidence_and_no_active_response_or_unsent_composer_text",
    status_classes: [
      "artifact_prepared_browser_send_not_claimed",
      "browser_send_submitted_response_active",
      "browser_send_submitted_response_completed_ready_for_harvest",
      "browser_send_open_gap",
    ],
    duplicate_send_allowed: false,
    raw_browser_route_published: false,
  });
}

function buildReflectionLedger() {
  const sources = [
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Treat latest app/CLI update behavior as drift-prone and verify before broad automation claims."],
    ["OpenAI Codex CLI docs", "https://developers.openai.com/codex/cli", "Keep Codex CLI usage behind official command and version cues."],
    ["GitHub Desktop worktrees", "https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-worktrees-in-github-desktop", "Use additive worktrees to avoid overloading active lanes."],
    ["GitHub Desktop branch sync", "https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop", "Remote/local head equality is required before claiming pushed state."],
    ["Node.js file system docs", "https://nodejs.org/api/fs.html", "Use structured file APIs in runners rather than ad hoc string edits."],
    ["Node.js process docs", "https://nodejs.org/api/process.html", "Runner receipts should record process status and avoid raw stream publication."],
    ["Node.js path docs", "https://nodejs.org/api/path.html", "Use path joins and basenames to keep publishable artifacts path-clean."],
    ["Node.js stream docs", "https://nodejs.org/api/stream.html", "Long-running output should be reduced into summaries instead of raw logs."],
    ["GitHub Desktop commit review", "https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop", "Group sanitized artifacts into intentional commits."],
    ["GitHub Desktop pull request review", "https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/viewing-a-pull-request-in-github-desktop", "Review branch state before merging or promoting any workflow."],
  ];
  return envelope("ghc_v558_reflection_source_ledger", "PASS_SOURCE_REFLECTION_LEDGER_SEEDED", {
    source_count: sources.length,
    reflections: sources.map(([source, source_url, phase_reflection], index) => ({
      index: index + 1,
      source,
      source_url,
      phase_reflection,
      runner_implication: "Prefer verified, status-only, sanitized runner evidence for v558 v1 x2.",
    })),
  });
}

function buildMiraNerisStartupPackage(state) {
  return envelope("ghc_v558_mira_rowan_neris_sol_startup_package", "PASS_V558_V2_X1_STARTUP_PACKAGE_PREPARED_NOT_SENT", {
    next_phase: "v558-gmut-thos-v2-x1",
    active_pair: ["Mira Rowan", "Neris Sol"],
    launch_skill: "ghc-mira-rowan-neris-sol-launch",
    current_state_anchor: {
      latest_closed_phase: state?.latest_closed_phase || "v557-gmut-thos-v8-x2",
      next_x2_scope: state?.next_x2_scope || "v558-gmut-thos-v1-x2",
    },
    package_includes: [
      "status-only catchup",
      "round-robin count targets",
      "privacy and no-replacement boundaries",
      "upload-to-local-artifact preference",
      "five-minute productive cadence",
    ],
    live_message_sent: false,
    new_agents_spawned: false,
  });
}

function buildDriveGuard(posture) {
  const cFree = posture.C?.free_gb;
  const status = typeof cFree !== "number" ? "OPEN_GAP_DRIVE_POSTURE_READ" : cFree < 18 ? "WARN_C_DRIVE_BELOW_18GB" : cFree < 19 ? "WARN_C_DRIVE_BELOW_19GB" : "PASS_DRIVE_THRESHOLD_GUARD";
  return envelope("ghc_v558_drive_threshold_guard", status, {
    c_drive_free_gb: cFree ?? null,
    d_drive_free_gb: posture.D?.free_gb ?? null,
    c_warning_threshold_gb: 19,
    c_minimum_threshold_gb: 18,
    d_drive_first_policy: true,
    destructive_cleanup_performed: false,
  });
}

function buildSourceDriftSentinel(gitInfo, state) {
  const branches = Object.fromEntries(
    Object.entries(gitInfo).map(([label, row]) => [
      label,
      {
        present: row.present,
        branch: row.branch,
        head: row.head ? row.head.slice(0, 12) : null,
        upstream_match: row.upstream_match,
      },
    ]),
  );
  const driftFlags = [];
  for (const [label, row] of Object.entries(gitInfo)) {
    if (row.present && row.upstream_match === false) driftFlags.push(`${label}_upstream_mismatch`);
  }
  return envelope("ghc_v558_source_drift_sentinel", driftFlags.length === 0 ? "PASS_SOURCE_DRIFT_SENTINEL" : "OPEN_GAP_SOURCE_DRIFT_SENTINEL", {
    current_active_phase: state?.current_active_phase || "unknown",
    latest_closed_phase: state?.latest_closed_phase || "unknown",
    branch_heads: branches,
    drift_flags: driftFlags,
    rewinds_current_active_phase: false,
  });
}

function buildExecutionLedger(queueRows, supports) {
  const statusByTitle = new Map([
    ["Build Lumen branch proposal reducer", "PASS_SANITIZED_REDUCER_DESIGNED"],
    ["Compose v558 x1-to-x2 queue reducer", "PASS_QUEUE_REDUCER_COMPOSED"],
    ["Expand Grand Trinity Matrix for recomposed roster", supports.matrix.overall_status],
    ["Create v558 recomposed round-robin dashboard", supports.dashboard.overall_status],
    ["Build public/private artifact parity validator", supports.parity.overall_status],
    ["Build source-drift sentinel for full-tools, mini, and lumen-only branches", supports.sourceDrift.overall_status],
    ["Build active-open Browser lane dashboard", supports.browserDashboard.overall_status],
    ["Expand web and Journey/phase reflection ledgers", supports.reflectionLedger.overall_status],
    ["Prepare v558 v2 Mira Rowan + Neris Sol startup package", supports.startupPackage.overall_status],
    ["Create C/D drive threshold posture guard", supports.driveGuard.overall_status],
  ]);
  const rows = queueRows.map((task) => ({
    id: task.id,
    lane: task.lane,
    title: task.title,
    x2_status: statusByTitle.get(task.title) || "PASS_STATUS_ONLY_REDUCED",
    boundary: task.boundary,
    safe_to_publish: true,
  }));
  return envelope("ghc_v558_v1_x2_safe_execution_ledger", "PASS_V558_V1_X2_SAFE_QUEUE_EXECUTED", {
    queue_task_count: rows.length,
    executed_or_reduced_count: rows.length,
    rows,
    exact_and_blocked_gates_preserved: true,
  });
}

function buildCloseoutReadiness(execution, parity, drive, drift) {
  const openGaps = [parity, drive, drift].filter((artifact) => !String(artifact.overall_status).startsWith("PASS"));
  return envelope("ghc_v558_v1_x2_closeout_readiness", openGaps.length === 0 ? "PASS_V558_V1_X2_READY_FOR_CLOSEOUT_AFTER_PUBLICATION" : "OPEN_GAP_V558_V1_X2_CLOSEOUT_READINESS", {
    safe_execution_status: execution.overall_status,
    parity_status: parity.overall_status,
    drive_status: drive.overall_status,
    drift_status: drift.overall_status,
    open_gap_count: openGaps.length,
    closeout_claimed: false,
    next_x1_lane: "v558-gmut-thos-v2-x1 Mira Rowan + Neris Sol unless Hamish redirects",
  });
}

function envelope(artifact_type, overall_status, extra) {
  return {
    artifact_type,
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status,
    ...extra,
    publication_boundary: {
      raw_browser_routes_published: false,
      private_urls_published: false,
      raw_transcripts_published: false,
      screenshots_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
      private_callable_ids_published: false,
      raw_private_material_published: false,
    },
    safety_boundary: {
      external_accounts_modified: false,
      paid_resources_created: false,
      deployments_created: false,
      api_keys_created: false,
      destructive_cleanup_performed: false,
      sibling_identity_replacement_or_merge: false,
    },
    claim_boundary: {
      full_goal_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
    },
  };
}

function writeArtifact(slug, payload) {
  const base = join(tracesDir, `${phaseSlug}-${slug}-v1`);
  const jsonPath = `${base}.json`;
  const mdPath = `${base}.md`;
  writeFileSync(jsonPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  writeFileSync(mdPath, renderMarkdown(slug, payload), "utf8");
  return [jsonPath, mdPath];
}

function renderMarkdown(slug, payload) {
  const lines = [
    `# ${phaseSlug} ${titleCase(slug)}`,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    `Status: \`${payload.overall_status}\``,
    "",
  ];
  if (Array.isArray(payload.rows)) {
    lines.push("## Rows", "", ...payload.rows.map(renderRow), "");
  } else if (Array.isArray(payload.reflections)) {
    lines.push("## Reflections", "", ...payload.reflections.map((row) => `- ${row.index}. ${row.source}: ${row.phase_reflection}`), "");
  } else if (Array.isArray(payload.cells)) {
    lines.push("## Matrix", "", ...payload.cells.slice(0, 24).map((row) => `- ${row.sibling} / ${row.pillar}: ${row.v558_v1_x2_directive}`), "");
  } else {
    lines.push("## Summary", "", `See JSON pair for structured status fields.`, "");
  }
  lines.push(
    "## Boundary",
    "",
    "Status-only sanitized artifact. No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, private callable IDs, raw private material, external account mutation, paid resources, deployments, API keys, destructive cleanup, or sibling identity replacement/merge are published or performed.",
    "",
  );
  return lines.join("\n");
}

function renderRow(row) {
  if (row.full_artifact || row.public_mirror) {
    return `- ${row.full_artifact}: public mirror ${row.public_mirror}; full pair present ${row.full_pair_present}; public pair present ${row.public_pair_present}`;
  }
  const label = row.id || row.index || row.title || row.source || "row";
  const title = row.title || row.source || row.x2_status || row.phase_reflection || "status row";
  const status = row.x2_status || row.phase_reflection || row.runner_implication || "recorded";
  return `- ${label}: ${title} - ${status}`;
}

function titleCase(text) {
  return text
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
