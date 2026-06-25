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
if (!selectedPhases.length) fail("No selected Lumen phases found in last-three sweep.");

const queueRows = [];
const matrixCells = [];
const sourceDigests = [];
for (const selectedPhase of selectedPhases) {
  const queueFile = path.join(tracesDir, `${selectedPhase}-lumen-proposal-hash-queue-v1.json`);
  const matrixFile = path.join(tracesDir, `${selectedPhase}-grand-trinity-matrix-v1.json`);
  if (!fs.existsSync(queueFile)) fail(`Missing sanitized queue for ${selectedPhase}.`);

  const queue = readJson(queueFile);
  sourceDigests.push({ phase_slug: selectedPhase, source_digest: queue.source_digest || null });
  const rows = Array.isArray(queue.queue_rows) ? queue.queue_rows : [];
  rows.forEach((row, index) => {
    queueRows.push({
      id: `${phaseSlug}-last-three-${selectedPhase}-${String(index + 1).padStart(4, "0")}`,
      source_phase_slug: selectedPhase,
      source_row_id: row.id || null,
      line_sha256: row.line_sha256,
      source_message_sha256: row.source_message_sha256,
      source_line_index: row.source_line_index,
      approval_bucket: row.approval_bucket,
      execution_lane: row.execution_lane,
      topic_tags: Array.isArray(row.topic_tags) ? row.topic_tags : [],
    });
  });

  if (fs.existsSync(matrixFile)) {
    const matrix = readJson(matrixFile);
    const cells = Array.isArray(matrix.matrix_cells) ? matrix.matrix_cells : [];
    cells.forEach((cell) => {
      matrixCells.push({
        ...cell,
        source_phase_slug: selectedPhase,
        carried_forward_to: phaseSlug,
      });
    });
  }
}

const categoryCounts = countBy(queueRows.map((row) => row.approval_bucket));
const executionLaneCounts = countBy(queueRows.map((row) => row.execution_lane));
const topicCounts = countTopics(queueRows);
const dedupedMatrixCells = dedupeMatrixCells(matrixCells, topicCounts);

const queueArtifact = {
  artifact_type: "ghc_v557_lumen_last_three_aggregate_proposal_hash_queue",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LAST_THREE_AGGREGATE_QUEUE_BUILT",
  selected_phases: selectedPhases,
  source_digests: sourceDigests,
  proposal_candidates_indexed: queueRows.length,
  queue_rows: queueRows,
  category_counts: categoryCounts,
  execution_lane_counts: executionLaneCounts,
  topic_counts: topicCounts,
  selection_policy: sweep.selection_policy || null,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const matrixArtifact = {
  artifact_type: "ghc_v557_grand_trinity_matrix_last_three_aggregate",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LAST_THREE_GRAND_TRINITY_MATRIX_AGGREGATED",
  matrix_version: "v1-last-three-aggregate",
  matrix_basis: {
    mind: "GMUT candidate remains an open knowledge and physics beacon.",
    body: "Trinity Hybrid OS remains the runner, toolchain, dashboard, and orchestration body.",
    heart: "Freed ID and CBR remain the identity, care, consent, and boundary layer.",
  },
  selected_phases: selectedPhases,
  proposal_candidates_indexed: queueRows.length,
  topic_counts: topicCounts,
  matrix_cells: dedupedMatrixCells,
  source_digest: {
    source_kind: "last_three_sanitized_lumen_queue_aggregate",
    raw_text_published: false,
    selected_phases: selectedPhases,
    source_digests: sourceDigests,
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writeJson(path.join(tracesDir, `${phaseSlug}-lumen-proposal-hash-queue-v1.json`), queueArtifact);
fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-lumen-proposal-hash-queue-v1.md`), renderQueueMd(queueArtifact), "utf8");
writeJson(path.join(tracesDir, `${phaseSlug}-grand-trinity-matrix-v1.json`), matrixArtifact);
fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-grand-trinity-matrix-v1.md`), renderMatrixMd(matrixArtifact), "utf8");
refreshBeacons([
  `docs/trinity-live-traces/${phaseSlug}-lumen-proposal-hash-queue-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-lumen-proposal-hash-queue-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-grand-trinity-matrix-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-grand-trinity-matrix-v1.md`,
], queueArtifact, matrixArtifact);

process.stdout.write(JSON.stringify({
  status: "PASS_LAST_THREE_AGGREGATE_QUEUE_AND_MATRIX_BUILT",
  phase_slug: phaseSlug,
  selected_session_count: selectedPhases.length,
  proposal_candidates_indexed: queueRows.length,
  matrix_cells: dedupedMatrixCells.length,
  raw_private_material_published: false,
}, null, 2) + "\n");

function dedupeMatrixCells(cells, topics) {
  const byCell = new Map();
  for (const cell of cells) {
    const key = cell.cell_id || `${cell.pillar || "pillar"}__${cell.layer || "layer"}`;
    const existing = byCell.get(key);
    if (!existing) {
      byCell.set(key, { ...cell, source_phase_slugs: [cell.source_phase_slug].filter(Boolean) });
      continue;
    }
    existing.evidence_weight = Number(existing.evidence_weight || 0) + Number(cell.evidence_weight || 0);
    existing.source_phase_slugs = unique([...(existing.source_phase_slugs || []), cell.source_phase_slug]);
  }
  if (byCell.size) return [...byCell.values()];

  const pillars = [
    ["mind_gmut", "GMUT / Mind"],
    ["body_thos", "Trinity Hybrid OS / Body"],
    ["heart_freed_id_cbr", "Freed ID + CBR / Heart"],
  ];
  const layers = [
    ["phase_truth", "Phase Truth"],
    ["source_reflection", "Source Reflection"],
    ["approval_eureka_split", "Approval And Eureka Split"],
    ["cleanup_classification", "Cleanup Classification"],
    ["sibling_orchestration", "Sibling Orchestration"],
    ["goal_compact_closeout", "Goal/Compact/Closeout"],
    ["storage_toolchain", "Storage And Toolchain"],
    ["held_sibling_prep", "Held-Sibling Prep"],
  ];
  return pillars.flatMap(([pillarId, pillar]) => layers.map(([layerId, layer]) => ({
    cell_id: `${pillarId}__${layerId}`,
    pillar,
    layer,
    evidence_weight: topics[layerId] || 0,
    safe_now_action: `Carry sanitized ${layer} planning through the ${pillar} lens.`,
    x2_build_use: `${layerId} runner/dashboard prototype`,
    open_gate: "major proof/canon/legal/deployment/private-material gates remain open",
  })));
}

function countTopics(rows) {
  const counts = {};
  for (const row of rows) {
    for (const topic of row.topic_tags || []) counts[topic] = (counts[topic] || 0) + 1;
  }
  return counts;
}

function countBy(values) {
  return values.reduce((acc, value) => {
    acc[value || "unknown"] = (acc[value || "unknown"] || 0) + 1;
    return acc;
  }, {});
}

function refreshBeacons(refs, queueArtifact, matrixArtifact) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.current_active_phase = phaseSlug;
    data.v557_last_three_aggregate_matrix = {
      status: matrixArtifact.overall_status,
      selected_session_count: selectedPhases.length,
      proposal_candidates_indexed: queueArtifact.proposal_candidates_indexed,
      matrix_cells: matrixArtifact.matrix_cells.length,
      raw_private_material_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refs]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderQueueMd(doc) {
  return [
    `# ${doc.phase_slug} Lumen Last-Three Aggregate Proposal Queue`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Selected sessions: \`${doc.selected_phases.join(", ")}\``,
    `Proposal candidates indexed: \`${doc.proposal_candidates_indexed}\``,
    `Category counts: \`${JSON.stringify(doc.category_counts)}\``,
    `Execution lane counts: \`${JSON.stringify(doc.execution_lane_counts)}\``,
    "",
    "No raw Lumen text, private routes, private callable IDs, screenshots, credentials, or local private paths are published.",
    "",
  ].join("\n");
}

function renderMatrixMd(doc) {
  return [
    `# ${doc.phase_slug} Grand Trinity Matrix Last-Three Aggregate`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Matrix cells: \`${doc.matrix_cells.length}\``,
    `Proposal candidates indexed: \`${doc.proposal_candidates_indexed}\``,
    "",
    "## Sample Cells",
    "",
    ...doc.matrix_cells.slice(0, 15).map((cell) => `- \`${cell.cell_id}\`: ${cell.safe_now_action || "sanitized carry-forward"}`),
    "",
    "No proof, canon, legal, deployment, account, paid-resource, API-key, private-material, or identity-merge closure is claimed.",
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
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 Last-Three Aggregate Matrix",
    "",
    `Status: \`${doc.v557_last_three_aggregate_matrix?.status || "not_recorded"}\``,
    `Selected sessions: \`${doc.v557_last_three_aggregate_matrix?.selected_session_count ?? "not_recorded"}\``,
    `Proposal candidates indexed: \`${doc.v557_last_three_aggregate_matrix?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Matrix cells: \`${doc.v557_last_three_aggregate_matrix?.matrix_cells ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((ref) => `- ${ref}`),
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    raw_lumen_text_published: false,
    raw_private_material_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
    credentials_published: false,
  };
}

function claimBoundary() {
  return {
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
    destructive_cleanup_performed: false,
  };
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

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(2);
}
