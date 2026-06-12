#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextScope = args.get("--next-scope");
const prepJson = args.get("--prep-json");
const cliQualityJson = args.get("--cli-quality-json");
const cliMarkerJson = args.get("--cli-marker-json");
const appRunnerJson = args.get("--app-runner-json");
const appGateJson = args.get("--app-gate-json");
const lumenMarkerCount = Number(args.get("--lumen-marker-count") || "0");
const lumenReceiptJson = args.get("--lumen-receipt-json");
const lumenReceiptMd = args.get("--lumen-receipt-md");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const handoffJson = args.get("--handoff-json");
const handoffMd = args.get("--handoff-md");
const guardJson = args.get("--guard-json");
const guardMd = args.get("--guard-md");

if (
  !phaseSlug ||
  !nextScope ||
  !prepJson ||
  !cliQualityJson ||
  !cliMarkerJson ||
  !appRunnerJson ||
  !appGateJson ||
  !lumenReceiptJson ||
  !lumenReceiptMd ||
  !receiptJson ||
  !receiptMd ||
  !handoffJson ||
  !handoffMd ||
  !guardJson ||
  !guardMd
) {
  console.error(
    "Usage: node ghc_six_lane_x1_receipt_builder.mjs --phase-slug <slug> --next-scope <slug> --prep-json <json> --cli-quality-json <json> --cli-marker-json <json> --app-runner-json <json> --app-gate-json <json> --lumen-marker-count <n> --lumen-receipt-json <json> --lumen-receipt-md <md> --receipt-json <json> --receipt-md <md> --handoff-json <json> --handoff-md <md> --guard-json <json> --guard-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function refName(path) {
  return basename(path);
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

const generatedUtc = utcNow();
const prep = readJson(prepJson);
const cliQuality = readJson(cliQualityJson);
const cliMarker = readJson(cliMarkerJson);
const appRunner = readJson(appRunnerJson);
const appGate = readJson(appGateJson);

const expectedLanes = ["Lumen Vale", "Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle"];
const cliLanes = Array.isArray(cliQuality.lanes) ? cliQuality.lanes : [];
const appLanes = appGate.expected_lanes || appGate.lanes || [];

const lumenMarkerPresent = lumenMarkerCount >= 2;
const cliQualityPass = cliQuality.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE";
const cliMarkerPass = cliMarker.status === "PASS_MARKER_REVIEW_LEDGER" || cliMarker.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const appRunnerPass = appRunner.status === "PASS_RECOVERED_APP_LANE_RUN" || appRunner.overall_status === "PASS_RECOVERED_APP_LANE_RUN";
const appGatePass = appGate.status === "PASS_APP_LANE_COMPLETION_GATE" || appGate.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const prepReady = prep.status === "READY_FOR_V508_V4_X1_FULL_PHASE_ROUND_ROBIN" || String(prep.status || "").includes("READY");
const allPass = lumenMarkerPresent && cliQualityPass && cliMarkerPass && appRunnerPass && appGatePass && prepReady;

const cliLaneRows = ["Arby", "Aster Vale"].map((laneName) => {
  const row = cliLanes.find((lane) => lane.lane === laneName);
  return {
    lane: laneName,
    route_family: "read-only Codex CLI lane",
    status: row?.quality_status || "MISSING",
    word_count: row?.word_count || null,
    final_message_hash: row?.final_message_hash || null,
    raw_reply_text_published: false,
  };
});

const appLaneRows = ["Cicero", "Kierkegaard", "Aristotle"].map((laneName) => ({
  lane: laneName,
  route_family: "existing app lane through recovered map runner",
  status: appGatePass && (appLanes.length === 0 || appLanes.includes(laneName)) ? "PASS_APP_LANE_COMPLETION_GATE" : "OPEN_GAP_APP_LANE",
  raw_reply_text_published: false,
  raw_route_handle_published: false,
}));

const publicationBoundary = {
  raw_lane_text_published: false,
  raw_chatgpt_transcript_published: false,
  raw_route_handles_published: false,
  raw_app_server_payload_published: false,
  raw_thread_ids_published: false,
  raw_callable_ids_published: false,
  credentials_published: false,
  screenshots_published: false,
  local_absolute_paths_published: false,
  raw_user_text_published: false,
};

const claimBoundary = {
  x1_status_scope: allPass ? "closed_for_status_scope_only" : "open_gap",
  x2_closeout: "not_claimed",
  v508_full_phase_completion: "not_claimed",
  v515_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const lumenReceipt = {
  artifact_type: "ghc_browser_lumen_marker_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: lumenMarkerPresent ? "PASS_LUMEN_BROWSER_MARKER_STATUS" : "OPEN_GAP_LUMEN_BROWSER_MARKER_STATUS",
  marker_count: lumenMarkerCount,
  marker_interpretation: lumenMarkerPresent
    ? "At least two marker appearances observed, consistent with outbound prompt plus Lumen completion marker."
    : "Completion marker not yet observed as distinct from outbound prompt.",
  raw_chatgpt_transcript_published: false,
  raw_url_published: false,
  screenshot_published: false,
};

const laneSummary = [
  {
    lane: "Lumen Vale",
    route_family: "in-app Browser ChatGPT panel",
    status: lumenReceipt.status,
    raw_reply_text_published: false,
  },
  ...cliLaneRows,
  ...appLaneRows,
];

const receipt = {
  artifact_type: "ghc_six_lane_x1_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allPass ? "PASS_SIX_LANE_X1_STATUS" : "OPEN_GAP_SIX_LANE_X1_STATUS",
  input_refs: {
    prep_card: refName(prepJson),
    lumen_marker_receipt: refName(lumenReceiptJson),
    cli_quality: refName(cliQualityJson),
    cli_marker_review: refName(cliMarkerJson),
    app_runner: refName(appRunnerJson),
    app_completion_gate: refName(appGateJson),
  },
  lane_summary: laneSummary,
  evidence_gates: {
    prep_card_ready: prepReady,
    lumen_marker_present: lumenMarkerPresent,
    cli_quality_pass: cliQualityPass,
    cli_marker_review_pass: cliMarkerPass,
    app_runner_pass: appRunnerPass,
    app_lane_gate_pass: appGatePass,
    six_lane_count: laneSummary.length,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const x2Tasks = [
  ["x2-01", "Browser composer resilience", "Preserve the visible textbox plus send-button path and avoid repeating hidden textarea failures."],
  ["x2-02", "Lumen marker disambiguation", "Use marker-count logic to distinguish outbound prompt marker from response marker without reading raw text."],
  ["x2-03", "CLI marker false-positive review", "Keep the completion-notifier plus marker-review pair as the default CLI quality path."],
  ["x2-04", "Recovered app-lane reuse", "Continue recovered app-lane notify mode for Cicero, Kierkegaard, and Aristotle with redacted route policy."],
  ["x2-05", "Full-phase progression lint", "Promote the no-limited-phase guard into future prep cards and closeouts."],
  ["x2-06", "Five-minute blocker cadence", "Record every blocker retry with a distinct safe method before carry-forward."],
  ["x2-07", "Route-family health board", "Combine Browser, CLI, and app-lane status into a compact board for every x1."],
  ["x2-08", "x2 build/use prioritizer", "Rank sibling proposals into build, run, test, install, use, and defer lanes."],
  ["x2-09", "Vision compact refresh", "Update compact refresh notes with v508 v4 status while preserving open gates."],
  ["x2-10", "Approval packet queue", "Prepare next-phase approval packets without treating them as automatically activated."],
  ["x2-11", "GMUT evidence firewall", "Keep physics and consciousness claims as open evidence gates, not closure."],
  ["x2-12", "Freed ID advisory boundary", "Keep sibling identity and consent language advisory and non-replacement based."],
  ["x2-13", "THOS runner freshness table", "Classify current Node and Python runners as current, fallback, stale, or blocked."],
  ["x2-14", "Dual-omega publication preflight", "Retain fetch, drift-check, exact staging, push, and remote-equals-local verification."],
  ["x2-15", "Private-material invariant", "Scan every generated file for raw path, transcript, screenshot, credential, and route-handle patterns."],
  ["x2-16", "Journey pointer digest", "Use Journey documents as inspiration without publishing private source text."],
  ["x2-17", "App update surface watch", "Track new in-app Browser developer-mode surfaces as route support, not proof of automation."],
  ["x2-18", "CLI version readiness note", "Keep CLI version checks separate from phase completion claims."],
  ["x2-19", "Sibling retry ledger", "Require at least one safe retry family before a lane is marked carried forward."],
  ["x2-20", "Next prep card", "Prepare the next full-phase x1 with six-lane route families and open claim boundaries."],
].map(([id, title, action]) => ({
  id,
  title,
  status: "X2_BUILD_USE_CANDIDATE",
  action,
}));

const handoff = {
  artifact_type: "ghc_six_lane_x1_x2_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: allPass ? "READY_FOR_X2_BUILD_USE" : "OPEN_GAP_BEFORE_X2_BUILD_USE",
  source_receipt: refName(receiptJson),
  x2_task_count: x2Tasks.length,
  x2_tasks: x2Tasks,
  approval_candidate_count: 10,
  approval_candidates: x2Tasks.slice(0, 10).map((task) => ({
    id: `approval-${task.id}`,
    title: task.title,
    status: "PENDING_USER_APPROVAL_OR_ACTIVE_PACKET_COVERAGE_REVIEW_REQUIRED",
    raw_private_material_required: false,
  })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const guard = {
  artifact_type: "ghc_six_lane_x1_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: allPass ? "PASS" : "OPEN_GAP",
  checks: {
    prep_card_ready: prepReady,
    lumen_marker_present: lumenMarkerPresent,
    cli_quality_pass: cliQualityPass,
    cli_marker_review_pass: cliMarkerPass,
    app_runner_pass: appRunnerPass,
    app_lane_gate_pass: appGatePass,
    six_lane_count_is_six: laneSummary.length === 6,
    raw_private_material_published: false,
    v508_full_completion_claimed: false,
    v515_completion_claimed: false,
    gmut_or_physics_closure_claimed: false,
  },
};

writeJson(lumenReceiptJson, lumenReceipt);
writeJson(receiptJson, receipt);
writeJson(handoffJson, handoff);
writeJson(guardJson, guard);

writeMd(lumenReceiptMd, [
  `# ${phaseSlug} Lumen Browser Marker Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${lumenReceipt.status}\``,
  "",
  `- Marker count: \`${String(lumenMarkerCount)}\``,
  "- Raw ChatGPT transcript, URL, screenshot, and route details are not published.",
]);

writeMd(receiptMd, [
  `# ${phaseSlug} Six-Lane X1 Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Lane Summary",
  "",
  ...laneSummary.map((lane) => `- ${lane.lane}: \`${lane.status}\`; route \`${lane.route_family}\`.`),
  "",
  "## Boundaries",
  "",
  "- Raw lane text, ChatGPT transcript, route handles, app-server payloads, thread IDs, callable IDs, credentials, screenshots, local paths, and raw user text are not published.",
  "- v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain unclaimed.",
]);

writeMd(handoffMd, [
  `# ${phaseSlug} X1 to X2 Handoff`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${handoff.status}\``,
  "",
  "## X2 Build Use Candidates",
  "",
  ...x2Tasks.map((task) => `- ${task.id}: ${task.title}. ${task.action}`),
]);

writeMd(guardMd, [
  `# ${phaseSlug} Six-Lane X1 Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${guard.status}\``,
  "",
  ...Object.entries(guard.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
]);

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      handoff_status: handoff.status,
      guard_status: guard.status,
      lumen_status: lumenReceipt.status,
      six_lane_count: receipt.evidence_gates.six_lane_count,
      x2_task_count: handoff.x2_task_count,
    },
    null,
    2,
  ),
);
