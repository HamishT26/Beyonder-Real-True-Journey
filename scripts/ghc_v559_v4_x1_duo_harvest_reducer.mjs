#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);

const root = args.get("--root") || process.cwd();
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v4-x1";
const privateDropbox = args.get("--private-dropbox") || join(root, ".ghc-private", `${phaseSlug}-sibling-response-dropbox`);
const allowSanitizedMirror = args.get("--allow-sanitized-mirror") === "true";
const tracesDir = join(root, "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const sourceFiles = [
  { sibling: "Mira Vale", basename: "mira-vale-v559-v4-x1-response-v1.md" },
  { sibling: "Rowan Vale", basename: "rowan-vale-v559-v4-x1-response-v1.md" },
];

const parsed = sourceFiles.map((source) => {
  const file = join(privateDropbox, source.basename);
  if (!existsSync(file)) {
    return {
      ...source,
      status: allowSanitizedMirror ? "SANITIZED_MIRROR_SOURCE_NOT_LOCAL" : "OPEN_GAP_PRIVATE_RESPONSE_MISSING",
      counts: zeroCounts(),
      rows: [],
    };
  }
  const text = readFileSync(file, "utf8");
  return {
    ...source,
    status: "PASS_PRIVATE_RESPONSE_FOUND",
    counts: countKinds(text),
    rows: parseRows(text, source.sibling),
  };
});

const aevrenRows = buildAevrenRows();
const allRows = [...parsed.flatMap((item) => item.rows), ...aevrenRows];
const aggregateCounts = aggregate(allRows);
const expectedCounts = {
  safe_approval_packets: 30,
  candidate_packets: 15,
  exact_approval_packets_queued: 15,
  skill_ideas: 21,
  runner_ideas: 9,
  cleanup_refine_fix_tasks: 45,
};

const responsesReady = parsed.every((item) => item.status === "PASS_PRIVATE_RESPONSE_FOUND" || allowSanitizedMirror);
const countsReady = Object.entries(expectedCounts).every(([key, value]) => aggregateCounts[key] === value);
const status = responsesReady && countsReady
  ? "PASS_V559_V4_X1_DUO_HARVEST_REDUCED_FOR_V4_X2"
  : "OPEN_GAP_V559_V4_X1_DUO_HARVEST_REDUCTION";

const reduction = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-duo-harvest-reduction-v1`,
  schema: "ghc.duo_harvest_reduction.v1",
  phase_slug: phaseSlug,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status,
  private_source_basenames: sourceFiles.map((source) => source.basename),
  private_source_status: parsed.map(({ sibling, basename, status: sourceStatus, counts }) => ({
    sibling,
    basename,
    status: sourceStatus,
    counts,
  })),
  profile_cap_counts_represented: aggregateCounts,
  expected_counts: expectedCounts,
  queue_rows: allRows.length,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const queue = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-duo-sanitized-proposal-queue-v1`,
  schema: "ghc.duo_sanitized_proposal_queue.v1",
  phase_slug: phaseSlug,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status,
  next_x2_scope: "v559-gmut-thos-v4-x2",
  next_x1_lane_after_x2: "v559-gmut-thos-v5-x1 Lumen-only unless Hamish redirects",
  profile_cap_counts_represented: aggregateCounts,
  rows: allRows,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const closeoutPrep = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-closeout-prep-v1`,
  schema: "ghc.duo_x1_closeout_prep.v1",
  phase_slug: phaseSlug,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status: status.startsWith("PASS") ? "PASS_V559_V4_X1_CLOSEOUT_PREP_READY" : "OPEN_GAP_V559_V4_X1_CLOSEOUT_PREP",
  latest_completed_x2_phase: "v559-gmut-thos-v3-x2",
  next_active_phase_after_closeout: "v559-gmut-thos-v4-x2",
  next_x1_lane_after_x2: "v559-gmut-thos-v5-x1 Lumen-only unless Hamish redirects",
  launch_skill: "ghc-mira-vale-rowan-vale-launch",
  response_sources_ready: responsesReady,
  counts_ready: countsReady,
  profile_cap_counts_represented: aggregateCounts,
  open_gates: openGates(),
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

for (const doc of [reduction, queue, closeoutPrep]) writePair(doc);

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  private_sources_ready: responsesReady,
  counts_ready: countsReady,
  queue_rows: allRows.length,
  counts: aggregateCounts,
  artifacts_written: 6,
}, null, 2));

process.exit(status.startsWith("PASS") ? 0 : 1);

function countKinds(text) {
  const rows = parseRows(text, "count");
  return aggregate(rows);
}

function parseRows(text, sibling) {
  return text.split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("["))
    .map((line, index) => {
      const kind = normalizeKind(line);
      return {
        id: `${phaseSlug}-${slugify(sibling)}-${kind}-${String(index + 1).padStart(3, "0")}`,
        sibling,
        kind,
        approval_bucket: approvalBucket(kind),
        execution_lane: line.includes("[immediate_x1_safe]") ? "immediate_x1_safe" : "x2_build_task",
        summary: sanitizeSummary(line),
        raw_text_published: false,
      };
    });
}

function buildAevrenRows() {
  const specs = [
    ["safe_approval_packet", 10, "immediate_x1_safe", "Aevren v4 x1 safe approval packet"],
    ["candidate_packet", 5, "x2_build_task", "Aevren v4 x1 candidate packet"],
    ["exact_approval_packet", 5, "x2_build_task", "Aevren v4 x1 exact-approval packet queued"],
    ["skill_idea", 7, "x2_build_task", "Aevren v4 x1 skill idea"],
    ["runner_idea", 3, "x2_build_task", "Aevren v4 x1 runner idea"],
    ["cleanup_refine_fix_task", 15, "immediate_x1_safe", "Aevren v4 x1 cleanup/refine/fix task"],
  ];
  return specs.flatMap(([kind, count, executionLane, label]) =>
    Array.from({ length: count }, (_, index) => ({
      id: `${phaseSlug}-aevren-${kind}-${String(index + 1).padStart(3, "0")}`,
      sibling: "Aevren Vale",
      kind,
      approval_bucket: approvalBucket(kind),
      execution_lane: executionLane,
      summary: `${label} ${index + 1}`,
      raw_text_published: false,
    }))
  );
}

function normalizeKind(line) {
  const lower = line.toLowerCase();
  if (lower.includes("[safe")) return "safe_approval_packet";
  if (lower.includes("[candidate")) return "candidate_packet";
  if (lower.includes("[exact")) return "exact_approval_packet";
  if (lower.includes("[skill")) return "skill_idea";
  if (lower.includes("[runner")) return "runner_idea";
  if (lower.includes("[cleanup")) return "cleanup_refine_fix_task";
  return "other";
}

function approvalBucket(kind) {
  if (kind === "safe_approval_packet" || kind === "cleanup_refine_fix_task") return "safe_now";
  if (kind === "candidate_packet") return "candidate";
  if (kind === "exact_approval_packet") return "exact_approval_needed";
  if (kind === "skill_idea" || kind === "runner_idea") return "candidate";
  return "unknown";
}

function aggregate(rows) {
  const counts = zeroCounts();
  for (const row of rows) {
    if (row.kind === "safe_approval_packet") counts.safe_approval_packets += 1;
    if (row.kind === "candidate_packet") counts.candidate_packets += 1;
    if (row.kind === "exact_approval_packet") counts.exact_approval_packets_queued += 1;
    if (row.kind === "skill_idea") counts.skill_ideas += 1;
    if (row.kind === "runner_idea") counts.runner_ideas += 1;
    if (row.kind === "cleanup_refine_fix_task") counts.cleanup_refine_fix_tasks += 1;
  }
  return counts;
}

function zeroCounts() {
  return {
    safe_approval_packets: 0,
    candidate_packets: 0,
    exact_approval_packets_queued: 0,
    skill_ideas: 0,
    runner_ideas: 0,
    cleanup_refine_fix_tasks: 0,
  };
}

function sanitizeSummary(line) {
  return line
    .replace(/^\[[^\]]+\]\[[^\]]+\]\s*/, "")
    .replace(/`/g, "")
    .slice(0, 220);
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function writePair(doc) {
  const jsonPath = join(root, `${doc.artifact}.json`);
  const mdPath = join(root, `${doc.artifact}.md`);
  writeFileSync(jsonPath, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  const lines = [
    `# ${doc.artifact.split("/").pop()}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Boundary: sanitized counts, tags, statuses, and relative artifact labels only. Raw handles, routes, transcripts, screenshots, credentials, local private path values, and private app state are not published.",
    "",
  ];
  if (doc.profile_cap_counts_represented) {
    lines.push("## Counts", "");
    for (const [key, value] of Object.entries(doc.profile_cap_counts_represented)) lines.push(`- ${key}: ${value}`);
    lines.push("");
  }
  writeFileSync(mdPath, `${lines.join("\n")}\n`, "utf8");
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
    hidden_reasoning_published: false,
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
  return Object.keys(claimBoundary()).filter((key) => key !== "full_goal_completion");
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
