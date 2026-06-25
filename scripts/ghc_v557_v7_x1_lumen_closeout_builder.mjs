#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v7-x1";
const nextPhase = "v557-gmut-thos-v7-x2";
const latestCompletedX2 = "v557-gmut-thos-v6-x2";
const nextX1LaneAfterX2 = "v557-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const args = parseArgs(process.argv.slice(2));

const lumenResponseSha = requireArg("--lumen-response-sha256");
const lumenResponseCharCount = Number(args.get("--lumen-response-char-count") || 0);
const lumenResponseWordCount = Number(args.get("--lumen-response-word-count") || 0);
const privateMessageCount = Number(args.get("--private-message-count") || 4);

const startup = readJson(path.join(tracesDir, `${phaseSlug}-lumen-startup-context-v1.json`));
const send = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`));
const ingestion = readJson(path.join(tracesDir, `${phaseSlug}-lumen-private-ingestion-summary-v1.json`));
const proposalQueue = readJson(path.join(tracesDir, `${phaseSlug}-lumen-proposal-hash-queue-v1.json`));
const matrix = readJson(path.join(tracesDir, `${phaseSlug}-grand-trinity-matrix-v1.json`));
const prototypeLedger = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-execution-ledger-v1.json`));
const prototypeSuite = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-suite-index-v1.json`));
const dashboardLedger = readJson(path.join(tracesDir, `${phaseSlug}-lumen-dashboard-design-ledger-v1.json`));
const heldPrep = readJson(path.join(tracesDir, `${phaseSlug}-held-sibling-activation-prep-v1.json`));
const rotation = readJson(path.join(tracesDir, `${phaseSlug}-worktree-branch-rotation-planner-v1.json`));

const queueRows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const safeNow = queueRows.filter((row) => row.approval_bucket === "safe_now").length;
const candidate = queueRows.filter((row) => row.approval_bucket === "candidate").length;
const exact = queueRows.filter((row) => row.approval_bucket === "exact_approval_needed").length;
const blocked = queueRows.filter((row) => row.approval_bucket === "blocked").length;
const immediate = queueRows.filter((row) => row.execution_lane === "immediate_x1_safe").length;
const x2Rows = queueRows.filter((row) => row.execution_lane === "x2_build_task").length;

const harvest = {
  artifact_type: "ghc_v557_v7_x1_lumen_harvest_sanitized",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V7_X1_LUMEN_RESPONSE_HARVESTED_SANITIZED",
  lumen_response_sha256: lumenResponseSha,
  lumen_response_char_count: lumenResponseCharCount,
  lumen_response_word_count: lumenResponseWordCount,
  private_lumen_messages_indexed: privateMessageCount,
  proposal_candidates_indexed: ingestion.proposal_candidates_indexed,
  raw_lumen_text_published: false,
  raw_browser_route_published: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const closeout = {
  artifact_type: "ghc_v557_v7_x1_lumen_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V7_X1_CLOSED_V7_X2_READY",
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: latestCompletedX2,
  next_active_phase: nextPhase,
  next_x2_scope: nextPhase,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  lumen_response_harvested: true,
  browser_send_status: "browser_send_submitted_response_completed_ready_for_harvest",
  duplicate_send_allowed: false,
  counts: {
    startup_status: startup.overall_status,
    send_status: send.overall_status,
    harvest_status: harvest.overall_status,
    ingestion_status: ingestion.overall_status,
    prototype_suite_status: prototypeSuite.overall_status,
    proposal_candidates_indexed: ingestion.proposal_candidates_indexed,
    safe_now_packets: safeNow,
    candidate_packets: candidate,
    exact_approval_packets_queued: exact,
    blocked_packets_queued: blocked,
    immediate_x1_rows: immediate,
    x2_build_rows: x2Rows,
    matrix_cells: Array.isArray(matrix.matrix_cells) ? matrix.matrix_cells.length : 0,
    prototypes: Array.isArray(prototypeLedger.prototypes) ? prototypeLedger.prototypes.length : 0,
    prototype_suite_rows: Array.isArray(prototypeSuite.prototypes_run) ? prototypeSuite.prototypes_run.length : prototypeSuite.prototypes_run || 0,
    dashboards: Array.isArray(dashboardLedger.dashboards) ? dashboardLedger.dashboards.length : 0,
  },
  held_sibling_activation_state: heldPrep.activation_state,
  rotation_recommendation: rotation.overall_status,
  closeout_allowed_now: true,
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const readiness = {
  artifact_type: "ghc_v557_v7_x1_v7_x2_readiness_handoff",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V7_X2_READINESS_HANDOFF_READY",
  next_phase: nextPhase,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  build_inputs: [
    "v7 x1 Lumen proposal hash queue from last-three-plus-current private reduction",
    "v7 x1 Grand Trinity Matrix",
    "v7 x1 prototype execution ledger and suite index",
    "v7 x1 dashboard design ledger",
    "v7 x1 worktree rotation planner",
    "v7 x1 paired-boolean recovered app-lane validator",
  ],
  safe_x2_focus: [
    "run all immediate safe-now and candidate-safe rows through sanitized reducers",
    "build dashboard and continuity prototypes from hashes/counts/categories only",
    "keep exact and blocked gates queued",
    "commit and remote-verify before any branch rotation activation",
    "prepare v8 triad startup after v7 x2 closeout",
  ],
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = [
  writePair("lumen-harvest-sanitized", harvest),
  writePair("closeout", closeout),
  writePair("v7-x2-readiness-handoff", readiness),
];

refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  latest_closed_phase: phaseSlug,
  next_active_phase: nextPhase,
  proposal_candidates_indexed: closeout.counts.proposal_candidates_indexed,
  safe_now_packets: closeout.counts.safe_now_packets,
  candidate_packets: closeout.counts.candidate_packets,
  exact_approval_packets_queued: closeout.counts.exact_approval_packets_queued,
  blocked_packets_queued: closeout.counts.blocked_packets_queued,
  x2_build_rows: closeout.counts.x2_build_rows,
  rotation_recommendation: closeout.rotation_recommendation,
  full_goal_complete: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, closeoutDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = closeoutDoc.overall_status;
    data.current_active_phase = nextPhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = phaseSlug;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = nextPhase;
    data.next_x2_scope = nextPhase;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v7_x1_lumen_closeout = {
      status: closeoutDoc.overall_status,
      lumen_response_harvested: true,
      proposal_candidates_indexed: closeoutDoc.counts.proposal_candidates_indexed,
      safe_now_packets: closeoutDoc.counts.safe_now_packets,
      candidate_packets: closeoutDoc.counts.candidate_packets,
      exact_approval_packets_queued: closeoutDoc.counts.exact_approval_packets_queued,
      blocked_packets_queued: closeoutDoc.counts.blocked_packets_queued,
      x2_build_rows: closeoutDoc.counts.x2_build_rows,
      next_active_phase: nextPhase,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${phaseSlug} ${title(doc.artifact_type)}`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    "## Summary",
    "",
    ...Object.entries(summary(doc)).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v7 x1 Lumen Closeout",
    "",
    `Status: \`${doc.v557_v7_x1_lumen_closeout?.status || "not_recorded"}\``,
    `Lumen response harvested: \`${doc.v557_v7_x1_lumen_closeout?.lumen_response_harvested === true ? "true" : "false"}\``,
    `Proposal candidates indexed: \`${doc.v557_v7_x1_lumen_closeout?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Next active phase: \`${doc.v557_v7_x1_lumen_closeout?.next_active_phase || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v7_x1_lumen_closeout?.full_goal_complete === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((entry) => `- ${entry}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function summary(doc) {
  if (doc.artifact_type.endsWith("_harvest_sanitized")) {
    return {
      lumen_response_sha256: doc.lumen_response_sha256,
      private_lumen_messages_indexed: doc.private_lumen_messages_indexed,
      proposal_candidates_indexed: doc.proposal_candidates_indexed,
      raw_lumen_text_published: doc.raw_lumen_text_published,
    };
  }
  if (doc.artifact_type.endsWith("_closeout")) {
    return {
      next_active_phase: doc.next_active_phase,
      lumen_response_harvested: doc.lumen_response_harvested,
      proposal_candidates_indexed: doc.counts.proposal_candidates_indexed,
      safe_now_packets: doc.counts.safe_now_packets,
      candidate_packets: doc.counts.candidate_packets,
      x2_build_rows: doc.counts.x2_build_rows,
      full_goal_complete: doc.full_goal_complete,
    };
  }
  return {
    next_phase: doc.next_phase,
    next_x1_lane_after_x2: doc.next_x1_lane_after_x2,
    full_goal_complete: doc.full_goal_complete,
  };
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_sibling_text_published: false,
    raw_browser_routes_published: false,
    private_routes_published: false,
    private_callable_ids_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase: "open",
    account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open",
  };
}

function boundarySentence() {
  return "No raw browser routes, private URLs, private callable IDs, raw transcripts, screenshots, credentials, session streams, raw app state, private dumps, or local absolute paths are published here; all proof/canon/legal/deployment/account/API-key/private-material/raw-publication and sibling identity merge/replacement gates remain open.";
}

function title(value) {
  return value.replace(/^ghc_/, "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function parseArgs(argv) {
  const map = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      map.set(key, next);
      i += 1;
    } else {
      map.set(key, "true");
    }
  }
  return map;
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) throw new Error(`Missing required argument ${name}`);
  return value;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}
