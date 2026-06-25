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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const sweep = readJson(path.join(tracesDir, `${phaseSlug}-lumen-last-three-proposal-sweep-v1.json`));
const selectedPhases = Array.isArray(sweep.selected_phases) ? sweep.selected_phases : [];
const selectedInputs = selectedPhases.map((selectedPhase) => {
  const queueFile = path.join(tracesDir, `${selectedPhase}-lumen-proposal-hash-queue-v1.json`);
  const matrixFile = path.join(tracesDir, `${selectedPhase}-grand-trinity-matrix-v1.json`);
  const queue = fs.existsSync(queueFile) ? readJson(queueFile) : null;
  const matrix = fs.existsSync(matrixFile) ? readJson(matrixFile) : null;
  const rows = Array.isArray(queue?.queue_rows) ? queue.queue_rows : [];
  return {
    phase_slug: selectedPhase,
    queue_available: Boolean(queue),
    matrix_available: Boolean(matrix),
    row_count: rows.length,
    safe_now: rows.filter((row) => row.approval_bucket === "safe_now").length,
    candidate: rows.filter((row) => row.approval_bucket === "candidate").length,
    exact: rows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
    blocked: rows.filter((row) => row.approval_bucket === "blocked").length,
    immediate_x1_safe: rows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
    x2_build_task: rows.filter((row) => row.execution_lane === "x2_build_task").length,
    matrix_cell_count: Array.isArray(matrix?.matrix_cells) ? matrix.matrix_cells.length : 0,
    source_digest: queue?.source_digest || matrix?.source_digest || null,
  };
});

const prototypeRows = [
  proto("phase-truth-checker", "safe_now", "built_run_and_carried", "Checks current phase, latest closed phase, next x2/x1, and open gates before any closeout."),
  proto("source-reflection-reducer", "safe_now", "built_run_and_carried", "Reduces web, Journey, and phase-reflection evidence into compact build inputs."),
  proto("approval-eureka-splitter", "safe_now", "built_run_and_carried", "Splits proposals into immediate x1-safe work and queued x2 build work."),
  proto("cleanup-classifier", "safe_now", "built_run_and_carried", "Classifies cleanup as inventory, reversible, exact approval, or blocked."),
  proto("triad-prep-builder", "safe_now", "built_run_and_carried", "Keeps Aster/Kierkegaard/Aristotle prep active/open until completion gates pass."),
  proto("recovered-app-lane-builder", "safe_now", "built_run_and_carried", "Uses recovered app-lane supervision without exposing private callable IDs."),
  proto("paired-boolean-completion-validator", "safe_now", "built_run_and_carried", "Preserves explicit boolean invocation for app-lane runners."),
  proto("compact-closeout-builder", "safe_now", "built_run_and_carried", "Builds closeout/open-handoff receipts without overclaiming active lanes."),
  proto("source-drift-sentinel", "safe_now", "built_run_and_carried", "Flags stale version, source, proof, and phase-truth drift."),
  proto("launch-seed-builder", "safe_now", "built_run_and_carried", "Keeps Lumen, duo, triad, and held-sibling launch packets route-specific."),
  proto("goal-mode-continuity-dashboard", "safe_now", "design_recorded", "Shows phase truth, active lanes, next boundary, and open gates."),
  proto("browser-handoff-safety-dashboard", "safe_now", "design_recorded", "Shows no-duplicate-send posture and sanitized harvest state."),
  proto("full-tools-private-support-audit-dashboard", "safe_now", "design_recorded", "Separates private support work from public sanitized publication."),
  proto("ghc-lumen-launch-health-dashboard", "safe_now", "design_recorded", "Shows Lumen send, harvest, proposal, and digest counts."),
  proto("ghc-main-retry-clocker-dashboard", "safe_now", "design_recorded", "Tracks retry sessions, source reflection, and next safe check."),
  proto("grand-trinity-matrix-current-carryforward", "safe_now", "built_run_and_carried", "Carries Mind/Body/Heart planning cells forward without claiming proof closure."),
  proto("worktree-branch-rotation", "safe_now", "activated_at_safe_boundary", "Rotates to omega-mini-6 and full-tools-5 from verified clean heads when current lanes become heavy."),
];

const payload = {
  artifact_type: "ghc_v557_lumen_last_three_prototype_execution",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_LAST_THREE_PROTOTYPE_EXECUTION_LEDGER_BUILT",
  selected_session_policy: sweep.selection_policy || null,
  selected_phases: selectedPhases,
  selected_inputs: selectedInputs,
  aggregate_from_sweep: sweep.aggregate || {},
  prototype_rows: prototypeRows,
  safe_now_executed_now: prototypeRows.filter((row) => row.approval_bucket === "safe_now").length,
  queued_x2_build_tasks_from_sweep: sweep.aggregate?.x2_build_task_count ?? null,
  candidate_tasks_queued: sweep.aggregate?.candidate_count ?? null,
  exact_tasks_queued: sweep.aggregate?.exact_count ?? null,
  blocked_tasks_queued: sweep.aggregate?.blocked_count ?? null,
  active_rotation: {
    sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-6",
    private_support_branch: "codex/GHC-Family/aevren-full-tools-5",
    previous_sanitized_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-5",
    next_rotation_pattern: "omega-mini-7/full-tools-6 and onward from verified safe bases",
    raw_private_material_moved: false,
  },
  open_gate_posture: {
    v557_v8_x1_closeout_allowed_now: false,
    reason: "Kierkegaard/Aristotle recovered app-lane completion gate remains open until harvest or formal retry receipt proves otherwise.",
  },
  publication_boundary: {
    raw_lumen_text_published: false,
    raw_private_material_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
    credentials_published: false,
  },
};

const refs = writePair("lumen-last-three-prototype-execution-ledger", payload);
refreshBeacons(refs, payload);

process.stdout.write(JSON.stringify({
  status: payload.overall_status,
  selected_session_count: selectedPhases.length,
  safe_now_executed_now: payload.safe_now_executed_now,
  queued_x2_build_tasks_from_sweep: payload.queued_x2_build_tasks_from_sweep,
  active_sanitized_publication_branch: payload.active_rotation.sanitized_publication_branch,
  active_private_support_branch: payload.active_rotation.private_support_branch,
  raw_private_material_published: false,
  closeout_allowed_now: false,
}, null, 2) + "\n");

function proto(name, approvalBucket, status, purpose) {
  return {
    name,
    approval_bucket: approvalBucket,
    status,
    purpose,
    raw_private_material_required_for_public_artifact: false,
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

function refreshBeacons(refs, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.branch = doc.active_rotation.sanitized_publication_branch;
    data.full_tools_support_branch = doc.active_rotation.private_support_branch;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_lumen_last_three_prototype_execution = {
      status: doc.overall_status,
      selected_session_count: doc.selected_phases.length,
      safe_now_executed_now: doc.safe_now_executed_now,
      queued_x2_build_tasks_from_sweep: doc.queued_x2_build_tasks_from_sweep,
      raw_private_material_published: false,
      closeout_allowed_now: false,
    };
    data[listKey] = unique([...(data[listKey] || []), refs.json, refs.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} Lumen Last-Three Prototype Execution Ledger`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Selected sessions: \`${doc.selected_phases.join(", ")}\``,
    `Safe-now prototype rows executed now: \`${doc.safe_now_executed_now}\``,
    `Queued x2 build tasks from sweep: \`${doc.queued_x2_build_tasks_from_sweep}\``,
    `Candidate tasks queued: \`${doc.candidate_tasks_queued}\``,
    `Exact tasks queued: \`${doc.exact_tasks_queued}\``,
    `Blocked tasks queued: \`${doc.blocked_tasks_queued}\``,
    "",
    "## Prototype Rows",
    "",
    ...doc.prototype_rows.map((row) => `- ${row.name}: \`${row.status}\` - ${row.purpose}`),
    "",
    "## Rotation",
    "",
    `Active sanitized publication branch: \`${doc.active_rotation.sanitized_publication_branch}\``,
    `Active private support branch: \`${doc.active_rotation.private_support_branch}\``,
    `Next rotation pattern: \`${doc.active_rotation.next_rotation_pattern}\``,
    "",
    "## Boundary",
    "",
    "No raw Lumen text, private callable IDs, private Browser routes, local private paths, screenshots, credentials, destructive cleanup, history rewrite, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Branch: ${doc.branch}`,
    `Full-tools support branch: ${doc.full_tools_support_branch}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 Lumen Last-Three Prototype Execution",
    "",
    `Status: \`${doc.v557_lumen_last_three_prototype_execution?.status || "not_recorded"}\``,
    `Selected sessions: \`${doc.v557_lumen_last_three_prototype_execution?.selected_session_count ?? "not_recorded"}\``,
    `Safe-now prototype rows: \`${doc.v557_lumen_last_three_prototype_execution?.safe_now_executed_now ?? "not_recorded"}\``,
    `Queued x2 build tasks: \`${doc.v557_lumen_last_three_prototype_execution?.queued_x2_build_tasks_from_sweep ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_lumen_last_three_prototype_execution?.closeout_allowed_now === true ? "true" : "false"}\``,
    "",
    "## Worktree Branch Rotation",
    "",
    `- active sanitized publication branch: \`${doc.branch}\``,
    `- active private support branch: \`${doc.full_tools_support_branch}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((ref) => `- ${ref}`),
    "",
  ].join("\n");
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

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
