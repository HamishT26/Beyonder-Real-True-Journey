#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const boardJson = args.get("--board-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !boardJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_route_family_status_board.mjs --phase-slug <slug> --board-json <partial-board-json> --receipt-json <json> --receipt-md <md>",
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

const board = JSON.parse(readFileSync(boardJson, "utf8"));
const lanes = Array.isArray(board.lane_status) ? board.lane_status : [];

const familyMap = new Map();
for (const lane of lanes) {
  const familyName = lane.route_family || "unknown";
  if (!familyMap.has(familyName)) {
    familyMap.set(familyName, {
      route_family: familyName,
      lane_count: 0,
      completed_count: 0,
      open_count: 0,
      lanes: [],
    });
  }
  const row = familyMap.get(familyName);
  const status = lane.status || "MISSING_STATUS";
  const completed = completionStatuses.has(status);
  row.lane_count += 1;
  if (completed) row.completed_count += 1;
  else row.open_count += 1;
  row.lanes.push({
    lane: lane.lane || "unknown",
    status,
    completed,
    evidence_present: Boolean(lane.evidence),
  });
}

const routeFamilies = [...familyMap.values()].sort((left, right) =>
  left.route_family.localeCompare(right.route_family),
);
const openLaneRows = routeFamilies.flatMap((family) =>
  family.lanes
    .filter((lane) => !lane.completed)
    .map((lane) => ({
      route_family: family.route_family,
      lane: lane.lane,
      status: lane.status,
    })),
);

const advanceState = board.advance_state && typeof board.advance_state === "object" ? board.advance_state : {};
const nextPhaseAllowed = advanceState.next_phase_allowed === true && openLaneRows.length === 0;
const overallStatus = nextPhaseAllowed
  ? "PASS_ROUTE_FAMILY_STATUS_BOARD"
  : "OPEN_GAP_ROUTE_FAMILY_STATUS_BOARD";

const receipt = {
  artifact_type: "ghc_route_family_status_board",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  input: boardJson,
  overall_status: overallStatus,
  lane_count: lanes.length,
  route_family_count: routeFamilies.length,
  route_families: routeFamilies,
  open_lane_rows: openLaneRows,
  advance_state: {
    source_next_phase_allowed: advanceState.next_phase_allowed === true,
    next_phase_allowed: nextPhaseAllowed,
    duration_is_completion_proof: advanceState.duration_is_completion_proof === true,
    reason: nextPhaseAllowed
      ? "all required route-family lane rows are complete"
      : "one or more route-family lane rows remain open or source advance state is false",
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
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Route-Family Status Board`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${overallStatus}\``,
  "",
  "## Route Families",
  "",
  ...routeFamilies.flatMap((family) => [
    `- ${family.route_family}: ${family.completed_count}/${family.lane_count} complete`,
    ...family.lanes.map((lane) => `  - ${lane.lane}: \`${lane.status}\``),
  ]),
  "",
  "## Open Lane Rows",
  "",
  ...(openLaneRows.length
    ? openLaneRows.map((row) => `- ${row.lane} (${row.route_family}): \`${row.status}\``)
    : ["- none"]),
  "",
  "## Advance State",
  "",
  `- Source next phase allowed: \`${receipt.advance_state.source_next_phase_allowed}\``,
  `- Board next phase allowed: \`${receipt.advance_state.next_phase_allowed}\``,
  `- Duration is completion proof: \`${receipt.advance_state.duration_is_completion_proof}\``,
  `- Reason: ${receipt.advance_state.reason}`,
  "",
  "## Boundary",
  "",
  "Status-only route-family board. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: overallStatus, open_lane_rows: openLaneRows }, null, 2));

if (overallStatus !== "PASS_ROUTE_FAMILY_STATUS_BOARD") {
  process.exit(1);
}
