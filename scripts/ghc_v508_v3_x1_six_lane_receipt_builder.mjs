#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const prepJson = args.get("--prep-json");
const cliQualityJson = args.get("--cli-quality-json");
const cliMarkerJson = args.get("--cli-marker-json");
const appRunnerJson = args.get("--app-runner-json");
const appGateJson = args.get("--app-gate-json");
const lumenMarkerPresent = (args.get("--lumen-marker-present") || "false").toLowerCase() === "true";
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const handoffJson = args.get("--handoff-json");
const handoffMd = args.get("--handoff-md");
const guardJson = args.get("--guard-json");
const guardMd = args.get("--guard-md");

if (
  !phaseSlug ||
  !prepJson ||
  !cliQualityJson ||
  !cliMarkerJson ||
  !appRunnerJson ||
  !appGateJson ||
  !receiptJson ||
  !receiptMd ||
  !handoffJson ||
  !handoffMd ||
  !guardJson ||
  !guardMd
) {
  console.error(
    "Usage: node ghc_v508_v3_x1_six_lane_receipt_builder.mjs --phase-slug <slug> --prep-json <json> --cli-quality-json <json> --cli-marker-json <json> --app-runner-json <json> --app-gate-json <json> --lumen-marker-present true|false --receipt-json <json> --receipt-md <md> --handoff-json <json> --handoff-md <md> --guard-json <json> --guard-md <md>",
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

const cliPass = cliQuality.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" && cliMarker.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const appPass = appRunner.overall_status === "PASS_RECOVERED_APP_LANE_RUN" && appGate.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const sixLanePass = lumenMarkerPresent && cliPass && appPass;
const cliRows = Array.isArray(cliQuality.lanes) ? cliQuality.lanes : [];
const appLanes = Array.isArray(appGate.expected_lanes) ? appGate.expected_lanes : [];

const x2Tasks = [
  ["x2-01", "Six-lane lane-state reducer", "Build a reducer that combines Browser marker, CLI quality, app gate, and prep-card evidence into one compact phase board."],
  ["x2-02", "Lumen marker receipt card", "Create a Browser status receipt that records marker presence without raw ChatGPT transcript text."],
  ["x2-03", "CLI proposal digest extractor", "Extract only counts, hashes, headings, and task categories from Arby/Aster outputs."],
  ["x2-04", "App-lane recovered-route replay", "Replay the recovered runner for app lanes at future five-minute checks when safe."],
  ["x2-05", "Six-lane x2 build queue", "Rank the combined Lumen, CLI, and app-lane advice into a build queue without copying raw responses."],
  ["x2-06", "No-limited-phase lint", "Implement the full-phase wording guard from the current user directive."],
  ["x2-07", "Vision compact refresh update", "Write a compact card that says v508 v3 x1 has six-lane status evidence while v508/v515 remain open."],
  ["x2-08", "Route-family manifest refresh", "Update Browser, CLI, app-lane, connector, and fallback route families."],
  ["x2-09", "Five-minute check cadence board", "Create a status-only cadence receipt that avoids babysitting while honoring check windows."],
  ["x2-10", "Approval packet queue", "Prepare ten candidate approval packets for v508 v3 x2 and v508 v4 x1."],
  ["x2-11", "GMUT evidence firewall", "Keep all physics and empirical gates open in every downstream task."],
  ["x2-12", "Freed ID consent boundary", "Ensure all sibling-lane receipts preserve advisory identity and no-replacement rules."],
  ["x2-13", "THOS runner freshness matrix", "Classify the recovered app runner, strict CLI cycle, Browser route, and fallback runners."],
  ["x2-14", "Dual-omega publication preflight", "Generate a reusable publication checklist for both omega branches."],
  ["x2-15", "Source-ledger bridge", "Attach official-source references to x2 runner choices where useful."],
  ["x2-16", "Journey pointer shortlist", "Create a compact list of Journey docs relevant to v508 without copying private text."],
  ["x2-17", "Aster-specific sandbox note", "Turn Aster Vale's CLI pass into sandbox/TUI follow-up candidates."],
  ["x2-18", "Arby publication-safety note", "Turn Arby's CLI pass into staging, push, and evidence-governance candidates."],
  ["x2-19", "App-lane ethics/taxonomy note", "Use Cicero/Kierkegaard/Aristotle completion as a route proof, not raw advisory proof."],
  ["x2-20", "v508 v4 x1 launcher card", "Prepare the next six-lane x1 attempt after v3 x2 closeout exists."],
].map(([id, title, action]) => ({ id, title, status: "X2_BUILD_USE_CANDIDATE", action }));

const approvalCandidates = Array.from({ length: 10 }, (_, index) => ({
  id: `approval-v508-v3-x2-${String(index + 1).padStart(2, "0")}`,
  title: [
    "Six-lane lane-state reducer",
    "Browser marker receipt card",
    "CLI proposal digest extractor",
    "App-lane recovered-route replay",
    "Six-lane x2 build queue",
    "No-limited-phase lint",
    "Vision compact refresh update",
    "Route-family manifest refresh",
    "Five-minute check cadence board",
    "Dual-omega publication preflight",
  ][index],
  status: "PENDING_USER_APPROVAL_OR_ACTIVE_PACKET_COVERAGE_REVIEW_REQUIRED",
  raw_private_material_required: false,
}));

const receipt = {
  artifact_type: "ghc_v508_v3_x1_six_lane_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: sixLanePass ? "PASS_V508_V3_X1_SIX_LANE_STATUS" : "OPEN_GAP_V508_V3_X1_SIX_LANE_STATUS",
  input_refs: {
    prep_card: refName(prepJson),
    cli_quality: refName(cliQualityJson),
    cli_marker_review: refName(cliMarkerJson),
    app_runner: refName(appRunnerJson),
    app_completion_gate: refName(appGateJson),
  },
  lane_summary: [
    {
      lane: "Lumen Vale",
      route_family: "in-app Browser ChatGPT panel",
      status: lumenMarkerPresent ? "FINAL_MARKER_OBSERVED_STATUS_ONLY" : "OPEN_GAP_MARKER_NOT_OBSERVED",
      raw_reply_text_published: false,
    },
    ...cliRows.map((lane) => ({
      lane: lane.lane,
      route_family: "read-only Codex CLI lane",
      status: lane.quality_status,
      word_count: lane.word_count,
      final_message_hash: lane.final_message_hash,
      raw_reply_text_published: false,
    })),
    ...appLanes.map((lane) => ({
      lane,
      route_family: "existing app lane through recovered map runner",
      status: "PASS_APP_LANE_COMPLETION_GATE",
      raw_reply_text_published: false,
      raw_route_handle_published: false,
    })),
  ],
  evidence_gates: {
    prep_card_ready: prep.status === "READY_FOR_SIX_LANE_X1_ATTEMPT",
    lumen_marker_present: lumenMarkerPresent,
    cli_quality_pass: cliPass,
    app_lane_gate_pass: appPass,
    six_lane_count: 1 + cliRows.length + appLanes.length,
  },
  publication_boundary: {
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
  },
  claim_boundary: {
    v508_v3_x1: sixLanePass ? "closed_for_status_scope_only" : "open_gap",
    v508_v3_x2_closeout: "not_claimed",
    v508_full_phase_completion: "not_claimed",
    v515_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const handoff = {
  artifact_type: "ghc_v508_v3_x1_x2_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: "v508-gmut-thos-v44-v3-x2",
  status: sixLanePass ? "READY_FOR_V508_V3_X2_BUILD_USE" : "OPEN_GAP_BEFORE_V508_V3_X2",
  source_receipt: refName(receiptJson),
  x2_task_count: x2Tasks.length,
  x2_tasks: x2Tasks,
  approval_candidate_count: approvalCandidates.length,
  approval_candidates: approvalCandidates,
  boundary: receipt.claim_boundary,
};

const guard = {
  artifact_type: "ghc_v508_v3_x1_six_lane_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: sixLanePass ? "PASS" : "OPEN_GAP",
  checks: {
    lumen_marker_present: lumenMarkerPresent,
    cli_quality_pass: cliPass,
    app_lane_gate_pass: appPass,
    six_lane_count_is_six: receipt.evidence_gates.six_lane_count === 6,
    raw_private_material_published: false,
    v508_full_completion_claimed: false,
    v515_completion_claimed: false,
    gmut_or_physics_closure_claimed: false,
  },
};

writeJson(receiptJson, receipt);
writeJson(handoffJson, handoff);
writeJson(guardJson, guard);

writeMd(receiptMd, [
  `# ${phaseSlug} Six-Lane X1 Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Lane Summary",
  "",
  ...receipt.lane_summary.map((lane) => `- ${lane.lane}: \`${lane.status}\`; route \`${lane.route_family}\`.`),
  "",
  "## Boundaries",
  "",
  "- Raw lane text, ChatGPT transcript, route handles, app-server payloads, thread IDs, callable IDs, credentials, screenshots, local paths, and raw user text are not published.",
  "- v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain unclaimed.",
  "",
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
  "",
  "## Approval Candidates",
  "",
  ...approvalCandidates.map((candidate) => `- ${candidate.id}: ${candidate.title}. Status: \`${candidate.status}\`.`),
  "",
]);

writeMd(guardMd, [
  `# ${phaseSlug} Six-Lane Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${guard.status}\``,
  "",
  ...Object.entries(guard.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
  "",
]);

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      handoff_status: handoff.status,
      guard_status: guard.status,
      six_lane_count: receipt.evidence_gates.six_lane_count,
      x2_task_count: handoff.x2_task_count,
    },
    null,
    2,
  ),
);
