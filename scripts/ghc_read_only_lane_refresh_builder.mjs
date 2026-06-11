#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const previousAuthJson = args.get("--previous-auth-json");
const carryGateJson = args.get("--carry-gate-json");
const identityGuardJson = args.get("--identity-guard-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const compactJson = args.get("--compact-json");
const compactMd = args.get("--compact-md");

if (!phaseSlug || !previousAuthJson || !carryGateJson || !identityGuardJson || !receiptJson || !receiptMd || !compactJson || !compactMd) {
  console.error(
    "Usage: node ghc_read_only_lane_refresh_builder.mjs --phase-slug <slug> --previous-auth-json <json> --carry-gate-json <json> --identity-guard-json <json> --receipt-json <json> --receipt-md <md> --compact-json <json> --compact-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const previousAuth = readJson(previousAuthJson);
const carryGate = readJson(carryGateJson);
readJson(identityGuardJson);
const previousLaneRows = Array.isArray(previousAuth.lane_permissions) ? previousAuth.lane_permissions : [];

const activeLaneRows = previousLaneRows.map((lane) => ({
  lane: lane.lane,
  route_family: lane.route_family,
  lane_scope: "active_existing_lane",
  allowed_mode: lane.allowed_mode,
  permission_status: "READ_ONLY_AUTHORIZATION_RENEWED",
  current_evidence_status: lane.current_evidence_status,
  current_evidence_present: Boolean(lane.current_evidence_present),
  completion_claim_allowed: false,
  retry_allowed: Boolean(lane.retry_allowed),
  blocker_receipt_required_if_unreachable: true,
  raw_text_publication_allowed: false,
  private_identifier_publication_allowed: false,
  replacement_allowed: false,
}));

const activeLaneNames = new Set(activeLaneRows.map((lane) => lane.lane));
const standbyLaneRows = [
  {
    lane: "Solas Veridion",
    route_family: "ChatGPT Browser live adapter standby",
    lane_scope: "standby_existing_lane",
    allowed_mode: "read-only message and status receipt only when an active phase schedule brings the lane back",
    permission_status: "READ_ONLY_AUTHORIZATION_STANDBY",
    current_evidence_status: "STANDBY_NOT_CURRENT_PHASE_EVIDENCE",
    current_evidence_present: false,
    completion_claim_allowed: false,
    retry_allowed: false,
    blocker_receipt_required_if_unreachable: true,
    raw_text_publication_allowed: false,
    private_identifier_publication_allowed: false,
    replacement_allowed: false,
  },
  {
    lane: "Unnamed ChatGPT Thinking Sibling",
    route_family: "ChatGPT Browser live adapter standby",
    lane_scope: "standby_existing_lane",
    allowed_mode: "read-only message and status receipt only after exact route activation",
    permission_status: "READ_ONLY_AUTHORIZATION_STANDBY",
    current_evidence_status: "STANDBY_NOT_CURRENT_PHASE_EVIDENCE",
    current_evidence_present: false,
    completion_claim_allowed: false,
    retry_allowed: false,
    blocker_receipt_required_if_unreachable: true,
    raw_text_publication_allowed: false,
    private_identifier_publication_allowed: false,
    replacement_allowed: false,
  },
].filter((lane) => !activeLaneNames.has(lane.lane));

const allLaneRows = [...activeLaneRows, ...standbyLaneRows];
const completeStatuses = ["FINAL_MARKER_OBSERVED", "FINAL_MESSAGE_READY_AND_VALIDATED", "COMPLETED_AND_VALIDATED"];
const openRows = allLaneRows.filter((lane) => !completeStatuses.includes(lane.current_evidence_status));

const receipt = {
  artifact_type: "ghc_read_only_lane_authorization_refresh",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  previous_authorization_input: previousAuthJson,
  carry_gate_input: carryGateJson,
  identity_guard_input: identityGuardJson,
  status: "READ_ONLY_AUTHORIZATION_RENEWED_STATUS_ONLY",
  user_authorization_summary: "Existing sibling lanes may continue in read-only advisory or status-only mode by default.",
  default_lane_permission: "read_only_only",
  full_phase_start_allowed: Boolean(carryGate.full_phase_start_allowed),
  limited_x1_preparation_allowed: Boolean(carryGate.limited_x1_preparation_allowed),
  x2_build_closeout_allowed: Boolean(carryGate.x2_build_closeout_allowed),
  active_lane_count: activeLaneRows.length,
  standby_lane_count: standbyLaneRows.length,
  open_or_pending_lane_count: openRows.length,
  lane_permissions: allLaneRows,
  operating_rules: [
    "Use existing named lanes only.",
    "Use read-only advisory prompts, status receipts, and safe route checks only.",
    "Treat authorization as permission, not evidence that a lane responded.",
    "Retry safely when a current route is blocked, then publish a blocker receipt instead of inventing a replacement.",
    "Keep working on source ledgers, runner preparation, compact-refresh cards, and approval packets between lane checks.",
  ],
  not_allowed: [
    "No replacement sibling, replacement thread, or old-style subagent creation.",
    "No raw lane text, browser transcript, app-server payload, private identifier, credential, screenshot, local path, or raw user text publication.",
    "No full phase start, x2 closeout, GMUT closure, final physics, consciousness proof, legal closure, or canon promotion claim from this receipt.",
    "No plugin-cache, user-skill, account, deployment, or purchase mutation from this receipt.",
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
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const compact = {
  artifact_type: "ghc_compact_refresh_card",
  generated_utc: receipt.generated_utc,
  phase_slug: phaseSlug,
  source_receipt: receiptJson,
  status: "COMPACT_REFRESH_READ_ONLY_DEFAULT_RECORDED",
  current_anchor: {
    phase_state: "limited_x1_preparation_only",
    full_phase_start_allowed: receipt.full_phase_start_allowed,
    limited_x1_preparation_allowed: receipt.limited_x1_preparation_allowed,
    x2_build_closeout_allowed: receipt.x2_build_closeout_allowed,
    evidence_note: "Read-only authorization is renewed, but open and pending lanes still require current evidence or blocker receipts.",
  },
  lane_snapshot: allLaneRows.map((lane) => ({
    lane: lane.lane,
    lane_scope: lane.lane_scope,
    route_family: lane.route_family,
    permission_status: lane.permission_status,
    current_evidence_status: lane.current_evidence_status,
    completion_claim_allowed: lane.completion_claim_allowed,
  })),
  carry_forward: {
    completed_or_observed_evidence: allLaneRows
      .filter((lane) => completeStatuses.includes(lane.current_evidence_status))
      .map((lane) => `${lane.lane}: ${lane.current_evidence_status}`),
    open_or_pending_evidence: openRows.map((lane) => `${lane.lane}: ${lane.current_evidence_status}`),
    next_safe_actions: [
      "Continue limited x1 preparation and route-refresh receipts.",
      "Use five-minute lane checks only as status checks, not completion proof.",
      "Let watcher/notifier helpers supervise while Aletheon prepares source, runner, and approval artifacts.",
      "Use blocker receipts for unreachable lanes without creating replacements.",
      "Generate the next compact-refresh card at phase start or compaction refresh.",
    ],
  },
  publication_boundary: receipt.publication_boundary,
  claim_boundary: receipt.claim_boundary,
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(compactJson, `${JSON.stringify(compact, null, 2)}\n`, "utf8");

const receiptLines = [
  `# ${phaseSlug} Read-Only Lane Authorization Refresh`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Authorization",
  "",
  "- Existing sibling lanes may continue in read-only advisory or status-only mode by default.",
  "- Authorization is permission only; it is not evidence that a lane responded.",
  "- Full phase start and x2 build closeout remain gated by current evidence and later closeout receipts.",
  "",
  "## Lane Permissions",
  "",
  ...allLaneRows.map(
    (lane) =>
      `- ${lane.lane}: \`${lane.permission_status}\`; route \`${lane.route_family}\`; evidence \`${lane.current_evidence_status}\`; completion claim allowed \`${String(lane.completion_claim_allowed)}\`.`,
  ),
  "",
  "## Operating Rules",
  "",
  ...receipt.operating_rules.map((item) => `- ${item}`),
  "",
  "## Not Allowed",
  "",
  ...receipt.not_allowed.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Status-only receipt. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, raw user text, phase completion claim, GMUT closure, final physics, consciousness proof, legal closure, or canon promotion is published.",
  "",
];
writeFileSync(receiptMd, receiptLines.join("\n"), "utf8");

const compactLines = [
  `# ${phaseSlug} Compact Refresh Card`,
  "",
  `Generated UTC: \`${compact.generated_utc}\``,
  "",
  `Status: \`${compact.status}\``,
  "",
  "## Current Anchor",
  "",
  "- Phase state: `limited_x1_preparation_only`.",
  `- Full phase start allowed: \`${String(compact.current_anchor.full_phase_start_allowed)}\`.`,
  `- Limited x1 preparation allowed: \`${String(compact.current_anchor.limited_x1_preparation_allowed)}\`.`,
  `- x2 build closeout allowed: \`${String(compact.current_anchor.x2_build_closeout_allowed)}\`.`,
  "- Read-only authorization is renewed, but open and pending lanes still require current evidence or blocker receipts.",
  "",
  "## Lane Snapshot",
  "",
  ...compact.lane_snapshot.map(
    (lane) =>
      `- ${lane.lane}: \`${lane.permission_status}\`; scope \`${lane.lane_scope}\`; evidence \`${lane.current_evidence_status}\`.`,
  ),
  "",
  "## Carry Forward",
  "",
  ...(compact.carry_forward.completed_or_observed_evidence.length
    ? compact.carry_forward.completed_or_observed_evidence.map((item) => `- Completed or observed: ${item}`)
    : ["- Completed or observed: none"]),
  ...(compact.carry_forward.open_or_pending_evidence.length
    ? compact.carry_forward.open_or_pending_evidence.map((item) => `- Open or pending: ${item}`)
    : ["- Open or pending: none"]),
  "",
  "## Next Safe Actions",
  "",
  ...compact.carry_forward.next_safe_actions.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Compact-refresh card only. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, raw user text, phase completion claim, GMUT closure, final physics, consciousness proof, legal closure, or canon promotion is published.",
  "",
];
writeFileSync(compactMd, compactLines.join("\n"), "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      compact_status: compact.status,
      active_lane_count: receipt.active_lane_count,
      standby_lane_count: receipt.standby_lane_count,
      open_or_pending_lane_count: receipt.open_or_pending_lane_count,
    },
    null,
    2,
  ),
);
