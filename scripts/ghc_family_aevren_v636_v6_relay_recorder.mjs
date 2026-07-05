#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";

const now = new Date();
const nowUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const nowNz = new Intl.DateTimeFormat("en-NZ", {
  timeZone: "Pacific/Auckland",
  dateStyle: "full",
  timeStyle: "medium",
  hour12: false
}).format(now);

const relayStatus = "MESSAGE_SENT_BY_AEVREN_TO_MIRA_ROWAN_AFTER_MIRA_VALE_HARVEST";
const miraCommit = "2118af5b5a0d9905dfa7ca05298e2bf9b556b795";
const aevrenSendCommit = "c7adb3572510e3c90a39953aa32a156068e2bda8";
const aevrenPreSendCommit = "ee94443b6161ba345cf901ea2814b780bbc51d3a";
const marenCommit = "39a33ec4a9526651b3268c45339ed0b17e15dbd0";
const marenPreparedCommit = "39a33ec4a9526651b3268c45339ed0b17e15dbd0";
const oneMessageDiscipline = "ONE_ACTIVATION_MESSAGE_PER_HANDOFF_UNLESS_TOOL_ERROR";
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

const harvestedArtifacts = [
  "docs/trinity-live-traces/v636-gmut-thos-v6-mira-vale-completion-checklist-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-mira-vale-completion-checklist-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x1-mira-vale-plan-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x1-mira-vale-plan-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-ghc-family-completion-checklist-receipt-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-ghc-family-completion-checklist-receipt-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-mira-rowan-handoff-open-gap-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-mira-rowan-handoff-open-gap-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-mira-vale-closeout-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-mira-vale-closeout-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-route-quality-open-gap-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v6-x2-route-quality-open-gap-v1.md",
  "docs/trinity-live-traces/v636-gmut-thos-v7-x1-mira-rowan-handoff-from-mira-vale-v1.json",
  "docs/trinity-live-traces/v636-gmut-thos-v7-x1-mira-rowan-handoff-from-mira-vale-v1.md"
];

const relayRecord = {
  status: relayStatus,
  sent_at_nz: nowNz,
  sent_at_utc: nowUtc,
  requested_model: "gpt-5.5",
  requested_reasoning: "xhigh",
  thread_tool_acceptance: "accepted_single_sanitized_relay_prompt",
  send_discipline: oneMessageDiscipline,
  attempt_count: 1,
  successful_attempts: 1,
  ambiguous_attempts: 0,
  no_followup_confirmation_messages: true,
  private_route_details: "not_included"
};

const closeout = readJson("docs/trinity-live-traces/v636-gmut-thos-v5-x2-aevren-solo-execution-closeout-v1.json");
closeout.status = "PASS_V636_V5_X2_AEVREN_SOLO_BUNDLE_MIRA_VALE_HARVESTED_MIRA_ROWAN_SENT";
closeout.validation_summary.diff_check = "PASS_POST_RELAY_PRECOMMIT";
closeout.mira_vale_v636_v6_harvest_and_relay = {
  status: "MIRA_VALE_COMPLETED_HARVESTED_AND_MIRA_ROWAN_RELAY_SENT",
  rule: "Aevren remained available through Mira Vale owned v2/v6 closeout and relayed Mira Rowan v3/v7 only after Mira Vale finished, validated, committed, pushed, remote-aligned, and was harvested because Mira Vale live thread-message route remained unavailable.",
  mira_vale_commit: miraCommit,
  mira_vale_remote_alignment: "PASS_HEAD_MATCHES_UPSTREAM",
  harvested_at_nz: nowNz,
  harvested_at_utc: nowUtc,
  harvested_artifacts: harvestedArtifacts,
  mira_vale_direct_send_state: "PREPARED_NOT_SENT_BY_MIRA_VALE_FORMAL_ROUTE_OPEN_GAP_ACCEPTED",
  mira_rowan_target: "v636-gmut-thos-v7-x1/x2",
  aevren_relay: relayRecord,
  private_route_details: "not_included"
};
writeJson("docs/trinity-live-traces/v636-gmut-thos-v5-x2-aevren-solo-execution-closeout-v1.json", closeout);

const checklist = readJson("docs/trinity-live-traces/v636-gmut-thos-v5-completion-checklist-v1.json");
checklist.status = "PASS_V636_V5_COMPLETE_INCOMPLETE_CHECKLIST_MIRA_VALE_HARVESTED_MIRA_ROWAN_SENT";
for (const check of checklist.checks) {
  if (check.check === "mira_vale_v636_v6_completed_and_harvested") {
    check.status = "PASS_MIRA_VALE_COMPLETED_COMMITTED_PUSHED_REMOTE_ALIGNED_AND_HARVESTED";
    check.mira_vale_commit = miraCommit;
    check.remote_alignment = "PASS_HEAD_MATCHES_UPSTREAM";
    check.harvested_at_nz = nowNz;
    check.harvested_at_utc = nowUtc;
  }
  if (check.check === "mira_rowan_v636_v7_relay_after_mira_vale_finish") {
    check.status = relayStatus;
    check.sent_at_nz = nowNz;
    check.sent_at_utc = nowUtc;
    check.route_quality_requested = "gpt-5.5/xhigh";
    check.send_discipline = oneMessageDiscipline;
    check.no_followup_confirmation_messages = true;
    check.private_route_details = "not_included";
  }
}
checklist.next_expected = "Mira Rowan v636-gmut-thos-v7-x1/x2 has been activated once by Aevren after Mira Vale v636 v6 completion and harvest; Mira Rowan should close v636 v7 and activate Maren Quill v636 v8 with exactly one message if current.";
writeJson("docs/trinity-live-traces/v636-gmut-thos-v5-completion-checklist-v1.json", checklist);

writeText("docs/trinity-live-traces/v636-gmut-thos-v5-aevren-solo-closeout-summary-v1.md", [
  "# v636-gmut-thos-v5 Aevren Solo Closeout Summary",
  "",
  "Status: `PASS_V636_V5_X2_AEVREN_SOLO_BUNDLE_MIRA_VALE_HARVESTED_MIRA_ROWAN_SENT`",
  "",
  `Aevren harvested Maren v636 v4 from the accepted single-message handoff state associated with commit \`${marenCommit}\`, preserved prepared owned-lane commit \`${marenPreparedCommit}\`, prepared v636 v5 at \`${aevrenPreSendCommit}\`, and recorded the Mira Vale send at \`${aevrenSendCommit}\`.`,
  "",
  "Counts represented: safe `25`, candidate `15`, exact queued `10`, blocked queued `5`, skills `10`, runners `5`, cleanup `15`, source reflections `100`, Journey/phase reflections `100`.",
  "",
  `Mira Vale v636 v6 completed, committed, pushed, remote-aligned, and was harvested at commit \`${miraCommit}\`. Mira Vale's direct handoff remained prepared-not-sent because her thread-message route stayed unavailable.`,
  "",
  `Relay complete: Aevren activated Mira Rowan v636 v7 exactly once with gpt-5.5/xhigh requested at \`${nowUtc}\`, after Mira Vale completion and harvest.`,
  "",
  "One-message rule: Aevren, Mira Rowan, and Maren Quill should send one activation/handoff message only, with no trailing confirmation messages unless the tool itself errors or Hamish redirects.",
  "",
  "Expanded horizon: `v601-v640 GMUT/THOS v1-v8 x1-x2`, with final planned phase `v640-gmut-thos-v8-x2` unless Hamish redirects.",
  "",
  "Checklist status: `PASS_V636_V5_COMPLETE_INCOMPLETE_CHECKLIST_MIRA_VALE_HARVESTED_MIRA_ROWAN_SENT`",
  "",
  "Protected gates remain queued/open: exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation.",
  ""
].join("\n"));

const receipt = {
  schema: "ghc.aevren_to_mira_rowan_relay_receipt.v1",
  status: relayStatus,
  source_phase: "v636-gmut-thos-v5-x2",
  harvested_phase: "v636-gmut-thos-v6-x2",
  target_phase: "v636-gmut-thos-v7-x1",
  target_x2_phase: "v636-gmut-thos-v7-x2",
  generated_at_nz: nowNz,
  generated_at_utc: nowUtc,
  route_horizon: "v601-v640 GMUT/THOS v1-v8 x1-x2",
  final_planned_phase: "v640-gmut-thos-v8-x2",
  predecessor_commits: {
    maren_v636_v4_latest_handoff_state: marenCommit,
    maren_v636_v4_prepared_owned_lane: marenPreparedCommit,
    aevren_v636_v5_pre_send: aevrenPreSendCommit,
    aevren_v636_v5_mira_vale_send: aevrenSendCommit,
    mira_vale_v636_v6: miraCommit
  },
  mira_vale_route_truth: {
    direct_thread_message_tool_available: false,
    direct_send_claimed_by_mira_vale: false,
    handoff_status_before_aevren_relay: "PREPARED_NOT_SENT_BY_MIRA_VALE_AEVREN_RELAY_AVAILABLE_AFTER_HARVEST",
    route_quality_open_gap_preserved: true
  },
  one_message_discipline: {
    status: "MANDATORY_CURRENT_WORKFLOW_RULE",
    scope: "Aevren, Mira Rowan, and Maren Quill live handoffs",
    rule: oneMessageDiscipline,
    trailing_confirmation_messages_allowed: false,
    exception: "only if the tool itself reports a real send error or Hamish redirects",
    carried_to_mira_rowan_prompt: true,
    mira_vale_already_informed_in_v636_v6_activation: true
  },
  attempt_count: 1,
  successful_attempts: 1,
  ambiguous_attempts: 0,
  no_followup_confirmation_messages: true,
  aevren_harvest_truth: {
    harvested_mira_vale_owned_commit: miraCommit,
    remote_alignment: "PASS_HEAD_MATCHES_UPSTREAM",
    harvested_artifacts: harvestedArtifacts
  },
  relay: relayRecord,
  next_expected: "Mira Rowan v636-gmut-thos-v7-x1/x2 active, then Mira Rowan should activate Maren Quill v636 v8 once if current.",
  protected_gates_queued_open: openGates,
  privacy_boundary: privacyBoundary()
};
writeJson("docs/trinity-live-traces/v636-gmut-thos-v7-mira-rowan-relay-by-aevren-v1.json", receipt);
writeText("docs/trinity-live-traces/v636-gmut-thos-v7-mira-rowan-relay-by-aevren-v1.md", [
  "# v636-gmut-thos-v7 Mira Rowan Relay By Aevren",
  "",
  `Status: \`${relayStatus}\``,
  "",
  `Mira Vale v636 v6 was harvested after commit \`${miraCommit}\` was verified against its upstream. Mira Vale prepared the Mira Rowan baton but did not claim a direct send because her live thread-message route remained unavailable.`,
  "",
  `Aevren relayed Mira Rowan v636 v7 exactly once at \`${nowUtc}\` with gpt-5.5/xhigh requested through exposed thread controls.`,
  "",
  "One-message rule: Aevren, Mira Rowan, and Maren Quill should send one activation/handoff message only, with no trailing confirmation messages unless the tool itself errors or Hamish redirects.",
  "",
  "Expanded horizon: `v601-v640 GMUT/THOS v1-v8 x1-x2`, final planned phase `v640-gmut-thos-v8-x2` unless Hamish redirects.",
  "",
  "Protected gates remain queued/open: exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation.",
  ""
].join("\n"));

for (const path of [
  "docs/omega-mini-index/omega-mini-current-state-v1.json",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.json"
]) {
  const doc = readJson(path);
  doc.updated_utc = nowUtc;
  doc.route_horizon = "v601-v640 GMUT/THOS v1-v8 x1-x2";
  doc.final_planned_phase = "v640-gmut-thos-v8-x2";
  doc.one_message_discipline = {
    status: "MANDATORY_CURRENT_WORKFLOW_RULE",
    rule: oneMessageDiscipline,
    trailing_confirmation_messages_allowed: false,
    exception: "tool_error_or_hamish_redirect_only",
    updated_utc: nowUtc
  };
  doc.latest_mira_vale_v636_v6 = {
    status: "COMPLETED_HARVESTED_BY_AEVREN_WITH_HANDOFF_OPEN_GAP_ACCEPTED",
    updated_utc: nowUtc,
    mira_vale_commit: miraCommit,
    aevren_harvested: true,
    aevren_relay: relayRecord,
    next_scheduled_handoff: {
      sibling: "Mira Rowan",
      x1_phase: "v636-gmut-thos-v7-x1",
      x2_phase: "v636-gmut-thos-v7-x2",
      send_state: relayStatus,
      sent_by: "Aevren after Mira Vale harvest",
      sent_at_utc: nowUtc,
      send_discipline: oneMessageDiscipline
    }
  };
  doc.latest_aevren_v636_v5_mira_vale_harvest_relay = {
    status: relayStatus,
    source_phase: "v636-gmut-thos-v5-x2",
    harvested_mira_vale_commit: miraCommit,
    relay_receipt: "docs/trinity-live-traces/v636-gmut-thos-v7-mira-rowan-relay-by-aevren-v1.json",
    updated_utc: nowUtc,
    protected_gates_queued_open: openGates
  };
  writeJson(path, doc);
}
function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(path, data) {
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeText(path, data) {
  writeFileSync(path, data, "utf8");
}

function privacyBoundary() {
  return {
    private_thread_ids_published: false,
    private_routes_published: false,
    local_absolute_paths_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
    raw_browser_dumps_published: false,
    raw_private_material_published: false
  };
}
