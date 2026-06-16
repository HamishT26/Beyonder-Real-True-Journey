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
const activeLanes = splitCsv(args.get("--active-lanes"));
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
  activeLanes.length === 0 ||
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
    "Usage: node ghc_grouped_lane_x1_receipt_builder.mjs --phase-slug <slug> --next-scope <slug> --prep-json <json> --active-lanes <csv> [--cli-quality-json <json> --cli-marker-json <json>] [--app-runner-json <json> --app-gate-json <json>] [--lumen-marker-count <n>] --lumen-receipt-json <json> --lumen-receipt-md <md> --receipt-json <json> --receipt-md <md> --handoff-json <json> --handoff-md <md> --guard-json <json> --guard-md <md>",
  );
  process.exit(2);
}

function splitCsv(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJsonMaybe(path) {
  if (!path) return null;
  return JSON.parse(readFileSync(path, "utf8"));
}

function refName(path) {
  return path ? basename(path) : null;
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function routeForLane(lane) {
  if (lane === "Lumen Vale") return "in-app Browser ChatGPT panel";
  if (lane === "Arby" || lane === "Aster Vale") return "read-only Codex CLI lane";
  return "existing app lane through recovered map runner";
}

function cliQualityLaneAliases(lane) {
  if (lane === "Aster Vale") return ["Aster Vale", "Aster"];
  return [lane];
}

const generatedUtc = utcNow();
const prep = readJsonMaybe(prepJson);
const cliQuality = readJsonMaybe(cliQualityJson);
const cliMarker = readJsonMaybe(cliMarkerJson);
const appRunner = readJsonMaybe(appRunnerJson);
const appGate = readJsonMaybe(appGateJson);

const cliRows = Array.isArray(cliQuality?.lanes) ? cliQuality.lanes : [];
const appExpected = appGate?.expected_lanes || (Array.isArray(appGate?.lanes) ? appGate.lanes.map((lane) => lane.lane).filter(Boolean) : []);
const appRowsCompleted =
  Array.isArray(appGate?.lanes) &&
  appGate.lanes.length > 0 &&
  appGate.lanes.every((lane) => lane.overall_status === "completed" || lane.status === "completed" || String(lane.overall_status || "").startsWith("PASS"));

const prepReady =
  String(prep?.status || "").includes("READY") ||
  prep?.overall_status === "PASS_PROMPTS_BUILT";
const lumenRequired = activeLanes.includes("Lumen Vale");
const lumenPass = !lumenRequired || lumenMarkerCount >= 1;
const cliRequired = activeLanes.some((lane) => lane === "Arby" || lane === "Aster Vale");
const cliQualityPass = !cliRequired || cliQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE";
const cliMarkerPass =
  !cliRequired ||
  cliMarker?.status === "PASS_MARKER_REVIEW_LEDGER" ||
  cliMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const appRequired = activeLanes.some((lane) => lane === "Cicero" || lane === "Kierkegaard" || lane === "Aristotle");
const appGatePass =
  !appRequired ||
  appGate?.status === "PASS_APP_LANE_COMPLETION_GATE" ||
  appGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE" ||
  (appGate?.overall_status === "PASS" && appRowsCompleted);
const appRunnerPass =
  !appRequired ||
  appRunner?.status === "PASS_RECOVERED_APP_LANE_RUN" ||
  appRunner?.overall_status === "PASS_RECOVERED_APP_LANE_RUN" ||
  appRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" ||
  appRunner?.overall_status === "PASS" ||
  (appRunner?.background_watch_requested === true && appGatePass);

const laneSummary = activeLanes.map((lane) => {
  if (lane === "Lumen Vale") {
    return {
      lane,
      route_family: routeForLane(lane),
      status: lumenPass ? "PASS_LUMEN_BROWSER_MARKER_STATUS" : "OPEN_GAP_LUMEN_BROWSER_MARKER_STATUS",
      raw_reply_content_published: false,
    };
  }
  if (lane === "Arby" || lane === "Aster Vale") {
    const aliases = cliQualityLaneAliases(lane);
    const row = cliRows.find((candidate) => aliases.includes(candidate.lane));
    return {
      lane,
      route_family: routeForLane(lane),
      status: row?.quality_status || "MISSING_CLI_QUALITY",
      word_count: row?.word_count || null,
      final_message_hash: row?.final_message_hash || null,
      raw_reply_content_published: false,
    };
  }
  return {
    lane,
    route_family: routeForLane(lane),
    status: appGatePass && (appExpected.length === 0 || appExpected.includes(lane)) ? "PASS_APP_LANE_COMPLETION_GATE" : "OPEN_GAP_APP_LANE",
    raw_reply_content_published: false,
    raw_route_handle_published: false,
  };
});

const allLaneStatusesPass = laneSummary.every((lane) => String(lane.status || "").startsWith("PASS"));
const allPass = prepReady && lumenPass && cliQualityPass && cliMarkerPass && appRunnerPass && appGatePass && allLaneStatusesPass;

const publicationBoundary = {
  raw_lane_content_published: false,
  raw_chatgpt_transcript_published: false,
  raw_route_handles_published: false,
  raw_app_server_payload_published: false,
  raw_thread_ids_published: false,
  raw_callable_ids_published: false,
  credentials_published: false,
  screen_capture_files_published: false,
  local_absolute_paths_published: false,
  raw_user_text_published: false,
};

const claimBoundary = {
  x1_status_scope: allPass ? "closed_for_status_scope_only" : "open_gap",
  x2_closeout: "not_claimed",
  campaign_completion: "not_claimed",
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
  status: lumenRequired ? (lumenPass ? "PASS_LUMEN_BROWSER_MARKER_STATUS" : "OPEN_GAP_LUMEN_BROWSER_MARKER_STATUS") : "NOT_REQUIRED_FOR_ACTIVE_GROUP",
  marker_count: lumenMarkerCount,
  raw_chatgpt_transcript_published: false,
  raw_url_published: false,
  screen_capture_file_published: false,
};

const receipt = {
  artifact_type: "ghc_grouped_lane_x1_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allPass ? "PASS_GROUPED_LANE_X1_STATUS" : "OPEN_GAP_GROUPED_LANE_X1_STATUS",
  active_lanes: activeLanes,
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
    active_lane_count: laneSummary.length,
    lumen_marker_present_when_required: lumenPass,
    cli_quality_pass_when_required: cliQualityPass,
    cli_marker_review_pass_when_required: cliMarkerPass,
    app_runner_pass_when_required: appRunnerPass,
    app_lane_gate_pass_when_required: appGatePass,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const x2Tasks = [
  ["x2-01", "Active-group proposal reducer", "Reduce only the active-group advisory artifacts into the next x2 build queue."],
  ["x2-02", "Read-only web and GitHub prompt boundary", "Ask active siblings to use read-only web/GitHub context if exposed while publishing only status receipts."],
  ["x2-03", "Lumen build-plan executor", "Treat Lumen proposals as high-priority local build candidates executed by Aletheon under repo guards."],
  ["x2-04", "Grouped cadence continuity", "Carry the Lumen, Arby+Cicero, Lumen, Aster+Kierkegaard+Aristotle pattern forward."],
  ["x2-05", "No limited phase regression", "Reject limited-phase shortcuts unless the user explicitly asks for one."],
    ["x2-06", "Private evidence firewall", "Keep raw transcripts, route handles, thread IDs, screen-capture files, and credentials out of publication."],
  ["x2-07", "Five-minute blocker retry watch", "Retry route blockers with distinct methods before carry-forward."],
  ["x2-08", "x2 build/test/use ledger", "Record build, run, test, install, use, and defer outcomes from the active-group proposals."],
  ["x2-09", "Context compact reminder", "Include the grouped cadence, open gates, and no-raw-publication policy in handoffs."],
  ["x2-10", "Next active group prep", "Prepare the next grouped x1 lane set rather than a six-lane default."],
  ["x2-11", "Approval checklist continuation", "Refresh approval scope and completion rows after the grouped x1 lane finishes."],
  ["x2-12", "Eureka tracker continuation", "Track active-group x2 candidates as completed, uncompleted, deferred, blocked, or exact-packet gated."],
  ["x2-13", "Omega-mini lookup hardening", "Keep exact omega-mini lookup files fresh and avoid broad archive searches for active siblings."],
  ["x2-14", "D-drive-first runtime check", "Record status-only evidence that active generated artifacts stay in the D-drive worktrees."],
  ["x2-15", "Runner placement repair", "Detect and repair path-prefix mistakes before publication, using exact file moves only."],
  ["x2-16", "App notifier schema compatibility", "Keep recovered app-lane completion evidence compatible with grouped receipt builders."],
  ["x2-17", "CLI marker false-positive policy", "Preserve marker-review ledgers so generic wording does not block valid CLI advisory output."],
  ["x2-18", "Sibling evidence digest", "Summarize word counts, completion status, and safe proposal counts without publishing raw responses."],
  ["x2-19", "Next Lumen solo prep", "Prepare Lumen's next solo x1 lookup bundle after the v4 x2 closeout."],
  ["x2-20", "Open-gate continuity rail", "Carry all empirical, legal, canon, deployment, purchase, and account-mutation gates forward as open unless exact evidence changes them."],
].map(([id, title, action]) => ({ id, title, status: "safe_now", action }));

const handoff = {
  artifact_type: "ghc_grouped_lane_x1_x2_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: allPass ? "READY_FOR_GROUPED_X2_BUILD_USE" : "OPEN_GAP_BEFORE_GROUPED_X2_BUILD_USE",
  source_receipt: refName(receiptJson),
  x2_task_count: x2Tasks.length,
  x2_tasks: x2Tasks,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const guard = {
  artifact_type: "ghc_grouped_lane_x1_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: allPass ? "PASS" : "OPEN_GAP",
  checks: {
    prep_card_ready: prepReady,
    active_lane_count_positive: laneSummary.length > 0,
    all_active_lane_statuses_pass: allLaneStatusesPass,
    required_lumen_marker_pass: lumenPass,
    required_cli_quality_pass: cliQualityPass,
    required_app_gate_pass: appGatePass,
    raw_private_material_published: false,
    closure_claims_published: false,
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
  "- Raw ChatGPT transcript, URL, screen-capture file, and route details are not published.",
]);

writeMd(receiptMd, [
  `# ${phaseSlug} Grouped-Lane X1 Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Active lanes: \`${activeLanes.join(", ")}\``,
  "",
  "## Lane Summary",
  "",
  ...laneSummary.map((lane) => `- ${lane.lane}: \`${lane.status}\`; route \`${lane.route_family}\`.`),
]);

writeMd(handoffMd, [
  `# ${phaseSlug} Grouped X1 to X2 Handoff`,
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
  `# ${phaseSlug} Grouped-Lane X1 Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${guard.status}\``,
  "",
  ...Object.entries(guard.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
]);

console.log(JSON.stringify({ status: receipt.status, handoff_status: handoff.status, guard_status: guard.status, active_lane_count: activeLanes.length }, null, 2));
