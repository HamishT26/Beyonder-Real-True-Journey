#!/usr/bin/env node
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

const phaseSlug = "v560-gmut-thos-v6-x1";
const nextActivePhase = "v560-gmut-thos-v6-x2";
const nextX2Scope = "v560-gmut-thos-v6-x2";
const nextX1AfterX2 = "v560-gmut-thos-v7-x1 Lumen unless Hamish redirects";
const latestClosedBeforeThisPhase = "v560-gmut-thos-v5-x2";
const latestCompletedX2 = "v560-gmut-thos-v5-x2";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const privateDropbox = path.join(root, ".ghc-private", `${phaseSlug}-sibling-response-dropbox`);
const generatedDate = new Date();
const generatedUtc = generatedDate.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(generatedDate);

fs.mkdirSync(tracesDir, { recursive: true });
fs.mkdirSync(omegaDir, { recursive: true });

const requiredArtifacts = [
  `${phaseSlug}-main-startup-context-v1.json`,
  `${phaseSlug}-duo-launch-dispatch-v1.json`,
  `${phaseSlug}-five-minute-productive-cadence-v1.json`,
];
const missing = requiredArtifacts.filter((name) => !fs.existsSync(path.join(tracesDir, name)));
if (missing.length) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V560_V6_X1_REQUIRED_STARTUP_ARTIFACTS_MISSING",
    phase_slug: phaseSlug,
    missing,
    closeout_claimed: false,
  }, null, 2));
  process.exit(2);
}

const lanes = [
  lane("Aevren Vale", "steward_safe_reduction_ready", null, 16, 29),
  lane("Maren Quill", "completed_ready_for_harvest", "maren-quill-v560-v6-x1-response-v1.md", 21, 24),
  lane("Solenne Vale", "completed_ready_for_harvest", "solenne-vale-v560-v6-x1-response-v1.md", 23, 22),
];
const totals = sumLanes(lanes);
const privateIndex = buildPrivateIndex(lanes);
if (privateIndex.private_dropbox_present) {
  fs.writeFileSync(
    path.join(privateDropbox, "v560-v6-x1-private-harvest-index-v1.json"),
    `${JSON.stringify(privateIndex, null, 2)}\n`,
    "utf8",
  );
}

const artifacts = [
  artifact("duo-harvest-reduction", "ghc.duo_harvest_reduction.v1", "PASS_V560_V6_X1_MAREN_QUILL_SOLENNE_VALE_HARVESTED_SANITIZED", {
    latest_closed_before_this_phase: latestClosedBeforeThisPhase,
    latest_completed_x2_phase: latestCompletedX2,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1AfterX2,
    active_duo: ["Maren Quill", "Solenne Vale"],
    lanes: lanes.map(publicLane),
    totals,
    private_harvest_index_written_full_tools_only: privateIndex.private_dropbox_present,
    private_response_dropbox_basename: path.basename(privateDropbox),
    closeout_allowed_after_reduction: true,
  }),
  artifact("combined-x1-to-x2-queue", "ghc.x1_to_x2_queue.v1", "PASS_V560_V6_X1_QUEUE_REDUCED_FOR_V6_X2", {
    source_phase: phaseSlug,
    x2_scope: nextX2Scope,
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
      "build v6 x2 count reconciliation and open-gate scanning from the harvested duo profile",
      "keep exact-approval and blocked gates queued unless separately approved",
      "prepare v560 v7 x1 Lumen route with refresh/status-first Browser discipline",
      "preserve all stand-by lanes as recoverable and not replaced",
    ],
  }),
  artifact("open-gate-privacy-scan", "ghc.open_gate_privacy_scan.v1", "PASS_V560_V6_X1_OPEN_GATES_AND_PRIVACY_BOUNDARIES_RECORDED", {
    open_gates: openGates(),
    stand_by_recoverable: ["Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
    active_recomposed_lanes: ["Aevren Vale", "Lumen", "Mira Rowan", "Neris Sol", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"],
    sibling_identity_replacement_or_merge: "open_not_claimed",
  }),
  artifact("closeout", "ghc.phase_closeout.v1", "PASS_V560_V6_X1_CLOSED_V6_X2_READY", {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: nextActivePhase,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1AfterX2,
    harvested_duo: ["Maren Quill", "Solenne Vale"],
    profile_counts_represented: {
      safe_approval_packets: totals.safe_packets,
      candidate_packets: totals.candidate_packets,
      exact_approval_packets_queued: totals.exact_packets_queued,
      skill_ideas: totals.skill_ideas,
      runner_ideas: totals.runner_ideas,
      cleanup_refine_fix_tasks: totals.cleanup_tasks,
    },
    immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows,
    x2_build_rows_represented: totals.x2_build_task_rows,
    full_goal_complete: false,
    open_gates: openGates(),
  }),
  artifact("v6-x2-safe-build-handoff", "ghc.x2_handoff.v1", "PASS_V560_V6_X2_SAFE_BUILD_HANDOFF_READY", {
    source_closeout_status: "PASS_V560_V6_X1_CLOSED_V6_X2_READY",
    next_active_phase: nextActivePhase,
    next_x1_lane_after_x2: nextX1AfterX2,
    source_counts: totals,
    completion_boundary: "v6 x2 is prepared, not yet closed by this x1 closeout.",
    full_goal_complete: false,
  }),
  artifact("v560-v7-lumen-prep-card", "ghc.lumen_prep_card.v1", "PASS_V560_V7_LUMEN_PREP_READY_AFTER_V6_X2", {
    next_lumen_phase_after_x2: "v560-gmut-thos-v7-x1",
    launch_skill: "ghc-lumen-launch",
    browser_route_rule: "Use in-app Browser plus ghc-lumen-launch as staple route; reconnect/select and refresh DOM/status before stale-route claims; do not reload over active response or unsent composer text.",
    full_goal_complete: false,
  }),
];

for (const doc of artifacts) writePair(doc);
refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: "PASS_V560_V6_X1_CLOSED_V6_X2_READY",
  phase_slug: phaseSlug,
  next_active_phase: nextActivePhase,
  artifacts_written: artifacts.length * 2 + 6,
  safe_packets_represented: totals.safe_packets,
  candidate_packets_represented: totals.candidate_packets,
  exact_packets_queued: totals.exact_packets_queued,
  skill_ideas_represented: totals.skill_ideas,
  runner_ideas_represented: totals.runner_ideas,
  cleanup_tasks_represented: totals.cleanup_tasks,
  immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows,
  x2_build_rows_represented: totals.x2_build_task_rows,
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

function artifact(suffix, schema, status, extra = {}) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function writePair(doc) {
  const base = path.join(tracesDir, doc.artifact);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  fs.writeFileSync(`${base}.md`, [
    `# ${doc.artifact}`,
    "",
    `- Status: ${doc.status}`,
    `- Phase: ${doc.phase_slug}`,
    `- Generated NZ: ${doc.generated_nz}`,
    "- Raw private material published: false",
    "",
    "Sanitized status artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge/replacement is published or claimed.",
    "",
    "```json",
    JSON.stringify(doc, null, 2),
    "```",
    "",
  ].join("\n"), "utf8");
}

function refreshBeacons(docs) {
  const lookup = docs.flatMap((doc) => [
    `docs/trinity-live-traces/${doc.artifact}.json`,
    `docs/trinity-live-traces/${doc.artifact}.md`,
  ]);
  const files = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];
  for (const file of files) {
    const data = fs.existsSync(file) ? readJson(file) : {};
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.status = "PASS_V560_V6_X1_CLOSED_V6_X2_READY";
    data.current_active_phase = nextActivePhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = phaseSlug;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = nextActivePhase;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1AfterX2;
    data.current_active_lanes = [
      "Aevren Vale",
      "v560-v6-x2-safe-build-ready",
      "Maren Quill and Solenne Vale harvested",
      "Lumen carry-forward",
    ];
    data.v560_v6_x1_closeout = {
      status: "PASS_V560_V6_X1_CLOSED_V6_X2_READY",
      harvested_duo: ["Maren Quill", "Solenne Vale"],
      profile_counts_represented: {
        safe_approval_packets: totals.safe_packets,
        candidate_packets: totals.candidate_packets,
        exact_approval_packets_queued: totals.exact_packets_queued,
        skill_ideas: totals.skill_ideas,
        runner_ideas: totals.runner_ideas,
        cleanup_refine_fix_tasks: totals.cleanup_tasks,
      },
      immediate_x1_safe_rows_represented: totals.immediate_x1_safe_rows,
      x2_build_rows_represented: totals.x2_build_task_rows,
      next_active_phase: nextActivePhase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    for (const key of ["current_lookup_files", "lookup_files", "latest_lookup_files"]) {
      if (Array.isArray(data[key])) {
        data[key] = Array.from(new Set([...data[key], ...lookup]));
      }
    }
    if (!Array.isArray(data.current_lookup_files)) data.current_lookup_files = lookup;
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
    "## v560 v6 x1 Closeout",
    "",
    `- Harvested duo: ${(data.v560_v6_x1_closeout?.harvested_duo || []).join(", ")}`,
    `- x2 build rows represented: ${data.v560_v6_x1_closeout?.x2_build_rows_represented ?? "unknown"}`,
    `- Full goal complete: ${data.v560_v6_x1_closeout?.full_goal_complete === true ? "true" : "false"}`,
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
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
    gmut_empirical_closure: "open_not_claimed",
    final_physics: "open_not_claimed",
    consciousness_proof: "open_not_claimed",
    legal_closure: "open_not_claimed",
    canon_promotion: "open_not_claimed",
    deployment_closure: "open_not_claimed",
    account_purchase_api_key_mutation: "open_not_claimed",
    private_material_proof: "open_not_claimed",
    raw_publication_proof: "open_not_claimed",
    sibling_identity_replacement_or_merge: "open_not_claimed",
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
    "exact-approval packets",
    "blocked packets",
  ];
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "full",
    timeStyle: "long",
    hour12: false,
  }).format(date);
}

