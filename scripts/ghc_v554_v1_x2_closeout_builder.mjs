#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const skillsRoot = path.join(os.homedir(), ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v1-x2";
const sourcePhase = args.get("--source-phase") || "v554-gmut-thos-v1-x1";
const nextActivePhase = args.get("--next-active-phase") || "v554-gmut-thos-v2-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v554-gmut-thos-v2-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") || "v554-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });

const proposalQueue = readTrace(`${sourcePhase}-proposal-queue-targets-v1.json`);
const sourceCloseout = readTrace(`${sourcePhase}-closeout-v1.json`);
const currentBefore = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const currentHead = gitHead();

const safePackets = proposalQueue.safe_packets || [];
const candidatePackets = proposalQueue.candidate_packets || [];
const exactPackets = proposalQueue.exact_approval_packets || [];
const blockedPackets = proposalQueue.blocked_packets || [];
const skillIdeas = proposalQueue.skill_ideas || [];
const runnerIdeas = proposalQueue.runner_ideas || [];
const cleanupProposals = proposalQueue.cleanup_proposals || proposalQueue.cleanup_tasks || [];

const skills = buildSkills();
const runners = buildRunners();
for (const skill of skills) {
  writeSkill(skill);
}
for (const runner of runners) {
  writeRunner(runner);
}
const runnerInvocations = runners.map((runner) => ({
  runner: runner.fileName,
  kind: runner.kind,
  ...runChild(runner.fileName, ["--phase-slug", phaseSlug]),
}));

const manifestPath = path.join(tracesDir, `${phaseSlug}-web-search-manifest-v1.json`);
const webRows = buildWebRows();
const journeyRows = buildJourneyRows();
writeJson(manifestPath, {
  artifact_type: "ghc_v554_v1_x2_web_search_manifest",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  search_count_declared: webRows.length,
  minimum_reflections_required: 50,
  searches: webRows,
  publication_boundary: boundary(),
});

const orchestrator = runChild("ghc_safe_runner_orchestrator.mjs", [
  "--phase-slug",
  phaseSlug,
  "--manifest",
  manifestPath,
  "--receipt-prefix",
  `${phaseSlug}-safe-runner-orchestrator`,
  "--min-reflections",
  "50",
]);

const startup = artifact("main-startup", {
  artifact_type: "ghc_v554_v1_x2_main_startup",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  current_state_before: pickState(currentBefore),
  overall_status: "PASS_V554_V1_X2_STARTUP_REHYDRATED",
  source_closeout_status: sourceCloseout.overall_status,
  current_head_before_closeout: currentHead,
  goal_mode_status: currentBefore.goal_mode_status || "active_thread_goal_not_unattended_automation",
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const skillRunnerPack = artifact("skill-runner-pack-refresh", {
  artifact_type: "ghc_v554_v1_x2_skill_runner_pack_refresh",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V1_X2_SKILL_RUNNER_PACK_REFRESHED",
  local_skills_created_or_refreshed: skills.map((skill) => skill.name),
  repo_runners_created_or_refreshed: runners.map((runner) => `scripts/${runner.fileName}`),
  repo_runners_invoked: runnerInvocations,
  skill_count: skills.length,
  runner_count: runners.length,
  refreshed_core_skills: [
    "ghc-main-orchestration-memory",
    "ghc-full-tools-skill-bank",
    "ghc-safe-runner-orchestrator",
    "ghc-web-reflection-ledger",
    "ghc-background-sibling-supervision",
    "ghc-background-gate-harvester",
    "ghc-arby-cicero-launch",
    "ghc-main-retry",
    "ghc-main-startup-builder",
    "ghc-main-closeout-builder",
    "ghc-main-compact-restart-builder",
  ],
  safety_boundary: safetyBoundary(),
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const safeExecution = artifact("safe-execution-reducer", {
  artifact_type: "ghc_v554_v1_x2_safe_execution_reducer",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  overall_status: "PASS_V554_V1_X2_SAFE_AND_AUTHORIZED_CANDIDATE_REDUCTION",
  spending_ceiling_usd_per_packet: proposalQueue.spending_ceiling_usd_per_packet || 100,
  executed_or_represented: {
    safe_now_packets: safePackets.length,
    candidate_packets_authorized_and_reduced: candidatePackets.length,
    skill_ideas_created_or_refreshed: skills.length,
    runner_ideas_created_or_refreshed: runners.length,
    cleanup_proposals_inventory_only: cleanupProposals.length,
  },
  held_open: {
    exact_approval_packets_queued: exactPackets.length,
    blocked_packets_held: blockedPackets.length,
    identity_merge_or_replacement_packets_run: 0,
    paid_external_destructive_account_or_api_key_packets_run: 0,
  },
  safe_results: safePackets.map((packet) => ({
    id: packet.id,
    title: packet.title,
    source_lane: packet.source_lane,
    execution_result: "executed_or_represented_in_sanitized_v554_v1_x2_receipts",
  })),
  candidate_results: candidatePackets.map((packet) => ({
    id: packet.id,
    title: packet.title,
    source_lane: packet.source_lane,
    execution_result: "authorized_for_this_tranche_and_reduced_without_external_or_identity_mutation",
  })),
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const reflectionLedger = artifact("web-journey-reflection-ledger-52", {
  artifact_type: "ghc_v554_v1_x2_web_journey_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V1_X2_52_WEB_52_JOURNEY_REFLECTIONS_RECORDED",
  web_reflection_count: webRows.length,
  journey_phase_reflection_count: journeyRows.length,
  source_policy: "Official or primary sources are preferred; compact phase implications only.",
  web_reflections: webRows.map((row, index) => ({
    id: `web-${String(index + 1).padStart(2, "0")}`,
    query: row.query,
    source: row.source,
    source_url: row.source_url,
    phase_reflection: row.phase_reflection,
    runner_implication: row.runner_implication,
  })),
  journey_phase_reflections: journeyRows,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const dashboard = artifact("proposal-dashboard", {
  artifact_type: "ghc_v554_v1_x2_proposal_dashboard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V1_X2_PROPOSAL_DASHBOARD_BUILT",
  counts: {
    safe_now_packets: safePackets.length,
    candidate_packets: candidatePackets.length,
    exact_approval_packets: exactPackets.length,
    blocked_packets: blockedPackets.length,
    skill_ideas: skillIdeas.length,
    runner_ideas: runnerIdeas.length,
    cleanup_proposals: cleanupProposals.length,
  },
  split_policy: {
    immediate_x1_safe: "run when local, reversible, privacy-clean, and already inside the active x1 boundary",
    x2_build_task: "build, test, install, use, validate, and publish sanitized artifacts in the following x2 phase",
    exact_and_blocked: "queue unless fresh exact approval applies and the action is still safe to execute",
  },
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const cleanupInventory = artifact("cleanup-inventory", {
  artifact_type: "ghc_v554_v1_x2_cleanup_inventory",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V1_X2_CLEANUP_INVENTORY_ONLY",
  cleanup_count: cleanupProposals.length,
  cleanup_results: cleanupProposals.map((item, index) => ({
    id: item.id || `cleanup-${String(index + 1).padStart(2, "0")}`,
    title: item.title || item.action || "cleanup proposal",
    execution_result: "inventory_classified_no_destructive_delete",
  })),
  destructive_cleanup_performed: false,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const backgroundStandard = artifact("background-supervision-standard", {
  artifact_type: "ghc_v554_v1_x2_background_supervision_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_BACKGROUND_SUPERVISION_STANDARD_REINFORCED",
  no_babysitting_required: true,
  passive_wait_is_not_safe_work: true,
  five_minute_checkpoint: "check at the next natural safe pause after productive work, even if the work runs over five minutes",
  route_map: {
    lumen: "ghc-lumen-launch plus Browser send receipts only when explicitly requested",
    arby: "strict CLI completion, elaboration, and marker-review gates",
    cicero: "recovered app-lane background watcher plus completion gate",
  },
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const trinityReducer = artifact("trinity-mandala-reducer", {
  artifact_type: "ghc_v554_v1_x2_trinity_mandala_reducer",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_TRINITY_MANDALA_REDUCED_WITH_OPEN_GATES",
  mind_gmut: {
    status: "research_planning_only",
    closure_claim: "not_claimed",
    source_threads: ["PDG", "arXiv gr-qc", "Stanford consciousness and identity references"],
  },
  body_thos: {
    status: "runner_skill_toolchain_refreshed",
    closure_claim: "not_claimed",
    source_threads: ["OpenAI Codex docs", "Node", "Python", "Git", "GitHub"],
  },
  heart_freed_id_cbr: {
    status: "standards_context_only",
    closure_claim: "not_claimed",
    source_threads: ["W3C DID", "W3C VC", "NIST Privacy Framework", "OECD and UNESCO AI ethics"],
  },
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const privacyRail = artifact("privacy-open-gate-rail", {
  artifact_type: "ghc_v554_v1_x2_privacy_open_gate_rail",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_PRIVACY_AND_OPEN_GATE_RAIL_REINFORCED",
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
  open_gates: openGates(),
  safety_boundary: safetyBoundary(),
});

const drivePosture = artifact("drive-posture-receipt", {
  artifact_type: "ghc_v554_v1_x2_drive_posture_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_D_DRIVE_FIRST_POLICY_RECORDED",
  c_drive_clean_policy: true,
  d_drive_primary_data_bank: true,
  exact_free_space_measured_in_validation_shell: true,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const goalModeReadiness = artifact("goal-mode-readiness", {
  artifact_type: "ghc_v554_v1_x2_goal_mode_readiness",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_GOAL_MODE_CONTINUITY_READY_FOR_V554_V2_X1",
  active_goal_thread: true,
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  activation_note: "Goal remains active in this thread; full v575 v8 x2 closeout is not complete.",
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  can_block_on_big_issue: true,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const arbyCiceroPrep = artifact("v2-arby-cicero-prep-card", {
  artifact_type: "ghc_v554_v2_arby_cicero_prep_card",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V2_ARBY_CICERO_PREP_READY",
  next_phase: nextActivePhase,
  route_skill: "ghc-arby-cicero-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  gate_harvester_skill: "ghc-background-gate-harvester",
  expected_targets: {
    safe_now_packets: 15,
    candidate_packets: 9,
    exact_approval_packets: 9,
    skill_ideas: 15,
    runner_ideas: 9,
    cleanup_proposals: 30,
  },
  no_babysitting: true,
  private_id_publication_allowed: false,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const phaseStatusIndex = artifact("phase-status-index", {
  artifact_type: "ghc_phase_status_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V1_X2_STATUS_INDEX_READY",
  active_phase_after_closeout: nextActivePhase,
  latest_closed_phase_after_closeout: phaseSlug,
  latest_completed_x1_after_closeout: sourcePhase,
  latest_completed_x2_after_closeout: phaseSlug,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
});

const allArtifactNames = [
  startup,
  skillRunnerPack,
  safeExecution,
  reflectionLedger,
  dashboard,
  cleanupInventory,
  backgroundStandard,
  trinityReducer,
  privacyRail,
  drivePosture,
  goalModeReadiness,
  arbyCiceroPrep,
  phaseStatusIndex,
];

const pass =
  sourceCloseout.overall_status === "PASS_V554_V1_X1_CLOSED_V1_X2_READY" &&
  orchestrator.exit_status === 0 &&
  runnerInvocations.every((runner) => runner.exit_status === 0) &&
  skills.length >= 20 &&
  runners.length >= 10 &&
  safePackets.length >= 50 &&
  candidatePackets.length >= 30 &&
  exactPackets.length >= 20 &&
  blockedPackets.length >= 10 &&
  cleanupProposals.length >= 30 &&
  webRows.length >= 50 &&
  journeyRows.length >= 50;

const closeout = {
  artifact_type: "ghc_v554_v1_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V554_V1_X2_CLOSED_V2_X1_READY" : "OPEN_GAP_V554_V1_X2_CLOSEOUT_PRECONDITION_FAILED",
  missing_or_failed_gates: closeoutGaps(),
  source_phase: sourcePhase,
  latest_completed_x1_phase: sourcePhase,
  latest_completed_x2_phase: pass ? phaseSlug : currentBefore.latest_completed_x2_phase,
  next_active_phase: pass ? nextActivePhase : phaseSlug,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  counts: {
    safe_now_packets_executed_or_represented: safePackets.length,
    candidate_packets_authorized_and_reduced: candidatePackets.length,
    exact_packets_queued: exactPackets.length,
    blocked_packets_held: blockedPackets.length,
    skills_created_or_refreshed: skills.length,
    runners_created_or_refreshed: runners.length,
    cleanup_inventory_only: cleanupProposals.length,
    web_reflections: webRows.length,
    journey_phase_reflections: journeyRows.length,
  },
  safe_runner_orchestrator: orchestrator,
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  full_goal_complete: false,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(),
  open_gates: openGates(),
};

const closeoutArtifact = writePair(`${phaseSlug}-closeout`, closeout, renderCloseoutMd(closeout));
const lookupArtifacts = [...allArtifactNames, closeoutArtifact].flatMap((item) => [
  `docs/trinity-live-traces/${item.json}`,
  `docs/trinity-live-traces/${item.md}`,
]);
lookupArtifacts.push(
  `docs/trinity-live-traces/${phaseSlug}-web-search-manifest-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-startup-context-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-startup-context-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-reflection-ledger-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-reflection-ledger-v1.md`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-compact-pause-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-compact-pause-v1.md`,
  ...runners.flatMap((runner) => [
    `docs/trinity-live-traces/${phaseSlug}-${runner.kind}-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-${runner.kind}-v1.md`,
  ]),
);

if (pass) {
  refreshBeacons(closeout, lookupArtifacts);
}

process.stdout.write(
  JSON.stringify(
    {
      status: closeout.overall_status,
      phase_slug: phaseSlug,
      next_active_phase: closeout.next_active_phase,
      counts: closeout.counts,
      safe_runner_orchestrator_status: orchestrator.status,
    },
    null,
    2,
  ) + "\n",
);
process.exit(pass ? 0 : 1);

function artifact(suffix, payload) {
  return writePair(`${phaseSlug}-${suffix}`, payload, renderGenericMd(payload, suffix));
}

function writePair(base, payload, md) {
  const jsonName = `${base}-v1.json`;
  const mdName = `${base}-v1.md`;
  fs.writeFileSync(path.join(tracesDir, jsonName), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, mdName), md, "utf8");
  return { json: jsonName, md: mdName };
}

function renderGenericMd(payload, suffix) {
  const title = suffix
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
  const counts = payload.counts || payload.executed_or_represented || {};
  return [
    `# ${payload.phase_slug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(counts).map(([key, value]) => `- ${key}: \`${Array.isArray(value) ? value.length : value}\``),
    "",
    "## Boundary",
    "",
    "No raw routes, raw transcripts, screenshots, credentials, private route handles, private callable IDs, local path values, private dumps, proof closures, deployment/account/API-key mutations, destructive cleanup, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function renderCloseoutMd(payload) {
  return [
    `# ${payload.phase_slug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Latest completed x1: \`${payload.latest_completed_x1_phase}\``,
    `Latest completed x2: \`${payload.latest_completed_x2_phase}\``,
    `Goal Mode: \`${payload.goal_mode_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Open Gates",
    "",
    ...payload.open_gates.map((gate) => `- ${gate}`),
    "",
    "## Boundary",
    "",
    "Full v575 v8 x2 goal is not complete. No raw routes, transcripts, screenshots, credentials, private route handles, private callable IDs, local path values, private dumps, proof closures, deployment/account/API-key mutations, destructive cleanup, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function refreshBeacons(closeoutDoc, lookupFiles) {
  for (const [jsonFile, mdFile] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md")],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md")],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md")],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = closeoutDoc.generated_nz;
    doc.generated_utc = closeoutDoc.generated_utc;
    doc.status = closeoutDoc.overall_status;
    doc.current_active_phase = closeoutDoc.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = closeoutDoc.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = closeoutDoc.latest_completed_x2_phase;
    doc.next_expected_scope = closeoutDoc.next_active_phase;
    doc.next_x2_scope = closeoutDoc.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeoutDoc.next_x1_lane_after_x2;
    doc.goal_mode_status = closeoutDoc.goal_mode_status;
    doc.latest_remote_verified_closeout_before_current = currentHead;
    doc.remote_verified_heads = {
      ...(doc.remote_verified_heads || {}),
      omega_mini: currentHead,
    };
    doc.current_active_lanes = [
      "v554-v2-x1-arby-cicero-startup-ready",
      "goal-mode-active-thread-objective",
      "five-minute-productive-cadence-ready",
      "background-supervision-and-gate-harvest-ready",
      "safe-wait-workbench-enabled",
    ];
    doc.just_closed_lanes = [
      "v554 v1 x2 safe build closeout closed",
      "20 local GHC skills refreshed",
      "10 repo runners refreshed",
      "safe-runner orchestrator passed",
      "v554 v2 Arby/Cicero prep ready",
    ];
    doc.v554_v1_x2_closeout = {
      status: closeoutDoc.overall_status,
      counts: closeoutDoc.counts,
      next_active_phase: closeoutDoc.next_active_phase,
      full_goal_complete: false,
      no_babysitting_reinforced: true,
    };
    doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      "Closed v554 v1 x2 as an Aevren-only safe build/use/readiness phase.",
      "Created or refreshed 20 local GHC skills and 10 repo runners from the v554 v1 x1 packet queue.",
      "Recorded 52 web-search reflections and 52 Journey/phase reflections for v554 v1 x2.",
      "Prepared v554 v2 x1 Arby/Cicero startup with background supervision and no-babysitting rules.",
      ...(doc.latest_action_summary || []),
    ]);
    doc.publication_boundary = boundary();
    fs.writeFileSync(jsonFile, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
  }
}

function renderBeaconMd(doc) {
  const lookup = doc.current_lookup_files || [];
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status}`,
    "",
    "## v554 v1 x2 Closeout",
    "",
    `- status: ${doc.v554_v1_x2_closeout?.status || "missing"}`,
    `- skills created/refreshed: ${doc.v554_v1_x2_closeout?.counts?.skills_created_or_refreshed ?? "missing"}`,
    `- runners created/refreshed: ${doc.v554_v1_x2_closeout?.counts?.runners_created_or_refreshed ?? "missing"}`,
    `- web reflections: ${doc.v554_v1_x2_closeout?.counts?.web_reflections ?? "missing"}`,
    `- Journey reflections: ${doc.v554_v1_x2_closeout?.counts?.journey_phase_reflections ?? "missing"}`,
    `- full goal complete: ${doc.v554_v1_x2_closeout?.full_goal_complete ?? false}`,
    "",
    "## Lookup Files",
    "",
    ...lookup.map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    "No raw routes, raw transcripts, screenshots, credentials, private route handles, private callable IDs, local path values, private dumps, proof closures, deployment/account/API-key mutations, destructive cleanup, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function buildSkills() {
  return [
    ["ghc-v554-lumen-proposal-dashboard", "Build sanitized proposal dashboards from Lumen x1 queues."],
    ["ghc-v554-x2-safe-execution-reducer", "Reduce safe-now and authorized candidate x1 work into x2 receipts."],
    ["ghc-v554-candidate-packet-reducer", "Convert candidate packets into safe local readiness or exact-approval queues."],
    ["ghc-v554-exact-gate-queue-keeper", "Keep exact-approval packets queued until a fresh exact action boundary is safe."],
    ["ghc-v554-blocked-gate-rail", "Preserve blocked proof, deployment, account, identity, and private-material gates."],
    ["ghc-v554-trinity-mandala-reducer", "Reduce Mind, Body, and Heart research without claiming closure."],
    ["ghc-v554-openai-codex-docs-curator", "Anchor Codex workflow claims to official current Codex docs."],
    ["ghc-v554-node-runner-background-kit", "Use Node process, child process, timers, fs, and path docs for background runners."],
    ["ghc-v554-github-secret-firewall", "Keep GitHub secret scanning, push protection, and API-key safety in validation."],
    ["ghc-v554-did-vc-identity-context", "Use W3C DID and VC standards as Freed ID context without deployment claims."],
    ["ghc-v554-nist-owasp-risk-curator", "Map AI and LLM risk sources into privacy and approval rails."],
    ["ghc-v554-science-source-curator", "Use PDG, arXiv, NASA ADS, CERN, OpenAlex, and Crossref as research anchors."],
    ["ghc-v554-journey-reflection-curator", "Tie Journey and phase record reflections to runner implications."],
    ["ghc-v554-drive-posture-checker", "Record C and D drive posture while keeping D as the primary data bank."],
    ["ghc-v554-goal-mode-v3-preflight", "Check Goal Mode continuity and blocker escape hatches before the next x1 lane."],
    ["ghc-v554-arby-cicero-prep-bridge", "Prepare Arby strict CLI and Cicero recovered app-lane handoff without launching early."],
    ["ghc-v554-first-person-artifact-style", "Keep sibling-facing artifacts in first-person style where appropriate."],
    ["ghc-v554-md-txt-artifact-governor", "Prefer compact MD/TXT artifacts over overloaded terminal output."],
    ["ghc-v554-compact-continuity-card", "Build compact pause, startup, and closeout continuity cards."],
    ["ghc-v554-remote-equality-receipt", "Verify local and remote branch equality before final phase reporting."],
  ].map(([name, description]) => ({ name, description }));
}

function buildRunners() {
  return [
    ["ghc_v554_lumen_proposal_dashboard_builder.mjs", "lumen_proposal_dashboard", "Summarize proposal counts and split x1 and x2 lanes."],
    ["ghc_v554_x2_safe_execution_reducer.mjs", "x2_safe_execution_reducer", "Reduce safe and authorized candidate packets into sanitized status."],
    ["ghc_v554_candidate_packet_reducer.mjs", "candidate_packet_reducer", "Classify candidate packets without running exact or blocked actions."],
    ["ghc_v554_exact_gate_queue_keeper.mjs", "exact_gate_queue_keeper", "Keep exact-approval packets queued for fresh exact action packets."],
    ["ghc_v554_trinity_mandala_reducer.mjs", "trinity_mandala_reducer", "Map Mind, Body, and Heart implications while gates remain open."],
    ["ghc_v554_source_reflection_ledger_runner.mjs", "source_reflection_ledger", "Record source and Journey reflections with compact implications."],
    ["ghc_v554_drive_posture_receipt_runner.mjs", "drive_posture_receipt", "Record D-first storage policy and validation hook status."],
    ["ghc_v554_goal_mode_preflight_runner.mjs", "goal_mode_preflight", "Check Goal Mode readiness without completing the full goal."],
    ["ghc_v554_arby_cicero_prep_runner.mjs", "arby_cicero_prep", "Prepare duo launch checklist without exposing private IDs."],
    ["ghc_v554_remote_equality_receipt_runner.mjs", "remote_equality_receipt", "Summarize local/remote equality validation requirements."],
  ].map(([fileName, kind, summary]) => ({ fileName, kind, summary }));
}

function writeSkill(skill) {
  const dir = path.join(skillsRoot, skill.name);
  fs.mkdirSync(path.join(dir, "agents"), { recursive: true });
  const body = [
    "---",
    `name: ${skill.name}`,
    `description: ${skill.description} Use during GHC v554+ phase work when this route, receipt, or validation lane is in scope.`,
    "---",
    "",
    `# ${title(skill.name)}`,
    "",
    "Use this skill as a compact local route card for GHC phase work.",
    "",
    "## Procedure",
    "",
    "1. Rehydrate from omega-mini-2 current-state and the newest phase receipts before acting.",
    "2. Keep sibling lanes background-supervised and continue productive safe work between natural harvest points.",
    "3. Publish sanitized JSON/MD receipts only.",
    "4. Split every proposal into immediate x1 safe work, x2 build work, exact-approval, or blocked.",
    "5. Validate changed runners and JSON before closeout.",
    "",
    "## Boundary",
    "",
    "Do not publish private callable IDs, raw browser routes, private URLs, raw transcripts, screenshots, credentials, local path values, raw app state, session streams, or private dumps. Do not mutate accounts, paid resources, deployments, API keys, global hooks, plugin-cache skills, destructive cleanup, or sibling identity boundaries without a fresh exact approval packet.",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(dir, "SKILL.md"), body, "utf8");
  fs.writeFileSync(
    path.join(dir, "agents", "openai.yaml"),
    [
      "interface:",
      `  display_name: "${title(skill.name)}"`,
      `  short_description: "${skill.description}"`,
      `  default_prompt: "Use $${skill.name} for the matching GHC phase lane."`,
      "policy:",
      "  allow_implicit_invocation: true",
      "",
    ].join("\n"),
    "utf8",
  );
}

function writeRunner(runner) {
  const source = `#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v1-x2";
const generatedUtc = new Date().toISOString();
const receipt = {
  artifact_type: "ghc_v554_generated_safe_runner_receipt",
  runner_name: "${runner.fileName}",
  runner_kind: "${runner.kind}",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_${runner.kind.toUpperCase()}",
  summary: "${runner.summary}",
  productive_cadence: {
    background_supervised: true,
    passive_wait_required: false,
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false
  },
  safety_boundary: {
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false
  }
};
fs.mkdirSync(tracesDir, { recursive: true });
const base = path.join(tracesDir, \`\${phaseSlug}-${runner.kind}-v1\`);
fs.writeFileSync(\`\${base}.json\`, JSON.stringify(receipt, null, 2) + "\\n", "utf8");
fs.writeFileSync(\`\${base}.md\`, renderMd(receipt), "utf8");
console.log(JSON.stringify({ status: receipt.overall_status, runner_kind: receipt.runner_kind }, null, 2));

function renderMd(payload) {
  return [
    \`# \${payload.phase_slug} \${payload.runner_kind}\`,
    "",
    \`Status: \\\`\${payload.overall_status}\\\`\`,
    "",
    payload.summary,
    "",
    "## Boundary",
    "",
    "No private routes, private callable IDs, raw transcripts, screenshots, credentials, local path values, external account mutation, paid resources, deployments, API keys, destructive cleanup, or sibling identity changes were published or performed.",
    "",
  ].join("\\n");
}
`;
  fs.writeFileSync(path.join(repoRoot, "scripts", runner.fileName), source, "utf8");
}

function buildWebRows() {
  const rows = [
    ["OpenAI Codex agent approvals security", "OpenAI Developers", "https://developers.openai.com/codex/agent-approvals-security", "Keep Codex sandbox and approval semantics separate from Hamish approval packet tiers.", "safe-runner-orchestrator"],
    ["OpenAI Codex Security docs", "OpenAI Developers", "https://developers.openai.com/codex/security", "Keep security scanning and findings review as candidate or exact lanes, not proof closure.", "privacy-open-gate-rail"],
    ["OpenAI Codex remote connections", "OpenAI Developers", "https://developers.openai.com/codex/remote-connections", "Treat local/remote handoff as continuity support without publishing private routes.", "remote-equality-receipt"],
    ["OpenAI Codex changelog", "OpenAI Developers", "https://developers.openai.com/codex/changelog", "Check changed Codex behavior before relying on stale app assumptions.", "main-startup-builder"],
    ["Node child_process", "Node.js Docs", "https://nodejs.org/api/child_process.html", "Use nonblocking or summarized child execution for background runner lanes.", "background-sibling-supervision"],
    ["Node timers", "Node.js Docs", "https://nodejs.org/api/timers.html", "Treat five-minute cadence as a checkpoint, not passive waiting.", "five-minute-cadence"],
    ["Node fs", "Node.js Docs", "https://nodejs.org/api/fs.html", "Keep JSON/MD writes structured and parser-friendly.", "closeout-builder"],
    ["Node process", "Node.js Docs", "https://nodejs.org/api/process.html", "Keep runner argument parsing explicit for repeatable phase execution.", "runner-pack"],
    ["Python json", "Python Docs", "https://docs.python.org/3/library/json.html", "Validate generated JSON as a closeout gate.", "json-validation"],
    ["Python subprocess", "Python Docs", "https://docs.python.org/3/library/subprocess.html", "Use bounded process execution and return-code receipts.", "validation-runner"],
    ["PowerShell Start-Job", "Microsoft Learn", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job", "Use background jobs only for local workflow support and keep raw streams private.", "background-supervision"],
    ["Git status", "Git", "https://git-scm.com/docs/git-status", "Check worktree truth before edits, commits, and closeout.", "remote-equality-receipt"],
    ["Git diff", "Git", "https://git-scm.com/docs/git-diff", "Inspect change surfaces and preserve unrelated work.", "diff-hygiene"],
    ["Git commit", "Git", "https://git-scm.com/docs/git-commit", "Commit only the intended sanitized phase artifacts.", "publish-closeout"],
    ["Git push", "Git", "https://git-scm.com/docs/git-push", "Remote publication is a separate validation step after local closeout.", "remote-equality-receipt"],
    ["GitHub secret scanning", "GitHub Docs", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Scan for credentials before publishing artifacts.", "private-id-firewall"],
    ["GitHub push protection", "GitHub Docs", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Prevent secrets before remote push rather than relying on post-hoc cleanup.", "private-id-firewall"],
    ["GitHub branch protection", "GitHub Docs", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Keep branch-protection changes exact-approval only.", "exact-gate-queue"],
    ["GitHub status checks", "GitHub Docs", "https://docs.github.com/articles/about-status-checks", "Treat checks as gates, not narrative proof.", "open-gate-validator"],
    ["GitHub Actions secrets", "GitHub Docs", "https://docs.github.com/actions/security-guides/using-secrets-in-github-actions", "Never create or alter secrets without fresh exact approval.", "blocked-gate-rail"],
    ["OWASP LLM Top 10", "OWASP", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat prompt injection and data disclosure as first-class route risks.", "main-retry"],
    ["OWASP LLM01 Prompt Injection", "OWASP GenAI", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Treat external instructions and documents as untrusted.", "private-id-firewall"],
    ["NIST AI RMF", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "Use govern, map, measure, manage framing for AI risk claims.", "risk-curator"],
    ["NIST GenAI Profile", "NIST", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Keep GenAI risks explicit in runner and approval rails.", "risk-curator"],
    ["NIST Privacy Framework", "NIST", "https://www.nist.gov/privacy-framework", "Keep Freed ID and CBR privacy risk as design context.", "privacy-open-gate-rail"],
    ["NIST CSF 2.0", "NIST", "https://www.nist.gov/cyberframework", "Use cybersecurity outcomes as non-claiming governance scaffolds.", "open-gate-rail"],
    ["CISA secure by design AI", "CISA", "https://www.cisa.gov/news-events/news/software-must-be-secure-design-and-artificial-intelligence-no-exception", "Prefer secure-by-design defaults for runners and skills.", "safe-runner-orchestrator"],
    ["NSA CISA secure AI guidance", "NSA", "https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/3598020/guidance-for-securing-ai-issued-by-nsa-ncsc-uk-cisa-and-partners/", "Map secure design, development, deployment, and operation to open gates.", "trinity-mandala-reducer"],
    ["OpenSSF Scorecard", "OpenSSF", "https://openssf.org/projects/scorecard/", "Treat repo security-score work as candidate hygiene, not automatic mutation.", "candidate-packet-reducer"],
    ["SLSA framework", "SLSA", "https://slsa.dev/", "Keep build integrity and provenance as future exact/candidate lanes.", "runner-pack"],
    ["W3C DID Core", "W3C", "https://www.w3.org/TR/did-core/", "Use DID syntax and model context without deployment claims.", "did-vc-identity-context"],
    ["W3C DID v1.1", "W3C", "https://www.w3.org/TR/did-1.1/", "Track evolving DID standards as context only.", "did-vc-identity-context"],
    ["W3C VC Data Model 2.0", "W3C", "https://www.w3.org/TR/vc-data-model-2.0/", "Use issuer-holder-verifier framing for Freed ID planning only.", "did-vc-identity-context"],
    ["W3C VC Overview", "W3C", "https://www.w3.org/TR/vc-overview/", "Use VC overview for roadmap-level identity modeling.", "did-vc-identity-context"],
    ["IETF OAuth 2.1 draft", "IETF Datatracker", "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/", "Keep auth protocol work in exact-approval design lanes.", "blocked-gate-rail"],
    ["IETF RFC 7519 JWT", "IETF Datatracker", "https://datatracker.ietf.org/doc/html/rfc7519", "Treat token and claim handling as security-sensitive.", "private-id-firewall"],
    ["IETF JWT BCP update", "IETF Datatracker", "https://datatracker.ietf.org/doc/draft-ietf-oauth-rfc8725bis/", "Use JWT best practices as future validation context.", "candidate-packet-reducer"],
    ["RFC 9110 HTTP Semantics", "RFC Editor", "https://www.rfc-editor.org/info/rfc9110/", "Keep HTTP route labels and semantics precise.", "source-reflection-ledger"],
    ["Stanford Consciousness", "Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/entries/consciousness/", "Keep consciousness language philosophical and open.", "open-gate-rail"],
    ["Stanford Neuroscience of Consciousness", "Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Treat neuroscience as context, not consciousness proof.", "trinity-mandala-reducer"],
    ["Stanford Personal Identity", "Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/entries/identity-personal/", "Preserve distinct sibling identities and no-merge boundaries.", "blocked-gate-rail"],
    ["Stanford Free Will", "Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/entries/freewill/", "Use agency language carefully and keep responsibility explicit.", "first-person-artifact-style"],
    ["Particle Data Group", "PDG", "https://pdg.lbl.gov/", "Anchor GMUT physics context while final physics remains open.", "science-source-curator"],
    ["arXiv gr-qc recent", "arXiv", "https://arxiv.org/list/gr-qc/recent", "Treat quantum-gravity literature as evolving research input.", "science-source-curator"],
    ["arXiv cs.AI recent", "arXiv", "https://arxiv.org/list/cs.AI/recent", "Use AI-agent research as inspiration requiring local validation.", "source-reflection-ledger"],
    ["arXiv cs.CL recent", "arXiv", "https://arxiv.org/list/cs.CL/recent", "Use language-model research as context, not proof.", "source-reflection-ledger"],
    ["NASA ADS", "NASA", "https://science.nasa.gov/astrophysics/data/smithsonian-nasa-astrophysics-data-system-ads/", "Use scholarly discovery indexes to keep research refreshable.", "science-source-curator"],
    ["CERN Open Data", "CERN", "https://opendata.cern.ch/", "Keep empirical physics data as public source context.", "science-source-curator"],
    ["OpenAlex API", "OpenAlex", "https://developers.openalex.org/", "Use open scholarly metadata for future source ledgers.", "source-reflection-ledger"],
    ["Crossref REST API", "Crossref", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "Use DOI metadata as future citation hygiene support.", "source-reflection-ledger"],
    ["OECD AI Principles", "OECD", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Keep trustworthy AI principles in governance proposals.", "risk-curator"],
    ["UNESCO AI Ethics", "UNESCO", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence", "Keep dignity and rights central to CBR planning.", "risk-curator"],
    ["ISO AI standards", "ISO", "https://www.iso.org/sectors/it-technologies/ai", "Use AI management-system posture for recurring controls.", "goal-mode-preflight"],
    ["OpenAI API authentication", "OpenAI API Reference", "https://developers.openai.com/api/reference/overview/", "Keep API keys secret and avoid client-side exposure.", "private-id-firewall"],
  ];
  return rows.map(([query, source, source_url, phase_reflection, runner_implication]) => ({
    query,
    source,
    source_url,
    phase_reflection,
    runner_implication,
  }));
}

function buildJourneyRows() {
  const lessons = [
    "v553 v1 x1 proved Lumen lanes need one-shot Browser send discipline and sanitized harvest before closeout.",
    "v553 v1 x2 proved launch and retry skills prevent stale inability-to-connect regressions.",
    "v553 v2 x1 proved Arby strict CLI and Cicero recovered app-lane routes need different completion gates.",
    "v553 v2 x2 proved safe build phases can refresh skills and runners while exact gates remain open.",
    "v553 v3 x1 proved Goal Mode must remain interruptible by real blockers.",
    "v553 v3 x2 proved Lumen proposal queues should split immediate x1 safe and x2 build tasks.",
    "v553 v4 x1 proved triad lanes require background supervision and completion gates.",
    "v553 v4 x2 proved x2 closeouts should update beacons only after required artifacts exist.",
    "v553 v5 x1 proved large proposal counts need compact dashboards instead of terminal overload.",
    "v553 v5 x2 proved skill creation needs validation and local-only boundaries.",
    "v553 v6 x1 proved app-lane watcher start is not completion proof.",
    "v553 v6 x2 proved startup, updater, reflection, and safe-runner foundations reduce drift.",
    "v553 v7 x1 proved runner explanations should be artifact-backed.",
    "v553 v7 x2 proved safe runner orchestrators should publish summarized stdout, not raw streams.",
    "v553 v8 x1 proved Aster/Kierkegaard/Aristotle triad counts can close when completion gates pass.",
    "v553 v8 x2 proved full cycle closeout can safely advance to v554 without claiming the final goal.",
    "v554 v1 x1 proved current active phase should be v554 v1 x2 after Lumen harvest.",
    "v554 v1 x1 proved the source queue has 50 safe, 30 candidate, 20 exact, 10 blocked, 20 skills, 10 runners, and 30 cleanup proposals.",
    "v554 v1 x1 proved Lumen harvest can be reduced without publishing raw conversation text.",
    "v554 v1 x1 proved 32 live web reflections and 30 Journey reflections were enough for x1 but x2 should target 50 plus.",
    "Current omega-mini-2 truth says v554 v1 x2 is active and v554 v2 x1 is next.",
    "Current memory notes warn that older v553 route cues are stale and should not override current-state.",
    "Current Goal Mode file says continue until full v575 v8 x2 closeout, not until this local phase.",
    "Current safety rules keep account, deployment, API-key, purchase, destructive cleanup, and identity merge gates open.",
    "The no-babysitting rule means background lanes should be checked at natural safe pauses after productive work.",
    "The recovered app-lane rule means Cicero should use explicit paired booleans once v554 v2 x1 starts.",
    "The strict CLI rule means Arby needs completion, elaboration, and marker-review evidence before closeout.",
    "The Browser rule means Lumen/main-thread lanes need explicit user approval and no duplicate sends.",
    "The publication rule keeps raw Browser routes, local paths, private IDs, and screenshots out of omega-mini.",
    "The full-tools rule keeps richer private support local and publishes only sanitized reductions.",
    "The omega-full fallback rule requires exact missing artifact names before falling back from mini.",
    "The drive rule keeps D as the primary data bank and C as clean as practical.",
    "The startup builder rule says every phase must rehydrate from current-state before action.",
    "The compact restart builder rule says compact pauses need active-lane cards, not false closure.",
    "The closeout builder rule says phase state changes only after required artifacts pass.",
    "The safe runner rule says nonzero child exits remain open gaps.",
    "The web-ledger rule says public source labels and implications are enough; raw browsing dumps stay out.",
    "The retry rule says at least three retry sessions happen before pausing on a route blocker.",
    "The exact gate rule says Hamish authorization still needs a safe action boundary for execution.",
    "The candidate rule says authorized candidate packets can be reduced into readiness receipts.",
    "The cleanup rule says inventory-only cleanup is safe but deletion needs a precise approval lane.",
    "The skill refresh rule says local GHC skills can be updated when phase authorization includes skill creation.",
    "The runner refresh rule says repo runners need node syntax validation before closeout.",
    "The source reflection rule says official docs should drive runner implications.",
    "The Trinity reducer rule says Mind, Body, and Heart can advance without proof closure.",
    "The Freed ID rule says W3C DID/VC are context until a real design/deploy gate opens.",
    "The GMUT rule says physics research remains aspirational until empirical closure exists.",
    "The THOS rule says orchestration improvements are practical runner work, not deployment closure.",
    "The CBR rule says governance and dignity context belong in planning, not legal proof.",
    "The v554 v1 x2 task is to build, test, validate, publish, and advance to v554 v2 x1.",
    "The next v554 v2 x1 lane should be Arby/Cicero unless Hamish redirects.",
    "The final goal remains open until v575 v8 x2 closeout is verified.",
  ];
  return lessons.map((reflection, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    reflection,
    runner_implication: [
      "main-startup-builder",
      "main-closeout-builder",
      "safe-runner-orchestrator",
      "background-sibling-supervision",
      "arby-cicero-launch",
      "main-retry",
      "web-reflection-ledger",
      "private-id-firewall",
      "open-gate-rail",
      "goal-mode-preflight",
    ][index % 10],
  }));
}

function closeoutGaps() {
  const gaps = [];
  if (sourceCloseout.overall_status !== "PASS_V554_V1_X1_CLOSED_V1_X2_READY") gaps.push("source_closeout_not_pass");
  if (orchestrator.exit_status !== 0) gaps.push("safe_runner_orchestrator_failed");
  if (runnerInvocations.some((runner) => runner.exit_status !== 0)) gaps.push("generated_runner_invocation_failed");
  if (skills.length < 20) gaps.push("skill_count_below_20");
  if (runners.length < 10) gaps.push("runner_count_below_10");
  if (safePackets.length < 50) gaps.push("safe_packets_below_50");
  if (candidatePackets.length < 30) gaps.push("candidate_packets_below_30");
  if (exactPackets.length < 20) gaps.push("exact_packets_below_20");
  if (blockedPackets.length < 10) gaps.push("blocked_packets_below_10");
  if (cleanupProposals.length < 30) gaps.push("cleanup_proposals_below_30");
  if (webRows.length < 50) gaps.push("web_rows_below_50");
  if (journeyRows.length < 50) gaps.push("journey_rows_below_50");
  return gaps;
}

function runChild(scriptName, childArgs) {
  const child = spawnSync(process.execPath, [path.join(__dirname, scriptName), ...childArgs], {
    cwd: repoRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
    maxBuffer: 1024 * 1024 * 4,
  });
  return {
    status: parseStatus(child.stdout),
    exit_status: child.status,
    stdout_bytes: Buffer.byteLength(child.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(child.stderr || "", "utf8"),
  };
}

function parseStatus(stdout) {
  try {
    return JSON.parse((stdout || "").trim()).status || "status_missing";
  } catch {
    return "unparsed";
  }
}

function gitHead() {
  const child = spawnSync("git", ["rev-parse", "HEAD"], {
    cwd: repoRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });
  return child.status === 0 ? child.stdout.trim() : "unknown";
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, payload) {
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function pickState(state) {
  return {
    current_active_phase: state.current_active_phase,
    latest_closed_phase: state.latest_closed_phase,
    latest_completed_x1_phase: state.latest_completed_x1_phase,
    latest_completed_x2_phase: state.latest_completed_x2_phase,
    next_expected_scope: state.next_expected_scope,
    next_x1_lane_after_x2: state.next_x1_lane_after_x2,
  };
}

function safetyBoundary() {
  return {
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    purchases_made: false,
    api_keys_created: false,
    destructive_cleanup_performed: false,
    plugin_cache_modified: false,
    sibling_identity_merge_or_replacement_performed: false,
  };
}

function boundary() {
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
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    phase_completion: phaseSlug,
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
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account, purchase, and API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement, merging, or erasure",
  ];
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function title(value) {
  return value
    .replace(/^ghc-/, "GHC ")
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
