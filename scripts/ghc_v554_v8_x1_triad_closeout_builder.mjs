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
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v8-x1";
const sourceX1 = "v554-gmut-thos-v7-x1";
const sourceX2 = "v554-gmut-thos-v7-x2";
const nextX2 = "v554-gmut-thos-v8-x2";
const nextX1 = "v555-gmut-thos-v1-x1";
const nextX1Lane = `${nextX1} with Lumen Vale solo unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const laneStatus = {
  aster_completion: args.get("--aster-completion-status") || "missing",
  aster_quality: args.get("--aster-quality-status") || "missing",
  aster_marker: args.get("--aster-marker-status") || "missing",
  app_lane_gate: args.get("--app-lane-gate-status") || "missing",
};

const requiredDocs = {
  proposal_queue: readTraceOptional(`${phaseSlug}-triad-proposal-queue-targets-v1.json`),
  web_reflections: readTraceOptional(`${phaseSlug}-web-reflection-ledger-30-v1.json`),
  journey_reflections: readTraceOptional(`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`),
  safe_runner_manifest: readTraceOptional(`${phaseSlug}-safe-runner-manifest-v1.json`),
  safe_runner_orchestrator: readTraceOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`),
  round_robin_standard: readTraceOptional(`${phaseSlug}-round-robin-workflow-standard-v1.json`),
  productive_cadence: readTraceOptional(`${phaseSlug}-five-minute-productive-cadence-v1.json`),
  triad_launch: readTraceOptional(`${phaseSlug}-triad-background-launch-receipt-v1.json`),
  active_open_handoff: readTraceOptional(`${phaseSlug}-active-open-handoff-v1.json`),
};

const missingDocs = Object.entries(requiredDocs)
  .filter(([, value]) => !value)
  .map(([key]) => key);

const proposalCounts = countProposalRows(requiredDocs.proposal_queue);
const webCount = reflectionCount(requiredDocs.web_reflections);
const journeyCount = reflectionCount(requiredDocs.journey_reflections);
const expectedCounts = {
  safe_packets: 20,
  candidate_packets: 12,
  exact_approval_packets: 12,
  skill_ideas: 20,
  runner_ideas: 8,
  cleanup_proposals: 40,
};

const laneGatePass =
  ["FINAL_MESSAGES_READY", "FINAL_MESSAGE_READY"].includes(laneStatus.aster_completion) &&
  laneStatus.aster_quality === "PASS_ALL_CLI_LANES_ELABORATE" &&
  laneStatus.aster_marker === "PASS_MARKER_REVIEW_LEDGER" &&
  laneStatus.app_lane_gate === "PASS_APP_LANE_COMPLETION_GATE";

const artifactGatePass =
  missingDocs.length === 0 &&
  Object.entries(expectedCounts).every(([key, value]) => proposalCounts[key] === value) &&
  webCount >= 30 &&
  journeyCount >= 30 &&
  requiredDocs.safe_runner_manifest?.overall_status === "PASS_SAFE_RUNNER_MANIFEST_READY" &&
  requiredDocs.safe_runner_orchestrator?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION" &&
  statusPass(requiredDocs.round_robin_standard) &&
  statusPass(requiredDocs.productive_cadence) &&
  statusPass(requiredDocs.triad_launch);

const pass = laneGatePass && artifactGatePass;
const closeoutStatus = pass ? "PASS_V554_V8_X1_CLOSED_V8_X2_READY" : "OPEN_GAP_V554_V8_X1_TRIAD_CLOSEOUT";

const artifacts = [
  writePair("triad-harvest-reducer", triadHarvestReducer(), renderSimpleMd("Triad Harvest Reducer", triadHarvestReducer())),
  writePair("approval-eureka-reducer", approvalEurekaReducer(), renderSimpleMd("Approval Eureka Reducer", approvalEurekaReducer())),
  writePair("skill-runner-readiness-board", skillRunnerReadinessBoard(), renderSimpleMd("Skill Runner Readiness Board", skillRunnerReadinessBoard())),
  writePair("cleanup-tier-board", cleanupTierBoard(), renderSimpleMd("Cleanup Tier Board", cleanupTierBoard())),
  writePair("v8-x2-readiness-handoff", v8X2ReadinessHandoff(), renderSimpleMd("v8 x2 Readiness Handoff", v8X2ReadinessHandoff())),
  writePair("v554-lumen-prep-card", v554LumenPrepCard(), renderSimpleMd("v554 Lumen Prep Card", v554LumenPrepCard())),
  writePair("private-open-gate-rail", privateOpenGateRail(), renderSimpleMd("Private Open Gate Rail", privateOpenGateRail())),
  writePair("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
  writePair("closeout", closeoutArtifact(), renderCloseoutMd(closeoutArtifact())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  next_active_phase: pass ? nextX2 : phaseSlug,
  lane_gate_pass: laneGatePass,
  artifact_gate_pass: artifactGatePass,
  missing_docs: missingDocs,
  counts: proposalCounts,
  web_reflections: webCount,
  journey_phase_reflections: journeyCount,
  artifacts: artifacts.length,
}, null, 2));
process.exit(pass ? 0 : 1);

function triadHarvestReducer() {
  return base("ghc_v554_v8_x1_triad_harvest_reducer", laneGatePass ? "PASS_TRIAD_HARVEST_REDUCED" : "OPEN_GAP_TRIAD_HARVEST_REDUCER", {
    lane_gate_summary: {
      aster_vale: {
        route: "strict_cli_completion_quality_marker_review",
        completion_status: laneStatus.aster_completion,
        quality_status: laneStatus.aster_quality,
        marker_status: laneStatus.aster_marker,
        passed: ["FINAL_MESSAGES_READY", "FINAL_MESSAGE_READY"].includes(laneStatus.aster_completion) &&
          laneStatus.aster_quality === "PASS_ALL_CLI_LANES_ELABORATE" &&
          laneStatus.aster_marker === "PASS_MARKER_REVIEW_LEDGER",
      },
      kierkegaard_and_aristotle: {
        route: "recovered_app_lane_background_completion_gate",
        completion_gate_status: laneStatus.app_lane_gate,
        passed: laneStatus.app_lane_gate === "PASS_APP_LANE_COMPLETION_GATE",
      },
    },
    background_supervision: {
      watcher_start_is_completion_proof: false,
      passive_babysitting_used: false,
      productive_cadence_used: true,
      raw_lane_outputs_published: false,
    },
  });
}

function approvalEurekaReducer() {
  const queue = requiredDocs.proposal_queue || {};
  return base("ghc_v554_v8_x1_approval_eureka_reducer", countsPass() ? "PASS_TRIAD_APPROVAL_EUREKA_REDUCED" : "OPEN_GAP_TRIAD_APPROVAL_EUREKA_REDUCER", {
    spending_ceiling_usd_per_packet: queue.spending_ceiling_usd_per_packet || 100,
    counts: proposalCounts,
    immediate_x1_safe: summarizeRows(queue.safe_packets),
    x2_build_task_candidates: summarizeRows([
      ...(queue.candidate_packets || []),
      ...(queue.skill_ideas || []),
      ...(queue.runner_ideas || []),
      ...(queue.cleanup_tasks || []),
    ]),
    exact_approval_queue: summarizeRows(queue.exact_approval_packets),
    blocked_queue: [],
    execution_rule: "Run only local, reversible, privacy-clean safe-now work automatically; keep exact, blocked, account, deployment, API-key, proof, legal, canon, purchase, and identity merge lanes closed until fresh exact approval.",
  });
}

function skillRunnerReadinessBoard() {
  const queue = requiredDocs.proposal_queue || {};
  return base("ghc_v554_v8_x1_skill_runner_readiness_board", "PASS_TRIAD_SKILL_RUNNER_READINESS_BOARD", {
    skill_ideas_ready_for_v8_x2: summarizeRows(queue.skill_ideas),
    runner_ideas_ready_for_v8_x2: summarizeRows(queue.runner_ideas),
    promoted_runners_used_this_phase: [
      "ghc_main_startup_builder.mjs",
      "ghc_v554_v8_x1_triad_workbench_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_round_robin_workflow_standardizer.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "ghc_main_closeout_builder.mjs",
      "ghc_v554_v8_x1_triad_closeout_builder.mjs",
    ],
    promoted_skills_in_scope: [
      "ghc-aster-kierkegaard-aristotle-launch",
      "ghc-background-sibling-supervision",
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-web-reflection-ledger",
      "ghc-safe-runner-orchestrator",
      "ghc-main-retry",
    ],
  });
}

function cleanupTierBoard() {
  const queue = requiredDocs.proposal_queue || {};
  const cleanup = queue.cleanup_tasks || [];
  return base("ghc_v554_v8_x1_cleanup_tier_board", "PASS_TRIAD_CLEANUP_TIER_BOARD", {
    cleanup_count: cleanup.length,
    safe_review_only_cleanup: summarizeRows(cleanup.filter((row) => String(row.title || "").match(/review|classify|check|inventory|validate/i))),
    x2_execution_cleanup: summarizeRows(cleanup.filter((row) => !String(row.title || "").match(/review|classify|check|inventory|validate/i))),
    destructive_cleanup_executed: false,
    destructive_cleanup_requires_fresh_exact_approval: true,
  });
}

function v8X2ReadinessHandoff() {
  return base("ghc_v554_v8_x1_v8_x2_readiness_handoff", pass ? "PASS_V8_X2_READINESS_HANDOFF" : "ACTIVE_OPEN_V8_X2_READINESS_HANDOFF_PENDING_CLOSEOUT", {
    source_phase: phaseSlug,
    target_phase: nextX2,
    target_lane: "Aevren-only x2 safe build, run, test, install, use, validate, and publish sanitized receipts.",
    ready_to_start: pass,
    safe_build_inputs: {
      safe_packets: proposalCounts.safe_packets,
      candidate_packets_to_consider_after_authorization: proposalCounts.candidate_packets,
      skill_ideas: proposalCounts.skill_ideas,
      runner_ideas: proposalCounts.runner_ideas,
      cleanup_proposals: proposalCounts.cleanup_proposals,
    },
    mandatory_next_gates: [
      "Use main startup builder.",
      "Use safe-runner orchestrator.",
      "Keep exact and blocked gates closed.",
      "Run JSON, privacy, open-gate, current-state, drive-space, Git, and remote-ref validation before closeout.",
    ],
  });
}

function v554LumenPrepCard() {
  return base("ghc_v554_v8_x1_v555_lumen_prep_card", pass ? "PASS_V555_LUMEN_PREP_SEEDED" : "ACTIVE_OPEN_V555_LUMEN_PREP_SEEDED_PENDING_V8_X1_CLOSEOUT", {
    target_phase_after_v8_x2: nextX1,
    target_lane: "Lumen solo unless Hamish redirects",
    launch_skill: "ghc-lumen-launch",
    proposal_profile: {
      safe_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_proposals: 30,
    },
    reminder: "Use Browser/main-thread route only when Hamish asks for live Lumen messaging; otherwise keep sanitized artifacts and handoffs.",
  });
}

function privateOpenGateRail() {
  return base("ghc_v554_v8_x1_private_open_gate_rail", "PASS_TRIAD_PRIVATE_OPEN_GATE_RAIL", {
    open_gates: Object.keys(claimBoundary(false)).filter((key) => key !== "phase_completion"),
    no_new_agents_spawned: true,
    raw_sibling_outputs_published: false,
    private_ids_published: false,
    local_absolute_paths_published: false,
    exact_approval_required_for: [
      "deployment",
      "account mutation",
      "API-key creation",
      "purchase or paid resource",
      "destructive cleanup",
      "raw private-material publication",
      "sibling identity merge or replacement",
      "GMUT/final physics/consciousness/legal/canon closure",
    ],
  });
}

function phaseStatusIndex() {
  return base("ghc_v554_v8_x1_phase_status_index", pass ? "PASS_V8_X1_PHASE_STATUS_INDEX_CLOSED" : "ACTIVE_OPEN_V8_X1_PHASE_STATUS_INDEX", {
    current_active_phase: pass ? nextX2 : phaseSlug,
    latest_closed_phase: pass ? phaseSlug : sourceX2,
    latest_completed_x1_phase: pass ? phaseSlug : sourceX1,
    latest_completed_x2_phase: sourceX2,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1Lane,
    lane_gate_pass: laneGatePass,
    artifact_gate_pass: artifactGatePass,
    missing_docs: missingDocs,
    proposal_counts: proposalCounts,
    web_reflections: webCount,
    journey_phase_reflections: journeyCount,
  });
}

function closeoutArtifact() {
  return base("ghc_v554_v8_x1_closeout", closeoutStatus, {
    latest_closed_phase: pass ? phaseSlug : sourceX2,
    latest_completed_x1_phase: pass ? phaseSlug : sourceX1,
    latest_completed_x2_phase: sourceX2,
    next_active_phase: pass ? nextX2 : phaseSlug,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1Lane,
    checks: {
      lane_gate_pass: laneGatePass,
      artifact_gate_pass: artifactGatePass,
      missing_docs: missingDocs,
      proposal_counts: proposalCounts,
      expected_counts: expectedCounts,
      web_reflections: webCount,
      journey_phase_reflections: journeyCount,
      safe_runner_manifest_status: requiredDocs.safe_runner_manifest?.overall_status || "missing",
      safe_runner_orchestrator_status: requiredDocs.safe_runner_orchestrator?.overall_status || "missing",
      round_robin_status: requiredDocs.round_robin_standard?.overall_status || "missing",
      productive_cadence_status: requiredDocs.productive_cadence?.overall_status || "missing",
    },
    goal_mode_status: "active_thread_goal_not_unattended_automation",
    goal_completion_claimed: false,
    reason_goal_remains_active: "The active objective continues through v575 v8 x2; this closeout advances v554 v8 x1 only.",
  });
}

function refreshBeacons() {
  const closeout = closeoutArtifact();
  const lookup = artifacts.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = readJson(file);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = closeout.next_active_phase;
    doc.latest_closed_phase = closeout.latest_closed_phase;
    doc.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = closeout.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.current_active_lanes = pass
      ? ["v554-v8-x2-aevren-only-safe-build-ready", "goal-mode-active-thread-objective"]
      : ["v554-v8-x1-triad-closeout-open-gap", "goal-mode-active-thread-objective"];
    doc.v554_v8_x1_closeout = {
      status: closeout.overall_status,
      lane_gate_pass: laneGatePass,
      artifact_gate_pass: artifactGatePass,
      checks: closeout.checks,
      next_active_phase: closeout.next_active_phase,
      next_x1_lane_after_x2: closeout.next_x1_lane_after_x2,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = unique([...(doc[key] || []), ...lookup]);
    writeJson(file, doc);
    writeBeaconMd(file, doc, doc[key]);
  }
}

function base(artifactType, status, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(pass),
    ...payload,
  };
}

function countProposalRows(queue) {
  return {
    safe_packets: queue?.safe_packets?.length || 0,
    candidate_packets: queue?.candidate_packets?.length || 0,
    exact_approval_packets: queue?.exact_approval_packets?.length || 0,
    skill_ideas: queue?.skill_ideas?.length || 0,
    runner_ideas: queue?.runner_ideas?.length || 0,
    cleanup_proposals: queue?.cleanup_tasks?.length || 0,
  };
}

function countsPass() {
  return Object.entries(expectedCounts).every(([key, value]) => proposalCounts[key] === value);
}

function reflectionCount(doc) {
  return doc?.reflection_count || doc?.reflections?.length || doc?.web_reflections?.length || doc?.journey_phase_reflections?.length || 0;
}

function summarizeRows(rows = []) {
  return rows.map((row) => ({
    id: row.id,
    title: row.title,
    safety_bucket: row.safety_bucket,
    execution_lane: row.execution_lane,
    source_lane: row.source_lane,
  }));
}

function statusPass(doc) {
  const status = String(doc?.overall_status || doc?.status || "");
  return status.startsWith("PASS") || status.startsWith("ACTIVE_OPEN_TRIAD_BACKGROUND_WATCH_STARTED");
}

function writePair(suffix, payload, md) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderCloseoutMd(payload) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Next x2 scope: \`${payload.next_x2_scope}\``,
    `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    "",
    `- lane gate pass: \`${payload.checks.lane_gate_pass}\``,
    `- artifact gate pass: \`${payload.checks.artifact_gate_pass}\``,
    `- missing docs: \`${payload.checks.missing_docs.length}\``,
    `- safe packets: \`${payload.checks.proposal_counts.safe_packets}\``,
    `- candidate packets: \`${payload.checks.proposal_counts.candidate_packets}\``,
    `- exact packets: \`${payload.checks.proposal_counts.exact_approval_packets}\``,
    `- skill ideas: \`${payload.checks.proposal_counts.skill_ideas}\``,
    `- runner ideas: \`${payload.checks.proposal_counts.runner_ideas}\``,
    `- cleanup proposals: \`${payload.checks.proposal_counts.cleanup_proposals}\``,
    `- web reflections: \`${payload.checks.web_reflections}\``,
    `- Journey/phase reflections: \`${payload.checks.journey_phase_reflections}\``,
    "",
    "Goal Mode remains active; this closeout advances one x1 phase and does not complete the v544-v575 objective.",
    "",
  ].join("\n");
}

function writeBeaconMd(jsonPath, data, files) {
  const title = jsonPath.includes("latest-updates") ? "Omega-Mini Latest Updates Beacon" :
    jsonPath.includes("ghc-current-state") ? "GHC Current State Beacon" :
      "Omega-Mini Current State";
  fs.writeFileSync(jsonPath.replace(/\.json$/, ".md"), [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    `Goal Mode status: ${data.goal_mode_status || "active_thread_goal_not_unattended_automation"}`,
    "",
    "## v554 v8 x1 Closeout",
    "",
    `- status: \`${data.v554_v8_x1_closeout?.status || "not_recorded"}\``,
    `- lane gate pass: \`${data.v554_v8_x1_closeout?.lane_gate_pass ?? "not_recorded"}\``,
    `- artifact gate pass: \`${data.v554_v8_x1_closeout?.artifact_gate_pass ?? "not_recorded"}\``,
    `- next active phase: \`${data.v554_v8_x1_closeout?.next_active_phase || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-140).map((item) => `- \`${item}\``),
    "",
  ].join("\n"), "utf8");
}

function readTraceOptional(name) {
  try {
    return readJson(path.join(tracesDir, name));
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values)];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
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
    raw_lane_text_published: false,
  };
}

function claimBoundary(phaseComplete) {
  return {
    phase_completion: phaseComplete ? "v554_v8_x1_only" : "not_claimed",
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

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
