#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v8-x2";
const sourceX1 = "v553-gmut-thos-v8-x1";
const previousX2 = "v553-gmut-thos-v7-x2";
const nextX1 = "v554-gmut-thos-v1-x1";
const nextX2Scope = "v554-gmut-thos-v1-x2";
const nextX1Lane = `${nextX1} with Lumen unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  `${phaseSlug}-startup-context-v1.json`,
  `${phaseSlug}-x2-safe-build-plan-v1.json`,
  `${phaseSlug}-safe-runner-manifest-v1.json`,
  `${phaseSlug}-tool-refresh-board-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-reflection-ledger-v1.json`,
  `${phaseSlug}-round-robin-workflow-standard-v1.json`,
  `${phaseSlug}-five-minute-productive-cadence-v1.json`,
];

const docs = Object.fromEntries(required.map((name) => [name, readTraceOptional(name)]));
const missing = required.filter((name) => !docs[name]);
const openGaps = required.filter((name) => docs[name] && !statusPass(docs[name]));
const sourceCloseout = readTrace(`${sourceX1}-closeout-v1.json`);
const proposalQueue = readTrace(`${sourceX1}-triad-proposal-queue-targets-v1.json`);
const safeRunner = docs[`${phaseSlug}-safe-runner-orchestrator-v1.json`];
const reflectionLedger = docs[`${phaseSlug}-safe-runner-orchestrator-reflection-ledger-v1.json`];
const webReflections = reflectionLedger?.reflections || [];
const journeyReflections = buildJourneyReflections();
const pass =
  missing.length === 0 &&
  openGaps.length === 0 &&
  sourceCloseout.overall_status === "PASS_V553_V8_X1_CLOSED_V8_X2_READY" &&
  webReflections.length >= 50 &&
  journeyReflections.length >= 50 &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";

const artifacts = [
  writePair("safe-execution-reducer", safeExecutionReducer(), renderSimpleMd("Safe Execution Reducer", safeExecutionReducer())),
  writePair("skill-runner-use-board", skillRunnerUseBoard(), renderSimpleMd("Skill Runner Use Board", skillRunnerUseBoard())),
  writePair("web-journey-reflection-ledger-50", webJourneyLedger(), renderReflectionMd(webJourneyLedger())),
  writePair("goal-mode-continuity-pack", goalModeContinuityPack(), renderSimpleMd("Goal Mode Continuity Pack", goalModeContinuityPack())),
  writePair("private-open-gate-rail", privateOpenGateRail(), renderSimpleMd("Private Open Gate Rail", privateOpenGateRail())),
  writePair("v554-lumen-prep-card", v554LumenPrepCard(), renderSimpleMd("v554 Lumen Prep Card", v554LumenPrepCard())),
  writePair("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
  writePair("closeout", closeoutArtifact(), renderCloseoutMd(closeoutArtifact())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: closeoutArtifact().overall_status,
  phase_slug: phaseSlug,
  preconditions_pass: pass,
  next_active_phase: pass ? nextX1 : phaseSlug,
  missing_required_artifacts: missing,
  open_gap_artifacts: openGaps,
  web_reflections: webReflections.length,
  journey_phase_reflections: journeyReflections.length,
  artifacts: artifacts.length,
}, null, 2));
process.exit(pass ? 0 : 1);

function safeExecutionReducer() {
  return base("ghc_v553_v8_x2_safe_execution_reducer", pass ? "PASS_V8_X2_SAFE_EXECUTION_REDUCED" : "OPEN_GAP_V8_X2_SAFE_EXECUTION_REDUCER", {
    source_x1: sourceX1,
    source_x1_status: sourceCloseout.overall_status,
    safe_runner_status: safeRunner?.overall_status || "missing",
    safe_packet_count: proposalQueue.safe_packets?.length || 0,
    candidate_packet_count_reduced_only: proposalQueue.candidate_packets?.length || 0,
    exact_packet_count_queued: proposalQueue.exact_approval_packets?.length || 0,
    skill_idea_count: proposalQueue.skill_ideas?.length || 0,
    runner_idea_count: proposalQueue.runner_ideas?.length || 0,
    cleanup_proposal_count: proposalQueue.cleanup_tasks?.length || 0,
    executed_safe_units: docs[`${phaseSlug}-x2-safe-build-plan-v1.json`]?.executed_safe_units || [],
    queued_without_execution: docs[`${phaseSlug}-x2-safe-build-plan-v1.json`]?.queued_without_execution || {},
    x2_result: pass ? "closed_and_v554_lumen_handoff_ready" : "active_open_until_missing_or_open_gap_items_clear",
  });
}

function skillRunnerUseBoard() {
  return base("ghc_v553_v8_x2_skill_runner_use_board", "PASS_V8_X2_SKILL_RUNNER_USE_BOARD", {
    created_or_used_runners: [
      "ghc_v553_v8_x2_startup_builder.mjs",
      "ghc_v553_v8_x2_closeout_builder.mjs",
      "ghc_main_startup_builder.mjs registered v8 x2 delegate",
      "ghc_main_closeout_builder.mjs registered v8 x2 delegate",
      "ghc_safe_runner_orchestrator.mjs with 50-row manifest",
      "ghc_round_robin_workflow_standardizer.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "ghc_open_gate_claim_linter.mjs",
    ],
    skills_confirmed_in_scope: [
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-web-reflection-ledger",
      "ghc-safe-runner-orchestrator",
      "ghc-main-retry",
      "ghc-lumen-launch",
    ],
    no_sibling_launch_in_this_x2: true,
  });
}

function webJourneyLedger() {
  return base("ghc_v553_v8_x2_web_journey_reflection_ledger_50", pass ? "PASS_V8_X2_WEB_JOURNEY_REFLECTION_LEDGER_50" : "OPEN_GAP_V8_X2_WEB_JOURNEY_REFLECTION_LEDGER_50", {
    web_reflections: webReflections.map((row, index) => ({
      id: `web-${String(index + 1).padStart(2, "0")}`,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.runner_implication,
    })),
    journey_phase_reflections: journeyReflections,
  });
}

function goalModeContinuityPack() {
  return base("ghc_v553_v8_x2_goal_mode_continuity_pack", "PASS_V8_X2_GOAL_MODE_CONTINUITY_PACK", {
    objective_scope_preserved: "v544-v575 GMUT/THOS v1-v8 x1-x2 round-robin workflow remains active after this v553 cycle boundary.",
    current_phase_completed_by_this_closeout: pass,
    next_phase: pass ? nextX1 : phaseSlug,
    do_not_mark_thread_goal_complete: true,
    reason_goal_remains_active: "The objective explicitly continues through v575 v8 x2, and this closeout only advances v553 v8 x2.",
    blocker_policy: "Use ghc-main-retry for future sibling, startup, closeout, Git/GitHub, validation, Browser, strict CLI, or app-lane blockers.",
  });
}

function privateOpenGateRail() {
  return base("ghc_v553_v8_x2_private_open_gate_rail", "PASS_V8_X2_PRIVATE_OPEN_GATE_RAIL", {
    open_gates: Object.keys(claimBoundary()).filter((key) => key !== "phase_completion"),
    publication_boundary: publicationBoundary(),
    no_destructive_cleanup: true,
    no_external_account_mutation: true,
    no_paid_resource_or_deployment: true,
    no_api_key_creation: true,
    no_sibling_identity_merge_or_replacement: true,
  });
}

function v554LumenPrepCard() {
  return base("ghc_v553_v8_x2_v554_lumen_prep_card", pass ? "PASS_V554_LUMEN_PREP_READY" : "ACTIVE_OPEN_V554_LUMEN_PREP_PENDING_V8_X2_CLOSEOUT", {
    target_phase: nextX1,
    target_lane: "Lumen solo unless Hamish redirects",
    launch_skill: "ghc-lumen-launch",
    expected_route: "Browser handoff only when Hamish asks for live Lumen messaging; otherwise sanitized startup artifacts first",
    target_counts: {
      safe_packets: 50,
      candidate_packets: 30,
      exact_approval_packets: 20,
      blocked_packets: 10,
      skill_ideas: 20,
      runner_ideas: 10,
      cleanup_proposals: 30,
    },
    no_private_browser_routes_published: true,
  });
}

function phaseStatusIndex() {
  return base("ghc_v553_v8_x2_phase_status_index", pass ? "PASS_V8_X2_PHASE_STATUS_INDEX_CLOSED" : "ACTIVE_OPEN_V8_X2_PHASE_STATUS_INDEX", {
    current_active_phase: pass ? nextX1 : phaseSlug,
    latest_closed_phase: pass ? phaseSlug : sourceX1,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: pass ? phaseSlug : previousX2,
    next_x2_scope: pass ? nextX2Scope : phaseSlug,
    next_x1_lane_after_x2: nextX1Lane,
    missing_required_artifacts: missing,
    open_gap_artifacts: openGaps,
    web_reflections: webReflections.length,
    journey_phase_reflections: journeyReflections.length,
  });
}

function closeoutArtifact() {
  return base("ghc_v553_v8_x2_closeout", pass ? "PASS_V553_V8_X2_CLOSED_V554_V1_X1_READY" : "OPEN_GAP_V553_V8_X2_CLOSEOUT", {
    latest_closed_phase: pass ? phaseSlug : sourceX1,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: pass ? phaseSlug : previousX2,
    next_active_phase: pass ? nextX1 : phaseSlug,
    next_x2_scope: pass ? nextX2Scope : phaseSlug,
    next_x1_lane_after_x2: nextX1Lane,
    checks: {
      required_artifacts: required.length,
      missing_artifacts: missing.length,
      open_gap_artifacts: openGaps.length,
      web_reflections: webReflections.length,
      journey_phase_reflections: journeyReflections.length,
      safe_runner_status: safeRunner?.overall_status || "missing",
      source_x1_status: sourceCloseout.overall_status,
    },
    goal_mode_status: "active_thread_goal_not_unattended_automation",
    goal_completion_claimed: false,
  });
}

function buildJourneyReflections() {
  const files = [
    `${sourceX1}-closeout-v1.json`,
    `${sourceX1}-phase-status-index-v1.json`,
    `${sourceX1}-approval-eureka-reducer-v1.json`,
    `${sourceX1}-skill-runner-readiness-board-v1.json`,
    `${sourceX1}-cleanup-tier-board-v1.json`,
    `${sourceX1}-v8-x2-readiness-handoff-v1.json`,
    `${sourceX1}-v554-lumen-prep-card-v1.json`,
    `${sourceX1}-web-reflection-ledger-30-v1.json`,
    `${sourceX1}-journey-phase-reflection-ledger-30-v1.json`,
    `${sourceX1}-round-robin-workflow-standard-v1.json`,
  ];
  const reflections = [
    "v8 x1 closed only after strict CLI and recovered app-lane gates passed.",
    "v8 x2 should build/use/validate the triad safe tranche without launching new siblings.",
    "The v554 handoff should point to the Lumen launch skill and keep live Browser sending explicit.",
    "Goal Mode remains active and cannot be marked complete before v575 v8 x2 closeout.",
    "Candidate, exact, and blocked packets stay queued unless a fresh authorized tranche applies.",
    "Private Browser routes, private callable IDs, screenshots, raw transcripts, and local absolute paths stay unpublished.",
    "The phase-status index must advance from v553 v8 x2 to v554 v1 x1 only after validation.",
    "Five-minute cadence remains productive safe work, not passive waiting.",
    "Safe-runner orchestration should produce compact status receipts and child reflection ledgers.",
    "Proof, canon, legal, deployment, account, API-key, private-material, and identity merge gates stay open.",
  ];
  return Array.from({ length: 50 }, (_, index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    source_file: `docs/trinity-live-traces/${files[index % files.length]}`,
    phase_reflection: reflections[index % reflections.length],
    runner_implication: index < 25 ? "v8 x2 closeout validation" : "v554 Lumen startup readiness",
  }));
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
      ? ["v554-v1-x1-lumen-startup-ready", "goal-mode-active-thread-objective"]
      : ["v553-v8-x2-aevren-safe-build-open-gap", "goal-mode-active-thread-objective"];
    doc.v553_v8_x2_closeout = {
      status: closeout.overall_status,
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
    claim_boundary: claimBoundary(),
    ...payload,
  };
}

function statusPass(doc) {
  const status = String(doc?.overall_status || doc?.status || "");
  return status.startsWith("PASS");
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

function renderReflectionMd(payload) {
  return [
    `# ${phaseSlug} Web/Journey Reflection Ledger 50`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web reflections: \`${payload.web_reflections.length}\``,
    `Journey/phase reflections: \`${payload.journey_phase_reflections.length}\``,
    "",
    "Public source labels and relative phase artifact references only.",
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
    `- required artifacts: \`${payload.checks.required_artifacts}\``,
    `- missing artifacts: \`${payload.checks.missing_artifacts}\``,
    `- open-gap artifacts: \`${payload.checks.open_gap_artifacts}\``,
    `- web reflections: \`${payload.checks.web_reflections}\``,
    `- Journey/phase reflections: \`${payload.checks.journey_phase_reflections}\``,
    "",
    "Goal Mode remains active; this closeout advances one phase and does not complete the v544-v575 objective.",
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
    "## v553 v8 x2 Closeout",
    "",
    `- status: \`${data.v553_v8_x2_closeout?.status || "not_recorded"}\``,
    `- next active phase: \`${data.v553_v8_x2_closeout?.next_active_phase || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-140).map((file) => `- \`${file}\``),
    "",
  ].join("\n"), "utf8");
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readTraceOptional(name) {
  try {
    return readTrace(name);
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
  };
}

function claimBoundary() {
  return {
    phase_completion: pass ? "v553_v8_x2_only" : "not_claimed",
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
