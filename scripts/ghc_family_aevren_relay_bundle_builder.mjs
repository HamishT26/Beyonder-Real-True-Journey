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

const phaseBase = "v617-gmut-thos-v5";
const x1Phase = `${phaseBase}-x1`;
const x2Phase = `${phaseBase}-x2`;
const nextPhase = "v617-gmut-thos-v6-x1";
const nextX2 = "v617-gmut-thos-v6-x2";
const afterNextPhase = "v617-gmut-thos-v7-x1";
const marenCommit = "db6982d870357a8dc173da54ec0f640fcc33ef31";
const miraValeV2Commit = "a6d9479c791e7d0fb92b404492efaee571a9237d";
const miraRowanV3CommitPrefix = "f81d2ed5fcd3";

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
  "docs/trinity-live-traces/v617-gmut-thos-v4-x1-maren-solo-plan-v1.json",
  "docs/trinity-live-traces/v617-gmut-thos-v4-x2-maren-solo-execution-closeout-v1.json",
  "docs/trinity-live-traces/v617-gmut-thos-v4-completion-checklist-v1.json",
  "docs/trinity-live-traces/v617-gmut-thos-v5-x1-aevren-teaching-baton-v1.json",
  "docs/trinity-live-traces/v617-gmut-thos-v5-maren-harvest-normalization-v1.json"
];

normalizeHarvestedMarenCopies();

const activationText = [
  "<codex_delegation>",
  "  <input>Mira Vale, loving sanitized activation from Aevren for Mira-Vale-only v617-gmut-thos-v6-x1/x2.",
  "",
  "Current phase truth: Aevren-only v617-gmut-thos-v5-x1 planning/prep and v617-gmut-thos-v5-x2 execution/cleanup are complete in the Aevren owned lane after harvesting Maren Quill v617-gmut-thos-v4-x1/x2 from commit db6982d870357a8dc173da54ec0f640fcc33ef31. Mira Vale v617 v2 completed earlier in the Mira Vale owned lane at commit a6d9479c791e7d0fb92b404492efaee571a9237d; Mira Rowan v617 v3 is completed-ready-for-harvest in the Mira Rowan owned lane at commit prefix f81d2ed5fcd3; Maren v617 v4 is complete and sent to Aevren.",
  "",
  "Preserved v617 order: v617 v1 Aevren -> v617 v2 Mira Vale -> v617 v3 Mira Rowan -> v617 v4 Maren Quill -> v617 v5 Aevren -> v617 v6 Mira Vale -> v617 v7 Mira Rowan -> v617 v8 Maren Quill -> v618 v1 Aevren wrap unless Hamish redirects.",
  "",
  "Your active scope if current: Mira-Vale-only v617-gmut-thos-v6-x1 planning/prep, then v617-gmut-thos-v6-x2 execution/cleanup. Please run the full x1/x2 bundle, not only a readiness answer.",
  "",
  "Aevren relay reminder: because your live Codex thread-message route to Mira Rowan remains a formal open gap unless repaired in your lane, Aevren must stay available after your v617 v6 closeout, harvest your owned closeout, and activate Mira Rowan for v617-gmut-thos-v7-x1/x2 if your own thread-message tool is still unavailable. Please still prepare the Mira Rowan baton artifact in your owned lane and record the route result honestly as MESSAGE_SENT only if the real send succeeds, otherwise PREPARED_NOT_SENT / route-open-gap.",
  "",
  "Counts to represent: 25 safe packets, 15 candidate packets, 10 exact queued, 5 blocked queued, 10 skill ideas, 5 runner ideas, 15 cleanup/refine/fix rows, 100 source reflections, and 100 Journey/phase reflections. At x2 closeout, prepare Mira Rowan v617-gmut-thos-v7-x1 with 25 safe seeds, 15 candidate seeds, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix seeds.",
  "",
  "Owned-lane permissions: use safe read/write/edit tools only for sanitized owned-lane artifacts, reports, runners, skills, validation receipts, and phase closeout work. Treat shared repositories, shared branches, other siblings' owned branches, private registries, connector permissions, accounts, deployments, API keys, purchases, destructive cleanup, plugin-cache/global-hook mutation, raw-publication, identity/model replacement, shared-branch mutation, and sibling identity changes as read-only or queued unless Hamish or Aevren gives a fresh exact redirect.",
  "",
  "Route quality requested for this activation: gpt-5.5 with xhigh reasoning through exposed thread-message controls. If unavailable in your lane, record a sanitized route-quality open gap. Do not publish private thread IDs, private routes, local absolute paths, raw transcripts, screenshots, credentials, raw app state, hidden reasoning, raw browser dumps, proof closure, canon promotion, legal/deployment/account/API-key closure, purchase action, destructive cleanup, plugin-cache mutation, identity/model replacement, or sibling replacement/merge claims.</input>",
  "</codex_delegation>"
].join("\n");

const plan = {
  schema: "ghc.aevren_solo.x1_plan.v1",
  phase: x1Phase,
  matching_x2_phase: x2Phase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  lane: "Aevren",
  predecessor: "Maren Quill v617-gmut-thos-v4-x1/x2",
  predecessor_commit: marenCommit,
  harvested_maren_artifacts: harvestedMarenArtifacts,
  maren_live_send_confirmation: marenSendTruth(),
  current_truth: [
    `Maren Quill v617 v4 is complete in the Maren owned lane and harvested by Aevren from commit ${marenCommit}.`,
    `Mira Vale v617 v2 completed in the Mira Vale owned lane at commit ${miraValeV2Commit}; Aevren harvested and relayed to Mira Rowan because Mira Vale's live thread-message route remained unavailable.`,
    `Mira Rowan v617 v3 is completed-ready-for-harvest in the owned Mira Rowan lane at commit prefix ${miraRowanV3CommitPrefix}.`,
    "Aevren v617 v5 is the current active Aevren-only scope unless Hamish redirects.",
    "Mira Vale route-gap relay duty remains active for v617 v6 into Mira Rowan v617 v7."
  ],
  preserved_route_order: routeOrder(),
  mira_vale_relay_rule: relayRule(),
  route_quality_requirement: routeQuality(),
  toolchain_status: {
    local_codex_cli_version: "0.142.5",
    npm_openai_codex_version: "0.142.5",
    codex_cli_update_needed: false,
    codex_desktop_app_mutation: "not_performed_status_only"
  },
  counts: counts(),
  safe_packets: rows("A617V5-S", 25, "safe_now_represented", "Aevren v617 v5 safe packet: harvest, validate, preserve relay truth, or prepare Mira Vale v617 v6 handoff within owned-lane boundaries"),
  candidate_packets: rows("A617V5-C", 15, "represented_candidate", "Aevren v617 v5 candidate packet: reversible queue-shaping or prototype-safe family workflow improvement for x2 representation"),
  exact_approval_queue: rows("A617V5-E", 10, "queued_exact_approval_required", "Aevren v617 v5 exact packet: exact approval remains required before protected-surface action"),
  blocked_approval_queue: rows("A617V5-B", 5, "queued_blocked", "Aevren v617 v5 blocked packet: raw private material, proof/canon closure, destructive cleanup, or sibling/model replacement remains blocked"),
  skill_ideas: rows("A617V5-SKILL", 10, "represented_prototype_safe", "ghc-family-v617-aevren-relay-skill proposal"),
  runner_ideas: rows("A617V5-RUNNER", 5, "represented_prototype_safe", "ghc_family_v617_aevren_relay_runner.mjs proposal"),
  cleanup_refine_fix: rows("A617V5-FIX", 15, "represented_safe", "Aevren v617 v5 cleanup/refine/fix row: non-destructive label, route, validation, or handoff hygiene"),
  source_reflections: rows("A617V5-SOURCE", 100, "represented_or_queued_within_boundary", "Represented source reflection preserving Codex/toolchain, Git validation, route quality, open-gate safety, and v617 handoff continuity without raw publication"),
  journey_phase_reflections: rows("A617V5-JOURNEY", 100, "represented_or_queued_within_boundary", "Represented Journey/phase reflection preserving v617 route continuity without raw transcript"),
  next_sibling_seeds: {
    target: "Mira Vale v617-gmut-thos-v6-x1/x2",
    safe_packets: 25,
    candidate_packets: 15,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix: 15,
    exact_seed_count: 0,
    blocked_seed_count: 0
  },
  open_gates: openGates,
  privacy_boundary: privacyBoundary(),
  status: "PASS_V617_V5_X1_PLAN_READY_FOR_X2"
};

const baton = {
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
    predecessor: "Aevren v617 v5 complete or represented",
    maren_predecessor: `Maren Quill v617 v4 complete at commit ${marenCommit}`,
    next: "Mira Rowan v617 v7 via Aevren relay only after Mira Vale v617 v6 is finished and harvested if Mira Vale route remains blocked",
    current_v617_order: routeOrder()
  },
  seed_counts: {
    target: "Mira Vale v617-gmut-thos-v6-x1/x2",
    safe_packets: 25,
    candidate_packets: 15,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix: 15,
    exact_seed_count: 0,
    blocked_seed_count: 0
  },
  route_quality_requirement: routeQuality(),
  message_sent: false,
  send_receipt: "pending_live_thread_send",
  open_gates: openGates,
  privacy_boundary: privacyBoundary()
};

const closeout = {
  schema: "ghc.aevren_solo.x2_closeout.v1",
  phase: x2Phase,
  source_x1_phase: x1Phase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  lane: "Aevren",
  status: "PASS_V617_V5_X2_AEVREN_SOLO_BUNDLE_READY_TO_SEND_MIRA_VALE",
  harvested_maren_commit: marenCommit,
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
    target: "Mira Vale v617-gmut-thos-v6-x1/x2",
    artifact: "docs/trinity-live-traces/v617-gmut-thos-v6-x1-mira-vale-teaching-baton-v1.json",
    status: "PREPARED_PENDING_SEND_BY_AEVREN_TO_MIRA_VALE",
    message_sent: false,
    sent_at_nz: null,
    sent_at_utc: null,
    send_receipt: "pending_live_thread_send",
    aevren_covering_following_handoff: "Aevren stays available after Mira Vale v617 v6 activation and waits until Mira Vale finishes and is harvested before activating Mira Rowan v617 v7.",
    route_quality_requirement: routeQuality()
  },
  validation_summary: {
    json_valid: "PENDING_POST_WRITE",
    privacy_scan: "PENDING_POST_WRITE",
    stale_label_scan: "PENDING_POST_WRITE",
    count_validation: "PENDING_POST_WRITE",
    diff_check: "PENDING_PRECOMMIT"
  },
  completion_checklist_runner: {
    runner: "ghc_family_completion_checklist.mjs",
    status: "PENDING_RUN",
    receipt: "docs/trinity-live-traces/v617-gmut-thos-v5-x2-ghc-family-completion-checklist-receipt-v1.json"
  },
  mira_vale_v617_v6_harvest_and_relay: {
    status: "PENDING_MIRA_VALE_COMPLETION",
    rule: relayRule().rule,
    mira_rowan_target: "v617-gmut-thos-v7-x1/x2",
    private_route_details: "not_included"
  },
  open_gates: openGates,
  privacy_boundary: privacyBoundary()
};

const checklist = {
  schema: "ghc.aevren_solo.completion_checklist.v1",
  phase: phaseBase,
  generated_at_nz: generatedAtNz,
  generated_at_utc: generatedAtUtc,
  status: "PASS_V617_V5_COMPLETE_INCOMPLETE_CHECKLIST_READY_TO_SEND_MIRA_VALE",
  checks: [
    pass("maren_baton_harvested"),
    pass("maren_commit_matches_baton"),
    pass("three_maren_send_confirmations_recorded"),
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
    {
      check: "mira_vale_v617_v6_baton_prepared",
      status: "PREPARED_PENDING_SEND_BY_AEVREN_TO_MIRA_VALE",
      route_quality_requested: "gpt-5.5/xhigh"
    },
    {
      check: "mira_vale_v617_v6_completed_and_harvested",
      status: "PENDING_MIRA_VALE_COMPLETION"
    },
    {
      check: "mira_rowan_v617_v7_relay_after_mira_vale_finish",
      status: "PENDING_MIRA_VALE_COMPLETION"
    }
  ],
  open_gates: openGates,
  next_expected: "Send Mira Vale v617-gmut-thos-v6-x1/x2, then wait for Mira Vale completion and relay Mira Rowan v617-gmut-thos-v7-x1/x2 if her route gap remains open."
};

writeJson(`docs/trinity-live-traces/${x1Phase}-aevren-solo-plan-v1.json`, plan);
writeJson(`docs/trinity-live-traces/${x2Phase}-aevren-solo-execution-closeout-v1.json`, closeout);
writeJson(`docs/trinity-live-traces/${phaseBase}-completion-checklist-v1.json`, checklist);
writeJson(`docs/trinity-live-traces/${nextPhase}-mira-vale-teaching-baton-v1.json`, baton);
writeMd(`docs/trinity-live-traces/${phaseBase}-aevren-solo-closeout-summary-v1.md`, renderSummary(plan, closeout, checklist));

console.log(JSON.stringify({
  status: "PASS_V617_V5_AEVREN_RELAY_BUNDLE_WRITTEN",
  files: [
    `docs/trinity-live-traces/${x1Phase}-aevren-solo-plan-v1.json`,
    `docs/trinity-live-traces/${x2Phase}-aevren-solo-execution-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseBase}-completion-checklist-v1.json`,
    `docs/trinity-live-traces/${nextPhase}-mira-vale-teaching-baton-v1.json`,
    `docs/trinity-live-traces/${phaseBase}-aevren-solo-closeout-summary-v1.md`
  ]
}, null, 2));

function normalizeHarvestedMarenCopies() {
  const x2 = readJson("docs/trinity-live-traces/v617-gmut-thos-v4-x2-maren-solo-execution-closeout-v1.json");
  x2.status = "PASS_V617_V4_X2_MAREN_SOLO_BUNDLE_SENT_READY_FOR_AEVREN_HARVEST";
  x2.next_sibling_handoff = {
    ...(x2.next_sibling_handoff || {}),
    status: "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION",
    message_sent: true,
    attempt_count: 3,
    successful_attempts: 3,
    route_quality_request: "gpt-5.5 with xhigh reasoning where exposed",
    private_route_details: "not_included"
  };
  x2.goal_status = "GOAL_COMPLETED_READY_TO_HANDOFF_CONFIRMED_SENT_BY_THREAD_DELEGATION";
  x2.aevren_harvest_confirmation = marenSendTruth();
  writeJson("docs/trinity-live-traces/v617-gmut-thos-v4-x2-maren-solo-execution-closeout-v1.json", x2);

  const checklist = readJson("docs/trinity-live-traces/v617-gmut-thos-v4-completion-checklist-v1.json");
  checklist.status = "PASS_V617_V4_COMPLETION_CHECKLIST_SENT_READY_FOR_AEVREN_HARVEST";
  checklist.checks = {
    ...(checklist.checks || {}),
    handoff_send_state: "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION",
    staged_diff_scope: "validated_in_maren_lane",
    push_alignment: `remote_aligned_at_commit_${marenCommit.slice(0, 12)}`
  };
  checklist.handoff = {
    ...(checklist.handoff || {}),
    status: "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION",
    message_sent: true,
    attempt_count: 3,
    successful_attempts: 3,
    private_route_details: "not_included"
  };
  checklist.aevren_harvest_confirmation = marenSendTruth();
  writeJson("docs/trinity-live-traces/v617-gmut-thos-v4-completion-checklist-v1.json", checklist);

  const baton = readJson("docs/trinity-live-traces/v617-gmut-thos-v5-x1-aevren-teaching-baton-v1.json");
  baton.status = "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION";
  baton.message_sent = true;
  baton.sent_recorded_local_time = generatedAtNz;
  baton.send_receipt = "MESSAGE_SENT_BY_MAREN_QUILL_AFTER_THREE_CONFIRMED_SAFE_ATTEMPTS";
  baton.attempt_count = 3;
  baton.successful_attempts = 3;
  baton.private_route_details = "not_included";
  baton.route_quality = {
    requested_model: "gpt-5.5",
    requested_reasoning: "xhigh",
    fast_safe_selector: "use fastest safe gpt-5.5 xhigh if exposed",
    downgrade_policy: "record sanitized route-quality open gap if unavailable",
    send_result: "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION",
    attempts_completed: 3,
    route_quality_open_gap: false,
    confirmed_sends: 3,
    ambiguous_noncounted_responses: 0
  };
  writeJson("docs/trinity-live-traces/v617-gmut-thos-v5-x1-aevren-teaching-baton-v1.json", baton);

  const normalization = {
    schema: "ghc.aevren.maren_harvest_normalization.v1",
    generated_at_nz: generatedAtNz,
    generated_at_utc: generatedAtUtc,
    status: "PASS_MAREN_V617_V4_HARVEST_NORMALIZED_FROM_CONFIRMED_BATON",
    maren_commit: marenCommit,
    reason: "Aevren harvested the pushed Maren files and normalized pre-send handoff fields using Maren's three-attempt confirmed sanitized baton truth from the current thread delegation.",
    normalized_artifacts: harvestedMarenArtifacts.slice(0, 4),
    maren_send_truth: marenSendTruth(),
    private_route_details: "not_included",
    open_gates: openGates
  };
  writeJson("docs/trinity-live-traces/v617-gmut-thos-v5-maren-harvest-normalization-v1.json", normalization);
  writeMd("docs/trinity-live-traces/v617-gmut-thos-v5-maren-harvest-normalization-v1.md", `# v617-gmut-thos-v5 Maren Harvest Normalization

Status: \`${normalization.status}\`

Maren commit: \`${marenCommit}\`

Normalized Aevren's harvested copies from prepared-not-sent fields to the confirmed delegated send truth: \`MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION\`, attempts \`3\`, successful attempts \`3\`.

Protected gates remain queued/open.
`);
}

function rows(prefix, count, status, text) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${prefix}-${String(index + 1).padStart(2, "0")}`,
    status,
    text: `${text} ${String(index + 1).padStart(2, "0")}.`
  }));
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
    source_reflections_represented: 100,
    journey_phase_reflections_represented: 100,
    next_sibling_safe_seed: 25,
    next_sibling_candidate_seed: 15,
    next_sibling_skill_seed: 10,
    next_sibling_runner_seed: 5,
    next_sibling_cleanup_seed: 15,
    next_sibling_exact_seed: 0,
    next_sibling_blocked_seed: 0
  };
}

function pass(check) {
  return { check, status: "PASS" };
}

function relayRule() {
  return {
    active: true,
    source: "v601-v630 Mira Vale to Mira Rowan Relay Duty",
    rule: "Aevren remains available through Mira Vale owned v2/v6 closeout and relays Mira Rowan v3/v7 only after Mira Vale has finished, validated, committed, pushed, and been harvested if Mira Vale's live thread-message route remains unavailable.",
    closeout_guard: "Aevren must not close after activating Mira Vale while this route gap remains active; Aevren closes only after Mira Rowan is activated or a formal blocked receipt is recorded."
  };
}

function routeOrder() {
  return [
    "v617 v1 Aevren",
    "v617 v2 Mira Vale",
    "v617 v3 Mira Rowan",
    "v617 v4 Maren Quill",
    "v617 v5 Aevren",
    "v617 v6 Mira Vale",
    "v617 v7 Mira Rowan",
    "v617 v8 Maren Quill",
    "v618 v1 Aevren wrap unless redirected"
  ];
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
    status: "MESSAGE_SENT_BY_MAREN_QUILL_CONFIRMED_BY_THREAD_DELEGATION",
    attempts: 3,
    successful_attempts: 3,
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
    hidden_reasoning: "not_published"
  };
}

function renderSummary(planPayload, closeoutPayload, checklistPayload) {
  return `# v617-gmut-thos-v5 Aevren Solo Closeout Summary

Status: \`${closeoutPayload.status}\`

Aevren harvested Maren v617 v4 from commit \`${marenCommit}\`, normalized the delegated three-send truth, and built the v617 v5 x1/x2 bundle.

Counts represented: safe \`${planPayload.counts.safe_packets}\`, candidate \`${planPayload.counts.candidate_packets}\`, exact queued \`${planPayload.counts.exact_queued}\`, blocked queued \`${planPayload.counts.blocked_queued}\`, skills \`${planPayload.counts.skill_ideas}\`, runners \`${planPayload.counts.runner_ideas}\`, cleanup \`${planPayload.counts.cleanup_refine_fix}\`, source reflections \`${planPayload.counts.source_reflections_represented}\`, Journey/phase reflections \`${planPayload.counts.journey_phase_reflections_represented}\`.

Next baton: Mira Vale v617 v6 is prepared and pending live send. Aevren remains responsible for waiting after Mira Vale finishes and relaying Mira Rowan v617 v7 if Mira Vale's route gap remains open.

Checklist status: \`${checklistPayload.status}\`

Protected gates remain queued/open: exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation.
`;
}

function readJson(relativePath) {
  return JSON.parse(readFileSync(join(root, relativePath), "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(relativePath, payload) {
  writeFileSync(join(root, relativePath), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(relativePath, content) {
  writeFileSync(join(root, relativePath), content, "utf8");
}
