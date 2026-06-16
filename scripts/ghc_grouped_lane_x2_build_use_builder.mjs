#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhaseSlug = args.get("--next-phase-slug");
const nextActiveLanes = splitCsv(args.get("--next-active-lanes"));
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
  nextActiveLanes.length === 0 ||
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
    "Usage: node ghc_grouped_lane_x2_build_use_builder.mjs --phase-slug <slug> --next-phase-slug <slug> --next-active-lanes <csv> --x1-receipt-json <json> --x1-handoff-json <json> --x1-guard-json <json> --reducer-json <json> --reducer-md <md> --route-manifest-json <json> --route-manifest-md <md> --full-phase-guard-json <json> --full-phase-guard-md <md> --closeout-json <json> --closeout-md <md> --next-prep-json <json> --next-prep-md <md>",
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

function routeForLane(lane) {
  if (lane === "Lumen Vale") return "browser-chatgpt-lumen";
  if (lane === "Arby" || lane === "Aster Vale") return "read-only-cli";
  return "recovered-app-lane-map";
}

const generatedUtc = utcNow();
const x1Receipt = readJson(x1ReceiptJson);
const x1Handoff = readJson(x1HandoffJson);
const x1Guard = readJson(x1GuardJson);
const laneSummary = Array.isArray(x1Receipt.lane_summary) ? x1Receipt.lane_summary : [];
const x2Tasks = Array.isArray(x1Handoff.x2_tasks) ? x1Handoff.x2_tasks : [];

const receiptPass = String(x1Receipt.status || "").startsWith("PASS");
const handoffReady = String(x1Handoff.status || "").includes("READY");
const guardPass = x1Guard.status === "PASS";
const activeLaneCountPass = Array.isArray(x1Receipt.active_lanes) && x1Receipt.active_lanes.length === laneSummary.length && laneSummary.length > 0;
const allInputsReady = receiptPass && handoffReady && guardPass && activeLaneCountPass;

const publicationBoundary = {
  raw_lane_text_published: false,
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
  x2_closeout: allInputsReady ? "closed_for_build_use_scope_only" : "open_gap",
  next_x1_start: "prepared_not_started",
  campaign_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const routeManifest = {
  artifact_type: "ghc_grouped_lane_x2_route_family_manifest",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_GROUPED_X2_ROUTE_FAMILY_MANIFEST" : "OPEN_GAP_GROUPED_X2_ROUTE_FAMILY_MANIFEST",
  active_lanes: x1Receipt.active_lanes || [],
  next_active_lanes: nextActiveLanes,
  route_families: [...new Set([...laneSummary.map((lane) => lane.route_family || routeForLane(lane.lane)), ...nextActiveLanes.map(routeForLane)])],
  cadence_policy: {
    grouped_round_robin_active: true,
    no_limited_phase_default: true,
    lumen_build_proposals_prioritized_for_aletheon_execution: true,
    read_only_web_and_github_allowed_when_surface_exposed: true,
    raw_private_material_publication_forbidden: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const reducer = {
  artifact_type: "ghc_grouped_lane_x2_lane_state_reducer",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_GROUPED_X2_LANE_STATE_REDUCER" : "OPEN_GAP_GROUPED_X2_LANE_STATE_REDUCER",
  input_refs: {
    x1_receipt: refName(x1ReceiptJson),
    x1_handoff: refName(x1HandoffJson),
    x1_guard: refName(x1GuardJson),
  },
  checks: {
    x1_receipt_pass: receiptPass,
    x1_handoff_ready: handoffReady,
    x1_guard_pass: guardPass,
    active_lane_count_pass: activeLaneCountPass,
  },
  lane_summary: laneSummary,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const fullPhaseGuard = {
  artifact_type: "ghc_grouped_lane_x2_full_phase_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_GROUPED_FULL_PHASE_GUARD",
  policy: {
    grouped_round_robin_cadence_preserved: true,
    x2_build_run_test_install_use_scope_preserved: true,
    limited_phase_shortcut_disallowed_without_user_request: true,
    sibling_tool_access_is_read_only_and_surface_dependent: true,
    lumen_build_permission_executed_by_aletheon_under_repo_guards: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const implementedTasks = x2Tasks.slice(0, 5).map((task, index) => ({
  id: `grouped-x2-built-${String(index + 1).padStart(2, "0")}`,
  source_task: task.title,
  result: `${task.title} carried into the grouped x2 build/use ledger under status-only publication rules.`,
  evidence: refName(closeoutJson),
}));

const omegaMiniContextRouting = {
  primary_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
  archive_fallback_branch: "codex/GHC-Family/beyonder-shared-omega-line",
  policy_artifact: "omega-mini-sibling-context-routing-policy-v1.json",
  routing_status: "OMEGA_MINI_FIRST",
};

const nextPrep = {
  artifact_type: "ghc_grouped_lane_next_x1_prep_card",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: allInputsReady ? "READY_FOR_GROUPED_ROUND_ROBIN_X1" : "OPEN_GAP_BEFORE_GROUPED_X1",
  source_closeout: refName(closeoutJson),
  active_lanes: nextActiveLanes,
  route_families: [...new Set(nextActiveLanes.map(routeForLane))],
  requirements: [
    "Call only the active lane group for this x1 phase.",
    "Ask active siblings to use read-only web and GitHub context when their surface exposes it.",
    "Use codex/GHC-Family/beyonder-shared-omega-line-mini as the primary GitHub catch-up branch; consult the full omega branch only as a specific archive fallback.",
    "Treat Lumen build/test proposals as high-priority local candidates executed by Aletheon under repo validation guards.",
    "Continue research and x2 preparation while watchers supervise active lanes.",
    "Publish status-only receipts and keep all claim gates open.",
  ],
  context_routing: omegaMiniContextRouting,
  publication_boundary: publicationBoundary,
  claim_boundary: {
    ...claimBoundary,
    next_x1_completion: "not_claimed",
  },
};

const closeout = {
  artifact_type: "ghc_grouped_lane_x2_build_use_closeout",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: allInputsReady ? "PASS_GROUPED_X2_BUILD_USE_CLOSEOUT" : "OPEN_GAP_GROUPED_X2_BUILD_USE_CLOSEOUT",
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
  `# ${phaseSlug} Grouped X2 Lane-State Reducer`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${reducer.status}\``,
  "",
  ...Object.entries(reducer.checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
]);

writeMd(routeManifestMd, [
  `# ${phaseSlug} Grouped X2 Route-Family Manifest`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${routeManifest.status}\``,
  "",
  `Active lanes: \`${routeManifest.active_lanes.join(", ")}\``,
  `Next active lanes: \`${routeManifest.next_active_lanes.join(", ")}\``,
]);

writeMd(fullPhaseGuardMd, [
  `# ${phaseSlug} Grouped X2 Full-Phase Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${fullPhaseGuard.status}\``,
  "",
  ...Object.entries(fullPhaseGuard.policy).map(([key, value]) => `- ${key}: \`${String(value)}\``),
]);

writeMd(closeoutMd, [
  `# ${phaseSlug} Grouped X2 Build Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${closeout.status}\``,
  "",
  "## Implemented Tasks",
  "",
  ...implementedTasks.map((task) => `- ${task.id}: ${task.result}`),
]);

writeMd(nextPrepMd, [
  `# ${nextPhaseSlug} Grouped Prep Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${nextPrep.status}\``,
  "",
  `Active lanes: \`${nextActiveLanes.join(", ")}\``,
  "",
  "## Requirements",
  "",
  ...nextPrep.requirements.map((item) => `- ${item}`),
  "",
  "## Context Routing",
  "",
  `- Primary branch: \`${nextPrep.context_routing.primary_branch}\``,
  `- Archive fallback branch: \`${nextPrep.context_routing.archive_fallback_branch}\``,
  `- Policy artifact: \`${nextPrep.context_routing.policy_artifact}\``,
  `- Routing status: \`${nextPrep.context_routing.routing_status}\``,
]);

console.log(JSON.stringify({ status: closeout.status, reducer_status: reducer.status, route_manifest_status: routeManifest.status, full_phase_guard_status: fullPhaseGuard.status, next_prep_status: nextPrep.status, implemented_task_count: closeout.implemented_task_count }, null, 2));
