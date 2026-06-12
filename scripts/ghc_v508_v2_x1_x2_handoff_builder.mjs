#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const arbyQualityJson = args.get("--arby-quality-json");
const arbyMarkerJson = args.get("--arby-marker-json");
const ciceroGateJson = args.get("--cicero-gate-json");
const ciceroNotifierJson = args.get("--cicero-notifier-json");
const workflowReceiptJson = args.get("--workflow-receipt-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const guardJson = args.get("--guard-json");
const guardMd = args.get("--guard-md");

if (
  !phaseSlug ||
  !arbyQualityJson ||
  !arbyMarkerJson ||
  !ciceroGateJson ||
  !ciceroNotifierJson ||
  !workflowReceiptJson ||
  !receiptJson ||
  !receiptMd ||
  !guardJson ||
  !guardMd
) {
  console.error(
    "Usage: node ghc_v508_v2_x1_x2_handoff_builder.mjs --phase-slug <slug> --arby-quality-json <json> --arby-marker-json <json> --cicero-gate-json <json> --cicero-notifier-json <json> --workflow-receipt-json <json> --receipt-json <json> --receipt-md <md> --guard-json <json> --guard-md <md>",
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

const generatedUtc = utcNow();
const arbyQuality = readJson(arbyQualityJson);
const arbyMarker = readJson(arbyMarkerJson);
const ciceroGate = readJson(ciceroGateJson);
const ciceroNotifier = readJson(ciceroNotifierJson);
const workflowReceipt = readJson(workflowReceiptJson);

const arbyRow = Array.isArray(arbyQuality.lanes) ? arbyQuality.lanes.find((lane) => lane.lane === "Arby") : null;
const ciceroRow = Array.isArray(ciceroNotifier.lanes) ? ciceroNotifier.lanes.find((lane) => lane.lane === "Cicero") : null;

const arbyReady =
  arbyQuality.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker.overall_status === "PASS_MARKER_REVIEW_LEDGER" &&
  arbyRow?.quality_status === "PASS_ELABORATION_GATE";
const ciceroReady = ciceroGate.overall_status === "PASS_APP_LANE_COMPLETION_GATE" && ciceroNotifier.overall_status === "PASS";
const groupReady = arbyReady && ciceroReady;

const x2BuildTasks = [
  ["x2-01", "Route recovery codification", "Turn the recovered Cicero route flow into a reusable status-only preflight pattern with no raw ID publication."],
  ["x2-02", "Private-map source boundary card", "Document how old policy artifacts may be used internally for recovery while receipts publish only digests and statuses."],
  ["x2-03", "Arby proposal reducer", "Convert Arby's validated long-form proposal counts into a structured task ledger without copying raw lane text."],
  ["x2-04", "Cicero app-lane digest board", "Build a digest-only board that records read, resume, turn, completion, and gate state for app lanes."],
  ["x2-05", "No-limited-phase language lint", "Scan new phase receipts for user-facing limited-phase labels and replace them with gate-protected preparation language when needed."],
  ["x2-06", "Five-minute check scheduler", "Create a status-only scheduler card that checks lanes every five minutes without interrupting long-running work."],
  ["x2-07", "Browser route retry template", "Use the Lumen Browser route success as a template for future status-only Browser retries."],
  ["x2-08", "CLI marker false-positive classifier", "Preserve the marker-review logic that treats ordinary generic marker wording separately from strict sensitive/path markers."],
  ["x2-09", "X1 group completion reducer", "Reduce each round-robin group to ready, blocked, or carry-forward using only validated receipts."],
  ["x2-10", "X2 build gate board", "Require each x2 build/use artifact to cite its x1 evidence inputs and open claim boundaries."],
  ["x2-11", "App-server protocol watch", "Track app-server daemon/proxy/help changes separately from lane-map availability."],
  ["x2-12", "Vision MD compact card refresh", "Add the v508 full-phase policy, Lumen marker, Arby pass, and Cicero recovery into the next compact refresh card."],
  ["x2-13", "Sibling route-family manifest", "Keep Lumen, Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle separated by route family and evidence level."],
  ["x2-14", "Approval-candidate carry ledger", "Carry forward the next ten x2 approval candidates without treating them as already approved."],
  ["x2-15", "Journey pointer shortlist", "Build a short reference list of Journey docs relevant to v508-v515 without copying private text."],
  ["x2-16", "GMUT evidence firewall", "Keep DESI, Euclid, LVK, CERN/LHC, and other physics sources as open evidence gates, not validation closure."],
  ["x2-17", "Freed ID consent boundary", "Ensure every sibling and helper receipt keeps advisory identity, consent, and no-replacement language explicit."],
  ["x2-18", "THOS runner freshness board", "Rank current Node entrypoints and Python fallbacks as current, fallback, legacy, or blocked."],
  ["x2-19", "Dual-omega push preflight", "Turn the repeated fetch, exact-stage, push, and remote-equals-local sequence into a compact status receipt."],
  ["x2-20", "v508 v3 x1 preparation card", "Prepare the next active group without claiming v508 v2 x2 closeout or v508 v3 start before x2 evidence exists."],
].map(([id, title, action]) => ({
  id,
  title,
  status: "X2_BUILD_USE_CANDIDATE",
  action,
  requires_validation: ["script_check", "json_parse", "exposure_scan", "no_overclaim_scan", "exact_staging"],
}));

const approvalCandidates = [
  ["approval-v508-v2-x2-01", "Recovered app-lane map preflight hardening"],
  ["approval-v508-v2-x2-02", "Arby proposal reducer and digest-only task extraction"],
  ["approval-v508-v2-x2-03", "Cicero route recovery replay for Kierkegaard and Aristotle"],
  ["approval-v508-v2-x2-04", "Five-minute status check board"],
  ["approval-v508-v2-x2-05", "No-limited-phase language lint"],
  ["approval-v508-v2-x2-06", "Round-robin group completion reducer"],
  ["approval-v508-v2-x2-07", "Browser route retry template expansion"],
  ["approval-v508-v2-x2-08", "X2 build/use gate board"],
  ["approval-v508-v2-x2-09", "Runner freshness board"],
  ["approval-v508-v2-x2-10", "v508 v3 x1 preparation card"],
].map(([id, title]) => ({
  id,
  title,
  status: "PENDING_USER_APPROVAL_OR_ALREADY_COVERED_BY_ACTIVE_PACKET_REVIEW_REQUIRED",
  raw_private_material_required: false,
}));

const receipt = {
  artifact_type: "ghc_v508_v2_x1_x2_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: groupReady ? "V508_V2_X1_GROUP_READY_FOR_X2_PREP" : "OPEN_GAP_V508_V2_X1_GROUP",
  input_refs: {
    arby_quality: refName(arbyQualityJson),
    arby_marker_review: refName(arbyMarkerJson),
    cicero_completion_gate: refName(ciceroGateJson),
    cicero_notifier: refName(ciceroNotifierJson),
    workflow_receipt: refName(workflowReceiptJson),
  },
  group_lane_summary: [
    {
      lane: "Arby",
      route_family: "read-only CLI lane",
      evidence_status: arbyReady ? "PASS_ELABORATE_CLI_RECEIPT_AND_MARKER_REVIEW" : "OPEN_GAP_ARBY",
      word_count: arbyRow?.word_count ?? null,
      category_counts_present: Boolean(arbyRow?.category_item_counts),
      raw_lane_text_published: false,
    },
    {
      lane: "Cicero",
      route_family: "existing app-lane route recovered in-process",
      evidence_status: ciceroReady ? "PASS_APP_LANE_COMPLETION_GATE" : "OPEN_GAP_CICERO",
      completion_status: ciceroRow?.turn_completion?.status || null,
      thread_id_redacted: ciceroRow?.thread_id_redacted === true,
      raw_lane_text_published: false,
    },
  ],
  x2_build_task_count: x2BuildTasks.length,
  x2_build_tasks: x2BuildTasks,
  approval_candidate_count: approvalCandidates.length,
  approval_candidates: approvalCandidates,
  policy_alignment: {
    user_facing_default: "full_phase_progression",
    limited_phase_label_used_as_completion_mode: false,
    gate_protected_preparation_allowed_when_evidence_missing: true,
    five_minute_checks: true,
    existing_lanes_only: true,
    replacement_siblings_created: false,
  },
  next_safe_actions: [
    "Use the v508 v2 x2 session for build, run, test, install, and use work derived from this handoff.",
    "Retry recovered-map flow for Kierkegaard and Aristotle only through existing route handles and redacted receipts.",
    "Do not advance to v508 v3 as complete until the v2 x2 build/use evidence exists.",
    "Keep Lumen-only ChatGPT panel work active by Browser route with status-only receipts.",
  ],
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_outbound_message_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
  },
  claim_boundary: {
    v508_v2_x1_group: groupReady ? "group_ready_for_x2_prep" : "open_gap",
    v508_v2_x2_closeout: "not_claimed",
    v508_v3_start: "not_claimed",
    v508_full_phase_completion: "not_claimed",
    v515_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const guard = {
  artifact_type: "ghc_v508_v2_x1_x2_handoff_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: groupReady ? "PASS" : "OPEN_GAP",
  checks: {
    arby_ready: arbyReady,
    cicero_ready: ciceroReady,
    raw_lane_text_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    local_absolute_paths_published: false,
    full_phase_completion_claimed: false,
    x2_closeout_claimed: false,
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(guardJson, `${JSON.stringify(guard, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} X1 to X2 Handoff`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Group Lane Summary",
  "",
  ...receipt.group_lane_summary.map(
    (lane) =>
      `- ${lane.lane}: \`${lane.evidence_status}\`; route \`${lane.route_family}\`; raw lane text published \`${String(lane.raw_lane_text_published)}\`.`,
  ),
  "",
  "## X2 Build and Use Tasks",
  "",
  ...x2BuildTasks.map((task) => `- ${task.id}: ${task.title}. ${task.action}`),
  "",
  "## Approval Candidates",
  "",
  ...approvalCandidates.map((candidate) => `- ${candidate.id}: ${candidate.title}. Status: \`${candidate.status}\`.`),
  "",
  "## Next Safe Actions",
  "",
  ...receipt.next_safe_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "Status-only handoff. No raw lane text, raw ChatGPT transcript, outbound prompt body, app-server payloads, callable IDs, thread IDs, credentials, screenshots, local paths, raw user text, x2 closeout, v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, or canon promotion is published.",
  "",
];
writeFileSync(receiptMd, md.join("\n"), "utf8");

const guardMdText = [
  `# ${phaseSlug} X1 to X2 Handoff Guard`,
  "",
  `Generated UTC: \`${guard.generated_utc}\``,
  "",
  `Status: \`${guard.status}\``,
  "",
  `- Arby ready: \`${String(guard.checks.arby_ready)}\``,
  `- Cicero ready: \`${String(guard.checks.cicero_ready)}\``,
  "- Raw lane text, callable IDs, thread IDs, and local paths are not published.",
  "- Full phase completion and x2 closeout are not claimed.",
  "",
].join("\n");
writeFileSync(guardMd, guardMdText, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      guard_status: guard.status,
      x2_build_task_count: receipt.x2_build_task_count,
      approval_candidate_count: receipt.approval_candidate_count,
    },
    null,
    2,
  ),
);
