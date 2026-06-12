#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const readOnlyJson = args.get("--read-only-json");
const sourceReviewJson = args.get("--source-review-json");
const gmutMindJson = args.get("--gmut-mind-json");
const compactJson = args.get("--compact-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !readOnlyJson || !sourceReviewJson || !gmutMindJson || !compactJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_x1_x2_eureka_approval_bridge_builder.mjs --phase-slug <slug> --read-only-json <json> --source-review-json <json> --gmut-mind-json <json> --compact-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const readOnly = readJson(readOnlyJson);
const sourceReview = readJson(sourceReviewJson);
const gmutMind = readJson(gmutMindJson);
const compact = readJson(compactJson);
const generatedUtc = utcNow();

const approvalCandidates = [
  {
    id: "approval-01-lane-refresh-retry-pack",
    title: "Read-only lane refresh retry pack",
    status: "PENDING_USER_APPROVAL",
    scope: "Run bounded read-only refresh attempts for Arby, Cicero, Kierkegaard, and Aristotle without replacement lanes.",
    x2_use: "Generate blocker receipts or current-evidence receipts that can feed the next phase gate.",
  },
  {
    id: "approval-02-gmut-model-comparison-caution-card",
    title: "GMUT model-comparison caution card",
    status: "PENDING_USER_APPROVAL",
    scope: "Separate hypotheses, datasets, likelihood assumptions, observations, and speculative synthesis for GMUT-mind work.",
    x2_use: "Build a caution validator that rejects closure language unless every dataset gate is explicitly satisfied.",
  },
  {
    id: "approval-03-vision-card-refresh-pack",
    title: "Vision and compact-refresh card pack",
    status: "PENDING_USER_APPROVAL",
    scope: "Create a compact phase-start card that binds lane state, source state, runner state, and open gates.",
    x2_use: "Use the card as the first artifact every future compact refresh consults.",
  },
  {
    id: "approval-04-runner-provenance-map",
    title: "Runner provenance map",
    status: "PENDING_USER_APPROVAL",
    scope: "Map current Node entrypoints to their inputs, outputs, guard receipts, and intended phase use.",
    x2_use: "Prevent older helpers from accidentally becoming the default path when newer validated runners exist.",
  },
  {
    id: "approval-05-official-source-decision-map",
    title: "Official-source decision map",
    status: "PENDING_USER_APPROVAL",
    scope: "Map the 30 reviewed source rows and 13 GMUT rows into concrete lane, runner, prompt, and guard decisions.",
    x2_use: "Turn source research into build decisions instead of leaving it as passive reading.",
  },
  {
    id: "approval-06-sibling-prompt-contract-refresh",
    title: "Sibling prompt contract refresh",
    status: "PENDING_USER_APPROVAL",
    scope: "Create current x1 prompt templates for Lumen, Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle.",
    x2_use: "Ensure each lane receives phase slug, read-only boundary, expected marker, and blocker fallback.",
  },
  {
    id: "approval-07-x2-build-smoke-suite",
    title: "X2 build smoke suite",
    status: "PENDING_USER_APPROVAL",
    scope: "Create a smoke suite for generated ledgers, guards, and future x2 build artifacts.",
    x2_use: "Run script checks, JSON parse, exposure, overclaim, replacement, and private-material scans with one Node entrypoint.",
  },
  {
    id: "approval-08-future-source-gate-ledger",
    title: "Future-source gate ledger",
    status: "PENDING_USER_APPROVAL",
    scope: "Track future DESI, Euclid, LVK, LHC, and other release gates that must remain open until public evidence exists.",
    x2_use: "Prevent phase language from treating expected future data as current evidence.",
  },
  {
    id: "approval-09-dual-branch-publication-health",
    title: "Dual-branch publication health check",
    status: "PENDING_USER_APPROVAL",
    scope: "Create a lightweight pre-push checker for the two omega branches and exact-staging rules.",
    x2_use: "Reduce repeated manual drift checks while preserving safety boundaries.",
  },
  {
    id: "approval-10-ghc-multiplex-ipc-bus-design-card",
    title: "GHC multiplex IPC bus design card",
    status: "PENDING_USER_APPROVAL",
    scope: "Draft the next implementation-safe design for a local multiplex bus across Browser, CLI, app-server, and future connectors.",
    x2_use: "Turn route-family lessons into a buildable adapter interface without touching private app state.",
  },
];

const eurekaTasks = [
  ["eureka-01", "Build a source-to-runner trace matrix", "Map every official-source row to one runner or guard decision."],
  ["eureka-02", "Build a GMUT caution validator", "Reject closure wording unless a future artifact explicitly proves each physics gate."],
  ["eureka-03", "Build a lane readiness reducer", "Condense lane receipts into completed, pending, blocked, and standby buckets."],
  ["eureka-04", "Build a compact card self-test", "Verify compact-refresh cards contain lane, source, runner, and claim boundaries."],
  ["eureka-05", "Build a prompt contract linter", "Check sibling prompts for phase slug, read-only scope, marker, and blocker fallback."],
  ["eureka-06", "Build an x2 smoke command", "Run all current validation commands from one Node entrypoint."],
  ["eureka-07", "Build a future-source calendar ledger", "Record future public data releases as open evidence gates."],
  ["eureka-08", "Build a route-family manifest", "Make Browser, CLI, app-server, Chrome fallback, and connector roles explicit."],
  ["eureka-09", "Build a guard receipt index", "Index all v508 guard receipts by artifact, status, and claim boundary."],
  ["eureka-10", "Build a source balance report", "Compare GMUT, THOS, and Freed ID source coverage by phase."],
  ["eureka-11", "Build a no-private-map detector", "Flag artifacts that imply hidden route maps or private identifier dependence."],
  ["eureka-12", "Build a runner freshness board", "Classify helpers as current, fallback, legacy, or pending review."],
  ["eureka-13", "Build a dual-branch drift preflight", "Package fetch and remote-equals-local checks into a status-only receipt."],
  ["eureka-14", "Build a lane retry receipt template", "Standardize retry count, blocker reason, and no-replacement evidence."],
  ["eureka-15", "Build a phase-start gate dashboard", "Summarize allowed movement and blocked claims without raw logs."],
  ["eureka-16", "Build a Journey document pointer map", "List relevant Journey docs as curated references without copying private text."],
  ["eureka-17", "Build a plugin-surface hold ledger", "Track plugin-cache, user-skill, and account mutations as approval-gated only."],
  ["eureka-18", "Build an x1-to-x2 handoff composer", "Turn x1 research outputs into x2 build tasks with validation requirements."],
  ["eureka-19", "Build a source-host allowlist updater", "Keep official-source host checks explicit and reviewable."],
  ["eureka-20", "Build a v509 readiness preview", "Preview which gates must change before v509 can start without overclaiming v508."],
].map(([id, title, x2Action]) => ({
  id,
  title,
  status: "X2_BUILD_CANDIDATE",
  x1_input: "current v508 source, lane, compact-refresh, and GMUT-mind receipts",
  x2_action: x2Action,
  validation_required: ["script_check", "json_parse", "exposure_guard", "no_overclaim_guard", "no_replacement_guard", "private_material_scan"],
}));

const receipt = {
  artifact_type: "ghc_x1_x2_eureka_approval_bridge",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  read_only_input: readOnlyJson,
  source_review_input: sourceReviewJson,
  gmut_mind_input: gmutMindJson,
  compact_refresh_input: compactJson,
  status: "X1_TO_X2_EUREKA_APPROVAL_BRIDGE_READY_FOR_REVIEW",
  phase_state: compact.current_anchor?.phase_state || "limited_x1_preparation_only",
  active_lane_count: readOnly.active_lane_count,
  standby_lane_count: readOnly.standby_lane_count,
  open_or_pending_lane_count: readOnly.open_or_pending_lane_count,
  source_rows_reviewed: sourceReview.source_rows_reviewed,
  gmut_mind_deepening_rows: gmutMind.source_count_this_batch,
  approval_candidate_count: approvalCandidates.length,
  eureka_task_count: eurekaTasks.length,
  approval_candidates: approvalCandidates,
  eureka_tasks: eurekaTasks,
  next_actions: [
    "Present these approval candidates for future authorization; do not treat them as approved by this artifact.",
    "Use the eureka tasks as x2 build candidates after the relevant approval packet is active.",
    "Prefer Node entrypoints and current validated runners before older helpers.",
    "Keep open lane blockers and all empirical or canon gates visible until exact evidence changes them.",
  ],
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
    raw_user_text_published: false,
    copyrighted_source_dump_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    approval_activation: "not_claimed",
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} X1 to X2 Eureka Approval Bridge`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Phase state: \`${receipt.phase_state}\``,
  `Approval candidates: \`${receipt.approval_candidate_count}\``,
  `Eureka tasks: \`${receipt.eureka_task_count}\``,
  `Source rows reviewed: \`${receipt.source_rows_reviewed}\``,
  `GMUT-mind deepening rows: \`${receipt.gmut_mind_deepening_rows}\``,
  "",
  "## Approval Candidates",
  "",
  ...approvalCandidates.flatMap((candidate) => [
    `### ${candidate.id}: ${candidate.title}`,
    "",
    `Status: \`${candidate.status}\``,
    "",
    `Scope: ${candidate.scope}`,
    "",
    `X2 use: ${candidate.x2_use}`,
    "",
  ]),
  "## Eureka Tasks",
  "",
  ...eurekaTasks.map((task) => `- ${task.id}: ${task.title}. X2 action: ${task.x2_action}`),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "This bridge proposes approval candidates and x2 build tasks only. It does not activate approvals, claim phase completion, start v508 fully, close x2, complete source targets, validate GMUT empirically, solve final physics, prove consciousness, close legal claims, promote canon, publish lane text, or publish private material.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      approval_candidate_count: receipt.approval_candidate_count,
      eureka_task_count: receipt.eureka_task_count,
      phase_state: receipt.phase_state,
    },
    null,
    2,
  ),
);
