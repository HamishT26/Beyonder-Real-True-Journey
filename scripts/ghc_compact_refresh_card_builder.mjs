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
    "Usage: node ghc_compact_refresh_card_builder.mjs --phase-slug <slug> --board-json <partial-board-json> --receipt-json <json> --receipt-md <md> [--next-phase <slug>] [--route-board-json <json>]",
  );
  process.exit(2);
}

const board = JSON.parse(readFileSync(boardJson, "utf8"));
const routeBoard = routeBoardJson ? JSON.parse(readFileSync(routeBoardJson, "utf8")) : null;
const lanes = Array.isArray(board.lane_status) ? board.lane_status : [];
const routeFamilies = Array.isArray(routeBoard?.route_families) ? routeBoard.route_families : [];
const openRows = Array.isArray(routeBoard?.open_lane_rows)
  ? routeBoard.open_lane_rows
  : lanes
      .filter((lane) => !["FINAL_MESSAGE_READY_AND_VALIDATED", "FINAL_MARKER_OBSERVED", "COMPLETED_AND_VALIDATED", "completed"].includes(lane.status))
      .map((lane) => ({ lane: lane.lane, route_family: lane.route_family, status: lane.status }));

const card = {
  current_anchor: `${phaseSlug} remains evidence-gated; ${nextPhase} can only proceed as explicitly approved preparation while open blockers remain.`,
  proven_route_evidence: lanes
    .filter((lane) => ["FINAL_MESSAGE_READY_AND_VALIDATED", "FINAL_MARKER_OBSERVED", "COMPLETED_AND_VALIDATED", "completed"].includes(lane.status))
    .map((lane) => `${lane.lane}: ${lane.status} via ${lane.route_family}`),
  open_blockers: openRows.map((row) => `${row.lane}: ${row.status} via ${row.route_family}`),
  route_family_snapshot: routeFamilies.map((family) => `${family.route_family}: ${family.completed_count}/${family.lane_count} complete`),
  next_actions: [
    "Do not advance as complete while app-lane blockers remain open.",
    "Use Browser and CLI evidence only as route-specific evidence.",
    "Retry private-map preflight only if the route map is restored in-process.",
    "Retry official thread-tool discovery only if tools become exposed.",
    "Continue x2 build work on validators, watcher cadence, source refresh, and approval packets.",
    "Use a blocker-boundary approval packet before any next-phase movement that carries open lanes.",
  ],
  hard_boundaries: [
    "No raw lane text.",
    "No private callable or thread IDs.",
    "No replacement siblings or old-style subagents.",
    "No screenshots, credentials, or local private paths.",
    "No GMUT closure, final physics, solved consciousness, or canon promotion claim.",
  ],
};

const receipt = {
  artifact_type: "ghc_compact_refresh_card",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  next_phase: nextPhase,
  input_board: boardJson,
  input_route_board: routeBoardJson || null,
  status: openRows.length > 0 ? "COMPACT_REFRESH_CARD_OPEN_BLOCKERS" : "COMPACT_REFRESH_CARD_READY",
  card,
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
  `# ${phaseSlug} Compact Refresh Card`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Current Anchor",
  "",
  card.current_anchor,
  "",
  "## Proven Route Evidence",
  "",
  ...(card.proven_route_evidence.length ? card.proven_route_evidence.map((item) => `- ${item}`) : ["- none"]),
  "",
  "## Open Blockers",
  "",
  ...(card.open_blockers.length ? card.open_blockers.map((item) => `- ${item}`) : ["- none"]),
  "",
  "## Route-Family Snapshot",
  "",
  ...(card.route_family_snapshot.length ? card.route_family_snapshot.map((item) => `- ${item}`) : ["- not supplied"]),
  "",
  "## Next Actions",
  "",
  ...card.next_actions.map((item) => `- ${item}`),
  "",
  "## Hard Boundaries",
  "",
  ...card.hard_boundaries.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Compact-refresh card only. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, open_blockers: card.open_blockers }, null, 2));
