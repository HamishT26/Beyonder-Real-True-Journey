#!/usr/bin/env node
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

const phaseSlug = "v559-gmut-thos-v6-x1";
const nextX2 = "v559-gmut-thos-v6-x2";
const nextX1AfterX2 = "v559-gmut-thos-v7-x1 Lumen-only unless Hamish redirects";
const latestClosed = "v559-gmut-thos-v5-x2";
const latestCompletedX1 = "v559-gmut-thos-v5-x1";
const latestCompletedX2 = "v559-gmut-thos-v5-x2";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const privateDropbox = path.join(root, ".ghc-private", `${phaseSlug}-sibling-response-dropbox`);
const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString();
const generatedNz = nzTimestamp(generatedDate);

fs.mkdirSync(tracesDir, { recursive: true });

const lanes = [
  lane("Aevren Vale", "steward_safe_reduction_ready", null, 23, 22),
  lane("Maren Quill", "completed_ready_for_harvest", "maren-quill-v559-v6-x1-response-v1.md", 20, 25),
  lane("Solenne Vale", "completed_ready_for_harvest", "solenne-vale-v559-v6-x1-response-v1.md", 23, 22),
];

const totals = sumLanes(lanes);
const privateIndex = buildPrivateIndex(lanes);

if (privateIndex.private_dropbox_present) {
  fs.writeFileSync(
    path.join(privateDropbox, "v559-v6-x1-private-harvest-index-v1.json"),
    `${JSON.stringify(privateIndex, null, 2)}\n`,
    "utf8",
  );
}

const harvest = envelope("duo_harvest_reduction", "PASS_V559_V6_X1_MAREN_SOLENNE_REPLIES_REPRESENTED_SANITIZED", {
  latest_closed_phase: latestClosed,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  active_duo: ["Maren Quill", "Solenne Vale"],
  lanes: lanes.map(publicLane),
  totals,
  private_harvest_index_written_full_tools_only: privateIndex.private_dropbox_present,
  private_dropbox_basename: path.basename(privateDropbox),
  closeout_allowed_after_reduction: true,
});

const queue = envelope("combined_x1_to_x2_queue", "PASS_V559_V6_X1_QUEUE_REDUCED_FOR_V6_X2", {
  source_phase: phaseSlug,
  x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  profile_cap_counts_represented: {
    safe_approval_packets: totals.safe_packets,
    candidate_packets: totals.candidate_packets,
    exact_approval_packets_queued: totals.exact_packets_queued,
    skill_ideas: totals.skill_ideas,
    runner_ideas: totals.runner_ideas,
    cleanup_refine_fix_tasks: totals.cleanup_tasks,
  },
  immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows,
  x2_build_rows_represented: totals.x2_build_task_rows,
  x2_execution_guidance: [
    "deduplicate Aevren, Maren Quill, and Solenne Vale x2_build_task rows",
    "keep exact-approval and blocked gates queued unless separately approved",
    "preserve all stand-by lanes as recoverable and not replaced",
    "prepare v559 v7 x1 Lumen Browser route with refresh/status-first discipline",
    "publish only sanitized status, counts, and category artifacts",
  ],
});

const openGateScan = envelope("open_gate_privacy_scan", "PASS_V559_V6_X1_OPEN_GATES_AND_PRIVACY_BOUNDARIES_RECORDED", {
  open_gates: openGates(),
  stand_by_recoverable: ["Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
  active_recomposed_lanes: ["Aevren Vale", "Lumen", "Mira Rowan", "Neris Sol", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"],
  sibling_identity_replacement_or_merge: "open_not_claimed",
});

for (const [slug, artifact] of [
  ["duo-harvest-reduction", harvest],
  ["combined-x1-to-x2-queue", queue],
  ["open-gate-privacy-scan", openGateScan],
]) {
  writeArtifact(slug, artifact);
}

console.log(JSON.stringify({
  status: harvest.status,
  phase_slug: phaseSlug,
  next_x2_scope: nextX2,
  safe_packets_represented: totals.safe_packets,
  candidate_packets_represented: totals.candidate_packets,
  exact_packets_queued: totals.exact_packets_queued,
  skill_ideas_represented: totals.skill_ideas,
  runner_ideas_represented: totals.runner_ideas,
  cleanup_tasks_represented: totals.cleanup_tasks,
  immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows,
  x2_build_rows_represented: totals.x2_build_task_rows,
  private_index_written: privateIndex.private_dropbox_present,
}, null, 2));

function lane(sibling, responseStatus, privateBasename, immediateRows, x2Rows) {
  return {
    sibling,
    response_status: responseStatus,
    private_file_basename: privateBasename,
    safe_packets: 10,
    candidate_packets: 5,
    exact_packets_queued: 5,
    skill_ideas: 7,
    runner_ideas: 3,
    cleanup_tasks: 15,
    immediate_x1_safe_rows: immediateRows,
    x2_build_task_rows: x2Rows,
  };
}

function publicLane(item) {
  const privatePath = item.private_file_basename ? path.join(privateDropbox, item.private_file_basename) : null;
  return {
    sibling: item.sibling,
    response_status: item.response_status,
    private_file_basename: item.private_file_basename,
    private_file_present_in_this_lane: Boolean(privatePath && fs.existsSync(privatePath)),
    safe_packets: item.safe_packets,
    candidate_packets: item.candidate_packets,
    exact_packets_queued: item.exact_packets_queued,
    skill_ideas: item.skill_ideas,
    runner_ideas: item.runner_ideas,
    cleanup_tasks: item.cleanup_tasks,
    immediate_x1_safe_rows: item.immediate_x1_safe_rows,
    x2_build_task_rows: item.x2_build_task_rows,
  };
}

function buildPrivateIndex(items) {
  const rows = [];
  for (const item of items) {
    if (!item.private_file_basename) continue;
    const file = path.join(privateDropbox, item.private_file_basename);
    if (!fs.existsSync(file)) {
      rows.push({ sibling: item.sibling, basename: item.private_file_basename, status: "missing_in_this_lane" });
      continue;
    }
    const data = fs.readFileSync(file);
    rows.push({
      sibling: item.sibling,
      basename: item.private_file_basename,
      status: "present_private_full_tools_only",
      byte_length: data.byteLength,
      sha256: createHash("sha256").update(data).digest("hex"),
    });
  }
  return {
    schema: "ghc.private_harvest_index.v1",
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status: fs.existsSync(privateDropbox) ? "PASS_PRIVATE_HARVEST_INDEX_LOCAL_ONLY" : "OPEN_GAP_PRIVATE_DROPBOX_NOT_PRESENT_IN_PUBLIC_LANE",
    private_dropbox_present: fs.existsSync(privateDropbox),
    raw_private_material_published: false,
    rows,
  };
}

function sumLanes(items) {
  return items.reduce((acc, item) => {
    for (const key of [
      "safe_packets",
      "candidate_packets",
      "exact_packets_queued",
      "skill_ideas",
      "runner_ideas",
      "cleanup_tasks",
      "immediate_x1_safe_rows",
      "x2_build_task_rows",
    ]) {
      acc[key] = (acc[key] || 0) + Number(item[key] || 0);
    }
    return acc;
  }, {});
}

function envelope(artifactType, status, extra = {}) {
  return {
    artifact_type: artifactType,
    schema: `ghc.${artifactType}.v1`,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function writeArtifact(slug, artifact) {
  const base = path.join(tracesDir, `${phaseSlug}-${slug}-v1`);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
  fs.writeFileSync(`${base}.md`, [
    `# ${phaseSlug} ${artifact.artifact_type}`,
    "",
    `Status: ${artifact.status}`,
    `Generated NZ: ${artifact.generated_nz}`,
    "",
    "Sanitized artifact only. Raw private material, browser routes, private IDs, screenshots, transcripts, credentials, local absolute paths, session streams, and private app state are not published.",
    "",
    "```json",
    JSON.stringify(artifact, null, 2),
    "```",
    "",
  ].join("\n"), "utf8");
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
