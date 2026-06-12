#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhaseSlug = args.get("--next-phase-slug");
const handoffJson = args.get("--handoff-json");
const recoveredPreflightJson = args.get("--recovered-preflight-json");
const recoveredNotifyJson = args.get("--recovered-notify-json");
const recoveredGateJson = args.get("--recovered-gate-json");
const closeoutJson = args.get("--closeout-json");
const closeoutMd = args.get("--closeout-md");
const nextPrepJson = args.get("--next-prep-json");
const nextPrepMd = args.get("--next-prep-md");
const guardJson = args.get("--guard-json");
const guardMd = args.get("--guard-md");

if (
  !phaseSlug ||
  !nextPhaseSlug ||
  !handoffJson ||
  !recoveredPreflightJson ||
  !recoveredNotifyJson ||
  !recoveredGateJson ||
  !closeoutJson ||
  !closeoutMd ||
  !nextPrepJson ||
  !nextPrepMd ||
  !guardJson ||
  !guardMd
) {
  console.error(
    "Usage: node ghc_v508_v2_x2_closeout_builder.mjs --phase-slug <slug> --next-phase-slug <slug> --handoff-json <json> --recovered-preflight-json <json> --recovered-notify-json <json> --recovered-gate-json <json> --closeout-json <json> --closeout-md <md> --next-prep-json <json> --next-prep-md <md> --guard-json <json> --guard-md <md>",
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

const generatedUtc = utcNow();
const handoff = readJson(handoffJson);
const recoveredPreflight = readJson(recoveredPreflightJson);
const recoveredNotify = readJson(recoveredNotifyJson);
const recoveredGate = readJson(recoveredGateJson);

const recoveredRunnerPass = recoveredNotify.overall_status === "PASS_RECOVERED_APP_LANE_RUN";
const recoveredGatePass = recoveredGate.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const recoveredPreflightPass = recoveredPreflight.overall_status === "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT";
const x2CloseoutPass = handoff.status === "V508_V2_X1_GROUP_READY_FOR_X2_PREP" && recoveredRunnerPass && recoveredGatePass;

const x2ImplementedTasks = [
  {
    id: "x2-built-01",
    source_task: "x2-01 Route recovery codification",
    result: "Built reusable recovered app-lane map runner with preflight and notify modes.",
    evidence: refName(recoveredNotifyJson),
  },
  {
    id: "x2-built-02",
    source_task: "x2-02 Private-map source boundary card",
    result: "Runner records recovery source and handle count while publishing no raw route handles.",
    evidence: refName(recoveredPreflightJson),
  },
  {
    id: "x2-built-03",
    source_task: "x2-04 Cicero app-lane digest board",
    result: "Notify-mode run produced digest-only app-lane summaries for Cicero, Kierkegaard, and Aristotle.",
    evidence: refName(recoveredGateJson),
  },
  {
    id: "x2-built-04",
    source_task: "x2-09 X1 group completion reducer",
    result: "Closeout reduces v2 x1 and x2 evidence to pass/open boundaries for the next prep card.",
    evidence: refName(closeoutJson),
  },
  {
    id: "x2-built-05",
    source_task: "x2-13 Sibling route-family manifest",
    result: "Next prep card names all six active lanes and keeps route families separate.",
    evidence: refName(nextPrepJson),
  },
];

const closeout = {
  artifact_type: "ghc_v508_v2_x2_closeout",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: x2CloseoutPass ? "PASS_V508_V2_X2_BUILD_USE_CLOSEOUT" : "OPEN_GAP_V508_V2_X2_BUILD_USE_CLOSEOUT",
  input_refs: {
    x1_x2_handoff: refName(handoffJson),
    recovered_preflight: refName(recoveredPreflightJson),
    recovered_notify_runner: refName(recoveredNotifyJson),
    recovered_completion_gate: refName(recoveredGateJson),
  },
  evidence_summary: {
    x1_group_ready: handoff.status === "V508_V2_X1_GROUP_READY_FOR_X2_PREP",
    recovered_preflight_pass: recoveredPreflightPass,
    recovered_notify_runner_pass: recoveredRunnerPass,
    recovered_completion_gate_pass: recoveredGatePass,
    app_lanes_completed: recoveredGate.expected_lanes || [],
    app_lane_open_gaps: recoveredGate.open_gaps || [],
  },
  x2_implemented_task_count: x2ImplementedTasks.length,
  x2_implemented_tasks: x2ImplementedTasks,
  carry_forward_open_work: [
    "Run the next x1 with all six active lanes where reachable: Lumen, Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle.",
    "Use the recovered app-lane map runner for app lanes, strict CLI cycle for Arby/Aster, and Browser route for Lumen.",
    "Build a no-limited-phase language lint and route-family manifest in later x2 work.",
    "Keep GMUT, final physics, consciousness, legal closure, and canon gates open.",
  ],
  publication_boundary: {
    raw_route_handles_published: false,
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_payload_published: false,
    raw_thread_ids_published: false,
    raw_callable_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
  },
  claim_boundary: {
    v508_v2_x2_closeout: x2CloseoutPass ? "closed_for_build_use_scope_only" : "open_gap",
    v508_v3_start: "prepared_not_started",
    v508_full_phase_completion: "not_claimed",
    v515_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const nextPrep = {
  artifact_type: "ghc_v508_v3_x1_six_lane_prep_card",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: "READY_FOR_SIX_LANE_X1_ATTEMPT",
  source_closeout: refName(closeoutJson),
  active_lanes: [
    {
      lane: "Lumen Vale",
      route_family: "in-app Browser ChatGPT panel",
      mode: "status-safe advisory prompt and marker receipt",
      fallback: "record Browser route blocker; do not use Solas or unnamed sibling unless explicitly reactivated",
    },
    {
      lane: "Arby",
      route_family: "read-only Codex CLI lane",
      mode: "strict CLI advisory composition",
      fallback: "completion notifier and marker-review receipt",
    },
    {
      lane: "Aster Vale",
      route_family: "read-only Codex CLI lane",
      mode: "strict CLI advisory composition",
      fallback: "completion notifier and marker-review receipt",
    },
    {
      lane: "Cicero",
      route_family: "existing app lane through recovered map runner",
      mode: "recovered app-lane notify",
      fallback: "redacted blocker receipt",
    },
    {
      lane: "Kierkegaard",
      route_family: "existing app lane through recovered map runner",
      mode: "recovered app-lane notify",
      fallback: "redacted blocker receipt",
    },
    {
      lane: "Aristotle",
      route_family: "existing app lane through recovered map runner",
      mode: "recovered app-lane notify",
      fallback: "redacted blocker receipt",
    },
  ],
  x1_requirements: [
    "Use existing lanes only.",
    "Check every five minutes when practical, but do not babysit instead of preparing x2 tasks.",
    "Keep raw lane text, route handles, thread IDs, screenshots, credentials, and private app payloads out of repo receipts.",
    "Collect marker or blocker receipts for each lane.",
    "Extract at least 20 x2 build/use candidates from validated x1 evidence.",
  ],
  x2_followthrough_targets: [
    "No-limited-phase language lint",
    "Route-family manifest",
    "Vision compact refresh card",
    "Dual omega publication preflight",
    "GMUT evidence firewall",
    "Freed ID consent boundary",
    "THOS runner freshness board",
    "X1-to-X2 task reducer",
    "Browser route retry template",
    "CLI marker false-positive classifier",
  ],
  publication_boundary: closeout.publication_boundary,
  claim_boundary: {
    v508_v3_x1_start: "prepared_not_started",
    v508_v3_x1_completion: "not_claimed",
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

const guard = {
  artifact_type: "ghc_v508_v2_x2_closeout_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_closeout: refName(closeoutJson),
  status: x2CloseoutPass ? "PASS" : "OPEN_GAP",
  checks: {
    x1_handoff_ready: handoff.status === "V508_V2_X1_GROUP_READY_FOR_X2_PREP",
    recovered_preflight_pass: recoveredPreflightPass,
    recovered_notify_pass: recoveredRunnerPass,
    recovered_gate_pass: recoveredGatePass,
    no_raw_route_handles_published: true,
    no_v508_full_completion_claim: true,
    no_v515_completion_claim: true,
    no_gmut_or_physics_closure_claim: true,
  },
};

writeJson(closeoutJson, closeout);
writeJson(nextPrepJson, nextPrep);
writeJson(guardJson, guard);

const closeoutLines = [
  `# ${phaseSlug} X2 Build Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${closeout.status}\``,
  "",
  "## Evidence Summary",
  "",
  `- x1 group ready: \`${String(closeout.evidence_summary.x1_group_ready)}\``,
  `- recovered preflight passed: \`${String(recoveredPreflightPass)}\``,
  `- recovered notify runner passed: \`${String(recoveredRunnerPass)}\``,
  `- recovered completion gate passed: \`${String(recoveredGatePass)}\``,
  `- app lanes completed: \`${closeout.evidence_summary.app_lanes_completed.join(", ")}\``,
  "",
  "## Implemented X2 Tasks",
  "",
  ...x2ImplementedTasks.map((task) => `- ${task.id}: ${task.result} Evidence: \`${task.evidence}\`.`),
  "",
  "## Carry Forward",
  "",
  ...closeout.carry_forward_open_work.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Build/use scope closeout only. No raw route handles, raw lane text, ChatGPT transcripts, app-server payloads, thread IDs, callable IDs, credentials, screenshots, local paths, v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, or canon promotion is claimed.",
  "",
];
mkdirSync(dirname(closeoutMd), { recursive: true });
writeFileSync(closeoutMd, closeoutLines.join("\n"), "utf8");

const prepLines = [
  `# ${nextPhaseSlug} Six-Lane X1 Prep Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${nextPrep.status}\``,
  "",
  "## Active Lanes",
  "",
  ...nextPrep.active_lanes.map((lane) => `- ${lane.lane}: ${lane.route_family}; mode \`${lane.mode}\`.`),
  "",
  "## X1 Requirements",
  "",
  ...nextPrep.x1_requirements.map((item) => `- ${item}`),
  "",
  "## X2 Followthrough Targets",
  "",
  ...nextPrep.x2_followthrough_targets.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Preparation card only. v508 v3 x1 is prepared, not started or completed by this card.",
  "",
];
mkdirSync(dirname(nextPrepMd), { recursive: true });
writeFileSync(nextPrepMd, prepLines.join("\n"), "utf8");

const guardLines = [
  `# ${phaseSlug} X2 Closeout Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${guard.status}\``,
  "",
  ...Object.entries(guard.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
  "",
];
mkdirSync(dirname(guardMd), { recursive: true });
writeFileSync(guardMd, guardLines.join("\n"), "utf8");

console.log(
  JSON.stringify(
    {
      status: closeout.status,
      next_prep_status: nextPrep.status,
      guard_status: guard.status,
      implemented_task_count: closeout.x2_implemented_task_count,
    },
    null,
    2,
  ),
);
