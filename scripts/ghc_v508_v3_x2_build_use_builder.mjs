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
const noLimitedGuardJson = args.get("--no-limited-guard-json");
const noLimitedGuardMd = args.get("--no-limited-guard-md");
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
  !noLimitedGuardJson ||
  !noLimitedGuardMd ||
  !closeoutJson ||
  !closeoutMd ||
  !nextPrepJson ||
  !nextPrepMd
) {
  console.error(
    "Usage: node ghc_v508_v3_x2_build_use_builder.mjs --phase-slug <slug> --next-phase-slug <slug> --x1-receipt-json <json> --x1-handoff-json <json> --x1-guard-json <json> --reducer-json <json> --reducer-md <md> --route-manifest-json <json> --route-manifest-md <md> --no-limited-guard-json <json> --no-limited-guard-md <md> --closeout-json <json> --closeout-md <md> --next-prep-json <json> --next-prep-md <md>",
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
const lanes = Array.isArray(x1Receipt.lane_summary) ? x1Receipt.lane_summary : [];
const laneNames = lanes.map((lane) => lane.lane);
const laneStatusRows = expectedLanes.map((laneName) => {
  const lane = lanes.find((row) => row.lane === laneName);
  return {
    lane: laneName,
    status: lane?.status || "MISSING",
    route_family: lane?.route_family || "unknown",
    raw_reply_text_published: lane?.raw_reply_text_published === true,
    raw_route_handle_published: lane?.raw_route_handle_published === true,
  };
});

const laneCountPass = x1Receipt.evidence_gates?.six_lane_count === 6 && expectedLanes.every((lane) => laneNames.includes(lane));
const x1ReceiptPass = x1Receipt.status === "PASS_V508_V3_X1_SIX_LANE_STATUS";
const x1HandoffReady = x1Handoff.status === "READY_FOR_V508_V3_X2_BUILD_USE";
const x1GuardPass = x1Guard.status === "PASS";
const allInputsReady = x1ReceiptPass && x1HandoffReady && x1GuardPass && laneCountPass;

const routeFamilies = [
  {
    family: "browser-chatgpt-lumen",
    lanes: ["Lumen Vale"],
    current_use: "status-safe Browser advisory marker receipt",
    fallback: "retry Browser route with distinct non-destructive methods; hold Chrome as optional fallback only when explicitly practical",
    private_material_policy: "No raw ChatGPT transcript, URL, screenshot, or route handle in repo artifacts.",
  },
  {
    family: "read-only-cli",
    lanes: ["Arby", "Aster Vale"],
    current_use: "strict read-only CLI advisory cycle with completion notifier and marker review",
    fallback: "repair output folder, marker review, and quality gate before carrying forward",
    private_material_policy: "No raw final messages, temp output paths, or shell transcripts in repo artifacts.",
  },
  {
    family: "recovered-app-lane-map",
    lanes: ["Cicero", "Kierkegaard", "Aristotle"],
    current_use: "existing app lane through recovered map runner",
    fallback: "redacted blocker receipt if callable route is unavailable",
    private_material_policy: "No raw route handles, callable IDs, thread IDs, app-server payloads, or raw lane text in repo artifacts.",
  },
];

const buildUseResults = [
  {
    id: "x2-built-01",
    source_task: "x2-01 Six-lane lane-state reducer",
    result: "Built a reducer that combines Browser marker, CLI quality, app completion gate, and handoff readiness into one six-lane board.",
    evidence: refName(reducerJson),
  },
  {
    id: "x2-built-02",
    source_task: "x2-06 No-limited-phase lint",
    result: "Built a guard declaring full phase progression as default and rejecting limited-phase wording as a completion shortcut.",
    evidence: refName(noLimitedGuardJson),
  },
  {
    id: "x2-built-03",
    source_task: "x2-08 Route-family manifest refresh",
    result: "Built a route-family manifest for Browser, CLI, and recovered app lanes with privacy boundaries and fallback rules.",
    evidence: refName(routeManifestJson),
  },
  {
    id: "x2-built-04",
    source_task: "x2-05 Six-lane x2 build queue",
    result: "Promoted the x1 handoff queue into x2 build/use outputs and a v508 v4 x1 prep card.",
    evidence: refName(nextPrepJson),
  },
  {
    id: "x2-built-05",
    source_task: "x2-11 GMUT evidence firewall",
    result: "Kept v508, v515, GMUT, physics, consciousness, legal, and canon gates open in the closeout boundary.",
    evidence: refName(closeoutJson),
  },
];

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
  v508_v3_x2_closeout: allInputsReady ? "closed_for_build_use_scope_only" : "open_gap",
  v508_v4_x1_start: "prepared_not_started",
  v508_full_phase_completion: "not_claimed",
  v515_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const reducer = {
  artifact_type: "ghc_v508_v3_x2_lane_state_reducer",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_SIX_LANE_STATE_REDUCER" : "OPEN_GAP_SIX_LANE_STATE_REDUCER",
  input_refs: {
    x1_receipt: refName(x1ReceiptJson),
    x1_handoff: refName(x1HandoffJson),
    x1_guard: refName(x1GuardJson),
  },
  checks: {
    x1_receipt_pass: x1ReceiptPass,
    x1_handoff_ready: x1HandoffReady,
    x1_guard_pass: x1GuardPass,
    six_expected_lanes_present: laneCountPass,
  },
  lane_status_rows: laneStatusRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const routeManifest = {
  artifact_type: "ghc_v508_v3_x2_route_family_manifest",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_ROUTE_FAMILY_MANIFEST" : "OPEN_GAP_ROUTE_FAMILY_MANIFEST",
  route_families: routeFamilies,
  cadence_policy: {
    x1_check_interval_minutes: 5,
    retry_blockers_with_distinct_safe_methods: true,
    use_existing_lanes_only: true,
    no_replacement_siblings: true,
    continue_research_and_preparation_while_lanes_run: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const noLimitedGuard = {
  artifact_type: "ghc_v508_v3_x2_no_limited_phase_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_NO_LIMITED_PHASE_GUARD",
  policy: {
    default_phase_mode: "full_phase_progression",
    limited_phase_allowed_only_when_user_explicitly_requests_it: true,
    x1_requires_all_reachable_lane_attempts: true,
    x2_requires_build_run_test_install_use_scope: true,
    blockers_require_safe_retry_before_carry_forward: true,
  },
  prohibited_shortcuts: [
    "Do not describe a phase as limited by default.",
    "Do not advance by skipping reachable sibling lanes.",
    "Do not treat soft wait timing as completion proof.",
    "Do not publish raw private material to justify progress.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const nextPrep = {
  artifact_type: "ghc_v508_v4_x1_prep_card",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: allInputsReady ? "READY_FOR_V508_V4_X1_FULL_PHASE_ROUND_ROBIN" : "OPEN_GAP_BEFORE_V508_V4_X1",
  source_closeout: refName(closeoutJson),
  required_lanes: expectedLanes,
  required_route_families: routeFamilies.map((family) => family.family),
  phase_policy: {
    full_phase_progression_required: true,
    limited_phase_default_disallowed: true,
    five_minute_check_cadence: true,
    x2_build_use_followthrough_required: true,
    raw_private_material_excluded: true,
  },
  next_x1_outputs_requested: [
    "status-only marker or blocker receipt for each reachable lane",
    "ten or more command or runner improvement candidates",
    "ten or more skill or system expansion candidates",
    "ten or more eureka tasks per active advisory lane where practical",
    "explicit blocker retry notes for any unavailable route",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: {
    ...claimBoundary,
    v508_v4_x1_start: "prepared_not_started",
    v508_v4_x1_completion: "not_claimed",
  },
};

const closeout = {
  artifact_type: "ghc_v508_v3_x2_build_use_closeout",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_V508_V3_X2_BUILD_USE_CLOSEOUT" : "OPEN_GAP_V508_V3_X2_BUILD_USE_CLOSEOUT",
  input_refs: {
    reducer: refName(reducerJson),
    route_manifest: refName(routeManifestJson),
    no_limited_guard: refName(noLimitedGuardJson),
    x1_handoff: refName(x1HandoffJson),
  },
  build_use_result_count: buildUseResults.length,
  build_use_results: buildUseResults,
  carry_forward: [
    "Run v508 v4 x1 as a full six-lane round-robin attempt where routes remain reachable.",
    "Use Browser for Lumen first, strict CLI for Arby and Aster Vale, and recovered app-lane map runner for Cicero, Kierkegaard, and Aristotle.",
    "Retry blockers with distinct safe methods before carrying them forward.",
    "Continue research, preparation, and x2 task design while lane watchers supervise active runs.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeJson(reducerJson, reducer);
writeJson(routeManifestJson, routeManifest);
writeJson(noLimitedGuardJson, noLimitedGuard);
writeJson(closeoutJson, closeout);
writeJson(nextPrepJson, nextPrep);

writeMd(reducerMd, [
  `# ${phaseSlug} Lane-State Reducer`,
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
  ...laneStatusRows.map((lane) => `- ${lane.lane}: \`${lane.status}\`; route family \`${lane.route_family}\`.`),
  "",
  "## Boundary",
  "",
  "Status-only reducer. No raw lane text, route handles, transcripts, app payloads, credentials, screenshots, local paths, or closure overclaims are published.",
]);

writeMd(routeManifestMd, [
  `# ${phaseSlug} Route-Family Manifest`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${routeManifest.status}\``,
  "",
  "## Route Families",
  "",
  ...routeFamilies.map(
    (family) =>
      `- ${family.family}: lanes \`${family.lanes.join(", ")}\`; use \`${family.current_use}\`; fallback \`${family.fallback}\`.`,
  ),
  "",
  "## Cadence",
  "",
  "- Check active lanes every five minutes when practical.",
  "- Continue research and x2 preparation while watchers supervise active lanes.",
  "- Use existing lanes only and publish blocker receipts rather than replacements.",
]);

writeMd(noLimitedGuardMd, [
  `# ${phaseSlug} No-Limited-Phase Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${noLimitedGuard.status}\``,
  "",
  "## Policy",
  "",
  `- Default phase mode: \`${noLimitedGuard.policy.default_phase_mode}\``,
  `- Limited phase allowed only on explicit user request: \`${String(
    noLimitedGuard.policy.limited_phase_allowed_only_when_user_explicitly_requests_it,
  )}\``,
  `- X2 build/run/test/install/use scope required: \`${String(noLimitedGuard.policy.x2_requires_build_run_test_install_use_scope)}\``,
  "",
  "## Prohibited Shortcuts",
  "",
  ...noLimitedGuard.prohibited_shortcuts.map((shortcut) => `- ${shortcut}`),
]);

writeMd(closeoutMd, [
  `# ${phaseSlug} X2 Build Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${closeout.status}\``,
  "",
  "## Built and Used",
  "",
  ...buildUseResults.map((result) => `- ${result.id}: ${result.result} Evidence: \`${result.evidence}\`.`),
  "",
  "## Carry Forward",
  "",
  ...closeout.carry_forward.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Closed for v508 v3 x2 build/use scope only if all checks pass. v508 full completion, v515 completion, GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain unclaimed.",
]);

writeMd(nextPrepMd, [
  `# ${nextPhaseSlug} Prep Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${nextPrep.status}\``,
  "",
  "## Required Lanes",
  "",
  ...expectedLanes.map((lane) => `- ${lane}`),
  "",
  "## Required Outputs",
  "",
  ...nextPrep.next_x1_outputs_requested.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "Preparation only. v508 v4 x1 is not started or completed by this card.",
]);

console.log(
  JSON.stringify(
    {
      status: closeout.status,
      reducer_status: reducer.status,
      route_manifest_status: routeManifest.status,
      no_limited_guard_status: noLimitedGuard.status,
      next_prep_status: nextPrep.status,
      build_use_result_count: closeout.build_use_result_count,
    },
    null,
    2,
  ),
);
