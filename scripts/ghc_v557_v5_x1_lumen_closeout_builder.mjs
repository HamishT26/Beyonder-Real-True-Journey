#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v5-x1";
const nextPhase = "v557-gmut-thos-v5-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const startup = readJson(path.join(tracesDir, `${phaseSlug}-lumen-startup-context-v1.json`));
const send = readJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`));
const safeCadence = readJson(path.join(tracesDir, `${phaseSlug}-lumen-background-supervision-watchcard-v1.json`));
const ingestion = readJson(path.join(tracesDir, `${phaseSlug}-lumen-private-ingestion-summary-v1.json`));
const proposalQueue = readJson(path.join(tracesDir, `${phaseSlug}-lumen-proposal-hash-queue-v1.json`));
const matrix = readJson(path.join(tracesDir, `${phaseSlug}-grand-trinity-matrix-v1.json`));
const prototypeLedger = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-execution-ledger-v1.json`));
const dashboardLedger = readJson(path.join(tracesDir, `${phaseSlug}-lumen-dashboard-design-ledger-v1.json`));
const heldPrep = readJson(path.join(tracesDir, `${phaseSlug}-held-sibling-activation-prep-v1.json`));

const queueRows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const safeNow = queueRows.filter((row) => row.approval_bucket === "safe_now").length;
const candidate = queueRows.filter((row) => row.approval_bucket === "candidate").length;
const exact = queueRows.filter((row) => row.approval_bucket === "exact_approval_needed").length;
const blocked = queueRows.filter((row) => row.approval_bucket === "blocked").length;
const immediate = queueRows.filter((row) => row.execution_lane === "immediate_x1_safe").length;
const x2Rows = queueRows.filter((row) => row.execution_lane === "x2_build_task").length;

const closeout = {
  artifact_type: "ghc_v557_v5_x1_lumen_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V5_X1_CLOSED_V5_X2_READY",
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: "v557-gmut-thos-v4-x2",
  next_active_phase: nextPhase,
  next_x2_scope: nextPhase,
  next_x1_lane_after_x2: "v557-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects",
  lumen_response_harvested: true,
  browser_send_status: "browser_send_submitted_response_completed_ready_for_harvest",
  duplicate_send_allowed: false,
  counts: {
    startup_status: startup.overall_status,
    send_status: send.overall_status,
    safe_cadence_status: safeCadence.overall_status,
    ingestion_status: ingestion.overall_status,
    proposal_candidates_indexed: ingestion.proposal_candidates_indexed,
    safe_now_packets: safeNow,
    candidate_packets: candidate,
    exact_approval_packets_queued: exact,
    blocked_packets_queued: blocked,
    immediate_x1_rows: immediate,
    x2_build_rows: x2Rows,
    matrix_cells: Array.isArray(matrix.matrix_cells) ? matrix.matrix_cells.length : 0,
    prototypes: Array.isArray(prototypeLedger.prototypes) ? prototypeLedger.prototypes.length : 0,
    dashboards: Array.isArray(dashboardLedger.dashboards) ? dashboardLedger.dashboards.length : 0,
  },
  held_sibling_activation_state: heldPrep.activation_state,
  closeout_allowed_now: true,
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const readiness = {
  artifact_type: "ghc_v557_v5_x1_v5_x2_readiness_handoff",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V5_X2_READINESS_HANDOFF_READY",
  next_phase: nextPhase,
  build_inputs: [
    "v5 x1 Lumen proposal hash queue",
    "v5 x1 Grand Trinity Matrix",
    "v5 x1 prototype execution ledger",
    "v5 x1 dashboard design ledger",
    "v5 x1 cleanup and source/reflection workbenches",
    "prior three-Lumen-message hash queue from v4 x1",
  ],
  safe_x2_focus: [
    "run safe/candidate proposal reducers without raw text publication",
    "build dashboard and continuity prototypes from sanitized rows",
    "refresh branch/worktree rotation watch without rotating unless needed",
    "preserve exact/blocked gates",
    "prepare v6 Arby/Cicero startup after x2 closeout",
  ],
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = [
  writePair("closeout", closeout),
  writePair("v5-x2-readiness-handoff", readiness),
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
    data.latest_completed_x2_phase = "v557-gmut-thos-v4-x2";
    data.next_expected_scope = nextPhase;
    data.next_x2_scope = nextPhase;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v5_x1_lumen_closeout = {
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
    "## v557 v5 x1 Lumen Closeout",
    "",
    `Status: \`${doc.v557_v5_x1_lumen_closeout?.status || "not_recorded"}\``,
    `Lumen response harvested: \`${doc.v557_v5_x1_lumen_closeout?.lumen_response_harvested === true ? "true" : "false"}\``,
    `Proposal candidates indexed: \`${doc.v557_v5_x1_lumen_closeout?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Next active phase: \`${doc.v557_v5_x1_lumen_closeout?.next_active_phase || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v5_x1_lumen_closeout?.full_goal_complete === true ? "true" : "false"}\``,
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
  if (doc.artifact_type.endsWith("_closeout")) {
    return {
      next_active_phase: doc.next_active_phase,
      lumen_response_harvested: doc.lumen_response_harvested,
      proposal_candidates_indexed: doc.counts.proposal_candidates_indexed,
      full_goal_complete: doc.full_goal_complete,
    };
  }
  return {
    next_phase: doc.next_phase,
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
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function title(type) {
  return type.replace(/^ghc_v557_v5_x1_/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
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

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
