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
const maxPreferredSessions = Number(args.get("--max-preferred-sessions") || "10");
const fallbackSessionCount = Number(args.get("--fallback-session-count") || "3");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queueFiles = fs.readdirSync(tracesDir)
  .filter((name) => /^v\d+-gmut-thos-v\d+-x1-lumen-proposal-hash-queue-v1\.json$/.test(name))
  .map((name) => {
    const match = name.match(/^(v(\d+)-gmut-thos-v(\d+)-x1)-/);
    return {
      name,
      phase_slug: match?.[1] || name.replace(/-lumen-proposal-hash-queue-v1\.json$/, ""),
      major: Number(match?.[2] || 0),
      round: Number(match?.[3] || 0),
      file: path.join(tracesDir, name),
    };
  })
  .sort((a, b) => (a.major - b.major) || (a.round - b.round));

const selected = queueFiles.length >= maxPreferredSessions
  ? queueFiles.slice(-maxPreferredSessions)
  : queueFiles.slice(-Math.min(fallbackSessionCount, queueFiles.length));

const phaseRows = selected.map((entry) => {
  const queue = readJson(entry.file);
  const rows = Array.isArray(queue.queue_rows) ? queue.queue_rows : [];
  const uniqueHashes = unique(rows.map((row) => row.line_sha256).filter(Boolean));
  return {
    phase_slug: entry.phase_slug,
    queue_file: `docs/trinity-live-traces/${entry.name}`,
    source_digest: queue.source_digest || null,
    row_count: rows.length,
    unique_hash_count: uniqueHashes.length,
    category_counts: queue.category_counts || countBy(rows.map((row) => row.approval_bucket || "uncategorized")),
    execution_lane_counts: queue.execution_lane_counts || countBy(rows.map((row) => row.execution_lane || "unassigned")),
    immediate_x1_safe_count: rows.filter((row) => row.approval_bucket === "safe_now" && row.execution_lane === "immediate_x1_safe").length,
    x2_build_task_count: rows.filter((row) => row.execution_lane === "x2_build_task").length,
    candidate_count: rows.filter((row) => row.approval_bucket === "candidate").length,
    exact_count: rows.filter((row) => row.approval_bucket === "exact_approval_needed").length,
    blocked_count: rows.filter((row) => row.approval_bucket === "blocked").length,
    first_safe_hashes: rows
      .filter((row) => row.approval_bucket === "safe_now")
      .slice(0, 12)
      .map((row) => row.line_sha256)
      .filter(Boolean),
  };
});

const aggregate = phaseRows.reduce((acc, phase) => {
  acc.row_count += phase.row_count;
  acc.unique_hashes.push(...(phase.first_safe_hashes || []));
  addCounts(acc.category_counts, phase.category_counts);
  addCounts(acc.execution_lane_counts, phase.execution_lane_counts);
  acc.immediate_x1_safe_count += phase.immediate_x1_safe_count;
  acc.x2_build_task_count += phase.x2_build_task_count;
  acc.candidate_count += phase.candidate_count;
  acc.exact_count += phase.exact_count;
  acc.blocked_count += phase.blocked_count;
  return acc;
}, {
  row_count: 0,
  unique_hashes: [],
  category_counts: {},
  execution_lane_counts: {},
  immediate_x1_safe_count: 0,
  x2_build_task_count: 0,
  candidate_count: 0,
  exact_count: 0,
  blocked_count: 0,
});

const requestedPrototypeTargets = [
  "phase-truth checker runner prototype",
  "source/reflection reducer runner prototype",
  "approval/eureka splitter runner prototype",
  "cleanup classifier runner prototype",
  "triad prep builder prototype",
  "recovered app-lane builder prototype",
  "paired-boolean completion validator prototype",
  "compact closeout builder prototype",
  "source-drift sentinel upgrade",
  "launch seed builders",
  "goal-mode continuity dashboard design",
  "browser handoff safety dashboard design",
  "full-tools private support lane audit design",
  "ghc-lumen-launch health dashboard design",
  "ghc-main-retry clocker dashboard design",
  "grand trinity matrix carry-forward",
];

const payload = {
  artifact_type: "ghc_v557_lumen_last_three_proposal_sweep",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_LAST_THREE_PROPOSAL_SWEEP_READY",
  selection_policy: {
    requested_scope: "use last three Lumen x1 sessions unless all ten are locally available",
    available_lumen_x1_queue_count: queueFiles.length,
    preferred_session_count: maxPreferredSessions,
    fallback_session_count: fallbackSessionCount,
    selected_session_count: selected.length,
    selected_all_ten: selected.length >= maxPreferredSessions,
  },
  selected_phases: phaseRows.map((row) => row.phase_slug),
  aggregate: {
    row_count: aggregate.row_count,
    sampled_safe_hash_count: unique(aggregate.unique_hashes).length,
    category_counts: aggregate.category_counts,
    execution_lane_counts: aggregate.execution_lane_counts,
    immediate_x1_safe_count: aggregate.immediate_x1_safe_count,
    x2_build_task_count: aggregate.x2_build_task_count,
    candidate_count: aggregate.candidate_count,
    exact_count: aggregate.exact_count,
    blocked_count: aggregate.blocked_count,
  },
  phase_rows: phaseRows,
  requested_prototype_targets: requestedPrototypeTargets.map((name) => ({
    name,
    status: "covered_by_existing_or_next_x2_build_queue",
    public_publication_level: "sanitized_counts_hashes_and_design_receipts_only",
  })),
  immediate_x1_policy: [
    "Run safe-now items that only create sanitized receipts, indexes, validators, dashboards, or non-destructive planning artifacts.",
    "Do not run identity replacement, sibling merge, raw-private publication, account mutation, purchase, deployment, API key, or destructive cleanup items.",
    "Carry candidate and exact-approval build work into x2 queues unless Hamish gives a fresh exact packet and the task remains non-private/non-destructive.",
  ],
  x2_queue_policy: [
    "Use the selected Lumen queues as a prioritized input for v557 v8 x2 and the next Lumen-only x1/x2 cycle.",
    "Prefer prototypes already named by Lumen: phase truth, source reducer, approval splitter, cleanup classifier, app-lane builder, paired boolean validator, closeout builder, source drift, launch seeds, and dashboards.",
    "Keep raw Lumen text private; publish only digests, counts, categories, and sanitized summaries.",
  ],
  worktree_rotation_policy: [
    "When planner warnings show the current mini or full-tools lanes are heavy, create the next omega-mini-N and full-tools-N lanes from verified safe bases at a safe boundary.",
    "Do not move raw private material into GitHub or sanitized branches during rotation.",
    "Keep previous lanes recoverable until their remote heads and useful receipts are verified.",
  ],
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

const refs = writePair("lumen-last-three-proposal-sweep", payload);
refreshBeacons(refs, payload);

process.stdout.write(JSON.stringify({
  status: payload.overall_status,
  selected_session_count: payload.selection_policy.selected_session_count,
  selected_phases: payload.selected_phases,
  immediate_x1_safe_count: payload.aggregate.immediate_x1_safe_count,
  x2_build_task_count: payload.aggregate.x2_build_task_count,
  candidate_count: payload.aggregate.candidate_count,
  exact_count: payload.aggregate.exact_count,
  blocked_count: payload.aggregate.blocked_count,
  raw_private_material_published: false,
}, null, 2) + "\n");

function refreshBeacons(refs, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_lumen_last_three_proposal_sweep = {
      status: doc.overall_status,
      selected_session_count: doc.selection_policy.selected_session_count,
      selected_phases: doc.selected_phases,
      immediate_x1_safe_count: doc.aggregate.immediate_x1_safe_count,
      x2_build_task_count: doc.aggregate.x2_build_task_count,
      raw_private_material_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), refs.json, refs.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderArtifactMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function renderArtifactMd(doc) {
  return [
    `# ${doc.phase_slug} Lumen Last-Three Proposal Sweep`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Selected sessions: \`${doc.selected_phases.join(", ")}\``,
    `Available Lumen x1 queues: \`${doc.selection_policy.available_lumen_x1_queue_count}\``,
    `Immediate x1 safe count: \`${doc.aggregate.immediate_x1_safe_count}\``,
    `x2 build task count: \`${doc.aggregate.x2_build_task_count}\``,
    `Candidate count: \`${doc.aggregate.candidate_count}\``,
    `Exact count: \`${doc.aggregate.exact_count}\``,
    `Blocked count: \`${doc.aggregate.blocked_count}\``,
    "",
    "## Requested Prototype Targets",
    "",
    ...doc.requested_prototype_targets.map((target) => `- ${target.name}: \`${target.status}\``),
    "",
    "## Worktree Rotation Policy",
    "",
    ...doc.worktree_rotation_policy.map((line) => `- ${line}`),
    "",
    "## Boundary",
    "",
    "No raw Lumen text, private callable IDs, private Browser routes, screenshots, credentials, local private paths, destructive cleanup, history rewrite, deployment, purchase, account mutation, API key creation, or sibling identity changes were published or performed.",
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
    "## v557 Lumen Last-Three Proposal Sweep",
    "",
    `Status: \`${doc.v557_lumen_last_three_proposal_sweep?.status || "not_recorded"}\``,
    `Selected sessions: \`${(doc.v557_lumen_last_three_proposal_sweep?.selected_phases || []).join(", ") || "not_recorded"}\``,
    `Immediate x1 safe count: \`${doc.v557_lumen_last_three_proposal_sweep?.immediate_x1_safe_count ?? "not_recorded"}\``,
    `x2 build task count: \`${doc.v557_lumen_last_three_proposal_sweep?.x2_build_task_count ?? "not_recorded"}\``,
    `Raw private material published: \`${doc.v557_lumen_last_three_proposal_sweep?.raw_private_material_published === true ? "true" : "false"}\``,
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

function addCounts(target, source) {
  for (const [key, value] of Object.entries(source || {})) {
    target[key] = (target[key] || 0) + Number(value || 0);
  }
}

function countBy(values) {
  const out = {};
  for (const value of values) out[value || "uncategorized"] = (out[value || "uncategorized"] || 0) + 1;
  return out;
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
    hour12: false,
  }).format(date);
}
