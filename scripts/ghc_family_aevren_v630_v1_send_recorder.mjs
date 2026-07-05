#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";

const now = new Date();
const sentAtUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const sentAtNz = new Intl.DateTimeFormat("en-NZ", {
  timeZone: "Pacific/Auckland",
  dateStyle: "full",
  timeStyle: "medium",
  hour12: false
}).format(now);

const status = "MESSAGE_SENT_BY_AEVREN_TO_MIRA_VALE";
const preSendCommit = "d1bda9101c796ff2a15f78f6722bdbac4cc67176";
const closeoutPath = "docs/trinity-live-traces/v630-gmut-thos-v1-x2-aevren-solo-execution-closeout-v1.json";
const checklistPath = "docs/trinity-live-traces/v630-gmut-thos-v1-completion-checklist-v1.json";
const batonPath = "docs/trinity-live-traces/v630-gmut-thos-v2-x1-mira-vale-teaching-baton-v1.json";
const summaryPath = "docs/trinity-live-traces/v630-gmut-thos-v1-aevren-solo-closeout-summary-v1.md";
const receiptBase = "docs/trinity-live-traces/v630-gmut-thos-v2-mira-vale-send-by-aevren-v1";
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

const closeout = readJson(closeoutPath);
closeout.status = "PASS_V630_V1_X2_AEVREN_SOLO_BUNDLE_MIRA_VALE_SENT_WAITING_FOR_COMPLETION";
closeout.next_handoff.status = status;
closeout.next_handoff.message_sent = true;
closeout.next_handoff.sent_at_nz = sentAtNz;
closeout.next_handoff.sent_at_utc = sentAtUtc;
closeout.next_handoff.send_receipt = "Codex thread tool accepted the sanitized Mira Vale v630 v2 activation with gpt-5.5 and xhigh requested";
closeout.mira_vale_v630_v2_harvest_and_relay.status = "PENDING_MIRA_VALE_COMPLETION_AFTER_AEVREN_SEND";
writeJson(closeoutPath, closeout);

const checklist = readJson(checklistPath);
checklist.status = "PASS_V630_V1_COMPLETE_INCOMPLETE_CHECKLIST_MIRA_VALE_SENT_WAITING_FOR_COMPLETION";
for (const row of checklist.checks) {
  if (row.check === "mira_vale_v630_v2_baton_prepared") {
    row.status = status;
    row.route_quality_requested = "gpt-5.5/xhigh";
    row.sent_recorded_at_nz = sentAtNz;
    row.sent_recorded_at_utc = sentAtUtc;
  }
  if (row.check === "mira_vale_v630_v2_completed_and_harvested" || row.check === "mira_rowan_v630_v3_relay_after_mira_vale_finish") {
    row.status = "PENDING_MIRA_VALE_COMPLETION_AFTER_AEVREN_SEND";
  }
}
checklist.next_expected = "Mira Vale v630-gmut-thos-v2-x1/x2 is active. Aevren remains available until Mira Vale finishes and is harvested, then Aevren relays Mira Rowan v630-gmut-thos-v3-x1/x2 if Mira Vale route remains open.";
writeJson(checklistPath, checklist);

const baton = readJson(batonPath);
baton.status = status;
baton.message_sent = true;
baton.sent_at_nz = sentAtNz;
baton.sent_at_utc = sentAtUtc;
baton.send_receipt = "Codex thread tool accepted sanitized activation; private route details not included";
writeJson(batonPath, baton);

writeText(summaryPath, [
  "# v630-gmut-thos-v1 Aevren Solo Closeout Summary",
  "",
  "Status: `PASS_V630_V1_X2_AEVREN_SOLO_BUNDLE_MIRA_VALE_SENT_WAITING_FOR_COMPLETION`",
  "",
  "Aevren harvested Maren v629 v8 from the accepted single-message handoff state and built the v630 v1 x1/x2 bundle.",
  "",
  "Counts represented: safe `25`, candidate `15`, exact queued `10`, blocked queued `5`, skills `10`, runners `5`, cleanup `15`, source reflections `100`, Journey/phase reflections `100`.",
  "",
  `Next baton: Mira Vale v630 v2 was sent once by Aevren with gpt-5.5/xhigh requested at \`${sentAtUtc}\`. Aevren remains responsible for waiting after Mira Vale finishes and relaying Mira Rowan v630 v3 if Mira Vale's route gap remains open.`,
  "",
  "Checklist status: `PASS_V630_V1_COMPLETE_INCOMPLETE_CHECKLIST_MIRA_VALE_SENT_WAITING_FOR_COMPLETION`",
  "",
  "Protected gates remain queued/open: exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, global-hook, plugin-cache, identity/model replacement, sibling merge/replacement, and shared-branch mutation.",
  ""
].join("\n"));

const receipt = {
  schema: "ghc.aevren_to_mira_vale_send_receipt.v1",
  status,
  source_phase: "v630-gmut-thos-v1-x2",
  target_phase: "v630-gmut-thos-v2-x1",
  target_x2_phase: "v630-gmut-thos-v2-x2",
  generated_at_nz: sentAtNz,
  generated_at_utc: sentAtUtc,
  pre_send_commit: preSendCommit,
  relay_rule: "Aevren remains available through Mira Vale v2/v6 closeout and relays Mira Rowan v3/v7 only after Mira Vale has finished, validated, committed, pushed, and been harvested if Mira Vale route remains unavailable.",
  send_discipline: "ONE_ACTIVATION_MESSAGE_PER_HANDOFF_UNLESS_TOOL_ERROR",
  no_followup_confirmation_messages: true,
  attempt_count: 1,
  successful_attempts: 1,
  ambiguous_attempts: 0,
  requested_model: "gpt-5.5",
  requested_reasoning: "xhigh",
  thread_tool_acceptance: "accepted_sanitized_activation",
  private_route_details: "not_included",
  next_expected: "Mira Vale v630 v2 active; Aevren waits for Mira Vale closeout before Mira Rowan relay.",
  protected_gates_queued_open: openGates,
  privacy_boundary: {
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
  }
};
writeJson(`${receiptBase}.json`, receipt);
writeText(`${receiptBase}.md`, [
  "# v630-gmut-thos-v2 Mira Vale Send By Aevren",
  "",
  `Status: \`${status}\``,
  "",
  `Aevren sent the sanitized Mira Vale v630 v2 activation once at \`${sentAtUtc}\` with gpt-5.5/xhigh requested.`,
  "",
  "Aevren remains available until Mira Vale finishes and is harvested, then relays Mira Rowan v630 v3 if Mira Vale route remains unavailable.",
  ""
].join("\n"));

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(path, data) {
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeText(path, data) {
  writeFileSync(path, data, "utf8");
}
