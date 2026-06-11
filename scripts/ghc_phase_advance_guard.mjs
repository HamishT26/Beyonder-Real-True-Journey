#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const input = args.get("--input");
const phaseSlug = args.get("--phase-slug");
const requiredLanes = (args.get("--required-lanes") || "")
  .split(",")
  .map((item) => item.trim())
  .filter(Boolean);
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!input || !phaseSlug || requiredLanes.length === 0 || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_phase_advance_guard.mjs --phase-slug <slug> --input <status-json> --required-lanes <csv> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const completionStatuses = new Set([
  "FINAL_MESSAGE_READY_AND_VALIDATED",
  "FINAL_MARKER_OBSERVED",
  "PASS_APP_LANE_COMPLETION_GATE",
  "COMPLETED_AND_VALIDATED",
  "completed",
]);

const statusPayload = JSON.parse(readFileSync(input, "utf8"));
const lanes = Array.isArray(statusPayload.lane_status) ? statusPayload.lane_status : [];
const laneByName = new Map(lanes.map((lane) => [lane.lane, lane]));

const laneChecks = requiredLanes.map((laneName) => {
  const lane = laneByName.get(laneName);
  const status = lane?.status || "MISSING_LANE_STATUS";
  const completed = completionStatuses.has(status);
  return {
    lane: laneName,
    observed_status: status,
    route_family: lane?.route_family || null,
    completed,
    evidence_present: Boolean(lane?.evidence),
  };
});

const missingOrOpen = laneChecks
  .filter((check) => !check.completed)
  .map((check) => `${check.lane}:${check.observed_status}`);

const sourceAdvanceState =
  statusPayload.advance_state && typeof statusPayload.advance_state === "object"
    ? statusPayload.advance_state
    : {};
const sourceAllowsAdvance = sourceAdvanceState.next_phase_allowed === true;
const durationIsProof = sourceAdvanceState.duration_is_completion_proof === true;
const publication = statusPayload.publication_boundary || {};
const claim = statusPayload.claim_boundary || {};

const boundaryFailures = [];
for (const [key, value] of Object.entries(publication)) {
  if (key.startsWith("raw_") && value === true) {
    boundaryFailures.push(`${key}:true`);
  }
}
if (publication.credentials_published === true) boundaryFailures.push("credentials_published:true");
if (publication.screenshots_published === true) boundaryFailures.push("screenshots_published:true");
if (publication.local_absolute_paths_published === true) boundaryFailures.push("local_absolute_paths_published:true");
if (claim.phase_completion && claim.phase_completion !== "not_claimed") {
  boundaryFailures.push(`phase_completion:${claim.phase_completion}`);
}
if (claim.canon_promotion && claim.canon_promotion !== "not_claimed") {
  boundaryFailures.push(`canon_promotion:${claim.canon_promotion}`);
}

const guardOpenGaps = [];
if (missingOrOpen.length) guardOpenGaps.push(...missingOrOpen);
if (!sourceAllowsAdvance) guardOpenGaps.push("source_advance_state:false");
if (durationIsProof) guardOpenGaps.push("duration_is_completion_proof:true");
guardOpenGaps.push(...boundaryFailures);

const overallStatus = guardOpenGaps.length === 0 ? "PASS_PHASE_ADVANCE_GUARD" : "BLOCK_PHASE_ADVANCE_GUARD";

const receipt = {
  artifact_type: "ghc_phase_advance_guard",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  input,
  overall_status: overallStatus,
  required_lanes: requiredLanes,
  lane_checks: laneChecks,
  source_advance_state: {
    next_phase_allowed: sourceAllowsAdvance,
    duration_is_completion_proof: durationIsProof,
    reason: sourceAdvanceState.reason || null,
  },
  open_gaps: [...new Set(guardOpenGaps)].sort(),
  next_phase_allowed_by_guard: overallStatus === "PASS_PHASE_ADVANCE_GUARD",
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_thread_ids_published: false,
    raw_callable_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
    phase_completion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Phase Advance Guard`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${overallStatus}\``,
  "",
  "## Required Lane Checks",
  "",
  ...laneChecks.map(
    (check) =>
      `- ${check.lane}: \`${check.observed_status}\`, route \`${check.route_family || "unknown"}\`, completed \`${check.completed}\``,
  ),
  "",
  "## Source Advance State",
  "",
  `- next_phase_allowed: \`${sourceAllowsAdvance}\``,
  `- duration_is_completion_proof: \`${durationIsProof}\``,
  sourceAdvanceState.reason ? `- reason: ${sourceAdvanceState.reason}` : "- reason: none",
  "",
  "## Open Gaps",
  "",
  ...(receipt.open_gaps.length ? receipt.open_gaps.map((gap) => `- \`${gap}\``) : ["- none"]),
  "",
  "## Guard Decision",
  "",
  overallStatus === "PASS_PHASE_ADVANCE_GUARD"
    ? "The guard permits next-phase movement from this evidence set."
    : "The guard blocks next-phase movement from this evidence set. Publish a blocker or restore missing lanes before closure.",
  "",
  "## Boundary",
  "",
  "No raw lane text, raw ChatGPT transcript, raw app-server result or error, thread IDs, callable IDs, credentials, screenshots, local absolute paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: overallStatus, open_gaps: receipt.open_gaps }, null, 2));

if (overallStatus !== "PASS_PHASE_ADVANCE_GUARD") {
  process.exit(1);
}
