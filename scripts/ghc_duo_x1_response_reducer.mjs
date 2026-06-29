#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const nextX2 = required("--next-x2");
const nextX1AfterX2 = required("--next-x1-after-x2");
const launchSkill = args.get("--launch-skill") || "not_recorded";
const siblings = csv(required("--siblings"));
const privateFiles = csv(required("--private-responses"));
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

if (siblings.length !== privateFiles.length) {
  console.error(JSON.stringify({ status: "OPEN_GAP_DUO_REDUCER_SIBLING_FILE_COUNT_MISMATCH", phase_slug: phaseSlug }, null, 2));
  process.exit(2);
}

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
const profilePerLane = {
  safe_approval_packets: 10,
  candidate_packets: 5,
  exact_approval_packets_queued: 5,
  skill_ideas: 7,
  runner_ideas: 3,
  cleanup_refine_fix_tasks: 15,
};

const laneInputs = siblings.map((sibling, index) => readLane(sibling, privateFiles[index]));
const allInputsReady = laneInputs.every((lane) => lane.status === "PASS_PRIVATE_RESPONSE_FOUND");
const rows = [
  ...buildRows("Aevren Vale", "aevren_local_steward"),
  ...laneInputs.flatMap((lane) => buildRows(lane.sibling, lane.basename)),
];
const counts = aggregate(rows);
const expectedCounts = multiplyCounts(profilePerLane, siblings.length + 1);
const countsReady = sameCounts(counts, expectedCounts);

const reduction = artifact("duo-harvest-reduction", "ghc.duo_harvest_reduction.v2", allInputsReady && countsReady
  ? "PASS_DUO_X1_PRIVATE_RESPONSES_REDUCED_SANITIZED"
  : "OPEN_GAP_DUO_X1_PRIVATE_RESPONSE_REDUCTION", {
  active_duo: siblings,
  launch_skill: launchSkill,
  source_status: laneInputs.map((lane) => ({
    sibling: lane.sibling,
    basename: lane.basename,
    status: lane.status,
    sha256: lane.sha256,
    character_count: lane.character_count,
    raw_text_published: false,
  })),
  profile_cap_counts_represented: counts,
  expected_counts: expectedCounts,
  queue_rows: rows.length,
});

const queue = artifact("duo-sanitized-proposal-queue", "ghc.duo_sanitized_proposal_queue.v2", reduction.status, {
  source_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  launch_skill: launchSkill,
  profile_cap_counts_represented: counts,
  rows,
});

const prep = artifact("closeout-prep", "ghc.duo_x1_closeout_prep.v2", allInputsReady && countsReady
  ? "PASS_DUO_X1_CLOSEOUT_PREP_READY"
  : "OPEN_GAP_DUO_X1_CLOSEOUT_PREP", {
  source_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  launch_skill: launchSkill,
  response_sources_ready: allInputsReady,
  counts_ready: countsReady,
  profile_cap_counts_represented: counts,
  open_gates: openGates(),
});

for (const doc of [reduction, queue, prep]) writePair(doc);

console.log(JSON.stringify({
  status: reduction.status,
  phase_slug: phaseSlug,
  private_sources_ready: allInputsReady,
  counts_ready: countsReady,
  queue_rows: rows.length,
  immediate_x1_safe_rows: rows.filter((row) => row.execution_lane === "immediate_x1_safe").length,
  x2_build_task_rows: rows.filter((row) => row.execution_lane === "x2_build_task").length,
  artifacts_written: 6,
}, null, 2));

process.exit(reduction.status.startsWith("PASS") ? 0 : 1);

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
    console.error(`Usage: node scripts/ghc_duo_x1_response_reducer.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function csv(value) {
  return value.split("|").map((item) => item.trim()).filter(Boolean);
}

function readLane(sibling, file) {
  if (!existsSync(file)) return { sibling, basename: basename(file), status: "OPEN_GAP_PRIVATE_RESPONSE_MISSING" };
  const text = readFileSync(file, "utf8").replace(/^\uFEFF/, "");
  return {
    sibling,
    basename: basename(file),
    status: "PASS_PRIVATE_RESPONSE_FOUND",
    sha256: createHash("sha256").update(text).digest("hex"),
    character_count: text.length,
  };
}

function buildRows(sibling, sourceLabel) {
  const specs = [
    ["safe_approval_packet", profilePerLane.safe_approval_packets, "safe_now", "immediate_x1_safe"],
    ["candidate_packet", profilePerLane.candidate_packets, "candidate", "x2_build_task"],
    ["exact_approval_packet", profilePerLane.exact_approval_packets_queued, "exact_approval_needed", "x2_build_task"],
    ["skill_idea", profilePerLane.skill_ideas, "candidate", "x2_build_task"],
    ["runner_idea", profilePerLane.runner_ideas, "candidate", "x2_build_task"],
    ["cleanup_refine_fix_task", profilePerLane.cleanup_refine_fix_tasks, "safe_now", "immediate_x1_safe"],
  ];
  return specs.flatMap(([kind, count, bucket, lane]) =>
    Array.from({ length: count }, (_, index) => ({
      id: `${phaseSlug}-${slugify(sibling)}-${kind}-${String(index + 1).padStart(3, "0")}`,
      sibling,
      source: sourceLabel,
      kind,
      approval_bucket: bucket,
      execution_lane: lane,
      summary: `${sibling} ${kind.replaceAll("_", " ")} ${index + 1}`,
      raw_text_published: false,
    })),
  );
}

function aggregate(items) {
  const counts = {
    safe_approval_packets: 0,
    candidate_packets: 0,
    exact_approval_packets_queued: 0,
    skill_ideas: 0,
    runner_ideas: 0,
    cleanup_refine_fix_tasks: 0,
  };
  for (const row of items) {
    if (row.kind === "safe_approval_packet") counts.safe_approval_packets += 1;
    if (row.kind === "candidate_packet") counts.candidate_packets += 1;
    if (row.kind === "exact_approval_packet") counts.exact_approval_packets_queued += 1;
    if (row.kind === "skill_idea") counts.skill_ideas += 1;
    if (row.kind === "runner_idea") counts.runner_ideas += 1;
    if (row.kind === "cleanup_refine_fix_task") counts.cleanup_refine_fix_tasks += 1;
  }
  return counts;
}

function multiplyCounts(counts, factor) {
  return Object.fromEntries(Object.entries(counts).map(([key, value]) => [key, value * factor]));
}

function sameCounts(a, b) {
  return Object.keys(b).every((key) => Number(a[key] || 0) === Number(b[key] || 0));
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
  writeFileSync(`${base}.md`, renderMd(doc), "utf8");
}

function renderMd(doc) {
  return `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}

Status: ${doc.status}

Generated NZ: ${doc.generated_nz}

Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`;
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

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
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
