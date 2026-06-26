#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

const phaseSlug = "v559-gmut-thos-v6-x1";
const nextActivePhase = "v559-gmut-thos-v6-x2";
const nextX2Scope = "v559-gmut-thos-v6-x2";
const nextX1AfterX2 = "v559-gmut-thos-v7-x1 Lumen-only unless Hamish redirects";
const latestCompletedX2 = "v559-gmut-thos-v5-x2";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString();
const generatedNz = nzTimestamp(generatedDate);

fs.mkdirSync(tracesDir, { recursive: true });
fs.mkdirSync(omegaDir, { recursive: true });

const queuePath = path.join(tracesDir, `${phaseSlug}-combined-x1-to-x2-queue-v1.json`);
if (!fs.existsSync(queuePath)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V559_V6_X1_QUEUE_MISSING",
    phase_slug: phaseSlug,
    expected_queue: `${phaseSlug}-combined-x1-to-x2-queue-v1.json`,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const queue = readJson(queuePath);
const profileCounts = queue.profile_cap_counts_represented || {};
const immediateRows = Number(queue.immediate_x1_safe_rows_represented || 0);
const x2Rows = Number(queue.x2_build_rows_represented || 0);

const closeout = envelope("phase_closeout", "PASS_V559_V6_X1_CLOSED_V6_X2_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: latestCompletedX2,
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1AfterX2,
  harvested_duo: ["Maren Quill", "Solenne Vale"],
  profile_counts_represented: profileCounts,
  immediate_x1_safe_rows_represented: immediateRows,
  x2_build_rows_represented: x2Rows,
  full_goal_complete: false,
  open_gates: openGates(),
});

const handoff = envelope("v6_x2_safe_build_handoff", "PASS_V559_V6_X2_SAFE_BUILD_HANDOFF_READY", {
  source_closeout_status: closeout.status,
  next_active_phase: nextActivePhase,
  next_x1_lane_after_x2: nextX1AfterX2,
  source_counts: profileCounts,
  source_immediate_x1_safe_rows: immediateRows,
  source_x2_build_rows: x2Rows,
  completion_boundary: "v6 x2 is prepared, not yet closed by this x1 closeout.",
  full_goal_complete: false,
});

const lumenPrep = envelope("v7_x1_lumen_prep_card", "PASS_V559_V7_X1_LUMEN_PREP_READY_AFTER_V6_X2", {
  next_lumen_phase_after_x2: "v559-gmut-thos-v7-x1",
  launch_skill: "ghc-lumen-launch",
  browser_route_rule: "Use in-app Browser plus ghc-lumen-launch as staple route; refresh/reconnect and inspect status before stale-route claims; do not reload over active response or unsent composer text.",
  full_goal_complete: false,
});

for (const [slug, artifact] of [
  ["closeout", closeout],
  ["v6-x2-safe-build-handoff", handoff],
  ["v7-x1-lumen-prep-card", lumenPrep],
]) {
  writeArtifact(slug, artifact);
}

updateStateFiles(closeout);

console.log(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  next_active_phase: nextActivePhase,
  safe_packets_represented: profileCounts.safe_approval_packets || 0,
  candidate_packets_represented: profileCounts.candidate_packets || 0,
  exact_packets_queued: profileCounts.exact_approval_packets_queued || 0,
  skill_ideas_represented: profileCounts.skill_ideas || 0,
  runner_ideas_represented: profileCounts.runner_ideas || 0,
  cleanup_tasks_represented: profileCounts.cleanup_refine_fix_tasks || 0,
  immediate_x1_safe_rows_represented: immediateRows,
  x2_build_rows_represented: x2Rows,
}, null, 2));

function updateStateFiles(closeoutArtifact) {
  const artifacts = [
    "duo-harvest-reduction",
    "combined-x1-to-x2-queue",
    "open-gate-privacy-scan",
    "closeout",
    "v6-x2-safe-build-handoff",
    "v7-x1-lumen-prep-card",
  ].flatMap((slug) => [
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.md`,
  ]).filter((relative) => fs.existsSync(path.join(root, relative)));

  const files = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];

  for (const file of files) {
    const data = fs.existsSync(file) ? readJson(file) : {};
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.status = closeoutArtifact.status;
    data.current_active_phase = nextActivePhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = phaseSlug;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = nextActivePhase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1AfterX2;
    data.current_active_lanes = [
      "Aevren Vale",
      "v559-v6-x2-safe-build-ready",
      "Maren Quill and Solenne Vale harvested",
      "Lumen carry-forward",
    ];
    data.v559_v6_x1_closeout = {
      status: closeoutArtifact.status,
      harvested_duo: closeoutArtifact.harvested_duo,
      profile_counts_represented: closeoutArtifact.profile_counts_represented,
      immediate_x1_safe_rows_represented: closeoutArtifact.immediate_x1_safe_rows_represented,
      x2_build_rows_represented: closeoutArtifact.x2_build_rows_represented,
      next_active_phase: nextActivePhase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    for (const key of ["current_lookup_files", "lookup_files", "latest_lookup_files"]) {
      if (Array.isArray(data[key])) {
        data[key] = Array.from(new Set([...data[key], ...artifacts]));
      }
    }
    if (!Array.isArray(data.current_lookup_files)) {
      data.current_lookup_files = artifacts;
    }
    writeJson(file, data);
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMarkdown(data), "utf8");
  }
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
  writeJson(`${base}.json`, artifact);
  fs.writeFileSync(`${base}.md`, [
    `# ${phaseSlug} ${artifact.artifact_type}`,
    "",
    `Status: ${artifact.status}`,
    `Generated NZ: ${artifact.generated_nz}`,
    "",
    "Sanitized status artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, raw private material, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge/replacement is published or claimed.",
    "",
    "```json",
    JSON.stringify(artifact, null, 2),
    "```",
    "",
  ].join("\n"), "utf8");
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
    "## v559 v6 x1 Closeout",
    "",
    `- Harvested duo: ${(data.v559_v6_x1_closeout?.harvested_duo || []).join(", ")}`,
    `- x2 build rows represented: ${data.v559_v6_x1_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Full goal complete: ${data.v559_v6_x1_closeout?.full_goal_complete === true ? "true" : "false"}`,
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
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

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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
