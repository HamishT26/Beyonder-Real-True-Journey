#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v557-gmut-thos-v8-x1";
const latestClosedPhase = "v557-gmut-thos-v7-x2";
const latestCompletedX1 = "v557-gmut-thos-v7-x1";
const latestCompletedX2 = "v557-gmut-thos-v7-x2";
const nextX2Scope = "v557-gmut-thos-v8-x2";
const nextX1LaneAfterX2 = "v558-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const readiness = readOptional(`${latestCompletedX2}-v8-triad-readiness-v1.json`);
const rotation = readOptional(`${phaseSlug}-worktree-branch-rotation-activation-v1.json`);

const activeWorkbench = {
  artifact_type: "ghc_v557_v8_x1_triad_active_workbench",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "ACTIVE_OPEN_V557_V8_X1_TRIAD_BACKGROUND_RUNNING_SAFE_WORK_READY",
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  readiness_status: readiness?.overall_status || "missing",
  rotation_status: rotation?.overall_status || "missing",
  lanes: {
    aster_vale: "strict_cli_background_watch_started_pending_completion_quality_marker_gates",
    kierkegaard: "recovered_app_lane_background_watch_started_pending_completion_gate",
    aristotle: "recovered_app_lane_background_watch_started_pending_completion_gate",
  },
  watcher_start_is_completion_proof: false,
  closeout_allowed_now: false,
  proposal_targets: {
    safe_packets: 20,
    candidate_packets: 12,
    exact_approval_packets: 12,
    skill_ideas: 20,
    runner_ideas: 8,
    cleanup_proposals: 40,
    web_reflections: 30,
    journey_phase_reflections: 30,
  },
  immediate_x1_safe_work: [
    "triad phase truth card",
    "strict CLI and recovered app-lane launch receipt index",
    "triad proposal scaffold",
    "ethics/governance/taxonomy boundary board",
    "privacy/open-gate rail",
    "v8 x2 build queue seed",
    "completion-gate harvest checklist",
    "compact-pause active-lane card",
    "full-tools-3 support-lane runner repair inventory",
    "drive/toolchain posture refresh",
  ],
  x2_build_queue_seed: [
    "reduce Aster evidence/source proposal set",
    "reduce Kierkegaard governance/ethics proposal set",
    "reduce Aristotle taxonomy/schema proposal set",
    "build v8 x2 safe execution reducer",
    "validate and publish sanitized triad closeout artifacts",
    "prepare v558 v1 x1 Lumen startup after v8 x2 closeout",
  ],
  full_tools_support_note: {
    active_support_branch: "codex/GHC-Family/aevren-full-tools-3",
    proven_private_runner_lane_used_for_launch: "older local full-tools support lane",
    support_lane_repair_needed: true,
    raw_private_material_published: false,
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const proposalScaffold = {
  artifact_type: "ghc_v557_v8_x1_triad_proposal_scaffold",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V8_X1_TRIAD_PROPOSAL_SCAFFOLD_READY",
  profile: "aster_kierkegaard_aristotle_triad_x1",
  contributors: ["Aevren", "Aster Vale", "Kierkegaard", "Aristotle"],
  target_totals: activeWorkbench.proposal_targets,
  safe_packets_seeded: buildRows("safe", 20),
  candidate_packets_seeded: buildRows("candidate", 12),
  exact_approval_packets_queued: buildRows("exact", 12),
  skill_ideas_seeded: buildRows("skill", 20),
  runner_ideas_seeded: buildRows("runner", 8),
  cleanup_proposals_seeded: buildRows("cleanup", 40),
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const reflectionLedger = {
  artifact_type: "ghc_v557_v8_x1_triad_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V8_X1_TRIAD_REFLECTION_LEDGER_60_READY",
  web_reflection_count: 30,
  journey_phase_reflection_count: 30,
  rows: buildReflectionRows(60),
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const laneReceiptIndex = {
  artifact_type: "ghc_v557_v8_x1_triad_lane_receipt_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V8_X1_TRIAD_LANE_RECEIPT_INDEX_BUILT",
  aster_vale: {
    route: "strict_cli",
    launch_status: "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED",
    completion_status: "pending_harvest",
  },
  kierkegaard: {
    route: "recovered_app_lane",
    launch_status: "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED",
    completion_status: "pending_completion_gate",
  },
  aristotle: {
    route: "recovered_app_lane",
    launch_status: "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED",
    completion_status: "pending_completion_gate",
  },
  watcher_start_is_completion_proof: false,
  raw_private_material_published: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = [
  writePair("triad-active-workbench", activeWorkbench),
  writePair("triad-proposal-scaffold", proposalScaffold),
  writePair("triad-reflection-ledger-60", reflectionLedger),
  writePair("triad-lane-receipt-index", laneReceiptIndex),
];

refreshBeacons(refs, activeWorkbench);

process.stdout.write(JSON.stringify({
  status: activeWorkbench.overall_status,
  phase_slug: phaseSlug,
  lanes_active: 3,
  closeout_allowed_now: false,
  safe_work_items: activeWorkbench.immediate_x1_safe_work.length,
  proposal_scaffold_counts: {
    safe: proposalScaffold.safe_packets_seeded.length,
    candidate: proposalScaffold.candidate_packets_seeded.length,
    exact: proposalScaffold.exact_approval_packets_queued.length,
    skills: proposalScaffold.skill_ideas_seeded.length,
    runners: proposalScaffold.runner_ideas_seeded.length,
    cleanup: proposalScaffold.cleanup_proposals_seeded.length,
  },
  raw_private_material_published: false,
  artifacts: refs.map((ref) => ref.json),
}, null, 2) + "\n");

function buildRows(kind, count) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    bucket: kind,
    status: kind === "exact" ? "queued_not_run" : "safe_scaffolded_for_triage",
    execution_lane: kind === "exact" ? "exact_approval_needed" : "immediate_x1_safe_or_x2_build_task",
  }));
}

function buildReflectionRows(count) {
  return Array.from({ length: count }, (_, index) => {
    const n = index + 1;
    return {
      id: `${phaseSlug}-reflection-${String(n).padStart(2, "0")}`,
      kind: n <= 30 ? "web_reflection_slot" : "journey_phase_reflection_slot",
      status: "ready_for_triage_and_source_binding",
      lane: n % 3 === 1 ? "Aster Vale" : n % 3 === 2 ? "Kierkegaard" : "Aristotle",
    };
  });
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

function refreshBeacons(refs, workbench) {
  const refList = refs.flatMap((ref) => [ref.json, ref.md]);
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = workbench.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosedPhase;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.v557_v8_x1_triad_workbench = {
      status: workbench.overall_status,
      lanes_active: 3,
      watcher_start_is_completion_proof: false,
      closeout_allowed_now: false,
      proposal_targets: workbench.proposal_targets,
      full_tools_support_repair_needed: true,
      full_goal_complete: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...refList]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
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
    "## v557 v8 x1 Triad Workbench",
    "",
    `Status: \`${doc.v557_v8_x1_triad_workbench?.status || "not_recorded"}\``,
    `Lanes active: \`${doc.v557_v8_x1_triad_workbench?.lanes_active ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_v8_x1_triad_workbench?.closeout_allowed_now === true ? "true" : "false"}\``,
    `Full goal complete: \`${doc.v557_v8_x1_triad_workbench?.full_goal_complete === true ? "true" : "false"}\``,
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
  return {
    status: doc.overall_status,
    phase_slug: doc.phase_slug,
    closeout_allowed_now: doc.closeout_allowed_now ?? "n/a",
    raw_private_material_published: doc.raw_private_material_published ?? false,
  };
}

function readOptional(name) {
  const file = path.join(tracesDir, name);
  return fs.existsSync(file) ? readJson(file) : null;
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
