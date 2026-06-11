#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const approvalIndexJson = args.get("--approval-index-json");
const readOnlyAuthJson = args.get("--read-only-auth-json");
const readinessJson = args.get("--readiness-json");
const activationJson = args.get("--activation-json");
const activationMd = args.get("--activation-md");
const carryGateJson = args.get("--carry-gate-json");
const carryGateMd = args.get("--carry-gate-md");

if (
  !phaseSlug ||
  !approvalIndexJson ||
  !readOnlyAuthJson ||
  !readinessJson ||
  !activationJson ||
  !activationMd ||
  !carryGateJson ||
  !carryGateMd
) {
  console.error(
    "Usage: node ghc_approval_activation_carry_gate.mjs --phase-slug <slug> --approval-index-json <json> --read-only-auth-json <json> --readiness-json <json> --activation-json <json> --activation-md <md> --carry-gate-json <json> --carry-gate-md <md>",
  );
  process.exit(2);
}

const approvalIndex = JSON.parse(readFileSync(approvalIndexJson, "utf8"));
const readOnlyAuth = JSON.parse(readFileSync(readOnlyAuthJson, "utf8"));
const readiness = JSON.parse(readFileSync(readinessJson, "utf8"));
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const candidates = Array.isArray(approvalIndex.candidates) ? approvalIndex.candidates : [];
const activatedCandidates = candidates.map((candidate) => ({
  ...candidate,
  previous_status: candidate.status,
  status: "APPROVED_USER_AUTHORIZED",
  authorization_scope: "curated preparation, route recovery, validator, watcher, and phase-planning work only",
}));

const blockerBoundaryCandidate = activatedCandidates.find(
  (candidate) => candidate.id === "packet-01-blocker-boundary-carry",
);
const readOnlyAuthorized = Array.isArray(readOnlyAuth.lane_permissions)
  ? readOnlyAuth.lane_permissions.every((lane) => lane.permission_status === "AUTHORIZED_READ_ONLY_ONLY")
  : false;
const pendingAfterActivation = activatedCandidates.filter(
  (candidate) => candidate.status !== "APPROVED_USER_AUTHORIZED",
);
const openLanes = Array.isArray(readiness.open_lanes) ? readiness.open_lanes : [];
const completedLanes = Array.isArray(readiness.completed_lanes) ? readiness.completed_lanes : [];

const publicationBoundary = {
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
};

const claimBoundary = {
  phase_completion: "not_claimed",
  v507_v8_completion: "not_claimed",
  v508_full_phase_start: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const activation = {
  artifact_type: "ghc_approval_activation_overlay",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  approval_index_input: approvalIndexJson,
  read_only_authorization_input: readOnlyAuthJson,
  authorization_source_type: "active_thread_user_authorization",
  authorization_summary:
    "The active goal context authorizes the previously prepared approval packet set; this overlay activates the v508 packet candidates without republishing raw user text.",
  status: "APPROVAL_CANDIDATES_AUTHORIZED_FOR_PREPARATION",
  candidate_count: activatedCandidates.length,
  approved_count: activatedCandidates.length - pendingAfterActivation.length,
  pending_count: pendingAfterActivation.length,
  activated_candidates: activatedCandidates,
  explicit_boundaries: [
    "Approval activation does not prove lane completion.",
    "Approval activation does not publish raw lane text, raw user text, private IDs, credentials, screenshots, or local absolute paths.",
    "Approval activation does not create replacement siblings, replacement routes, old-style subagents, new threads, or account mutations.",
    "Approval activation does not close GMUT, physics, consciousness, legal, or canon gates.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const blockerBoundaryCarryAuthorized = blockerBoundaryCandidate?.status === "APPROVED_USER_AUTHORIZED";
const approvalsActive = pendingAfterActivation.length === 0;
const preparationAllowed = Boolean(readiness.preparation_allowed) && approvalsActive && readOnlyAuthorized;
const limitedX1PreparationAllowed = preparationAllowed && blockerBoundaryCarryAuthorized;
const fullPhaseStartAllowed = Boolean(readiness.phase_start_allowed) && openLanes.length === 0 && approvalsActive;
const carryStatus = fullPhaseStartAllowed
  ? "PASS_FULL_PHASE_START_READY"
  : limitedX1PreparationAllowed
    ? "OPEN_LANE_CARRY_APPROVED_LIMITED_X1_PREPARATION_READY"
    : "BLOCKED_PENDING_APPROVAL_OR_READ_ONLY_AUTHORIZATION";

const carryGate = {
  artifact_type: "ghc_approval_activation_carry_gate",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  readiness_input: readinessJson,
  activation_input: activationJson,
  read_only_authorization_input: readOnlyAuthJson,
  status: carryStatus,
  full_phase_start_allowed: fullPhaseStartAllowed,
  limited_x1_preparation_allowed: limitedX1PreparationAllowed,
  x2_build_closeout_allowed: false,
  approvals_active: approvalsActive,
  read_only_lanes_authorized: readOnlyAuthorized,
  blocker_boundary_carry_authorized: blockerBoundaryCarryAuthorized,
  completed_lanes: completedLanes,
  open_lanes: openLanes,
  next_allowed_work: [
    "Run read-only route refresh and status receipt attempts for the six-lane roster.",
    "Continue source-refresh, Journey/Trinity reflection, and watcher-cadence artifacts between checks.",
    "Prepare v508 x1 plans and approval packets while keeping open app-lane blockers visible.",
    "Build validators and compact-refresh cards that make the next handoff recoverable.",
  ],
  not_allowed_work: [
    "Claim full v508 x1 phase start or closeout until required lane evidence is present or a later gate explicitly permits it.",
    "Claim v507 v8 completion while Kierkegaard and Aristotle remain unresolved.",
    "Treat read-only authorization as evidence that a sibling responded.",
    "Create replacement siblings, replacement threads, old-style subagents, or hidden private maps.",
    "Publish raw lane text, browser transcripts, app-server payloads, private IDs, credentials, screenshots, or local absolute paths.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

mkdirSync(dirname(activationJson), { recursive: true });
writeFileSync(activationJson, `${JSON.stringify(activation, null, 2)}\n`, "utf8");
writeFileSync(carryGateJson, `${JSON.stringify(carryGate, null, 2)}\n`, "utf8");

const activationLines = [
  `# ${phaseSlug} Approval Activation Overlay`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${activation.status}\``,
  "",
  "This overlay records that the previously prepared v508 approval packet candidates are now authorized for curated preparation work. It does not republish raw user text and does not rewrite the older pending snapshot.",
  "",
  "## Activated Candidates",
  "",
  ...activatedCandidates.map(
    (candidate) =>
      `- ${candidate.id}: ${candidate.title} changed from \`${candidate.previous_status}\` to \`${candidate.status}\`.`,
  ),
  "",
  "## Boundaries",
  "",
  ...activation.explicit_boundaries.map((boundary) => `- ${boundary}`),
  "",
];

const carryLines = [
  `# ${phaseSlug} Approval Carry Readiness Gate`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${carryStatus}\``,
  "",
  `Full phase start allowed: \`${fullPhaseStartAllowed}\``,
  `Limited x1 preparation allowed: \`${limitedX1PreparationAllowed}\``,
  `x2 build closeout allowed: \`${carryGate.x2_build_closeout_allowed}\``,
  "",
  "## Current Lane Evidence",
  "",
  "Completed lanes:",
  ...(completedLanes.length
    ? completedLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "Open lanes:",
  ...(openLanes.length
    ? openLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Next Allowed Work",
  "",
  ...carryGate.next_allowed_work.map((item) => `- ${item}`),
  "",
  "## Not Allowed Work",
  "",
  ...carryGate.not_allowed_work.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "This is a carry gate, not a completion certificate. It activates preparation under the approved read-only and no-replacement rules while preserving unresolved app-lane blockers.",
  "",
];

writeFileSync(activationMd, activationLines.join("\n"), "utf8");
writeFileSync(carryGateMd, carryLines.join("\n"), "utf8");

console.log(
  JSON.stringify(
    {
      activation_status: activation.status,
      carry_status: carryGate.status,
      approved_count: activation.approved_count,
      pending_count: activation.pending_count,
      full_phase_start_allowed: carryGate.full_phase_start_allowed,
      limited_x1_preparation_allowed: carryGate.limited_x1_preparation_allowed,
    },
    null,
    2,
  ),
);
