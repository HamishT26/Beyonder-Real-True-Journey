#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhase = args.get("--next-phase") || "next-phase";
const boardJson = args.get("--board-json");
const routeBoardJson = args.get("--route-board-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !boardJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_blocker_boundary_packet_builder.mjs --phase-slug <slug> --board-json <partial-board-json> --receipt-json <json> --receipt-md <md> [--next-phase <slug>] [--route-board-json <json>]",
  );
  process.exit(2);
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const board = readJson(boardJson);
const routeBoard = routeBoardJson ? readJson(routeBoardJson) : null;
const lanes = Array.isArray(board.lane_status) ? board.lane_status : [];
const openLanes = lanes.filter((lane) => !["FINAL_MESSAGE_READY_AND_VALIDATED", "FINAL_MARKER_OBSERVED", "COMPLETED_AND_VALIDATED", "completed"].includes(lane.status));
const completedLanes = lanes.filter((lane) => !openLanes.includes(lane));
const routeOpenRows = Array.isArray(routeBoard?.open_lane_rows) ? routeBoard.open_lane_rows : [];

const approvalPacket = {
  title: `${phaseSlug} to ${nextPhase} Blocker-Boundary Override Candidate`,
  status: "PENDING_USER_APPROVAL",
  purpose:
    "Allow preparation-only or limited next-phase design work to continue while preserving explicit open app-lane blockers.",
  approved_if_signed: [
    "Carry the open app-lane blocker into the next phase without claiming completion.",
    "Continue route-recovery tooling, watcher cadence, source refresh, and approval drafting.",
    "Use completed Browser and CLI lane evidence only for route-specific synthesis.",
    "Publish curated blocker, route-family, and no-replacement receipts.",
    "Retry official thread-tool discovery or private-map preflight only when safe route evidence changes.",
  ],
  not_approved: [
    "Claiming v507 v8 completion.",
    "Treating Browser or CLI completion as Kierkegaard or Aristotle app-lane completion.",
    "Creating replacement siblings, replacement lanes, or new old-style subagents.",
    "Publishing raw transcripts, private IDs, screenshots, credentials, local private paths, or app-server raw payloads.",
    "Promoting GMUT, final physics, solved consciousness, empirical closure, legal closure, or canon claims.",
  ],
  required_receipts: [
    "partial board preserving open app-lane rows",
    "route-family status board",
    "no-replacement sibling guard",
    "phase-advance guard showing blocked or explicitly waived state",
    "exposure and no-overclaim guards",
  ],
};

const receipt = {
  artifact_type: "ghc_blocker_boundary_packet_builder",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  next_phase: nextPhase,
  input_board: boardJson,
  input_route_board: routeBoardJson || null,
  status: openLanes.length > 0 ? "PENDING_APPROVAL_OPEN_BLOCKER_BOUNDARY" : "NO_OPEN_BLOCKER_BOUNDARY_NEEDED",
  completed_lanes: completedLanes.map((lane) => ({
    lane: lane.lane,
    route_family: lane.route_family,
    status: lane.status,
  })),
  open_lanes: openLanes.map((lane) => ({
    lane: lane.lane,
    route_family: lane.route_family,
    status: lane.status,
  })),
  route_open_rows: routeOpenRows,
  approval_packet: approvalPacket,
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
  `# ${approvalPacket.title}`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Purpose",
  "",
  approvalPacket.purpose,
  "",
  "## Completed Route-Specific Evidence",
  "",
  ...(receipt.completed_lanes.length
    ? receipt.completed_lanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Open Blockers To Preserve",
  "",
  ...(receipt.open_lanes.length
    ? receipt.open_lanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Approved If Signed",
  "",
  ...approvalPacket.approved_if_signed.map((item) => `- ${item}`),
  "",
  "## Not Approved",
  "",
  ...approvalPacket.not_approved.map((item) => `- ${item}`),
  "",
  "## Required Receipts",
  "",
  ...approvalPacket.required_receipts.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "This is a pending approval candidate, not an approval and not a phase-completion claim. It publishes no raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, GMUT closure, or canon promotion.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, open_lanes: receipt.open_lanes }, null, 2));
