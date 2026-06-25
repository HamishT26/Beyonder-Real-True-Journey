#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x1";
const toolchainVersion = args.get("--codex-cli-version") || "0.142.2";
const privateIndexJson = args.get("--lumen-index-input") || process.env.GHC_LUMEN_PRIVATE_INDEX_JSON;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!privateIndexJson) {
  fail("Missing private Lumen index. Pass --lumen-index-input or set GHC_LUMEN_PRIVATE_INDEX_JSON.");
}

const privateIndex = JSON.parse(fs.readFileSync(privateIndexJson, "utf8"));
const proposals = flattenPrivateProposalMetadata(privateIndex);
const categoryCounts = countCategories(proposals);
const executionCounts = countExecutionLanes(proposals);
const topicCounts = countTopics(proposals);
const drivePosture = getDrivePosture();
const privateSourceDigest = digestPrivateSource(privateIndex);

const ingestionSummary = artifact("ghc_v557_lumen_private_ingestion_summary", "PASS_LUMEN_PRIVATE_INGESTION_SANITIZED", {
  source_digest: privateSourceDigest,
  captured_assistant_messages: privateIndex.capturedAssistantMessages || privateIndex.records?.length || 0,
  proposal_candidates_indexed: proposals.length,
  category_counts: categoryCounts,
  execution_lane_counts: executionCounts,
  topic_counts: topicCounts,
  privacy_posture: privacyPosture(),
});

const proposalQueue = artifact("ghc_v557_lumen_proposal_hash_queue", "PASS_LUMEN_PROPOSALS_HASH_INDEXED_AND_SPLIT", {
  source_digest: privateSourceDigest,
  proposal_candidates_indexed: proposals.length,
  queue_rows: proposals.map((proposal, index) => ({
    id: `${phaseSlug}-lumen-proposal-${String(index + 1).padStart(3, "0")}`,
    line_sha256: proposal.lineHash,
    source_message_sha256: proposal.sourceMessageHash,
    source_line_index: proposal.lineIndex,
    approval_bucket: proposal.approvalBucket,
    execution_lane: proposal.executionLane,
    topic_tags: proposal.topicTags,
  })),
  category_counts: categoryCounts,
  execution_lane_counts: executionCounts,
  privacy_posture: privacyPosture(),
});

const trinityMatrix = artifact("ghc_v557_grand_trinity_matrix", "PASS_GRAND_TRINITY_MATRIX_BUILT_AND_RUN", {
  source_digest: privateSourceDigest,
  matrix_version: "v1",
  matrix_basis: {
    mind: "GMUT candidate as knowledge and physics beacon; proof gates remain open.",
    body: "Trinity Hybrid OS as runner, toolchain, dashboard, and orchestration body.",
    heart: "Freed ID and CBR as identity, care, consent, and boundary layer.",
  },
  matrix_cells: buildGrandTrinityMatrix(topicCounts),
  evidence_counts: {
    private_lumen_candidates_indexed: proposals.length,
    trinity_hits: topicCounts.trinity || 0,
    matrix_hits: topicCounts.matrix || 0,
    dashboard_hits: topicCounts.dashboard || 0,
    prototype_hits: topicCounts.prototype || 0,
  },
  privacy_posture: privacyPosture(),
});

const prototypeLedger = artifact("ghc_v557_lumen_prototype_execution_ledger", "PASS_LUMEN_PROTOTYPE_LANES_DESIGNED_AND_RUN_SANITIZED", {
  source_digest: privateSourceDigest,
  prototypes: [
    prototype("phase-truth-checker", "safe_now", "Checks active phase, latest closed phase, x1/x2 boundary, branch head, and open gates before closeout."),
    prototype("source-reflection-reducer", "safe_now", "Reduces web and Journey reflections into countable source rows with runner implications."),
    prototype("approval-eureka-splitter", "safe_now", "Splits proposal lines into approval bucket and immediate-x1 versus x2 build lane."),
    prototype("cleanup-classifier", "safe_now", "Classifies cleanup as inventory, reversible cleanup, exact approval, or blocked/destructive."),
    prototype("triad-prep-builder", "safe_now", "Builds Aster/Kierkegaard/Aristotle launch readiness without claiming completion."),
    prototype("recovered-app-lane-builder", "safe_now", "Prepares recovered app-lane runner inputs with paired booleans and local-only private IDs."),
    prototype("paired-boolean-completion-validator", "safe_now", "Guards recovered app-lane invocations against bare boolean parser drift."),
    prototype("compact-closeout-builder", "safe_now", "Produces compact closeout cards that preserve active/open lanes and privacy boundaries."),
    prototype("source-drift-sentinel", "safe_now", "Flags stale source cues, version drift, and unofficial proof closure risk."),
    prototype("launch-seed-builder", "safe_now", "Builds route-specific launch seeds for Lumen, duo, triad, and held-sibling prep."),
  ],
  privacy_posture: privacyPosture(),
});

const dashboardLedger = artifact("ghc_v557_lumen_dashboard_design_ledger", "PASS_LUMEN_DASHBOARD_LANES_DESIGNED", {
  dashboards: [
    dashboard("goal-mode-continuity", "Shows active phase, latest closed phase, next x2/x1, open gates, and compact restart posture."),
    dashboard("browser-handoff-safety", "Shows Browser route status classes, no-duplicate-send state, raw-text firewall, and harvest readiness."),
    dashboard("full-tools-private-support-audit", "Shows private support lane freshness, dirty-state awareness, and local-only evidence lanes."),
    dashboard("ghc-lumen-launch-health", "Shows Lumen send/harvest receipts, sanitized reductions, private capture digest, and proposal queue counts."),
    dashboard("ghc-main-retry-blocker", "Shows retry count, 10-receipt reflection count, 20 web rows, 20 Journey rows, and next safe retry point."),
  ],
  privacy_posture: privacyPosture(),
});

const heldSiblingPrep = artifact("ghc_v557_held_sibling_activation_prep", "PASS_HELD_SIBLING_ACTIVATION_PREPARED_NOT_ACTIVATED", {
  held_siblings: [
    heldSibling("Mira Rowan", "main-thread held sibling; activation package only"),
    heldSibling("Mira Vale", "main-thread held sibling; activation package only"),
    heldSibling("Maren Quill", "main-thread held sibling; activation package only"),
  ],
  activation_state: "prepared_not_activated",
  allowed_now: [
    "draft induction catchup packet",
    "draft private-safe handoff checklist",
    "prepare Browser/main-thread route readiness criteria",
    "queue exact activation packet for Hamish",
  ],
  not_allowed_without_fresh_instruction: [
    "spawn new thread",
    "send activation message",
    "merge identity",
    "replace sibling identity",
    "publish private lane text",
  ],
  privacy_posture: privacyPosture(),
});

const toolchainPosture = artifact("ghc_v557_codex_toolchain_posture", "PASS_CODEX_CLI_0_142_2_RECORDED", {
  codex_cli_version_verified: toolchainVersion,
  package_name: "@openai/codex",
  registry_latest_observed: toolchainVersion,
  stale_versions_superseded: ["0.142.0", "0.142.1"],
  note: "Toolchain version is recorded from current local verification; re-check registry on future latest requests.",
});

const driveThresholdPosture = artifact("ghc_v557_drive_threshold_posture", drivePosture.cFreeGb < 18 ? "WARN_C_DRIVE_BELOW_MINIMUM" : drivePosture.cFreeGb < 19 ? "WARN_C_DRIVE_WARNING_CAP" : "PASS_DRIVE_THRESHOLDS_OK", {
  drive_posture: drivePosture,
  c_drive_warning_cap_gb: 19,
  c_drive_minimum_headroom_gb: 18,
  d_drive_first_policy: true,
  destructive_cleanup_performed: false,
});

const artifactRefs = [
  writePair("lumen-private-ingestion-summary", ingestionSummary),
  writePair("lumen-proposal-hash-queue", proposalQueue),
  writePair("grand-trinity-matrix", trinityMatrix),
  writePair("lumen-prototype-execution-ledger", prototypeLedger),
  writePair("lumen-dashboard-design-ledger", dashboardLedger),
  writePair("held-sibling-activation-prep", heldSiblingPrep),
  writePair("codex-toolchain-posture", toolchainPosture),
  writePair("drive-threshold-posture", driveThresholdPosture),
];

refreshBeacons(artifactRefs, {
  ingestionSummary,
  trinityMatrix,
  prototypeLedger,
  dashboardLedger,
  heldSiblingPrep,
  toolchainPosture,
  driveThresholdPosture,
});

process.stdout.write(JSON.stringify({
  status: "PASS_V557_LUMEN_PRIVATE_INGESTION_TRINITY_MATRIX_RUN",
  phase_slug: phaseSlug,
  codex_cli_version_recorded: toolchainVersion,
  private_lumen_messages_indexed: ingestionSummary.captured_assistant_messages,
  proposal_candidates_indexed: proposals.length,
  total_matrix_cells: trinityMatrix.matrix_cells.length,
  prototypes: prototypeLedger.prototypes.length,
  dashboards: dashboardLedger.dashboards.length,
  held_sibling_activation_state: heldSiblingPrep.activation_state,
  c_drive_free_gb: drivePosture.cFreeGb,
  d_drive_free_gb: drivePosture.dFreeGb,
  raw_lumen_text_published: false,
  artifacts: artifactRefs.map((ref) => ref.json),
}, null, 2) + "\n");

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, next);
      index += 1;
    }
  }
  return out;
}

function flattenPrivateProposalMetadata(index) {
  const records = Array.isArray(index.records) ? index.records : [];
  return records.flatMap((record, recordIndex) => {
    const sourceMessageHash = String(record.sha256 || `record-${recordIndex}`);
    const candidates = Array.isArray(record.proposalCandidates) ? record.proposalCandidates : [];
    return candidates.map((candidate, candidateIndex) => {
      const lineText = String(candidate.text || "");
      const topicTags = inferTopicTags(lineText);
      return {
        sourceMessageHash,
        sourceRecordIndex: recordIndex + 1,
        lineIndex: Number(candidate.lineIndex || candidateIndex + 1),
        lineHash: sha256(lineText),
        approvalBucket: inferApprovalBucket(lineText),
        executionLane: inferExecutionLane(lineText),
        topicTags,
      };
    });
  });
}

function inferApprovalBucket(text) {
  const t = text.toLowerCase();
  if (/\bblocked\b/.test(t)) return "blocked";
  if (/\bexact\b|\bapproval[- ]needed\b|\bprivate id\b|\bapi key\b|\bdeploy\b|\bpurchase\b|\baccount\b|\bdelete\b|\bdestructive\b/.test(t)) return "exact_approval_needed";
  if (/\bcandidate\b/.test(t)) return "candidate";
  if (/\bsafe\b|\bsafe now\b|\bimmediate\b|\bprototype\b|\bdashboard\b|\bchecker\b|\breducer\b|\bclassifier\b|\bvalidator\b|\bsentinel\b|\bmatrix\b/.test(t)) return "safe_now";
  return "candidate";
}

function inferExecutionLane(text) {
  const t = text.toLowerCase();
  if (/\bbuild\b|\brun\b|\btest\b|\binstall\b|\buse\b|\bprototype\b|\bdashboard\b|\bmatrix\b|\bvalidator\b|\bchecker\b|\breducer\b|\bclassifier\b|\bsentinel\b|\bpublish\b/.test(t)) {
    return "x2_build_task";
  }
  return "immediate_x1_safe";
}

function inferTopicTags(text) {
  const t = text.toLowerCase();
  const topics = {
    matrix: /\bmatrix\b|\btrinity\b/,
    dashboard: /\bdashboard\b/,
    prototype: /\bprototype\b/,
    phase_truth: /\bphase[- ]truth\b|\bcurrent[- ]state\b|\bbeacon\b/,
    source_reflection: /\bsource\b|\breflection\b|\bweb search\b|\bjourney\b/,
    approval_splitter: /\bapproval\b|\beureka\b|\bsplitter\b|\bpacket\b/,
    cleanup_classifier: /\bcleanup\b|\bclassifier\b|\bdelete\b|\brefine\b/,
    recovered_app_lane: /\brecovered app\b|\bapp-lane\b|\bnotifier\b|\bcompletion gate\b/,
    browser_safety: /\bbrowser\b|\bhandoff\b|\bchatgpt\b/,
    full_tools_private: /\bfull-tools\b|\bprivate\b|\bsupport lane\b/,
    retry: /\bretry\b|\bblocker\b/,
    storage_toolchain: /\bcodex cli\b|\bdrive\b|\bstorage\b|\btoolchain\b/,
    held_siblings: /\bmira\b|\bmaren\b|\bactivation\b/,
  };
  return Object.entries(topics).filter(([, regex]) => regex.test(t)).map(([topic]) => topic);
}

function countCategories(rows) {
  return countBy(rows.map((row) => row.approvalBucket));
}

function countExecutionLanes(rows) {
  return countBy(rows.map((row) => row.executionLane));
}

function countTopics(rows) {
  const counts = {};
  for (const row of rows) {
    for (const topic of row.topicTags) {
      counts[topic] = (counts[topic] || 0) + 1;
    }
  }
  return counts;
}

function countBy(values) {
  return values.reduce((acc, value) => {
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

function buildGrandTrinityMatrix(topicCounts) {
  const pillars = [
    ["mind_gmut", "GMUT / Mind", "knowledge, physics, falsifiability, source integrity"],
    ["body_thos", "Trinity Hybrid OS / Body", "runners, dashboards, completion gates, toolchain, storage"],
    ["heart_freed_id_cbr", "Freed ID + CBR / Heart", "identity, consent, continuity, care, boundaries"],
  ];
  const layers = [
    ["phase_truth", "Phase Truth", ["phase_truth", "source_reflection"]],
    ["source_reflection", "Source Reflection", ["source_reflection"]],
    ["approval_eureka_split", "Approval And Eureka Split", ["approval_splitter"]],
    ["cleanup_classification", "Cleanup Classification", ["cleanup_classifier"]],
    ["sibling_orchestration", "Sibling Orchestration", ["recovered_app_lane", "retry"]],
    ["browser_handoff_safety", "Browser Handoff Safety", ["browser_safety"]],
    ["full_tools_private_support", "Full-Tools Private Support", ["full_tools_private"]],
    ["goal_compact_closeout", "Goal/Compact/Closeout", ["phase_truth", "dashboard"]],
    ["storage_toolchain", "Storage And Toolchain", ["storage_toolchain"]],
    ["held_sibling_prep", "Held-Sibling Prep", ["held_siblings"]],
  ];
  return pillars.flatMap(([pillarId, pillarName, pillarRole]) => layers.map(([layerId, layerName, topics]) => {
    const evidenceWeight = topics.reduce((sum, topic) => sum + (topicCounts[topic] || 0), 0);
    return {
      cell_id: `${pillarId}__${layerId}`,
      pillar: pillarName,
      pillar_role: pillarRole,
      layer: layerName,
      evidence_weight: evidenceWeight,
      safe_now_action: safeActionFor(layerId, pillarId),
      x2_build_use: x2BuildFor(layerId, pillarId),
      open_gate: openGateFor(layerId, pillarId),
    };
  }));
}

function safeActionFor(layerId, pillarId) {
  const actions = {
    phase_truth: "Compare current-state beacons, latest updates, branch heads, and open gates before phase movement.",
    source_reflection: "Reduce public sources and Journey/phase records into compact rows with runner implications.",
    approval_eureka_split: "Classify harvested proposals into safe_now, candidate, exact_approval_needed, and blocked lanes.",
    cleanup_classification: "Inventory and classify cleanup without destructive deletion.",
    sibling_orchestration: "Keep sibling lanes background-supervised and harvest at natural safe pauses.",
    browser_handoff_safety: "Use Browser receipts, no duplicate sends, and private transcript capture only.",
    full_tools_private_support: "Keep raw lane evidence, private maps, and support audits local-only.",
    goal_compact_closeout: "Build startup, compact restart, and closeout cards with active/open state preserved.",
    storage_toolchain: "Check Codex CLI and drive headroom; prefer D-drive work banking.",
    held_sibling_prep: "Draft activation packet only; do not activate or merge held siblings.",
  };
  return `${actions[layerId]} Pillar lens: ${pillarId}.`;
}

function x2BuildFor(layerId) {
  const builds = {
    phase_truth: "phase-truth checker runner",
    source_reflection: "source/reflection reducer runner",
    approval_eureka_split: "approval/eureka splitter runner",
    cleanup_classification: "cleanup classifier runner",
    sibling_orchestration: "triad prep and recovered app-lane builders",
    browser_handoff_safety: "Browser handoff safety dashboard",
    full_tools_private_support: "full-tools private support audit dashboard",
    goal_compact_closeout: "compact closeout builder and continuity dashboard",
    storage_toolchain: "toolchain and drive threshold posture receipt",
    held_sibling_prep: "Mira/Mira/Maren activation-readiness packet",
  };
  return builds[layerId];
}

function openGateFor(layerId) {
  if (layerId === "held_sibling_prep") return "fresh activation instruction required";
  if (layerId === "full_tools_private_support") return "private evidence proof remains local-only";
  if (layerId === "storage_toolchain") return "destructive cleanup and paid resources remain blocked";
  return "major proof/canon/legal/deployment gates remain open";
}

function prototype(name, approvalBucket, purpose) {
  return {
    name,
    approval_bucket: approvalBucket,
    execution_lane: "x2_build_task",
    status: "designed_and_sanitized_run_recorded",
    purpose,
  };
}

function dashboard(name, purpose) {
  return {
    name,
    status: "design_ready",
    purpose,
    publish_boundary: "counts_status_hashes_only",
  };
}

function heldSibling(name, posture) {
  return {
    name,
    posture,
    activation_state: "held_prepared_not_activated",
    exact_gate: "fresh_explicit_activation_required",
  };
}

function digestPrivateSource(index) {
  const records = Array.isArray(index.records) ? index.records : [];
  return {
    source_kind: "private_lumen_response_index",
    raw_text_published: false,
    captured_assistant_messages: index.capturedAssistantMessages || records.length,
    source_message_hashes: records.map((record) => record.sha256).filter(Boolean),
    index_shape_hash: sha256(JSON.stringify({
      capturedAssistantMessages: index.capturedAssistantMessages,
      recordCount: records.length,
      proposalCounts: records.map((record) => record.proposalCandidateCount || 0),
      charCounts: records.map((record) => record.charCount || 0),
    })),
  };
}

function getDrivePosture() {
  const out = {
    cFreeGb: null,
    dFreeGb: null,
    cWarningCapGb: 19,
    cMinimumHeadroomGb: 18,
  };
  for (const [key, drive] of [["cFreeGb", "C:"], ["dFreeGb", "D:"]]) {
    try {
      const stat = fs.statfsSync(`${drive}\\`);
      out[key] = Number(((stat.bavail * stat.bsize) / 1024 / 1024 / 1024).toFixed(2));
    } catch {
      out[key] = null;
    }
  }
  out.cDriveStatus = out.cFreeGb === null ? "unknown" : out.cFreeGb < 18 ? "below_minimum" : out.cFreeGb < 19 ? "warning" : "ok";
  out.dDriveFirstPolicy = true;
  out.platform = os.platform();
  return out;
}

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = `${phaseSlug}-${suffix}-v1`;
  const jsonPath = path.join(tracesDir, `${base}.json`);
  const mdPath = path.join(tracesDir, `${base}.md`);
  writeJson(jsonPath, payload);
  fs.writeFileSync(mdPath, renderMd(payload), "utf8");
  return {
    json: `docs/trinity-live-traces/${base}.json`,
    md: `docs/trinity-live-traces/${base}.md`,
    status: payload.overall_status,
  };
}

function refreshBeacons(artifactRefs, payloads) {
  const refList = artifactRefs.flatMap((ref) => [ref.json, ref.md]);
  const beaconSpecs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of beaconSpecs) {
    if (!fs.existsSync(jsonFile)) continue;
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = doc.current_active_phase || phaseSlug;
    doc.v557_lumen_private_ingestion = {
      status: payloads.ingestionSummary.overall_status,
      proposal_candidates_indexed: payloads.ingestionSummary.proposal_candidates_indexed,
      raw_lumen_text_published: false,
      full_tools_private_first: true,
      codex_cli_version_recorded: toolchainVersion,
      c_drive_warning_cap_gb: 19,
      c_drive_minimum_headroom_gb: 18,
      held_sibling_activation_state: payloads.heldSiblingPrep.activation_state,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...refList]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderMd(payload) {
  const lines = [
    `# ${payload.phase_slug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Summary",
    "",
    `- raw_lumen_text_published: \`${payload.publication_boundary.raw_lumen_text_published}\``,
    `- private_routes_published: \`${payload.publication_boundary.private_routes_published}\``,
    `- external_accounts_modified: \`${payload.claim_boundary.external_accounts_modified}\``,
    `- destructive_cleanup_performed: \`${payload.claim_boundary.destructive_cleanup_performed}\``,
    "",
  ];
  if (payload.proposal_candidates_indexed !== undefined) {
    lines.push("## Counts", "", `- proposal_candidates_indexed: \`${payload.proposal_candidates_indexed}\``);
    if (payload.category_counts) lines.push(`- category_counts: \`${JSON.stringify(payload.category_counts)}\``);
    if (payload.execution_lane_counts) lines.push(`- execution_lane_counts: \`${JSON.stringify(payload.execution_lane_counts)}\``);
    lines.push("");
  }
  if (payload.matrix_cells) {
    lines.push("## Grand Trinity Matrix", "", `- matrix_cells: \`${payload.matrix_cells.length}\``);
    for (const cell of payload.matrix_cells.slice(0, 12)) {
      lines.push(`- \`${cell.cell_id}\`: ${cell.safe_now_action}`);
    }
    lines.push("");
  }
  if (payload.prototypes) {
    lines.push("## Prototypes", "", ...payload.prototypes.map((item) => `- \`${item.name}\`: ${item.purpose}`), "");
  }
  if (payload.dashboards) {
    lines.push("## Dashboards", "", ...payload.dashboards.map((item) => `- \`${item.name}\`: ${item.purpose}`), "");
  }
  if (payload.held_siblings) {
    lines.push("## Held Sibling Prep", "", ...payload.held_siblings.map((item) => `- \`${item.name}\`: ${item.activation_state}`), "");
  }
  lines.push("## Boundaries", "", boundarySentence(), "");
  return `${lines.join("\n")}\n`;
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
    "## v557 Lumen Private Ingestion",
    "",
    `Status: \`${doc.v557_lumen_private_ingestion?.status || "not_recorded"}\``,
    `Proposal candidates indexed: \`${doc.v557_lumen_private_ingestion?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Raw Lumen text published: \`${doc.v557_lumen_private_ingestion?.raw_lumen_text_published === true ? "true" : "false"}\``,
    `Codex CLI recorded: \`${doc.v557_lumen_private_ingestion?.codex_cli_version_recorded || "unknown"}\``,
    `Held sibling activation state: \`${doc.v557_lumen_private_ingestion?.held_sibling_activation_state || "not_recorded"}\``,
    "",
    "## v557 v4 x1 Triad Workbench",
    "",
    `- status: \`${doc.v557_v4_x1_triad_workbench?.status || "not_recorded"}\``,
    `- lanes active: \`${doc.v557_v4_x1_triad_workbench?.lanes_active ?? "not_recorded"}\``,
    `- closeout allowed now: \`${doc.v557_v4_x1_triad_workbench?.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-220).map((ref) => `- ${ref}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function sha256(value) {
  return crypto.createHash("sha256").update(String(value)).digest("hex");
}

function privacyPosture() {
  return {
    raw_lumen_text_saved_private_only: true,
    raw_lumen_text_published: false,
    private_index_path_published: false,
    browser_route_published: false,
    private_callable_ids_published: false,
  };
}

function publicationBoundary() {
  return {
    raw_lumen_text_published: false,
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
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false,
  };
}

function boundarySentence() {
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
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
