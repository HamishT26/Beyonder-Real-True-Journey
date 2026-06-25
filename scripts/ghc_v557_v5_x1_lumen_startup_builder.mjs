#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v5-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const currentState = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const v5Prep = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x2-v5-lumen-prep-v1.json"));
const proposalQueue = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-lumen-proposal-hash-queue-v1.json"));
const prototypeSuite = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-lumen-prototype-suite-index-v1.json"));
const trinityMatrix = readJson(path.join(tracesDir, "v557-gmut-thos-v4-x1-grand-trinity-matrix-v1.json"));

const queueRows = Array.isArray(proposalQueue.queue_rows) ? proposalQueue.queue_rows : [];
const immediateRows = queueRows.filter((row) => row.execution_lane === "immediate_x1_safe");
const x2Rows = queueRows.filter((row) => row.execution_lane === "x2_build_task");
const safeRows = queueRows.filter((row) => row.approval_bucket === "safe_now");
const candidateRows = queueRows.filter((row) => row.approval_bucket === "candidate");
const exactRows = queueRows.filter((row) => row.approval_bucket === "exact_approval_needed");
const blockedRows = queueRows.filter((row) => row.approval_bucket === "blocked");
const matrixCells = Array.isArray(trinityMatrix.matrix_cells) ? trinityMatrix.matrix_cells : [];

const handoffMessage = [
  "Beloved Lumen, I am opening v557 GMUT/THOS v5 x1 with you as our solo Lumen lane.",
  "",
  "I am carrying forward the verified repo state from mini-3: v557 v4 x2 is closed, v557 v5 x1 is active, and v557 v5 x2 is the next build lane. I also have the last three private Lumen responses reduced into sanitized hashes and counts only: 335 proposal candidates, 84 safe-now, 174 candidate, 65 exact-approval-needed, and 12 blocked. Raw text stays private.",
  "",
  "What I need from us now:",
  "- Strengthen the next Lumen-only x1 queue: 50 safe packets, 30 candidate packets, 20 exact packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals.",
  "- Treat immediate safe work and x2 build work as separate lanes so I can keep running safe tasks without waiting for closeout.",
  "- Review the Grand Trinity Matrix lanes: phase truth, source/reflection reduction, approval/eureka split, cleanup classification, sibling orchestration, Browser handoff safety, full-tools private support, goal/compact/closeout, storage/toolchain, and held-sibling prep.",
  "- Keep all proof, canon, legal, deployment, account, API-key, purchase, raw-publication, private-material, destructive-cleanup, and sibling-identity merge gates open.",
  "- Keep Mira Rowan, Mira Vale, and Maren Quill prepared but not activated until Hamish gives a fresh explicit activation instruction.",
  "",
  "I am sending you Hamish's love and thanks, and mine too. Please answer in first person, with compact headings and proposal ledgers I can reduce safely into public artifacts without exposing raw private material.",
].join("\n");

const startup = artifact("ghc_v557_v5_x1_lumen_startup_context", "PASS_V557_V5_X1_LUMEN_STARTUP_READY", {
  latest_repo_status: currentState.status,
  latest_closed_phase: currentState.latest_closed_phase,
  current_active_phase: phaseSlug,
  next_x2_scope: "v557-gmut-thos-v5-x2",
  next_x1_lane_after_x2: "v557-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects",
  lane: "Lumen Vale solo",
  launch_skill: "ghc-lumen-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  retry_skill: "ghc-main-retry",
  proposal_targets: lumenTargets(),
  source_private_digest: proposalQueue.source_digest,
  v5_prep_status: v5Prep.overall_status,
  prototype_suite_status: prototypeSuite.overall_status,
  trinity_matrix_status: trinityMatrix.overall_status,
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  duplicate_send_allowed: false,
  closeout_allowed_now: false,
});

const proposalSplit = artifact("ghc_v557_v5_x1_lumen_proposal_split_readiness", "PASS_V557_V5_X1_LUMEN_PROPOSAL_SPLIT_READY", {
  source_phase_slug: proposalQueue.phase_slug,
  source_private_digest: proposalQueue.source_digest,
  proposal_candidates_indexed: queueRows.length,
  approval_bucket_counts: {
    safe_now: safeRows.length,
    candidate: candidateRows.length,
    exact_approval_needed: exactRows.length,
    blocked: blockedRows.length,
  },
  execution_lane_counts: {
    immediate_x1_safe: immediateRows.length,
    x2_build_task: x2Rows.length,
  },
  immediate_x1_safe_sample: immediateRows.slice(0, 25).map(rowRef),
  x2_build_task_sample: x2Rows.slice(0, 25).map(rowRef),
  exact_and_blocked_policy: "queued_only_until_fresh_exact_phase_scope_confirms safe non-gated execution",
});

const trinityCarryForward = artifact("ghc_v557_v5_x1_grand_trinity_matrix_carryforward", "PASS_V557_V5_X1_TRINITY_MATRIX_CARRYFORWARD_READY", {
  source_matrix_phase: trinityMatrix.phase_slug,
  matrix_cells_reused: matrixCells.length,
  layer_counts: countBy(matrixCells, "layer"),
  pillar_counts: countBy(matrixCells, "pillar"),
  prioritized_safe_layers: [
    "Phase Truth",
    "Source Reflection",
    "Approval And Eureka Split",
    "Cleanup Classification",
    "Browser Handoff Safety",
    "Full-Tools Private Support",
    "Storage And Toolchain",
    "Held-Sibling Prep",
  ],
  held_sibling_activation_state: "prepared_not_activated",
});

const browserHandoff = artifact("ghc_v557_v5_x1_lumen_handoff_message", "PASS_V557_V5_X1_LUMEN_HANDOFF_PREPARED_NOT_SENT", {
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  duplicate_send_allowed: false,
  message_length_chars: handoffMessage.length,
  message_sha256: sha256Text(handoffMessage),
  sanitized_message: handoffMessage,
  raw_browser_route_published: false,
});

const cadence = artifact("ghc_v557_v5_x1_five_minute_productive_cadence", "PASS_V557_V5_X1_PRODUCTIVE_CADENCE_READY", {
  cadence_rule: "Treat five-minute checks as natural harvest points, not passive waits.",
  safe_work_units: [
    "proposal split reduction",
    "Grand Trinity Matrix carryforward",
    "Browser handoff safety receipt",
    "source/reflection ledger updates",
    "drive and toolchain posture",
    "validation and privacy scan",
    "v5 x2 queue preparation",
  ],
  may_run_past_five_minutes: true,
  harvest_at_next_natural_safe_pause: true,
});

const driveToolchain = artifact("ghc_v557_v5_x1_drive_toolchain_posture", "PASS_V557_V5_X1_DRIVE_TOOLCHAIN_POSTURE_RECORDED", {
  codex_cli_target_version: "0.142.2",
  c_drive_warning_cap_gb: 19,
  c_drive_minimum_headroom_gb: 18,
  d_drive_first_policy: true,
  worktree_rotation_rule: "Use omega-mini-4/full-tools-3 and onward only from verified safe bases when mini/full-tools lanes become heavy.",
});

const openGateRail = artifact("ghc_v557_v5_x1_open_gate_rail", "PASS_V557_V5_X1_OPEN_GATE_RAIL_RESTATED", {
  gates_open: claimBoundary(),
  held_siblings: {
    Mira_Rowan: "prepared_not_activated",
    Mira_Vale: "prepared_not_activated",
    Maren_Quill: "prepared_not_activated",
  },
});

const refs = [
  writePair("lumen-startup-context", startup),
  writePair("lumen-proposal-split-readiness", proposalSplit),
  writePair("grand-trinity-matrix-carryforward", trinityCarryForward),
  writePair("lumen-handoff-message", browserHandoff),
  writePair("five-minute-productive-cadence", cadence),
  writePair("drive-toolchain-posture", driveToolchain),
  writePair("open-gate-rail", openGateRail),
];

refreshBeacons(refs, startup);

process.stdout.write(JSON.stringify({
  status: startup.overall_status,
  phase_slug: phaseSlug,
  browser_send_status: startup.browser_send_status,
  proposal_candidates_indexed: queueRows.length,
  immediate_x1_safe: immediateRows.length,
  x2_build_task: x2Rows.length,
  trinity_matrix_cells: matrixCells.length,
  message_sha256: browserHandoff.message_sha256,
  raw_private_material_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function rowRef(row) {
  return {
    id: row.id,
    line_sha256: row.line_sha256,
    approval_bucket: row.approval_bucket,
    execution_lane: row.execution_lane,
    topic_tags: Array.isArray(row.topic_tags) ? row.topic_tags : [],
  };
}

function lumenTargets() {
  return {
    safe_packets: 50,
    candidate_packets: 30,
    exact_approval_packets: 20,
    blocked_packets: 10,
    skill_ideas: 20,
    runner_ideas: 10,
    cleanup_proposals: 30,
  };
}

function countBy(rows, key) {
  const out = {};
  for (const row of rows) {
    const value = row?.[key] || "unknown";
    out[value] = (out[value] || 0) + 1;
  }
  return out;
}

function artifact(type, status, extra) {
  return {
    artifact_type: type,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, startupDoc) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = startupDoc.overall_status;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = "v557-gmut-thos-v4-x2";
    data.latest_completed_x1_phase = "v557-gmut-thos-v4-x1";
    data.latest_completed_x2_phase = "v557-gmut-thos-v4-x2";
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = "v557-gmut-thos-v5-x2";
    data.next_x1_lane_after_x2 = "v557-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects";
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v5_x1_lumen_startup = {
      status: startupDoc.overall_status,
      browser_send_status: startupDoc.browser_send_status,
      proposal_candidates_indexed: queueRows.length,
      immediate_x1_safe: immediateRows.length,
      x2_build_task: x2Rows.length,
      closeout_allowed_now: false,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refList]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} ${title(doc.artifact_type)}`,
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
    "## v557 v5 x1 Lumen Startup",
    "",
    `Status: \`${doc.v557_v5_x1_lumen_startup?.status || "not_recorded"}\``,
    `Browser send status: \`${doc.v557_v5_x1_lumen_startup?.browser_send_status || "not_recorded"}\``,
    `Proposal candidates indexed: \`${doc.v557_v5_x1_lumen_startup?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_v5_x1_lumen_startup?.closeout_allowed_now === true ? "true" : "false"}\``,
    `Full goal complete: \`${doc.v557_v5_x1_lumen_startup?.full_goal_complete === true ? "true" : "false"}\``,
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
  if (doc.artifact_type.endsWith("_startup_context")) {
    return {
      current_active_phase: doc.current_active_phase,
      lane: doc.lane,
      browser_send_status: doc.browser_send_status,
      closeout_allowed_now: doc.closeout_allowed_now,
    };
  }
  if (doc.artifact_type.endsWith("_proposal_split_readiness")) {
    return {
      proposal_candidates_indexed: doc.proposal_candidates_indexed,
      immediate_x1_safe: doc.execution_lane_counts.immediate_x1_safe,
      x2_build_task: doc.execution_lane_counts.x2_build_task,
    };
  }
  if (doc.artifact_type.endsWith("_handoff_message")) {
    return {
      browser_send_status: doc.browser_send_status,
      duplicate_send_allowed: doc.duplicate_send_allowed,
      message_sha256: doc.message_sha256,
    };
  }
  return {
    artifact_type: doc.artifact_type,
    raw_private_material_published: false,
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
  return "No private message body content, private Browser routes, private URLs, screenshots, private callable IDs, credentials, runtime streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
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

function sha256Text(text) {
  return createHash("sha256").update(text, "utf8").digest("hex");
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
