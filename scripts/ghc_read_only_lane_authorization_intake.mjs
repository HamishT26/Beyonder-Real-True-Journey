#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const routeBoardJson = args.get("--route-board-json");
const readinessJson = args.get("--readiness-json");
const approvalIndexJson = args.get("--approval-index-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !routeBoardJson || !readinessJson || !approvalIndexJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_read_only_lane_authorization_intake.mjs --phase-slug <slug> --route-board-json <json> --readiness-json <json> --approval-index-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const routeBoard = JSON.parse(readFileSync(routeBoardJson, "utf8"));
const readiness = JSON.parse(readFileSync(readinessJson, "utf8"));
const approvalIndex = JSON.parse(readFileSync(approvalIndexJson, "utf8"));

const roster = [
  {
    lane: "Lumen Vale",
    route_family: "Browser in-app live adapter",
    allowed_mode: "read-only message and status receipt",
  },
  {
    lane: "Arby",
    route_family: "Codex CLI read-only lane",
    allowed_mode: "read-only advisory prompt with no shell and no tools",
  },
  {
    lane: "Aster Vale",
    route_family: "Codex CLI read-only lane",
    allowed_mode: "read-only advisory prompt with no shell and no tools",
  },
  {
    lane: "Cicero",
    route_family: "Codex app local callable lane",
    allowed_mode: "read-only advisory message through existing callable route only",
  },
  {
    lane: "Kierkegaard",
    route_family: "Codex app local callable lane",
    allowed_mode: "read-only advisory message through existing callable route only",
  },
  {
    lane: "Aristotle",
    route_family: "Codex app local callable lane",
    allowed_mode: "read-only advisory message through existing callable route only",
  },
];

const boardRows = new Map();
for (const family of routeBoard.route_families || []) {
  for (const lane of family.lanes || []) {
    boardRows.set(lane.lane, {
      status: lane.status,
      completed: Boolean(lane.completed),
      evidence_present: Boolean(lane.evidence_present),
      route_family: family.route_family,
    });
  }
}

const lanePermissions = roster.map((lane) => {
  const evidence = boardRows.get(lane.lane);
  const evidenceStatus = evidence
    ? evidence.status
    : "PENDING_CURRENT_EVIDENCE_REFRESH";
  return {
    ...lane,
    permission_status: "AUTHORIZED_READ_ONLY_ONLY",
    current_evidence_status: evidenceStatus,
    current_evidence_present: Boolean(evidence?.evidence_present),
    completed_claim_allowed: false,
    retry_allowed: true,
    blocker_receipt_required_if_unreachable: true,
  };
});

const pendingApprovals = Array.isArray(approvalIndex.candidates)
  ? approvalIndex.candidates.filter((candidate) => candidate.status !== "APPROVED_USER_AUTHORIZED").length
  : approvalIndex.pending_count;

const receipt = {
  artifact_type: "ghc_read_only_lane_authorization_intake",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  route_board_input: routeBoardJson,
  readiness_input: readinessJson,
  approval_index_input: approvalIndexJson,
  user_authorization_scope:
    "Existing sibling lanes are authorized for read-only operation only; no replacement siblings, new old-style subagents, raw publication, or completion overclaim.",
  status: "READ_ONLY_AUTHORIZATION_RECORDED_PREPARATION_ONLY",
  phase_start_allowed: Boolean(readiness.phase_start_allowed),
  preparation_allowed: Boolean(readiness.preparation_allowed),
  pending_approval_count_observed: pendingApprovals,
  lane_permissions: lanePermissions,
  cadence_policy: {
    check_interval_minutes: 5,
    busy_waiting_allowed: false,
    work_between_checks_required: true,
    allowed_between_checks: [
      "source-refresh ledgers",
      "Journey and Trinity reflection cards",
      "watcher and validator improvements",
      "approval packet drafting",
      "phase-start and compact-refresh preparation",
    ],
  },
  retry_policy: {
    safe_retries_before_blocker_receipt: 5,
    retry_scope: "read-only route refresh, message send retry, status receipt retry, validator rerun",
    not_retry_scope: "new sibling creation, replacement thread creation, private ID publication, raw transcript publication",
  },
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
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    v507_v8_completion: "not_claimed",
    v508_phase_start: readiness.phase_start_allowed ? "allowed_by_readiness_gate" : "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Read-Only Lane Authorization Intake`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "This records the latest read-only authorization for existing sibling lanes only. It does not start v508, complete v507 v8, approve replacement lanes, or clear unresolved app-lane blockers.",
  "",
  "## Lane Permissions",
  "",
  ...lanePermissions.map(
    (lane) =>
      `- ${lane.lane} (${lane.route_family}): \`${lane.permission_status}\`; evidence \`${lane.current_evidence_status}\`; mode ${lane.allowed_mode}.`,
  ),
  "",
  "## Cadence Policy",
  "",
  `- Check interval: \`${receipt.cadence_policy.check_interval_minutes} minutes\`.`,
  "- Busy-waiting is not allowed.",
  "- Preparation work continues between checks.",
  "",
  "Allowed between checks:",
  ...receipt.cadence_policy.allowed_between_checks.map((item) => `- ${item}`),
  "",
  "## Retry Policy",
  "",
  `- Safe retries before blocker receipt: \`${receipt.retry_policy.safe_retries_before_blocker_receipt}\`.`,
  `- Retry scope: ${receipt.retry_policy.retry_scope}.`,
  `- Not retry scope: ${receipt.retry_policy.not_retry_scope}.`,
  "",
  "## Readiness Boundary",
  "",
  `- Phase start allowed by prior readiness gate: \`${receipt.phase_start_allowed}\`.`,
  `- Preparation allowed by prior readiness gate: \`${receipt.preparation_allowed}\`.`,
  `- Pending approval count observed in index: \`${receipt.pending_approval_count_observed}\`.`,
  "",
  "## Publication Boundary",
  "",
  "No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, v507 v8 completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      lanes: lanePermissions.length,
      phase_start_allowed: receipt.phase_start_allowed,
      preparation_allowed: receipt.preparation_allowed,
    },
    null,
    2,
  ),
);
