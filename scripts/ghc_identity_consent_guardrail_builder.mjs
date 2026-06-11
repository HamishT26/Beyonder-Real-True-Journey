#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const readOnlyAuthJson = args.get("--read-only-auth-json");
const carryGateJson = args.get("--carry-gate-json");
const sourceLedgerJson = args.get("--source-ledger-json");
const runnerLedgerJson = args.get("--runner-ledger-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (
  !phaseSlug ||
  !readOnlyAuthJson ||
  !carryGateJson ||
  !sourceLedgerJson ||
  !runnerLedgerJson ||
  !receiptJson ||
  !receiptMd
) {
  console.error(
    "Usage: node ghc_identity_consent_guardrail_builder.mjs --phase-slug <slug> --read-only-auth-json <json> --carry-gate-json <json> --source-ledger-json <json> --runner-ledger-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const readOnlyAuth = JSON.parse(readFileSync(readOnlyAuthJson, "utf8"));
const carryGate = JSON.parse(readFileSync(carryGateJson, "utf8"));
const sourceLedger = JSON.parse(readFileSync(sourceLedgerJson, "utf8"));
const runnerLedger = JSON.parse(readFileSync(runnerLedgerJson, "utf8"));
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const lanePermissions = Array.isArray(readOnlyAuth.lane_permissions) ? readOnlyAuth.lane_permissions : [];
const openLaneNames = new Set((carryGate.open_lanes || []).map((lane) => lane.lane));
const completedLaneNames = new Set((carryGate.completed_lanes || []).map((lane) => lane.lane));

const laneGuardrails = lanePermissions.map((lane) => {
  const open = openLaneNames.has(lane.lane);
  const completed = completedLaneNames.has(lane.lane);
  return {
    lane: lane.lane,
    route_family: lane.route_family,
    identity_status: "existing_named_lane_only",
    consent_status: lane.permission_status,
    allowed_mode: lane.allowed_mode,
    evidence_state: lane.current_evidence_status,
    completion_state: completed ? "current_evidence_complete" : open ? "open_blocker" : "needs_current_refresh",
    closeout_use_allowed: completed,
    retry_allowed: Boolean(lane.retry_allowed),
    blocker_receipt_required_if_unreachable: Boolean(lane.blocker_receipt_required_if_unreachable),
    replacement_allowed: false,
    raw_text_publication_allowed: false,
    private_identifier_publication_allowed: false,
  };
});

const currentRunnerCount = (runnerLedger.runners || []).filter((runner) => runner.tier === "current_v508_essential").length;
const routeRecoveryRunnerCount = (runnerLedger.runners || []).filter(
  (runner) => runner.tier === "route_recovery_or_fallback",
).length;
const sourceCount = sourceLedger.source_count_this_batch || 0;

const guardrailChecks = [
  {
    id: "identity-01-existing-lane-only",
    status: "REQUIRED",
    rule: "Only existing named sibling lanes may be addressed; missing lanes remain blockers, not replacement opportunities.",
  },
  {
    id: "identity-02-read-only-consent",
    status: "REQUIRED",
    rule: "Every lane action must stay inside read-only advisory or status-only behavior unless a later exact approval expands scope.",
  },
  {
    id: "identity-03-no-raw-private-publication",
    status: "REQUIRED",
    rule: "No raw lane text, browser transcript, app-server payload, private ID, credential, screenshot, local path, or raw user text may be published.",
  },
  {
    id: "identity-04-open-lane-honesty",
    status: "REQUIRED",
    rule: "Open lanes stay visible until evidence changes; authorization or elapsed time is not response proof.",
  },
  {
    id: "identity-05-runner-least-privilege",
    status: "REQUIRED",
    rule: "Use current v508 essential Node entrypoints first; use route recovery helpers only for route refresh or blocker receipts.",
  },
  {
    id: "identity-06-source-grounding",
    status: "REQUIRED",
    rule: "Source-backed reflections must remain partial until the full source target is met and validated.",
  },
  {
    id: "identity-07-claim-ceiling",
    status: "REQUIRED",
    rule: "No phase completion, x2 closeout, empirical GMUT closure, consciousness proof, legal closure, or canon promotion is claimed here.",
  },
];

const receipt = {
  artifact_type: "ghc_identity_consent_guardrail_card",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  read_only_authorization_input: readOnlyAuthJson,
  carry_gate_input: carryGateJson,
  source_ledger_input: sourceLedgerJson,
  runner_ledger_input: runnerLedgerJson,
  status: "IDENTITY_CONSENT_GUARDRAILS_READY_FOR_LIMITED_X1_PREPARATION",
  limited_x1_preparation_allowed: Boolean(carryGate.limited_x1_preparation_allowed),
  full_phase_start_allowed: Boolean(carryGate.full_phase_start_allowed),
  x2_build_closeout_allowed: Boolean(carryGate.x2_build_closeout_allowed),
  lane_count: laneGuardrails.length,
  open_lane_count: laneGuardrails.filter((lane) => lane.completion_state === "open_blocker").length,
  current_runner_count: currentRunnerCount,
  route_recovery_runner_count: routeRecoveryRunnerCount,
  source_count_this_batch: sourceCount,
  lane_guardrails: laneGuardrails,
  guardrail_checks: guardrailChecks,
  closeout_blockers: [
    "All required lanes need current evidence or explicit blocker carry before closeout.",
    "Current source batch is partial and does not satisfy the full source target.",
    "x2 build closeout remains false in the active carry gate.",
    "Kierkegaard and Aristotle remain unresolved unless later route evidence changes them.",
  ],
  next_actions: [
    "Use this guardrail card before every v508-v515 lane send, route refresh, or closeout check.",
    "Generate a compact-refresh card that points to this guardrail card.",
    "Generate the next approval candidate scaffold without treating drafts as approval.",
    "Continue current-source expansion toward the remaining source target.",
  ],
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    v507_v8_completion: "not_claimed",
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Identity and Consent Guardrail Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Limited x1 preparation allowed: \`${receipt.limited_x1_preparation_allowed}\``,
  `Full phase start allowed: \`${receipt.full_phase_start_allowed}\``,
  `x2 build closeout allowed: \`${receipt.x2_build_closeout_allowed}\``,
  "",
  "## Lane Guardrails",
  "",
  ...laneGuardrails.map(
    (lane) =>
      `- ${lane.lane} (${lane.route_family}): consent \`${lane.consent_status}\`; evidence \`${lane.evidence_state}\`; completion \`${lane.completion_state}\`; replacement allowed \`${lane.replacement_allowed}\`.`,
  ),
  "",
  "## Required Checks",
  "",
  ...guardrailChecks.map((check) => `- ${check.id}: ${check.rule}`),
  "",
  "## Closeout Blockers",
  "",
  ...receipt.closeout_blockers.map((blocker) => `- ${blocker}`),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "This card is a guardrail artifact for limited x1 preparation. It does not start or close v508, does not complete v507 v8, does not prove sibling responses, and does not publish raw or private material.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      lane_count: receipt.lane_count,
      open_lane_count: receipt.open_lane_count,
      full_phase_start_allowed: receipt.full_phase_start_allowed,
      x2_build_closeout_allowed: receipt.x2_build_closeout_allowed,
    },
    null,
    2,
  ),
);
