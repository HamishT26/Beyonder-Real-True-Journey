#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const prepQueueJson = args.get("--prep-queue-json");
const boundaryJson = args.get("--boundary-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !prepQueueJson || !boundaryJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_phase_start_readiness_gate.mjs --phase-slug <slug> --prep-queue-json <json> --boundary-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const prepQueue = JSON.parse(readFileSync(prepQueueJson, "utf8"));
const boundary = JSON.parse(readFileSync(boundaryJson, "utf8"));
const candidates = Array.isArray(prepQueue.approval_candidates) ? prepQueue.approval_candidates : [];
const openLanes = Array.isArray(prepQueue.current_evidence?.open_lanes) ? prepQueue.current_evidence.open_lanes : [];
const completedLanes = Array.isArray(prepQueue.current_evidence?.completed_lanes)
  ? prepQueue.current_evidence.completed_lanes
  : [];

const pendingCandidates = candidates.filter((candidate) => candidate.status !== "APPROVED_USER_AUTHORIZED");
const boundaryPending =
  boundary.status === "PENDING_APPROVAL_OPEN_BLOCKER_BOUNDARY" ||
  boundary.approval_packet?.status === "PENDING_USER_APPROVAL";
const openBlockersPresent = openLanes.length > 0;
const approvalReady = pendingCandidates.length === 0;
const recoveredOrClear = openLanes.length === 0;

let status;
let phaseStartAllowed;
let preparationAllowed;
let reason;
if (recoveredOrClear && approvalReady) {
  status = "PASS_PHASE_START_READY";
  phaseStartAllowed = true;
  preparationAllowed = true;
  reason = "all lane blockers are clear and approval candidates are authorized";
} else if (openBlockersPresent && boundaryPending) {
  status = "BLOCK_PHASE_START_PENDING_BLOCKER_BOUNDARY_APPROVAL";
  phaseStartAllowed = false;
  preparationAllowed = true;
  reason = "open app-lane blockers remain and blocker-boundary carry is still pending approval";
} else if (!approvalReady) {
  status = "BLOCK_PHASE_START_PENDING_APPROVAL_CANDIDATES";
  phaseStartAllowed = false;
  preparationAllowed = true;
  reason = "one or more approval candidates remain pending";
} else {
  status = "BLOCK_PHASE_START_UNPROVEN";
  phaseStartAllowed = false;
  preparationAllowed = true;
  reason = "readiness evidence is not strong enough for phase start";
}

const receipt = {
  artifact_type: "ghc_phase_start_readiness_gate",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  prep_queue_input: prepQueueJson,
  boundary_input: boundaryJson,
  status,
  phase_start_allowed: phaseStartAllowed,
  preparation_allowed: preparationAllowed,
  reason,
  completed_lanes: completedLanes,
  open_lanes: openLanes,
  approval_candidate_count: candidates.length,
  pending_approval_count: pendingCandidates.length,
  boundary_pending: boundaryPending,
  required_before_start: [
    "Recover Kierkegaard and Aristotle app-lane evidence or receive explicit blocker-boundary carry approval.",
    "Convert pending approval candidates to explicit approved receipts before treating them as authorization.",
    "Run route-family, no-replacement, exposure, no-overclaim, and phase-advance gates.",
    "Keep Browser and CLI evidence route-specific.",
  ],
  allowed_now: [
    "Preparation-only planning.",
    "Validator and watcher tooling.",
    "Approval packet drafting.",
    "Source-refresh and compact-refresh artifacts.",
  ],
  not_allowed_now: [
    "Claiming v508 has started as a completed phase.",
    "Claiming v507 v8 complete.",
    "Treating pending approval candidates as approved.",
    "Creating replacement siblings or old-style subagents.",
    "Publishing raw lane data or private IDs.",
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
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Phase-Start Readiness Gate`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Phase start allowed: \`${phaseStartAllowed}\``,
  `Preparation allowed: \`${preparationAllowed}\``,
  `Reason: ${reason}`,
  "",
  "## Completed Route-Specific Evidence",
  "",
  ...(completedLanes.length
    ? completedLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Open Lanes",
  "",
  ...(openLanes.length
    ? openLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Required Before Start",
  "",
  ...receipt.required_before_start.map((item) => `- ${item}`),
  "",
  "## Allowed Now",
  "",
  ...receipt.allowed_now.map((item) => `- ${item}`),
  "",
  "## Not Allowed Now",
  "",
  ...receipt.not_allowed_now.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Readiness gate only. This does not start v508 and does not complete v507. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status, phase_start_allowed: phaseStartAllowed, preparation_allowed: preparationAllowed }, null, 2));

if (phaseStartAllowed !== true) {
  process.exit(1);
}
