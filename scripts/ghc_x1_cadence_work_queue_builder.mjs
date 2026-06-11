#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const carryGateJson = args.get("--carry-gate-json");
const readOnlyAuthJson = args.get("--read-only-auth-json");
const prepQueueJson = args.get("--prep-queue-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !carryGateJson || !readOnlyAuthJson || !prepQueueJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_x1_cadence_work_queue_builder.mjs --phase-slug <slug> --carry-gate-json <json> --read-only-auth-json <json> --prep-queue-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const carryGate = JSON.parse(readFileSync(carryGateJson, "utf8"));
const readOnlyAuth = JSON.parse(readFileSync(readOnlyAuthJson, "utf8"));
const prepQueue = JSON.parse(readFileSync(prepQueueJson, "utf8"));
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const lanes = Array.isArray(readOnlyAuth.lane_permissions) ? readOnlyAuth.lane_permissions : [];
const cadenceMinutes = readOnlyAuth.cadence_policy?.check_interval_minutes || 5;
const limitedPreparation = Boolean(carryGate.limited_x1_preparation_allowed);
const fullPhaseStartAllowed = Boolean(carryGate.full_phase_start_allowed);
const openLanes = Array.isArray(carryGate.open_lanes) ? carryGate.open_lanes : [];

const checkWindows = [0, cadenceMinutes, cadenceMinutes * 2, cadenceMinutes * 3].map((minute, index) => ({
  index: index + 1,
  minute_mark: minute,
  purpose:
    minute === 0
      ? "send or refresh read-only lane prompts where a safe route exists"
      : "status-only lane check; if blocked, record blocker and continue independent prep",
  lanes: lanes.map((lane) => ({
    lane: lane.lane,
    route_family: lane.route_family,
    permitted_action:
      minute === 0
        ? "read-only send or route-refresh attempt"
        : "status-only check; no raw transcript capture",
    current_evidence_status: lane.current_evidence_status,
    blocker_receipt_required_if_unreachable: lane.blocker_receipt_required_if_unreachable,
  })),
}));

const approvalCandidates = Array.isArray(prepQueue.approval_candidates) ? prepQueue.approval_candidates : [];
const sourcePackets = approvalCandidates.map((candidate) => candidate.id).slice(0, 10);

const betweenCheckWorkQueue = [
  {
    id: "work-01-source-refresh",
    pillar: "GMUT mind",
    objective: "Prepare a primary-source refresh ledger without claiming empirical closure.",
    inputs: ["official OpenAI/Codex notes", "MCP/security references", "NVIDIA and Google infrastructure references"],
    output: "source-refresh receipt scaffold",
  },
  {
    id: "work-02-trinity-hybrid-os-runner-hardening",
    pillar: "THOS body",
    objective: "Map Node entrypoint runners that are current, safe, and reusable for v508-v515.",
    inputs: ["scripts/ghc_*.mjs", "latest phase receipts", "read-only lane authorization"],
    output: "runner compatibility ledger",
  },
  {
    id: "work-03-freed-id-cbr-guardrails",
    pillar: "Freed ID and CBR heart",
    objective: "Convert identity, consent, no-replacement, and no-overclaim rules into reusable closeout checks.",
    inputs: ["read-only lane authorization", "no-replacement guard", "claim boundaries"],
    output: "identity and consent guardrail card",
  },
  {
    id: "work-04-approval-packet-drafting",
    pillar: "governance",
    objective: "Draft the next 10 phase-local approval packets without treating drafts as approval.",
    inputs: sourcePackets,
    output: "next approval candidate scaffold",
  },
  {
    id: "work-05-compact-refresh",
    pillar: "continuity",
    objective: "Produce a compact-refresh card that survives context compaction and names current blockers plainly.",
    inputs: [carryGateJson, readOnlyAuthJson, prepQueueJson],
    output: "compact refresh card scaffold",
  },
  {
    id: "work-06-route-recovery",
    pillar: "coordination",
    objective: "Continue safe read-only route recovery for Arby, Cicero, Kierkegaard, and Aristotle evidence gaps.",
    inputs: ["route-family status board", "read-only lane authorization", "app-lane blocker receipts"],
    output: "route recovery checklist update",
  },
];

const receipt = {
  artifact_type: "ghc_x1_cadence_work_queue",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  carry_gate_input: carryGateJson,
  read_only_authorization_input: readOnlyAuthJson,
  prep_queue_input: prepQueueJson,
  status: limitedPreparation
    ? "LIMITED_X1_PREPARATION_CADENCE_READY"
    : "BLOCKED_CADENCE_NOT_AUTHORIZED",
  limited_x1_preparation_allowed: limitedPreparation,
  full_phase_start_allowed: fullPhaseStartAllowed,
  x2_build_closeout_allowed: Boolean(carryGate.x2_build_closeout_allowed),
  open_lane_count: openLanes.length,
  lane_count: lanes.length,
  check_interval_minutes: cadenceMinutes,
  busy_waiting_allowed: false,
  check_windows: checkWindows,
  between_check_work_queue: betweenCheckWorkQueue,
  required_before_any_closeout: [
    "Collect current status-only evidence or blocker receipts for every required lane row.",
    "Keep open app-lane blockers visible until real route evidence changes them.",
    "Run exposure, no-overclaim, no-replacement, JSON, script, whitespace, and exact-stage checks.",
    "Do not treat elapsed time, authorization, or route intent as completion evidence.",
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
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} x1 Cadence Work Queue`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Limited x1 preparation allowed: \`${limitedPreparation}\``,
  `Full phase start allowed: \`${fullPhaseStartAllowed}\``,
  `x2 build closeout allowed: \`${receipt.x2_build_closeout_allowed}\``,
  "",
  "## Five-Minute Check Cadence",
  "",
  ...checkWindows.flatMap((window) => [
    `### Check ${window.index}: minute ${window.minute_mark}`,
    "",
    window.purpose,
    "",
    ...window.lanes.map(
      (lane) =>
        `- ${lane.lane} (${lane.route_family}): ${lane.permitted_action}; evidence \`${lane.current_evidence_status}\`.`,
    ),
    "",
  ]),
  "## Work Between Checks",
  "",
  ...betweenCheckWorkQueue.flatMap((item) => [
    `### ${item.id}: ${item.objective}`,
    "",
    `Pillar: ${item.pillar}`,
    "",
    `Output: ${item.output}`,
    "",
  ]),
  "## Required Before Any Closeout",
  "",
  ...receipt.required_before_any_closeout.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "This queue organizes limited x1 preparation only. It does not start or close v508, does not complete v507 v8, does not prove lane responses, and does not publish raw or private material.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      lane_count: receipt.lane_count,
      check_windows: receipt.check_windows.length,
      work_items: receipt.between_check_work_queue.length,
      full_phase_start_allowed: receipt.full_phase_start_allowed,
    },
    null,
    2,
  ),
);

if (!limitedPreparation) {
  process.exit(1);
}
