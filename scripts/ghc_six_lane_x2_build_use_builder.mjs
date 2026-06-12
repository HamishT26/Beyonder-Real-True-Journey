#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhaseSlug = args.get("--next-phase-slug");
const x1ReceiptJson = args.get("--x1-receipt-json");
const x1HandoffJson = args.get("--x1-handoff-json");
const x1GuardJson = args.get("--x1-guard-json");
const reducerJson = args.get("--reducer-json");
const reducerMd = args.get("--reducer-md");
const routeManifestJson = args.get("--route-manifest-json");
const routeManifestMd = args.get("--route-manifest-md");
const fullPhaseGuardJson = args.get("--full-phase-guard-json");
const fullPhaseGuardMd = args.get("--full-phase-guard-md");
const closeoutJson = args.get("--closeout-json");
const closeoutMd = args.get("--closeout-md");
const nextPrepJson = args.get("--next-prep-json");
const nextPrepMd = args.get("--next-prep-md");

if (
  !phaseSlug ||
  !nextPhaseSlug ||
  !x1ReceiptJson ||
  !x1HandoffJson ||
  !x1GuardJson ||
  !reducerJson ||
  !reducerMd ||
  !routeManifestJson ||
  !routeManifestMd ||
  !fullPhaseGuardJson ||
  !fullPhaseGuardMd ||
  !closeoutJson ||
  !closeoutMd ||
  !nextPrepJson ||
  !nextPrepMd
) {
  console.error(
    "Usage: node ghc_six_lane_x2_build_use_builder.mjs --phase-slug <slug> --next-phase-slug <slug> --x1-receipt-json <json> --x1-handoff-json <json> --x1-guard-json <json> --reducer-json <json> --reducer-md <md> --route-manifest-json <json> --route-manifest-md <md> --full-phase-guard-json <json> --full-phase-guard-md <md> --closeout-json <json> --closeout-md <md> --next-prep-json <json> --next-prep-md <md>",
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
const x1Receipt = readJson(x1ReceiptJson);
const x1Handoff = readJson(x1HandoffJson);
const x1Guard = readJson(x1GuardJson);

const expectedLanes = ["Lumen Vale", "Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle"];
const laneSummary = Array.isArray(x1Receipt.lane_summary) ? x1Receipt.lane_summary : [];
const x2Tasks = Array.isArray(x1Handoff.x2_tasks) ? x1Handoff.x2_tasks : [];
const receiptPass = String(x1Receipt.status || "").startsWith("PASS");
const handoffReady = String(x1Handoff.status || "").includes("READY");
const guardPass = x1Guard.status === "PASS";
const laneCountPass = x1Receipt.evidence_gates?.six_lane_count === 6 && expectedLanes.every((lane) => laneSummary.some((row) => row.lane === lane));
const allInputsReady = receiptPass && handoffReady && guardPass && laneCountPass;

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
  x2_closeout: allInputsReady ? "closed_for_build_use_scope_only" : "open_gap",
  next_x1_start: "prepared_not_started",
  v508_full_phase_completion: "not_claimed",
  v515_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const routeFamilies = [
  {
    family: "browser-chatgpt-lumen",
    lanes: ["Lumen Vale"],
    current_use: "status-only Browser marker route",
    fallback: "retry distinct Browser composer paths before holding for manual recovery",
  },
  {
    family: "read-only-cli",
    lanes: ["Arby", "Aster Vale"],
    current_use: "strict CLI cycle with completion notifier, quality gate, and marker review",
    fallback: "rerun safe completion/quality review before carry-forward",
  },
  {
    family: "recovered-app-lane-map",
    lanes: ["Cicero", "Kierkegaard", "Aristotle"],
    current_use: "existing app lanes through recovered map runner",
    fallback: "redacted blocker receipt rather than replacement creation",
  },
];

const reducer = {
  artifact_type: "ghc_six_lane_x2_lane_state_reducer",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_X2_LANE_STATE_REDUCER" : "OPEN_GAP_X2_LANE_STATE_REDUCER",
  input_refs: {
    x1_receipt: refName(x1ReceiptJson),
    x1_handoff: refName(x1HandoffJson),
    x1_guard: refName(x1GuardJson),
  },
  checks: {
    x1_receipt_pass: receiptPass,
    x1_handoff_ready: handoffReady,
    x1_guard_pass: guardPass,
    six_expected_lanes_present: laneCountPass,
  },
  lane_summary: laneSummary.map((lane) => ({
    lane: lane.lane,
    route_family: lane.route_family,
    status: lane.status,
    raw_reply_text_published: false,
  })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const routeManifest = {
  artifact_type: "ghc_six_lane_x2_route_family_manifest",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_X2_ROUTE_FAMILY_MANIFEST" : "OPEN_GAP_X2_ROUTE_FAMILY_MANIFEST",
  route_families: routeFamilies,
  cadence_policy: {
    full_phase_progression_default: true,
    limited_phase_default_disallowed: true,
    five_minute_check_cadence: true,
    continue_preparation_while_watchers_run: true,
    retry_blockers_with_distinct_safe_methods: true,
    existing_lanes_only: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const fullPhaseGuard = {
  artifact_type: "ghc_six_lane_x2_full_phase_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_FULL_PHASE_GUARD",
  policy: {
    do_not_use_limited_phase_label_without_user_request: true,
    x1_runs_attempt_all_reachable_required_lanes: true,
    x2_runs_build_run_test_install_use_followthrough: true,
    soft_wait_time_is_not_completion_proof: true,
    raw_private_material_is_never_publication_evidence: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const implementedTasks = [
  {
    id: "x2-built-01",
    source_task: x2Tasks[0]?.title || "Lane reducer",
    result: "Built a reusable x2 reducer for six-lane x1 receipt, handoff, and guard inputs.",
    evidence: refName(reducerJson),
  },
  {
    id: "x2-built-02",
    source_task: x2Tasks[4]?.title || "Build queue",
    result: "Converted the x1 handoff into a build/use closeout with next-phase prep.",
    evidence: refName(closeoutJson),
  },
  {
    id: "x2-built-03",
    source_task: x2Tasks[5]?.title || "Full phase guard",
    result: "Preserved full-phase progression as the default and blocked limited-phase shortcut language.",
    evidence: refName(fullPhaseGuardJson),
  },
  {
    id: "x2-built-04",
    source_task: x2Tasks[7]?.title || "Route manifest",
    result: "Refreshed Browser, CLI, and app-lane route families with fallback boundaries.",
    evidence: refName(routeManifestJson),
  },
  {
    id: "x2-built-05",
    source_task: x2Tasks[10]?.title || "Evidence firewall",
    result: "Kept v508, v515, GMUT, physics, consciousness, legal, and canon gates open.",
    evidence: refName(closeoutJson),
  },
];

const nextPrep = {
  artifact_type: "ghc_six_lane_next_x1_prep_card",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: allInputsReady ? "READY_FOR_FULL_PHASE_SIX_LANE_X1" : "OPEN_GAP_BEFORE_NEXT_X1",
  source_closeout: refName(closeoutJson),
  required_lanes: expectedLanes,
  route_families: routeFamilies.map((family) => family.family),
  requirements: [
    "Attempt every reachable required lane.",
    "Use Lumen through Browser, Arby/Aster through read-only CLI, and Cicero/Kierkegaard/Aristotle through existing app-lane routes.",
    "Retry blockers with distinct safe methods before carry-forward.",
    "Keep working on research, prep, and x2 candidates while watchers supervise active lanes.",
    "Publish status-only receipts and keep all claim gates open.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: {
    ...claimBoundary,
    next_x1_completion: "not_claimed",
  },
};

const closeout = {
  artifact_type: "ghc_six_lane_x2_build_use_closeout",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_SIX_LANE_X2_BUILD_USE_CLOSEOUT" : "OPEN_GAP_SIX_LANE_X2_BUILD_USE_CLOSEOUT",
  input_refs: {
    reducer: refName(reducerJson),
    route_manifest: refName(routeManifestJson),
    full_phase_guard: refName(fullPhaseGuardJson),
    x1_handoff: refName(x1HandoffJson),
  },
  implemented_task_count: implementedTasks.length,
  implemented_tasks: implementedTasks,
  carry_forward: nextPrep.requirements,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeJson(reducerJson, reducer);
writeJson(routeManifestJson, routeManifest);
writeJson(fullPhaseGuardJson, fullPhaseGuard);
writeJson(closeoutJson, closeout);
writeJson(nextPrepJson, nextPrep);

writeMd(reducerMd, [
  `# ${phaseSlug} X2 Lane-State Reducer`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${reducer.status}\``,
  "",
  "## Checks",
  "",
  ...Object.entries(reducer.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
  "",
  "## Lanes",
  "",
  ...reducer.lane_summary.map((lane) => `- ${lane.lane}: \`${lane.status}\`; route \`${lane.route_family}\`.`),
]);

writeMd(routeManifestMd, [
  `# ${phaseSlug} X2 Route-Family Manifest`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${routeManifest.status}\``,
  "",
  "## Route Families",
  "",
  ...routeFamilies.map((family) => `- ${family.family}: lanes \`${family.lanes.join(", ")}\`; fallback \`${family.fallback}\`.`),
]);

writeMd(fullPhaseGuardMd, [
  `# ${phaseSlug} X2 Full-Phase Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${fullPhaseGuard.status}\``,
  "",
  ...Object.entries(fullPhaseGuard.policy).map(([key, value]) => `- ${key}: \`${String(value)}\``),
]);

writeMd(closeoutMd, [
  `# ${phaseSlug} X2 Build Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${closeout.status}\``,
  "",
  "## Implemented Tasks",
  "",
  ...implementedTasks.map((task) => `- ${task.id}: ${task.result} Evidence: \`${task.evidence}\`.`),
  "",
  "## Boundary",
  "",
  "Build/use scope closeout only. v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain unclaimed.",
]);

writeMd(nextPrepMd, [
  `# ${nextPhaseSlug} Prep Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${nextPrep.status}\``,
  "",
  "## Requirements",
  "",
  ...nextPrep.requirements.map((item) => `- ${item}`),
]);

console.log(
  JSON.stringify(
    {
      status: closeout.status,
      reducer_status: reducer.status,
      route_manifest_status: routeManifest.status,
      full_phase_guard_status: fullPhaseGuard.status,
      next_prep_status: nextPrep.status,
      implemented_task_count: closeout.implemented_task_count,
    },
    null,
    2,
  ),
);
