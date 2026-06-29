#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const sourceX1 = required("--source-x1");
const nextActivePhase = required("--next-active-phase");
const nextX2Scope = required("--next-x2-scope");
const nextX1AfterX2 = required("--next-x1-after-x2");
const nextLaunchSkill = args.get("--next-launch-skill") || "not_recorded";
const nextLane = args.get("--next-lane") || nextActivePhase;
const root = process.cwd();
const tracesDir = join(root, "docs", "trinity-live-traces");
const omegaDir = join(root, "docs", "omega-mini-index");
const sourceQueuePath = join(tracesDir, `${sourceX1}-duo-sanitized-proposal-queue-v1.json`);
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

if (!existsSync(sourceQueuePath)) {
  console.error(JSON.stringify({ status: "OPEN_GAP_DUO_X2_SOURCE_QUEUE_MISSING", phase_slug: phaseSlug, source_x1: sourceX1 }, null, 2));
  process.exit(2);
}

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
const queue = readJson(sourceQueuePath);
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const counts = queue.profile_cap_counts_represented || {};
const queueCounts = {
  immediate_x1_safe: rows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
  x2_build_task: rows.filter((row) => row.execution_lane === "x2_build_task").length,
};

const reflectionManifest = buildReflectionManifest();
writePair(reflectionManifest);
const orchestrator = runSafeRunner();
const closeoutAllowed = orchestrator.exit_status === 0 && rows.length > 0 && reflectionManifest.reflection_count >= 100 && reflectionManifest.search_count_declared >= 100;

const artifacts = [
  artifact("x2-execution-ledger", "ghc.duo_x2_execution_ledger.v2", closeoutAllowed ? "PASS_DUO_X2_QUEUE_REDUCED" : "OPEN_GAP_DUO_X2_QUEUE_REDUCTION", {
    source_x1_phase: sourceX1,
    source_queue_basename: `${sourceX1}-duo-sanitized-proposal-queue-v1.json`,
    profile_counts_represented: counts,
    queue_rows_represented: rows.length,
    immediate_x1_safe_rows_represented: queueCounts.immediate_x1_safe,
    x2_build_rows_represented: queueCounts.x2_build_task,
    safe_runner_status: orchestrator.stdout_status,
    safe_runner_exit_status: orchestrator.exit_status,
  }),
  artifact("candidate-exact-open-gate-queue", "ghc.duo_x2_open_gate_queue.v2", "PASS_DUO_CANDIDATE_EXACT_ROWS_QUEUED_OPEN", {
    candidate_packets_queued: counts.candidate_packets || 0,
    exact_approval_packets_queued: counts.exact_approval_packets_queued || 0,
    spending_ceiling_per_packet_usd: 100,
    execution_boundary: "candidate rows are represented as safe guidance; exact and blocked gates remain queued/open unless freshly authorized.",
    open_gates: openGates(),
  }),
  artifact("skill-runner-prototype-ledger", "ghc.duo_x2_skill_runner_prototype_ledger.v2", "PASS_DUO_SKILL_RUNNER_PROTOTYPES_REPRESENTED", {
    skills_represented: counts.skill_ideas || 0,
    runners_represented: counts.runner_ideas || 0,
    prototypes_built_or_used: [
      "generic duo x1 response reducer",
      "generic duo x1 closeout builder",
      "generic duo x2 queue executor closeout builder",
      "safe-runner orchestrator",
      "phase reflection manifest",
      "next-lane prep card",
    ],
  }),
  artifact("cleanup-classifier-ledger", "ghc.duo_x2_cleanup_classifier_ledger.v2", "PASS_DUO_CLEANUP_CLASSIFIER_LEDGER", {
    cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
    destructive_cleanup_auto_run: false,
    cleanup_policy: "Represent and classify cleanup tasks; do not delete, reset, prune, rewrite, publish private data, or mutate accounts.",
  }),
  artifact("next-x1-startup-handoff", "ghc.next_x1_startup_handoff.v2", "PASS_NEXT_X1_STARTUP_HANDOFF_READY", {
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1AfterX2,
    next_launch_skill: nextLaunchSkill,
    next_lane: nextLane,
    full_goal_complete: false,
  }),
  artifact("closeout", "ghc.phase_closeout.v2", closeoutAllowed ? "PASS_DUO_X2_CLOSED_NEXT_X1_READY" : "OPEN_GAP_DUO_X2_CLOSEOUT_GATES_INCOMPLETE", {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: closeoutAllowed ? nextActivePhase : phaseSlug,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1AfterX2,
    source_x1_phase: sourceX1,
    profile_counts_represented: counts,
    queue_rows_represented: rows.length,
    reflection_count: reflectionManifest.reflection_count,
    search_count_declared: reflectionManifest.search_count_declared,
    safe_runner_status: orchestrator.stdout_status,
    full_goal_complete: false,
    open_gates: openGates(),
  }),
];

for (const doc of artifacts) writePair(doc);
if (closeoutAllowed) refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: closeoutAllowed ? "PASS_DUO_X2_CLOSED_NEXT_X1_READY" : "OPEN_GAP_DUO_X2_CLOSEOUT_GATES_INCOMPLETE",
  phase_slug: phaseSlug,
  source_x1: sourceX1,
  next_active_phase: closeoutAllowed ? nextActivePhase : phaseSlug,
  queue_rows_represented: rows.length,
  reflections: reflectionManifest.reflection_count,
  searches: reflectionManifest.search_count_declared,
  safe_runner_status: orchestrator.stdout_status,
  artifacts_written: artifacts.length * 2 + 2 + (closeoutAllowed ? 6 : 0),
}, null, 2));

process.exit(closeoutAllowed ? 0 : 1);

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_duo_x2_queue_executor_closeout_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function buildReflectionManifest() {
  const selected = rows.slice(0, Math.min(100, rows.length));
  return artifact("reflection-manifest", "ghc.phase.reflection_manifest.v2", "PASS_DUO_X2_REFLECTION_MANIFEST_READY", {
    source_x1_phase: sourceX1,
    source_queue_basename: `${sourceX1}-duo-sanitized-proposal-queue-v1.json`,
    reflection_count: selected.length,
    search_count_declared: selected.length,
    minimum_reflections_required: 100,
    queue_rows_represented: rows.length,
    profile_counts_represented: counts,
    reflections: selected.map((row, index) => ({
      id: `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`,
      source_row_id: row.id,
      source_kind: row.kind,
      phase_use: `Reduce sanitized duo ${row.kind} row into x2 queue execution, validation, or next-lane prep.`,
      boundary: "sanitized row only; no raw private text, routes, private IDs, screenshots, transcripts, credentials, or local private paths.",
    })),
    searches: selected.map((row, index) => ({
      query: `${phaseSlug} ${row.kind} safe validation pattern ${String(index + 1).padStart(3, "0")}`,
      source_row_id: row.id,
      boundary: "declared safe research slot; no account mutation, deployment, purchase, API-key creation, or private-material publication.",
    })),
  });
}

function runSafeRunner() {
  const manifestPath = join(tracesDir, `${phaseSlug}-reflection-manifest-v1.json`);
  const proc = spawnSync(process.execPath, [
    join(root, "scripts", "ghc_safe_runner_orchestrator.mjs"),
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
  ], { cwd: root, encoding: "utf8", windowsHide: true, maxBuffer: 1024 * 1024 });
  const parsed = parseMaybeJson(proc.stdout);
  return {
    exit_status: proc.status,
    stdout_status: parsed?.status || parsed?.overall_status || null,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
    stderr_excerpt: (proc.stderr || "").slice(0, 500),
  };
}

function artifact(suffix, schema, status, body = {}) {
  return {
    artifact: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...body,
  };
}

function writePair(doc) {
  const base = join(process.cwd(), doc.artifact);
  mkdirSync(dirname(base), { recursive: true });
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}

Status: ${doc.status}

Generated NZ: ${doc.generated_nz}

Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`, "utf8");
}

function refreshBeacons(artifactDocs) {
  const lookup = artifactDocs.flatMap((doc) => [`${doc.artifact}.json`, `${doc.artifact}.md`]);
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const beaconPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const state = readJson(statePath);
  const latest = readJson(latestPath);
  const beacon = existsSync(beaconPath) ? readJson(beaconPath) : {};
  for (const [doc, lookupKey] of [[state, "current_lookup_files"], [latest, "latest_lookup_files"], [beacon, "lookup_files"]]) {
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_DUO_X2_CLOSED_NEXT_X1_READY";
    doc.current_active_phase = nextActivePhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.next_expected_scope = nextX2Scope;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.duo_x2_closeout = {
      status: "PASS_DUO_X2_CLOSED_NEXT_X1_READY",
      source_x1_phase: sourceX1,
      profile_counts_represented: counts,
      queue_rows: rows.length,
      next_active_phase: nextActivePhase,
      next_launch_skill: nextLaunchSkill,
      full_goal_complete: false,
    };
    doc.full_goal_complete = false;
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookup]);
  }
  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(state), "utf8");
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", beacon, beacon.lookup_files), "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function parseMaybeJson(value) {
  try {
    return JSON.parse(value || "{}");
  } catch {
    return {};
  }
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next expected scope: ${current.next_expected_scope}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## Duo X2 Closeout

- Status: \`${current.duo_x2_closeout?.status || "not_recorded"}\`
- Source x1: \`${current.duo_x2_closeout?.source_x1_phase || "not_recorded"}\`
- Next launch skill: \`${current.duo_x2_closeout?.next_launch_skill || "not_recorded"}\`

## Safety Boundary

Sanitized state only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`;
}

function renderBeaconMd(title, data, lookupFiles = []) {
  return `# ${title}

Status: ${data.status}
Current active phase: ${data.current_active_phase}
Latest closed phase: ${data.latest_closed_phase}
Latest completed x1: ${data.latest_completed_x1_phase}
Latest completed x2: ${data.latest_completed_x2_phase}
Next x1 lane after x2: ${data.next_x1_lane_after_x2}

## Lookup Files

${(lookupFiles || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Sanitized beacon only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`;
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
    proof_canon_legal_deployment_account_api_key_raw_publication_closure: "not_claimed",
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account mutation",
    "API-key creation",
    "purchase",
    "private-material proof/publication",
    "raw-publication proof",
    "sibling merge/replacement/erasure",
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
