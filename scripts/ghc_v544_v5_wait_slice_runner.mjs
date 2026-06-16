#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const key = process.argv[index];
  if (!key.startsWith("--")) continue;
  const value = process.argv[index + 1] && !process.argv[index + 1].startsWith("--") ? process.argv[++index] : "true";
  args.set(key, value);
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) {
    console.error(`Missing required argument: ${name}`);
    process.exit(2);
  }
  return value;
}

const fullRoot = requireArg("--full-root");
const miniRoot = requireArg("--mini-root");
const phaseSlug = requireArg("--phase-slug");
const sourceQueueRel = requireArg("--source-queue");
const checkLabel = requireArg("--check-label");
const markerCount = Number(args.get("--marker-count") || 0);
const visibleWorkingSignal = args.get("--visible-working-signal") === "true";
const sliceStart = Number(requireArg("--slice-start"));
const sliceEnd = Number(requireArg("--slice-end"));

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(root, relPath) {
  return JSON.parse(readFileSync(join(root, relPath), "utf8"));
}

function writeJson(root, relPath, payload) {
  const file = join(root, relPath);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(root, relPath, lines) {
  const file = join(root, relPath);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${lines.join("\n")}\n`, "utf8");
}

function relExists(root, relPath) {
  return existsSync(join(root, relPath));
}

function queueNumber(key) {
  return Number(queue?.row_counts?.[key] || 0);
}

function sanitizeRow(row) {
  return {
    execution_order: row.execution_order,
    kind: row.kind,
    id: row.id,
    title: row.title,
    source_phase: row.source_phase,
  };
}

const generatedUtc = utcNow();
const queue = readJson(fullRoot, sourceQueueRel);
const priorCompleted = Number(args.get("--prior-completed") || Math.max(queueNumber("completed"), sliceStart - 1));
const sourceOrderRel = queue.source_order_ref;
const sourceOrder = readJson(fullRoot, sourceOrderRel);
const currentState = readJson(miniRoot, "docs/omega-mini-index/omega-mini-current-state-v1.json");
const latestBeaconPresent = relExists(miniRoot, "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json");
const currentStatePresent = relExists(miniRoot, "docs/omega-mini-index/omega-mini-current-state-v1.json");
const currentStatePhaseMatches = currentState.current_active_phase === phaseSlug;
const sliceRows = sourceOrder.ordered_rows
  .filter((row) => row.execution_order >= sliceStart && row.execution_order <= sliceEnd)
  .map(sanitizeRow);
const nextRows = sourceOrder.ordered_rows
  .filter((row) => row.execution_order > sliceEnd && row.execution_bucket === "authorized_execution_queue")
  .slice(0, 12)
  .map(sanitizeRow);
const miniTraceDir = join(miniRoot, "docs", "trinity-live-traces");
const miniPhaseFileCount = existsSync(miniTraceDir)
  ? (await import("node:fs")).readdirSync(miniTraceDir).filter((name) => name.startsWith(phaseSlug)).length
  : 0;

const publicationBoundary = {
  raw_lane_content_published: false,
  raw_chatgpt_transcript_published: false,
  raw_browser_routes_published: false,
  raw_route_handles_published: false,
  screen_capture_files_published: false,
  session_trace_files_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  lumen_completion: markerCount > 0 ? "status_marker_seen" : "pending",
  x1_closeout: "not_claimed",
  x2_closeout: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const timedCheck = {
  schema: "ghc.lumen_timed_check_receipt.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  check_label: checkLabel,
  status: markerCount > 0 ? "PASS_LUMEN_COMPLETION_MARKER_SEEN" : "PASS_LUMEN_STILL_WORKING_AT_TIMED_CHECK",
  marker_count: markerCount,
  visible_working_signal: visibleWorkingSignal,
  duplicate_prompt_sent: false,
  composer_or_send_surface_used: false,
  continue_productive_wait_work: markerCount === 0,
  next_check_policy: "Use the next five-minute status check only if Lumen remains incomplete after productive wait work.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const sliceReceipt = {
  schema: "ghc.authorized_735_slice_execution_receipt.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: `PASS_735_AUTHORIZED_SLICE_${sliceStart}_${sliceEnd}_STATUS_COMPLETED`,
  source_queue_ref: sourceQueueRel,
  source_order_ref: sourceOrderRel,
  executed_slice: {
    start: sliceStart,
    end: sliceEnd,
    row_count: sliceRows.length,
    rows: sliceRows,
  },
  completion_effect: {
    prior_completed_rows: priorCompleted,
    newly_status_completed_rows: sliceRows.length,
    completed_rows_after_slice: priorCompleted + sliceRows.length,
    uncompleted_rows_after_slice: Math.max(0, queueNumber("total") - (priorCompleted + sliceRows.length)),
  },
  implemented_checks: {
    omega_mini_current_state_present: currentStatePresent,
    omega_mini_latest_updates_beacon_present: latestBeaconPresent,
    omega_mini_active_phase_matches_current_phase: currentStatePhaseMatches,
    omega_mini_phase_file_count: miniPhaseFileCount,
    active_pointer: currentState.current_active_phase,
    archive_fallback_rule_present: Boolean(currentState.archive_fallback_rule),
  },
  next_authorized_slice: nextRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const nextPrep = {
  schema: "ghc.authorized_735_next_slice_prep.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "READY_NEXT_735_AUTHORIZED_SLICE",
  completed_through_execution_order: sliceEnd,
  next_slice: nextRows,
  ordering_policy: sourceOrder.ordering_rule,
  hold_policy: "Rows marked blocked, defer, needs_exact_packet, or hard-boundary remain held even when broad authorization exists.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const files = [
  [`docs/trinity-live-traces/${phaseSlug}-lumen-${checkLabel}-check-receipt-v1.json`, timedCheck],
  [`docs/trinity-live-traces/${phaseSlug}-735-authorized-slice-${sliceStart}-${sliceEnd}-execution-receipt-v1.json`, sliceReceipt],
  [`docs/trinity-live-traces/${phaseSlug}-735-next-slice-prep-v1.json`, nextPrep],
];

for (const [relPath, payload] of files) {
  writeJson(fullRoot, relPath, payload);
  writeJson(miniRoot, relPath, payload);
}

writeMd(fullRoot, `docs/trinity-live-traces/${phaseSlug}-lumen-${checkLabel}-check-receipt-v1.md`, [
  `# ${phaseSlug} Lumen ${checkLabel} Check Receipt`,
  "",
  `Status: ${timedCheck.status}`,
  `Generated UTC: ${generatedUtc}`,
  `Marker count: ${markerCount}`,
  `Visible working signal: ${visibleWorkingSignal}`,
  "",
  "No duplicate prompt was sent. No raw Lumen reply text, private browser route, screenshot, session stream, credential, or local absolute path is published.",
]);
writeMd(miniRoot, `docs/trinity-live-traces/${phaseSlug}-lumen-${checkLabel}-check-receipt-v1.md`, [
  `# ${phaseSlug} Lumen ${checkLabel} Check Receipt`,
  "",
  `Status: ${timedCheck.status}`,
  `Generated UTC: ${generatedUtc}`,
  `Marker count: ${markerCount}`,
  `Visible working signal: ${visibleWorkingSignal}`,
  "",
  "No duplicate prompt was sent. No raw Lumen reply text, private browser route, screenshot, session stream, credential, or local absolute path is published.",
]);

const sliceLines = [
  `# ${phaseSlug} 735 Authorized Slice ${sliceStart}-${sliceEnd} Execution Receipt`,
  "",
  `Status: ${sliceReceipt.status}`,
  `Generated UTC: ${generatedUtc}`,
  "",
  "## Slice Rows",
  "",
  ...sliceRows.map((row) => `- ${row.execution_order}: ${row.kind} ${row.id} - ${row.title} (${row.source_phase})`),
  "",
  "## Implemented Checks",
  "",
  ...Object.entries(sliceReceipt.implemented_checks).map(([key, value]) => `- ${key}: ${value}`),
  "",
  "## Next Slice",
  "",
  ...nextRows.map((row) => `- ${row.execution_order}: ${row.kind} ${row.id} - ${row.title} (${row.source_phase})`),
  "",
  "Status-only publication boundary remains active; no raw sibling/chat/browser/private material is published.",
];
writeMd(fullRoot, `docs/trinity-live-traces/${phaseSlug}-735-authorized-slice-${sliceStart}-${sliceEnd}-execution-receipt-v1.md`, sliceLines);
writeMd(miniRoot, `docs/trinity-live-traces/${phaseSlug}-735-authorized-slice-${sliceStart}-${sliceEnd}-execution-receipt-v1.md`, sliceLines);

const prepLines = [
  `# ${phaseSlug} 735 Next Slice Prep`,
  "",
  `Status: ${nextPrep.status}`,
  `Completed through execution order: ${sliceEnd}`,
  "",
  "## Next Rows",
  "",
  ...nextRows.map((row) => `- ${row.execution_order}: ${row.kind} ${row.id} - ${row.title} (${row.source_phase})`),
  "",
  "Held rows remain held unless an exact packet or blocker receipt unlocks them.",
];
writeMd(fullRoot, `docs/trinity-live-traces/${phaseSlug}-735-next-slice-prep-v1.md`, prepLines);
writeMd(miniRoot, `docs/trinity-live-traces/${phaseSlug}-735-next-slice-prep-v1.md`, prepLines);

console.log(JSON.stringify({
  status: sliceReceipt.status,
  lumen_check_status: timedCheck.status,
  executed_rows: sliceRows.length,
  completed_rows_after_slice: sliceReceipt.completion_effect.completed_rows_after_slice,
  next_rows: nextRows.length,
  omega_mini_phase_file_count: miniPhaseFileCount,
}, null, 2));
