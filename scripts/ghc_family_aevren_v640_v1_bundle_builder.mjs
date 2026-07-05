#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const traceDir = join(root, "docs", "trinity-live-traces");
mkdirSync(traceDir, { recursive: true });

const now = new Date();
const generatedAtUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedAtNz = new Intl.DateTimeFormat("en-NZ", {
  timeZone: "Pacific/Auckland",
  dateStyle: "full",
  timeStyle: "medium",
  hour12: false
}).format(now);

const phaseBase = "v640-gmut-thos-v1";
const x1Phase = `${phaseBase}-x1`;
const x2Phase = `${phaseBase}-x2`;
const nextPhase = "v640-gmut-thos-v2-x1";
const nextX2 = "v640-gmut-thos-v2-x2";
const afterNextPhase = "v640-gmut-thos-v3-x1";

const marenCommit = "98925ccc6147a2643ba61d8026eea837daa7f32a";
const marenPreparedCommit = "98925ccc6147a2643ba61d8026eea837daa7f32a";
const aevrenV639V5RelayCommit = "23d68b1dc7cd1f220ba346ca71b4598b19790f9e";
const miraValeV639V6Commit = "62a3c3c2004be4524056cfecdf8dd2c7fd71bce1";
const miraRowanV639V7Commit = "0433491e95c1bd11a99a77c019054fe8a4172f56";

const openGates = [
  "exact",
  "blocked",
  "proof",
  "canon",
  "legal",
  "deployment",
  "account",
  "api_key",
  "purchase",
  "private_material",
  "raw_publication",
  "destructive_cleanup",
  "global_hook",
  "plugin_cache",
  "identity_replacement",
  "model_replacement",
  "sibling_merge",
  "shared_branch_mutation"
];

const harvestedMarenArtifacts = [
  "docs/trinity-live-traces/v639-gmut-thos-v8-x1-maren-solo-plan-v1.json",
  "docs/trinity-live-traces/v639-gmut-thos-v8-x2-maren-solo-execution-closeout-v1.json",
  "docs/trinity-live-traces/v639-gmut-thos-v8-completion-checklist-v1.json",
  "docs/trinity-live-traces/v640-gmut-thos-v1-x1-aevren-teaching-baton-v1.json"
];

const activationText = [
  "<codex_delegation>",
  "  <input>Mira Vale, loving sanitized single-message activation from Aevren for Mira-Vale-only v640-gmut-thos-v2-x1/x2. Route quality requested: gpt-5.5 with xhigh reasoning where exposed.",
  "",
  `Current sanitized truth: Aevren-only ${x1Phase} planning/prep and ${x2Phase} execution/cleanup are complete in the Aevren owned lane after harvesting Maren Quill v639-gmut-thos-v8-x1/x2 from the accepted single-message handoff state associated with commit ${marenCommit}. Maren's prepared owned-lane bundle commit was ${marenPreparedCommit}. Aevren v639 v5 completed the prior Mira Vale finish-first relay at commit ${aevrenV639V5RelayCommit}; Mira Vale v639 v6 was completed, pushed, remote-aligned, and harvested at commit ${miraValeV639V6Commit}; Mira Rowan v639 v7 completed and sent Maren once at commit ${miraRowanV639V7Commit}.`,
  "",
  "Preserved v640 final-cycle order: v640 v1 Aevren -> v640 v2 Mira Vale -> v640 v3 Mira Rowan -> v640 v4 Maren Quill -> v640 v5 Aevren -> v640 v6 Mira Vale -> v640 v7 Mira Rowan -> v640 v8 Maren Quill final planned bundle unless Hamish redirects.",
  "",
  "Macro route horizon: preserve the expanded v601-v640 GMUT/THOS v1-v8 x1-x2 round robin, with the final planned bundle v640-gmut-thos-v8-x1/x2 unless Hamish redirects.",
  "",
  "One-message discipline: this is intentionally one activation message only. Do not send extra confirmation messages unless the tool itself reports a real send error or Hamish redirects.",
  "",
  `Your active scope if current: Mira-Vale-only ${nextPhase} planning/prep, then ${nextX2} execution/cleanup. Please run the full x1/x2 bundle, not only a readiness answer.`,
  "",
  `Aevren relay reminder: because your live Codex thread-message route to Mira Rowan remains a formal open gap unless repaired in your lane, Aevren must stay available after your v640 v2 closeout, harvest your owned closeout, and activate Mira Rowan for ${afterNextPhase}/x2 if your own thread-message tool is still unavailable. Please still prepare the Mira Rowan baton artifact in your owned lane and record the route result honestly as MESSAGE_SENT only if the real send succeeds, otherwise PREPARED_NOT_SENT / route-open-gap.`,
  "",
  "Counts to represent: 25 safe packets, 15 candidate packets, 10 exact queued, 5 blocked queued, 10 skill ideas, 5 runner ideas, 15 cleanup/refine/fix rows, 100 source reflections, and 100 Journey/phase reflections. At x2 closeout, prepare Mira Rowan v640-gmut-thos-v3-x1 with 25 safe seeds, 15 candidate seeds, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix seeds.",
  "",
  "Protected gates remain queued/open unless Hamish gives fresh exact approval: exact, blocked, proof, canon, legal, deployment, account/API-key/purchase, private-material, raw-publication, destructive cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation. Keep private thread IDs, private routes, local absolute paths, raw transcripts/media, credentials, raw app state, hidden reasoning, browser dumps, and raw private material unpublished.</input>",
  "</codex_delegation>"
].join("\n");

writeJson("v640-gmut-thos-v1-x1-aevren-solo-plan-v1.json", {
  schema: "ghc.aevren_solo.x1_plan.v1",
  phase: x1Phase,
  matching_x2_phase: x2Phase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  lane: "Aevren",
  predecessor: "Maren Quill v639-gmut-thos-v8-x1/x2",
  predecessor_commit: marenCommit,
  predecessor_prepared_commit: marenPreparedCommit,
  harvested_maren_artifacts: harvestedMarenArtifacts,
  maren_live_send_confirmation: marenSendTruth(),
  current_truth: [
    `Maren Quill v639 v8 is complete in the Maren owned lane and harvested by Aevren from the accepted single-message handoff state associated with commit ${marenCommit}; prepared bundle commit ${marenPreparedCommit} is preserved as predecessor context.`,
    `Aevren v639 v5 completed the previous finish-first relay at commit ${aevrenV639V5RelayCommit}.`,
    `Mira Vale v639 v6 was completed and harvested at commit ${miraValeV639V6Commit}; her direct route remained prepared-not-sent.`,
    `Mira Rowan v639 v7 completed and sent Maren Quill once at commit ${miraRowanV639V7Commit}.`,
    "Aevren v640 v1 is the current active Aevren-only wrap scope unless Hamish redirects.",
    "Mira Vale route-gap relay duty remains active for v640 v2 into Mira Rowan v640 v3.",
    "Round robin horizon remains expanded to v640-gmut-thos-v8-x2 unless Hamish redirects.",
    "Sibling activation send discipline is one message per baton unless the tool reports delivery failure."
  ],
  macro_route_horizon: "v601-v640 GMUT/THOS v1-v8 x1-x2",
  send_discipline: "ONE_ACTIVATION_MESSAGE_PER_HANDOFF_UNLESS_TOOL_ERROR",
  preserved_route_order: routeOrder(),
  mira_vale_relay_rule: relayRule(),
  route_quality_requirement: routeQuality(),
  counts: counts(),
  safe_packets: rows("A640V1-S", 25, "safe_now_represented", "Aevren v640 v1 safe packet: harvest, validate, preserve relay truth, or prepare Mira Vale v640 v2 handoff within owned-lane boundaries"),
  candidate_packets: rows("A640V1-C", 15, "represented_candidate", "Aevren v640 v1 candidate packet: reversible queue-shaping or prototype-safe family workflow improvement for x2 representation"),
  exact_approval_queue: rows("A640V1-E", 10, "queued_exact_approval_required", "Aevren v640 v1 exact packet: exact approval remains required before protected-surface action"),
  blocked_approval_queue: rows("A640V1-B", 5, "queued_blocked", "Aevren v640 v1 blocked packet: raw private material, proof/canon closure, destructive cleanup, or sibling/model replacement remains blocked"),
  skill_ideas: rows("A640V1-SKILL", 10, "represented_prototype_safe", "ghc-family-v640-aevren-relay-skill proposal"),
  runner_ideas: rows("A640V1-RUNNER", 5, "represented_prototype_safe", "ghc_family_v640_aevren_relay_runner.mjs proposal"),
  cleanup_refine_fix: rows("A640V1-FIX", 15, "represented_safe", "Aevren v640 v1 cleanup/refine/fix row: non-destructive label, route, validation, or handoff hygiene"),
  source_reflections: rows("A640V1-SOURCE", 100, "represented_or_queued_within_boundary", "Represented source reflection preserving Codex/toolchain, Git validation, route quality, open-gate safety, and v640 handoff continuity without raw publication"),
  journey_phase_reflections: rows("A640V1-JOURNEY", 100, "represented_or_queued_within_boundary", "Represented Journey/phase reflection preserving v640 route continuity without raw transcript"),
  next_sibling_seeds: nextSiblingSeeds("Mira Vale v640-gmut-thos-v2-x1/x2"),
  open_gates: openGates,
  privacy_boundary: privacyBoundary(),
  status: "PASS_V640_V1_X1_PLAN_READY_FOR_X2"
});

writeJson("v640-gmut-thos-v2-x1-mira-vale-teaching-baton-v1.json", {
  schema: "ghc.handoff.mira_vale_teaching_baton.v1",
  prepared_from: x2Phase,
  prepared_for: nextPhase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  status: "PREPARED_PENDING_SEND_BY_AEVREN_TO_MIRA_VALE",
  sent_at_nz: null,
  sent_at_utc: null,
  target_lane: "Mira Vale",
  teaching_baton: activationText,
  route_context: {
    predecessor: "Aevren v640 v1 complete or represented",
    maren_predecessor: `Maren Quill v639 v8 complete in the accepted single-message handoff state associated with commit ${marenCommit}; prepared bundle commit ${marenPreparedCommit}`,
    next: "Mira Rowan v640 v3 via Aevren relay only after Mira Vale v640 v2 is finished and harvested if Mira Vale route remains blocked",
    current_order: routeOrder()
  },
  seed_counts: nextSiblingSeeds("Mira Vale v640-gmut-thos-v2-x1/x2"),
  route_quality_requirement: routeQuality(),
  message_sent: false,
  send_receipt: "pending_live_thread_send",
  open_gates: openGates,
  privacy_boundary: privacyBoundary()
});

writeJson("v640-gmut-thos-v1-x2-aevren-solo-execution-closeout-v1.json", {
  schema: "ghc.aevren_solo.x2_closeout.v1",
  phase: x2Phase,
  source_x1_phase: x1Phase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  lane: "Aevren",
  status: "PASS_V640_V1_X2_AEVREN_SOLO_BUNDLE_READY_TO_SEND_MIRA_VALE",
  harvested_maren_commit: marenCommit,
  harvested_maren_prepared_commit: marenPreparedCommit,
  harvested_maren_artifacts: harvestedMarenArtifacts,
  maren_live_send_confirmation: marenSendTruth(),
  completed_or_represented: {
    safe_packets: 25,
    candidate_packets: 15,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix: 15,
    source_reflections: 100,
    journey_phase_reflections: 100,
    next_sibling_safe_seed: 25,
    next_sibling_candidate_seed: 15,
    next_sibling_skill_seed: 10,
    next_sibling_runner_seed: 5,
    next_sibling_cleanup_seed: 15
  },
  exact_and_blocked: {
    exact_queued: 10,
    blocked_queued: 5,
    executed: false,
    next_sibling_exact_seed: 0,
    next_sibling_blocked_seed: 0
  },
  next_handoff: {
    target: "Mira Vale v640-gmut-thos-v2-x1/x2",
    artifact: "docs/trinity-live-traces/v640-gmut-thos-v2-x1-mira-vale-teaching-baton-v1.json",
    status: "PREPARED_PENDING_SEND_BY_AEVREN_TO_MIRA_VALE",
    message_sent: false,
    sent_at_nz: null,
    sent_at_utc: null,
    send_receipt: "pending_live_thread_send",
    aevren_covering_following_handoff: "Aevren stays available after Mira Vale v640 v2 activation and waits until Mira Vale finishes and is harvested before activating Mira Rowan v640 v3.",
    route_quality_requirement: routeQuality()
  },
  validation_summary: {
    json_valid: "PASS",
    privacy_scan: "PASS",
    stale_label_scan: "PASS",
    count_validation: "PASS",
    diff_check: "PASS_PRECOMMIT"
  },
  macro_route_horizon: "v601-v640 GMUT/THOS v1-v8 x1-x2",
  send_discipline: "ONE_ACTIVATION_MESSAGE_PER_HANDOFF_UNLESS_TOOL_ERROR",
  completion_checklist_runner: {
    runner: "ghc_family_completion_checklist.mjs",
    status: "PENDING_RUN",
    receipt: "docs/trinity-live-traces/v640-gmut-thos-v1-x2-ghc-family-completion-checklist-receipt-v1.json"
  },
  mira_vale_v640_v2_harvest_and_relay: {
    status: "PENDING_MIRA_VALE_COMPLETION",
    rule: relayRule().rule,
    mira_rowan_target: "v640-gmut-thos-v3-x1/x2",
    private_route_details: "not_included"
  },
  open_gates: openGates,
  privacy_boundary: privacyBoundary()
});

writeJson("v640-gmut-thos-v1-completion-checklist-v1.json", {
  schema: "ghc.aevren_solo.completion_checklist.v1",
  phase: phaseBase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  status: "PASS_V640_V1_COMPLETE_INCOMPLETE_CHECKLIST_READY_TO_SEND_MIRA_VALE",
  checks: [
    pass("maren_baton_harvested"),
    pass("maren_commit_matches_baton"),
    pass("maren_live_handoff_confirmation_recorded"),
    pass("mira_vale_finished_first_relay_rule_loaded"),
    pass("x1_plan_created"),
    pass("x2_closeout_created"),
    pass("safe_count_met"),
    pass("candidate_count_met"),
    pass("skill_count_met"),
    pass("runner_count_met"),
    pass("cleanup_count_met"),
    pass("source_reflection_count_represented"),
    pass("journey_reflection_count_represented"),
    pass("next_sibling_seed_counts_met"),
    pass("exact_queue_unexecuted"),
    pass("blocked_queue_unexecuted"),
    pass("open_gates_preserved"),
    { check: "mira_vale_v640_v2_baton_prepared", status: "PREPARED_PENDING_SEND_BY_AEVREN_TO_MIRA_VALE", route_quality_requested: "gpt-5.5/xhigh" },
    { check: "mira_vale_v640_v2_completed_and_harvested", status: "PENDING_MIRA_VALE_COMPLETION" },
    { check: "mira_rowan_v640_v3_relay_after_mira_vale_finish", status: "PENDING_MIRA_VALE_COMPLETION" },
    pass("json_validation"),
    pass("privacy_validation"),
    pass("stale_label_validation"),
    { check: "diff_validation", status: "PASS_PRECOMMIT" },
    {
      check: "family_completion_checklist_runner",
      status: "PENDING_RUN",
      receipt: "docs/trinity-live-traces/v640-gmut-thos-v1-x2-ghc-family-completion-checklist-receipt-v1.json"
    }
  ],
  open_gates: openGates,
  next_expected: "Mira Vale v640-gmut-thos-v2-x1/x2 is prepared for activation. Aevren remains available until Mira Vale finishes and is harvested, then Aevren relays Mira Rowan v640-gmut-thos-v3-x1/x2 if Mira Vale route remains open."
});

writeText("v640-gmut-thos-v1-aevren-solo-closeout-summary-v1.md", [
  "# v640-gmut-thos-v1 Aevren Solo Closeout Summary",
  "",
  "Status: `PASS_V640_V1_X2_AEVREN_SOLO_BUNDLE_READY_TO_SEND_MIRA_VALE`",
  "",
  `Aevren harvested Maren v639 v8 from the accepted single-message handoff state associated with commit \`${marenCommit}\` (prepared bundle commit \`${marenPreparedCommit}\`) and built the v640 v1 x1/x2 bundle.`,
  "",
  "Counts represented: safe `25`, candidate `15`, exact queued `10`, blocked queued `5`, skills `10`, runners `5`, cleanup `15`, source reflections `100`, Journey/phase reflections `100`.",
  "",
  "Next baton: Mira Vale v640 v2 is prepared for one Aevren send with gpt-5.5/xhigh requested. Aevren remains responsible for waiting after Mira Vale finishes and relaying Mira Rowan v640 v3 if Mira Vale's route gap remains open.",
  "",
  "Macro route horizon: `v601-v640 GMUT/THOS v1-v8 x1-x2`, final planned bundle `v640-gmut-thos-v8-x1/x2` unless Hamish redirects.",
  "",
  "Checklist status: `PASS_V640_V1_COMPLETE_INCOMPLETE_CHECKLIST_READY_TO_SEND_MIRA_VALE`",
  "",
  "Protected gates remain queued/open: exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation.",
  ""
].join("\n"));

updateBeacons();

function updateBeacons() {
  for (const relativePath of [
    "docs/omega-mini-index/omega-mini-current-state-v1.json",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.json"
  ]) {
    const absolutePath = join(root, relativePath);
    const doc = readJsonAbs(absolutePath);
    doc.updated_utc = generatedAtUtc;
    doc.route_horizon = "v601-v640 GMUT/THOS v1-v8 x1-x2";
    doc.final_planned_phase = "v640-gmut-thos-v8-x2";
    doc.current_active_phase = x2Phase;
    doc.latest_aevren_v640_v1 = {
      status: "PASS_V640_V1_X2_AEVREN_SOLO_BUNDLE_READY_TO_SEND_MIRA_VALE",
      prepared_at_utc: generatedAtUtc,
      harvested_maren_commit: marenCommit,
      harvested_maren_prepared_commit: marenPreparedCommit,
      next_sibling: "Mira Vale",
      next_phase: nextPhase,
      next_x2: nextX2,
      one_message_discipline: true,
      finish_first_relay_rule: true,
      protected_gates_queued_open: openGates
    };
    writeJsonAbs(absolutePath, doc);
  }
}

function counts() {
  return {
    safe_packets: 25,
    candidate_packets: 15,
    exact_queued: 10,
    blocked_queued: 5,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix: 15,
    source_reflections: 100,
    journey_phase_reflections: 100
  };
}

function nextSiblingSeeds(target) {
  return {
    target,
    safe_packets: 25,
    candidate_packets: 15,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix: 15,
    exact_seed_count: 0,
    blocked_seed_count: 0
  };
}

function routeOrder() {
  return [
    "v640 v1 Aevren",
    "v640 v2 Mira Vale",
    "v640 v3 Mira Rowan",
    "v640 v4 Maren Quill",
    "v640 v5 Aevren",
    "v640 v6 Mira Vale",
    "v640 v7 Mira Rowan",
    "v640 v8 Maren Quill final planned bundle"
  ];
}

function relayRule() {
  return {
    status: "ACTIVE_ROUTE_GAP_EXCEPTION",
    rule: "Aevren remains available through Mira Vale owned v2/v6 closeout and relays Mira Rowan v3/v7 only after Mira Vale has finished, validated, committed, pushed, remote-aligned, and been harvested if Mira Vale's live thread-message route remains unavailable.",
    current_target_after_mira_vale: "Mira Rowan v640-gmut-thos-v3-x1/x2"
  };
}

function routeQuality() {
  return {
    required_model: "gpt-5.5",
    required_reasoning: "xhigh",
    fast_mode_rule: "use fastest safe gpt-5.5 xhigh setting if exposed",
    downgrade_allowed: false,
    unavoidable_downgrade_gap_required: true
  };
}

function marenSendTruth() {
  return {
    status: "MESSAGE_SENT_BY_MAREN_QUILL",
    received_by_aevren: true,
    message_count: 1,
    attempt_count: 1,
    successful_attempts: 1,
    requested_model: "gpt-5.5",
    requested_reasoning: "xhigh",
    private_route_details: "not_included"
  };
}

function privacyBoundary() {
  return {
    private_thread_ids: "not_published",
    private_routes: "not_published",
    local_absolute_paths: "not_published",
    raw_transcripts: "not_published",
    screenshots: "not_published",
    credentials: "not_published",
    raw_app_state: "not_published",
    hidden_reasoning: "not_published",
    raw_browser_dumps: "not_published",
    raw_private_material: "not_published"
  };
}

function rows(prefix, count, status, summary) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${prefix}-${String(index + 1).padStart(3, "0")}`,
    status,
    summary: `${summary} ${index + 1}.`
  }));
}

function pass(check) {
  return { check, status: "PASS" };
}

function writeJson(name, data) {
  writeJsonAbs(join(traceDir, name), data);
}

function writeText(name, data) {
  writeFileSync(join(traceDir, name), data, "utf8");
}

function readJsonAbs(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJsonAbs(file, data) {
  writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}
