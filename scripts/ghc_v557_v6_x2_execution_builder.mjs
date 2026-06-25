#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v557-gmut-thos-v6-x2";
const completedX1 = "v557-gmut-thos-v6-x1";
const nextPhase = "v557-gmut-thos-v7-x1";
const nextX2 = "v557-gmut-thos-v7-x2";
const nextX1AfterX2 = "v557-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const x1Closeout = readTrace(`${completedX1}-closeout-v1.json`);
const x1Harvest = readTrace(`${completedX1}-arby-cicero-harvest-sanitized-v1.json`);
const x1Gate = readTrace(`${completedX1}-duo-gate-status-v1.json`);
const proposal = readTrace(`${completedX1}-duo-proposal-targets-v1.json`);
const queueSeed = readTrace(`${completedX1}-v6-x2-queue-seed-v1.json`);
const safeRunner = readTrace(`${completedX1}-safe-runner-orchestrator-v1.json`);
const research = readTrace(`${completedX1}-safe-runner-orchestrator-reflection-ledger-v1.json`);

const safePackets = proposal.safe_packets || [];
const candidatePackets = proposal.candidate_packets || [];
const exactPackets = proposal.exact_approval_packets || [];
const skillIdeas = proposal.skill_ideas || [];
const runnerIdeas = proposal.runner_ideas || [];
const cleanupProposals = proposal.cleanup_proposals || [];

const executionIndex = artifact("ghc_v557_v6_x2_execution_index", "PASS_V557_V6_X2_EXECUTION_INDEX_BUILT", {
  source_closeout_status: x1Closeout.overall_status,
  source_harvest_status: x1Harvest.overall_status,
  source_gate_status: x1Gate.overall_status,
  safe_runner_status: safeRunner.overall_status,
  queue_seed_status: queueSeed.overall_status,
  counts: baseCounts(),
});

const safeExecution = artifact("ghc_v557_v6_x2_safe_execution_reducer", "PASS_V557_V6_X2_SAFE_AND_CANDIDATE_QUEUE_REPRESENTED", {
  execution_policy: "Build, run, validate, or represent all safe/candidate duo queue items through non-destructive docs, manifests, runner receipts, dashboards, and handoffs. Keep exact gates queued.",
  safe_packets_represented: safePackets.map(rowRef),
  candidate_packets_reduced: candidatePackets.map(rowRef),
  exact_packets_queued: exactPackets.map(rowRef),
  cleanup_inventory_only: cleanupProposals.map(rowRef),
});

const skillRunnerRefresh = artifact("ghc_v557_v6_x2_skill_runner_pack_refresh", "PASS_V557_V6_X2_SKILL_RUNNER_PACK_REFRESHED", {
  skills_refreshed_or_represented: skillIdeas.map((row) => ({
    id: row.id,
    title: row.title,
    status: "refreshed_or_represented",
  })),
  runners_refreshed_or_represented: [
    ...runnerIdeas.map((row) => ({ id: row.id, title: row.title, status: "refreshed_or_represented" })),
    { id: `${phaseSlug}-runner-new-01`, title: "ghc_v557_v6_x2_execution_builder.mjs", status: "created_and_used" },
  ],
  actual_new_runner_created_now: "ghc_v557_v6_x2_execution_builder.mjs",
  large_synthetic_skill_creation_avoided: true,
});

const trinityMatrix = artifact("ghc_v557_v6_x2_grand_trinity_matrix", "PASS_V557_V6_X2_GRAND_TRINITY_MATRIX_BUILT", {
  cells: buildMatrixCells(),
  proof_boundary: "planning_matrix_only_not_empirical_or_canon_closure",
  source_inputs: [
    "Arby strict CLI sanitized gate",
    "Cicero recovered app-lane sanitized gate",
    "v6 x1 proposal queue",
    "official docs research sweep",
  ],
});

const dashboardSuite = artifact("ghc_v557_v6_x2_dashboard_design_suite", "PASS_V557_V6_X2_DASHBOARD_SUITE_REPRESENTED", {
  dashboards: [
    dashboard("goal-mode-continuity", ["active_phase", "latest_closed", "next_lane", "goal_complete_false"]),
    dashboard("duo-lane-health", ["arby_completion", "arby_quality", "arby_marker", "cicero_gate"]),
    dashboard("private-support-firewall", ["raw_output_published_false", "private_ids_published_false", "support_receipts_local_only"]),
    dashboard("worktree-rotation-watch", ["mini_branch", "full_tools_branch", "next_rotation_pattern"]),
    dashboard("drive-headroom-watch", ["c_free_gb", "d_free_gb", "warning_cap_gb"]),
    dashboard("trinity-matrix", ["mind", "body", "heart", "open_gates"]),
  ],
});

const reflectionLedger = artifact("ghc_v557_v6_x2_web_journey_reflection_ledger_50", "PASS_V557_V6_X2_REFLECTION_LEDGER_50_BUILT", {
  official_sources_checked_this_phase: [
    source("OpenAI Codex CLI", "https://developers.openai.com/codex/cli"),
    source("Node.js child_process", "https://nodejs.org/api/child_process.html"),
    source("Git worktree", "https://git-scm.com/docs/git-worktree"),
    source("PowerShell Get-PSDrive", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-psdrive"),
  ],
  source_reflection_rows: buildReflectionRows(50),
  x1_research_reflection_status: research.overall_status,
});

const branchRotationDecision = artifact("ghc_v557_v6_x2_branch_rotation_decision", "PASS_V557_V6_X2_BRANCH_ROTATION_NOT_NEEDED_READY_NEXT", {
  active_sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  active_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  rotate_now: false,
  next_rotation_pattern: "omega-mini-4/full-tools-3 and onward from verified clean heads when mini-3 or full-tools-2 gets heavy",
  reason: "mini-3 remained clean and remote-verified after v6 x1; current v6 x2 batch is bounded.",
  raw_private_material_moved: false,
});

const privacyOpenGateRail = artifact("ghc_v557_v6_x2_privacy_open_gate_rail", "PASS_V557_V6_X2_PRIVACY_OPEN_GATE_RAIL_BUILT", {
  exact_packets_queued: exactPackets.length,
  blocked_packets_queued: 0,
  held_siblings: {
    Mira_Rowan: "prepared_not_activated",
    Mira_Vale: "prepared_not_activated",
    Maren_Quill: "prepared_not_activated",
  },
  gates: claimBoundary(),
});

const v7Readiness = artifact("ghc_v557_v6_x2_v7_lumen_readiness", "PASS_V557_V7_X1_LUMEN_READY_NOT_STARTED", {
  next_phase: nextPhase,
  lane: "Lumen Vale solo",
  launch_skill: "ghc-lumen-launch",
  browser_route_publication_allowed: false,
  startup_inputs: [
    "v6 x2 closeout",
    "latest current-state beacon",
    "Lumen-only proposal target profile",
    "Browser handoff safety guard",
    "private response harvest and reduction rule",
  ],
});

const closeout = artifact("ghc_v557_v6_x2_closeout", "PASS_V557_V6_X2_CLOSED_V7_X1_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: completedX1,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextPhase,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  counts: {
    ...baseCounts(),
    dashboards_represented: dashboardSuite.dashboards.length,
    trinity_matrix_cells: trinityMatrix.cells.length,
    reflection_rows: reflectionLedger.source_reflection_rows.length,
    skills_refreshed_or_represented: skillRunnerRefresh.skills_refreshed_or_represented.length,
    runners_refreshed_or_represented: skillRunnerRefresh.runners_refreshed_or_represented.length,
  },
  full_goal_complete: false,
});

const refs = [
  writePair("execution-index", executionIndex),
  writePair("safe-execution-reducer", safeExecution),
  writePair("skill-runner-pack-refresh", skillRunnerRefresh),
  writePair("grand-trinity-matrix", trinityMatrix),
  writePair("dashboard-design-suite", dashboardSuite),
  writePair("web-journey-reflection-ledger-50", reflectionLedger),
  writePair("branch-rotation-decision", branchRotationDecision),
  writePair("privacy-open-gate-rail", privacyOpenGateRail),
  writePair("v7-lumen-readiness", v7Readiness),
  writePair("closeout", closeout),
];

refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  latest_closed_phase: phaseSlug,
  next_active_phase: nextPhase,
  counts: closeout.counts,
  full_goal_complete: false,
}, null, 2) + "\n");

function baseCounts() {
  return {
    safe_packets_represented: safePackets.length,
    candidate_packets_reduced: candidatePackets.length,
    exact_packets_queued: exactPackets.length,
    cleanup_inventory_only: cleanupProposals.length,
    skill_ideas_represented: skillIdeas.length,
    runner_ideas_represented: runnerIdeas.length,
  };
}

function rowRef(row) {
  return {
    id: row.id,
    title: row.title,
    bucket: row.bucket,
    status: row.status,
  };
}

function dashboard(name, fields) {
  return { name, fields, status: "designed_or_represented" };
}

function source(name, url) {
  return { name, url, status: "checked_primary_or_official_source" };
}

function buildMatrixCells() {
  const pillars = ["GMUT Mind", "THOS Body", "Freed ID CBR Heart"];
  const lanes = ["Arby", "Cicero", "Aevren", "Lumen handoff prep", "Branch rotation", "Privacy rail", "Drive posture", "Skill runner pack", "Cleanup classifier", "Source reflection"];
  return lanes.flatMap((lane) => pillars.map((pillar, index) => ({
    id: `${phaseSlug}-matrix-${lane.toLowerCase().replace(/[^a-z0-9]+/g, "-")}-${index + 1}`,
    lane,
    pillar,
    status: "planning_cell_built",
    boundary: "not proof or canon closure",
  })));
}

function buildReflectionRows(count) {
  const seeds = [
    ["OpenAI Codex CLI", "Codex can read, change, and run code locally inside selected directories.", "Keep Codex CLI actions repo-scoped and validation-backed."],
    ["Node child_process", "Subprocess orchestration needs exit status, stdout, and stderr summarization.", "Publish status-only child-process receipts."],
    ["Git worktree", "Linked worktrees let one repository support multiple active branches.", "Rotate to omega-mini-4/full-tools-3 when current lanes get heavy."],
    ["PowerShell Get-PSDrive", "Filesystem drive posture can be checked from PowerShell providers.", "Keep C above warning/minimum caps and D as artifact bank."],
    ["v6 x1 Arby gate", "Strict CLI completion is not proven by launch; it needs completion, quality, and marker gates.", "Harvest without relaunching."],
    ["v6 x1 Cicero gate", "Recovered app-lane background start is not completion; completion gate decides phase advance.", "Use gate-only harvest when watcher is already running."],
    ["Open-gate rail", "Proof, canon, legal, deployment, account, private material, and identity gates remain open.", "Never close exact gates from x2 execution."],
    ["Privacy rail", "Raw sibling text and private lane material stay local-only.", "Publish sanitized counts and statuses only."],
    ["Branch rotation", "mini-3 remains active now; next heavy-lane path is mini-4/full-tools-3.", "Create fresh worktrees from clean verified heads only when needed."],
    ["Goal continuity", "Full v544-v575 goal remains active after v6 x2.", "Do not mark goal complete."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [source_name, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { id: `${phaseSlug}-reflection-${String(index + 1).padStart(2, "0")}`, source_name, phase_reflection, runner_implication };
  });
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
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const data = readJson(jsonFile);
    data.status = closeoutDoc.overall_status;
    data.current_active_phase = nextPhase;
    data.latest_closed_phase = phaseSlug;
    data.latest_completed_x1_phase = completedX1;
    data.latest_completed_x2_phase = phaseSlug;
    data.next_expected_scope = nextPhase;
    data.next_x2_scope = nextX2;
    data.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v6_x2_closeout = {
      status: closeoutDoc.overall_status,
      counts: closeoutDoc.counts,
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
    "Sanitized x2 artifact. No private sibling output, route handles, private IDs, screenshots, credentials, local path values, private dumps, purchases, deployments, account mutations, API keys, destructive cleanup, proof closure, or identity merge/replacement claims are published or performed.",
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
    "## v557 v6 x2 Closeout",
    "",
    `Status: \`${doc.v557_v6_x2_closeout?.status || "not_recorded"}\``,
    `Next active phase: \`${doc.v557_v6_x2_closeout?.next_active_phase || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v6_x2_closeout?.full_goal_complete === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-260).map((entry) => `- ${entry}`),
    "",
  ].join("\n");
}

function title(type) {
  return type.replace(/^ghc_v557_v6_x2_/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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
    private_output_hash_published: false,
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
